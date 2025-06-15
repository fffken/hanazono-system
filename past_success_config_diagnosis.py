#!/usr/bin/env python3
# 過去成功設定完全診断（完全非破壊的）
import os
import json
import datetime

class PastSuccessConfigDiagnosis:
    """過去成功時の設定完全診断（元ファイル完全保護）"""
    
    def __init__(self):
        self.diagnosis_results = {}
        self.working_config = None
        
    def diagnose_settings_files(self):
        """設定ファイル診断"""
        print("🔍 設定ファイル完全診断")
        print("=" * 50)
        
        # 1. settings.json確認
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                self.diagnosis_results['settings_json'] = settings_data
                print("✅ settings.json読み込み成功")
                
                # メール関連設定確認
                if 'email' in settings_data:
                    print(f"✅ email設定発見: {list(settings_data['email'].keys())}")
                else:
                    print("⚠️ email設定未発見")
                    
            except Exception as e:
                print(f"❌ settings.json読み込みエラー: {e}")
                self.diagnosis_results['settings_json'] = None
        else:
            print("❌ settings.json未発見")
            self.diagnosis_results['settings_json'] = None
            
        # 2. email_config.py確認
        if os.path.exists('email_config.py'):
            try:
                with open('email_config.py', 'r', encoding='utf-8') as f:
                    config_content = f.read()
                self.diagnosis_results['email_config_py'] = config_content
                print("✅ email_config.py読み込み成功")
                
                # パスワード情報確認
                if 'password' in config_content.lower():
                    print("✅ パスワード設定発見")
                    
            except Exception as e:
                print(f"❌ email_config.py読み込みエラー: {e}")
                self.diagnosis_results['email_config_py'] = None
        else:
            print("❌ email_config.py未発見")
            self.diagnosis_results['email_config_py'] = None
            
    def analyze_working_email_file(self):
        """動作確認済みメールファイル解析"""
        print("\n🔍 過去成功メールファイル解析")
        print("=" * 50)
        
        # 過去成功ファイルリスト
        working_files = [
            'email_notifier_SAFE_WORKING_20250604_003408.py',
            'email_notifier_SAFE_WORKING_20250604_003114.py',
            'email_notifier_simple_backup_20250604_002433.py'
        ]
        
        for filename in working_files:
            if os.path.exists(filename):
                print(f"📋 {filename} 解析中...")
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 設定取得方法確認
                    if 'self.config.get(' in content:
                        print(f"✅ {filename}: config.get()方式使用")
                        
                        # 具体的な設定確認
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'smtp_password' in line or 'password' in line:
                                print(f"   設定行{i+1}: {line.strip()}")
                                
                        self.working_config = {'file': filename, 'method': 'config.get'}
                        break
                        
                except Exception as e:
                    print(f"❌ {filename} 読み込みエラー: {e}")
                    
        if not self.working_config:
            print("❌ 動作確認済み設定ファイル未発見")
            
    def extract_working_email_config(self):
        """動作する設定情報抽出"""
        print(f"\n🔧 動作する設定情報抽出")
        print("=" * 50)
        
        if not self.working_config:
            print("❌ 動作設定未発見")
            return None
            
        try:
            # 設定情報を安全に抽出
            config_data = {}
            
            # settings.jsonから抽出
            if self.diagnosis_results.get('settings_json'):
                settings = self.diagnosis_results['settings_json']
                if 'email' in settings:
                    email_settings = settings['email']
                    config_data.update({
                        'smtp_server': email_settings.get('smtp_server'),
                        'smtp_port': email_settings.get('smtp_port'),
                        'smtp_user': email_settings.get('smtp_user'),
                        'smtp_password': email_settings.get('smtp_password')
                    })
                    
            print("✅ 動作設定抽出成功")
            for key, value in config_data.items():
                if 'password' in key:
                    print(f"   {key}: {'*' * len(str(value)) if value else 'None'}")
                else:
                    print(f"   {key}: {value}")
                    
            return config_data
            
        except Exception as e:
            print(f"❌ 設定抽出エラー: {e}")
            return None
            
    def create_working_email_system(self, config_data):
        """動作する設定でメールシステム作成"""
        print(f"\n📧 動作設定メールシステム作成")
        print("=" * 50)
        
        if not config_data:
            print("❌ 設定データなし")
            return None
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"hanazono_working_config_email_{timestamp}.py"
        
        # 動作確認済み設定を使用したメールシステム
        email_system_code = f'''#!/usr/bin/env python3
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
        self.config = {{
            'smtp_server': '{config_data.get("smtp_server", "smtp.gmail.com")}',
            'smtp_port': {config_data.get("smtp_port", 587)},
            'smtp_user': '{config_data.get("smtp_user", "fffken@gmail.com")}',
            'smtp_password': '{config_data.get("smtp_password", "")}'
        }}
        
    def get_battery_data(self):
        """バッテリーデータ取得"""
        try:
            json_files = glob.glob('data/collected_data_*.json')
            if not json_files:
                return {{'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}}
            latest_file = max(json_files, key=lambda x: os.path.getctime(x))
            with open(latest_file, 'r') as f:
                data = json.load(f)
            record = data[0] if isinstance(data, list) else data
            params = record.get('parameters', {{}})
            
            result = {{}}
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
            return {{'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}}
            
    def send_working_config_email(self):
        """動作設定でメール送信"""
        try:
            battery_data = self.get_battery_data()
            
            subject = f"【動作設定確認】HANAZONOシステム {datetime.datetime.now().strftime('%Y年%m月%d日')}"
            
            body = f"""HANAZONOシステム 動作設定確認レポート

🔋 バッテリー状況（実データ）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

バッテリー残量: {{battery_data['soc']}}%
電圧: {{battery_data['voltage']}}V
取得時刻: {{battery_data['timestamp']}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 設定確認
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

設定方式: 動作確認済み設定使用
SMTP: {{self.config['smtp_server']}}:{{self.config['smtp_port']}}
ユーザー: {{self.config['smtp_user']}}

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
                
            print(f"✅ 動作設定メール送信成功: {{datetime.datetime.now().isoformat()}}")
            return True
            
        except Exception as e:
            print(f"❌ 動作設定メール送信エラー: {{e}}")
            return False
            
if __name__ == "__main__":
    system = HANAZONOWorkingConfigEmail()
    system.send_working_config_email()
'''
        
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(email_system_code)
            
        print(f"✅ 動作設定メールシステム作成: {new_filename}")
        return new_filename
        
    def run_complete_diagnosis(self):
        """完全診断実行"""
        print("🎯 過去成功設定完全診断開始（完全非破壊的）")
        print("=" * 60)
        
        # 1. 設定ファイル診断
        self.diagnose_settings_files()
        
        # 2. 動作確認済みファイル解析
        self.analyze_working_email_file()
        
        # 3. 動作設定抽出
        config_data = self.extract_working_email_config()
        
        # 4. 動作設定メールシステム作成
        working_system_file = self.create_working_email_system(config_data)
        
        print(f"\n" + "=" * 60)
        print("🎉 過去成功設定診断完了")
        print("=" * 60)
        print("✅ 完全非破壊的保証: 元ファイル無変更")
        
        if working_system_file:
            print(f"✅ 動作設定システム: {working_system_file}")
            print(f"\n🧪 テスト実行:")
            print(f"   python3 {working_system_file}")
        else:
            print("❌ 動作設定システム作成失敗")
            
        return working_system_file

if __name__ == "__main__":
    diagnosis = PastSuccessConfigDiagnosis()
    diagnosis.run_complete_diagnosis()
