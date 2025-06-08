import os
import sys
import json
import sqlite3
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 依存モジュールのインポート
sys.path.append('.') 
from weather_forecast import get_weather_forecast
from season_detector import get_current_season
from settings_recommender import SettingsRecommender
from lvyuan_collector import LVYUANCollector

class EnhancedEmailNotifier:
    def __init__(self, settings, logger=None):
        self.settings = settings
        self.email_config = self.settings.get('notification', {}).get('email', {})
        self.logger = logger if logger else logging.getLogger('email_diagnoser')
        self.logger.setLevel(logging.INFO)
        # ログハンドラが重複しないようにする
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
        self.recommender = SettingsRecommender(self.settings)
        self.db_path = os.path.join(self.settings.get('files', {}).get('data_directory', 'data'), 'solar_data.db')

    def get_weather_forecast_3days(self):
        self.logger.info("--- [1/6] 天気予報データ取得開始 ---")
        try:
            data = get_weather_forecast()
            self.logger.info("✅ 天気予報データ取得成功")
            return data
        except Exception as e:
            self.logger.error(f"❌ 天気予報データ取得エラー: {e}")
            return None

    def get_current_battery_status(self):
        self.logger.info("--- [2/6] 現在バッテリー状況取得開始 ---")
        try:
            collector = LVYUANCollector()
            data, _ = collector.collect_data()
            if data and data.get('parameters'):
                self.logger.info("✅ 現在バッテリー状況取得成功")
                return data['parameters']
            self.logger.warning("⚠️ バッテリーデータは収集できましたが、中身が期待通りではありません。")
            return None
        except Exception as e:
            self.logger.error(f"❌ 現在バッテリー状況取得エラー: {e}")
            return None

    def get_24h_battery_pattern(self):
        self.logger.info("--- [3/6] 24時間バッテリーパターン取得開始 ---")
        self.logger.warning("⚠️ 24時間パターン取得は現在ダミー実装です。")
        return {"07:00": 47, "23:00": 40, "現在": 69}

    def calculate_daily_achievement(self):
        self.logger.info("--- [4/6] 今日の達成状況計算開始 ---")
        self.logger.warning("⚠️ 達成状況計算は現在ダミー実装です。")
        return {"solar_generation": {"current": 10.5, "target": 12.0}, "battery_efficiency": 97.5}

    def calculate_1year_comparison(self):
        self.logger.info("--- [5/6] 1年前比較データ計算開始 ---")
        self.logger.warning("⚠️ 1年前比較は現在ダミー実装です。")
        return {"last_year_cost": 17157, "this_year_cost": 9200}
        
    def calculate_cost_savings(self):
        self.logger.info("--- [6/6] 電気代節約効果計算開始 ---")
        self.logger.warning("⚠️ 節約効果計算は現在ダミー実装です。")
        return {"today": 421, "monthly_forecast": 12630}

    def _generate_email_content(self, data):
        # この診断では本文生成は簡略化
        return f"データ収集サマリー:\n{json.dumps(data, indent=2, ensure_ascii=False)}"

    def send_daily_report(self, data, test_mode=False):
        self.logger.info("=== レポート生成プロセス開始 ===")
        all_data = {}
        all_data['weather'] = self.get_weather_forecast_3days()
        all_data['battery_now'] = self.get_current_battery_status()
        all_data['battery_pattern'] = self.get_24h_battery_pattern()
        all_data['achievement'] = self.calculate_daily_achievement()
        all_data['comparison'] = self.calculate_1year_comparison()
        all_data['savings'] = self.calculate_cost_savings()
        
        self.logger.info("=== 全データ収集完了。メール送信プロセスへ ===")
        # ... (実際のメール送信ロジックは省略) ...
        self.logger.info("メール送信プロセス完了（テストモード）。")
        return True

if __name__ == '__main__':
    # このファイルが直接実行された場合のテスト用コード
    print("このスクリプトはmain.pyから呼び出されることを想定しています。")
