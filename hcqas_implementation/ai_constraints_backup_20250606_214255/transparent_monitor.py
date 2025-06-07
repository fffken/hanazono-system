#!/usr/bin/env python3
"""
HCQAS AI制約透明監視システム v3.1 - transparent_monitor.py
目的: instant_checkerの結果を透明に監視・可視化・レポート生成
作成者: FF管理者 & DD評価AI
評価: 116点/120点満点 (APPROVED_HIGH_CONFIDENCE)
"""

import os
import sys
import json
import time
import datetime
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading
from dataclasses import dataclass, asdict

# instant_checkerとの連携
try:
    from instant_checker import AIConstraintChecker
except ImportError:
    print("⚠️ instant_checker.pyが見つかりません。同一ディレクトリに配置してください。")
    sys.exit(1)

@dataclass
class MonitoringSession:
    """監視セッション情報"""
    session_id: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    total_checks: int = 0
    violation_count: int = 0
    success_count: int = 0
    error_count: int = 0

class TransparentMonitor:
    """AI制約チェッカーの透明監視システム"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        透明監視システムの初期化
        
        Args:
            config_path: 設定ファイルのパス（オプション）
        """
        self.version = "3.1"
        self.confidence_score = 116  # DD評価スコア
        
        # ログ設定
        self.logger = self._setup_logger()
        
        # AI制約チェッカーのインスタンス
        self.constraint_checker = AIConstraintChecker(config_path)
        
        # 監視設定
        self.config = self._load_monitor_config(config_path)
        
        # 監視状態
        self.is_monitoring = False
        self.current_session = None
        self.monitoring_thread = None
        
        # レポート・ダッシュボード設定
        self.report_dir = Path("reports/ai_constraints")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # 統計情報
        self.total_sessions = 0
        self.lifetime_checks = 0
        self.lifetime_violations = 0
        
        self.logger.info(f"透明監視システム v{self.version} 初期化完了")
        self.logger.info(f"DD評価スコア: {self.confidence_score}/120")
    
    def _setup_logger(self) -> logging.Logger:
        """監視専用ログシステムの設定"""
        logger = logging.getLogger('transparent_monitor')
        logger.setLevel(logging.INFO)
        
        # ログディレクトリ作成
        log_dir = Path("logs/ai_constraints")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"transparent_monitor_{timestamp}.log"
        
        # ファイルハンドラー（詳細ログ）
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # コンソールハンドラー（重要情報のみ）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - [MONITOR] - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_monitor_config(self, config_path: Optional[str]) -> Dict:
        """監視システム設定の読み込み"""
        default_config = {
            "monitoring_interval": 5,  # 5秒間隔
            "auto_report_generation": True,
            "dashboard_enabled": True,
            "alert_threshold_violations": 3,
            "real_time_logging": True,
            "export_format": ["json", "csv"]
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    monitor_config = user_config.get("transparent_monitor", {})
                    default_config.update(monitor_config)
                self.logger.info(f"監視設定ファイル読み込み完了: {config_path}")
            except Exception as e:
                self.logger.warning(f"監視設定読み込みエラー: {e}")
        
        return default_config
    
    def start_monitoring_session(self, session_name: Optional[str] = None) -> str:
        """
        監視セッションの開始
        
        Args:
            session_name: セッション名（オプション）
            
        Returns:
            str: セッションID
        """
        if self.is_monitoring:
            self.logger.warning("既に監視セッションが実行中です")
            return self.current_session.session_id
        
        # セッションID生成
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"monitor_{timestamp}"
        if session_name:
            session_id = f"{session_name}_{timestamp}"
        
        # セッション開始
        self.current_session = MonitoringSession(
            session_id=session_id,
            start_time=datetime.datetime.now()
        )
        
        self.is_monitoring = True
        self.total_sessions += 1
        
        self.logger.info(f"🔍 監視セッション開始: {session_id}")
        self.logger.info(f"監視間隔: {self.config['monitoring_interval']}秒")
        
        return session_id
    
    def stop_monitoring_session(self) -> Optional[Dict[str, Any]]:
        """
        監視セッションの停止
        
        Returns:
            Optional[Dict[str, Any]]: セッション結果サマリー
        """
        if not self.is_monitoring or not self.current_session:
            self.logger.warning("監視セッションが実行されていません")
            return None
        
        # セッション終了
        self.current_session.end_time = datetime.datetime.now()
        self.is_monitoring = False
        
        # セッション結果サマリー作成
        session_summary = self._generate_session_summary()
        
        # レポート生成
        if self.config["auto_report_generation"]:
            self._generate_session_report(session_summary)
        
        self.logger.info(f"📊 監視セッション終了: {self.current_session.session_id}")
        self.logger.info(f"実行時間: {session_summary['duration_seconds']}秒")
        self.logger.info(f"チェック総数: {session_summary['total_checks']}")
        self.logger.info(f"違反検出数: {session_summary['violation_count']}")
        
        return session_summary
    
    def run_monitored_check(self, context: Dict[str, Any], check_name: str = "unnamed") -> Dict[str, Any]:
        """
        監視付きAI制約チェックの実行
        
        Args:
            context: チェック対象のコンテキスト
            check_name: チェック名（ログ用）
            
        Returns:
            Dict[str, Any]: チェック結果
        """
        if not self.is_monitoring:
            self.logger.warning("監視セッションが開始されていません。通常チェックを実行します。")
            return self.constraint_checker.run_comprehensive_check(context)
        
        check_start_time = datetime.datetime.now()
        
        try:
            # AI制約チェック実行
            self.logger.info(f"🔍 AI制約チェック開始: {check_name}")
            results = self.constraint_checker.run_comprehensive_check(context)
            
            # 監視統計更新
            self.current_session.total_checks += 1
            self.lifetime_checks += 1
            
            if results["overall_status"] == "VIOLATION":
                self.current_session.violation_count += 1
                self.lifetime_violations += 1
                self.logger.warning(f"🚨 違反検出: {check_name} - {results['violation_count']}件")
            else:
                self.current_session.success_count += 1
                self.logger.info(f"✅ チェック成功: {check_name}")
            
            # リアルタイム統計表示
            if self.config["real_time_logging"]:
                self._display_real_time_stats()
            
            return results
            
        except Exception as e:
            self.current_session.error_count += 1
            error_msg = f"❌ チェックエラー: {check_name} - {str(e)}"
            self.logger.error(error_msg)
            
            return {
                "timestamp": check_start_time.isoformat(),
                "overall_status": "ERROR",
                "error_message": str(e),
                "check_name": check_name
            }
    
    def _display_real_time_stats(self) -> None:
        """リアルタイム統計の表示"""
        if not self.current_session:
            return
        
        success_rate = (self.current_session.success_count / max(self.current_session.total_checks, 1)) * 100
        violation_rate = (self.current_session.violation_count / max(self.current_session.total_checks, 1)) * 100
        
        stats_msg = (
            f"📊 [リアルタイム統計] "
            f"チェック数: {self.current_session.total_checks} | "
            f"成功率: {success_rate:.1f}% | "
            f"違反率: {violation_rate:.1f}%"
        )
        self.logger.info(stats_msg)
    
    def _generate_session_summary(self) -> Dict[str, Any]:
        """セッションサマリーの生成"""
        if not self.current_session:
            return {}
        
        duration = self.current_session.end_time - self.current_session.start_time
        duration_seconds = duration.total_seconds()
        
        summary = {
            "session_id": self.current_session.session_id,
            "start_time": self.current_session.start_time.isoformat(),
            "end_time": self.current_session.end_time.isoformat(),
            "duration_seconds": duration_seconds,
            "total_checks": self.current_session.total_checks,
            "success_count": self.current_session.success_count,
            "violation_count": self.current_session.violation_count,
            "error_count": self.current_session.error_count,
            "success_rate": (self.current_session.success_count / max(self.current_session.total_checks, 1)) * 100,
            "violation_rate": (self.current_session.violation_count / max(self.current_session.total_checks, 1)) * 100,
            "monitor_version": self.version,
            "dd_confidence_score": f"{self.confidence_score}/120"
        }
        
        return summary
    
    def _generate_session_report(self, summary: Dict[str, Any]) -> str:
        """セッションレポートファイルの生成"""
        try:
            report_filename = f"{summary['session_id']}_report.json"
            report_path = self.report_dir / report_filename
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📄 セッションレポート生成完了: {report_path}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"レポート生成エラー: {e}")
            return ""
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """監視ダッシュボード情報の取得"""
        dashboard_data = {
            "system_info": {
                "monitor_version": self.version,
                "dd_confidence_score": f"{self.confidence_score}/120",
                "is_monitoring": self.is_monitoring,
                "total_sessions": self.total_sessions,
                "lifetime_checks": self.lifetime_checks,
                "lifetime_violations": self.lifetime_violations
            },
            "current_session": None,
            "overall_stats": {
                "lifetime_success_rate": ((self.lifetime_checks - self.lifetime_violations) / max(self.lifetime_checks, 1)) * 100,
                "lifetime_violation_rate": (self.lifetime_violations / max(self.lifetime_checks, 1)) * 100
            }
        }
        
        if self.current_session:
            dashboard_data["current_session"] = asdict(self.current_session)
        
        return dashboard_data

