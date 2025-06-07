import os
import sys
import json
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def expand_env_vars(config):
    if isinstance(config, dict): return {k: expand_env_vars(v) for k, v in config.items()}
    if isinstance(config, list): return [expand_env_vars(i) for i in config]
    if isinstance(config, str): return os.path.expandvars(config)
    return config

class EnhancedEmailNotifier:
    def __init__(self, settings, logger=None):
        self.settings = expand_env_vars(settings)
        # 唯一の正しい場所からメール設定を読み込む
        self.email_config = self.settings.get('notification', {}).get('email', {})
        self.logger = logger if logger else logging.getLogger('email_notifier_v2')

    def send_daily_report(self, data, test_mode=False):
        try:
            if not self.email_config:
                self.logger.error('設定に"notification.email"キーが見つかりません。')
                return False
            
            required = ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'email_sender', 'email_recipients']
            if not all(self.email_config.get(k) for k in required):
                self.logger.error('メール設定が不完全です。')
                return False

            subject_template = self.email_config.get('template', {}).get('subject', 'システムレポート')
            subject = subject_template.format(timestamp=datetime.now().strftime('%Y-%m-%d'))
            
            if test_mode:
                self.logger.info("テストモードのため、メール送信をスキップしました。")
                self.logger.info(f"件名: {subject}")
                return True

            # 本番メール送信ロジック（現在はテストモードでスキップされる）
            content = "本番レポート内容"
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email_sender']
            msg['To'] = ", ".join(self.email_config['email_recipients'])
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            
            self.logger.info(f'最適化レポートを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信で予期せぬエラー: {e}', exc_info=True)
            return False

def test_email_system():
    print("📧 Enhanced Email System v2.2 テスト開始")
    print("=" * 60)
    settings = {}
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except Exception as e:
        print(f"⚠️ 設定ファイル読み込みエラー: {e}")
        return False
    
    notifier = EnhancedEmailNotifier(settings)
    success = notifier.send_daily_report({}, test_mode=True)

    if success:
        print("\n✅ メールシステムテスト完了")
    else:
        print("\n❌ メールシステムテスト失敗")
    return success

if __name__ == "__main__":
    test_email_system()
