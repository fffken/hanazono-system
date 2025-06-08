#!/usr/bin/env python3
"""
HANAZONO Safe Guardian v2.0
AI誤判断完全対応・自動修復暴走防止システム
"""
import os
import time
import json
import threading
import subprocess
from datetime import datetime
from ultimate_protection_system import UltimateProtection

class HANAZONOSafeGuardian:
    def __init__(self):
        self.protector = UltimateProtection()
        self.monitoring = True
        self.last_health_check = None
        
        # 鉄壁保護設定
        self.sacred_vault = "email_protection_vault"
        self.emergency_contacts = ["fffken@gmail.com"]
        
        # AI暴走検知パターン
        self.dangerous_patterns = [
            "find.*-exec.*sed",  # 一括sed実行
            "while.*read.*sed",  # ループ内sed
            "for.*in.*sed",      # for文内sed
            "xargs.*sed",        # xargs sed
            "parallel.*sed"      # 並列sed
        ]
    
    def continuous_monitor(self):
        """24時間継続監視"""
        print("👁️ 24時間監視システム開始")
        
        while self.monitoring:
            try:
                # 1分間隔で重要機能チェック
                self.health_check()
                
                # 危険プロセス監視
                self.detect_dangerous_processes()
                
                # ファイル改竄検知
                self.detect_file_tampering()
                
                time.sleep(60)  # 1分間隔
                
            except Exception as e:
                self.emergency_alert(f"監視システムエラー: {e}")
                time.sleep(30)
    
    def health_check(self):
        """重要機能の健康度チェック"""
        critical_functions = {
            'email': 'python3 email_notifier.py --send-test-email',
            'data_collection': 'python3 lvyuan_collector.py --collect',
            'main_system': 'python3 main.py --check-cron'
        }
        
        for name, command in critical_functions.items():
            try:
                result = subprocess.run(
                    command.split(), 
                    capture_output=True, 
                    timeout=30,
                    cwd='/home/pi/lvyuan_solar_control'
                )
                
                if result.returncode != 0:
                    self.emergency_response(f"{name}機能異常検知")
                    
            except subprocess.TimeoutExpired:
                self.emergency_response(f"{name}機能タイムアウト")
            except Exception as e:
                self.emergency_response(f"{name}機能エラー: {e}")
    
    def detect_dangerous_processes(self):
        """危険な自動修復プロセス検知"""
        try:
            # 実行中プロセス確認
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = result.stdout
            
            for pattern in self.dangerous_patterns:
                if pattern in processes:
                    self.emergency_stop_dangerous_process(pattern)
                    
        except Exception as e:
            print(f"プロセス監視エラー: {e}")
    
    def emergency_stop_dangerous_process(self, pattern):
        """危険プロセスの緊急停止"""
        print(f"🚨 危険プロセス検知・緊急停止: {pattern}")
        
        # 関連プロセス全停止
        subprocess.run(['pkill', '-f', 'auto'], capture_output=True)
        subprocess.run(['pkill', '-f', 'fix'], capture_output=True)
        subprocess.run(['pkill', '-f', 'sed'], capture_output=True)
        
        # 緊急アラート
        self.emergency_alert(f"危険プロセス緊急停止: {pattern}")
    
    def emergency_response(self, crisis_message):
        """緊急対応システム"""
        print(f"🚨 緊急対応発動: {crisis_message}")
        
        # 1. 即座バックアップ
        self.create_emergency_backup()
        
        # 2. 自動修復停止
        self.stop_all_automation()
        
        # 3. 聖域ファイル復旧
        self.restore_sacred_files()
        
        # 4. 緊急通知
        self.emergency_alert(crisis_message)
    
    def create_emergency_backup(self):
        """緊急時バックアップ作成"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"CRISIS_BACKUP_{timestamp}"
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            for sacred_file in self.protector.sacred_files:
                if os.path.exists(sacred_file):
                    subprocess.run([
                        'cp', sacred_file, 
                        f"{backup_dir}/{sacred_file}_crisis_backup"
                    ])
            print(f"✅ 緊急バックアップ完了: {backup_dir}")
        except Exception as e:
            print(f"❌ 緊急バックアップ失敗: {e}")
    
    def stop_all_automation(self):
        """全自動化システム停止"""
        dangerous_scripts = [
            'auto_guardian.py',
            'syntax_error_auto_fixer.sh',
            'safe_mass_fix.sh',
            'auto_fix_system.sh'
        ]
        
        for script in dangerous_scripts:
            # プロセス停止
            subprocess.run(['pkill', '-f', script], capture_output=True)
            
            # スクリプト無効化
            if os.path.exists(script):
                subprocess.run(['mv', script, f"{script}.EMERGENCY_DISABLED"])
    
    def emergency_alert(self, message):
        """緊急アラート送信"""
        try:
            alert_command = [
                'python3', 'email_notifier.py', 
                '--emergency-alert', 
                f"🚨 HANAZONO緊急事態: {message}"
            ]
            subprocess.run(alert_command, timeout=30)
        except Exception as e:
            print(f"緊急アラート送信失敗: {e}")

if __name__ == "__main__":
    guardian = HANAZONOSafeGuardian()
    print("🛡️ HANAZONO Safe Guardian 起動")
    
    # 監視スレッド開始
    monitor_thread = threading.Thread(target=guardian.continuous_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    print("✅ 鉄壁保護システム稼働開始")
    
    try:
        while True:
            time.sleep(300)  # 5分間隔でメイン監視
    except KeyboardInterrupt:
        print("🛡️ Safe Guardian 停止")
        guardian.monitoring = False
