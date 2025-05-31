#!/usr/bin/env python3
"""
HANAZONO システム運用最適化エンジン v1.0
自動問題解決・予防保守・継続的効率化
"""

import os
import sys
import json
import subprocess
import psutil
import glob
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

class HANAZONOOptimizer:
    def __init__(self):
        self.base_dir = Path.home() / "lvyuan_solar_control"
        self.optimization_log = self.base_dir / "logs" / "optimization.log"
        self.optimization_log.parent.mkdir(exist_ok=True)
        self.issues_found = []
        self.fixes_applied = []
        
    def run_optimization(self, mode="standard"):
        """運用最適化メイン実行"""
        print("🏆 HANAZONOシステム運用最適化エンジン v1.0")
        print("=" * 60)
        print("⚡ 自動問題解決・予防保守・継続的効率化実行中...")
        
        # 最適化ログ開始
        self._log_start()
        
        if mode == "health":
            self._health_check_mode()
        elif mode == "monitor":
            self._monitoring_mode()
        else:
            self._standard_optimization()
            
        # 結果レポート
        self._generate_optimization_report()
        
    def _standard_optimization(self):
        """標準最適化実行"""
        optimizations = [
            ("🔍 システム診断", self._system_diagnosis),
            ("🔧 自動問題修正", self._auto_problem_fixing),
            ("📊 パフォーマンス最適化", self._performance_optimization),
            ("🗂️ ファイルシステム整理", self._filesystem_cleanup),
            ("🔄 予防保守実行", self._preventive_maintenance),
            ("📈 効率化提案生成", self._generate_efficiency_suggestions)
        ]
        
        for step, optimization_func in optimizations:
            print(f"\n{step}実行中...")
            try:
                optimization_func()
                print(f"   ✅ {step}完了")
            except Exception as e:
                print(f"   ⚠️ {step}部分失敗: {e}")
                self.issues_found.append(f"{step}: {e}")
    
    def _health_check_mode(self):
        """健康診断モード"""
        print("🩺 システム健康診断モード実行中...")
        
        health_checks = [
            ("CPU・メモリ使用率", self._check_resource_usage),
            ("ディスク容量", self._check_disk_space),
            ("プロセス状況", self._check_processes),
            ("ログファイル状況", self._check_log_files),
            ("Git リポジトリ", self._check_git_health),
            ("Python環境", self._check_python_environment)
        ]
        
        health_score = 0
        total_checks = len(health_checks)
        
        for check_name, check_func in health_checks:
            print(f"▶️ {check_name}確認中...")
            try:
                result = check_func()
                if result:
                    print(f"   ✅ {check_name}: 正常")
                    health_score += 1
                else:
                    print(f"   ⚠️ {check_name}: 要注意")
                    self.issues_found.append(f"{check_name}: 問題検出")
            except Exception as e:
                print(f"   ❌ {check_name}: エラー - {e}")
                self.issues_found.append(f"{check_name}: {e}")
        
        # 健康スコア表示
        health_percentage = (health_score / total_checks) * 100
        print(f"\n🏥 システム健康スコア: {health_percentage:.1f}% ({health_score}/{total_checks})")
        
        if health_percentage >= 90:
            print("✅ システム状態: 非常に良好")
        elif health_percentage >= 70:
            print("🟡 システム状態: 良好（軽微な改善推奨）")
        else:
            print("🔴 システム状態: 要改善（最適化推奨）")
    
    def _monitoring_mode(self):
        """24時間監視モード"""
        print("📊 24時間監視モード開始")
        print("手動終了: Ctrl+C")
        
        try:
            monitor_count = 0
            while monitor_count < 144:  # 24時間（10分間隔）
                print(f"\n📈 監視サイクル {monitor_count + 1}/144")
                
                # リアルタイム監視
                self._realtime_monitoring()
                
                # 問題自動検出・修正
                if monitor_count % 6 == 0:  # 1時間ごと
                    self._auto_problem_detection()
                
                # 予防保守
                if monitor_count % 36 == 0:  # 6時間ごと
                    self._preventive_maintenance()
                
                monitor_count += 1
                time.sleep(600)  # 10分待機
                
        except KeyboardInterrupt:
            print("\n📊 監視モード手動終了")
    
    def _system_diagnosis(self):
        """システム診断"""
        # CPU・メモリ・ディスク使用率チェック
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 警告レベルチェック
        if cpu_percent > 80:
            self.issues_found.append(f"高CPU使用率: {cpu_percent}%")
        if memory.percent > 80:
            self.issues_found.append(f"高メモリ使用率: {memory.percent}%")
        if disk.percent > 90:
            self.issues_found.append(f"ディスク容量不足: {disk.percent}%")
        
        # プロセス異常チェック
        python_processes = [p for p in psutil.process_iter() if 'python' in p.name().lower()]
        if len(python_processes) == 0:
            self.issues_found.append("Pythonプロセスが実行されていません")
        elif len(python_processes) > 10:
            self.issues_found.append(f"Pythonプロセス数が多すぎます: {len(python_processes)}個")
    
    def _auto_problem_fixing(self):
        """自動問題修正"""
        fixes_applied = 0
        
        # Python cache削除
        try:
            subprocess.run(['find', '.', '-name', '__pycache__', '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'], 
                          cwd=self.base_dir, check=False)
            fixes_applied += 1
            self.fixes_applied.append("Python cache削除")
        except:
            pass
        
        # 古いログファイル圧縮
        try:
            logs_dir = self.base_dir / "logs"
            if logs_dir.exists():
                cutoff_date = datetime.now() - timedelta(days=7)
                for log_file in logs_dir.glob("*.log"):
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        if log_file.stat().st_size > 1024 * 1024:  # 1MB以上
                            # gzip圧縮
                            subprocess.run(['gzip', str(log_file)], check=False)
                            fixes_applied += 1
                            self.fixes_applied.append(f"ログ圧縮: {log_file.name}")
        except:
            pass
        
        # Git状態自動整理
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if changes > 15:
                # 自動Git整理実行
                subprocess.run(['bash', 'scripts/auto_git_organize_push.sh'], 
                             cwd=self.base_dir, check=False)
                fixes_applied += 1
                self.fixes_applied.append("Git状態自動整理")
        except:
            pass
        
        print(f"   🔧 自動修正実行: {fixes_applied}件")
    
    def _performance_optimization(self):
        """パフォーマンス最適化"""
        optimizations = 0
        
        # メモリ使用量最適化
        try:
            if psutil.virtual_memory().percent > 70:
                # 不要プロセス確認（実際には終了しない、警告のみ）
                processes = []
                for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                    if p.info['memory_percent'] > 5:
                        processes.append(p.info)
                
                if processes:
                    optimizations += 1
                    self.fixes_applied.append("高メモリ使用プロセス検出")
        except:
            pass
        
        # ディスク最適化
        try:
            # 一時ファイル削除
            temp_dirs = ["/tmp", "/var/tmp"]
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    temp_files = glob.glob(f"{temp_dir}/*hanazono*")
                    for temp_file in temp_files:
                        try:
                            if os.path.isfile(temp_file):
                                os.remove(temp_file)
                                optimizations += 1
                        except:
                            pass
        except:
            pass
        
        print(f"   ⚡ パフォーマンス最適化: {optimizations}件")
    
    def _filesystem_cleanup(self):
        """ファイルシステム整理"""
        cleanup_count = 0
        
        # 古いバックアップファイル整理
        try:
            backup_dirs = list(self.base_dir.glob("system_backups/backup_*"))
            if len(backup_dirs) > 10:  # 10個以上ある場合
                # 最新10個以外を削除
                backup_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for old_backup in backup_dirs[10:]:
                    try:
                        shutil.rmtree(old_backup)
                        cleanup_count += 1
                        self.fixes_applied.append(f"古いバックアップ削除: {old_backup.name}")
                    except:
                        pass
        except:
            pass
        
        # 重複ファイル確認
        try:
            backup_files = list(self.base_dir.glob("*.backup*"))
            if len(backup_files) > 20:
                # 最新20個以外を削除
                backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for old_file in backup_files[20:]:
                    try:
                        old_file.unlink()
                        cleanup_count += 1
                        self.fixes_applied.append(f"古いバックアップファイル削除: {old_file.name}")
                    except:
                        pass
        except:
            pass
        
        print(f"   🗂️ ファイル整理: {cleanup_count}件")
    
    def _preventive_maintenance(self):
        """予防保守"""
        maintenance_count = 0
        
        # システム設定確認
        try:
            settings_file = self.base_dir / "settings.json"
            if settings_file.exists():
                with open(settings_file) as f:
                    settings = json.load(f)
                
                # 設定の整合性確認
                required_keys = ['inverter', 'email', 'monitoring']
                missing_keys = [key for key in required_keys if key not in settings]
                if missing_keys:
                    self.issues_found.append(f"設定キー不足: {missing_keys}")
                else:
                    maintenance_count += 1
                    self.fixes_applied.append("設定ファイル整合性確認")
        except:
            pass
        
        # cron設定確認
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                cron_jobs = [line for line in result.stdout.split('\n') 
                           if line.strip() and not line.startswith('#')]
                if len(cron_jobs) > 0:
                    maintenance_count += 1
                    self.fixes_applied.append(f"cron設定確認: {len(cron_jobs)}個のジョブ")
                else:
                    self.issues_found.append("cron設定が見つかりません")
        except:
            pass
        
        print(f"   🔄 予防保守: {maintenance_count}件")
    
    def _generate_efficiency_suggestions(self):
        """効率化提案生成"""
        suggestions = []
        
        # システムリソースベースの提案
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        if cpu_percent < 20 and memory.percent < 50:
            suggestions.append("リソース余裕あり - 追加機能実装可能")
        elif cpu_percent > 60:
            suggestions.append("CPU使用率高 - プロセス最適化推奨")
        elif memory.percent > 70:
            suggestions.append("メモリ使用率高 - メモリ効率化推奨")
        
        # Git状態ベースの提案
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if changes == 0:
                suggestions.append("Git状態良好 - 新機能開発推奨")
            elif changes > 10:
                suggestions.append("Git整理推奨 - auto_git_organize_push.sh実行")
        except:
            pass
        
        # ファイル数ベースの提案
        python_files = list(self.base_dir.glob("*.py"))
        if len(python_files) > 20:
            suggestions.append("Pythonファイル多数 - モジュール化検討推奨")
        
        if not suggestions:
            suggestions = ["システム最適化済み - 高効率運用中"]
        
        print(f"   📈 効率化提案: {len(suggestions)}件生成")
        self.fixes_applied.extend([f"提案: {s}" for s in suggestions[:3]])
    
    # 健康診断用チェック関数群
    def _check_resource_usage(self):
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        return cpu < 80 and memory < 80
    
    def _check_disk_space(self):
        disk = psutil.disk_usage('/')
        return disk.percent < 90
    
    def _check_processes(self):
        python_processes = [p for p in psutil.process_iter() if 'python' in p.name().lower()]
        return 1 <= len(python_processes) <= 10
    
    def _check_log_files(self):
        logs_dir = self.base_dir / "logs"
        if not logs_dir.exists():
            return False
        log_files = list(logs_dir.glob("*.log"))
        return len(log_files) > 0
    
    def _check_git_health(self):
        try:
            result = subprocess.run(['git', 'status'], cwd=self.base_dir, 
                                  capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_python_environment(self):
        try:
            import flask, psutil
            return True
        except ImportError:
            return False
    
    def _realtime_monitoring(self):
        """リアルタイム監視"""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        
        print(f"   📊 CPU: {cpu}% | メモリ: {memory}% | 時刻: {datetime.now().strftime('%H:%M:%S')}")
        
        # 異常検出
        if cpu > 90:
            print(f"   🚨 CPU異常: {cpu}%")
        if memory > 90:
            print(f"   🚨 メモリ異常: {memory}%")
    
    def _auto_problem_detection(self):
        """自動問題検出"""
        print("   🔍 自動問題検出実行中...")
        detected = 0
        
        # リソース異常検出
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        
        if cpu > 85:
            print(f"   ⚠️ 高CPU使用率検出: {cpu}%")
            detected += 1
        if memory > 85:
            print(f"   ⚠️ 高メモリ使用率検出: {memory}%")
            detected += 1
        
        if detected == 0:
            print("   ✅ 問題検出なし")
    
    def _log_start(self):
        """最適化ログ開始"""
        with open(self.optimization_log, 'a') as f:
            f.write(f"\n=== 最適化実行開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    def _generate_optimization_report(self):
        """最適化レポート生成"""
        print("\n" + "=" * 60)
        print("📊 HANAZONOシステム運用最適化レポート")
        print("=" * 60)
        
        print(f"🔍 問題検出: {len(self.issues_found)}件")
        for issue in self.issues_found[:5]:
            print(f"   • {issue}")
        
        print(f"\n🔧 自動修正実行: {len(self.fixes_applied)}件")
        for fix in self.fixes_applied[:5]:
            print(f"   • {fix}")
        
        # システム状態サマリー
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            print(f"\n💻 現在のシステム状態:")
            print(f"   CPU: {cpu}% | メモリ: {memory}% | ディスク: {disk}%")
        except:
            pass
        
        print("\n🎯 推奨次アクション:")
        if len(self.issues_found) == 0:
            print("   ✅ システム最適化済み - 高効率運用継続")
        elif len(self.issues_found) <= 3:
            print("   🟡 軽微な改善推奨 - 継続監視")
        else:
            print("   🔴 重要な問題あり - 詳細確認推奨")
        
        print("=" * 60)
        
        # ログファイルに記録
        with open(self.optimization_log, 'a') as f:
            f.write(f"問題検出: {len(self.issues_found)}件\n")
            f.write(f"自動修正: {len(self.fixes_applied)}件\n")
            f.write(f"完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    if len(sys.argv) == 1:
        # デフォルト: 標準最適化
        optimizer = HANAZONOOptimizer()
        optimizer.run_optimization("standard")
    elif len(sys.argv) == 2:
        mode = sys.argv[1]
        optimizer = HANAZONOOptimizer()
        
        if mode in ["health", "monitor", "standard"]:
            optimizer.run_optimization(mode)
        else:
            print(f"❓ 不明なモード: {mode}")
            print("使用法: python3 hanazono_optimizer.py [health|monitor|standard]")
    else:
        print("使用法: python3 hanazono_optimizer.py [health|monitor|standard]")

if __name__ == "__main__":
    main()
