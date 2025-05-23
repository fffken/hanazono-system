#!/usr/bin/env python3
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
        self.logger = logging.getLogger("email_notifier")

        # 設定マネージャーがある場合はそこから設定を取得
        if settings_manager:
            self.smtp_server = settings_manager.get('email.smtp_server')
            self.smtp_port = settings_manager.get('email.smtp_port')
            self.smtp_user = settings_manager.get('email.smtp_user')
            self.smtp_password = settings_manager.get('email.smtp_password')
            self.sender = settings_manager.get('email.sender')
            self.recipients = settings_manager.get('email.recipients', [])
        else:
            # 設定マネージャーがない場合はデフォルト値または環境変数から読み込む
            import os
            self.smtp_server = os.environ.get("SMTP_SERVER")
            self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
            self.smtp_user = os.environ.get("SMTP_USER")
            self.smtp_password = os.environ.get("SMTP_PASSWORD")
            self.sender = os.environ.get("EMAIL_SENDER")
            self.recipients = os.environ.get("EMAIL_RECIPIENTS", "").split(",")

    def send_weather_notification(self, weather_data, recommended_settings, battery_status=None):
        """天気予報と推奨設定の通知メールを送信"""
        subject = f"☀️ 天気予報とソーラー設定推奨 {weather_data['date']}"

        # 天気アイコン
        weather_emoji = self._get_weather_emoji(
            weather_data.get("weather", ""))

        # HTMLメール本文
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; }}
                .section {{ margin-bottom: 25px; }}
                h2 {{ color: #333366; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #ffffcc; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>{weather_emoji} 天気予報 - {weather_data['date']}</h2>
                <div class="section">
                    <p>天気: {weather_data.get('weather', '不明')} {weather_emoji}</p>
                    <p>気温: 最高 {weather_data.get('temp_high', '不明')}°C / 最低 {weather_data.get('temp_low', '不明')}°C</p>
                    <p>降水確率: {weather_data.get('rain_probability', '不明')}%</p>
                </div>
                
                <h2>⚙️ 推奨設定</h2>
                <div class="section">
                    <table>
                        <tr>
                            <th>項目</th>
                            <th>設定値</th>
                        </tr>
                        <tr>
                            <td>充電電流</td>
                            <td>{recommended_settings.get('charge_current', '不明')} A</td>
                        </tr>
                        <tr>
                            <td>充電時間</td>
                            <td>{recommended_settings.get('charge_time', '不明')} 分</td>
                        </tr>
                        <tr>
                            <td>SOC設定</td>
                            <td>{recommended_settings.get('soc', '不明')} %</td>
                        </tr>
                    </table>
                </div>
        """

        # バッテリー状態データがある場合は追加
        if battery_status:
            html_content += f"""
                <h2>🔋 バッテリー状態</h2>
                <div class="section">
                    <table>
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
                        <tr>
                            <td>現在のSOC</td>
                            <td>{battery_status.get('soc', '不明')} %</td>
                        </tr>
                        <tr>
                            <td>電圧</td>
                            <td>{battery_status.get('voltage', '不明')} V</td>
                        </tr>
                        <tr>
                            <td>電流</td>
                            <td>{battery_status.get('current', '不明')} A</td>
                        </tr>
                        <tr>
                            <td>最終更新</td>
                            <td>{battery_status.get('datetime', '不明')}</td>
                        </tr>
                    </table>
                </div>
            """

        # フッター部分
        html_content += f"""
                <div class="footer">
                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>
                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # メール送信
        self._send_html_email(subject, html_content)

    def send_daily_report(self, report_data, chart_paths=None):
        """日次レポートをメールで送信"""
        if not report_data:
            self.logger.error("日次レポートデータがありません")
            return False

        subject = f"📊 ソーラーシステム日次レポート {report_data['formatted_date']}"

        # HTMLメール本文
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; }}
                .section {{ margin-bottom: 25px; }}
                h2 {{ color: #333366; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #ffffcc; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📊 日次レポート - {report_data['formatted_date']}</h2>
                <div class="section">
                    <table>
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
                        <tr>
                            <td>朝7時のSOC</td>
                            <td>{report_data.get('soc_morning', '不明')} %</td>
                        </tr>
                        <tr>
                            <td>夜23時のSOC</td>
                            <td>{report_data.get('soc_night', '不明')} %</td>
                        </tr>
                        <tr>
                            <td>SOC最小値</td>
                            <td>{report_data.get('soc_min', '不明')} %</td>
                        </tr>
                        <tr>
                            <td>SOC最大値</td>
                            <td>{report_data.get('soc_max', '不明')} %</td>
                        </tr>
                        <tr>
                            <td>平均電圧</td>
                            <td>{report_data.get('voltage_avg', '不明'):.1f} V</td>
                        </tr>
                        <tr>
                            <td>平均電流</td>
                            <td>{report_data.get('current_avg', '不明'):.1f} A</td>
                        </tr>
                        <tr>
                            <td>データポイント数</td>
                            <td>{report_data.get('data_points', '不明')}</td>
                        </tr>
                        <tr>
                            <td>測定期間</td>
                            <td>{report_data.get('first_timestamp', '不明')} ～ {report_data.get('last_timestamp', '不明')}</td>
                        </tr>
                    </table>
                </div>
                
                <h2>📈 グラフ</h2>
                <div class="section">
                    <p>SOCの推移：</p>
                    <img src="cid:soc_chart" style="width: 100%; max-width: 800px;">
                    
                    <p>電圧と電流の推移：</p>
                    <img src="cid:voltage_current_chart" style="width: 100%; max-width: 800px;">
                </div>
                
                <div class="footer">
                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>
                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # メール送信（グラフ画像添付）
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
            self.logger.error("週次レポートデータがありません")
            return False

        subject = f"📊 ソーラーシステム週次レポート {report_data['formatted_period']}"

        # HTMLメール本文
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; }}
                .section {{ margin-bottom: 25px; }}
                h2 {{ color: #333366; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #ffffcc; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📊 週次レポート - {report_data['formatted_period']}</h2>
                <div class="section">
                    <table>
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
                        <tr>
                            <td>朝7時のSOC平均</td>
                            <td>{report_data.get('soc_morning_avg', '不明'):.1f} %</td>
                        </tr>
                        <tr>
                            <td>夜23時のSOC平均</td>
                            <td>{report_data.get('soc_night_avg', '不明'):.1f} %</td>
                        </tr>
                        <tr>
                            <td>対象日数</td>
                            <td>{report_data.get('days_count', '不明')} 日</td>
                        </tr>
                    </table>
                </div>
                
                <h2>📈 グラフ</h2>
                <div class="section">
                    <p>週間SOC推移：</p>
                    <img src="cid:weekly_soc_chart" style="width: 100%; max-width: 800px;">
                </div>
                
                <div class="footer">
                    <p>このメールはLVYUANソーラー蓄電システム自動最適化システムによって送信されました。</p>
                    <p>送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # メール送信（グラフ画像添付）
        image_paths = {}
        if chart_paths:
            if 'weekly_soc' in chart_paths:
                image_paths['weekly_soc_chart'] = chart_paths['weekly_soc']

        self._send_html_email(subject, html_content, image_paths)
        return True

    def _get_weather_emoji(self, weather):
        """天気に応じた絵文字を返す"""
        weather_emojis = {
            '晴れ': '☀️',
            '曇り': '☁️',
            '雨': '🌧️',
            '雪': '❄️',
            '雷': '⚡',
            '霧': '🌫️',
            '曇のち晴': '⛅',
            '晴れのち曇り': '⛅',
            '晴のち雨': '🌦️',
            '雨のち晴れ': '🌦️',
            '曇りのち雨': '🌧️',
            '雨のち曇り': '🌧️'
        }

        for key, emoji in weather_emojis.items():
            if key in weather:
                return emoji

        # デフォルトは太陽
        return '☀️'

    def _send_html_email(self, subject, html_content, image_paths=None):
        """HTMLメールを送信する"""
        if not self.recipients:
            self.logger.error("受信者が設定されていません。")
            return False

        try:
            # マルチパートメッセージを作成
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = self.sender
            msg['To'] = ', '.join(self.recipients)

            # HTMLコンテンツを添付
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)

            msg_text = MIMEText(html_content, 'html', 'utf-8')
            msg_alternative.attach(msg_text)

            # 画像がある場合は添付
            if image_paths:
                for img_id, img_path in image_paths.items():
                    try:
                        with open(img_path, 'rb') as f:
                            img_data = f.read()
                            img = MIMEImage(img_data)
                            img.add_header('Content-ID', f'<{img_id}>')
                            img.add_header(
                                'Content-Disposition', 'inline', filename=os.path.basename(img_path))
                            msg.attach(img)
                    except Exception as e:
                        self.logger.error(f"画像 {img_path} の添付エラー: {e}")

            # SMTPサーバに接続
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)

            # メール送信
            server.sendmail(self.sender, self.recipients, msg.as_string())
            server.quit()

            self.logger.info(f"メール送信成功: {subject}")
            return True

        except Exception as e:
            self.logger.error(f"メール送信エラー: {e}")
            return False


