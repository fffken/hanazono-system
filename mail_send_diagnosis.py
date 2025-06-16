#!/usr/bin/env python3
# メール送信診断（完全非破壊的）
import datetime
import subprocess
import os
import glob

def diagnose_mail_sending():
    """メール送信診断"""
    print("🔍 メール送信診断開始")
    print("=" * 60)
    
    # 1. アイコン修正版ファイル実行診断
    target_file = "abc_integration_icon_fixed_20250615_223350.py"
    
    print(f"📧 {target_file} 実行診断:")
    
    try:
        # ファイル存在確認
        if os.path.exists(target_file):
            print(f"✅ ファイル存在: {target_file}")
            file_size = os.path.getsize(target_file)
            print(f"📊 ファイルサイズ: {file_size}バイト")
        else:
            print(f"❌ ファイル不存在: {target_file}")
            return False
        
        # 2. テスト実行（出力キャプチャ）
        print(f"\n🧪 テスト実行開始...")
        result = subprocess.run(['python3', target_file], 
                              capture_output=True, text=True, timeout=60)
        
        print(f"実行結果:")
        print(f"返却コード: {result.returncode}")
        
        if result.stdout:
            print(f"標準出力:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    print(f"  {line}")
        
        if result.stderr:
            print(f"エラー出力:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"  ERROR: {line}")
        
        # 3. メール送信成功判定
        success_indicators = [
            "メール送信成功",
            "✅",
            "送信完了"
        ]
        
        output_text = result.stdout + result.stderr
        mail_success = any(indicator in output_text for indicator in success_indicators)
        
        print(f"\n📧 メール送信判定: {'✅ 成功' if mail_success else '❌ 失敗'}")
        
        # 4. エラー分析
        if not mail_success or result.returncode != 0:
            print(f"\n🔧 エラー分析:")
            
            # よくあるエラーパターン確認
            error_patterns = {
                "ModuleNotFoundError": "モジュール不足",
                "FileNotFoundError": "ファイル不存在",
                "TimeoutError": "通信タイムアウト", 
                "SMTPAuthenticationError": "Gmail認証エラー",
                "ConnectionError": "ネットワーク接続エラー",
                "ImportError": "インポートエラー"
            }
            
            for pattern, description in error_patterns.items():
                if pattern in output_text:
                    print(f"  🚨 {description}: {pattern}")
            
            # 5. 修復提案
            print(f"\n🛠️ 修復提案:")
            if "ModuleNotFoundError" in output_text:
                print(f"  - 必要モジュールインストール確認")
            if "weather_forecast" in output_text:
                print(f"  - weather_forecast.py ファイル確認")
            if "SMTP" in output_text:
                print(f"  - Gmail設定・認証確認")
            if "json" in output_text:
                print(f"  - data/collected_data_*.json ファイル確認")
                
        return mail_success
        
    except subprocess.TimeoutExpired:
        print(f"❌ 実行タイムアウト（60秒）")
        return False
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return False

if __name__ == "__main__":
    diagnose_mail_sending()
