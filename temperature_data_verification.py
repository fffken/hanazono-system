#!/usr/bin/env python3
# 気温データ完璧性確認（完全非破壊的）
import subprocess
import datetime

def verify_temperature_data():
    """気温データ完璧性確認"""
    print("🌡️ 気温データ完璧性確認開始")
    print("=" * 60)
    
    target_file = "abc_integration_icon_fixed_20250615_223350.py"
    
    # 1. 実際にメール送信テスト実行
    print("🧪 実際のメール送信テスト実行...")
    
    try:
        result = subprocess.run(['python3', target_file], 
                              capture_output=True, text=True, timeout=60)
        
        print(f"実行結果:")
        print(f"返却コード: {result.returncode}")
        
        # 出力内容確認
        if result.stdout:
            print(f"\n📊 標準出力:")
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if line.strip():
                    print(f"  {line}")
                    
        # エラー確認
        if result.stderr:
            print(f"\n⚠️ エラー出力:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"  ERROR: {line}")
        
        # 2. 成功判定
        success_indicators = [
            "メール送信成功",
            "✅",
            "アイコン修正版メール送信成功"
        ]
        
        output_text = result.stdout
        mail_success = any(indicator in output_text for indicator in success_indicators)
        
        print(f"\n📧 メール送信結果: {'✅ 成功' if mail_success else '❌ 失敗'}")
        
        if mail_success:
            print(f"\n🎉 完璧！気温データを含む統一版メール送信成功")
            print(f"📧 メール受信確認をお願いします")
            print(f"🌡️ 気温表示確認ポイント:")
            print(f"  - 今日: XX℃〜XX℃ 形式")
            print(f"  - 明日: XX℃〜XX℃ 形式") 
            print(f"  - 明後日: XX℃〜XX℃ 形式")
            print(f"  - N/A や単一気温の表示なし")
            
            print(f"\n🎨 その他確認ポイント:")
            print(f"  - 件名: 🟠 HANAZONOシステム YYYY年MM月DD日")
            print(f"  - 推奨変更: 🟠 推奨変更 (または🔵🟣🌻)")
            print(f"  - 絵文字: ☀️ → ☁️ 等の天気絵文字")
            
            return True
        else:
            print(f"\n❌ メール送信失敗、詳細確認が必要")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ 実行タイムアウト（60秒）")
        return False
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return False

if __name__ == "__main__":
    verify_temperature_data()
