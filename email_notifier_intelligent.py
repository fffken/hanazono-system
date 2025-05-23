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
        self.settings_recommender = SettingsRecommender()

    def send_daily_report(self, data):
        try:
            # メール設定取得
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_username')
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
        report = "=== HANAZONOシステム 最適化レポート ===\n\n"

        try:
            # 1. 天気予報取得
            self.logger.info("天気予報を取得中...")
            weather = get_weather_forecast()

            # 2. 季節判定
            season = get_current_season()
            detailed_season = get_detailed_season()

            # 3. 現在のバッテリー状態
            battery_info = self._extract_battery_info(data)
            report += f"■ 現在の状態\n"
            report += f"{battery_info}\n"

            # 4. 天気予報分析
            report += f"■ 天気予報分析\n"
            if weather:
                today_weather = weather.get('today', {})
                tomorrow_weather = weather.get('tomorrow', {})

                report += f"今日: {today_weather.get('condition', 'データなし')}\n"
                report += f"明日: {tomorrow_weather.get('condition', 'データなし')}\n\n"

                # 5. 最適化推奨（HANAZONOシステムの核心機能）
                recommendations = self._generate_recommendations(
                    weather, season, battery_info)
                report += f"■ 最適化推奨 🚀\n"
                report += f"{recommendations}\n"
            else:
                report += "天気データ取得失敗\n\n"
                report += f"■ 最適化推奨\n"
                report += "天気データなしのため基本推奨を適用\n"

            # 6. システム状態
            report += f"■ システム情報\n"
            report += f"季節判定: {season} ({detailed_season})\n"
            report += f"データ更新: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

        except Exception as e:
            self.logger.error(f"レポート生成エラー: {e}")
            report += f"レポート生成中にエラーが発生しました: {e}\n"

        report += "\n--- HANAZONOシステム 自動最適化 ---"
        return report

    def _extract_b


q
