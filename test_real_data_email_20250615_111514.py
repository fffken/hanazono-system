#!/usr/bin/env python3
# 実データ統合メールシステムテスト
import sys
import os

# 統合版メールシステムをインポート
sys.path.insert(0, '.')

try:
    from hanazono_email_real_data_integrated_20250615_111514 import *
    
    print("🧪 実データ統合メールテスト開始")
    print("=" * 50)
    
    # バッテリーデータ取得テスト
    battery_data = get_real_battery_data()
    if battery_data:
        print("✅ 実データ取得成功:")
        print(f"   SOC: {battery_data.get('soc', 'N/A')}%")
        print(f"   電圧: {battery_data.get('voltage', 'N/A')}V")
        print(f"   電流: {battery_data.get('current', 'N/A') or 'N/A'}A")
        print(f"   時刻: {battery_data.get('timestamp', 'N/A')}")
    else:
        print("❌ 実データ取得失敗")
        
    # メール送信テスト（実際に送信）
    print("\n📧 実データメール送信テスト")
    print("=" * 50)
    
    # メールシステムクラスを探して実行
    for name in globals():
        if 'HANAZONO' in name and 'System' in name:
            try:
                system_class = globals()[name]
                system = system_class()
                
                if hasattr(system, 'run_daily_optimization'):
                    result = system.run_daily_optimization()
                    print(f"✅ メール送信結果: {result}")
                elif hasattr(system, 'send_detailed_report'):
                    result = system.send_detailed_report()
                    print(f"✅ メール送信結果: {result}")
                else:
                    print("⚠️ メール送信メソッド未発見")
                break
            except Exception as e:
                print(f"❌ メール送信エラー: {e}")
                
except ImportError as e:
    print(f"❌ インポートエラー: {e}")
except Exception as e:
    print(f"❌ テスト実行エラー: {e}")
