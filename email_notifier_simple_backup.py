#!/usr/bin/env python3
"""
メール通知システム - 強化版
完全構文エラーフリー設計
"""
import os
import sys
import json
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from settings_manager import SettingsManager
    SETTINGS_AVAILABLE = True
except ImportError:
    print("警告: settings_manager import失敗")
    SETTINGS_AVAILABLE = False

class EmailNotifier:
    """メール通知クラス"""
    
    def __init__(self, config=None):
        self.logger = self._setup_logger()
        
        if config:
            self.config = config
        elif SETTINGS_AVAILABLE:
            try:
                manager = SettingsManager()
                self.config = manager.get_email_config()
            except Exception as e:
                self.logger.error(f"設定取得エラー: {str(e)}")
                self.config = self._get_default_config()
        else:
            self.config = self._get_default_config()
        
        self.logger.info("EmailNotifier初期化完了")
    
    def _setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('email_notifier')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _get_default_config(self):
        """デフォルト設定"""
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': 'fffken@gmail.com',
            'smtp_password': os.getenv('SMTP_PASSWORD', ''),
            'sender': 'fffken@gmail.com',
            'recipients': ['fffken@gmail.com']
        }
    
    def _expand_env_vars(self, text):
        """環境変数展開"""
        if isinstance(text, str) and text.startswith('${') and text.endswith('}'):
            var_name = text[2:-1]
            return os.getenv(var_name, text)
        return text
    
    def send_test_email(self):
        """テストメール送信"""
        subject = f"HANAZONOシステム テストメール - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
HANAZONOシステム テストメール

送信時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
システム状態: 正常動作中

このメールはシステムの動作確認のために送信されました。

---
HANAZONO自動最適化システム
"""
        
        return self.send_email(subject, body)
    
    def send_daily_report(self, data=None):
        """日次レポート送信"""
        subject = f"HANAZONOシステム 日次レポート - {datetime.now().strftime('%Y-%m-%d')}"
        
        if data:
            body = self._generate_report_body(data)
        else:
            body = f"""
HANAZONOシステム 日次レポート

レポート日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

システム状態: 正常動作中
データ収集: 継続中

詳細なデータ分析機能は開発中です。

---
HANAZONO自動最適化システム
"""
        
        return self.send_email(subject, body)
    
    def _generate_report_body(self, data):
        """レポート本文生成"""
        report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        body = f"""
HANAZONOシステム 詳細レポート

レポート生成時刻: {report_time}
データ取得時刻: {data.get('datetime', 'Unknown')}

【収集データ】
"""
        
        if 'parameters' in data:
            for param_data in data['parameters'].values():
                name = param_data.get('name', 'Unknown')
                value = param_data.get('formatted_value', 'N/A')
                unit = param_data.get('unit', '')
                emoji = param_data.get('emoji', '')
                
                body += f"{emoji} {name}: {value}{unit}\n"
        
        body += f"""

【システム情報】
インバーターIP: {data.get('ip_address', 'Unknown')}
データファイル: 自動保存済み

---
HANAZONO自動最適化システム
"""
        
        return body
    
    def send_error_alert(self, error_message):
        """エラーアラート送信"""
        subject = f"🚨 HANAZONOシステム エラーアラート - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
🚨 HANAZONOシステム エラーアラート

発生時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
エラー内容: {error_message}

システム管理者による確認が必要です。

---
HANAZONO自動最適化システム
"""
        
        return self.send_email(subject, body)
    
    def send_email(self, subject, body):
        """メール送信基本機能"""
        try:
            # 設定値を取得・展開
            smtp_server = self.config.get('smtp_server')
            smtp_port = int(self.config.get('smtp_port', 587))
            username = self._expand_env_vars(self.config.get('smtp_user'))
            password = self._expand_env_vars(self.config.get('smtp_password'))
            sender = self._expand_env_vars(self.config.get('sender'))
            recipients = self.config.get('recipients', [])
            
            if not all([smtp_server, username, password, sender, recipients]):
                self.logger.error("メール設定が不完全です")
                return False
            
            # メッセージ作成
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTP送信
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            
            text = msg.as_string()
            server.sendmail(sender, recipients, text)
            server.quit()
            
            self.logger.info(f"メール送信成功: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"メール送信エラー: {str(e)}")
            return False

def test_email_system():
    """メールシステムテスト"""
    print("🧪 メールシステムテスト開始")
    
    try:
        notifier = EmailNotifier()
        print("✅ EmailNotifier初期化成功")
        
        # 設定確認
        if notifier.config.get('smtp_password'):
            print("✅ SMTP設定確認済み")
        else:
            print("⚠️ SMTP_PASSWORD環境変数が未設定")
        
        # テストメール送信（実際は送信しない）
        print("✅ テストメール機能準備完了")
        print("ℹ️ 実際の送信は --send-test-email オプションで実行してください")
        
        print("🎉 メールシステムテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ メールシステムテストエラー: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="メール通知システムテスト")
    parser.add_argument('--send-test-email', action='store_true', help='実際にテストメールを送信')
    parser.add_argument('--send-daily-report', action='store_true', help='日次レポートを送信')
    
    args = parser.parse_args()
    
    if args.send_test_email:
        notifier = EmailNotifier()
        success = notifier.send_test_email()
        print("✅ テストメール送信成功" if success else "❌ テストメール送信失敗")
    elif args.send_daily_report:
        notifier = EmailNotifier()
        success = notifier.send_daily_report()
        print("✅ 日次レポート送信成功" if success else "❌ 日次レポート送信失敗")
    else:
        test_email_system()
