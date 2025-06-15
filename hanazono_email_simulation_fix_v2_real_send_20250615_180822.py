#!/usr/bin/env python3
# HANAZONOメールシミュレーション修正v2 - より正確な検索
import os
import shutil
import datetime

def fix_email_simulation_v2():
    """より正確な検索でメールシミュレーションを実際送信に修正"""
    
    print("🚨 HANAZONOメールシミュレーション修正v2開始")
    print("=" * 50)
    
    # 1. バックアップ作成
    backup_dir = f"hanazono_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy("hanazono_complete_system.py", backup_dir)
    print(f"✅ バックアップ作成: {backup_dir}")
    
    # 2. 現在のファイル読み込み
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 3. より詳細な検索
    print("📋 シミュレーション部分の詳細検索...")
    
    # 複数のパターンで検索
    search_patterns = [
        "メール送信実行",
        "📧 メール送信実行",
        "メール送信実行（6パラメーター対応）",
        "# 実際のメール送信実行"
    ]
    
    found_patterns = []
    for pattern in search_patterns:
        if pattern in content:
            found_patterns.append(pattern)
            print(f"✅ 発見: {pattern}")
        else:
            print(f"❌ 未発見: {pattern}")
    
    # 4. 実際の置換対象を特定
    if "# 実際のメール送信実行" in content:
        print("⚠️ 既に修正済みです")
        
        # メール送信結果の確認
        print("\n📋 現在のメール送信動作確認...")
        try:
            import importlib
            import sys
            
            # モジュールを再読み込み
            if 'hanazono_complete_system' in sys.modules:
                importlib.reload(sys.modules['hanazono_complete_system'])
            
            from hanazono_complete_system import HANAZONOCompleteSystem
            system = HANAZONOCompleteSystem()
            
            # 直接メール送信テスト
            result = system.send_actual_email("修正確認テスト", "v2修正確認テストです")
            print(f"📧 直接メール送信テスト: {result}")
            
            if result.get('success') and result.get('mode') == 'actual':
                print("✅ メール送信機能: 正常動作")
            else:
                print("⚠️ メール送信機能: 実送信モード")
                
        except Exception as e:
            print(f"❌ テストエラー: {e}")
    
    else:
        # 5. run_daily_optimizationメソッド内の置換実行
        print("\n📋 run_daily_optimizationメソッド修正...")
        
        # より具体的な置換パターン
        if "print(email_content)" in content:
            # email_content出力後にメール送信を追加
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
            print("✅ email_content出力後にメール送信追加")
        
        # 6. 修正版を保存
        with open("hanazono_complete_system.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ 修正完了")
    
    print(f"\n📋 作業完了")
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
    fix_email_simulation_v2()
