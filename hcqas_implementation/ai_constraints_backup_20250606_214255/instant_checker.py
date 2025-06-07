#!/usr/bin/env python3
"""
HCQAS AI制約チェッカー v3.1 - instant_checker.py
目的: AI生成における4つの禁止事項の即座チェック
作成者: FF管理者 & DD評価AI
評価: 116点/120点満点 (APPROVED_HIGH_CONFIDENCE)
"""

import os
import sys
import json
import logging
import datetime
import traceback
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

class AIConstraintChecker:
    """AI制約違反の即座検出・防止システム"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        AI制約チェッカーの初期化
        
        Args:
            config_path: 設定ファイルのパス（オプション）
        """
        self.version = "3.1"
        self.confidence_score = 116  # DD評価スコア
        self.max_score = 120
        
        # ログ設定
        self.logger = self._setup_logger()
        
        # 設定読み込み
        self.config = self._load_config(config_path)
        
        # 4つの制約定義
        self.constraints = {
            "constraint_1": {
                "name": "事前確認なしコード生成",
                "description": "コード生成前の要件確認必須",
                "severity": "HIGH",
                "enabled": True
            },
            "constraint_2": {
                "name": "元コードの不完全把握",
                "description": "既存コードの完全理解必須",
                "severity": "HIGH", 
                "enabled": True
            },
            "constraint_3": {
                "name": "推測による実装",
                "description": "推測禁止・事実ベース実装必須",
                "severity": "CRITICAL",
                "enabled": True
            },
            "constraint_4": {
                "name": "安全システムの無視",
                "description": "安全機能・バックアップの維持必須",
                "severity": "CRITICAL",
                "enabled": True
            }
        }
        
        # チェック履歴
        self.check_history = []
        self.violation_count = 0
        
        self.logger.info(f"AI制約チェッカー v{self.version} 初期化完了")
        self.logger.info(f"DD評価スコア: {self.confidence_score}/{self.max_score}")
    
    def _setup_logger(self) -> logging.Logger:
        """ログシステムの設定"""
        logger = logging.getLogger('ai_constraint_checker')
        logger.setLevel(logging.INFO)
        
        # ログファイル設定
        log_dir = Path("logs/ai_constraints")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"instant_checker_{timestamp}.log"
        
        # ファイルハンドラー
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """設定ファイルの読み込み"""
        default_config = {
            "check_mode": "strict",
            "auto_block": True,
            "notification_enabled": True,
            "log_level": "INFO",
            "hcqas_integration": True
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                self.logger.info(f"設定ファイル読み込み完了: {config_path}")
            except Exception as e:
                self.logger.warning(f"設定ファイル読み込みエラー: {e}")
        
        return default_config
    
    def check_constraint_1(self, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        制約1: 事前確認なしコード生成のチェック
        
        Args:
            context: チェック対象のコンテキスト情報
            
        Returns:
            Tuple[bool, str]: (違反有無, 詳細メッセージ)
        """
        try:
            # 要件確認フラグのチェック
            requirements_confirmed = context.get("requirements_confirmed", False)
            code_generation_request = context.get("code_generation_request", False)
            
            if code_generation_request and not requirements_confirmed:
                violation_msg = "🚨 制約1違反: 事前確認なしでコード生成が要求されました"
                self.logger.warning(violation_msg)
                return True, violation_msg
            
            success_msg = "✅ 制約1クリア: 適切な事前確認が実施されています"
            self.logger.info(success_msg)
            return False, success_msg
            
        except Exception as e:
            error_msg = f"❌ 制約1チェックエラー: {str(e)}"
            self.logger.error(error_msg)
            return True, error_msg
    
    def check_constraint_2(self, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        制約2: 元コードの不完全把握のチェック
        
        Args:
            context: チェック対象のコンテキスト情報
            
        Returns:
            Tuple[bool, str]: (違反有無, 詳細メッセージ)
        """
        try:
            # 既存コード理解度のチェック
            code_understanding_score = context.get("code_understanding_score", 0)
            minimum_understanding_threshold = 80  # 80%以上の理解が必要
            
            if code_understanding_score < minimum_understanding_threshold:
                violation_msg = f"🚨 制約2違反: コード理解度不足 ({code_understanding_score}% < {minimum_understanding_threshold}%)"
                self.logger.warning(violation_msg)
                return True, violation_msg
            
            success_msg = f"✅ 制約2クリア: 十分なコード理解 ({code_understanding_score}%)"
            self.logger.info(success_msg)
            return False, success_msg
            
        except Exception as e:
            error_msg = f"❌ 制約2チェックエラー: {str(e)}"
            self.logger.error(error_msg)
            return True, error_msg
    
    def check_constraint_3(self, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        制約3: 推測による実装のチェック
        
        Args:
            context: チェック対象のコンテキスト情報
            
        Returns:
            Tuple[bool, str]: (違反有無, 詳細メッセージ)
        """
        try:
            # 推測ベース実装の検出
            speculation_indicators = context.get("speculation_indicators", [])
            fact_based_evidence = context.get("fact_based_evidence", [])
            
            if speculation_indicators and not fact_based_evidence:
                violation_msg = f"🚨 制約3違反: 推測ベース実装検出 - {len(speculation_indicators)}件の推測要素"
                self.logger.warning(violation_msg)
                return True, violation_msg
            
            success_msg = f"✅ 制約3クリア: 事実ベース実装 - {len(fact_based_evidence)}件の根拠"
            self.logger.info(success_msg)
            return False, success_msg
            
        except Exception as e:
            error_msg = f"❌ 制約3チェックエラー: {str(e)}"
            self.logger.error(error_msg)
            return True, error_msg
    
    def check_constraint_4(self, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        制約4: 安全システムの無視のチェック
        
        Args:
            context: チェック対象のコンテキスト情報
            
        Returns:
            Tuple[bool, str]: (違反有無, 詳細メッセージ)
        """
        try:
            # 安全機能の維持確認
            safety_systems_intact = context.get("safety_systems_intact", True)
            backup_procedures_followed = context.get("backup_procedures_followed", True)
            
            if not safety_systems_intact or not backup_procedures_followed:
                violation_msg = "🚨 制約4違反: 安全システムまたはバックアップ手順が無視されています"
                self.logger.warning(violation_msg)
                return True, violation_msg
            
            success_msg = "✅ 制約4クリア: 安全システム・バックアップ手順が適切に維持されています"
            self.logger.info(success_msg)
            return False, success_msg
            
        except Exception as e:
            error_msg = f"❌ 制約4チェックエラー: {str(e)}"
            self.logger.error(error_msg)
            return True, error_msg
    
    def run_comprehensive_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        全制約の包括的チェック実行
        
        Args:
            context: チェック対象のコンテキスト情報
            
        Returns:
            Dict[str, Any]: チェック結果の詳細
        """
        check_timestamp = datetime.datetime.now()
        results = {
            "timestamp": check_timestamp.isoformat(),
            "checker_version": self.version,
            "dd_confidence_score": f"{self.confidence_score}/{self.max_score}",
            "constraints": {},
            "overall_status": "PASS",
            "violation_count": 0,
            "warnings": [],
            "recommendations": []
        }
        
        # 各制約のチェック実行
        constraint_checks = [
            ("constraint_1", self.check_constraint_1),
            ("constraint_2", self.check_constraint_2),
            ("constraint_3", self.check_constraint_3),
            ("constraint_4", self.check_constraint_4)
        ]
        
        for constraint_id, check_func in constraint_checks:
            if self.constraints[constraint_id]["enabled"]:
                try:
                    is_violation, message = check_func(context)
                    results["constraints"][constraint_id] = {
                        "name": self.constraints[constraint_id]["name"],
                        "severity": self.constraints[constraint_id]["severity"],
                        "status": "VIOLATION" if is_violation else "PASS",
                        "message": message
                    }
                    
                    if is_violation:
                        results["violation_count"] += 1
                        results["overall_status"] = "VIOLATION"
                        
                except Exception as e:
                    error_msg = f"制約{constraint_id}チェック中にエラー: {str(e)}"
                    results["warnings"].append(error_msg)
                    self.logger.error(error_msg)
        
        # 履歴に記録
        self.check_history.append(results)
        self.violation_count += results["violation_count"]
        
        # 結果ログ出力
        self._log_check_results(results)
        
        return results
    
    def _log_check_results(self, results: Dict[str, Any]) -> None:
        """チェック結果のログ出力"""
        status_icon = "🚨" if results["overall_status"] == "VIOLATION" else "✅"
        self.logger.info(f"{status_icon} AI制約チェック完了 - ステータス: {results['overall_status']}")
        self.logger.info(f"違反件数: {results['violation_count']}/4")
        
        for constraint_id, constraint_result in results["constraints"].items():
            status_icon = "🚨" if constraint_result["status"] == "VIOLATION" else "✅"
            self.logger.info(f"{status_icon} {constraint_result['name']}: {constraint_result['status']}")

def test_instant_checker():
    """instant_checker.pyの基本テスト"""
    print("🧪 AI制約チェッカー v3.1 テスト開始")
    print("=" * 60)
    
    # チェッカー初期化
    checker = AIConstraintChecker()
    
    # テストケース1: 正常ケース
    print("\n📋 テストケース1: 正常ケース")
    normal_context = {
        "requirements_confirmed": True,
        "code_generation_request": True,
        "code_understanding_score": 95,
        "speculation_indicators": [],
        "fact_based_evidence": ["existing_code_analysis", "requirements_doc"],
        "safety_systems_intact": True,
        "backup_procedures_followed": True
    }
    
    results = checker.run_comprehensive_check(normal_context)
    print(f"結果: {results['overall_status']}")
    print(f"違反件数: {results['violation_count']}/4")
    
    # テストケース2: 違反ケース
    print("\n📋 テストケース2: 違反ケース")
    violation_context = {
        "requirements_confirmed": False,
        "code_generation_request": True,
        "code_understanding_score": 30,
        "speculation_indicators": ["guess_implementation", "assume_behavior"],
        "fact_based_evidence": [],
        "safety_systems_intact": False,
        "backup_procedures_followed": False
    }
    
    results = checker.run_comprehensive_check(violation_context)
    print(f"結果: {results['overall_status']}")
    print(f"違反件数: {results['violation_count']}/4")
    
    print("\n✅ AI制約チェッカーテスト完了")

if __name__ == "__main__":
    test_instant_checker()
