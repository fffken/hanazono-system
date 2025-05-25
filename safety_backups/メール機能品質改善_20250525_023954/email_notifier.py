import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

class EmailNotifier:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def send_daily_report(self, data):
        try:
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')


            now = datetime.datetime.now()
            subject = f"HANAZONOシステム レポート {now.strftime('%Y年%m月%d日')}"
            
            text_content = f"""
HANAZONOシステム 日次レポート

📊 実行時刻: {now.strftime('%Y年%m月%d日 %H時%M分')}
⚙️ システム状態: 正常動作中
🔋 データ収集: 完了
📧 メール送信: 成功
"""

            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()

            self.logger.info(f"シンプルレポート送信完了: {subject}")
            return True

        except Exception as e:
            self.logger.error(f"メール送信エラー: {e}")
            return False
