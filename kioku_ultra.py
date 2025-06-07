#!/usr/bin/env python3
"""
🧠 kioku超強化システム v1.0
二度と壊れない自己修復AI記憶システム
"""
import os
import sys
import json
import shutil
import subprocess
import logging
import re
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

class KiokuUltraSystem:
    """kioku超強化システム"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.logger = self._setup_logger()
        self.config = self._load_config()
        
        # 重要ファイルリスト
        self.critical_files = [
            'main.py', 'settings_manager.py', 'email_notifier.py',
            'lvyuan_collector.py', 'logger.py', 'data_util.py',
            'settings.json'
        ]
        
        # 成功状態の参照
        self.success_snapshots = self._find_success_snapshots()
        
        self.logger.info("kioku超強化システム初期化完了")
    
    def _setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('kioku_ultra')
        logger.setLevel(logging.INFO)
        
        # ファイルハンドラー
        log_file = f"logs/kioku_ultra_{self.timestamp}.log"
        os.makedirs('logs', exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    def _load_config(self):
        """設定読み込み"""
        config_file = 'kioku_ultra_config.json'
        
        default_config = {
            "auto_backup_interval": 300,  # 5分
            "health_check_interval": 60,  # 1分
            "max_backups": 50,
            "syntax_check_enabled": True,
            "auto_repair_enabled": True,
            "emergency_mode": False
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                self.logger.warning(f"設定ファイル読み込みエラー: {e}")
        
        return default_config
    
    def _find_success_snapshots(self):
        """成功スナップショットを検索"""
        snapshots = []
        for item in Path('.').glob('*success_snapshot*'):
            if item.is_dir():
                snapshots.append(str(item))
        
        snapshots.sort(reverse=True)  # 新しい順
        self.logger.info(f"成功スナップショット発見: {len(snapshots)}個")
        return snapshots
    
    def comprehensive_health_check(self):
        """包括的健康チェック"""
        self.logger.info("包括的健康チェック開始")
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'issues': [],
            'warnings': [],
            'file_status': {}
        }
        
        # 1. ファイル存在チェック
        for file_path in self.critical_files:
            if os.path.exists(file_path):
                health_report['file_status'][file_path] = 'exists'
            else:
                health_report['file_status'][file_path] = 'missing'
                health_report['issues'].append(f"重要ファイル不存在: {file_path}")
        
        # 2. 構文チェック
        syntax_errors = self._check_all_syntax()
        if syntax_errors:
            health_report['issues'].extend(syntax_errors)
        
        # 3. 依存関係チェック
        dependency_issues = self._check_dependencies()
        if dependency_issues:
            health_report['warnings'].extend(dependency_issues)
        
        # 4. システムリソースチェック
        resource_warnings = self._check_system_resources()
        if resource_warnings:
            health_report['warnings'].extend(resource_warnings)
        
        # 総合判定
        if health_report['issues']:
            health_report['overall_status'] = 'critical'
        elif health_report['warnings']:
            health_report['overall_status'] = 'warning'
        
        return health_report
    
    def _check_all_syntax(self):
        """全Pythonファイル構文チェック"""
        syntax_errors = []
        
        for file_path in self.critical_files:
            if file_path.endswith('.py') and os.path.exists(file_path):
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'py_compile', file_path],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        syntax_errors.append(f"構文エラー: {file_path}")
                except Exception as e:
                    syntax_errors.append(f"構文チェック失敗: {file_path} - {str(e)}")
        
        return syntax_errors
    
    def _check_dependencies(self):
        """依存関係チェック"""
        warnings = []
        
        # 重要モジュールのimportテスト
        critical_modules = [
            'lvyuan_collector', 'settings_manager', 'email_notifier'
        ]
        
        for module in critical_modules:
            try:
                __import__(module)
            except ImportError as e:
                warnings.append(f"モジュールimport警告: {module} - {str(e)}")
        
        return warnings
    
    def _check_system_resources(self):
        """システムリソースチェック"""
        warnings = []
        
        try:
            # ディスク容量チェック
            disk_usage = shutil.disk_usage('.')
            free_space_gb = disk_usage.free / (1024**3)
            
            if free_space_gb < 1:  # 1GB未満
                warnings.append(f"ディスク容量不足: {free_space_gb:.1f}GB")
            
            # メモリチェック（簡易）
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    if 'MemAvailable' in meminfo:
                        for line in meminfo.split('\n'):
                            if 'MemAvailable' in line:
                                mem_kb = int(line.split()[1])
                                mem_mb = mem_kb / 1024
                                if mem_mb < 100:  # 100MB未満
                                    warnings.append(f"メモリ不足: {mem_mb:.0f}MB")
                                break
            except:
                pass  # メモリチェック失敗は無視
                
        except Exception as e:
            warnings.append(f"リソースチェック失敗: {str(e)}")
        
        return warnings
    
    def auto_backup_system(self):
        """自動バックアップシステム"""
        backup_dir = f"kioku_auto_backup_{self.timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        self.logger.info(f"自動バックアップ開始: {backup_dir}")
        
        backed_up_files = []
        for file_path in self.critical_files:
            if os.path.exists(file_path):
                try:
                    if os.path.isdir(file_path):
                        shutil.copytree(file_path, os.path.join(backup_dir, file_path))
                    else:
                        shutil.copy2(file_path, backup_dir)
                    backed_up_files.append(file_path)
                except Exception as e:
                    self.logger.error(f"バックアップエラー {file_path}: {str(e)}")
        
        # バックアップメタデータ
        metadata = {
            'timestamp': self.timestamp,
            'backed_up_files': backed_up_files,
            'system_status': 'healthy'
        }
        
        with open(os.path.join(backup_dir, 'backup_metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"バックアップ完了: {len(backed_up_files)}ファイル")
        return backup_dir
    
    def emergency_recovery(self):
        """緊急復旧システム"""
        self.logger.critical("緊急復旧システム開始")
        
        if not self.success_snapshots:
            self.logger.error("成功スナップショットが見つかりません")
            return False
        
        latest_snapshot = self.success_snapshots[0]
        self.logger.info(f"最新スナップショットから復旧: {latest_snapshot}")
        
        recovery_log = []
        
        for file_path in self.critical_files:
            snapshot_file = os.path.join(latest_snapshot, file_path)
            if os.path.exists(snapshot_file):
                try:
                    # 現在のファイルをバックアップ
                    if os.path.exists(file_path):
                        backup_name = f"{file_path}.emergency_backup_{self.timestamp}"
                        shutil.copy2(file_path, backup_name)
                    
                    # スナップショットから復旧
                    if os.path.isdir(snapshot_file):
                        if os.path.exists(file_path):
                            shutil.rmtree(file_path)
                        shutil.copytree(snapshot_file, file_path)
                    else:
                        shutil.copy2(snapshot_file, file_path)
                    
                    recovery_log.append(f"復旧成功: {file_path}")
                    self.logger.info(f"復旧成功: {file_path}")
                    
                except Exception as e:
                    recovery_log.append(f"復旧失敗: {file_path} - {str(e)}")
                    self.logger.error(f"復旧失敗: {file_path} - {str(e)}")
        
        # 復旧後の健康チェック
        health_report = self.comprehensive_health_check()
        
        if health_report['overall_status'] == 'healthy':
            self.logger.info("緊急復旧成功")
            return True
        else:
            self.logger.error("緊急復旧後も問題が残存")
            return False
    
    def continuous_monitoring(self, duration_minutes=60):
        """継続監視システム"""
        self.logger.info(f"継続監視開始: {duration_minutes}分間")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        last_backup = start_time
        last_health_check = start_time
        
        while time.time() < end_time:
            current_time = time.time()
            
            # 定期バックアップ
            if current_time - last_backup > self.config['auto_backup_interval']:
                self.auto_backup_system()
                last_backup = current_time
            
            # 定期健康チェック
            if current_time - last_health_check > self.config['health_check_interval']:
                health_report = self.comprehensive_health_check()
                
                if health_report['overall_status'] == 'critical':
                    self.logger.critical("重大な問題を検出、緊急復旧を実行")
                    if self.config['auto_repair_enabled']:
                        self.emergency_recovery()
                
                last_health_check = current_time
            
            time.sleep(10)  # 10秒間隔
        
        self.logger.info("継続監視完了")
    
    def generate_status_report(self):
        """ステータスレポート生成"""
        health_report = self.comprehensive_health_check()
        
        report = f"""
