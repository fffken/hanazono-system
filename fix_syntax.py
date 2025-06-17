#!/usr/bin/env python3
import datetime
import os
import shutil

def fix_syntax():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔧 シンタックスエラー確認 {timestamp}")
    
    target_file = "system_health_monitor.py"
    backup_file = f"backup_{timestamp}.py"
    
    # バックアップ作成
    shutil.copy2(target_file, backup_file)
    print(f"✅ バックアップ: {backup_file}")
    
    # エラー箇所確認
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"🔍 エラー行周辺:")
    for i in range(2, 8):
        line_num = i + 1
        line_content = lines[i].rstrip()
        marker = " → " if line_num == 4 else "   "
        print(f"{marker}行{line_num}: {repr(line_content)}")

if __name__ == "__main__":
    fix_syntax()
