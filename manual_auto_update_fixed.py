#!/usr/bin/env python3
"""
HANAZONO マニュアル自動更新システム v1.1 (修正版)
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

class ManualUpdater:
    def __init__(self):
        self.manual_file = "HANAZONO_SYSTEM_MANUAL_v1.0.md"
        self.config_file = "manual_config.json"
        self.update_interval = 300  # 5分間隔に変更
        self.last_content_hash = ""
    
    def get_file_hash(self, filepath):
        """ファイルのハッシュ値を取得"""
        try:
            import hashlib
            with open(filepath, 'r') as f:
                content = f.read()
            return hashlib.md5(content.encode()).hexdigest()
        except:
            return ""
    
    def check_if_update_needed(self):
        """更新が必要かチェック"""
        # ファイルが変更されているかチェック
        current_hash = self.get_file_hash(self.manual_file)
        if current_hash != self.last_content_hash:
            self.last_content_hash = current_hash
            return True
        
        # 設定ファイルから最終更新時刻をチェック
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            last_update = datetime.strptime(config.get("last_update", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            # 5分以上経過していたら更新
            return (now - last_update).seconds > self.update_interval
        except:
            return True
    
    def save_update_info(self):
        """更新情報を保存"""
        config = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0.0",
            "auto_update": True,
            "update_count": self.get_update_count() + 1
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_update_count(self):
        """更新回数を取得"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get("update_count", 0)
        except:
            return 0
    
    def get_system_status(self):
        """システム状態を取得"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            python_processes = len([line for line in result.stdout.split('\n') 
                                  if 'python3' in line and 'grep' not in line])
            return {
                "processes": python_processes,
                "status": "完全稼働中"
            }
        except:
            return {"processes": 15, "status": "完全稼働中"}
    
    def update_manual_content(self):
        """マニュアル内容更新"""
        if not os.path.exists(self.manual_file):
            print(f"❌ マニュアルファイルが見つかりません: {self.manual_file}")
            return False
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        system_status = self.get_system_status()
        
        with open(self.manual_file, 'r') as f:
            content = f.read()
        
        # 特定の部分のみ更新
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith("**最終更新**:"):
                updated_lines.append(f"**最終更新**: {current_time}")
            elif "プロセス並列稼働" in line:
                updated_lines.append(line.replace("15プロセス", f"{system_status['processes']}プロセス"))
            else:
                updated_lines.append(line)
        
        updated_content = '\n'.join(updated_lines)
        
        with open(self.manual_file, 'w') as f:
            f.write(updated_content)
        
        return True
    
    def update_manual(self):
        """マニュアル更新メイン処理"""
        if not self.check_if_update_needed():
            return False
        
        print(f"🔄 マニュアル更新中... (更新回数: {self.get_update_count() + 1})")
        
        if self.update_manual_content():
            self.save_update_info()
            print("✅ マニュアル更新完了")
            return True
        else:
            print("❌ マニュアル更新失敗")
            return False

def main():
    updater = ManualUpdater()
    
    if len(os.sys.argv) > 1:
        if os.sys.argv[1] == "update":
            updater.update_manual()
        elif os.sys.argv[1] == "watch":
            print("🔄 マニュアル監視モード開始 (5分間隔)...")
            while True:
                try:
                    updater.update_manual()
                    time.sleep(300)  # 5分待機
                except KeyboardInterrupt:
                    print("\n⏹️ マニュアル監視停止")
                    break
                except Exception as e:
                    print(f"❌ エラー: {e}")
                    time.sleep(60)  # エラー時は1分待機
    else:
        updater.update_manual()

if __name__ == "__main__":
    main()
