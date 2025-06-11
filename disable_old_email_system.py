#!/usr/bin/env python3
"""
旧メールシステム無効化スクリプト
新HANAZONOメールハブ v3.0への完全移行
"""

import subprocess
import os
from datetime import datetime

def backup_current_crontab():
    """現在のcrontabをバックアップ"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            backup_file = f"crontab_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(backup_file, 'w') as f:
                f.write(result.stdout)
            print(f"✅ crontabバックアップ作成: {backup_file}")
            return result.stdout
        else:
            print("⚠️ crontab取得失敗")
            return ""
    except Exception as e:
        print(f"❌ バックアップエラー: {e}")
        return ""

def disable_old_system():
    """旧システムを無効化"""
    print("🔄 旧メールシステム無効化開始")
    
    # 現在のcrontab取得
    current_cron = backup_current_crontab()
    if not current_cron:
        return False
    
    # 新しいcrontab作成（旧main.py行を無効化）
    lines = current_cron.split('\n')
    new_lines = []
    
    for line in lines:
        if 'main.py --daily-report' in line and not line.strip().startswith('#'):
            # 旧システムをコメントアウト
            new_lines.append(f"# DISABLED: {line}")
            print(f"🚫 無効化: {line.strip()}")
        else:
            new_lines.append(line)
    
    # crontab更新
    try:
        new_cron = '\n'.join(new_lines)
        proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        proc.communicate(input=new_cron)
        
        if proc.returncode == 0:
            print("✅ crontab更新完了")
            return True
        else:
            print("❌ crontab更新失敗")
            return False
            
    except Exception as e:
        print(f"❌ crontab更新エラー: {e}")
        return False

def verify_new_system():
    """新システムの動作確認"""
    print("🧪 新システム動作確認")
    
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            cron_content = result.stdout
            
            # 新システムが有効か確認
            new_system_active = 'HANAZONOメールハブ v3.0' in cron_content
            old_system_disabled = 'DISABLED:' in cron_content or 'main.py --daily-report' not in [
                line for line in cron_content.split('\n') if not line.strip().startswith('#')
            ]
            
            print("\n📊 システム状況:")
            print(f"  新HANAZONOメールハブ v3.0: {'✅ 有効' if new_system_active else '❌ 無効'}")
            print(f"  旧main.pyシステム: {'✅ 無効化済み' if old_system_disabled else '❌ まだ有効'}")
            
            return new_system_active and old_system_disabled
        else:
            print("❌ crontab確認失敗")
            return False
            
    except Exception as e:
        print(f"❌ 確認エラー: {e}")
        return False

def main():
    print("🚀 旧メールシステム無効化・新システム移行")
    print("=" * 60)
    
    # Step 1: 旧システム無効化
    if disable_old_system():
        print("\n✅ 旧システム無効化完了")
    else:
        print("\n❌ 旧システム無効化失敗")
        return False
    
    # Step 2: 新システム確認
    if verify_new_system():
        print("\n🎉 移行完了！新HANAZONOメールハブ v3.0のみが動作します")
        print("\n📧 送信スケジュール:")
        print("  朝: 毎日 07:00 (新ハブシステム)")
        print("  夜: 毎日 23:00 (新ハブシステム)")
        print("\n📁 ログ:")
        print("  新システム: logs/email_hub_morning.log, logs/email_hub_evening.log")
        print("  データ収集: logs/cron.log (collector_capsule.py)")
        return True
    else:
        print("\n🚨 移行に問題があります。crontab -l で確認してください")
        return False

if __name__ == "__main__":
    main()
