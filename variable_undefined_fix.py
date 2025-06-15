#!/usr/bin/env python3
# 変数未定義エラー修正（完全非破壊的）
import os
import datetime

class VariableUndefinedFix:
    """email_result未定義エラー修正（元ファイル完全保護）"""
    
    def __init__(self):
        self.target_file = "hanazono_complete_system_real_send_20250615_180822.py"
        
    def fix_email_result_error(self):
        """email_result変数エラー修正"""
        print("🔧 email_result変数エラー修正")
        print("=" * 50)
        
        if not os.path.exists(self.target_file):
            print(f"❌ {self.target_file} 未発見")
            return None
            
        try:
            with open(self.target_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # email_result変数の定義箇所を確認・修正
            lines = content.split('\n')
            modified_lines = []
            
            for i, line in enumerate(lines):
                # email_resultが参照されているが定義されていない箇所を修正
                if 'email_result' in line and 'email_result =' not in line:
                    # email_resultの定義を追加
                    if 'modules["email_hub_ml"]' in line:
                        # 正しい定義を挿入
                        modified_lines.append('                email_result = self.modules["email_hub_ml"].send_daily_report()')
                        modified_lines.append(line)
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
                    
            # 新ファイル保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fixed_filename = f"hanazono_variable_fixed_{timestamp}.py"
            
            with open(fixed_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(modified_lines))
                
            print(f"✅ 変数修正版作成: {fixed_filename}")
            return fixed_filename
            
        except Exception as e:
            print(f"❌ 修正エラー: {e}")
            return None
            
    def create_final_test(self, fixed_file):
        """最終動作テスト作成"""
        print(f"\n🧪 最終動作テスト作成")
        print("=" * 50)
        
        test_script = f'''#!/usr/bin/env python3
# 最終動作テスト
print("🧪 最終動作テスト開始")
print("=" * 50)

try:
    from {fixed_file[:-3]} import HANAZONOCompleteSystem
    
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 最終テスト完了")
    print(f"📧 結果: {{result}}")
    
    # 成功判定
    if isinstance(result, dict):
        email_success = result.get('results', {{}}).get('email_report', {{}}).get('success', False)
        if email_success:
            print("✅ メール送信成功！受信確認をお願いします")
        else:
            error_msg = result.get('results', {{}}).get('email_report', {{}}).get('error', 'Unknown')
            print(f"❌ メール送信失敗: {{error_msg}}")
    
except Exception as e:
    print(f"❌ テストエラー: {{e}}")
'''
        
        test_filename = f"final_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_script)
            
        print(f"✅ 最終テスト作成: {test_filename}")
        return test_filename
        
    def run_fix(self):
        """変数エラー修正実行"""
        print("🎯 変数未定義エラー修正開始（完全非破壊的）")
        print("=" * 60)
        
        # 修正版作成
        fixed_file = self.fix_email_result_error()
        if not fixed_file:
            return False
            
        # 最終テスト作成
        test_script = self.create_final_test(fixed_file)
        
        print(f"\n" + "=" * 60)
        print("🎉 変数エラー修正完了")
        print("=" * 60)
        print(f"✅ 修正版: {fixed_file}")
        print(f"🧪 最終テスト: {test_script}")
        
        print(f"\n🚀 実行: python3 {test_script}")
        
        print(f"\n🛡️ 完全非破壊的保証:")
        print(f"   - 元ファイル無変更")
        print(f"   - 修正版新ファイル")
        print(f"   - 即座復旧可能")
        
        return True

if __name__ == "__main__":
    fixer = VariableUndefinedFix()
    fixer.run_fix()
