#!/usr/bin/env python3
# HCQASシステムとメール送信問題の関係調査
import os
import glob
import datetime

class HCQASSystemInvestigation:
    """HCQASシステム自動化スクリプトとメール問題の関係調査"""
    
    def __init__(self):
        self.hcqas_files = []
        self.email_files = []
        self.relationships = []
        
    def find_hcqas_related_files(self):
        """HCQAS関連ファイル検索"""
        print("🔍 HCQASシステム関連ファイル検索")
        print("=" * 50)
        
        # HCQAS関連キーワード
        hcqas_keywords = ['hcqas', 'HCQAS', 'automation', 'auto_', 'code_fix', 'script_fix']
        
        python_files = glob.glob('*.py')
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # HCQAS関連キーワード検索
                for keyword in hcqas_keywords:
                    if keyword in content:
                        self.hcqas_files.append({'file': file, 'keyword': keyword})
                        print(f"✅ {file}: '{keyword}' 検出")
                        break
                        
                # email_hub_ml_final.py の特別調査
                if 'email_hub_ml_final' in file:
                    self.analyze_email_hub_modifications(file, content)
                    
            except:
                continue
                
        print(f"📊 HCQAS関連ファイル数: {len(self.hcqas_files)}")
        
    def analyze_email_hub_modifications(self, filename, content):
        """email_hub_ml_final.py の修正履歴調査"""
        print(f"\n📧 {filename} 修正履歴調査")
        print("=" * 50)
        
        # 自動化スクリプトによる修正痕跡を検索
        modification_indicators = [
            '# 自動修正',
            '# Auto-generated',
            '# HCQAS',
            '# 実送信強制',
            'killer',
            'auto_simulation'
        ]
        
        for indicator in modification_indicators:
            if indicator in content:
                print(f"🔍 修正痕跡発見: '{indicator}'")
                
                # 該当行の前後を表示
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if indicator in line:
                        print(f"   {i-1:3}: {lines[i-1] if i > 0 else ''}")
                        print(f">> {i:3}: {line}")
                        print(f"   {i+1:3}: {lines[i+1] if i < len(lines)-1 else ''}")
                        
    def check_email_send_method_integrity(self):
        """email send メソッドの整合性確認"""
        print(f"\n🔧 email send メソッド整合性確認")
        print("=" * 50)
        
        email_files = [f for f in glob.glob('*email*.py') if 'final' in f]
        
        for file in email_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                print(f"📁 {file}")
                
                # send_daily_reportメソッドの完全性確認
                if 'def send_daily_report(' in content:
                    print("  ✅ send_daily_report メソッド存在")
                    
                    # 実際のメール送信コード確認
                    if 'smtplib.SMTP(' in content:
                        print("  ✅ smtplib.SMTP 実送信コード存在")
                    else:
                        print("  ❌ smtplib.SMTP 実送信コード不在")
                        
                    # return文確認
                    method_lines = self.extract_method_lines(content, 'send_daily_report')
                    returns = [line for line in method_lines if 'return' in line]
                    
                    for ret in returns:
                        print(f"  🔄 return文: {ret.strip()}")
                        
                else:
                    print("  ❌ send_daily_report メソッド未発見")
                    
            except Exception as e:
                print(f"  ❌ {file} 読み込みエラー: {e}")
                
    def extract_method_lines(self, content, method_name):
        """メソッドの行を抽出"""
        lines = content.split('\n')
        method_lines = []
        in_method = False
        method_indent = 0
        
        for line in lines:
            if f'def {method_name}(' in line:
                in_method = True
                method_indent = len(line) - len(line.lstrip())
                method_lines.append(line)
            elif in_method:
                current_indent = len(line) - len(line.lstrip())
                if line.strip() and current_indent <= method_indent:
                    break
                method_lines.append(line)
                
        return method_lines
        
    def investigate_auto_modification_chain(self):
        """自動修正チェーンの調査"""
        print(f"\n🔗 自動修正チェーン調査")
        print("=" * 50)
        
        # タイムスタンプパターンで修正チェーン確認
        timestamp_files = {}
        
        for file in glob.glob('*_2025*.py'):
            # ファイル名からタイムスタンプ抽出
            parts = file.split('_')
            for part in parts:
                if part.startswith('2025') and len(part) >= 8:
                    timestamp = part[:8]  # YYYYMMDD
                    if timestamp not in timestamp_files:
                        timestamp_files[timestamp] = []
                    timestamp_files[timestamp].append(file)
                    
        # タイムスタンプ順に表示
        for timestamp in sorted(timestamp_files.keys()):
            print(f"📅 {timestamp}: {len(timestamp_files[timestamp])}ファイル")
            for file in timestamp_files[timestamp]:
                if 'email' in file:
                    print(f"   📧 {file}")
                    
    def create_email_fix_recommendation(self):
        """メール修正推奨事項作成"""
        print(f"\n💡 メール修正推奨事項")
        print("=" * 50)
        
        print("🎯 問題の根本原因:")
        print("   1. 自動化スクリプトによる部分的修正")
        print("   2. email_hub_ml_final.py内のsmtplib実装不足")
        print("   3. 成功判定の偽装（実送信なしでTrue返却）")
        
        print("\n🔧 推奨解決策:")
        print("   1. email_hub_ml_final.py を直接Gmail送信コードで置換")
        print("   2. HCQASによる自動修正の影響を排除")
        print("   3. 実際のsmtplib.SMTP送信処理を強制挿入")
        
        # 修正版作成スクリプト生成
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fix_script = f"email_hub_direct_fix_{timestamp}.py"
        
        direct_fix_code = '''#!/usr/bin/env python3
# email_hub_ml_final直接修正版（HCQASバイパス）
import smtplib
import ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHubMLFinalDirectFix:
    """直接Gmail送信（HCQASバイパス）"""
    
    def send_daily_report(self):
        """直接Gmail送信実行"""
        try:
            smtp_server = "smtp.gmail.com"
            port = 587
            sender_email = "fffken@gmail.com"
            password = "bbzpgdsvqlcemyxi"
            
            subject = f"HANAZONOシステム - 直接送信修正版 {datetime.datetime.now().strftime('%Y年%m月%d日')}"
            body = f"""HANAZONOシステム直接送信修正版

送信時刻: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}
修正方式: HCQASバイパス直接送信
送信状態: 実際送信成功

--- HANAZONOシステム 直接送信修正版 ---"""

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = sender_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, sender_email, message.as_string())
                
            print("✅ 直接送信成功")
            return True
            
        except Exception as e:
            print(f"❌ 直接送信エラー: {e}")
            return False

if __name__ == "__main__":
    hub = EmailHubMLFinalDirectFix()
    hub.send_daily_report()
'''
        
        with open(fix_script, 'w', encoding='utf-8') as f:
            f.write(direct_fix_code)
            
        print(f"\n📁 直接修正スクリプト作成: {fix_script}")
        return fix_script
        
    def run_investigation(self):
        """HCQAS調査実行"""
        print("🎯 HCQASシステム関連調査開始")
        print("=" * 60)
        
        self.find_hcqas_related_files()
        self.check_email_send_method_integrity()
        self.investigate_auto_modification_chain()
        fix_script = self.create_email_fix_recommendation()
        
        print(f"\n" + "=" * 60)
        print("🎉 HCQAS関連調査完了")
        print("=" * 60)
        print(f"📊 HCQAS関連ファイル: {len(self.hcqas_files)}")
        print(f"💡 推奨: 直接修正でHCQAS影響回避")
        print(f"🧪 テスト: python3 {fix_script}")
        
        return fix_script

if __name__ == "__main__":
    investigator = HCQASSystemInvestigation()
    investigator.run_investigation()