🧠 kioku超強化システム ステータスレポート
生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【総合状態】
状態: {health_report['overall_status'].upper()}

【ファイル状態】
"""
        
        for file_path, status in health_report['file_status'].items():
            status_emoji = "✅" if status == "exists" else "❌"
            report += f"{status_emoji} {file_path}: {status}\n"
        
        if health_report['issues']:
            report += "\n【重要な問題】\n"
            for issue in health_report['issues']:
                report += f"🚨 {issue}\n"
        
        if health_report['warnings']:
            report += "\n【警告】\n"
            for warning in health_report['warnings']:
                report += f"⚠️ {warning}\n"
        
        report += f"""
【バックアップ状況】
成功スナップショット: {len(self.success_snapshots)}個
最新スナップショット: {self.success_snapshots[0] if self.success_snapshots else 'なし'}

【システム構成】
Python: {sys.version.split()[0]}
作業ディレクトリ: {os.getcwd()}
監視対象ファイル: {len(self.critical_files)}個

---
kioku超強化システム v1.0
"""
        
        return report

def main():
    """メイン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description="kioku超強化システム")
    parser.add_argument('--health-check', action='store_true', help='健康チェック実行')
    parser.add_argument('--backup', action='store_true', help='バックアップ実行')
    parser.add_argument('--recovery', action='store_true', help='緊急復旧実行')
    parser.add_argument('--monitor', type=int, default=60, help='継続監視（分）')
    parser.add_argument('--report', action='store_true', help='ステータスレポート')
    
    args = parser.parse_args()
    
    kioku = KiokuUltraSystem()
    
    if args.health_check:
        report = kioku.comprehensive_health_check()
        print(f"健康状態: {report['overall_status']}")
        if report['issues']:
            print("問題:", report['issues'])
    
    elif args.backup:
        backup_dir = kioku.auto_backup_system()
        print(f"バックアップ完了: {backup_dir}")
    
    elif args.recovery:
        success = kioku.emergency_recovery()
        print("緊急復旧成功" if success else "緊急復旧失敗")
    
    elif args.report:
        report = kioku.generate_status_report()
        print(report)
    
    else:
        print("継続監視を開始します...")
        kioku.continuous_monitoring(args.monitor)

if __name__ == "__main__":
    main()
