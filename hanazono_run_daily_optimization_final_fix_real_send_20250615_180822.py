#!/usr/bin/env python3
# run_daily_optimization内への確実なメール送信統合
import os
import shutil
import datetime
import re

def final_fix_run_daily_optimization():
    """run_daily_optimization内に確実にメール送信を統合"""
    
    print("🚨 run_daily_optimization最終メール修正")
    print("=" * 50)
    
    # 1. バックアップ作成
    backup_dir = f"hanazono_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy("hanazono_complete_system.py", backup_dir)
    print(f"✅ バックアップ作成: {backup_dir}")
    
    # 2. ファイル読み込み
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 3. run_daily_optimizationメソッドの終了部分を特定
    print("📋 run_daily_optimizationメソッドの終了部分を特定...")
    
    # return文の直前に実際のメール送信を挿入
    return_pattern = r'return\s*{\s*["\']success["\']\s*:\s*True'
    
    if re.search(return_pattern, content):
        print("✅ return文発見")
        
        # return文の直前に実際のメール送信を挿入
        insert_code = '''
        # 実際のメール送信実行
        try:
            email_subject = f"最適化レポート {datetime.now().strftime('%Y年%m月%d日')}"
            email_result = self.send_actual_email(email_subject, email_content)
            
            if email_result.get('success'):
                if email_result.get('mode') == 'actual':
                    print("📧 実際のメール送信: ✅ 成功")
                else:
                    print("📧 実際のメール送信: ✅ シミュレーション")
            else:
                print(f"📧 実際のメール送信: ❌ 失敗 - {email_result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"📧 メール送信エラー: {e}")
        
        '''
        
        # return文の直前に挿入
        content = re.sub(
            r'(\s+)(return\s*{\s*["\']success["\']\s*:\s*True)',
            r'\1' + insert_code + r'\1\2',
            content
        )
        print("✅ return文直前にメール送信コード挿入")
        
    else:
        print("❌ return文が見つかりません")
        
        # 別の方法：メソッドの最後に追加
        # run_daily_optimizationメソッドの終了を探す
        method_pattern = r'(def run_daily_optimization\(self.*?\n)(.*?)(\n\s+def\s+\w+|\n\s*$|\nclass\s+)'
        
        def add_email_to_method(match):
            method_def = match.group(1)
            method_body = match.group(2)
            next_part = match.group(3) if match.group(3) else ""
            
            # メソッドの最後に実際のメール送信を追加
            email_code = '''
        # 実際のメール送信実行
        try:
            email_subject = f"最適化レポート {datetime.now().strftime('%Y年%m月%d日')}"
            email_result = self.send_actual_email(email_subject, email_content)
            
            if email_result.get('success'):
                if email_result.get('mode') == 'actual':
                    print("📧 実際のメール送信: ✅ 成功")
                else:
                    print("📧 実際のメール送信: ✅ シミュレーション")
            else:
                print(f"📧 実際のメール送信: ❌ 失敗")
        except Exception as e:
            print(f"📧 メール送信エラー: {e}")
'''
            
            return method_def + method_body + email_code + next_part
        
        content = re.sub(method_pattern, add_email_to_method, content, flags=re.DOTALL)
        print("✅ メソッド最後にメール送信コード追加")
    
    # 4. 保存
    with open("hanazono_complete_system.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 修正完了")
    
    # 5. 確認テスト
    print("\n📋 修正確認テスト...")
    try:
        import importlib
        import sys
        if 'hanazono_complete_system' in sys.modules:
            importlib.reload(sys.modules['hanazono_complete_system'])
        
        import inspect
        from hanazono_complete_system import HANAZONOCompleteSystem
        system = HANAZONOCompleteSystem()
        
        # run_daily_optimizationのソースコード確認
        source = inspect.getsource(system.run_daily_optimization)
        if 'send_actual_email' in source:
            print("✅ 修正確認: run_daily_optimization内にsend_actual_email呼び出しあり")
        else:
            print("❌ 修正確認: まだsend_actual_email呼び出しなし")
            
    except Exception as e:
        print(f"❌ 確認テストエラー: {e}")
    
    print(f"\n📋 最終修正完了")
    print(f"🛡️ 復旧方法: cp {backup_dir}/hanazono_complete_system.py ./")
    
    # 5分後に自動削除
    import threading
    def cleanup():
        import time
        time.sleep(300)
        try:
            os.remove(__file__)
        except:
            pass
    threading.Thread(target=cleanup, daemon=True).start()

if __name__ == "__main__":
    final_fix_run_daily_optimization()
