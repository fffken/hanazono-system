"""拡張版メール通知モジュール"""
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime

class EmailNotifier:

    def __init__(self, settings_manager=None):
        self.settings_manager = settings_manager
        self.logger = logging.getLogger('email_notifier')
        if settings_manager:
            self.smtp_server = settings_manager.get('email.smtp_server')
            self.smtp_port = settings_manager.get('email.smtp_port')
            self.smtp_user = settings_manager.get('email.smtp_user')
            self.smtp_password = settings_manager.get('email.smtp_password')
            self.sender = settings_manager.get('email.sender')
            self.recipients = settings_manager.get('email.recipients', [])
        else:
            import os
            self.smtp_server = os.environ.get('SMTP_SERVER')
            self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            self.smtp_user = os.environ.get('SMTP_USER')
            self.smtp_password = os.environ.get('SMTP_PASSWORD')
            self.sender = os.environ.get('EMAIL_SENDER')
            self.recipients = os.environ.get('EMAIL_RECIPIENTS', '').split(',')

    def send_weather_notification(self, weather_data, recommended_settings, battery_status=None):
        """天気予報と推奨設定の通知メールを送信"""
        subject = f"☀️ 天気予報とソーラー設定推奨 {weather_data['date']}"
        weather_emoji = self._get_weather_emoji(weather_data.get('weather', ''))
        html_content = f"""\n        <html>\n        <head>\n            <style>\n                body {{ font-family: Arial, sans-serif; }}\n                .container {{ padding: 20px; }}\n                .section {{ margin-bottom: 25px; }}\n                h2 {{ color: #333366; }}\n                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}\n                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}\n                th {{ background-color: #f2f2f2; }}\n                .highlight {{ background-color: #ffffcc; }}\n                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}\n            </style>\n        </head>\n        <body>\n            <div class="container">\n                <h2>{weather_emoji} 天気予報 - {weather_data['date']}</h2>\n                <div class="section">\n                    <p>天気: {weather_data.get('weather', '不明')} {weather_emoji}</p>\n                    <p>気温: 最高 {weather_data.get('temp_high', '不明')}°C / 最低 {weather_data.get('temp_low', '不明')}°C</p>\n                    <p>降水確率: {weather_data.get('rain_probability', '不明')}%</p>\n                </div>\n\n                <h2>⚙️ 推奨設定</h2>\n                <div class="section">\n                    <table>\n                        <tr>\n                            <th>項目</th>\n                            <th>設定値</th>\n                        </tr>\n                        <tr>\n                            <td>充電電流</td>\n                            <td>{recommended_settings.get('charge_current', '不明')} A</td>\n                        </tr>\n                        <tr>\n                            <td>充電時間</td>\n                            <td>{recommended_settings.get('charge_time', '不明')} 分</td>\n                        </tr>\n                        <tr>\n                            <td>SOC設定</td>\n                            <td>{recommended_settings.get('soc', '不明')} %</td>\n                        </tr>\n                    </table>\n                </div>\n        """
        if battery_status:
            html_content += f"""\n                <h2>🔋 バッテリー状態</h2>\n                <div class="section">\n                    <table>\n                        <tr>\n                            <th>項目</th>\n                            <th>値</th>\n                        </tr>\n                        <tr>\n                            <td>現在のSOC</td>\n                            <td>{battery_status.get('soc', '不明')} %</td>\n                        </tr>\n                        <tr>\n                            <td>電圧</td>\n                            <td>{battery_status.get('voltage', '不明')} V</td>\n                        </tr>\n                        <tr>\n                            <td>電流</td>\n                            <td>{battery_status.get('current', '不明')} A</td>\n                        </tr>\n                        <tr>\n                            <td>最終更新</td>\n                            <td>{battery_status.get('datetime', '不明')}</td>\n                        </tr>\n                    </table>\n                </div>\n            """
        html_content += f"""\n                <div class="footer">\n                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>\n                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        """
        self._send_html_email(subject, html_content)

    def send_daily_report(self, report_data, chart_paths=None):
        """日次レポートをメールで送信"""
        if not report_data:
            self.logger.error('日次レポートデータがありません')
            return False
        subject = f"📊 ソーラーシステム日次レポート {report_data['formatted_date']}"
        html_content = f"""\n        <html>\n        <head>\n            <style>\n                body {{ font-family: Arial, sans-serif; }}\n                .container {{ padding: 20px; }}\n                .section {{ margin-bottom: 25px; }}\n                h2 {{ color: #333366; }}\n                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}\n                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}\n                th {{ background-color: #f2f2f2; }}\n                .highlight {{ background-color: #ffffcc; }}\n                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}\n            </style>\n        </head>\n        <body>\n            <div class="container">\n                <h2>📊 日次レポート - {report_data['formatted_date']}</h2>\n                <div class="section">\n                    <table>\n                        <tr>\n                            <th>項目</th>\n                            <th>値</th>\n                        </tr>\n                        <tr>\n                            <td>朝7時のSOC</td>\n                            <td>{report_data.get('soc_morning', '不明')} %</td>\n                        </tr>\n                        <tr>\n                            <td>夜23時のSOC</td>\n                            <td>{report_data.get('soc_night', '不明')} %</td>\n                        </tr>\n                        <tr>\n                            <td>SOC最小値</td>\n                            <td>{report_data.get('soc_min', '不明')} %</td>\n                        </tr>\n                        <tr>\n                            <td>SOC最大値</td>\n                            <td>{report_data.get('soc_max', '不明')} %</td>\n                        </tr>\n                        <tr>\n                            <td>平均電圧</td>\n                            <td>{report_data.get('voltage_avg', '不明'):.1f} V</td>\n                        </tr>\n                        <tr>\n                            <td>平均電流</td>\n                            <td>{report_data.get('current_avg', '不明'):.1f} A</td>\n                        </tr>\n                        <tr>\n                            <td>データポイント数</td>\n                            <td>{report_data.get('data_points', '不明')}</td>\n                        </tr>\n                        <tr>\n                            <td>測定期間</td>\n                            <td>{report_data.get('first_timestamp', '不明')} ～ {report_data.get('last_timestamp', '不明')}</td>\n                        </tr>\n                    </table>\n                </div>\n\n                <h2>📈 グラフ</h2>\n                <div class="section">\n                    <p>SOCの推移：</p>\n                    <img src="cid:soc_chart" style="width: 100%; max-width: 800px;">\n\n                    <p>電圧と電流の推移：</p>\n                    <img src="cid:voltage_current_chart" style="width: 100%; max-width: 800px;">\n                </div>\n\n                <div class="footer">\n                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>\n                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        """
        image_paths = {}
        if chart_paths:
            if 'soc' in chart_paths:
                image_paths['soc_chart'] = chart_paths['soc']
            if 'voltage_current' in chart_paths:
                image_paths['voltage_current_chart'] = chart_paths['voltage_current']
        self._send_html_email(subject, html_content, image_paths)
        return True

    def send_weekly_report(self, report_data, chart_paths=None):
        """週次レポートをメールで送信"""
        if not report_data:
            self.logger.error('週次レポートデータがありません')
            return False
        subject = f"📊 ソーラーシステム週次レポート {report_data['formatted_period']}"
        html_content = f"""\n        <html>\n        <head>\n            <style>\n                body {{ font-family: Arial, sans-serif; }}\n                .container {{ padding: 20px; }}\n                .section {{ margin-bottom: 25px; }}\n                h2 {{ color: #333366; }}\n                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}\n                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}\n                th {{ background-color: #f2f2f2; }}\n                .highlight {{ background-color: #ffffcc; }}\n                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}\n            </style>\n        </head>\n        <body>\n            <div class="container">\n                <h2>📊 週次レポート - {report_data['formatted_period']}</h2>\n                <div class="section">\n                    <table>\n                        <tr>\n                            <th>項目</th>\n                            <th>値</th>\n                        </tr>\n                        <tr>\n                            <td>朝7時のSOC平均</td>\n                            <td>{report_data.get('soc_morning_avg', '不明'):.1f} %</td>\n                        </tr>\n                        <tr>\n                            <td>夜23時のSOC平均</td>\n                            <td>{report_data.get('soc_night_avg', '不明'):.1f} %</td>\n                        </tr>\n                        <tr>\n                            <td>対象日数</td>\n                            <td>{report_data.get('days_count', '不明')} 日</td>\n                        </tr>\n                    </table>\n                </div>\n\n                <h2>📈 グラフ</h2>\n                <div class="section">\n                    <p>週間SOC推移：</p>\n                    <img src="cid:weekly_soc_chart" style="width: 100%; max-width: 800px;">\n                </div>\n\n                <div class="footer">\n                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>\n                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        """
        image_paths = {}
        if chart_paths:
            if 'weekly_soc' in chart_paths:
                image_paths['weekly_soc_chart'] = chart_paths['weekly_soc']
        self._send_html_email(subject, html_content, image_paths)
        return True

    def _get_weather_emoji(self, weather):
        """天気に応じた絵文字を返す"""
        weather_emojis = {'晴れ': '☀️', '曇り': '☁️', '雨': '🌧️', '雪': '❄️', '雷': '⚡', '霧': '🌫️', '曇のち晴': '⛅', '晴れのち曇り': '⛅', '晴のち雨': '🌦️', '雨のち晴れ': '🌦️', '曇りのち雨': '🌧️', '雨のち曇り': '🌧️'}
        for key, emoji in weather_emojis.items():
            if key in weather:
                return emoji
        return '☀️'

    def _send_html_email(self, subject, html_content, image_paths=None):
        """HTMLメールを送信する"""
        if not self.recipients:
            self.logger.error('受信者が設定されていません。')
            return False
        try:
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = self.sender
            msg['To'] = ', '.join(self.recipients)
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)
            msg_text = MIMEText(html_content, 'html', 'utf-8')
            msg_alternative.attach(msg_text)
            if image_paths:
                for img_id, img_path in image_paths.items():
                    try:
                        with open(img_path, 'rb') as f:
                            img_data = f.read()
                            img = MIMEImage(img_data)
                            img.add_header('Content-ID', f'<{img_id}>')
                            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
                            msg.attach(img)
                    except Exception as e:
                        self.logger.error(f'画像 {img_path} の添付エラー: {e}')
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender, self.recipients, msg.as_string())
            server.quit()
            self.logger.info(f'メール送信成功: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}')
            return False
