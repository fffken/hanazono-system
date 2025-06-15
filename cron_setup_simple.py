#!/usr/bin/env python3
# 簡潔版cron設定（完全非破壊的）
import datetime
import subprocess
import os

def setup_hanazono_cron():
    """HANAZONOシステムcron設定"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"⏰ HANAZONOシステムcron設定開始 {timestamp}")
    
    # 1. 現在のcrontabバックアップ
    backup_file = f"crontab_backup_{timestamp}.txt"
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""
        
        with open(backup_file, 'w') as f:
            f.write(current_crontab)
        print(f"✅ crontabバックアップ: {backup_file}")
    except Exception as e:
        print(f"❌ バックアップエラー: {e}")
        return False
    
    # 2. 新しいcronジョブ作成
    current_dir = os.getcwd()
    new_jobs = [
        "",
        "# HANAZONOシステム 定期配信",
        f"0 7 * * * cd {current_dir} && python3 abc_integration_complete_test.py",
        f"0 19 * * * cd {current_dir} && python3 abc_integration_complete_test.py",
        ""
    ]
    
    # 3. crontab適用
    new_crontab = current_crontab + "\n".join(new_jobs)
    temp_file = f"temp_crontab_{timestamp}.txt"
    
    try:
        with open(temp_file, 'w') as f:
            f.write(new_crontab)
        
        result = subprocess.run(['crontab', temp_file], capture_output=True, text=True)
        os.remove(temp_file)
        
        if result.returncode == 0:
            print("✅ cron設定適用成功")
            print("⏰ 朝7:00・夜19:00に自動メール配信開始")
            
            # 管理スクリプト作成
            manager_script = f"""#!/bin/bash
# HANAZONOシステム cron管理
case "$1" in
    "status") crontab -l | grep -A 5 "HANAZONO" ;;
    "restore") crontab {backup_file} ;;
    "test") cd {current_dir} && python3 abc_integration_complete_test.py ;;
    *) echo "使用方法: bash $0 [status|restore|test]" ;;
esac"""
            
            manager_file = f"hanazono_cron_manager.sh"
            with open(manager_file, 'w') as f:
                f.write(manager_script)
            os.chmod(manager_file, 0o755)
            
            print(f"✅ 管理スクリプト: {manager_file}")
            print(f"🔧 管理: bash {manager_file} status")
            print(f"🔄 復旧: bash {manager_file} restore")
            
            return True
        else:
            print(f"❌ cron設定失敗: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ cron適用エラー: {e}")
        return False

if __name__ == "__main__":
    success = setup_hanazono_cron()
    if success:
        print("🎉 10分完成！自動配信開始")
    else:
        print("❌ 設定失敗")
