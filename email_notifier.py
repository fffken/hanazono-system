import logging
from enhanced_email_system import EnhancedEmailSystem
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime
from weather_forecast import get_weather_forecast
from season_detector import get_current_season, get_detailed_season
from settings_recommender import SettingsRecommender


class EmailNotifier:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.enhanced_system = EnhancedEmailSystem(config, logger)
        self.settings_recommender = SettingsRecommender()

    def send_daily_report(self, data):
        try:
            # メール設定取得
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')

            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error("メール設定が不完全です")
                return False

            # インテリジェントレポート生成
            now = datetime.datetime.now()
            time_suffix = "(07時)" if 5 <= now.hour < 12 else "(23時)"
            date_str = now.strftime("%Y年%m月%d日")
            subject = f"HANAZONOシステム最適化レポート {date_str} {time_suffix}"

            text_content = self._generate_intelligent_report(data)

            # メール送信
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ", ".join(recipients)
            msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()

            self.logger.info(f"最適化レポートを送信しました: {subject}")
            return True

        except Exception as e:
            self.logger.error(f"メール送信エラー: {e}")
            return False

    def _generate_intelligent_report(self, data):
        """拡張版インテリジェントレポート生成"""
        try:
            # 天気予報取得
            from weather_forecast import get_weather_forecast
            weather_data = get_weather_forecast()
            
            # バッテリー情報取得
            battery_info = self._extract_battery_info(data)
            
            # 拡張システムでHTMLレポート生成
            html_report = self.enhanced_system.generate_complete_report(
                data, weather_data, battery_info
            )
            
            return html_report
            
        except Exception as e:
            self.logger.error(f"拡張レポート生成エラー: {e}")
            # フォールバック：従来のテキストレポート
            return self._generate_fallback_report(data)
    
    def _extract_battery_info(self, data):
        """バッテリー情報を抽出（修正版）"""
        try:
            if isinstance(data, tuple) and len(data) > 0:
                actual_data = data[0]
            elif isinstance(data, dict):
                actual_data = data
            else:
                return "バッテリー情報: データ形式エラー"
            if 'parameters' in actual_data:
                params = actual_data['parameters']
                soc_value = params.get('0x0100', {}).get('value', 'N/A')
                voltage_value = params.get('0x0101', {}).get('value', 'N/A')
                current_value = params.get('0x0102', {}).get('value', 'N/A')
                timestamp = actual_data.get('datetime', 'N/A')
                return f"🔋 バッテリー残量: {soc_value}% (取得時刻: {timestamp})\n⚡ 電圧: {voltage_value}V 🔌 電流: {current_value}A"
            else:
                return "バッテリー情報: parametersが見つかりません"
        except Exception as e:
            return f"バッテリー情報取得エラー: {e}"

    def _generate_recommendations(self, weather, season, battery_info):
        """天気予報と季節に基づく最適化推奨を生成"""
        recommendations = []

        try:
            if weather:
                tomorrow = weather.get('tomorrow', {})
                condition = tomorrow.get('weather', '')

                if '雨' in condition or '曇' in condition:
                    recommendations.append("☔ 明日は発電量低下予想")
                    recommendations.append("→ 今夜の放電を控えめに設定推奨")
                    recommendations.append("→ バッテリー残量80%以上を維持")

                elif '晴' in condition:
                    recommendations.append("☀️ 明日は好天で高発電予想")
                    recommendations.append("→ 今夜は積極的放電OK")
                    recommendations.append("→ バッテリー残量50%程度まで使用可能")

                if season == '夏':
                    recommendations.append("🌞 夏期間: 午後の高温による効率低下注意")
                elif season == '冬':
                    recommendations.append("❄️ 冬期間: 朝の霜・積雪チェック推奨")

            return "\n".join(recommendations) if recommendations else "標準運用を継続"

        except Exception as e:
            return f"推奨生成エラー: {e}"

    def _generate_fallback_report(self, data):
        """フォールバック用シンプルレポート生成"""
        try:
            battery_info = self._extract_battery_info(data)
            return f"""
HANAZONOシステム 簡易レポート

バッテリー状態:
- SOC: {battery_info.get('soc', 'N/A')}%
- 電圧: {battery_info.get('voltage', 'N/A')}V

データファイル: {data.get('source_file', 'N/A')}
生成時刻: {data.get('timestamp', 'N/A')}

※ 詳細レポート生成でエラーが発生したため、簡易版を表示しています。
"""
        except Exception as e:
            return f"エラー: レポート生成に失敗しました - {str(e)}"

