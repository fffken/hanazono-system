#!/usr/bin/env python3
# system_health_monitor.py 動作確認＆事前調整（完全非破壊的）
import datetime
import subprocess
import os

def test_health_monitor():
    """system_health_monitor.py 動作確認＆事前調整"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🧪 system_health_monitor.py 動作確認＆事前調整開始 {timestamp}")
    print("=" * 70)
    
    target_file = "system_health_monitor.py"
    
    # 1. ファイル存在・基本情報確認
    print(f"📄 ファイル基本情報:")
    if os.path.exists(target_file):
        file_size = os.path.getsize(target_file)
        mtime = os.path.getmtime(target_file)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"  ✅ ファイル: {target_file}")
        print(f"  💾 サイズ: {file_size:,}バイト")
        print(f"  📅 更新日: {mtime_str}")
    else:
        print(f"  ❌ ファイル未発見: {target_file}")
        return False
    
    return True

if __name__ == "__main__":
    test_health_monitor()
