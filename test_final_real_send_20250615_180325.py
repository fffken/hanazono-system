#!/usr/bin/env python3
# EmailHubMLFinal引数修正版最終テスト
import sys
sys.path.insert(0, '.')

print("🧪 引数修正版最終テスト開始")
print("=" * 50)

try:
    # 修正版をインポート
    module_name = "hanazono_real_send_fixed_20250615_180325"  # .py除去
    exec(f"from {module_name} import HANAZONOCompleteSystem")
    
    # システム実行
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 引数修正版テスト完了")
    print(f"📧 結果: {result}")
    
    # 成功判定
    if isinstance(result, dict) and result.get('success'):
        print("✅ 実送信成功！メール受信確認をお願いします")
    else:
        print("❌ まだ問題があります")
        
except Exception as e:
    print(f"❌ テストエラー: {e}")
