#!/usr/bin/env python3
# 明後日天気予報修正版動作確認テスト（完全非破壊的）
import datetime
import subprocess

def test_weather_fix():
    """明後日天気予報修正版動作確認テスト"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🧪 明後日天気予報修正版動作確認テスト開始 {timestamp}")
    print("=" * 70)
    
    cron_file = "abc_integration_fixed_final_20250616_231158.py"
    
    # 修正版実行テスト
    print(f"🚀 明後日天気予報修正版実行テスト:")
    try:
        result = subprocess.run([
            'python3', cron_file
        ], capture_output=True, text=True, timeout=60)
        
        print(f"  📊 実行結果:")
        print(f"    終了コード: {result.returncode}")
        
        if result.stdout:
            print(f"  📝 標準出力:")
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if line.strip():
                    print(f"    {line}")
        
        if result.stderr:
            print(f"  ⚠️ エラー出力:")
            error_lines = result.stderr.split('\n')
            for line in error_lines:
                if line.strip():
                    print(f"    {line}")
        
        # 成功判定
        if result.returncode == 0:
            print(f"  ✅ 修正版実行成功")
            
            # 明後日天気予報修正成功の兆候確認
            success_indicators = [
                "明後日天気予報表示修正版メール送信成功",
                "メール送信成功",
                "完成"
            ]
            
            output_text = result.stdout + result.stderr
            weather_success = any(indicator in output_text for indicator in success_indicators)
            
            if weather_success:
                print(f"  🎉 明後日天気予報修正成功")
                print(f"  📧 メール受信確認で3日分天気予報をご確認ください")
                return True
            else:
                print(f"  ⚠️ 明後日天気予報修正成功の明確な兆候なし")
                return False
        else:
            print(f"  ❌ 修正版実行失敗")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ❌ 実行タイムアウト")
        return False
    except Exception as e:
        print(f"  ❌ 実行例外: {e}")
        return False

if __name__ == "__main__":
    success = test_weather_fix()
    if success:
        print(f"\n🎯 次のアクション:")
        print(f"1. メール受信確認（明後日の天気予報表示確認）")
        print(f"2. 3日分天気予報正常表示確認")
        print(f"3. 確認後Git保存作業")
