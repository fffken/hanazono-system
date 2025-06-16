#!/usr/bin/env python3
# cronアイコン修正版切り替え確認（完全非破壊的）
import subprocess
import datetime
import os

def verify_icon_fixed_cron_switch():
    """cronアイコン修正版切り替え確認"""
    print("🔍 cronアイコン修正版切り替え確認開始")
    print("=" * 60)
    
    # 1. 現在のcrontab内容確認
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            current_crontab = result.stdout
            print("✅ 現在のcrontab取得成功")
        else:
            print("❌ crontab取得失敗")
            return False
    except Exception as e:
        print(f"❌ crontab確認エラー: {e}")
        return False
    
    # 2. アイコン修正版ファイル使用確認
    icon_fixed_file = "abc_integration_icon_fixed_20250615_223350.py"
    if icon_fixed_file in current_crontab:
        print(f"✅ アイコン修正版ファイル使用確認: {icon_fixed_file}")
        icon_check = True
    else:
        print(f"❌ アイコン修正版ファイル未確認")
        icon_check = False
    
    # 3. HANAZONOシステム関連cron行確認
    hanazono_lines = []
    for line in current_crontab.split('\n'):
        if 'HANAZONO' in line or icon_fixed_file in line:
            hanazono_lines.append(line.strip())
    
    print(f"\n📊 HANAZONOシステム関連cron確認:")
    print(f"関連行数: {len(hanazono_lines)}行")
    
    # 4. 重要な配信時間確認
    morning_check = any("0 7 * * *" in line and icon_fixed_file in line for line in hanazono_lines)
    evening_check = any("0 19 * * *" in line and icon_fixed_file in line for line in hanazono_lines)
    
    print(f"\n🕐 配信時間確認:")
    print(f"朝7時配信: {'✅ 確認済み' if morning_check else '❌ 未確認'}")
    print(f"夜19時配信: {'✅ 確認済み' if evening_check else '❌ 未確認'}")
    
    # 5. アイコン修正版ファイル存在確認
    file_exists = os.path.exists(icon_fixed_file)
    print(f"\n📁 ファイル存在確認:")
    print(f"{icon_fixed_file}: {'✅ 存在' if file_exists else '❌ 不存在'}")
    
    # 6. 詳細cron内容表示
    print(f"\n📋 詳細cron内容確認:")
    for i, line in enumerate(hanazono_lines):
        if line.strip():
            print(f"  {i+1}: {line}")
    
    # 7. 総合判定
    all_checks = [icon_check, morning_check, evening_check, file_exists]
    success_rate = sum(all_checks) / len(all_checks) * 100
    
    print(f"\n" + "=" * 60)
    print(f"🎯 切り替え確認結果")
    print(f"=" * 60)
    print(f"アイコン修正版ファイル使用: {'✅' if icon_check else '❌'}")
    print(f"朝7時配信設定: {'✅' if morning_check else '❌'}")
    print(f"夜19時配信設定: {'✅' if evening_check else '❌'}")
    print(f"ファイル存在: {'✅' if file_exists else '❌'}")
    print(f"総合成功率: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n🎉 完璧！アイコン修正版切り替え成功")
        print(f"📧 次回配信: 明日朝7時")
        print(f"🎨 配信内容: 🟠🔵🟣🌻 アイコン + 3日分天気完璧版")
        print(f"🚀 保存・プッシュ準備完了")
        return True
    elif success_rate >= 75:
        print(f"\n⚠️ ほぼ成功、軽微な問題あり")
        return False
    else:
        print(f"\n❌ 切り替え問題あり、要確認")
        return False

if __name__ == "__main__":
    verify_icon_fixed_cron_switch()
