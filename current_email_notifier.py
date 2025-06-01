"""
HANAZONOシステム: メール通知機能
ソーラー蓄電システムの状態レポートをメール送信する機能
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import logging
import argparse

class EmailNotifier:
    """
    メール通知機能を提供するクラス
    """

    def __init__(self, config, logger):
        """
        初期化

        Args:
            config: 設定情報
            logger: ロガーインスタンス
        """
        self.config = config
        self.logger = logger

    def _get_weather_emoji(self, condition):
        """
        天気状態に対応する絵文字を返す（改良版）

        Args:
            condition: 天気状態の文字列

        Returns:
            天気に対応する絵文字
        """
        if not condition or condition == 'データなし':
            return '🌐'
        elif '雨' in condition:
            return '🌧️'
        elif '雪' in condition:
            return '❄️'
        elif '曇' in condition or 'くもり' in condition:
            return '☁️'
        elif '霧' in condition or '霞' in condition:
            return '🌫️'
        elif '晴' in condition:
            return '☀️'
        elif '曇りがち' in condition or '厚い雲' in condition:
            return '☁️'
        else:
            return '🌈'

    def _parse_weather_components(self, weather_text):
        """
        天気文字列から各成分を抽出する

        Args:
            weather_text: 天気状態の文字列

        Returns:
            天気成分のリスト
        """
        if not weather_text or weather_text == 'データなし':
            return ['データなし']
        components = []
        for delimiter in [' のち ', 'のち', ' 後 ', '後']:
            if delimiter in weather_text:
                components = weather_text.split(delimiter)
                break
        if not components:
            components = [weather_text]
        return components

    def _format_weather_emojis(self, weather_text):
        """
        天気情報を絵文字の連結に変換

        Args:
            weather_text: 天気状態の文字列

        Returns:
            絵文字の連結（例: ☀️→☁️）
        """
        if not weather_text or weather_text == 'データなし':
            return '🌐'
        components = self._parse_weather_components(weather_text)
        emojis = [self._get_weather_emoji(comp.strip()) for comp in components]
        emoji_text = '→'.join(emojis)
        return emoji_text

    def _format_weather_line(self, weather_text):
        """
        天気情報を2行フォーマット（絵文字の連結 + テキスト）に整形

        Args:
            weather_text: 天気状態の文字列

        Returns:
            整形された天気表示テキスト
        """
        if not weather_text or weather_text == 'データなし':
            return '🌐\nデータなし'
        emoji_text = self._format_weather_emojis(weather_text)
        display_text = weather_text
        for term in [' のち ', 'のち', ' 後 ', '後']:
            display_text = display_text.replace(term, '→')
        return f'{emoji_text}\n{display_text}'

    def _format_date_jp(self, date_obj):
        """
        日付を日本語フォーマットに変換

        Args:
            date_obj: datetime オブジェクト

        Returns:
            日本語形式の日付文字列 (例: 2025年5月11日(日))
        """
        weekday_jp = ['月', '火', '水', '木', '金', '土', '日']
        weekday = weekday_jp[date_obj.weekday()]
        return f'{date_obj.year}年{date_obj.month}月{date_obj.day}日({weekday})'

    def _generate_text_report(self, data):
        """
        テキスト形式のレポートを生成

        Args:
            data: レポートデータ

        Returns:
            テキスト形式のレポート
        """
        now = datetime.datetime.now()
        date_str = self._format_date_jp(now)
        report = f'===== HANAZONOシステム状態レポート =====\n'
        report += f'日付: {date_str}\n\n'
        report += '■ 電力情報\n'
        if 'power_data' in data:
            power_data = data['power_data']
            report += f"バッテリー残量: {power_data.get('battery_level', 'N/A')}%\n"
            report += f"太陽光発電: {power_data.get('solar_generation', 'N/A')} W\n"
            report += f"消費電力: {power_data.get('consumption', 'N/A')} W\n"
        else:
            report += 'データなし\n'
        report += '\n'
        report += '■ 天気予報\n'
        if 'weather' in data:
            weather = data['weather']
            weather_today = weather.get('today', 'データなし')
            weather_tomorrow = weather.get('tomorrow', 'データなし')
            today_formatted = self._format_weather_line(weather_today)
            tomorrow_formatted = self._format_weather_line(weather_tomorrow)
            report += f'今日: {today_formatted}\n'
            report += f'明日: {tomorrow_formatted}\n'
        else:
            report += 'データなし\n'
        report += '\n'
        report += '■ システム状態\n'
        if 'system_status' in data:
            status = data['system_status']
            report += f"動作モード: {status.get('mode', 'N/A')}\n"
            report += f"最終更新: {status.get('last_update', 'N/A')}\n"
            report += f"システム温度: {status.get('temperature', 'N/A')} °C\n"
        else:
            report += 'データなし\n'
        return report

    def _generate_html_report(self, data):
        """
        HTML形式のレポートを生成

        Args:
            data: レポートデータ

        Returns:
            HTML形式のレポート
        """
        now = datetime.datetime.now()
        date_str = self._format_date_jp(now)
        html = f'\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <meta charset="UTF-8">\n            <style>\n                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }}\n                .container {{ max-width: 600px; margin: 0 auto; }}\n                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}\n                .section {{ margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 5px; }}\n                .section h2 {{ margin-top: 0; color: #4CAF50; }}\n                .weather-box {{ display: flex; align-items: center; margin-bottom: 10px; }}\n                .weather-emoji {{ font-size: 24px; margin-right: 10px; }}\n                .footer {{ margin-top: 20px; text-align: center; font-size: 12px; color: #777; }}\n            </style>\n        </head>\n        <body>\n            <div class="container">\n                <div class="header">\n                    <h1>HANAZONOシステム状態レポート</h1>\n                    <p>{date_str}</p>\n                </div>\n        '
        html += '\n                <div class="section">\n                    <h2>電力情報</h2>\n        '
        if 'power_data' in data:
            power_data = data['power_data']
            html += f"\n                    <p>バッテリー残量: <strong>{power_data.get('battery_level', 'N/A')}%</strong></p>\n                    <p>太陽光発電: {power_data.get('solar_generation', 'N/A')} W</p>\n                    <p>消費電力: {power_data.get('consumption', 'N/A')} W</p>\n            "
        else:
            html += '<p>データなし</p>'
        html += '\n                </div>\n        '
        html += '\n                <div class="section">\n                    <h2>天気予報</h2>\n        '
        if 'weather' in data:
            weather = data['weather']
            weather_today = weather.get('today', 'データなし')
            weather_tomorrow = weather.get('tomorrow', 'データなし')
            today_emojis = self._format_weather_emojis(weather_today)
            tomorrow_emojis = self._format_weather_emojis(weather_tomorrow)
            today_text = weather_today
            tomorrow_text = weather_tomorrow
            for term in [' のち ', 'のち', ' 後 ', '後']:
                today_text = today_text.replace(term, '→')
                tomorrow_text = tomorrow_text.replace(term, '→')
            html += f'\n                    <div class="weather-box">\n                        <span class="weather-emoji">{today_emojis}</span>\n                        <div>\n                            <strong>今日:</strong> {today_text}\n                        </div>\n                    </div>\n                    <div class="weather-box">\n                        <span class="weather-emoji">{tomorrow_emojis}</span>\n                        <div>\n                            <strong>明日:</strong> {tomorrow_text}\n                        </div>\n                    </div>\n            '
        else:
            html += '<p>データなし</p>'
        html += '\n                </div>\n        '
        html += '\n                <div class="section">\n                    <h2>システム状態</h2>\n        '
        if 'system_status' in data:
            status = data['system_status']
            html += f"\n                    <p>動作モード: <strong>{status.get('mode', 'N/A')}</strong></p>\n                    <p>最終更新: {status.get('last_update', 'N/A')}</p>\n                    <p>システム温度: {status.get('temperature', 'N/A')} °C</p>\n            "
        else:
            html += '<p>データなし</p>'
        html += '\n                </div>\n                <div class="footer">\n                    <p>このメールはHANAZONOシステムによって自動送信されています</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        '
        return html

    def send_daily_report(self, data):
        """
        日次レポートをメール送信

        Args:
            data: レポートデータ

        Returns:
            bool: 送信成功の場合True、失敗の場合False
        """
        try:
            now = datetime.datetime.now()
            date_str = self._format_date_jp(now)
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_username')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error('メール設定が不完全です')
                return False
            time_suffix = '(07時)' if 5 <= now.hour < 12 else '(23時)'
            subject = f'HANAZONOシステム状態レポート {date_str} {time_suffix}'
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            text_content = self._generate_text_report(data)
            html_content = self._generate_html_report(data)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(text_part)
            msg.attach(html_part)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            self.logger.info(f'レポートメールを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}')
            return False

    def send_alert(self, title, message, priority='中'):
        """
        アラートメールを送信

        Args:
            title: アラートタイトル
            message: アラート本文
            priority: 優先度（"高", "中", "低"）

        Returns:
            bool: 送信成功の場合True、失敗の場合False
        """
        try:
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_username')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error('メール設定が不完全です')
                return False
            priority_emoji = {'高': '⚠️', '中': 'ℹ️', '低': '📝'}.get(priority, 'ℹ️')
            now = datetime.datetime.now()
            date_str = self._format_date_jp(now)
            time_str = now.strftime('%H:%M:%S')
            subject = f'{priority_emoji} [HANAZONO] {title}'
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            text_content = f'\n===== HANAZONOシステム アラート =====\n日時: {date_str} {time_str}\n優先度: {priority} {priority_emoji}\n\n{message}\n\n---\nこのメールはHANAZONOシステムによって自動送信されています\n'
            html_content = f"""\n<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n    <style>\n        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }}\n        .container {{ max-width: 600px; margin: 0 auto; }}\n        .header {{ background-color: #f0ad4e; color: white; padding: 10px; text-align: center; }}\n        .content {{ margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 5px; }}\n        .footer {{ margin-top: 20px; text-align: center; font-size: 12px; color: #777; }}\n        .priority-high {{ color: #d9534f; }}\n        .priority-medium {{ color: #f0ad4e; }}\n        .priority-low {{ color: #5bc0de; }}\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="header">\n            <h1>{priority_emoji} HANAZONOシステム アラート</h1>\n            <p>{date_str} {time_str}</p>\n        </div>\n        <div class="content">\n            <p><strong>優先度:</strong> <span class="priority-{('high' if priority == '高' else 'medium' if priority == '中' else 'low')}">{priority} {priority_emoji}</span></p>\n            <h2>{title}</h2>\n            <p>{message}</p>\n        </div>\n        <div class="footer">\n            <p>このメールはHANAZONOシステムによって自動送信されています</p>\n        </div>\n    </div>\n</body>\n</html>\n"""
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(text_part)
            msg.attach(html_part)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            self.logger.info(f'アラートメールを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'アラートメール送信エラー: {e}')
            return False
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HANAZONOシステム メール通知機能')
    parser.add_argument('--test', action='store_true', help='テストモードで実行')
    args = parser.parse_args()
    if args.test:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('logs/email_notifier_test.log'), logging.StreamHandler()])
        logger = logging.getLogger('EmailNotifier')
        test_config = {'smtp_server': 'smtp.example.com', 'smtp_port': 465, 'smtp_username': 'test@example.com', 'smtp_password': 'password', 'email_sender': 'hanazono@example.com', 'email_recipients': ['user@example.com']}
        test_data = {'power_data': {'battery_level': 85, 'solar_generation': 520, 'consumption': 320}, 'weather': {'today': '晴れ 後 曇り', 'tomorrow': '雨 のち 曇り'}, 'system_status': {'mode': '自動運転', 'last_update': '2025-05-11 10:15:30', 'temperature': 42.5}}
        notifier = EmailNotifier(test_config, logger)
        logger.info('===== テキストレポートのプレビュー =====')
        text_report = notifier._generate_text_report(test_data)
        logger.info('\n' + text_report)
        logger.info('===== HTMLレポートのプレビュー =====')
        html_report = notifier._generate_html_report(test_data)
        logger.info('\n' + html_report)
        logger.info('===== 天気絵文字テスト =====')
        test_conditions = ['晴れ', '曇り', '雨', '晴れ 後 曇り', 'くもりがち', '霧', 'データなし', '']
        for condition in test_conditions:
            emoji = notifier._format_weather_emojis(condition)
            formatted = notifier._format_weather_line(condition)
            logger.info(f"'{condition}' → '{emoji}' → '{formatted}'")
        logger.info('テスト完了')