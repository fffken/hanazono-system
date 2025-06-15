#!/usr/bin/env python3
# メールシステム実データ統合修正版作成スクリプト
import os
import datetime
import shutil

class EmailSystemRealDataIntegration:
    """メールシステムに実データ統合機能を追加"""
    
    def __init__(self):
        self.backup_files = []
        self.integration_success = False
        
    def backup_current_system(self):
        """現在のメールシステムをバックアップ"""
        print("💾 現在のメールシステムバックアップ")
        print("=" * 50)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # バックアップ対象ファイル
        email_files = [
            'hanazono_complete_system.py',
            'email_notifier_v2_1.py',
            'ultimate_email_integration.py'
        ]
        
        for filename in email_files:
            if os.path.exists(filename):
                backup_name = f"{filename}.backup_{timestamp}"
                shutil.copy2(filename, backup_name)
                self.backup_files.append(backup_name)
                print(f"✅ バックアップ: {filename} → {backup_name}")
            else:
                print(f"⚠️ ファイル未発見: {filename}")
                
        print(f"🎉 バックアップ完了: {len(self.backup_files)}ファイル")
        return len(self.backup_files) > 0
        
    def create_integrated_email_system(self):
        """実データ統合メールシステム作成"""
        print("\n📧 実データ統合メールシステム作成")
        print("=" * 50)
        
        # 現在のメールシステムを読み込み
        source_file = None
        for filename in ['hanazono_complete_system.py', 'email_notifier_v2_1.py']:
            if os.path.exists(filename):
                source_file = filename
                break
                
        if not source_file:
            print("❌ メールシステムファイル未発見")
            return None
            
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            print(f"✅ 元ファイル読み込み: {source_file}")
            
            # 実データ取得機能を統合
            integrated_content = self.integrate_real_data_function(original_content)
            
            # 新しいファイルとして保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"hanazono_email_real_data_integrated_{timestamp}.py"
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(integrated_content)
                
            print(f"✅ 統合版作成: {new_filename}")
            return new_filename
            
        except Exception as e:
            print(f"❌ 統合版作成失敗: {e}")
            return None
            
    def integrate_real_data_function(self, original_content):
        """実データ取得機能を統合"""
        
        # 実データ取得関数
        real_data_function = '''
def get_real_battery_data():
    """実際のバッテリーデータ取得"""
    import json
    import glob
    import os
    
    try:
        # 最新データファイル取得
        json_files = glob.glob('data/collected_data_*.json')
        if not json_files:
            return None
            
        latest_file = max(json_files, key=os.path.getctime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 最新レコード取得
        latest_record = data[0] if isinstance(data, list) else data
        params = latest_record.get('parameters', {})
        
        # バッテリーデータ抽出
        battery_info = {}
        
        # SOC
        if '0x0100' in params:
            soc = params['0x0100']
            battery_info['soc'] = soc.get('value', soc.get('raw_value', 0))
            
        # 電圧
        if '0x0101' in params:
            voltage = params['0x0101']
            battery_info['voltage'] = voltage.get('value', voltage.get('raw_value', 0))
            
        # 電流
        if '0x0102' in params:
            current = params['0x0102']
            battery_info['current'] = current.get('value', current.get('raw_value', 0))
        else:
            battery_info['current'] = None
            
        battery_info['timestamp'] = latest_record.get('datetime', 'Unknown')
        
        return battery_info
        
    except Exception as e:
        print(f"バッテリーデータ取得エラー: {e}")
        return None

'''
        
        # 元のコンテンツに実データ取得機能を追加
        # 1. import文の後に実データ取得関数を挿入
        lines = original_content.split('\n')
        insert_position = 0
        
        # import文の最後を見つける
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                insert_position = i + 1
                
        # 実データ取得関数を挿入
        lines.insert(insert_position, real_data_function)
        
        # 2. メール本文生成部分を修正
        modified_lines = []
        for line in lines:
            # 固定値のバッテリー情報を実データに置換
            if 'バッテリー残量: 取得中%' in line or 'バッテリー残量: 取得失敗%' in line:
                modified_lines.append(line.replace(
                    'バッテリー残量: 取得中%',
                    'バッテリー残量: {real_data.get("soc", "取得失敗")}%'
                ).replace(
                    'バッテリー残量: 取得失敗%',
                    'バッテリー残量: {real_data.get("soc", "取得失敗")}%'
                ))
            elif '電圧: 取得中V' in line or '電圧: 取得失敗V' in line:
                modified_lines.append(line.replace(
                    '電圧: 取得中V',
                    '電圧: {real_data.get("voltage", "取得失敗")}V'
                ).replace(
                    '電圧: 取得失敗V', 
                    '電圧: {real_data.get("voltage", "取得失敗")}V'
                ))
            elif '電流: 取得中A' in line or '電流: 取得失敗A' in line:
                modified_lines.append(line.replace(
                    '電流: 取得中A',
                    '電流: {real_data.get("current", "N/A") if real_data.get("current") is not None else "N/A"}A'
                ).replace(
                    '電流: 取得失敗A',
                    '電流: {real_data.get("current", "N/A") if real_data.get("current") is not None else "N/A"}A'
                ))
            elif '取得時刻: 取得失敗' in line:
                modified_lines.append(line.replace(
                    '取得時刻: 取得失敗',
                    '取得時刻: {real_data.get("timestamp", "取得失敗")}'
                ))
            else:
                modified_lines.append(line)
                
        # 3. メール送信関数内で実データ取得を呼び出す
        final_lines = []
        for line in modified_lines:
            if 'def send_' in line and 'report' in line:
                final_lines.append(line)
                final_lines.append('        # 実データ取得')
                final_lines.append('        real_data = get_real_battery_data() or {}')
            else:
                final_lines.append(line)
                
        return '\n'.join(final_lines)
        
    def create_test_email_script(self, integrated_filename):
        """テスト用メール送信スクリプト作成"""
        print(f"\n🧪 テスト用メール送信スクリプト作成")
        print("=" * 50)
        
        test_script = f'''#!/usr/bin/env python3
# 実データ統合メールシステムテスト
import sys
import os

# 統合版メールシステムをインポート
sys.path.insert(0, '.')

try:
    from {integrated_filename[:-3]} import *
    
    print("🧪 実データ統合メールテスト開始")
    print("=" * 50)
    
    # バッテリーデータ取得テスト
    battery_data = get_real_battery_data()
    if battery_data:
        print("✅ 実データ取得成功:")
        print(f"   SOC: {{battery_data.get('soc', 'N/A')}}%")
        print(f"   電圧: {{battery_data.get('voltage', 'N/A')}}V")
        print(f"   電流: {{battery_data.get('current', 'N/A') or 'N/A'}}A")
        print(f"   時刻: {{battery_data.get('timestamp', 'N/A')}}")
    else:
        print("❌ 実データ取得失敗")
        
    # メール送信テスト（実際に送信）
    print("\\n📧 実データメール送信テスト")
    print("=" * 50)
    
    # メールシステムクラスを探して実行
    for name in globals():
        if 'HANAZONO' in name and 'System' in name:
            try:
                system_class = globals()[name]
                system = system_class()
                
                if hasattr(system, 'run_daily_optimization'):
                    result = system.run_daily_optimization()
                    print(f"✅ メール送信結果: {{result}}")
                elif hasattr(system, 'send_detailed_report'):
                    result = system.send_detailed_report()
                    print(f"✅ メール送信結果: {{result}}")
                else:
                    print("⚠️ メール送信メソッド未発見")
                break
            except Exception as e:
                print(f"❌ メール送信エラー: {{e}}")
                
except ImportError as e:
    print(f"❌ インポートエラー: {{e}}")
except Exception as e:
    print(f"❌ テスト実行エラー: {{e}}")
'''
        
        test_filename = f"test_real_data_email_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_script)
            
        print(f"✅ テストスクリプト作成: {test_filename}")
        return test_filename
        
    def run_integration(self):
        """完全統合実行"""
        print("🎯 メールシステム実データ統合開始")
        print("=" * 60)
        
        # 1. バックアップ
        backup_ok = self.backup_current_system()
        if not backup_ok:
            print("❌ バックアップ失敗")
            return False
            
        # 2. 統合版作成
        integrated_file = self.create_integrated_email_system()
        if not integrated_file:
            print("❌ 統合版作成失敗")
            return False
            
        # 3. テストスクリプト作成
        test_script = self.create_test_email_script(integrated_file)
        
        print(f"\n" + "=" * 60)
        print("🎉 実データ統合完了")
        print("=" * 60)
        print(f"💾 バックアップファイル: {len(self.backup_files)}個")
        for backup in self.backup_files:
            print(f"   📁 {backup}")
            
        print(f"✅ 統合版ファイル: {integrated_file}")
        print(f"🧪 テストスクリプト: {test_script}")
        
        print(f"\n🚀 次のステップ:")
        print(f"   1. python3 {test_script}  # 統合テスト実行")
        print(f"   2. メール受信確認（実データ表示確認）")
        print(f"   3. 動作確認後、手動置換判断")
        
        print(f"\n🛡️ 復旧方法:")
        print(f"   問題時の復旧: cp {self.backup_files[0] if self.backup_files else '[backup_file]'} hanazono_complete_system.py")
        
        return True

if __name__ == "__main__":
    integrator = EmailSystemRealDataIntegration()
    integrator.run_integration()
