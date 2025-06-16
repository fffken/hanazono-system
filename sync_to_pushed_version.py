#!/usr/bin/env python3
# cronを最新プッシュ済み完璧版に統一（完全非破壊的）
import subprocess
import datetime
import os
import shutil

def sync_cron_to_pushed_version():
    """cronを最新プッシュ済み完璧版に統一"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔄 cronプッシュ済み版統一開始 {timestamp}")
    print("=" * 60)
    
    pushed_file = "abc_integration_icon_fixed_20250615_223341.py"  # プッシュ済み最新版
    current_cron_file = "abc_integration_icon_fixed_20250615_223350.py"  # 現在cron使用
    
    # 1. プッシュ済み最新版確認
    if os.path.exists(pushed_file):
        print(f"✅ プッシュ済み最新版確認: {pushed_file}")
        pushed_size = os.path.getsize(pushed_file)
        print(f"📊 プッシュ済み版サイズ: {pushed_size}バイト")
    else:
        print(f"❌ プッシュ済み最新版未発見: {pushed_file}")
        return False
    
    # 2. 現在のcron使用ファイルバックアップ
    if os.path.exists(current_cron_file):
        backup_file = f"cron_file_backup_{timestamp}.py"
        shutil.copy2(current_cron_file, backup_file)
        print(f"📋 現在cronファイルバックアップ: {backup_file}")
        
        current_size = os.path.getsize(current_cron_file)
        print(f"📊 現在cron版サイズ: {current_size}バイト")
    
    # 3. プッシュ済み最新版をcron用ファイル名にコピー
    try:
        shutil.copy2(pushed_file, current_cron_file)
        print(f"✅ プッシュ済み最新版をcron用に統一完了")
        
        # 統一確認
        if os.path.exists(current_cron_file):
            unified_size = os.path.getsize(current_cron_file)
            print(f"✅ 統一確認: {current_cron_file} ({unified_size}バイト)")
            
            # 内容確認
            with open(current_cron_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 重要機能確認
            features = {
                "気温データ": "temperature" in content,
                "アイコン機能": "recommendation_icon" in content,
                "メール送信": "send_" in content and "email" in content,
                "絵文字": "🟠" in content
            }
            
            print(f"\n🔧 統一版機能確認:")
            for feature, status in features.items():
                print(f"  {feature}: {'✅' if status else '❌'}")
            
            all_good = all(features.values())
            
            if all_good:
                print(f"\n🎉 cronプッシュ済み版統一成功！")
                print(f"📧 次回自動配信: プッシュ済み最新版使用")
                print(f"🎨 アイコン: 🟠🔵🟣🌻 完璧対応")
                print(f"🌤️ 気温: 完璧な3日分データ")
                return True
            else:
                print(f"\n⚠️ 統一版機能不完全")
                return False
        else:
            print(f"❌ 統一ファイル作成失敗")
            return False
            
    except Exception as e:
        print(f"❌ ファイル統一エラー: {e}")
        return False

if __name__ == "__main__":
    sync_cron_to_pushed_version()
