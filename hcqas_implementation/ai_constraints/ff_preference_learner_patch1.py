import os
import sqlite3
import logging
from datetime import datetime

class FFPreferenceLearner:
    """FF管理者好み学習システム（DD2改善完全版）"""

    def __init__(self, storage_path: str = None):
        # DD2改善: メモリ最適化ストレージ
        self.storage = MemoryOptimizedStorage(max_memory_mb=50)

        # 学習パターン初期化
        self.preference_patterns = {
            'code_style': WeightedPattern(decay_rate=0.98),
            'complexity_level': AdaptivePattern(adaptation_rate=0.08),
            'error_tolerance': LearningPattern(learning_rate=0.03),
            'automation_acceptance': TrustPattern()
        }

        # データベース設定
        self.storage_path = storage_path or os.path.expanduser('~/.hcqas/ff_preferences.db')
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self._init_database()

        # 学習状態
        self.learning_active = True
        self.interaction_count = 0
        self.last_analysis_time = datetime.now()

        # DD2改善: 学習データ圧縮
        self.data_compressor = DataCompressor()

        logging.info("FF Preference Learner initialized with DD2 optimizations")

    def _init_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.storage_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    ff_request TEXT NOT NULL,
                    choices_made TEXT NOT NULL
                )
            ''')

    # --- 追加: 学習メソッド ---
    def learn_from_interaction(self, interaction_data):
        """
        インタラクションデータから好みを学習。
        interaction_data: Dictまたはオブジェクト（選択・評価履歴など）
        """
        if not self.learning_active:
            return
        try:
            for pattern_name, pattern in self.preference_patterns.items():
                if pattern_name in interaction_data:
                    pattern.update(interaction_data[pattern_name])
            self.interaction_count += 1
            self.last_analysis_time = datetime.now()
            # 必要に応じてDB保存・圧縮
            self.data_compressor.compress(self.preference_patterns)
        except Exception as e:
            logging.warning(f"Learning from interaction failed: {e}")
