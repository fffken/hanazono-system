#!/usr/bin/env python3
# HANAZONOメールシステム実データ統合版（文字修復）
import os
import json
import datetime
import smtplib
import ssl
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_real_battery_data():
    """実際のバッテリーデータ取得"""
    try:
        json_files = glob.glob('data/collected_data_*.json')
        if not json_files:
            return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}
            
        latest_file = max(json_files, key=lambda x: os.path.getctime(x))
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        latest_record = data[0] if isinstance(data, list) else data
        params = latest_record.get('parameters', {})
        
        result = {}
        if '0x0100' in params:
            soc_data = params['0x0100']
            result['soc'] = soc_data.get('value', soc_data.get('raw_value', '取得失敗'))
        else:
            result['soc'] = '取得失敗'
            
        if '0x0101' in params:
            voltage_data = params['0x0101']
            result['voltage'] = voltage_data.get('value', voltage_data.get('raw_value', '取得失敗'))
        else:
            result['voltage'] = '取得失敗'
            
        result['timestamp'] = latest_record.get('datetime', '取得失敗')
        return result
        
    except Exception as e:
        return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}

class HANAZONOCompleteSystem:
    """HANAZONOシステム完全版（実データ統合）"""
    
    def __init__(self):
        self.modules = {}
        self.initialize_system()
        
    def initialize_system(self):
        """システム初期化"""
        try:
            from email_hub_ml_integration_v2_1 import EmailHubMLIntegration
            self.modules["email_hub_ml"] = EmailHubMLIntegration()
            print("✅ Email Hub ML統合成功")
        except ImportError:
            print("⚠️ Email Hub ML統合警告: モジュール未発見")
            
        print("🚀 HANAZONOシステム v4.0.0-COMPLETE-FINAL 初期化完了")
        
    def run_daily_optimization(self):
        """日次最適化実行（実データ統合版）"""
        try:
            # 実データ取得
            real_data = get_real_battery_data()
            
            print(f"🌅 日次最適化開始: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            results = {}
            
            # メール送信実行
            if "email_hub_ml" in self.modules:
                email_result = self.modules["email_hub_ml"].send_daily_report_with_real_data(real_data)
                results["email_report"] = {"success": email_result, "timestamp": datetime.datetime.now().isoformat()}
                print(f"📧 メールレポート: {'✅ 実際送信成功' if email_result else '❌ 失敗'}")
            else:
                # フォールバック：直接メール送信
                email_result = self.send_direct_email_with_real_data(real_data)
                results["email_report"] = {"success": email_result, "timestamp": datetime.datetime.now().isoformat()}
                print(f"📧 メールレポート: {'✅ 実際送信成功' if email_result else '❌ 失敗'}")
        else:
            result['voltage'] = '取得失敗'
            
        result['timestamp'] = latest_record.get('datetime', '取得失敗')
        return result
        
    except Exception as e:
        return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}

class HANAZONOCompleteSystem:
    """HANAZONOシステム完全版（実データ統合）"""
    
    def __init__(self):
        self.modules = {}
        self.initialize_system()
        
    def initialize_system(self):
        """システム初期化"""
        try:
            from email_hub_ml_integration_v2_1 import EmailHubMLIntegration
            self.modules["email_hub_ml"] = EmailHubMLIntegration()
            print("✅ Email Hub ML統合成功")
        except ImportError:
            print("⚠️ Email Hub ML統合警告: モジュール未発見")
            
        print("🚀 HANAZONOシステム v4.0.0-COMPLETE-FINAL 初期化完了")
        
    def run_daily_optimization(self):
        """日次最適化実行（実データ統合版）"""
        try:
            # 実データ取得
            real_data = get_real_battery_data()
            
            print(f"🌅 日次最適化開始: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            results = {}
            
            # メール送信実行
            if "email_hub_ml" in self.modules:
                email_result = self.modules["email_hub_ml"].send_daily_report()
                results["email_report"] = {"success": email_result, "timestamp": datetime.datetime.now().isoformat()}
                print(f"📧 メールレポート: {'✅ 実際送信成功' if email_result else '❌ 失敗'}")
            else:
                # フォールバック：直接メール送信
                email_result = self.send_direct_email_with_real_data(real_data)
                results["email_report"] = {"success": email_result, "timestamp": datetime.datetime.now().isoformat()}
                print(f"📧 メールレポート: {'✅ 実際送信成功' if email_result else '❌ 失敗'}")
            
            print("🎉 日次最適化完了: 総合成功")
            return results
            
        except Exception as e:
            print(f"❌ 日次最適化エラー: {e}")
            return {"error": str(e)}
    
    def send_direct_email_with_real_data(self, real_data):
        """実データ統合直接メール送信"""
        try:
            # Gmail設定
            smtp_server = "smtp.gmail.com"
            port = 587
            sender_email = "fffken@gmail.com"
            password = "mrph lkec ovka rjmf"
            receiver_email = "fffken@gmail.com"
            
            # メール本文作成（実データ統合）
            subject = f"HANAZONOシステム - 実データ統合レポート {datetime.datetime.now().strftime('%Y年%m月%d日')}"
            
            body = f"""HANAZONOシステム実データ統合レポート {datetime.datetime.now().strftime('%Y年%m月%d日 (%H時)')}
            
バッテリー残量: {real_data['soc']}%
電圧: {real_data['voltage']}V
取得時刻: {real_data['timestamp']}

--- HANAZONOシステム 実データ統合版 ---"""
            
            # メール送信
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"メール送信エラー: {e}")
            return False

if __name__ == "__main__":
    system = HANAZONOCompleteSystem()
    system.run_daily_optimization()
