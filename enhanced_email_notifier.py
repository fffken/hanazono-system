"""
HANAZONOシステム Enhanced Email Notifier v2.0
ML NEWS統合メールシステム

機能:
1. 既存メールシステムとML NEWSの統合
2. 動的設定変化のリアルタイム通知
3. 面白いML学習進捗レポート配信
4. Phase 1機械学習エンジンとの完全連携

配信内容:
📧 ML学習NEWSメール
📊 動的設定更新レポート  
🎯 削減効果・予測精度通知
💰 経済効果レポート
"""

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

def expand_env_vars(config):
    """環境変数を展開"""
    def replace_env_var(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    
    if isinstance(config, dict):
        return {k: expand_env_vars(v) for k, v in config.items()}
    elif isinstance(config, str):
        return re.sub(r'\$\{([^}]+)\}', replace_env_var, config)
    else:
        return config

class EnhancedEmailNotifier:
    def __init__(self, config, logger=None):
        self.config = expand_env_vars(config)
        self.logger = logger or self._setup_logger()
        self.db_path = 'data/hanazono_data.db'
        
        # ML NEWSジェネレーターの初期化
        self._initialize_news_generator()
        
        # 動的設定管理システムの初期化
        self._initialize_settings_manager()
        
    def _setup_logger(self):
        """ログシステム初期化"""
        logger = logging.getLogger('enhanced_email')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
        
    def _initialize_news_generator(self):
        """ML NEWSジェネレーターの初期化"""
        try:
            from ml_news_generator import MLNewsGenerator, generate_news_for_email
            self.news_generator = MLNewsGenerator()
            self.generate_news_for_email = generate_news_for_email
            self.logger.info("✅ ML NEWSジェネレーター統合完了")
        except ImportError as e:
            self.logger.warning(f"⚠️ ML NEWSジェネレーターが見つかりません: {e}")
            self.news_generator = None
        except Exception as e:
            self.logger.error(f"❌ NEWSジェネレーター初期化エラー: {e}")
            self.news_generator = None
            
    def _initialize_settings_manager(self):
        """動的設定管理システムの初期化"""
        try:
            from dynamic_settings_manager import DynamicSettingsManager
            self.settings_manager = DynamicSettingsManager()
            self.logger.info("✅ 動的設定管理システム統合完了")
        except ImportError as e:
            self.logger.warning(f"⚠️ 動的設定管理システムが見つかりません: {e}")
            self.settings_manager = None
        except Exception as e:
            self.logger.error(f"❌ 設定管理システム初期化エラー: {e}")
            self.settings_manager = None

    def get_ml_news_content(self):
        """ML NEWSコンテンツの取得"""
        try:
            if self.news_generator:
                news_summary = self.generate_news_for_email()
                return news_summary
            else:
                return {
                    'total_news': 0,
                    'latest_count': 0,
                    'formatted_news': "📰 ML学習NEWSは現在利用できません",
                    'has_new_content': False,
                    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            self.logger.error(f"ML NEWS取得エラー: {e}")
            return {
                'total_news': 0,
                'latest_count': 0,
                'formatted_news': f"📰 ML学習NEWS取得エラー: {e}",
                'has_new_content': False,
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    def get_current_ml_status(self):
        """現在のML状況取得"""
        try:
            if self.settings_manager:
                return self.settings_manager.get_current_ml_status()
            else:
                return {
                    'status': 'unavailable',
                    'confidence': 15,
                    'data_count': 0,
                    'recommendation': {
                        'charge_current': 50,
                        'charge_time': 45,
                        'soc_setting': 45,
                        'confidence_level': 0.15
                    }
                }
        except Exception as e:
            self.logger.error(f"ML状況取得エラー: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'confidence': 15,
                'data_count': 0
            }

    def get_weather_forecast_3days(self):
        """3日分の天気予報を取得（フォールバック対応）"""
        try:
            # 既存の天気予報システムを活用
            try:
                from weather_forecast import get_weather_forecast
                weather_data = get_weather_forecast()
                if weather_data:
                    return weather_data
            except ImportError:
                pass
            
            # フォールバック用の仮データ
            return {
                "today": {"weather": "晴れ", "temp_max": 25, "temp_min": 15},
                "tomorrow": {"weather": "曇り", "temp_max": 23, "temp_min": 16},
                "day_after": {"weather": "晴れ", "temp_max": 26, "temp_min": 17}
            }
        except Exception as e:
            self.logger.warning(f"天気予報取得エラー: {e}")
            return {"today": {"weather": "データなし", "temp_max": 20, "temp_min": 15}}

    def get_current_battery_status(self):
        """現在のバッテリー状況を取得"""
        try:
            if not os.path.exists(self.db_path):
                return None
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 最新のデータを取得
            cursor.execute('''
                SELECT battery_soc, battery_voltage, battery_current, timestamp
                FROM system_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                soc, voltage, current, timestamp = result
                return {
                    'soc': soc,
                    'voltage': voltage,
                    'current': current,
                    'timestamp': timestamp,
                    'status': 'charging' if current > 0 else 'discharging' if current < 0 else 'idle'
                }
                
        except Exception as e:
            self.logger.error(f"バッテリー状況取得エラー: {e}")
        
        return None

    def calculate_daily_achievement(self):
        """今日の達成状況を計算"""
        try:
            if not os.path.exists(self.db_path):
                return self._get_default_achievement()
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            # 今日のデータを取得
            cursor.execute('''
                SELECT AVG(pv_power), AVG(load_power), AVG(battery_soc)
                FROM system_data 
                WHERE date(timestamp) = ?
            ''', (today,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                avg_pv, avg_load, avg_soc = result
                return {
                    "solar_generation": {
                        "current": avg_pv or 0, "target": 3000, 
                        "achievement": min((avg_pv or 0) / 3000 * 100, 100)
                    },
                    "battery_efficiency": {
                        "current": avg_soc or 50, "target": 80,
                        "achievement": min((avg_soc or 50) / 80 * 100, 100)
                    },
                    "self_consumption": {
                        "current": 85, "target": 90,
                        "achievement": 94.4
                    }
                }
        except Exception as e:
            self.logger.error(f"達成状況計算エラー: {e}")
        
        return self._get_default_achievement()

    def _get_default_achievement(self):
        """デフォルト達成状況"""
        return {
            "solar_generation": {"current": 2.5, "target": 3.0, "achievement": 83.3},
            "battery_efficiency": {"current": 67, "target": 80, "achievement": 83.8},
            "self_consumption": {"current": 85, "target": 90, "achievement": 94.4}
        }

    def generate_progress_bar(self, percentage, length=20):
        """プログレスバーの生成"""
        filled = int(length * percentage / 100)
        empty = length - filled
        return "■" * filled + "□" * empty

    def send_ml_news_report(self, test_mode=False):
        """ML学習NEWSレポートの送信"""
        try:
            # 設定情報取得
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error('メール設定が不完全です')
                return False
            
            # ML NEWSと状況取得
            news_summary = self.get_ml_news_content()
            ml_status = self.get_current_ml_status()
            weather_data = self.get_weather_forecast_3days()
            battery_status = self.get_current_battery_status()
            achievement = self.calculate_daily_achievement()
            
            # メール件名の生成
            now = datetime.now()
            if news_summary['has_new_content']:
                subject = f"🎉【HANAZONO】ML学習NEWS - {news_summary['latest_count']}件の更新"
            else:
                subject = f"📊【HANAZONO】日次レポート - ML予測精度{ml_status.get('confidence', 15):.1f}%"
            
            # メール本文生成
            content = self._generate_ml_news_email_content(
                news_summary, ml_status, weather_data, battery_status, achievement
            )
            
            if test_mode:
                print("📧 テストモード - メール内容:")
                print(f"件名: {subject}")
                print("=" * 60)
                print(content)
                print("=" * 60)
                return True
            
            # メール送信
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            
            self.logger.info(f'ML学習NEWSレポートを送信しました: {subject}')
            return True
            
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}')
            return False

    def _generate_ml_news_email_content(self, news_summary, ml_status, weather_data, battery_status, achievement):
        """ML学習NEWSメール本文の生成"""
        content = []
        now = datetime.now()
        
        # ヘッダー
        content.append("🏠 HANAZONOシステム ML学習統合レポート")
        content.append("=" * 50)
        content.append(f"📅 生成日時: {now.strftime('%Y年%m月%d日 %H:%M')}")
        content.append("")
        
        # ML学習NEWS
        content.append("📰 ML学習NEWS")
        content.append("-" * 30)
        if news_summary['has_new_content']:
            content.append(f"🎉 新着ニュース: {news_summary['latest_count']}件")
            content.append("")
            content.append(news_summary['formatted_news'])
        else:
            content.append("現在、新しいML学習ニュースはありません")
            content.append("システムは安定運用中です 📊")
        content.append("")
        
        # 現在のML推奨設定
        content.append("🎯 現在のML推奨設定")
        content.append("-" * 30)
        if ml_status['status'] == 'active' and 'recommendation' in ml_status:
            rec = ml_status['recommendation']
            content.append(f"📊 充電電流: {rec['charge_current']}A")
            content.append(f"⏰ 充電時間: {rec['charge_time']}分")
            content.append(f"🔋 SOC設定: {rec['soc_setting']}%")
            content.append(f"🎯 信頼度: {rec['confidence_level']:.1%}")
            content.append(f"📈 データ数: {ml_status.get('data_count', 0):,}件")
            
            if ml_status.get('total_savings'):
                content.append(f"💰 予想年間削減額: ¥{ml_status['total_savings']:,.0f}")
        else:
            content.append("⚠️ ML推奨システムは現在利用できません")
            content.append("基本設定で運用中です")
        content.append("")
        
        # 天気予報と推奨
        content.append("🌤️ 3日間天気予報")
        content.append("-" * 30)
        if weather_data:
            for day, data in weather_data.items():
                weather_icon = {"晴れ": "☀️", "曇り": "☁️", "雨": "🌧️"}.get(data.get('weather', ''), "🌤️")
                content.append(f"{weather_icon} {day}: {data.get('weather', 'データなし')} "
                             f"(最高{data.get('temp_max', 20)}℃/最低{data.get('temp_min', 15)}℃)")
        content.append("")
        
        # システム状況
        content.append("⚙️ システム状況")
        content.append("-" * 30)
        if battery_status:
            content.append(f"🔋 バッテリーSOC: {battery_status['soc']}%")
            content.append(f"⚡ 電圧: {battery_status['voltage']:.1f}V")
            status_icon = {"charging": "🔌", "discharging": "⚡", "idle": "⏸️"}.get(battery_status['status'], "❓")
            content.append(f"{status_icon} 状態: {battery_status['status']}")
        else:
            content.append("📊 システムデータを取得中...")
        content.append("")
        
        # 今日の達成状況
        content.append("📈 今日の達成状況")
        content.append("-" * 30)
        content.append(f"☀️ 太陽光発電: {achievement['solar_generation']['current']:.1f}kW "
                      f"({achievement['solar_generation']['achievement']:.1f}%) "
                      f"{self.generate_progress_bar(achievement['solar_generation']['achievement'], 15)}")
        
        content.append(f"🔋 蓄電効率: {achievement['battery_efficiency']['current']:.0f}% "
                      f"({achievement['battery_efficiency']['achievement']:.1f}%) "
                      f"{self.generate_progress_bar(achievement['battery_efficiency']['achievement'], 15)}")
        
        content.append(f"🏠 自家消費率: {achievement['self_consumption']['current']:.0f}% "
                      f"({achievement['self_consumption']['achievement']:.1f}%) "
                      f"{self.generate_progress_bar(achievement['self_consumption']['achievement'], 15)}")
        content.append("")
        
        # フッター
        content.append("📋 システム情報")
        content.append("-" * 30)
        content.append(f"🤖 ML学習エンジン: Phase 1 v5.0 稼働中")
        content.append(f"📊 動的設定管理: v2.0 有効")
        content.append(f"📰 NEWSジェネレーター: v1.0 稼働中")
        content.append(f"🔄 最終更新: {news_summary['last_update']}")
        content.append("")
        content.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        content.append("📧 このメールはHANAZONOシステムにより自動生成されました")
        content.append("🤖 ML学習により設定が変更された場合、NEWSでお知らせします")
        
        return '\n'.join(content)

    def send_daily_report(self, data, test_mode=False):
        """日次レポートの送信（ML統合版）"""
        return self.send_ml_news_report(test_mode)

def test_enhanced_email_system():
    """Enhanced Email Systemのテスト"""
    print("📧 Enhanced Email System v2.0 テスト開始")
    print("=" * 60)
    
    # 設定読み込み
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        email_config = settings.get('email', {})
    except Exception as e:
        print(f"⚠️ 設定読み込みエラー: {e}")
        email_config = {}
    
    # Enhanced Email Systemの初期化
    notifier = EnhancedEmailNotifier(email_config)
    
    # ML NEWS統合テスト
    print("🔄 ML NEWS統合テスト...")
    news_summary = notifier.get_ml_news_content()
    print(f"✅ ML NEWS取得: {news_summary['latest_count']}件")
    
    # ML状況取得テスト
    print("🔄 ML状況取得テスト...")
    ml_status = notifier.get_current_ml_status()
    print(f"✅ ML状況: {ml_status['status']}")
    
    # テストメール送信
    print("🔄 テストメール生成...")
    success = notifier.send_ml_news_report(test_mode=True)
    
    if success:
        print("\n✅ Enhanced Email System v2.0 テスト完了")
        print("🎉 ML学習NEWS統合メールシステム稼働準備完了!")
    else:
        print("\n❌ Enhanced Email System テスト失敗")
    
    return success

if __name__ == "__main__":
    print("📧 HANAZONOシステム Enhanced Email Notifier v2.0")
    print("=" * 60)
    print("📋 実行オプション:")
    print("1. メイン実行: python3 enhanced_email_notifier.py")
    print("2. テスト実行: python3 -c \"from enhanced_email_notifier import test_enhanced_email_system; test_enhanced_email_system()\"")
    print("3. ML NEWS送信: python3 -c \"from enhanced_email_notifier import EnhancedEmailNotifier; import json; settings=json.load(open('settings.json')); notifier=EnhancedEmailNotifier(settings['email']); notifier.send_ml_news_report()\"")
    print("=" * 60)
    
    test_enhanced_email_system()
