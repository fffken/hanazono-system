import logging
from typing import Dict

class SmartProposalUI:
    def __init__(self, suggestion_engine, transparency_engine):
        self.suggestion_engine = suggestion_engine
        self.transparency_engine = transparency_engine
        self.transparency_levels = {
            'basic': ['approach_type', 'quality_score'],
            'full': ['implementation', 'alternatives', 'metadata', 'created_at'],
        }

    def _create_friendly_summary(self, data):
        """使いやすい要約作成"""
        approach = getattr(data, 'generation_method', 'balanced')
        quality = 0
        # 型安全なアクセス
        if hasattr(data, "quality_score"):
            qs = getattr(data, "quality_score")
            if isinstance(qs, dict) and "total" in qs:
                quality = qs["total"]
            elif hasattr(data, "total_quality_score"):
                quality = data.total_quality_score

        approach_descriptions = {
            'ff_optimized': 'FF管理者の好みに最適化',
            'balanced': 'バランス重視',
            'security_first': 'セキュリティ最優先',
        }
        approach_desc = approach_descriptions.get(approach, approach)
        return f"[{approach_desc}] 品質スコア: {quality}点"

    # 他のUIメソッドも同様に型安全なアクセスへ
    # ...（省略: 既存ロジックを適宜コピペ・移植）
