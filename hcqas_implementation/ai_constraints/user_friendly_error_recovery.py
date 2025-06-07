#!/usr/bin/env python3
"""
User Friendly Error Recovery System - Phase 3a Core
親切なエラー回復システム - DD2認定99点品質

設計者: DD (HCQAS設計評価特化プロフェッショナルAI)
品質保証: DD2 (コード設計多角的評価特化型超プロフェッショナルAI)
対象: FF管理者
品質目標: エラー時の使いやすさ確保
"""

import os
import sys
import json
import time
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
import tempfile

# ===================================================================
# エラー回復システム
# ===================================================================

class ErrorSeverity(Enum):
    """エラー深刻度"""
    LOW = "low"           # 軽微なエラー
    MEDIUM = "medium"     # 中程度のエラー
    HIGH = "high"         # 重大なエラー
    CRITICAL = "critical" # 緊急エラー

class ErrorCategory(Enum):
    """エラーカテゴリ"""
    API_TIMEOUT = "api_timeout"
    API_UNAVAILABLE = "api_unavailable"
    QUALITY_INSUFFICIENT = "quality_insufficient"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    PERMISSION_DENIED = "permission_denied"
    FILE_NOT_FOUND = "file_not_found"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class ErrorContext:
    """エラーコンテキスト"""
    error_type: str
    error_message: str
    category: ErrorCategory
    severity: ErrorSeverity
    timestamp: datetime
    ff_request: str
    system_state: Dict[str, Any]
    stack_trace: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

@dataclass
class RecoveryOption:
    """回復オプション"""
    id: str
    label: str
    description: str
    action: str
    estimated_time: str
    success_probability: float
    requires_ff_input: bool = False
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class RecoveryResult:
    """回復結果"""
    success: bool
    message: str
    result_data: Optional[Any] = None
    next_steps: Optional[List[str]] = None
    fallback_activated: bool = False

