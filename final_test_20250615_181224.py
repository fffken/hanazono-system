#!/usr/bin/env python3
# 最終動作テスト
print("🧪 最終動作テスト開始")
print("=" * 50)

try:
    from hanazono_variable_fixed_20250615_181224 import HANAZONOCompleteSystem
    
    system = HANAZONOCompleteSystem()
    result = system.run_daily_optimization()
    
    print("✅ 最終テスト完了")
    print(f"📧 結果: {result}")
    
    # 成功判定
    if isinstance(result, dict):
        email_success = result.get('results', {}).get('email_report', {}).get('success', False)
        if email_success:
            print("✅ メール送信成功！受信確認をお願いします")
        else:
            error_msg = result.get('results', {}).get('email_report', {}).get('error', 'Unknown')
            print(f"❌ メール送信失敗: {error_msg}")
    
except Exception as e:
    print(f"❌ テストエラー: {e}")
