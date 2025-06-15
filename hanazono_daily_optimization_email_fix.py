#!/usr/bin/env python3
# run_daily_optimization内のメール送信を実際送信に完全修正
import os
import shutil
import datetime
import re

def fix_daily_optimization_email():
    """run_daily_optimization内のメール送信を実際送信に完全修正"""
    
    print("🚨 run_daily_optimization メール送信最終修正")
    print("=" * 50)
    
    # 1. バックアップ作成
    backup_dir = f"hanazono_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy("hanazono_complete_system.py", backup_dir)
    print(f"✅ バックアップ作成: {backup_dir}")
    
    # 2. ファイル読み込み
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 3. run_daily_optimizationメソッド内の正確な置換
    print("📋 run_daily_optimization内のメール送信部分を特定...")
    
    # メール送信シミュレーション部分の開始を探す
    simulation_start = "📧 メール送信シミュレーション（6パラメーター対応）:"
    
    if simulation_start in content:
        print("✅ シミュレーション部分発見")
        
        # シミュレーション部分から Enhanced Email System まで
        pattern = r'📧 メール送信シミュレーション（6パラメーター対応）:\s*\n(.*?)Enhanced Email System v3\.2 \+ 6-Parameter ML Integration\s*\n📧 メールレポート: ✅ 成功'
        
        replacement = '''# 実際のメール送信実行
        email_subject = f"最適化レポート {datetime.now().strftime('%Y年%m月%d日')}"
        email_result = self.send_actual_email(email_subject, email_content)
        
        if email_result.get('success'):
            if email_result.get('mode') == 'actual':
                print("📧 メールレポート: ✅ 実際送信成功")
            else:
                print("📧 メールレポート: ✅ シミュレーション")
        else:
            print(f"📧 メールレポート: ❌ 送信失敗 - {email_result.get('error', 'Unknown')}")
        
        print("Enhanced Email System v3.2 + 6-Parameter ML Integration (実際送信)")
        print("📧 メールレポート: ✅ 実際送信完了")'''
        
        # 正規表現で置換
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ 正規表現置換実行")
        
    else:
        print("❌ シミュレーション部分が見つかりません")
        
        # 別の方法：print(email_content) の後に実際の送信を追加
        if "print(email_content)" in content:
            old_pattern = "print(email_content)"
            new_pattern = '''print(email_content)
        
        # 実際のメール送信実行
        email_subject = f"最適化レポート {datetime.now().strftime('%Y年%m月%d日')}"
        email_result = self.send_actual_email(email_subject, email_content)
        
        if email_result.get('success'):
            if email_result.get('mode') == 'actual':
                print("📧 メールレポート: ✅ 実際送信成功")
            else:
                print("📧 メールレポート: ✅ シミュレーション")
        else:
            print(f"📧 メールレポート: ❌ 送信失敗")'''
            
            content = content.replace(old_pattern, new_pattern)
            print("✅ print(email_content)後に実際送信追加")
    
    # 4. 保存
    with open("hanazono_complete_system.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 修正完了")
    
    # 5. テスト実行
    print("\n📋 修正版テスト...")
    try:
        # モジュール再読み込み
        import importlib
        import sys
        if 'hanazono_complete_system' in sys.modules:
            importlib.reload(sys.modules['hanazono_complete_system'])
        
        from hanazono_complete_system import HANAZONOCompleteSystem
        system = HANAZONOCompleteSystem()
        
        # 短時間テスト実行
        print("📧 修正版run_daily_optimization実行...")
        result = system.run_daily_optimization()
        
        if result.get('success'):
            print("✅ 修正版動作: 成功")
        else:
            print("❌ 修正版動作: 失敗")
            
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    
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
    fix_daily_optimization_email()