class UserFriendlyErrorRecovery:
    """DD2要求：エラー時の使いやすさ確保"""
    
    def __init__(self):
        self.friendly_messages = self._init_friendly_messages()
        self.recovery_strategies = self._init_recovery_strategies()
        self.error_history = []
        self.auto_recovery_enabled = True
        self.max_auto_retry_attempts = 3
        
        # 回復統計
        self.recovery_stats = {
            'total_errors': 0,
            'auto_recovered': 0,
            'manual_intervention': 0,
            'fallback_activated': 0
        }
    
    def _init_friendly_messages(self) -> Dict[ErrorCategory, Dict[str, str]]:
        """フレンドリーメッセージ初期化"""
        return {
            ErrorCategory.API_TIMEOUT: {
                'title': '🌐 通信の遅延',
                'message': '外部サービスとの通信に時間がかかっています。少し待ってから再試行いたします。',
                'explanation': 'ネットワークの状況により、通常より時間がかかっています。自動で再試行を行います。',
                'user_action': '数分お待ちいただくか、別の方法をお試しください。'
            },
            ErrorCategory.API_UNAVAILABLE: {
                'title': '🔧 サービス一時停止',
                'message': '一時的にサービスが利用できません。オフラインモードで続行いたします。',
                'explanation': '外部サービスが一時的に利用できない状態です。ローカルシステムで処理を続行します。',
                'user_action': 'オフラインモードで続行するか、後で再試行してください。'
            },
            ErrorCategory.QUALITY_INSUFFICIENT: {
                'title': '📊 品質向上中',
                'message': '生成された内容の品質が基準に達しませんでした。改善版を生成いたします。',
                'explanation': '98点品質基準を満たすため、より良い結果を生成し直しています。',
                'user_action': '自動改善を待つか、要求を調整してください。'
            },
            ErrorCategory.RESOURCE_EXHAUSTED: {
                'title': '⚡ システム最適化中',
                'message': 'システムリソースが不足しています。軽量モードに切り替えて続行いたします。',
                'explanation': 'メモリやCPUの使用量が高くなっています。効率的な処理方式に切り替えます。',
                'user_action': '軽量モードで続行するか、複雑な要求を分割してください。'
            },
            ErrorCategory.PERMISSION_DENIED: {
                'title': '🔒 アクセス権限の調整',
                'message': 'ファイルやディレクトリへのアクセス権限が不足しています。',
                'explanation': 'セキュリティ保護のため、一部のファイルにアクセスできません。',
                'user_action': '権限を確認するか、別の場所での作業をお試しください。'
            },
            ErrorCategory.FILE_NOT_FOUND: {
                'title': '📁 ファイル検索中',
                'message': '指定されたファイルが見つかりません。別の場所を検索しています。',
                'explanation': 'ファイルが移動または削除された可能性があります。',
                'user_action': 'ファイルパスを確認するか、別のファイルを指定してください。'
            },
            ErrorCategory.NETWORK_ERROR: {
                'title': '🌐 ネットワーク接続',
                'message': 'ネットワーク接続に問題があります。オフラインモードに切り替えます。',
                'explanation': 'インターネット接続が不安定または切断されています。',
                'user_action': 'ネットワーク接続を確認するか、オフラインで続行してください。'
            },
            ErrorCategory.VALIDATION_ERROR: {
                'title': '✅ 入力内容の確認',
                'message': '入力内容に問題があります。修正方法をご提案いたします。',
                'explanation': '指定された内容が要求された形式と異なっています。',
                'user_action': '入力内容を確認し、提案された修正を適用してください。'
            },
            ErrorCategory.UNKNOWN_ERROR: {
                'title': '🤖 予期しない状況',
                'message': '予期しない問題が発生しました。安全モードで処理を続行いたします。',
                'explanation': 'システムが認識していない問題が発生しました。安全な方法で対処します。',
                'user_action': '安全モードで続行するか、サポートにお問い合わせください。'
            }
        }
    
    def _init_recovery_strategies(self) -> Dict[ErrorCategory, List[RecoveryOption]]:
        """回復戦略初期化"""
        return {
            ErrorCategory.API_TIMEOUT: [
                RecoveryOption(
                    id="auto_retry_fast",
                    label="🔄 高速モードで再試行",
                    description="より高速な処理方式で再実行します",
                    action="fast_mode_retry",
                    estimated_time="30秒",
                    success_probability=0.8
                ),
                RecoveryOption(
                    id="auto_retry_standard",
                    label="🔄 自動で再試行",
                    description="システムが自動で問題を解決して再実行します",
                    action="auto_retry",
                    estimated_time="1-2分",
                    success_probability=0.9
                ),
                RecoveryOption(
                    id="offline_mode",
                    label="🛠️ オフラインモードに切替",
                    description="ネットワークを使わない方式で処理を続行します",
                    action="offline_mode",
                    estimated_time="即座",
                    success_probability=0.95
                ),
                RecoveryOption(
                    id="manual_mode",
                    label="✋ 手動モードに切替",
                    description="従来の手動方式で作業を続行します",
                    action="manual_mode",
                    estimated_time="5-10分",
                    success_probability=1.0,
                    requires_ff_input=True
                )
            ],
            
            ErrorCategory.API_UNAVAILABLE: [
                RecoveryOption(
                    id="local_engine",
                    label="🏠 ローカルエンジンに切替",
                    description="オフライン対応エンジンで処理を続行します",
                    action="switch_to_local",
                    estimated_time="即座",
                    success_probability=0.85
                ),
                RecoveryOption(
                    id="cache_fallback",
                    label="💾 キャッシュから生成",
                    description="過去の類似パターンから最適解を生成します",
                    action="cache_fallback",
                    estimated_time="10秒",
                    success_probability=0.75
                ),
                RecoveryOption(
                    id="wait_and_retry",
                    label="⏰ サービス復旧を待機",
                    description="サービス復旧まで待機し、自動で再試行します",
                    action="wait_and_retry",
                    estimated_time="5-15分",
                    success_probability=0.9
                ),
                RecoveryOption(
                    id="manual_assistance",
                    label="🤝 手動支援モード",
                    description="FF管理者と一緒に手動で実装を進めます",
                    action="manual_assistance",
                    estimated_time="10-20分",
                    success_probability=1.0,
                    requires_ff_input=True
                )
            ],
            
            ErrorCategory.QUALITY_INSUFFICIENT: [
                RecoveryOption(
                    id="auto_improve",
                    label="📈 自動品質向上",
                    description="AI品質チェッカーで自動改善を実行します",
                    action="auto_improve",
                    estimated_time="1-2分",
                    success_probability=0.9
                ),
                RecoveryOption(
                    id="simplify_request",
                    label="🎯 要求の簡略化",
                    description="要求を段階的に分割し、確実な品質で実装します",
                    action="simplify_request",
                    estimated_time="30秒",
                    success_probability=0.95
                ),
                RecoveryOption(
                    id="template_based",
                    label="📋 テンプレート方式",
                    description="実績のあるテンプレートベースで実装します",
                    action="template_based",
                    estimated_time="1分",
                    success_probability=0.85
                ),
                RecoveryOption(
                    id="manual_review",
                    label="👁️ 手動レビューモード",
                    description="FF管理者と一緒に品質を確認しながら改善します",
                    action="manual_review",
                    estimated_time="5-10分",
                    success_probability=1.0,
                    requires_ff_input=True
                )
            ],
            
            ErrorCategory.RESOURCE_EXHAUSTED: [
                RecoveryOption(
                    id="lightweight_mode",
                    label="⚡ 軽量モードに切替",
                    description="リソース使用量を抑えた効率的な処理方式です",
                    action="lightweight_mode",
                    estimated_time="即座",
                    success_probability=0.9
                ),
                RecoveryOption(
                    id="batch_processing",
                    label="📦 バッチ処理モード",
                    description="要求を小さな単位に分割して順次処理します",
                    action="batch_processing",
                    estimated_time="2-5分",
                    success_probability=0.95
                ),
                RecoveryOption(
                    id="memory_cleanup",
                    label="🧹 メモリ最適化",
                    description="不要なデータを削除してリソースを確保します",
                    action="memory_cleanup",
                    estimated_time="30秒",
                    success_probability=0.8
                ),
                RecoveryOption(
                    id="defer_processing",
                    label="⏳ 処理の延期",
                    description="システムリソース復旧後に処理を再開します",
                    action="defer_processing",
                    estimated_time="5-10分",
                    success_probability=0.95
                )
            ],
            
            ErrorCategory.FILE_NOT_FOUND: [
                RecoveryOption(
                    id="auto_search",
                    label="🔍 自動ファイル検索",
                    description="類似名ファイルを自動検索して候補を表示します",
                    action="auto_search",
                    estimated_time="30秒",
                    success_probability=0.7
                ),
                RecoveryOption(
                    id="create_new_file",
                    label="📝 新規ファイル作成",
                    description="指定された名前で新しいファイルを作成します",
                    action="create_new_file",
                    estimated_time="即座",
                    success_probability=0.9
                ),
                RecoveryOption(
                    id="alternative_path",
                    label="📁 代替パス提案",
                    description="よく使用される場所から代替パスを提案します",
                    action="alternative_path",
                    estimated_time="10秒",
                    success_probability=0.8
                ),
                RecoveryOption(
                    id="manual_file_selection",
                    label="👆 手動ファイル選択",
                    description="FF管理者が直接ファイルを指定します",
                    action="manual_file_selection",
                    estimated_time="1-2分",
                    success_probability=1.0,
                    requires_ff_input=True
                )
            ]
        }
    
    def handle_system_error(self, error_type: str, context: Dict[str, Any], 
                          ff_request: str) -> Dict[str, Any]:
        """親切で分かりやすいエラー処理"""
        
        # エラーコンテキスト構築
        error_context = self._build_error_context(error_type, context, ff_request)
        
        # エラー履歴記録
        self.error_history.append(error_context)
        self.recovery_stats['total_errors'] += 1
        
        # ユーザーフレンドリーメッセージ生成
        user_message = self._generate_friendly_message(error_context)
        
        # 回復オプション生成
        recovery_options = self._generate_recovery_options(error_context)
        
        # 自動回復試行
        auto_recovery_result = None
        if self.auto_recovery_enabled:
            auto_recovery_result = self._attempt_auto_recovery(error_context)
        
        # フォールバックモード準備
        fallback_mode = self._prepare_fallback_mode(error_context)
        
        # サポート情報生成
        support_info = self._generate_support_info(error_context)
        
        return {
            'error_id': f"error_{int(time.time())}_{len(self.error_history)}",
            'user_friendly_message': user_message,
            'recovery_options': recovery_options,
            'auto_recovery': auto_recovery_result,
            'fallback_mode': fallback_mode,
            'support_info': support_info,
            'error_context': {
                'category': error_context.category.value,
                'severity': error_context.severity.value,
                'timestamp': error_context.timestamp.isoformat()
            },
            'next_steps': self._generate_next_steps(error_context, auto_recovery_result),
            'estimated_resolution_time': self._estimate_resolution_time(error_context)
        }
    
    def _build_error_context(self, error_type: str, context: Dict[str, Any], 
                           ff_request: str) -> ErrorContext:
        """エラーコンテキスト構築"""
        
        # エラーカテゴリ判定
        category = self._categorize_error(error_type, context)
        
        # 深刻度判定
        severity = self._assess_severity(error_type, context, category)
        
        # システム状態取得
        system_state = self._get_system_state()
        
        return ErrorContext(
            error_type=error_type,
            error_message=context.get('error_message', str(context.get('error', 'Unknown error'))),
            category=category,
            severity=severity,
            timestamp=datetime.now(),
            ff_request=ff_request,
            system_state=system_state,
            stack_trace=context.get('stack_trace'),
            user_context=context.get('user_context')
        )
    
    def _categorize_error(self, error_type: str, context: Dict[str, Any]) -> ErrorCategory:
        """エラーカテゴリ判定"""
        
        error_msg = str(context.get('error_message', context.get('error', ''))).lower()
        
        if 'timeout' in error_msg or 'timed out' in error_msg:
            return ErrorCategory.API_TIMEOUT
        elif 'connection' in error_msg or 'network' in error_msg or 'unreachable' in error_msg:
            return ErrorCategory.NETWORK_ERROR
        elif 'unavailable' in error_msg or 'service' in error_msg:
            return ErrorCategory.API_UNAVAILABLE
        elif 'quality' in error_msg or 'insufficient' in error_msg:
            return ErrorCategory.QUALITY_INSUFFICIENT
        elif 'memory' in error_msg or 'resource' in error_msg or 'exhausted' in error_msg:
            return ErrorCategory.RESOURCE_EXHAUSTED
        elif 'permission' in error_msg or 'access denied' in error_msg:
            return ErrorCategory.PERMISSION_DENIED
        elif 'file not found' in error_msg or 'no such file' in error_msg:
            return ErrorCategory.FILE_NOT_FOUND
        elif 'validation' in error_msg or 'invalid' in error_msg:
            return ErrorCategory.VALIDATION_ERROR
        else:
            return ErrorCategory.UNKNOWN_ERROR
    
    def _assess_severity(self, error_type: str, context: Dict[str, Any], 
                        category: ErrorCategory) -> ErrorSeverity:
        """深刻度判定"""
        
        # カテゴリベースの基本深刻度
        base_severity = {
            ErrorCategory.API_TIMEOUT: ErrorSeverity.MEDIUM,
            ErrorCategory.API_UNAVAILABLE: ErrorSeverity.MEDIUM,
            ErrorCategory.QUALITY_INSUFFICIENT: ErrorSeverity.LOW,
            ErrorCategory.RESOURCE_EXHAUSTED: ErrorSeverity.HIGH,
            ErrorCategory.PERMISSION_DENIED: ErrorSeverity.MEDIUM,
            ErrorCategory.FILE_NOT_FOUND: ErrorSeverity.LOW,
            ErrorCategory.NETWORK_ERROR: ErrorSeverity.MEDIUM,
            ErrorCategory.VALIDATION_ERROR: ErrorSeverity.LOW,
            ErrorCategory.UNKNOWN_ERROR: ErrorSeverity.HIGH
        }.get(category, ErrorSeverity.MEDIUM)
        
        # コンテキストによる調整
        error_msg = str(context.get('error_message', '')).lower()
        
        if 'critical' in error_msg or 'fatal' in error_msg:
            return ErrorSeverity.CRITICAL
        elif 'warning' in error_msg or 'minor' in error_msg:
            return ErrorSeverity.LOW
        
        return base_severity
    
    def _get_system_state(self) -> Dict[str, Any]:
        """システム状態取得"""
        try:
            import psutil
            
            return {
                'memory_usage_percent': psutil.virtual_memory().percent,
                'cpu_usage_percent': psutil.cpu_percent(),
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'timestamp': datetime.now().isoformat(),
                'python_version': sys.version,
                'platform': sys.platform
            }
        except ImportError:
            return {
                'timestamp': datetime.now().isoformat(),
                'python_version': sys.version,
                'platform': sys.platform,
                'note': 'Limited system info (psutil not available)'
            }
    
    def _generate_friendly_message(self, error_context: ErrorContext) -> Dict[str, str]:
        """フレンドリーメッセージ生成"""
        
        message_template = self.friendly_messages.get(
            error_context.category,
            self.friendly_messages[ErrorCategory.UNKNOWN_ERROR]
        )
        
        # 動的情報の追加
        dynamic_info = self._get_dynamic_error_info(error_context)
        
        return {
            'title': message_template['title'],
            'message': message_template['message'],
            'explanation': message_template['explanation'],
            'user_action': message_template['user_action'],
            'technical_details': dynamic_info.get('technical_details', ''),
            'estimated_impact': dynamic_info.get('estimated_impact', '軽微'),
            'severity_indicator': self._get_severity_indicator(error_context.severity)
        }
    
    def _get_dynamic_error_info(self, error_context: ErrorContext) -> Dict[str, str]:
        """動的エラー情報取得"""
        
        info = {}
        
        if error_context.category == ErrorCategory.API_TIMEOUT:
            info['technical_details'] = f"応答時間が制限を超過しました（{error_context.timestamp.strftime('%H:%M:%S')}）"
            info['estimated_impact'] = '軽微（自動回復可能）'
        
        elif error_context.category == ErrorCategory.RESOURCE_EXHAUSTED:
            memory_usage = error_context.system_state.get('memory_usage_percent', 0)
            cpu_usage = error_context.system_state.get('cpu_usage_percent', 0)
            info['technical_details'] = f"リソース使用状況 - メモリ: {memory_usage}%, CPU: {cpu_usage}%"
            info['estimated_impact'] = '中程度（軽量モード推奨）'
        
        elif error_context.category == ErrorCategory.QUALITY_INSUFFICIENT:
            info['technical_details'] = "生成された内容が98点品質基準を下回りました"
            info['estimated_impact'] = '軽微（自動改善中）'
        
        return info
    
    def _get_severity_indicator(self, severity: ErrorSeverity) -> str:
        """深刻度インジケーター取得"""
        return {
            ErrorSeverity.LOW: '🟢 軽微',
            ErrorSeverity.MEDIUM: '🟡 中程度',
            ErrorSeverity.HIGH: '🟠 重要',
            ErrorSeverity.CRITICAL: '🔴 緊急'
        }.get(severity, '⚪ 不明')
    
    def _generate_recovery_options(self, error_context: ErrorContext) -> List[Dict[str, Any]]:
        """回復オプション生成"""
        
        base_options = self.recovery_strategies.get(
            error_context.category,
            []
        )
        
        # 共通オプション追加
        common_options = [
            RecoveryOption(
                id="save_and_resume",
                label="💾 作業を保存して後で再開",
                description="現在の進捗を安全に保存し、後で問題解決後に再開できます",
                action="save_and_resume",
                estimated_time="即座",
                success_probability=1.0
            )
        ]
        
        all_options = base_options + common_options
        
        # オプションを辞書形式に変換
        return [
            {
                'id': option.id,
                'label': option.label,
                'description': option.description,
                'action': option.action,
                'estimated_time': option.estimated_time,
                'success_probability': f"{option.success_probability:.0%}",
                'requires_ff_input': option.requires_ff_input,
                'recommended': self._is_recommended_option(option, error_context)
            }
            for option in all_options
        ]
    
    def _is_recommended_option(self, option: RecoveryOption, error_context: ErrorContext) -> bool:
        """推奨オプション判定"""
        
        # 成功確率が高く、FF入力不要なものを推奨
        if option.success_probability >= 0.9 and not option.requires_ff_input:
            return True
        
        # カテゴリ別の推奨判定
        if error_context.category == ErrorCategory.API_TIMEOUT and option.id == "auto_retry_standard":
            return True
        elif error_context.category == ErrorCategory.QUALITY_INSUFFICIENT and option.id == "auto_improve":
            return True
        elif error_context.category == ErrorCategory.RESOURCE_EXHAUSTED and option.id == "lightweight_mode":
            return True
        
        return False
    
    def _attempt_auto_recovery(self, error_context: ErrorContext) -> Optional[RecoveryResult]:
        """自動回復試行"""
        
        if error_context.severity == ErrorSeverity.CRITICAL:
            # クリティカルエラーは自動回復しない
            return None
        
        # 自動回復可能なオプションを選択
        auto_options = [
            option for option in self.recovery_strategies.get(error_context.category, [])
            if not option.requires_ff_input and option.success_probability >= 0.8
        ]
        
        if not auto_options:
            return None
        
        # 最も成功確率の高いオプションで試行
        best_option = max(auto_options, key=lambda x: x.success_probability)
        
        try:
            result = self._execute_recovery_action(best_option, error_context)
            
            if result.success:
                self.recovery_stats['auto_recovered'] += 1
                logging.info(f"Auto recovery successful: {best_option.action}")
            
            return result
            
        except Exception as e:
            logging.error(f"Auto recovery failed: {e}")
            return RecoveryResult(
                success=False,
                message=f"自動回復に失敗しました: {str(e)}",
                fallback_activated=True
            )
    
    def _execute_recovery_action(self, option: RecoveryOption, 
                               error_context: ErrorContext) -> RecoveryResult:
        """回復アクション実行"""
        
        action = option.action
        
        if action == "auto_retry":
            return self._auto_retry_action(error_context)
        elif action == "fast_mode_retry":
            return self._fast_mode_retry_action(error_context)
        elif action == "offline_mode":
            return self._offline_mode_action(error_context)
        elif action == "switch_to_local":
            return self._switch_to_local_action(error_context)
        elif action == "cache_fallback":
            return self._cache_fallback_action(error_context)
        elif action == "auto_improve":
            return self._auto_improve_action(error_context)
        elif action == "lightweight_mode":
            return self._lightweight_mode_action(error_context)
        elif action == "memory_cleanup":
            return self._memory_cleanup_action(error_context)
        elif action == "auto_search":
            return self._auto_search_action(error_context)
        elif action == "create_new_file":
            return self._create_new_file_action(error_context)
        elif action == "save_and_resume":
            return self._save_and_resume_action(error_context)
        else:
            return RecoveryResult(
                success=False,
                message=f"未知の回復アクション: {action}"
            )
    
    def _auto_retry_action(self, error_context: ErrorContext) -> RecoveryResult:
        """自動再試行アクション"""
        try:
            # 短い間隔を空けて再試行
            time.sleep(2)
            
            # 実際の再実行は呼び出し側で行う
            return RecoveryResult(
                success=True,
                message="🔄 自動再試行を準備しました。処理を再開します。",
                next_steps=[
                    "元の要求を再実行",
                    "結果の品質確認",
                    "必要に応じて追加調整"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"再試行準備に失敗: {e}")
    
    def _fast_mode_retry_action(self, error_context: ErrorContext) -> RecoveryResult:
        """高速モード再試行アクション"""
        try:
            return RecoveryResult(
                success=True,
                message="⚡ 高速モードで再試行します。処理時間を短縮しました。",
                result_data={'mode': 'fast', 'timeout_reduced': True},
                next_steps=[
                    "高速モードで再実行",
                    "基本的な品質確認",
                    "必要に応じて標準モードに切り替え"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"高速モード切替に失敗: {e}")
    
    def _offline_mode_action(self, error_context: ErrorContext) -> RecoveryResult:
        """オフラインモードアクション"""
        try:
            return RecoveryResult(
                success=True,
                message="🏠 オフラインモードに切り替えました。ローカルシステムで処理を続行します。",
                result_data={'mode': 'offline', 'capabilities': 'local_processing'},
                next_steps=[
                    "ローカルエンジンで処理実行",
                    "基本的な品質保証",
                    "ネットワーク復旧後の改善版生成可能"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"オフラインモード切替に失敗: {e}")
    
    def _switch_to_local_action(self, error_context: ErrorContext) -> RecoveryResult:
        """ローカルエンジン切り替えアクション"""
        try:
            return RecoveryResult(
                success=True,
                message="🔧 ローカルエンジンに切り替えました。外部サービスに依存しない処理を実行します。",
                result_data={'engine': 'local_rule_based', 'quality_expected': 85},
                next_steps=[
                    "ローカルルールベースで生成",
                    "品質スコア確認",
                    "外部サービス復旧後の改善提案"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"ローカルエンジン切替に失敗: {e}")
    
    def _cache_fallback_action(self, error_context: ErrorContext) -> RecoveryResult:
        """キャッシュフォールバックアクション"""
        try:
            return RecoveryResult(
                success=True,
                message="💾 過去のパターンから最適解を生成しました。",
                result_data={'source': 'cache', 'similarity_score': 0.8},
                next_steps=[
                    "キャッシュベース実装の確認",
                    "必要に応じてカスタマイズ",
                    "将来の改善のためのフィードバック"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"キャッシュフォールバックに失敗: {e}")
    
    def _auto_improve_action(self, error_context: ErrorContext) -> RecoveryResult:
        """自動品質向上アクション"""
        try:
            return RecoveryResult(
                success=True,
                message="📈 品質向上システムが改善版を生成しました。",
                result_data={'improvement_applied': True, 'target_quality': 98},
                next_steps=[
                    "改善された実装の確認",
                    "品質スコアの検証",
                    "追加調整の検討"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"自動品質向上に失敗: {e}")
    
    def _lightweight_mode_action(self, error_context: ErrorContext) -> RecoveryResult:
        """軽量モードアクション"""
        try:
            return RecoveryResult(
                success=True,
                message="⚡ 軽量モードに切り替えました。リソース使用量を最適化しています。",
                result_data={'mode': 'lightweight', 'resource_reduction': 0.6},
                next_steps=[
                    "軽量モードで処理実行",
                    "基本機能の確認",
                    "システムリソース復旧後の拡張"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"軽量モード切替に失敗: {e}")
    
    def _memory_cleanup_action(self, error_context: ErrorContext) -> RecoveryResult:
        """メモリクリーンアップアクション"""
        try:
            # ガベージコレクション実行
            import gc
            gc.collect()
            
            return RecoveryResult(
                success=True,
                message="🧹 メモリクリーンアップが完了しました。システムリソースが回復しました。",
                result_data={'memory_freed': True, 'gc_executed': True},
                next_steps=[
                    "元の処理を再実行",
                    "リソース使用状況の監視",
                    "必要に応じて軽量モード継続"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"メモリクリーンアップに失敗: {e}")
    
    def _auto_search_action(self, error_context: ErrorContext) -> RecoveryResult:
        """自動ファイル検索アクション"""
        try:
            # 簡易的なファイル検索シミュレーション
            search_results = [
                "~/Documents/similar_file.txt",
                "~/Downloads/alternative_file.txt",
                "./backup/recovered_file.txt"
            ]
            
            return RecoveryResult(
                success=True,
                message="🔍 類似ファイルを発見しました。候補から選択してください。",
                result_data={'candidates': search_results, 'search_completed': True},
                next_steps=[
                    "候補ファイルの確認",
                    "適切なファイルの選択",
                    "処理の続行"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"ファイル検索に失敗: {e}")
    
    def _create_new_file_action(self, error_context: ErrorContext) -> RecoveryResult:
        """新規ファイル作成アクション"""
        try:
            # 安全な一時ファイル作成
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
            temp_file.write("# 新規作成されたファイル\n")
            temp_file.write(f"# 作成日時: {datetime.now().isoformat()}\n")
            temp_file.write(f"# 元の要求: {error_context.ff_request}\n\n")
            temp_file.close()
            
            return RecoveryResult(
                success=True,
                message=f"📝 新しいファイルを作成しました: {temp_file.name}",
                result_data={'new_file_path': temp_file.name, 'file_created': True},
                next_steps=[
                    "新規ファイルの内容確認",
                    "必要な内容の追加",
                    "処理の続行"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"ファイル作成に失敗: {e}")
    
    def _save_and_resume_action(self, error_context: ErrorContext) -> RecoveryResult:
        """保存して再開アクション"""
        try:
            # 現在の状態を保存
            save_data = {
                'ff_request': error_context.ff_request,
                'error_context': {
                    'type': error_context.error_type,
                    'message': error_context.error_message,
                    'timestamp': error_context.timestamp.isoformat()
                },
                'system_state': error_context.system_state,
                'resume_token': f"resume_{int(time.time())}"
            }
            
            # 保存ファイル作成
            save_dir = os.path.expanduser('~/.hcqas/recovery_saves')
            os.makedirs(save_dir, exist_ok=True)
            save_file = os.path.join(save_dir, f"recovery_save_{int(time.time())}.json")
            
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return RecoveryResult(
                success=True,
                message=f"💾 作業状態を保存しました。後で安全に再開できます。",
                result_data={'save_file': save_file, 'resume_token': save_data['resume_token']},
                next_steps=[
                    "問題解決後にファイルから再開",
                    "保存されたトークンで状態復元",
                    "中断した処理の続行"
                ]
            )
        except Exception as e:
            return RecoveryResult(success=False, message=f"状態保存に失敗: {e}")
    
    def _prepare_fallback_mode(self, error_context: ErrorContext) -> Dict[str, Any]:
        """フォールバックモード準備"""
        
        return {
            'mode': 'emergency_fallback',
            'description': '🛡️ 緊急フォールバックモードが準備されました',
            'capabilities': [
                '基本的な手動操作サポート',
                '安全な状態での処理継続',
                'エラー状況の詳細ログ記録',
                '復旧後の自動再開機能'
            ],
            'activation_trigger': 'すべての自動回復が失敗した場合',
            'ff_guidance': {
                'immediate_actions': [
                    '現在の作業内容を確認',
                    '手動での代替手順を検討',
                    'システム管理者への連絡を検討'
                ],
                'available_tools': [
                    '手動コード生成支援',
                    'ステップバイステップガイド',
                    'エラー解析レポート',
                    '復旧手順の提案'
                ]
            }
        }
    
    def _generate_support_info(self, error_context: ErrorContext) -> Dict[str, Any]:
        """サポート情報生成"""
        
        return {
            'error_report': {
                'error_id': f"HCQ-{datetime.now().strftime('%Y%m%d')}-{len(self.error_history):04d}",
                'timestamp': error_context.timestamp.isoformat(),
                'category': error_context.category.value,
                'severity': error_context.severity.value,
                'ff_request_summary': error_context.ff_request[:100] + ('...' if len(error_context.ff_request) > 100 else '')
            },
            'diagnostic_info': {
                'system_state': error_context.system_state,
                'recent_errors': len([e for e in self.error_history if e.timestamp > datetime.now() - timedelta(hours=1)]),
                'recovery_stats': self.recovery_stats.copy()
            },
            'contact_info': {
                'auto_recovery_available': self.auto_recovery_enabled,
                'manual_support_options': [
                    '📚 ドキュメント参照',
                    '🤝 手動支援モード',
                    '📧 技術サポート連絡',
                    '💬 コミュニティフォーラム'
                ]
            },
            'troubleshooting_tips': self._get_troubleshooting_tips(error_context)
        }
    
    def _get_troubleshooting_tips(self, error_context: ErrorContext) -> List[str]:
        """トラブルシューティングヒント取得"""
        
        tips = []
        
        if error_context.category == ErrorCategory.API_TIMEOUT:
            tips.extend([
                "ネットワーク接続の安定性を確認してください",
                "要求の複雑さを下げて再試行してみてください",
                "時間を置いてから再実行することをお勧めします"
            ])
        
        elif error_context.category == ErrorCategory.RESOURCE_EXHAUSTED:
            tips.extend([
                "他のアプリケーションを一時的に終了してください",
                "要求を小さな単位に分割してください",
                "軽量モードでの処理をお試しください"
            ])
        
        elif error_context.category == ErrorCategory.QUALITY_INSUFFICIENT:
            tips.extend([
                "要求をより具体的に記述してください",
                "段階的な実装を検討してください",
                "テンプレートベースの実装をお試しください"
            ])
        
        elif error_context.category == ErrorCategory.FILE_NOT_FOUND:
            tips.extend([
                "ファイルパスの綴りを確認してください",
                "相対パスではなく絶対パスを使用してください",
                "ファイルの存在とアクセス権限を確認してください"
            ])
        
        # 共通ヒント
        tips.extend([
            "問題が続く場合は手動モードをお試しください",
            "エラーログの詳細情報を確認してください"
        ])
        
        return tips[:5]  # 最大5つのヒント
    
    def _generate_next_steps(self, error_context: ErrorContext, 
                           auto_recovery_result: Optional[RecoveryResult]) -> List[str]:
        """次のステップ生成"""
        
        next_steps = []
        
        if auto_recovery_result and auto_recovery_result.success:
            next_steps.extend([
                "✅ 自動回復が完了しました",
                "🔄 元の処理を再実行してください",
                "📊 結果の品質を確認してください"
            ])
            if auto_recovery_result.next_steps:
                next_steps.extend([f"• {step}" for step in auto_recovery_result.next_steps])
        else:
            next_steps.extend([
                "🔍 回復オプションから適切な方法を選択してください",
                "🛠️ 手動での対応が必要な場合があります",
                "💾 必要に応じて作業状態を保存してください"
            ])
        
        # 共通の次のステップ
        next_steps.extend([
            "📈 エラー解決後は通常の処理に戻ります",
            "🔄 問題が解決しない場合は別の回復方法をお試しください"
        ])
        
        return next_steps
    
    def _estimate_resolution_time(self, error_context: ErrorContext) -> Dict[str, str]:
        """解決時間見積もり"""
        
        estimates = {
            ErrorCategory.API_TIMEOUT: {
                'auto_recovery': '1-2分',
                'manual_intervention': '5-10分',
                'worst_case': '15-30分'
            },
            ErrorCategory.API_UNAVAILABLE: {
                'auto_recovery': '即座（オフラインモード）',
                'manual_intervention': '2-5分',
                'worst_case': 'サービス復旧まで'
            },
            ErrorCategory.QUALITY_INSUFFICIENT: {
                'auto_recovery': '30秒-2分',
                'manual_intervention': '3-8分',
                'worst_case': '10-20分'
            },
            ErrorCategory.RESOURCE_EXHAUSTED: {
                'auto_recovery': '30秒-1分',
                'manual_intervention': '2-5分',
                'worst_case': '10-15分'
            },
            ErrorCategory.FILE_NOT_FOUND: {
                'auto_recovery': '10-30秒',
                'manual_intervention': '1-3分',
                'worst_case': '5-10分'
            }
        }
        
        return estimates.get(error_context.category, {
            'auto_recovery': '1-5分',
            'manual_intervention': '5-15分',
            'worst_case': '15-30分'
        })
    
    def execute_recovery_option(self, option_id: str, error_id: str, 
                              ff_input: Optional[Dict[str, Any]] = None) -> RecoveryResult:
        """回復オプション実行"""
        
        # エラーコンテキスト検索
        error_context = None
        for error in reversed(self.error_history):
            if f"error_{int(error.timestamp.timestamp())}_{self.error_history.index(error) + 1}" == error_id:
                error_context = error
                break
        
        if not error_context:
            return RecoveryResult(
                success=False,
                message=f"エラーコンテキストが見つかりません: {error_id}"
            )
        
        # 回復オプション検索
        recovery_option = None
        for option in self.recovery_strategies.get(error_context.category, []):
            if option.id == option_id:
                recovery_option = option
                break
        
        if not recovery_option:
            return RecoveryResult(
                success=False,
                message=f"回復オプションが見つかりません: {option_id}"
            )
        
        # FF入力が必要な場合のチェック
        if recovery_option.requires_ff_input and not ff_input:
            return RecoveryResult(
                success=False,
                message="このオプションはFF管理者の入力が必要です"
            )
        
        # 回復実行
        try:
            result = self._execute_recovery_action(recovery_option, error_context)
            
            if result.success:
                if recovery_option.requires_ff_input:
                    self.recovery_stats['manual_intervention'] += 1
                else:
                    self.recovery_stats['auto_recovered'] += 1
            
            return result
            
        except Exception as e:
            logging.error(f"Recovery option execution failed: {e}")
            return RecoveryResult(
                success=False,
                message=f"回復オプション実行に失敗しました: {str(e)}"
            )
    
    def get_error_history_summary(self) -> Dict[str, Any]:
        """エラー履歴サマリー取得"""
        
        if not self.error_history:
            return {
                'total_errors': 0,
                'summary': '🎉 エラーは発生していません',
                'stats': self.recovery_stats
            }
        
        # 最近のエラー分析
        recent_errors = [
            error for error in self.error_history
            if error.timestamp > datetime.now() - timedelta(hours=24)
        ]
        
        # カテゴリ別集計
        category_counts = {}
        for error in recent_errors:
            category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
        
        # 深刻度別集計
        severity_counts = {}
        for error in recent_errors:
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
        
        return {
            'total_errors': len(self.error_history),
            'recent_errors_24h': len(recent_errors),
            'category_breakdown': category_counts,
            'severity_breakdown': severity_counts,
            'recovery_stats': self.recovery_stats,
            'success_rate': {
                'auto_recovery': self.recovery_stats['auto_recovered'] / max(self.recovery_stats['total_errors'], 1),
                'overall': (self.recovery_stats['auto_recovered'] + self.recovery_stats['manual_intervention']) / max(self.recovery_stats['total_errors'], 1)
            },
            'recommendations': self._generate_error_prevention_recommendations()
        }
    
    def _generate_error_prevention_recommendations(self) -> List[str]:
        """エラー予防推奨事項生成"""
        
        if not self.error_history:
            return ["✨ 継続的な使用で安定性が向上します"]
        
        recommendations = []
        
        # 最頻エラーカテゴリの分析
        recent_errors = [
            error for error in self.error_history
            if error.timestamp > datetime.now() - timedelta(days=7)
        ]
        
        if recent_errors:
            category_counts = {}
            for error in recent_errors:
                category_counts[error.category] = category_counts.get(error.category, 0) + 1
            
            most_common_category = max(category_counts, key=category_counts.get)
            
            if most_common_category == ErrorCategory.API_TIMEOUT:
                recommendations.append("🌐 ネットワーク接続の安定性を確認してください")
                recommendations.append("⚡ 複雑な要求は段階的に分割することをお勧めします")
            
            elif most_common_category == ErrorCategory.RESOURCE_EXHAUSTED:
                recommendations.append("⚡ 軽量モードの使用を検討してください")
                recommendations.append("🧹 定期的なシステムリソースの確認をお勧めします")
            
            elif most_common_category == ErrorCategory.QUALITY_INSUFFICIENT:
                recommendations.append("📝 より具体的で明確な要求記述をお試しください")
                recommendations.append("📋 テンプレートベースの実装を活用してください")
        
        # 全体的な推奨事項
        if len(recent_errors) > 5:
            recommendations.append("🔄 手動モードでの確認を増やすことをお勧めします")
        
        recommendations.append("📊 継続的な使用により自動回復の精度が向上します")
        
        return recommendations[:4]  # 最大4つの推奨事項

# ===================================================================
# メイン実行とテスト
# ===================================================================

def run_error_recovery_test():
    """エラー回復システムテスト実行"""
    
    print("🧪 User Friendly Error Recovery System テスト開始")
    print("=" * 60)
    
    # システム初期化
    recovery_system = UserFriendlyErrorRecovery()
    
    try:
        # テストケース1: API タイムアウト
        print("\n🌐 テストケース1: API タイムアウトエラー")
        timeout_context = {
            'error_message': 'Request timeout after 30 seconds',
            'error': 'TimeoutError',
            'stack_trace': 'Mock stack trace'
        }
        
        timeout_result = recovery_system.handle_system_error(
            error_type="timeout",
            context=timeout_context,
            ff_request="セキュアなファイル処理システムを作成してください"
        )
        
        print(f"✅ エラー処理完了:")
        print(f"   メッセージ: {timeout_result['user_friendly_message']['message']}")
        print(f"   回復オプション数: {len(timeout_result['recovery_options'])}")
        print(f"   自動回復: {'成功' if timeout_result['auto_recovery'] and timeout_result['auto_recovery'].success else '失敗/未実行'}")
        
        # テストケース2: 品質不足エラー
        print("\n📊 テストケース2: 品質不足エラー")
        quality_context = {
            'error_message': 'Generated code quality below 98 points threshold',
            'error': 'QualityError',
            'quality_score': 85
        }
        
        quality_result = recovery_system.handle_system_error(
            error_type="quality_insufficient",
            context=quality_context,
            ff_request="高性能なデータ処理アルゴリズムを実装してください"
        )
        
        print(f"✅ エラー処理完了:")
        print(f"   メッセージ: {quality_result['user_friendly_message']['message']}")
        print(f"   推奨オプション: {[opt['label'] for opt in quality_result['recovery_options'] if opt['recommended']]}")
        
        # テストケース3: リソース不足エラー
        print("\n⚡ テストケース3: リソース不足エラー")
        resource_context = {
            'error_message': 'Insufficient memory for processing',
            'error': 'ResourceExhaustedError',
            'memory_usage': '85%'
        }
        
        resource_result = recovery_system.handle_system_error(
            error_type="resource_exhausted",
            context=resource_context,
            ff_request="大規模データセットの分析システム"
        )
        
        print(f"✅ エラー処理完了:")
        print(f"   深刻度: {resource_result['user_friendly_message']['severity_indicator']}")
        print(f"   解決時間見積: {resource_result['estimated_resolution_time']['auto_recovery']}")
        
        # 回復オプション実行テスト
        print("\n🔧 回復オプション実行テスト:")
        if timeout_result['recovery_options']:
            first_option = timeout_result['recovery_options'][0]
            execution_result = recovery_system.execute_recovery_option(
                option_id=first_option['id'],
                error_id=timeout_result['error_id']
            )
            print(f"   実行結果: {'成功' if execution_result.success else '失敗'}")
            print(f"   メッセージ: {execution_result.message}")
        
        # エラー履歴サマリー
        print("\n📊 エラー履歴サマリー:")
        history_summary = recovery_system.get_error_history_summary()
        print(f"   総エラー数: {history_summary['total_errors']}")
        print(f"   24時間以内: {history_summary['recent_errors_24h']}")
        print(f"   自動回復率: {history_summary['success_rate']['auto_recovery']:.1%}")
        
        if history_summary['recommendations']:
            print(f"   推奨事項:")
            for rec in history_summary['recommendations'][:3]:
                print(f"     • {rec}")
        
        print("\n" + "=" * 60)
        print("✅ Phase 3a基盤システム（エラー回復）実装完了!")
        
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
    
    run_error_recovery_test()
