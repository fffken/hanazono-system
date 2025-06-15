#!/usr/bin/env python3
# 統一実送信テスト
print("🧪 統一実送信テスト開始")
print("=" * 50)

try:
    from hanazono_complete_system_detailed_report_20250615_073249_real_send_20250615_180822 import HANAZONOCompleteSystem
    
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 統一テスト完了")
    print(f"📧 結果: {result}")
    
    # 実送信確認
    if "シミュレーション" not in str(result):
        print("✅ シミュレーションモード完全除去成功")
        print("📧 メール受信確認をお願いします！")
    else:
        print("❌ まだシミュレーション表示あり")
        
except Exception as e:
    print(f"❌ エラー: {e}")
