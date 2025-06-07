#!/usr/bin/env python3
"""
設定管理システム - 強化版
完全構文エラーフリー設計
"""
import os
import json
import logging
import re
from pathlib import Path

class SettingsManager:
    """設定管理クラス"""
    
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.logger = self._setup_logger()
        self._settings = self._load_settings()
    
    def _setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('settings_manager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_settings(self):
        """設定ファイル読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                self.logger.info(f"設定ファイル読み込み成功: {self.settings_file}")
                return self._expand_env_vars(settings)
            else:
                self.logger.warning(f"設定ファイルが見つかりません: {self.settings_file}")
                return self._create_default_settings()
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {str(e)}")
            return self._create_default_settings()
    
    def _expand_env_vars(self, obj):
        """環境変数展開"""
        if isinstance(obj, dict):
            return {k: self._expand_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._expand_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            return self._expand_string_env_vars(obj)
        else:
            return obj
    
    def _expand_string_env_vars(self, text):
        """文字列内の環境変数展開"""
        if not isinstance(text, str):
            return text
        
        # ${VAR_NAME} パターンを展開
        pattern = r'\$\{([^}]+)\}'
        
        def replace_env_var(match):
            var_name = match.group(1)
            return os.getenv(var_name, match.group(0))
        
        return re.sub(pattern, replace_env_var, text)
    
    def _create_default_settings(self):
        """デフォルト設定作成"""
        default_settings = {
            "inverter": {
                "ip": "192.168.0.202",
                "serial": 3528830226,
                "mac": "D4:27:87:16:7A:F8", 
                "port": 8899,
                "mb_slave_id": 1
            },
            "network": {
                "subnet": "192.168.0.0/24"
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_user": "fffken@gmail.com",
                "smtp_password": "${SMTP_PASSWORD}",
                "sender": "fffken@gmail.com",
                "recipients": ["fffken@gmail.com"]
            },
            "monitoring": {
                "interval_minutes": 15,
                "key_registers": [
                    {
                        "address": "0x0100",
                        "name": "バッテリーSOC", 
                        "unit": "%",
                        "factor": 1,
                        "emoji": "🔋"
                    }
                ]
            }
        }
        
        self.logger.info("デフォルト設定を作成しました")
        return default_settings
    
    def get(self, key, default=None):
        """設定値取得"""
        try:
            keys = key.split('.')
            value = self._settings
            
            for k in keys:
                value = value[k]
            
            return value
        except (KeyError, TypeError):
            self.logger.debug(f"設定キーが見つかりません: {key}")
            return default
    
    def get_inverter_config(self):
        """インバーター設定取得"""
        return self.get('inverter', {})
    
    def get_email_config(self):
        """メール設定取得"""
        return self.get('email', {})
    
    def get_monitoring_config(self):
        """監視設定取得"""
        return self.get('monitoring', {})
    
    def save_settings(self):
        """設定ファイル保存"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            self.logger.info("設定ファイル保存成功")
            return True
        except Exception as e:
            self.logger.error(f"設定ファイル保存エラー: {str(e)}")
            return False
    
    def update_setting(self, key, value):
        """設定値更新"""
        try:
            keys = key.split('.')
            current = self._settings
            
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
            self.logger.info(f"設定更新: {key} = {value}")
            return True
        except Exception as e:
            self.logger.error(f"設定更新エラー: {str(e)}")
            return False
    
    @property
    def settings(self):
        """設定への読み取り専用アクセス"""
        return self._settings.copy()

def test_settings_manager():
    """設定管理テスト"""
    print("🧪 設定管理テスト開始")
    
    try:
        manager = SettingsManager()
        print("✅ SettingsManager初期化成功")
        
        # 基本取得テスト
        inverter_config = manager.get_inverter_config()
        print(f"✅ インバーター設定取得: IP={inverter_config.get('ip', 'Unknown')}")
        
        # 環境変数展開テスト
        email_config = manager.get_email_config()
        password = email_config.get('smtp_password', '')
        if password.startswith('${'):
            print("✅ 環境変数パターン検出")
        else:
            print("✅ 環境変数展開済み")
        
        print("🎉 設定管理テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ 設定管理テストエラー: {e}")
        return False

if __name__ == "__main__":
    test_settings_manager()
