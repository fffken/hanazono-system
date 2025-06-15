#!/usr/bin/env python3
# EmailHubMLFinal引数問題完全診断・修正（完全非破壊的）
import os
import datetime
import inspect

class EmailHubArgumentFix:
    """EmailHubMLFinal引数問題修正（元ファイル完全保護）"""
    
    def __init__(self):
        self.email_hub_file = "email_hub_ml_final.py"
        self.real_send_file = "hanazono_real_send_mode_20250615_180033.py"
        self.method_signature = None
        
    def diagnose_email_hub_arguments(self):
        """EmailHubMLFinal引数診断"""
        print("🔍 EmailHubMLFinal引数診断")
        print("=" * 50)
        
        try:
            # EmailHubMLFinalのsend_daily_reportメソッド引数確認
            from email_hub_ml_final import EmailHubMLFinal
            
            sig = inspect.signature(EmailHubMLFinal.send_daily_report)
            self.method_signature = sig
            print(f"✅ send_daily_report引数: {sig}")
            
            # 引数詳細確認
            params = list(sig.parameters.keys())
            print(f"✅ 引数リスト: {params}")
            
            # test_modeの存在確認
            if 'test_mode' in params:
                print("✅ test_mode引数: 存在")
            else:
                print("❌ test_mode引数: 不存在")
                
            return True
            
        except Exception as e:
            print(f"❌ EmailHubMLFinal診断エラー: {e}")
            return False
            
    def test_correct_email_call(self):
        """正しいメール呼び出しテスト"""
        print("\n📧 正しいメール呼び出しテスト")
        print("=" * 50)
        
        try:
            from email_hub_ml_final import EmailHubMLFinal
            
            hub = EmailHubMLFinal()
            
            # 引数なしでテスト
            print("📋 1. 引数なしテスト")
            result1 = hub.send_daily_report()
            print(f"✅ 引数なし結果: {result1}")
            
            # 可能な引数でテスト
            if self.method_signature:
                params = list(self.method_signature.parameters.keys())
                if len(params) > 1:  # selfを除く
                    print(f"📋 2. 利用可能引数: {params[1:]}")
                    
            return True
            
        except Exception as e:
            print(f"❌ メール呼び出しテスト失敗: {e}")
            return False
            
    def create_fixed_real_send_version(self):
        """修正版実送信システム作成"""
        print("\n🔧 修正版実送信システム作成")
        print("=" * 50)
        
        if not os.path.exists(self.real_send_file):
            print(f"❌ {self.real_send_file} 未発見")
            return None
            
        try:
            # 元の実送信版を読み込み
            with open(self.real_send_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 問題のある引数呼び出しを修正
            modified_content = content
            
            # test_mode=False引数を削除
            modified_content = modified_content.replace(
                'send_daily_report(test_mode=False)',
                'send_daily_report()'
            )
            
            modified_content = modified_content.replace(
                'send_daily_report(test_mode=False, actual_send=True)',
                'send_daily_report()'
            )
            
            # その他の不正な引数も削除
            modified_content = modified_content.replace(
                'send_daily_report(actual_send=True)',
                'send_daily_report()'
            )
            
            # 新ファイル保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fixed_filename = f"hanazono_real_send_fixed_{timestamp}.py"
            
            with open(fixed_filename, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"✅ 修正版実送信システム作成: {fixed_filename}")
            return fixed_filename
            
        except Exception as e:
            print(f"❌ 修正版作成エラー: {e}")
            return None
            
    def create_final_test_script(self, fixed_file):
        """最終テストスクリプト作成"""
        print(f"\n🧪 最終テストスクリプト作成")
        print("=" * 50)
        
        test_script = f'''#!/usr/bin/env python3
# EmailHubMLFinal引数修正版最終テスト
import sys
sys.path.insert(0, '.')

print("🧪 引数修正版最終テスト開始")
print("=" * 50)

try:
    # 修正版をインポート
    module_name = "{fixed_file[:-3]}"  # .py除去
    exec(f"from {{module_name}} import HANAZONOCompleteSystem")
    
    # システム実行
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 引数修正版テスト完了")
    print(f"📧 結果: {{result}}")
    
    # 成功判定
    if isinstance(result, dict) and result.get('success'):
        print("✅ 実送信成功！メール受信確認をお願いします")
    else:
        print("❌ まだ問題があります")
        
except Exception as e:
    print(f"❌ テストエラー: {{e}}")
'''
        
        test_filename = f"test_final_real_send_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_script)
            
        print(f"✅ 最終テストスクリプト作成: {test_filename}")
        return test_filename
        
    def run_argument_fix(self):
        """引数問題修正実行"""
        print("🎯 EmailHubMLFinal引数問題修正開始（完全非破壊的）")
        print("=" * 60)
        
        # 1. 引数診断
        if not self.diagnose_email_hub_arguments():
            return False
            
        # 2. 正しい呼び出しテスト
        if not self.test_correct_email_call():
            return False
            
        # 3. 修正版作成
        fixed_file = self.create_fixed_real_send_version()
        if not fixed_file:
            return False
            
        # 4. 最終テストスクリプト作成
        test_script = self.create_final_test_script(fixed_file)
        
        print(f"\n" + "=" * 60)
        print("🎉 引数問題修正完了")
        print("=" * 60)
        print(f"✅ 診断: EmailHubMLFinal引数確認済み")
        print(f"✅ 修正版: {fixed_file}")
        print(f"🧪 最終テスト: {test_script}")
        
        print(f"\n🚀 次のステップ:")
        print(f"   python3 {test_script}")
        
        print(f"\n🛡️ 完全非破壊的保証:")
        print(f"   - 全元ファイル無変更")
        print(f"   - 修正版は新ファイル")
        print(f"   - 即座復旧可能")
        
        return True

if __name__ == "__main__":
    fixer = EmailHubArgumentFix()
    fixer.run_argument_fix()
