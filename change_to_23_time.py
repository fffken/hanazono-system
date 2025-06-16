#!/usr/bin/env python3
# 19時→23時変更（完全非破壊的）
import subprocess
import datetime
import os

def change_evening_to_23():
    """19時→23時変更"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🕐 夜間配信時間 19時→23時変更開始 {timestamp}")
    print("=" * 60)
    
    # 1. 現在のcrontab取得
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            current_crontab = result.stdout
            print("✅ 現在のcrontab取得成功")
        else:
            print("❌ crontab取得失敗")
            return False
    except Exception as e:
        print(f"❌ crontab取得エラー: {e}")
        return False
    
    # 2. 現在のcronバックアップ
    backup_file = f"crontab_before_23time_{timestamp}.txt"
    with open(backup_file, 'w') as f:
        f.write(current_crontab)
    print(f"✅ cronバックアップ: {backup_file}")
    
    # 3. 19時→23時変更
    print(f"\n🔧 19時→23時変更処理...")
    
    new_crontab_lines = []
    change_count = 0
    
    for line in current_crontab.split('\n'):
        if line.strip():
            # 19時のHANAZONO配信を23時に変更
            if '0 19' in line and ('HANAZONO' in line or 'abc_integration' in line):
                new_line = line.replace('0 19', '0 23')
                new_line = new_line.replace('evening', 'night')  # ログファイル名も変更
                new_crontab_lines.append(new_line)
                print(f"🔄 変更: {line}")
                print(f"    →  {new_line}")
                change_count += 1
            else:
                new_crontab_lines.append(line)
    
    if change_count == 0:
        print("⚠️ 変更対象が見つかりませんでした")
        return False
    
    # 4. 新しいcrontab作成
    new_crontab_content = '\n'.join(new_crontab_lines)
    
    # 5. 一時ファイルに保存
    temp_crontab_file = f"temp_23time_crontab_{timestamp}.txt"
    with open(temp_crontab_file, 'w') as f:
        f.write(new_crontab_content)
    
    print(f"\n📊 変更サマリー:")
    print(f"変更件数: {change_count}件")
    print(f"新しい配信時間:")
    print(f"  朝: 7時 ✅")
    print(f"  夜: 23時 ✅")
    
    # 6. crontab適用
    try:
        result = subprocess.run(['crontab', temp_crontab_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 23時変更cron適用成功")
            
            # 適用確認
            verify_result = subprocess.run(['crontab', '-l'], 
                                         capture_output=True, text=True)
            if verify_result.returncode == 0:
                verify_crontab = verify_result.stdout
                morning_count = verify_crontab.count("0 7")
                evening_count = verify_crontab.count("0 19") 
                night_count = verify_crontab.count("0 23")
                
                print(f"✅ 変更確認:")
                print(f"  朝7時ジョブ: {morning_count}個")
                print(f"  夜19時ジョブ: {evening_count}個")
                print(f"  夜23時ジョブ: {night_count}個")
                
                if night_count > 0 and evening_count == 0:
                    print(f"🎉 23時変更完了！")
                    
                    # 一時ファイル削除
                    os.remove(temp_crontab_file)
                    
                    print(f"\n🕐 新しい配信スケジュール:")
                    print(f"🌅 朝7:00: 完璧な天気絵文字メール配信")
                    print(f"🌙 夜23:00: 完璧な天気絵文字メール配信")
                    print(f"📧 内容: ☁️（☀️）☁️ → ☀️（☔️⚡️）等完璧対応")
                    
                    return True
                else:
                    print(f"⚠️ 変更確認に問題あり")
                    return False
            else:
                print(f"❌ 変更確認失敗")
                return False
        else:
            print(f"❌ 23時変更cron適用失敗: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ cron適用エラー: {e}")
        return False
    
    print(f"\n🔄 復旧方法（問題発生時）:")
    print(f"crontab {backup_file}")

if __name__ == "__main__":
    print("❓ 夜の配信時間を19時→23時に変更しますか？")
    print("現在: 朝7時・夜19時")
    print("変更後: 朝7時・夜23時")
    print("")
    print("変更する場合は、このスクリプトを実行してください。")
    
    # 実際の変更実行
    change_evening_to_23()
