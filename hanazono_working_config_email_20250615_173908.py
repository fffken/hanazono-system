#!/usr/bin/env python3
# HANAZONO動作設定メールシステム（完全非破壊的）
import datetime
import smtplib
import ssl
import glob
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class HANAZONOWorkingConfigEmail:
    """動作確認済み設定を使用したメールシステム"""
    
    def __init__(self):
        # 動作確認済み設定
        self.config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': 'None',
            'smtp_password': 'None'
        }
        
    def get_battery_data(self):
        """バッテリーデータ取得"""
        try:
            json_files = glob.glob('data/collected_data_*.json')
            if not json_files:
                return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}
            latest_file = max(json_files, key=lambda x: os.path.getctime(x))
            with open(latest_file, 'r') as f:
                data = json.load(f)
            record = data[0] if isinstance(data, list) else data
            params = record.get('parameters', {})
            
            result = {}
            if '0x0100' in params:
                soc_data = params['0x0100']
                result['soc'] = soc_data.get('value', soc_data.get('raw_value', '取得失敗'))
            if '0x0101' in params:
                voltage_data = params['0x0101']
                voltage_raw = voltage_data.get('value', voltage_data.get('raw_value', '取得失敗'))
                result['voltage'] = round(float(voltage_raw), 1) if voltage_raw != '取得失敗' else '取得失敗'
            result['timestamp'] = record.get('datetime', '取得失敗')
            
            return result
        except:
            return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}
            
    def send_working_config_email(self):
        """動作設定でメール送信"""
        try:
            battery_data = self.get_battery_data()
            
            subject = f"【動作設定確認】HANAZONOシステム 2025年06月15日"
            
            body = f"""HANAZONOシステム 動作設定確認レポート

🔋 バッテリー状況（実データ）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

バッテリー残量: {battery_data['soc']}%
電圧: {battery_data['voltage']}V
取得時刻: {battery_data['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 設定確認
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

設定方式: 動作確認済み設定使用
SMTP: {self.config['smtp_server']}:{self.config['smtp_port']}
ユーザー: {self.config['smtp_user']}

--- HANAZONOシステム 動作設定版 ---"""

            message = MIMEMultipart()
            message["From"] = self.config['smtp_user']
            message["To"] = self.config['smtp_user']
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.config['smtp_user'], self.config['smtp_password'])
                server.sendmail(self.config['smtp_user'], self.config['smtp_user'], message.as_string())
                
            print(f"✅ 動作設定メール送信成功: {datetime.datetime.now().isoformat()}")
            return True
            
        except Exception as e:
            print(f"❌ 動作設定メール送信エラー: {e}")
            return False
            
if __name__ == "__main__":
    system = HANAZONOWorkingConfigEmail()
    system.send_working_config_email()
