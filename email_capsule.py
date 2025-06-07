import smtplib
import logging
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 設定データをコード内に直接埋め込む ---
SETTINGS_DATA = {
    "notification": {
        "email": {
            "enabled": True,
            "template": {
                "subject": "【ソーラー蓄電システム】日次レポート - {timestamp}"
            },
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_user": "fffken@gmail.com",
            "smtp_password": os.environ.get('SMTP_PASSWORD', ''), # 環境変数から取得
            "email_sender": "fffken@gmail.com",
            "email_recipients": ["fffken@gmail.com"]
        }
    }
}

def send_email_report():
    """メールレポートを送信する自己完結型関数"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('email_capsule')
    
    email_config = SETTINGS_DATA.get('notification', {}).get('email', {})
    
    try:
        email_config['smtp_password'] = os.path.expandvars(email_config.get('smtp_password', ''))

        required = ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'email_sender', 'email_recipients']
        if not all(email_config.get(k) for k in required):
            logger.error('メール設定が不完全です。SMTPパスワードが環境変数に設定されているか確認してください。')
            return False

        subject_template = email_config.get('template', {}).get('subject', 'システムレポート')
        subject = subject_template.format(timestamp=datetime.now().strftime('%Y-%m-%d'))
        
        # 本番ではここで完全なレポート内容を生成する
        content = f"これは{datetime.now().strftime('%Y年%m月%d日')}の日次レポートです。\n\n（現在テスト中のため、内容は簡略化されています）"

        msg = MIMEMultipart()
        msg['From'] = email_config['email_sender']
        msg['To'] = ", ".join(email_config['email_recipients'])
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 実際のメール送信はコメントアウト（テスト時は不要）
        # with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        #     server.starttls()
        #     server.login(email_config['smtp_user'], email_config['smtp_password'])
        #     server.sendmail(msg['From'], msg['To'], msg.as_string())

        logger.info("メールレポート生成成功（テストモード）。")
        logger.info(f"件名: {subject}")
        return True
        
    except Exception as e:
        logger.error(f'メールレポート生成中にエラー: {e}', exc_info=True)
        return False

if __name__ == "__main__":
    print("--- 📧 メール通知カプセル実行 ---")
    if send_email_report():
        print("✅ 正常に処理が完了しました。")
    else:
        print("❌ 処理中にエラーが発生しました。")
