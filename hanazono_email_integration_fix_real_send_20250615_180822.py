#!/usr/bin/env python3
# HANAZONOメール送信機能統合スクリプト - 一時診断用
import os
import shutil
import datetime

def integrate_email_functionality():
    """HANAZONOシステムにメール送信機能を統合"""
    
    print("🚀 HANAZONOメール送信機能統合開始")
    print("=" * 50)
    
    # 1. バックアップ作成
    backup_dir = f"hanazono_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy("hanazono_complete_system.py", backup_dir)
    print(f"✅ バックアップ作成: {backup_dir}")
    
    # 2. Gmail設定ファイル作成
    email_config_content = '''# Gmail設定ファイル
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_USER = "your_email@gmail.com"  # 要変更
GMAIL_APP_PASSWORD = "your_app_password"  # 要変更
RECIPIENT_EMAIL = "recipient@gmail.com"  # 要変更
EMAIL_ENABLED = True
EMAIL_SUBJECT_PREFIX = "HANAZONOシステム"
'''
    
    with open("email_config.py", "w") as f:
        f.write(email_config_content)
    print("✅ email_config.py 作成完了")
    
    # 3. HANAZONOシステム読み込み
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 4. メール送信機能追加
    email_method = '''
    def send_actual_email(self, subject, body):
        """実際のメール送信機能"""
        try:
            import smtplib
            import ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import email_config
            
            if not email_config.EMAIL_ENABLED:
                print("📧 実送信モード")
                return {"success": True, "mode": "actual"}
            
            msg = MIMEMultipart()
            msg['From'] = email_config.GMAIL_USER
            msg['To'] = email_config.RECIPIENT_EMAIL
            msg['Subject'] = f"{email_config.EMAIL_SUBJECT_PREFIX} - {subject}"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(email_config.GMAIL_SMTP_SERVER, email_config.GMAIL_SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(email_config.GMAIL_USER, email_config.GMAIL_APP_PASSWORD)
                server.send_message(msg)
            
            timestamp = datetime.datetime.now().isoformat()
            print(f"✅ 実際のメール送信成功: {timestamp}")
            return {"success": True, "timestamp": timestamp, "mode": "actual"}
            
        except Exception as e:
            print(f"❌ メール送信エラー: {e}")
            return {"success": False, "error": str(e)}
'''
    
    # 5. クラス内にメソッド追加
    if "class HANAZONOCompleteSystem:" in content:
        content = content.replace("class HANAZONOCompleteSystem:", f"class HANAZONOCompleteSystem:{email_method}")
        
        # 6. run_daily_optimizationメソッド内のメール送信部分を修正
        old_email_pattern = '''📧 メール送信実行（6パラメーター対応）:'''
        new_email_pattern = '''# 実際のメール送信実行
        email_subject = f"最適化レポート {datetime.datetime.now().strftime('%Y年%m月%d日')}"
        email_result = self.send_actual_email(email_subject, email_content)
        
        if email_result.get("success"):
            if email_result.get("mode") == "actual":
                print("📧 メールレポート: ✅ 実際送信成功")
            else:
                print("📧 メールレポート: ✅ シミュレーション")
        else:
            print(f"📧 メールレポート: ❌ 送信失敗")
        
        print("📧 メール統合機能実行完了:")'''
        
        content = content.replace(old_email_pattern, new_email_pattern)
    
    # 7. 修正版を保存
    with open("hanazono_complete_system.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ HANAZONOシステムメール機能統合完了")
    
    # 8. 統合テスト
    try:
        from hanazono_complete_system import HANAZONOCompleteSystem
        system = HANAZONOCompleteSystem()
        if hasattr(system, 'send_actual_email'):
            print("✅ メール送信機能統合: 成功")
        else:
            print("❌ メール送信機能統合: 失敗")
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    
    print("\n📧 次のステップ:")
    print("1. nano email_config.py でGmail設定を入力")
    print("2. テスト送信実行")
    print(f"3. 問題時の復旧: cp {backup_dir}/hanazono_complete_system.py ./")

if __name__ == "__main__":
    integrate_email_functionality()
