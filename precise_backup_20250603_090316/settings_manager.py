import logging
import json
import os
import sys
import re # 環境変数展開のために追加

# グローバルロガーインスタンスへの参照を試みる
# main.py などで _hanazono_logger_instance が設定されることを期待
_logger = None
try:
    # mainモジュールからロガーを取得しようと試みる
    if hasattr(sys.modules.get('__main__'), '_hanazono_logger_instance'):
        _logger = sys.modules.get('__main__')._hanazono_logger_instance
    if _logger is None: # それでもNoneなら、標準のロガーを使うか、printにする
        _logger = logging.getLogger(__name__) # このモジュール用のロガー
        # _logger.warning("メインロガーが見つからず、SettingsManager専用ロガーを使用します。") # 必要なら警告
except Exception:
    _logger = logging.getLogger(__name__) # フォールバック

class SettingsManager:
    """設定を一元管理するクラス"""
    _instance = None
    _settings = None
    _settings_file_path = None # 設定ファイルのフルパスを保持

    def __new__(cls, settings_file="""settings.json"""): # settings_fileを引数に取るように変更
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            # __init__ で初期化するように変更
        return cls._instance

    def __init__(self, settings_file="settings.json"):
        # シングルトンで初回のみロード
        if self._settings is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self._settings_file_path = os.path.join(base_dir, settings_file)
            self._load_settings()

    def _expand_env_vars_recursive(self, item):
        """設定データ内の環境変数プレースホルダーを再帰的に展開する"""
        if isinstance(item, dict):
            return {k: self._expand_env_vars_recursive(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._expand_env_vars_recursive(i) for i in item]
        elif isinstance(item, str):
            # ${VAR_NAME} 形式のプレースホルダーを検索し置換
            def replace_match(match):
                var_name = match.group(1)
                # 環境変数の値を取得。見つからなければ元の文字列 (プレースホルダー全体) を返す
                return os.environ.get(var_name, match.group(0))
            
            return re.sub(r"""\$\{(\w+)\}""", replace_match, item)
        return item

    def _load_settings(self):
        """設定ファイルを読み込み、環境変数を展開する"""
        try:
            with open(self._settings_file_path, 'r', encoding='utf-8') as f:
                raw_settings = json.load(f)
            
            # 環境変数を展開
            self._settings = self._expand_env_vars_recursive(raw_settings)
            
            # print('設定ファイルを読み込み、環境変数を展開しました。') # ログはmain.py等に任せるか、loggerを使う
            if _logger:
                _logger.info(f"""設定ファイル '{self._settings_file_path}' を読み込み、環境変数を展開しました。""")
            else:
                print(f"設定ファイル '{self._settings_file_path}' を読み込み、環境変数を展開しました。 (ロガー利用不可)")

        except FileNotFoundError:
            if _logger:
                _logger.error(f"設定ファイルが見つかりません: {self._settings_file_path}")
            else:
                print(f"設定ファイルが見つかりません: {self._settings_file_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            if _logger:
                _logger.error(f"設定ファイル ({self._settings_file_path}) のJSONフォーマットが不正です。")
            else:
                print(f"設定ファイル ({self._settings_file_path}) のJSONフォーマットが不正です。")
            sys.exit(1)
        except Exception as e:
            if _logger:
                _logger.error(f"設定ファイル ({self._settings_file_path}) の読み込み中に予期せぬエラー: {e}", exc_info=True)
            else:
                print(f"設定ファイル ({self._settings_file_path}) の読み込み中に予期せぬエラー: {e}")
            sys.exit(1)

    def save_settings(self):
        """設定をファイルに保存する"""
        try:
            backup_path = f'{self._settings_file_path}.bak_{os.path.getpid()}' # プロセスIDで一時的なバックアップ
            try:
                if os.path.exists(self._settings_file_path):
                    os.rename(self._settings_file_path, backup_path) # 元ファイルをリネームしてバックアップ
                    if _logger: _logger.info(f'設定ファイルのバックアップを作成: {backup_path}')
                else: # 元ファイルがない場合はバックアップなし
                    backup_path = None 
            except Exception as e:
                if _logger: _logger.warning(f'バックアップ作成/リネームエラー: {str(e)}')
                backup_path = None # バックアップ失敗

            with open(self._settings_file_path, 'w', encoding='utf-8') as f:
                # 保存する際は展開前のプレースホルダーを保存したい場合、工夫が必要。
                # ここでは現在の _settings (展開済み) を保存。
                # 展開前のデータを保持しておき、それを保存するのが理想。
                # 今回の課題は読み込み時の展開なので、保存は現状維持とします。
                json.dump(self._settings, f, ensure_ascii=False, indent=2)
            
            if _logger: _logger.info('設定ファイルを保存しました')
            if backup_path and os.path.exists(backup_path): # 成功したら古いバックアップは消してもよいが、ここでは残す
                pass
            return True
        except Exception as e:
            if _logger: _logger.error(f'設定ファイルの保存エラー: {str(e)}', exc_info=True)
            # 保存に失敗した場合、バックアップから復元を試みる
            if backup_path and os.path.exists(backup_path):
                try:
                    os.rename(backup_path, self._settings_file_path)
                    if _logger: _logger.info(f'保存失敗のため、{backup_path} から設定を復元しました。')
                except Exception as e_restore:
                    if _logger: _logger.error(f'バックアップからの復元失敗: {str(e_restore}')
            return False

    def get_inverter_parameters(self):
        return self._settings.get('inverter_parameters', {})

    def get_season_settings(self, season, setting_type):
        detailed_map = self._settings.get('detailed_seasonal_settings', {})
        basic_season = detailed_map.get(season, {}).get('reference', season)
        seasonal_settings = self._settings.get('seasonal_settings', {})
        season_data = seasonal_settings.get(basic_season, {})
        return season_data.get(setting_type, {})

    def get_weather_icon(self, weather_description):
        weather_icons = self._settings.get('weather_icons', {})
        for key, icon in weather_icons.items():
            if key in weather_description:
                return icon
        return '🌐' # Default icon

    def get_season_icon(self, season):
        return self._settings.get('season_icons', {}).get(season, '🌐')

    def get_email_config(self): # メール設定全体を返すように変更
        return self._settings.get('notification', {}).get('email', {})

    # is_email_enabled, get_email_template は get_email_config() を使うように変更可能
    # または、直接アクセスも維持する

    def is_email_enabled(self):
        return self.get_email_config().get('enabled', False)

    def get_email_template(self):
        return self.get_email_config().get('template', {})
        
    def is_line_enabled(self):
        return self._settings.get('notification', {}).get('line', {}).get('enabled', False)

    def get_line_template(self):
        return self._settings.get('notification', {}).get('line', {}).get('template', {})

    def update_season_settings(self, season, setting_type, new_values):
        detailed_map = self._settings.get('detailed_seasonal_settings', {})
        basic_season = detailed_map.get(season, {}).get('reference', season)
        if basic_season in self._settings.get('seasonal_settings', {}):
            if setting_type in self._settings['seasonal_settings'][basic_season]:
                self._settings['seasonal_settings'][basic_season][setting_type].update(new_values)
                return True
        return False

    def get_weather_connectors(self):
        return self._settings.get('weather_connectors', ['　後　', '　のち　', '　時々　', '　一時　', '　夜　', '　夜遅く　', '　所により　', '　で　', '　から　', '　または　'])

    def get(self, key, default=None):
        """設定階層をドット区切りで指定して値を取得 (例: 'notification.email.smtp_port')"""
        keys = key.split('.')
        val = self._settings
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    @property
    def settings(self):
        """ロードされ、環境変数が展開された設定への直接アクセスを提供します。"""
        if self._settings is None: # まだロードされていない場合（通常は__init__でロードされる）
            self._load_settings()
        return self_settings

# グローバルインスタンス (シングルトン)
# settings_manager = SettingsManager() # アプリケーションのどこかで一度だけ初期化
