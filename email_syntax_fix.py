#!/usr/bin/env python3
# メールシステム構文修復スクリプト
import os
import re
import datetime

class EmailSyntaxFixer:
    """構文エラー自動修復"""
    
    def __init__(self):
        self.error_file = "hanazono_email_real_data_integrated_20250615_111514.py"
        self.fixed_content = ""
        
    def diagnose_syntax_error(self):
        """構文エラー診断"""
        print("🔍 構文エラー診断開始")
        print("=" * 50)
        
        if not os.path.exists(self.error_file):
            print(f"❌ ファイル未発見: {self.error_file}")
            return False
            
        try:
            with open(self.error_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            print(f"✅ ファイル読み込み成功: {len(lines)}行")
            
            # line 127周辺を確認
            if len(lines) >= 127:
                print(f"🔍 エラー箇所周辺確認 (line 125-130):")
                for i in range(124, min(131, len(lines))):
                    line_num = i + 1
                    marker = ">>>" if line_num == 127 else "   "
                    print(f"{marker} {line_num:3}: {lines[i]}")
                    
            return True
            
        except Exception as e:
            print(f"❌ ファイル読み込み失敗: {e}")
            return False
            
    def create_fixed_version(self):
        """修復版作成"""
        print("\n🔧 構文修復版作成")
        print("=" * 50)
        
        # 元のメールシステムから再作成（より安全なアプローチ）
        source_file = "hanazono_complete_system.py"
        
        if not os.path.exists(source_file):
            print(f"❌ 元ファイル未発見: {source_file}")
            return None
            
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            print(f"✅ 元ファイル読み込み: {source_file}")
            
            # シンプルな修正アプローチ
            fixed_content = self.create_simple_integration(original_content)
            
            # 修復版保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fixed_filename = f"hanazono_email_fixed_{timestamp}.py"
            
            with open(fixed_filename, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
                
            print(f"✅ 修復版作成: {fixed_filename}")
            
            # 構文チェック
            if self.syntax_check(fixed_filename):
                print("✅ 構文チェック: OK")
                return fixed_filename
            else:
                print("❌ 構文チェック: NG")
                return None
                
        except Exception as e:
            print(f"❌ 修復版作成失敗: {e}")
            return None
            
    def create_simple_integration(self, original_content):
        """シンプルな実データ統合"""
        
        # 実データ取得関数（簡潔版）
        real_data_function = '''
def get_real_battery_data():
    """実際のバッテリーデータ取得（簡潔版）"""
    try:
        import json
        import glob
        
        json_files = glob.glob('data/collected_data_*.json')
        if not json_files:
            return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}
            
        latest_file = max(json_files, key=lambda x: os.path.getctime(x))
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        latest_record = data[0] if isinstance(data, list) else data
        params = latest_record.get('parameters', {})
        
        result = {}
        result['soc'] = params.get('0x0100', {}).get('value', params.get('0x0100', {}).get('raw_value', '取得失敗'))
        result['voltage'] = params.get('0x0101', {}).get('value', params.get('0x0101', {}).get('raw_value', '取得失敗'))
        result['timestamp'] = latest_record.get('datetime', '取得失敗')
        
        return result
        
    except:
        return {'soc': '取得失敗', 'voltage': '取得失敗', 'timestamp': '取得失敗'}

'''
        
        # 元コンテンツを修正
        lines = original_content.split('\n')
        
        # import文の後に実データ取得関数を追加
        modified_lines = []
        import_section_end = False
        
        for line in lines:
            modified_lines.append(line)
            
            # import文の終了を検出
            if (line.strip().startswith('import ') or line.strip().startswith('from ')) and not import_section_end:
                continue
            elif not import_section_end and line.strip() and not line.strip().startswith('#'):
                # import文終了、関数を挿入
                modified_lines.append('')
                modified_lines.extend(real_data_function.strip().split('\n'))
                modified_lines.append('')
                import_section_end = True
                
        # メール本文の固定値を動的値に置換
        final_lines = []
        in_email_function = False
        
        for line in modified_lines:
            # メール関数の開始を検出
            if 'def send_' in line or 'def run_daily_optimization' in line:
                in_email_function = True
                final_lines.append(line)
                final_lines.append('        # 実データ取得')
                final_lines.append('        real_data = get_real_battery_data()')
                continue
                
            # 固定値を動的値に置換
            if 'バッテリー残量:' in line and ('取得中' in line or '取得失敗' in line):
                final_lines.append(line.replace('取得中', '{real_data["soc"]}').replace('取得失敗', '{real_data["soc"]}'))
            elif '電圧:' in line and ('取得中' in line or '取得失敗' in line):
                final_lines.append(line.replace('取得中', '{real_data["voltage"]}').replace('取得失敗', '{real_data["voltage"]}'))
            elif '取得時刻:' in line and '取得失敗' in line:
                final_lines.append(line.replace('取得失敗', '{real_data["timestamp"]}'))
            else:
                final_lines.append(line)
                
        return '\n'.join(final_lines)
        
    def syntax_check(self, filename):
        """構文チェック"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, filename, 'exec')
            return True
        except SyntaxError as e:
            print(f"構文エラー: {e}")
            return False
        except Exception as e:
            print(f"チェックエラー: {e}")
            return False
            
    def create_test_script(self, fixed_filename):
        """テストスクリプト作成"""
        print(f"\n🧪 修復版テストスクリプト作成")
        print("=" * 50)
        
        test_script = f'''#!/usr/bin/env python3
# 修復版実データメールテスト
print("🧪 修復版実データメールテスト開始")
print("=" * 50)

# 実データ取得テスト
try:
    exec(open("{fixed_filename}").read())
    
    battery_data = get_real_battery_data()
    print("✅ 実データ取得テスト:")
    print(f"   SOC: {{battery_data['soc']}}%")
    print(f"   電圧: {{battery_data['voltage']}}V")
    print(f"   時刻: {{battery_data['timestamp']}}")
    
    # メール送信テスト
    print("\\n📧 メール送信テスト")
    print("=" * 50)
    
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    print(f"✅ メール送信結果: {{result}}")
    
except Exception as e:
    print(f"❌ テストエラー: {{e}}")
'''
        
        test_filename = f"test_fixed_email_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_script)
            
        print(f"✅ テストスクリプト作成: {test_filename}")
        return test_filename
        
    def run_fix(self):
        """修復実行"""
        print("🎯 メールシステム構文修復開始")
        print("=" * 60)
        
        # 1. エラー診断
        if not self.diagnose_syntax_error():
            return False
            
        # 2. 修復版作成
        fixed_file = self.create_fixed_version()
        if not fixed_file:
            return False
            
        # 3. テストスクリプト作成
        test_script = self.create_test_script(fixed_file)
        
        print(f"\n" + "=" * 60)
        print("🎉 構文修復完了")
        print("=" * 60)
        print(f"✅ 修復版: {fixed_file}")
        print(f"🧪 テストスクリプト: {test_script}")
        
        print(f"\n🚀 次のステップ:")
        print(f"   python3 {test_script}")
        
        return True

if __name__ == "__main__":
    fixer = EmailSyntaxFixer()
    fixer.run_fix()
