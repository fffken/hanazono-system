#!/usr/bin/env python3
"""
HANAZONOメールハブ v3.0 自動送信設定
朝7時・夜23時の定期配信設定
"""

import subprocess
import os
from datetime import datetime

def setup_cron_jobs():
    """cron設定の追加"""
    print("🕐 HANAZONOメールハブ v3.0 自動送信設定開始")
    
    # 現在のcrontab取得
    try:
        current_cron = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if current_cron.returncode == 0:
            existing_jobs = current_cron.stdout
        else:
            existing_jobs = ""
    except Exception as e:
        print(f"⚠️ 現在のcrontab取得エラー: {e}")
        existing_jobs = ""
    
    # 新しいcronジョブ定義
    project_path = os.path.expanduser("~/lvyuan_solar_control")
    new_jobs = [
        f"# HANAZONOメールハブ v3.0 自動送信",
        f"0 7 * * * cd {project_path} && /usr/bin/python3 -c \"from email_hub_core import EmailHubCore; hub = EmailHubCore(); hub.run_daily_report()\" >> logs/email_hub_morning.log 2>&1",
        f"0 23 * * * cd {project_path} && /usr/bin/python3 -c \"from email_hub_core import EmailHubCore; hub = EmailHubCore(); hub.run_daily_report()\" >> logs/email_hub_evening.log 2>&1",
        ""
    ]
    
    # 既存ジョブから重複削除
    lines = existing_jobs.split('\n')
    filtered_lines = []
    
    for line in lines:
        if 'HANAZONOメールハブ' not in line and 'email_hub_core' not in line:
            if line.strip():  # 空行でない場合のみ追加
                filtered_lines.append(line)
    
    # 新しいcrontab作成
    updated_cron = '\n'.join(filtered_lines + new_jobs)
    
    # crontab更新
    try:
        proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        proc.communicate(input=updated_cron)
        
        if proc.returncode == 0:
            print("✅ crontab設定完了")
            return True
        else:
            print("❌ crontab設定失敗")
            return False
            
    except Exception as e:
        print(f"❌ crontab設定エラー: {e}")
        return False

def create_log_directory():
    """ログディレクトリ作成"""
    log_dir = os.path.expanduser("~/lvyuan_solar_control/logs")
    os.makedirs(log_dir, exist_ok=True)
    print(f"📁 ログディレクトリ確保: {log_dir}")

def test_manual_execution():
    """手動実行テスト"""
    print("🧪 手動実行テスト開始")
    try:
        import sys
        sys.path.append('.')
        from email_hub_core import EmailHubCore
        
        hub = EmailHubCore()
        success = hub.run_daily_report()
        
        if success:
            print("✅ 手動実行テスト成功")
            return True
        else:
            print("❌ 手動実行テスト失敗")
            return False
            
    except Exception as e:
        print(f"❌ 手動実行テストエラー: {e}")
        return False

def main():
    print("🚀 HANAZONOメールハブ v3.0 自動送信設定")
    print("=" * 60)
    
    # Step 1: ログディレクトリ作成
    create_log_directory()
    
    # Step 2: 手動実行テスト
    if not test_manual_execution():
        print("🚨 手動実行テストが失敗したため、cron設定をスキップします")
        return False
    
    # Step 3: cron設定
    if setup_cron_jobs():
        print("\n🎉 設定完了！")
        print("📧 自動送信スケジュール:")
        print("  朝: 毎日 07:00")
        print("  夜: 毎日 23:00")
        print("\n📁 ログファイル:")
        print("  朝: logs/email_hub_morning.log")
        print("  夜: logs/email_hub_evening.log")
        print("\n🔍 設定確認コマンド:")
        print("  crontab -l")
        return True
    else:
        print("🚨 cron設定に失敗しました")
        return False

if __name__ == "__main__":
    main()