# テスト用メイン処理
if __name__ == "__main__":
    import argparse

    # ロギング設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='メール通知テスト')
    parser.add_argument('--weather', action='store_true', help='天気予報通知のテスト')
    parser.add_argument('--daily', help='日次レポート通知のテスト（レポートJSONファイルのパス）')
    parser.add_argument('--weekly', help='週次レポート通知のテスト（レポートJSONファイルのパス）')

    args = parser.parse_args()

    notifier = EmailNotifier()

    if args.weather:
        # テスト用天気データ
        weather_data = {
            'date': '2025年5月1日',
            'weather': '晴れ',
            'temp_high': 28,
            'temp_low': 18,
            'rain_probability': 10
        }

        # テスト用推奨設定
        recommended_settings = {
            'charge_current': 50.0,
            'charge_time': 45,
            'soc': 45
        }

        # テスト用バッテリー状態
        battery_status = {
            'soc': 75,
            'voltage': 52.4,
            'current': 9.5,
            'datetime': '2025-05-01 12:30:00'
        }

        notifier.send_weather_notification(
            weather_data, recommended_settings, battery_status)

    if args.daily:
        import json
        try:
            with open(args.daily, 'r') as f:
                report_data = json.load(f)

            # テスト用グラフパス
            date_str = report_data.get('date', '20250501')
            data_dir = os.path.join(os.path.expanduser(
                '~'), 'lvyuan_solar_control', 'data')
            charts_dir = os.path.join(data_dir, 'charts')

            chart_paths = {
                'soc': os.path.join(charts_dir, f"soc_{date_str}.png"),
                'voltage_current': os.path.join(charts_dir, f"voltage_current_{date_str}.png")
            }

            notifier.send_daily_report(report_data, chart_paths)
        except Exception as e:
            logging.error(f"日次レポート通知テストエラー: {e}")

    if args.weekly:
        import json
        try:
            with open(args.weekly, 'r') as f:
                report_data = json.load(f)

            # テスト用グラフパス
            timestamp = time.strftime("%Y%m%d")
            data_dir = os.path.join(os.path.expanduser(
                '~'), 'lvyuan_solar_control', 'data')
            charts_dir = os.path.join(data_dir, 'charts')

            chart_paths = {
                'weekly_soc': os.path.join(charts_dir, f"weekly_soc_{timestamp}.png")
            }

            notifier.send_weekly_report(report_data, chart_paths)
        except Exception as e:
            logging.error(f"週次レポート通知テストエラー: {e}")
