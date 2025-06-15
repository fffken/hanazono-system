#!/usr/bin/env python3
# 天気統合テスト（HCQASバイパス）
print("🧪 天気統合テスト開始")
print("=" * 50)

try:
    from hanazono_weather_integrated_20250615_185647 import HANAZONOCompleteSystem
    
    system = HANAZONOCompleteSystem()
    
    # 天気データ統合テスト
    weather_data = system.get_integrated_weather_data()
    print("✅ 天気データ統合成功")
    print(f"📊 天気データ:\n{weather_data}")
    
    # メール送信テスト（天気データ含む）
    print("\n📧 天気データ含むメール送信テスト")
    result = system.run_daily_optimization()
    
    print("✅ 天気統合テスト完了")
    print(f"📧 結果: {result}")
    
    # 成功判定
    if isinstance(result, dict) and result.get('success'):
        print("✅ 天気統合成功！メール受信確認をお願いします")
        print("📧 実際の天気データがメールに含まれているか確認してください")
    else:
        print("❌ 天気統合に問題があります")
        
except Exception as e:
    print(f"❌ 天気統合テストエラー: {e}")