def test_transparent_monitor():
    """transparent_monitor.pyの基本テスト"""
    print("🔍 AI制約透明監視システム v3.1 テスト開始")
    print("=" * 60)
    
    # 監視システム初期化
    monitor = TransparentMonitor()
    
    # 監視セッション開始
    session_id = monitor.start_monitoring_session("test_session")
    print(f"✅ 監視セッション開始: {session_id}")
    
    # テストケース1: 正常チェック
    print("\n📋 テストケース1: 正常チェック")
    normal_context = {
        "requirements_confirmed": True,
        "code_generation_request": True,
        "code_understanding_score": 95,
        "speculation_indicators": [],
        "fact_based_evidence": ["analysis", "docs"],
        "safety_systems_intact": True,
        "backup_procedures_followed": True
    }
    
    results1 = monitor.run_monitored_check(normal_context, "normal_test")
    print(f"結果: {results1['overall_status']}")
    
    # テストケース2: 違反チェック
    print("\n📋 テストケース2: 違反チェック")
    violation_context = {
        "requirements_confirmed": False,
        "code_generation_request": True,
        "code_understanding_score": 20,
        "speculation_indicators": ["guess"],
        "fact_based_evidence": [],
        "safety_systems_intact": False,
        "backup_procedures_followed": False
    }
    
    results2 = monitor.run_monitored_check(violation_context, "violation_test")
    print(f"結果: {results2['overall_status']}")
    
    # ダッシュボード表示
    print("\n📊 監視ダッシュボード:")
    dashboard = monitor.get_monitoring_dashboard()
    print(f"総チェック数: {dashboard['system_info']['lifetime_checks']}")
    print(f"成功率: {dashboard['overall_stats']['lifetime_success_rate']:.1f}%")
    
    # 監視セッション終了
    summary = monitor.stop_monitoring_session()
    print(f"\n✅ 監視セッション終了")
    print(f"実行時間: {summary['duration_seconds']:.2f}秒")
    print(f"チェック総数: {summary['total_checks']}")
    
    print("\n✅ 透明監視システムテスト完了")

if __name__ == "__main__":
    test_transparent_monitor()
