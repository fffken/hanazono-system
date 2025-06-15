#!/usr/bin/env python3
# 実送信モードテスト
import sys
sys.path.insert(0, '.')

print("🧪 実送信モードテスト開始")
print("=" * 50)

try:
    # 実送信モード版をインポート
    module_name = "hanazono_real_send_mode_20250615_180033"  # .py除去
    exec(f"from {module_name} import HANAZONOCompleteSystem")
    
    # システム実行
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 実送信モードテスト完了")
    print(f"📧 結果: {result}")
    
    # シミュレーション表示チェック
    if "シミュレーション" in str(result):
        print("❌ まだ実送信モードです")
    else:
        print("✅ 実送信モードに変更成功")
        
except Exception as e:
    print(f"❌ テストエラー: {e}")
