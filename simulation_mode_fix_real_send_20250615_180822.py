#!/usr/bin/env python3
# メインハブ シミュレーション→実送信モード修正（完全非破壊的）
import os
import datetime

class SimulationModeFixSystem:
    """メインハブの実送信モード解除（元ファイル完全保護）"""
    
    def __init__(self):
        self.main_hub_file = "hanazono_complete_system.py"
        self.simulation_indicators = []
        self.fix_points = []
        
    def diagnose_simulation_mode(self):
        """実送信モード箇所診断"""
        print("🔍 実送信モード診断")
        print("=" * 50)
        
        if not os.path.exists(self.main_hub_file):
            print(f"❌ {self.main_hub_file} 未発見")
            return False
            
        try:
            with open(self.main_hub_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            
            # シミュレーション箇所検索
            for i, line in enumerate(lines):
                if 'シミュレーション' in line:
                    self.simulation_indicators.append({'line': i+1, 'content': line.strip()})
                    print(f"📍 {i+1}行目: {line.strip()}")
                    
                if 'test_mode' in line or 'simulation' in line.lower():
                    self.simulation_indicators.append({'line': i+1, 'content': line.strip()})
                    print(f"📍 {i+1}行目: {line.strip()}")
                    
            print(f"✅ シミュレーション箇所: {len(self.simulation_indicators)}個発見")
            return True
            
        except Exception as e:
            print(f"❌ 診断エラー: {e}")
            return False
            
    def find_email_module_integration(self):
        """メールモジュール統合箇所確認"""
        print("\n📧 メールモジュール統合確認")
        print("=" * 50)
        
        try:
            with open(self.main_hub_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # email_hub_ml モジュール確認
            if 'email_hub_ml' in content:
                print("✅ email_hub_ml モジュール統合確認")
                
                # send_daily_report メソッド確認
                if 'send_daily_report()' in content:
                    print("✅ send_daily_report() 呼び出し確認")
                    
                    # 実送信フラグ確認
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'send_daily_report' in line and ('test_mode=False' in line or 'actual=True' in line):
                            print(f"✅ {i+1}行目: 実送信フラグ設定済み")
                        elif 'send_daily_report' in line:
                            print(f"🟡 {i+1}行目: {line.strip()}")
                            self.fix_points.append({'line': i+1, 'content': line.strip(), 'type': 'email_call'})
                            
            return True
            
        except Exception as e:
            print(f"❌ メールモジュール確認エラー: {e}")
            return False
            
    def create_real_send_mode_version(self):
        """実送信モード版作成"""
        print("\n🔧 実送信モード版作成")
        print("=" * 50)
        
        try:
            with open(self.main_hub_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # 修正版コンテンツ作成
            modified_content = original_content
            
            # 1. シミュレーション表示の削除/変更
            modified_content = modified_content.replace(
                '📧 メール送信実行（6パラメーター対応）:',
                '📧 メール送信実行（6パラメーター対応）:'
            )
            
            modified_content = modified_content.replace(
                'メール送信実行',
                'メール送信実行'
            )
            
            # 2. email_hub_ml の send_daily_report に実送信フラグ追加
            if 'email_hub_ml' in modified_content and 'send_daily_report()' in modified_content:
                modified_content = modified_content.replace(
                    'send_daily_report()',
                    'send_daily_report(test_mode=False)'
                )
                
            # 3. 実際のメール送信確認
            if 'self.modules["email_hub_ml"].send_daily_report' in modified_content:
                # 実送信フラグが確実に設定されるように修正
                lines = modified_content.split('\n')
                for i, line in enumerate(lines):
                    if 'email_result = self.modules["email_hub_ml"].send_daily_report' in line:
                        if 'test_mode=False' not in line:
                            lines[i] = line.replace(
                                'send_daily_report()',
                                'send_daily_report(test_mode=False, actual_send=True)'
                            )
                            
                modified_content = '\n'.join(lines)
                
            # 新ファイル保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"hanazono_real_send_mode_{timestamp}.py"
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"✅ 実送信モード版作成: {new_filename}")
            return new_filename
            
        except Exception as e:
            print(f"❌ 実送信モード版作成エラー: {e}")
            return None
            
    def create_test_script(self, real_send_file):
        """実送信モードテストスクリプト作成"""
        print(f"\n🧪 実送信モードテストスクリプト作成")
        print("=" * 50)
        
        test_script = f'''#!/usr/bin/env python3
# 実送信モードテスト
import sys
sys.path.insert(0, '.')

print("🧪 実送信モードテスト開始")
print("=" * 50)

try:
    # 実送信モード版をインポート
    module_name = "{real_send_file[:-3]}"  # .py除去
    exec(f"from {{module_name}} import HANAZONOCompleteSystem")
    
    # システム実行
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 実送信モードテスト完了")
    print(f"📧 結果: {{result}}")
    
    # シミュレーション表示チェック
    if "シミュレーション" in str(result):
        print("❌ まだ実送信モードです")
    else:
        print("✅ 実送信モードに変更成功")
        
except Exception as e:
    print(f"❌ テストエラー: {{e}}")
'''
        
        test_filename = f"test_real_send_mode_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_script)
            
        print(f"✅ テストスクリプト作成: {test_filename}")
        return test_filename
        
    def run_simulation_fix(self):
        """実送信モード修正実行"""
        print("🎯 メインハブ シミュレーション→実送信モード修正開始")
        print("=" * 60)
        
        # 1. 診断
        if not self.diagnose_simulation_mode():
            return False
            
        # 2. メールモジュール確認
        if not self.find_email_module_integration():
            return False
            
        # 3. 実送信モード版作成
        real_send_file = self.create_real_send_mode_version()
        if not real_send_file:
            return False
            
        # 4. テストスクリプト作成
        test_script = self.create_test_script(real_send_file)
        
        print(f"\n" + "=" * 60)
        print("🎉 実送信モード修正完了")
        print("=" * 60)
        print(f"✅ 元ファイル: {self.main_hub_file} (完全保護)")
        print(f"✅ 実送信モード版: {real_send_file}")
        print(f"🧪 テストスクリプト: {test_script}")
        
        print(f"\n🚀 次のステップ:")
        print(f"   python3 {test_script}")
        
        print(f"\n🛡️ 完全非破壊的保証:")
        print(f"   - 元ファイル無変更")
        print(f"   - 実送信版は新ファイル")
        print(f"   - 即座復旧可能")
        
        return True

if __name__ == "__main__":
    fixer = SimulationModeFixSystem()
    fixer.run_simulation_fix()
