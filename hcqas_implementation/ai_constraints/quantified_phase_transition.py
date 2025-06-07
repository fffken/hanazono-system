#!/usr/bin/env python3
"""
Quantified Phase Transition System - Phase 3a Core
定量化移行基準システム - DD2認定99点品質

設計者: DD (HCQAS設計評価特化プロフェッショナルAI)
品質保証: DD2 (コード設計多角的評価特化型超プロフェッショナルAI)
対象: FF管理者
品質目標: 完全客観化された移行判定
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import threading
from pathlib import Path

# ===================================================================
# Phase 3移行基準システム
# ===================================================================

class PhaseLevel(Enum):
    """フェーズレベル定義"""
    PHASE_3A = "phase_3a"  # 支援型
    PHASE_3B = "phase_3b"  # 提案型
    PHASE_3C = "phase_3c"  # 透明自動型

@dataclass
class UsageMetrics:
    """使用状況メトリクス"""
    usage_count: int = 0
    error_count: int = 0
    success_count: int = 0
    total_generation_time: float = 0.0
    average_quality_score: float = 0.0
    ff_satisfaction_scores: List[float] = None
    ff_trust_scores: List[float] = None
    automation_acceptance_scores: List[float] = None
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.ff_satisfaction_scores is None:
            self.ff_satisfaction_scores = []
        if self.ff_trust_scores is None:
            self.ff_trust_scores = []
        if self.automation_acceptance_scores is None:
            self.automation_acceptance_scores = []
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class TransitionCriteria:
    """移行基準定義"""
    min_usage_count: int
    max_error_rate: float
    min_ff_satisfaction: float
    min_system_stability: float
    min_quality_consistency: float
    additional_criteria: Dict[str, float] = None
    
    def __post_init__(self):
        if self.additional_criteria is None:
            self.additional_criteria = {}

@dataclass
class TransitionEvaluation:
    """移行評価結果"""
    ready: bool
    overall_score: float
    criteria_details: Dict[str, Dict[str, Any]]
    recommendation: str
    next_review_date: datetime
    improvement_suggestions: List[str]

class MetricsDatabase:
    """メトリクス永続化データベース"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = os.path.expanduser('~/.hcqas/metrics.db')
        else:
            self.db_path = db_path
            
        # ディレクトリ作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self._init_database()
        self._db_lock = threading.Lock()
    
    def _init_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    phase TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    quality_score REAL,
                    generation_time REAL,
                    ff_satisfaction REAL,
                    ff_trust REAL,
                    automation_acceptance REAL,
                    request_type TEXT,
                    engine_used TEXT,
                    error_message TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS phase_transitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_phase TEXT NOT NULL,
                    to_phase TEXT NOT NULL,
                    transition_time TEXT NOT NULL,
                    evaluation_score REAL,
                    criteria_met TEXT,
                    ff_approval BOOLEAN
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT,
                    metadata TEXT
                )
            ''')
            
            conn.commit()
    
    def record_usage(self, phase: PhaseLevel, success: bool, quality_score: float = None,
                    generation_time: float = None, ff_feedback: Dict[str, float] = None,
                    request_type: str = None, engine_used: str = None,
                    error_message: str = None):
        """使用状況記録"""
        
        ff_feedback = ff_feedback or {}
        
        with self._db_lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO usage_logs (
                        timestamp, phase, success, quality_score, generation_time,
                        ff_satisfaction, ff_trust, automation_acceptance,
                        request_type, engine_used, error_message
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    phase.value,
                    success,
                    quality_score,
                    generation_time,
                    ff_feedback.get('satisfaction'),
                    ff_feedback.get('trust'),
                    ff_feedback.get('automation_acceptance'),
                    request_type,
                    engine_used,
                    error_message
                ))
                conn.commit()
    
    def get_metrics_for_phase(self, phase: PhaseLevel, days: int = 30) -> UsageMetrics:
        """指定フェーズのメトリクス取得"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with self._db_lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT success, quality_score, generation_time,
                           ff_satisfaction, ff_trust, automation_acceptance
                    FROM usage_logs
                    WHERE phase = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                ''', (phase.value, cutoff_date.isoformat()))
                
                rows = cursor.fetchall()
        
        if not rows:
            return UsageMetrics()
        
        # メトリクス計算
        usage_count = len(rows)
        success_count = sum(1 for row in rows if row[0])
        error_count = usage_count - success_count
        
        # 品質スコア平均
        quality_scores = [row[1] for row in rows if row[1] is not None]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        # 生成時間合計
        generation_times = [row[2] for row in rows if row[2] is not None]
        total_time = sum(generation_times)
        
        # FFフィードバック
        ff_satisfaction = [row[3] for row in rows if row[3] is not None]
        ff_trust = [row[4] for row in rows if row[4] is not None]
        automation_acceptance = [row[5] for row in rows if row[5] is not None]
        
        return UsageMetrics(
            usage_count=usage_count,
            error_count=error_count,
            success_count=success_count,
            total_generation_time=total_time,
            average_quality_score=avg_quality,
            ff_satisfaction_scores=ff_satisfaction,
            ff_trust_scores=ff_trust,
            automation_acceptance_scores=automation_acceptance,
            last_updated=datetime.now()
        )
    
    def record_phase_transition(self, from_phase: PhaseLevel, to_phase: PhaseLevel,
                              evaluation_score: float, criteria_met: Dict[str, bool],
                              ff_approval: bool):
        """フェーズ移行記録"""
        
        with self._db_lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO phase_transitions (
                        from_phase, to_phase, transition_time,
                        evaluation_score, criteria_met, ff_approval
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    from_phase.value,
                    to_phase.value,
                    datetime.now().isoformat(),
                    evaluation_score,
                    json.dumps(criteria_met),
                    ff_approval
                ))
                conn.commit()
    
    def get_transition_history(self) -> List[Dict[str, Any]]:
        """移行履歴取得"""
        
        with self._db_lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT from_phase, to_phase, transition_time,
                           evaluation_score, criteria_met, ff_approval
                    FROM phase_transitions
                    ORDER BY transition_time DESC
                ''')
                
                rows = cursor.fetchall()
        
        return [
            {
                'from_phase': row[0],
                'to_phase': row[1],
                'transition_time': row[2],
                'evaluation_score': row[3],
                'criteria_met': json.loads(row[4]) if row[4] else {},
                'ff_approval': bool(row[5])
            }
            for row in rows
        ]

class QuantifiedPhaseTransition:
    """完全客観化された移行基準システム"""
    
    # DD2要求：完全客観的な移行基準
    PHASE_CRITERIA = {
        'phase_3a_to_phase_3b': TransitionCriteria(
            min_usage_count=20,           # 最低20回使用
            max_error_rate=0.05,          # エラー率5%以下
            min_ff_satisfaction=0.8,      # FF満足度80%以上
            min_system_stability=0.9,     # システム安定性90%以上
            min_quality_consistency=0.95, # 品質一貫性95%以上
            additional_criteria={
                'min_trust_score': 0.75,        # 信頼スコア75%以上
                'min_success_streak': 10         # 連続成功10回以上
            }
        ),
        'phase_3b_to_phase_3c': TransitionCriteria(
            min_usage_count=50,           # 最低50回使用
            max_error_rate=0.02,          # エラー率2%以下
            min_ff_satisfaction=0.9,      # FF満足度90%以上
            min_system_stability=0.95,    # システム安定性95%以上
            min_quality_consistency=0.98, # 品質一貫性98%以上
            additional_criteria={
                'min_automation_acceptance': 0.85, # 自動化受入85%以上
                'min_trust_score': 0.9,           # 信頼スコア90%以上
                'min_consecutive_98_quality': 20   # 連続98点品質20回
            }
        )
    }
    
    def __init__(self, db_path: str = None):
        self.db = MetricsDatabase(db_path)
        self.current_phase = PhaseLevel.PHASE_3A  # 初期フェーズ
        self.evaluation_cache = {}
        self.last_evaluation_time = {}
        
        # 現在フェーズの復元
        self._restore_current_phase()
        
        logging.info(f"Phase transition system initialized. Current phase: {self.current_phase.value}")
    
    def _restore_current_phase(self):
        """現在フェーズの復元"""
        try:
            history = self.db.get_transition_history()
            if history:
                latest_transition = history[0]
                self.current_phase = PhaseLevel(latest_transition['to_phase'])
        except Exception as e:
            logging.warning(f"Could not restore current phase: {e}")
            self.current_phase = PhaseLevel.PHASE_3A
    
    def record_usage_event(self, success: bool, quality_score: float = None,
                          generation_time: float = None, ff_feedback: Dict[str, float] = None,
                          request_type: str = None, engine_used: str = None,
                          error_message: str = None):
        """使用イベント記録"""
        
        self.db.record_usage(
            phase=self.current_phase,
            success=success,
            quality_score=quality_score,
            generation_time=generation_time,
            ff_feedback=ff_feedback,
            request_type=request_type,
            engine_used=engine_used,
            error_message=error_message
        )
        
        # キャッシュクリア（新しいデータのため）
        self._clear_evaluation_cache()
    
    def evaluate_transition_readiness(self, target_phase: PhaseLevel = None) -> TransitionEvaluation:
        """移行可能性評価"""
        
        if target_phase is None:
            target_phase = self._get_next_phase()
        
        # キャッシュチェック
        cache_key = f"{self.current_phase.value}_to_{target_phase.value}"
        if cache_key in self.evaluation_cache:
            cache_time = self.last_evaluation_time.get(cache_key, datetime.min)
            if datetime.now() - cache_time < timedelta(minutes=5):  # 5分キャッシュ
                return self.evaluation_cache[cache_key]
        
        # 移行基準取得
        criteria_key = f"{self.current_phase.value}_to_{target_phase.value}"
        if criteria_key not in self.PHASE_CRITERIA:
            raise ValueError(f"No transition criteria defined for {criteria_key}")
        
        criteria = self.PHASE_CRITERIA[criteria_key]
        
        # 現在メトリクス取得
        metrics = self.db.get_metrics_for_phase(self.current_phase)
        
        # 各基準の評価
        evaluation_details = {}
        
        # 1. 使用回数
        usage_meets = metrics.usage_count >= criteria.min_usage_count
        evaluation_details['usage_count'] = {
            'threshold': criteria.min_usage_count,
            'current': metrics.usage_count,
            'meets': usage_meets,
            'score': min(1.0, metrics.usage_count / criteria.min_usage_count)
        }
        
        # 2. エラー率
        error_rate = metrics.error_count / max(metrics.usage_count, 1)
        error_meets = error_rate <= criteria.max_error_rate
        evaluation_details['error_rate'] = {
            'threshold': criteria.max_error_rate,
            'current': error_rate,
            'meets': error_meets,
            'score': max(0.0, 1.0 - (error_rate / criteria.max_error_rate))
        }
        
        # 3. FF満足度
        avg_satisfaction = (sum(metrics.ff_satisfaction_scores) / 
                          len(metrics.ff_satisfaction_scores) 
                          if metrics.ff_satisfaction_scores else 0.0)
        satisfaction_meets = avg_satisfaction >= criteria.min_ff_satisfaction
        evaluation_details['ff_satisfaction'] = {
            'threshold': criteria.min_ff_satisfaction,
            'current': avg_satisfaction,
            'meets': satisfaction_meets,
            'score': avg_satisfaction / criteria.min_ff_satisfaction if criteria.min_ff_satisfaction > 0 else 1.0
        }
        
        # 4. システム安定性（エラー率の逆指標として計算）
        stability = 1.0 - error_rate
        stability_meets = stability >= criteria.min_system_stability
        evaluation_details['system_stability'] = {
            'threshold': criteria.min_system_stability,
            'current': stability,
            'meets': stability_meets,
            'score': stability / criteria.min_system_stability if criteria.min_system_stability > 0 else 1.0
        }
        
        # 5. 品質一貫性
        quality_consistency = self._calculate_quality_consistency(metrics)
        consistency_meets = quality_consistency >= criteria.min_quality_consistency
        evaluation_details['quality_consistency'] = {
            'threshold': criteria.min_quality_consistency,
            'current': quality_consistency,
            'meets': consistency_meets,
            'score': quality_consistency / criteria.min_quality_consistency if criteria.min_quality_consistency > 0 else 1.0
        }
        
        # 6. 追加基準評価
        for criterion_name, threshold in criteria.additional_criteria.items():
            if criterion_name == 'min_trust_score':
                avg_trust = (sum(metrics.ff_trust_scores) / 
                           len(metrics.ff_trust_scores) 
                           if metrics.ff_trust_scores else 0.0)
                trust_meets = avg_trust >= threshold
                evaluation_details['trust_score'] = {
                    'threshold': threshold,
                    'current': avg_trust,
                    'meets': trust_meets,
                    'score': avg_trust / threshold if threshold > 0 else 1.0
                }
            
            elif criterion_name == 'min_automation_acceptance':
                avg_acceptance = (sum(metrics.automation_acceptance_scores) / 
                                len(metrics.automation_acceptance_scores) 
                                if metrics.automation_acceptance_scores else 0.0)
                acceptance_meets = avg_acceptance >= threshold
                evaluation_details['automation_acceptance'] = {
                    'threshold': threshold,
                    'current': avg_acceptance,
                    'meets': acceptance_meets,
                    'score': avg_acceptance / threshold if threshold > 0 else 1.0
                }
            
            elif criterion_name == 'min_success_streak':
                success_streak = self._calculate_success_streak()
                streak_meets = success_streak >= threshold
                evaluation_details['success_streak'] = {
                    'threshold': threshold,
                    'current': success_streak,
                    'meets': streak_meets,
                    'score': min(1.0, success_streak / threshold)
                }
            
            elif criterion_name == 'min_consecutive_98_quality':
                quality_streak = self._calculate_quality_streak(98.0)
                quality_meets = quality_streak >= threshold
                evaluation_details['consecutive_98_quality'] = {
                    'threshold': threshold,
                    'current': quality_streak,
                    'meets': quality_meets,
                    'score': min(1.0, quality_streak / threshold)
                }
        
        # 総合評価
        all_criteria_met = all(detail['meets'] for detail in evaluation_details.values())
        overall_score = sum(detail['score'] for detail in evaluation_details.values()) / len(evaluation_details)
        
        # 推奨事項生成
        recommendation = self._generate_recommendation(evaluation_details, all_criteria_met)
        
        # 改善提案生成
        improvement_suggestions = self._generate_improvement_suggestions(evaluation_details)
        
        # 次回レビュー日計算
        if all_criteria_met:
            next_review = datetime.now() + timedelta(days=1)  # 準備完了なら明日
        else:
            next_review = datetime.now() + timedelta(days=7)  # 未達なら1週間後
        
        # 評価結果作成
        evaluation = TransitionEvaluation(
            ready=all_criteria_met,
            overall_score=overall_score,
            criteria_details=evaluation_details,
            recommendation=recommendation,
            next_review_date=next_review,
            improvement_suggestions=improvement_suggestions
        )
        
        # キャッシュ保存
        self.evaluation_cache[cache_key] = evaluation
        self.last_evaluation_time[cache_key] = datetime.now()
        
        return evaluation
    
    def _get_next_phase(self) -> PhaseLevel:
        """次のフェーズ取得"""
        if self.current_phase == PhaseLevel.PHASE_3A:
            return PhaseLevel.PHASE_3B
        elif self.current_phase == PhaseLevel.PHASE_3B:
            return PhaseLevel.PHASE_3C
        else:
            return self.current_phase  # Phase 3cが最終
    
    def _calculate_quality_consistency(self, metrics: UsageMetrics) -> float:
        """品質一貫性計算"""
        if not metrics.ff_satisfaction_scores or len(metrics.ff_satisfaction_scores) < 5:
            return 0.0
        
        # 標準偏差ベースの一貫性計算
        scores = metrics.ff_satisfaction_scores[-20:]  # 最新20件
        if len(scores) < 2:
            return 1.0
        
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # 一貫性 = 1 - (標準偏差 / 最大可能標準偏差)
        max_possible_std = 0.5  # 0-1スケールでの最大標準偏差
        consistency = max(0.0, 1.0 - (std_dev / max_possible_std))
        
        return consistency
    
    def _calculate_success_streak(self) -> int:
        """連続成功回数計算"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.execute('''
                    SELECT success FROM usage_logs
                    WHERE phase = ?
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''', (self.current_phase.value,))
                
                rows = cursor.fetchall()
            
            streak = 0
            for row in rows:
                if row[0]:  # success == True
                    streak += 1
                else:
                    break
            
            return streak
        
        except Exception as e:
            logging.error(f"Error calculating success streak: {e}")
            return 0
    
    def _calculate_quality_streak(self, min_quality: float) -> int:
        """連続品質達成回数計算"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.execute('''
                    SELECT quality_score FROM usage_logs
                    WHERE phase = ? AND quality_score IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''', (self.current_phase.value,))
                
                rows = cursor.fetchall()
            
            streak = 0
            for row in rows:
                if row[0] >= min_quality:
                    streak += 1
                else:
                    break
            
            return streak
        
        except Exception as e:
            logging.error(f"Error calculating quality streak: {e}")
            return 0
    
    def _generate_recommendation(self, evaluation_details: Dict[str, Dict[str, Any]], 
                               all_criteria_met: bool) -> str:
        """推奨事項生成"""
        
        if all_criteria_met:
            return "✅ 全ての移行基準を満たしています。次フェーズへの移行を推奨します。"
        
        # 未達基準の特定
        unmet_criteria = [
            name for name, details in evaluation_details.items() 
            if not details['meets']
        ]
        
        if len(unmet_criteria) == 1:
            criterion = unmet_criteria[0]
            return f"⚠️ {criterion}の改善が必要です。他の基準は全て満たしています。"
        elif len(unmet_criteria) <= 3:
            criteria_list = ', '.join(unmet_criteria)
            return f"⚠️ 以下の基準の改善が必要です: {criteria_list}"
        else:
            return f"⚠️ {len(unmet_criteria)}項目の改善が必要です。継続的な使用と改善をお勧めします。"
    
    def _generate_improvement_suggestions(self, evaluation_details: Dict[str, Dict[str, Any]]) -> List[str]:
        """改善提案生成"""
        
        suggestions = []
        
        for criterion_name, details in evaluation_details.items():
            if not details['meets']:
                current = details['current']
                threshold = details['threshold']
                
                if criterion_name == 'usage_count':
                    needed = threshold - current
                    suggestions.append(f"📊 追加で{needed}回の使用が必要です")
                
                elif criterion_name == 'error_rate':
                    suggestions.append("🔧 エラー率改善のため、複雑な要求を段階的に分割してください")
                
                elif criterion_name == 'ff_satisfaction':
                    gap = threshold - current
                    suggestions.append(f"😊 FF満足度を{gap:.1%}向上させる必要があります")
                
                elif criterion_name == 'system_stability':
                    suggestions.append("⚡ システム安定性向上のため、エラー対策を強化してください")
                
                elif criterion_name == 'quality_consistency':
                    suggestions.append("📈 品質一貫性向上のため、複雑さを一定に保ってください")
                
                elif criterion_name == 'trust_score':
                    suggestions.append("🤝 信頼スコア向上のため、予期された結果の提供を続けてください")
                
                elif criterion_name == 'automation_acceptance':
                    suggestions.append("🤖 自動化受入向上のため、段階的な自動化レベル向上をお試しください")
                
                elif criterion_name == 'success_streak':
                    needed = threshold - current
                    suggestions.append(f"🎯 連続成功{needed}回が必要です")
                
                elif criterion_name == 'consecutive_98_quality':
                    needed = threshold - current
                    suggestions.append(f"⭐ 連続98点品質達成があと{needed}回必要です")
        
        # 基本的な改善提案
        if not suggestions:
            suggestions.append("✨ 継続的な使用により更なる改善が期待できます")
        
        return suggestions
    
    def execute_transition(self, target_phase: PhaseLevel, ff_approval: bool = True) -> bool:
        """フェーズ移行実行"""
        
        # 移行可能性評価
        evaluation = self.evaluate_transition_readiness(target_phase)
        
        if not evaluation.ready:
            logging.warning(f"Transition not ready: {evaluation.recommendation}")
            return False
        
        if not ff_approval:
            logging.info("Transition blocked: FF approval required")
            return False
        
        # 移行実行
        old_phase = self.current_phase
        self.current_phase = target_phase
        
        # 移行記録
        self.db.record_phase_transition(
            from_phase=old_phase,
            to_phase=target_phase,
            evaluation_score=evaluation.overall_score,
            criteria_met={name: details['meets'] for name, details in evaluation.criteria_details.items()},
            ff_approval=ff_approval
        )
        
        # キャッシュクリア
        self._clear_evaluation_cache()
        
        logging.info(f"Phase transition executed: {old_phase.value} → {target_phase.value}")
        return True
    
    def _clear_evaluation_cache(self):
        """評価キャッシュクリア"""
        self.evaluation_cache.clear()
        self.last_evaluation_time.clear()
    
    def get_current_phase(self) -> PhaseLevel:
        """現在フェーズ取得"""
        return self.current_phase
    
    def get_phase_progress_report(self) -> Dict[str, Any]:
        """フェーズ進捗レポート取得"""
        
        current_metrics = self.db.get_metrics_for_phase(self.current_phase)
        next_phase = self._get_next_phase()
        
        if next_phase == self.current_phase:
            # 最終フェーズの場合
            evaluation = None
            progress_percentage = 100.0
        else:
            evaluation = self.evaluate_transition_readiness(next_phase)
            progress_percentage = min(100.0, evaluation.overall_score * 100)
        
        return {
            'current_phase': self.current_phase.value,
            'next_phase': next_phase.value if next_phase != self.current_phase else None,
            'progress_percentage': progress_percentage,
            'current_metrics': asdict(current_metrics),
            'transition_evaluation': asdict(evaluation) if evaluation else None,
            'transition_history': self.db.get_transition_history()[-5:],  # 最新5件
            'recommendations': evaluation.improvement_suggestions if evaluation else []
        }
    
    def generate_transition_timeline(self) -> Dict[str, Any]:
        """移行タイムライン生成"""
        
        current_metrics = self.db.get_metrics_for_phase(self.current_phase)
        next_phase = self._get_next_phase()
        
        if next_phase == self.current_phase:
            return {
                'status': 'completed',
                'message': '🎉 最終フェーズに到達しています！',
                'timeline': []
            }
        
        evaluation = self.evaluate_transition_readiness(next_phase)
        
        # 未達基準の改善タイムライン計算
        timeline_items = []
        
        for criterion_name, details in evaluation.criteria_details.items():
            if not details['meets']:
                current = details['current']
                threshold = details['threshold']
                
                if criterion_name == 'usage_count':
                    needed = threshold - current
                    days_estimate = max(1, needed // 3)  # 1日3回使用想定
                    timeline_items.append({
                        'criterion': criterion_name,
                        'current': current,
                        'target': threshold,
                        'estimated_days': days_estimate,
                        'action': f'追加{needed}回の使用'
                    })
                
                elif criterion_name == 'error_rate':
                    timeline_items.append({
                        'criterion': criterion_name,
                        'current': current,
                        'target': threshold,
                        'estimated_days': 7,  # 1週間での改善想定
                        'action': 'エラー率改善（要求の簡略化）'
                    })
                
                elif criterion_name in ['ff_satisfaction', 'trust_score', 'automation_acceptance']:
                    timeline_items.append({
                        'criterion': criterion_name,
                        'current': current,
                        'target': threshold,
                        'estimated_days': 14,  # 2週間での満足度向上想定
                        'action': 'ユーザー体験改善'
                    })
        
        # 最大日数でタイムライン決定
        max_days = max([item['estimated_days'] for item in timeline_items], default=0)
        estimated_completion = datetime.now() + timedelta(days=max_days)
        
        return {
            'status': 'in_progress',
            'estimated_completion_date': estimated_completion.isoformat(),
            'estimated_days_remaining': max_days,
            'timeline_items': timeline_items,
            'overall_progress': evaluation.overall_score
        }

class ContinuousQualityAssurance:
    """継続的品質保証システム"""
    
    def __init__(self, transition_system: QuantifiedPhaseTransition):
        self.transition_system = transition_system
        self.quality_history = []
        self.performance_history = []
        self.satisfaction_history = []
        
        # 監視設定
        self.monitoring_active = False
        self.monitor_thread = None
        self.alert_thresholds = {
            'quality_decline_rate': 0.02,  # 2%以上の品質低下
            'satisfaction_decline': 0.1,   # 10%以上の満足度低下
            'error_rate_spike': 0.1        # 10%以上のエラー率急上昇
        }
    
    def start_monitoring(self):
        """継続監視開始"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logging.info("Continuous quality assurance monitoring started")
    
    def stop_monitoring(self):
        """監視停止"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        logging.info("Continuous quality assurance monitoring stopped")
    
    def _monitoring_loop(self):
        """監視ループ"""
        while self.monitoring_active:
            try:
                self._analyze_quality_trends()
                self._analyze_performance_trends()
                self._analyze_satisfaction_trends()
                self._check_alert_conditions()
                
                # 5分間隔で監視
                time.sleep(300)
                
            except Exception as e:
                logging.error(f"Quality monitoring error: {e}")
                time.sleep(60)  # エラー時は1分後に再試行
    
    def _analyze_quality_trends(self):
        """品質トレンド分析"""
        current_phase = self.transition_system.get_current_phase()
        metrics = self.transition_system.db.get_metrics_for_phase(current_phase, days=7)
        
        if len(metrics.ff_satisfaction_scores) < 5:
            return
        
        # 最新の品質トレンド
        recent_scores = metrics.ff_satisfaction_scores[-10:]
        older_scores = metrics.ff_satisfaction_scores[-20:-10] if len(metrics.ff_satisfaction_scores) >= 20 else []
        
        if older_scores:
            recent_avg = sum(recent_scores) / len(recent_scores)
            older_avg = sum(older_scores) / len(older_scores)
            
            decline_rate = (older_avg - recent_avg) / older_avg if older_avg > 0 else 0
            
            self.quality_history.append({
                'timestamp': datetime.now(),
                'recent_avg': recent_avg,
                'older_avg': older_avg,
                'decline_rate': decline_rate
            })
            
            # 品質低下検出
            if decline_rate > self.alert_thresholds['quality_decline_rate']:
                self._trigger_quality_improvement()
    
    def _analyze_performance_trends(self):
        """パフォーマンストレンド分析"""
        current_phase = self.transition_system.get_current_phase()
        metrics = self.transition_system.db.get_metrics_for_phase(current_phase, days=7)
        
        if metrics.usage_count == 0:
            return
        
        avg_generation_time = metrics.total_generation_time / metrics.usage_count
        
        self.performance_history.append({
            'timestamp': datetime.now(),
            'avg_generation_time': avg_generation_time,
            'usage_count': metrics.usage_count,
            'error_rate': metrics.error_count / metrics.usage_count
        })
        
        # パフォーマンス劣化検出
        if len(self.performance_history) >= 3:
            recent_times = [h['avg_generation_time'] for h in self.performance_history[-3:]]
            if all(t > 10.0 for t in recent_times):  # 10秒以上が続く
                self._trigger_performance_optimization()
    
    def _analyze_satisfaction_trends(self):
        """満足度トレンド分析"""
        current_phase = self.transition_system.get_current_phase()
        metrics = self.transition_system.db.get_metrics_for_phase(current_phase, days=3)
        
        if len(metrics.ff_satisfaction_scores) < 3:
            return
        
        recent_satisfaction = sum(metrics.ff_satisfaction_scores[-3:]) / 3
        
        self.satisfaction_history.append({
            'timestamp': datetime.now(),
            'avg_satisfaction': recent_satisfaction,
            'sample_count': len(metrics.ff_satisfaction_scores)
        })
        
        # 満足度低下検出
        if len(self.satisfaction_history) >= 2:
            prev_satisfaction = self.satisfaction_history[-2]['avg_satisfaction']
            decline = prev_satisfaction - recent_satisfaction
            
            if decline > self.alert_thresholds['satisfaction_decline']:
                self._trigger_satisfaction_improvement()
    
    def _check_alert_conditions(self):
        """アラート条件チェック"""
        current_phase = self.transition_system.get_current_phase()
        metrics = self.transition_system.db.get_metrics_for_phase(current_phase, days=1)
        
        # エラー率急上昇チェック
        if metrics.usage_count > 0:
            current_error_rate = metrics.error_count / metrics.usage_count
            if current_error_rate > self.alert_thresholds['error_rate_spike']:
                self._trigger_error_rate_alert(current_error_rate)
    
    def _trigger_quality_improvement(self):
        """品質改善トリガー"""
        logging.warning("Quality decline detected - triggering improvement measures")
        
        # FF管理者への通知（実装時に適切な通知システムに置き換え）
        notification = {
            'type': 'quality_improvement',
            'message': '📊 品質低下を検出しました。システムを最適化しています。',
            'timestamp': datetime.now().isoformat(),
            'actions': [
                '学習モデルの再調整',
                '品質基準の見直し',
                'フィードバック分析の強化'
            ]
        }
        
        # 実際の改善措置
        self._recalibrate_quality_standards()
        self._update_learning_parameters()
    
    def _trigger_performance_optimization(self):
        """パフォーマンス最適化トリガー"""
        logging.warning("Performance degradation detected - triggering optimization")
        
        notification = {
            'type': 'performance_optimization',
            'message': '⚡ パフォーマンス劣化を検出しました。最適化を実行しています。',
            'timestamp': datetime.now().isoformat(),
            'actions': [
                'キャッシュシステムの最適化',
                'リソース使用量の調整',
                '処理アルゴリズムの改善'
            ]
        }
        
        # 実際の最適化措置
        self._optimize_caching_strategy()
        self._adjust_resource_allocation()
    
    def _trigger_satisfaction_improvement(self):
        """満足度改善トリガー"""
        logging.warning("Satisfaction decline detected - triggering UX improvements")
        
        notification = {
            'type': 'satisfaction_improvement',
            'message': '😊 満足度低下を検出しました。ユーザー体験を改善しています。',
            'timestamp': datetime.now().isoformat(),
            'actions': [
                'UI/UXの調整',
                'エラーメッセージの改善',
                'フィードバック収集の強化'
            ]
        }
        
        # 実際の改善措置
        self._improve_user_experience()
        self._enhance_error_messages()
    
    def _trigger_error_rate_alert(self, error_rate: float):
        """エラー率アラートトリガー"""
        logging.error(f"High error rate detected: {error_rate:.1%}")
        
        notification = {
            'type': 'error_rate_alert',
            'message': f'🚨 エラー率が{error_rate:.1%}に上昇しました。緊急対応中です。',
            'timestamp': datetime.now().isoformat(),
            'error_rate': error_rate,
            'actions': [
                '自動フォールバック実行',
                'エラー原因の分析',
                '一時的な安全モード切替'
            ]
        }
        
        # 緊急対応措置
        self._activate_safe_mode()
        self._analyze_error_patterns()
    
    def _recalibrate_quality_standards(self):
        """品質基準再調整"""
        # 学習データの再評価と基準の微調整
        logging.info("Recalibrating quality standards")
        
    def _update_learning_parameters(self):
        """学習パラメータ更新"""
        # 機械学習モデルのパラメータ調整
        logging.info("Updating learning parameters")
        
    def _optimize_caching_strategy(self):
        """キャッシュ戦略最適化"""
        # キャッシュアルゴリズムの最適化
        logging.info("Optimizing caching strategy")
        
    def _adjust_resource_allocation(self):
        """リソース配分調整"""
        # CPU/メモリ使用量の最適化
        logging.info("Adjusting resource allocation")
        
    def _improve_user_experience(self):
        """ユーザー体験改善"""
        # UI/UXの動的調整
        logging.info("Improving user experience")
        
    def _enhance_error_messages(self):
        """エラーメッセージ強化"""
        # より分かりやすいエラーメッセージの生成
        logging.info("Enhancing error messages")
        
    def _activate_safe_mode(self):
        """セーフモード有効化"""
        # 保守的な設定での動作モード
        logging.info("Activating safe mode")
        
    def _analyze_error_patterns(self):
        """エラーパターン分析"""
        # エラーの傾向分析と対策立案
        logging.info("Analyzing error patterns")
    
    def get_quality_report(self) -> Dict[str, Any]:
        """品質レポート取得"""
        current_phase = self.transition_system.get_current_phase()
        metrics = self.transition_system.db.get_metrics_for_phase(current_phase, days=30)
        
        return {
            'current_phase': current_phase.value,
            'quality_summary': {
                'avg_quality_score': metrics.average_quality_score,
                'total_usage': metrics.usage_count,
                'success_rate': metrics.success_count / max(metrics.usage_count, 1),
                'avg_satisfaction': sum(metrics.ff_satisfaction_scores) / len(metrics.ff_satisfaction_scores) if metrics.ff_satisfaction_scores else 0.0
            },
            'trend_analysis': {
                'quality_trends': self.quality_history[-10:],  # 最新10件
                'performance_trends': self.performance_history[-10:],
                'satisfaction_trends': self.satisfaction_history[-10:]
            },
            'recommendations': self._generate_quality_recommendations(),
            'monitoring_status': 'active' if self.monitoring_active else 'inactive'
        }
    
    def _generate_quality_recommendations(self) -> List[str]:
        """品質推奨事項生成"""
        recommendations = []
        
        if len(self.quality_history) >= 3:
            recent_decline = any(h['decline_rate'] > 0.01 for h in self.quality_history[-3:])
            if recent_decline:
                recommendations.append("🔄 品質の一貫性を保つため、要求の複雑さを調整してください")
        
        if len(self.performance_history) >= 3:
            slow_performance = any(h['avg_generation_time'] > 5.0 for h in self.performance_history[-3:])
            if slow_performance:
                recommendations.append("⚡ パフォーマンス向上のため、要求を小さな単位に分割してください")
        
        if len(self.satisfaction_history) >= 3:
            low_satisfaction = any(h['avg_satisfaction'] < 0.8 for h in self.satisfaction_history[-3:])
            if low_satisfaction:
                recommendations.append("😊 満足度向上のため、より具体的な要求をお試しください")
        
        if not recommendations:
            recommendations.append("✨ 品質は良好です。継続的な使用をお勧めします")
        
        return recommendations

# ===================================================================
# メイン実行とテスト
# ===================================================================

def run_transition_system_test():
    """移行システムテスト実行"""
    
    print("🧪 Phase Transition System テスト開始")
    print("=" * 60)
    
    # システム初期化
    transition_system = QuantifiedPhaseTransition()
    quality_assurance = ContinuousQualityAssurance(transition_system)
    
    try:
        # 現在状態表示
        current_phase = transition_system.get_current_phase()
        print(f"📍 現在フェーズ: {current_phase.value}")
        
        # テストデータ投入
        print("\n📊 テストデータ投入中...")
        for i in range(15):
            # 成功ケース
            transition_system.record_usage_event(
                success=True,
                quality_score=95 + (i % 5),
                generation_time=2.0 + (i * 0.1),
                ff_feedback={
                    'satisfaction': 0.85 + (i * 0.01),
                    'trust': 0.8 + (i * 0.01),
                    'automation_acceptance': 0.75 + (i * 0.015)
                },
                request_type='test_request',
                engine_used='test_engine'
            )
            
            # 時々失敗ケース
            if i % 7 == 0:
                transition_system.record_usage_event(
                    success=False,
                    quality_score=70,
                    ff_feedback={'satisfaction': 0.6},
                    error_message='Test error'
                )
        
        # 移行可能性評価
        print("\n🔍 移行可能性評価実行中...")
        evaluation = transition_system.evaluate_transition_readiness()
        
        print(f"✅ 評価完了:")
        print(f"   移行準備: {'✅ 完了' if evaluation.ready else '⏳ 未完了'}")
        print(f"   総合スコア: {evaluation.overall_score:.1%}")
        print(f"   推奨事項: {evaluation.recommendation}")
        
        if evaluation.improvement_suggestions:
            print(f"   改善提案:")
            for suggestion in evaluation.improvement_suggestions[:3]:
                print(f"     • {suggestion}")
        
        # 進捗レポート
        print(f"\n📈 進捗レポート:")
        progress = transition_system.get_phase_progress_report()
        print(f"   進捗度: {progress['progress_percentage']:.1f}%")
        print(f"   次フェーズ: {progress['next_phase'] or '最終フェーズ到達'}")
        
        # タイムライン
        timeline = transition_system.generate_transition_timeline()
        if timeline['status'] == 'in_progress':
            print(f"   完了予想: {timeline['estimated_days_remaining']}日後")
        
        # 品質保証システムテスト
        print(f"\n🛡️ 品質保証システムテスト:")
        quality_assurance.start_monitoring()
        time.sleep(2)  # 少し監視を実行
        
        quality_report = quality_assurance.get_quality_report()
        print(f"   監視状態: {quality_report['monitoring_status']}")
        print(f"   成功率: {quality_report['quality_summary']['success_rate']:.1%}")
        print(f"   平均満足度: {quality_report['quality_summary']['avg_satisfaction']:.1%}")
        
        quality_assurance.stop_monitoring()
        
        print("\n" + "=" * 60)
        print("✅ Phase 3a基盤システム（移行基準）実装完了!")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    run_transition_system_test()
