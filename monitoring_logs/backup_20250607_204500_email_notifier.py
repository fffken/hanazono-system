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
    # クラッシュを防ぐためのダミー関数を定義
    def get_weather_forecast():
        logging.warning("ダミーの天気予報データを返します。")
        return None

try:
    from season_detector import get_current_season, get_detailed_season
    SEASON_DETECTOR_AVAILABLE = True
except ImportError:
    logging.warning("season_detector.pyが見つかりません。季節はダミーデータを使用します。")
    SEASON_DETECTOR_AVAILABLE = False
    # クラッシュを防ぐためのダミー関数を定義
    def get_current_season(): return "spring_fall"
    def get_detailed_season(): return "spring_mid"
# --- インポートここまで ---

def expand_env_vars(config):
    """環境変数を展開する"""
    if isinstance(config, dict):
        return {k: expand_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [expand_env_vars(i) for i in config]
    elif isinstance(config, str):
        return os.path.expandvars(config)
    return config

class EnhancedEmailNotifier:
    def __init__(self, config, logger=None):
        self.config = expand_env_vars(config)
        self.logger = logger if logger else logging.getLogger('email_notifier_v2')
        self.db_path = os.path.join(self.config.get('files', {}).get('data_directory', 'data'), 'solar_data.db')
        
        if SETTINGS_RECOMMENDER_AVAILABLE:
            self.recommender = SettingsRecommender(self.config)
        else:
            self.recommender = None

    def get_weather_forecast_3days(self):
        """3日分の天気予報を取得"""
        try:
            weather_data = get_weather_forecast()
            if weather_data and isinstance(weather_data, list) and len(weather_data) >= 3:
                forecast_3days = {
                    "today": weather_data[0],
                    "tomorrow": weather_data[1],
                    "day_after_tomorrow": weather_data[2]
                }
                return forecast_3days
        except Exception as e:
            self.logger.warning(f"天気予報取得処理でエラー: {e}")
        
        # フォールバック用の仮データ
        return {
            "today": {"weather": "不明", "temp_max": 25, "temp_min": 15},
            "tomorrow": {"weather": "不明", "temp_max": 25, "temp_min": 15},
            "day_after_tomorrow": {"weather": "不明", "temp_max": 25, "temp_min": 15},
        }

    def get_current_battery_status(self):
        # このメソッドはダミー実装のままです
        return {"soc": 69, "voltage": 54.2, "current": 5.1}

    def get_24h_battery_pattern(self):
        # このメソッドはダミー実装のままです
        return {"07:00": 46, "12:00": 51, "18:00": 57, "23:00": 39, "現在": 69}

    def calculate_daily_achievement(self):
        # このメソッドはダミー実装のままです
        return {"solar_generation": {"current": 10.5, "target": 12.0}}

    def calculate_cost_savings(self):
        # このメソッドはダミー実装のままです
        return {"daily": 150, "monthly_total": 4500}

    def _generate_bar(self, current, target):
        """シンプルなテキストバーを生成"""
        if target == 0: return "N/A"
        percentage = min(100, int(current / target * 100))
        filled = int(percentage / 10)
        empty = 10 - filled
        return f"[{'■' * filled}{'□' * empty}] {percentage}%"

    def _generate_email_content(self, weather_data, recommendation, battery_status,
                                  battery_pattern, achievement, cost_savings):
        """メール本文を生成"""
        content = []
        # ここでは簡略化した内容を生成します
        content.append("--- HANAZONOシステム 日次レポート ---")
        content.append(f"\n【天気予報】")
        content.append(f"本日: {weather_data['today']['weather']}")
        content.append(f"\n【推奨設定】")
        if recommendation:
            content.append(f"充電電流: {recommendation['charge_current']}A, 充電時間: {recommendation['charge_time']}分, SOC: {recommendation['soc']}%")
        else:
            content.append("推奨設定はありません。")

        content.append(f"\n【バッテリー状況】")
        content.append(f"現在のSOC: {battery_status['soc']}%")

        footer = self.config.get('template', {}).get('footer', '')
        content.append(f"\n{footer}")
        return '\n'.join(content)

    def send_daily_report(self, data, test_mode=False):
        """日次レポートを送信"""
        try:
            smtp_conf = self.config
            if not all([smtp_conf.get(k) for k in ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'email_sender', 'email_recipients']]):
                self.logger.error('メール設定が不完全です')
                return False

            if test_mode:
                self.logger.info("テストモードのため、メール送信をスキップしました。")
                self.logger.info(f"件名: 🟣 HANAZONOシステム最適化レポート {datetime.now().strftime('%Y年%m月%d日')} (テスト)")
                return True

            weather_data = self.get_weather_forecast_3days()
            recommendation = self.recommender.recommend_settings(weather_data, "typeA") if self.recommender else None
            battery_status = self.get_current_battery_status()
            battery_pattern = self.get_24h_battery_pattern()
            achievement = self.calculate_daily_achievement()
            cost_savings = self.calculate_cost_savings()
            
            subject = self.config.get('template', {}).get('subject', 'システムレポート').format(timestamp=datetime.now().strftime('%Y-%m-%d'))
            content = self._generate_email_content(weather_data, recommendation, battery_status, battery_pattern, achievement, cost_savings)

            msg = MIMEMultipart()
            msg['From'] = smtp_conf['email_sender']
            msg['To'] = ", ".join(smtp_conf['email_recipients'])
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            server = smtplib.SMTP(smtp_conf['smtp_server'], smtp_conf['smtp_port'])
            server.starttls()
            server.login(smtp_conf['smtp_user'], smtp_conf['smtp_password'])
            server.sendmail(smtp_conf['email_sender'], smtp_conf['email_recipients'], msg.as_string())
            server.quit()

            self.logger.info(f'最適化レポートを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}', exc_info=True)
            return False

def test_email_system():
    """メールシステムのテスト"""
    print("📧 Enhanced Email System v2.2 テスト開始")
    print("=" * 60)
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        email_config = settings.get('email', {})
    except Exception as e:
        print(f"⚠️ 設定読み込みエラー: {e}")
        email_config = {}

    notifier = EnhancedEmailNotifier(email_config)
    success = notifier.send_daily_report({}, test_mode=True)

    if success:
        print("\n✅ メールシステムテスト完了")
    else:
        print("\n❌ メールシステムテスト失敗")

if __name__ == "__main__":
    test_email_system()
