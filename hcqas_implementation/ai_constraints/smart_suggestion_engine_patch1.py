from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class SmartSuggestion:
    """スマート提案データ"""
    suggestion_id: str
    ff_request: str
    implementation: str
    quality_score: Dict[str, int]
    ff_alignment_score: float
    confidence_level: float
    generation_method: str
    alternative_options: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime

    # --- dict互換アクセサ追加 ---
    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        if key in self.__dict__:
            return self.__dict__[key]
        return default

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        return hasattr(self, key) or key in self.__dict__
