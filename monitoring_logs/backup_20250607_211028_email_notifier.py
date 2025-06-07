import os
import sys
import json
import sqlite3
import smtplib
import logging
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ロギングの基本設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- 依存モジュールの安全なインポート ---
try:
    from settings_recommender import SettingsRecommender
    SETTINGS_RECOMMENDER_AVAILABLE = True
except ImportError:
    logging.warning("settings_recommender.pyが見つかりません。推奨設定機能は無効です。")
    SETTINGS_RECOMMENDER_AVAILABLE = False

try:
    from weather_forecast import get_weather_forecast
    WEATHER_FORECAST_AVAILABLE = True
except ImportError:
    logging.warning("weather_forecast.pyが見つかりません。天気予報はダミーデータを使用します。")
    WEATHER_FORECAST_AVAILABLE = False
    def get_weather_forecast():
        logging.warning("ダミーの天気予報データを返します。")
        return None

try:
    from season_detector import get_current_season, get_detailed_season
    SEASON_DETECTOR_AVAILABLE = True
except ImportError:
    logging.warning("season_detector.pyが見つかりません。季節はダミーデータを使用します。")
    SEASON_DETECTOR_AVAILABLE = False
    def get_current_season(): return "spring_fall"
    def get_detailed_season(): return "spring_mid"
# --- インポートここまで ---

def expand_env_vars(config):
    """設定辞書内の環境変数を再帰的に展開する"""
    if isinstance(config, dict):
        return {k: expand_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [expand_env_vars(i) for i in config]
    elif isinstance(config, str):
        return os.path.expandvars(config)
    return config

class EnhancedEmailNotifier:
    def __init__(self, settings, logger=None):
        self.settings = expand_env_vars(settings)
        self.email_config = self.settings.get('email', {})
        self.logger = logger if logger else logging.getLogger('email_notifier_v2')
        self.db_path = os.path.join(self.settings.get('files', {}).get('data_directory', 'data'), 'solar_data.db')
        
        if SETTINGS_RECOMMENDER_AVAILABLE:
            self.recommender = SettingsRecommender(self.settings)
        else:
            self.recommender = None

    def get_weather_forecast_3days(self):
        """3日分の天気予報を取得。エラー発生時はフォールバック"""
        try:
            if WEATHER_FORECAST_AVAILABLE:
                weather_data = get_weather_forecast()
                if isinstance(weather_data, list) and len(weather_data) >= 3:
                    return {
                        "today": weather_data[0],
                        "tomorrow": weather_data[1],
                        "day_after_tomorrow": weather_data[2]
                    }
        except Exception as e:
            self.logger.warning(f"天気予報取得処理でエラー: {e}")
        
        return {
            "today": {"weather": "不明", "temp_max": 0, "temp_min": 0},
            "tomorrow": {"weather": "不明", "temp_max": 0, "temp_min": 0},
            "day_after_tomorrow": {"weather": "不明", "temp_max": 0, "temp_min": 0},
        }

    # 以下、ダミーのデータ取得メソッド群
    def get_current_battery_status(self): return {"soc": 0, "voltage": 0, "current": 0}
    def get_24h_battery_pattern(self): return {}
    def calculate_daily_achievement(self): return {"solar_generation": {"current": 0, "target": 0}}
    def calculate_cost_savings(self): return {"daily": 0, "monthly_total": 0}

    def _generate_email_content(self, weather_data, recommendation, **kwargs):
        """メール本文を生成"""
        content = ["--- HANAZONOシステム 日次レポート ---"]
        content.append(f"\n【天気予報】\n本日: {weather_data['today']['weather']}")
        content.append("\n【推奨設定】")
        if recommendation:
            content.append(f"充電電流: {recommendation.get('charge_current')}A, 充電時間: {recommendation.get('charge_time')}分, SOC: {recommendation.get('soc')}%")
        else:
            content.append("推奨設定はありません。")
        footer = self.settings.get('notification', {}).get('email', {}).get('template', {}).get('footer', '')
        content.append(f"\n\n{footer}")
        return '\n'.join(content)

    def send_daily_report(self, data, test_mode=False):
        """日次レポートを送信"""
        try:
            if not self.email_config:
                self.logger.error('メール設定がsettings.json内に見つかりません。')
                return False
            
            required_keys = ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'email_sender', 'email_recipients']
            if not all(self.email_config.get(k) for k in required_keys):
                self.logger.error('メール設定が不完全です。必要なキーが不足しています。')
                return False

            if test_mode:
                subject = f"🟣 HANAZONOシステム最適化レポート {datetime.now().strftime('%Y年%m月%d日')} (テスト)"
                self.logger.info("テストモードのため、メール送信をスキップしました。")
                self.logger.info(f"件名: {subject}")
                return True

            weather_data = self.get_weather_forecast_3days()
            recommendation = self.recommender.recommend_settings(weather_data, "typeA") if self.recommender else None
            
            subject = self.email_config.get('template', {}).get('subject', 'システムレポート').format(timestamp=datetime.now().strftime('%Y-%m-%d'))
            content = self._generate_email_content(
                weather_data=weather_data,
                recommendation=recommendation
            )

            msg = MIMEMultipart()
            msg['From'] = self.email_config['email_sender']
            msg['To'] = ", ".join(self.email_config['email_recipients'])
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()

            self.logger.info(f'最適化レポートを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信で予期せぬエラー: {e}', exc_info=True)
            return False

def test_email_system():
    """メールシステムのテスト"""
    print("📧 Enhanced Email System v2.2 テスト開始")
    print("=" * 60)
    settings = {}
    try:
        # settings.jsonを丸ごと読み込む
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        print("⚠️ settings.jsonが見つかりません。テストを中止します。")
        return False
    except Exception as e:
        print(f"⚠️ 設定ファイル読み込みエラー: {e}")
        return False
    
    # クラスにはsettings全体を渡す
    notifier = EnhancedEmailNotifier(settings)
    success = notifier.send_daily_report({}, test_mode=True)

    if success:
        print("\n✅ メールシステムテスト完了")
    else:
        print("\n❌ メールシステムテスト失敗")
    return success

if __name__ == "__main__":
    test_email_system()