if __name__ == '__main__':
    import argparse
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='メール通知テスト')
    parser.add_argument('--weather', action='store_true', help='天気予報通知のテスト')
    parser.add_argument('--daily', help='日次レポート通知のテスト（レポートJSONファイルのパス）')
    parser.add_argument('--weekly', help='週次レポート通知のテスト（レポートJSONファイルのパス）')
    args = parser.parse_args()
    notifier = EmailNotifier()
    if args.weather:
        weather_data = {'date': '2025年5月1日', 'weather': '晴れ', 'temp_high': 28, 'temp_low': 18, 'rain_probability': 10}
        recommended_settings = {'charge_current': 50.0, 'charge_time': 45, 'soc': 45}
        battery_status = {'soc': 75, 'voltage': 52.4, 'current': 9.5, 'datetime': '2025-05-01 12:30:00'}
        notifier.send_weather_notification(weather_data, recommended_settings, battery_status)
    if args.daily:
        import json
        try:
            with open(args.daily, 'r') as f:
                report_data = json.load(f)
            date_str = report_data.get('date', '20250501')
            data_dir = os.path.join(os.path.expanduser('~'), 'lvyuan_solar_control', 'data')
            charts_dir = os.path.join(data_dir, 'charts')
            chart_paths = {'soc': os.path.join(charts_dir, f'soc_{date_str}.png'), 'voltage_current': os.path.join(charts_dir, f'voltage_current_{date_str}.png')}
            notifier.send_daily_report(report_data, chart_paths)
        except Exception as e:
            logging.error(f'日次レポート通知テストエラー: {e}')
    if args.weekly:
        import json
        try:
            with open(args.weekly, 'r') as f:
                report_data = json.load(f)
            timestamp = time.strftime('%Y%m%d')
            data_dir = os.path.join(os.path.expanduser('~'), 'lvyuan_solar_control', 'data')
            charts_dir = os.path.join(data_dir, 'charts')
            chart_paths = {'weekly_soc': os.path.join(charts_dir, f'weekly_soc_{timestamp}.png')}
            notifier.send_weekly_report(report_data, chart_paths)
        except Exception as e:
            logging.error(f'週次レポート通知テストエラー: {e}')