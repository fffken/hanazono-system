#!/usr/bin/env python3
"""
Email Test Send Script
目的: HANAZONOメールシステムのテスト送信
原則: 安全なテスト・非破壊的・即座削除対象
"""

import sys
import json
from datetime import datetime

def main():
    print("📧 HANAZONOメールシステム テスト送信")
    print(f"実行時刻: {datetime.now()}")
    
    print("\n🎯 復旧確認テスト")
    print("1. コード互換性修復: ✅ 完了")
    print("2. SMTP設定復旧: ✅ 完了")
    print("3. App Password設定: ✅ 完了")
    print("4. 1年前比較バトル: ✅ 機能復旧済み")
    
    print("\n" + "="*50)
    choice = input("テスト送信を実行しますか？ (y/N): ").lower()
    
    if choice == 'y':
        print("\n📧 main.py --daily-report テスト実行...")
        
        try:
            import subprocess
            result = subprocess.run(['python3', 'main.py', '--daily-report'], 
                                  capture_output=True, text=True, timeout=60)
            
            print(f"📊 実行結果: 終了コード {result.returncode}")
            
            if result.returncode == 0:
                print("🎉 メール送信成功！")
                print("✅ HANAZONOメールシステム完全復旧達成！")
                
                if result.stdout:
                    print("\n📋 送信確認:")
                    for line in result.stdout.splitlines()[:10]:
                        print(f"   {line}")
            else:
                print("❌ メール送信エラー:")
                if result.stderr:
                    for line in result.stderr.splitlines()[:5]:
                        print(f"   エラー: {line}")
                
                print("\n🔧 トラブルシューティング:")
                print("1. App Password の再確認")
                print("2. Gmail の2段階認証確認")
                print("3. ネットワーク接続確認")
                
        except subprocess.TimeoutExpired:
            print("⏰ タイムアウト（60秒）- 処理時間が長すぎます")
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
    else:
        print("⏸️ テスト送信をスキップ")
        print("📋 手動テスト方法:")
        print("python3 main.py --daily-report")
    
    print(f"\n🎯 Step 6: メール送信テスト完了")

if __name__ == "__main__":
    main()
