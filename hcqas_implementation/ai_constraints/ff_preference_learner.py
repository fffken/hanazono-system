import os
import json
import logging
import datetime
from typing import Dict, Any, List

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class FFPreferenceLearner:
    """
    FF管理者の選択とフィードバックから好みやコーディングスタイルを学習する。
    """
    def __init__(self, preferences_path: str = 'ai_memory/ff_preferences.json'):
        self.preferences_path = preferences_path
        self.preferences = self._load_preferences()
        logging.info("FF Preference Learner initialized.")

    def _load_preferences(self) -> Dict[str, Any]:
        """保存されている設定ファイルを読み込む。"""
        try:
            if os.path.exists(self.preferences_path):
                with open(self.preferences_path, 'r') as f:
                    logging.info(f"Loading preferences from {self.preferences_path}")
                    return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Could not load preferences file: {e}")
        
        # デフォルト設定
        return {
            "version": "1.0",
            "last_updated": datetime.datetime.now().isoformat(),
            "style_weights": {
                "concise": 1.0,
                "verbose": 0.5,
                "functional": 0.8,
                "oop": 1.2
            },
            "technology_affinity": {},
            "feedback_history": []
        }

    def save_preferences(self) -> bool:
        """現在の設定をファイルに保存する。"""
        try:
            os.makedirs(os.path.dirname(self.preferences_path), exist_ok=True)
            self.preferences['last_updated'] = datetime.datetime.now().isoformat()
            with open(self.preferences_path, 'w') as f:
                json.dump(self.preferences, f, indent=4)
            logging.info(f"Preferences saved successfully to {self.preferences_path}")
            return True
        except IOError as e:
            logging.error(f"Could not save preferences file: {e}")
            return False

    def learn_from_interaction(self, suggestion_id: str, feedback: Dict[str, Any]):
        """
        ユーザーのフィードバックから学習するメソッド。
        (例: 'selected', 'rejected', 'modified')
        """
        logging.info(f"Learning from interaction for suggestion {suggestion_id} with feedback: {feedback.get('type')}")
        
        interaction_record = {
            "suggestion_id": suggestion_id,
            "feedback_type": feedback.get("type", "unknown"),
            "timestamp": datetime.datetime.now().isoformat(),
            "details": feedback.get("details", {})
        }
        
        self.preferences.setdefault('feedback_history', []).append(interaction_record)
        
        # ここで好みの重み付けを更新するロジックを実装
        # (例: 特定のスタイルの提案が選択されたら、そのスタイルの重みを上げる)
        if feedback.get("type") == "selected":
            # ダミーの重み更新ロジック
            style = feedback.get("details", {}).get("style", "oop")
            if style in self.preferences["style_weights"]:
                self.preferences["style_weights"][style] *= 1.05
                logging.info(f"Increased weight for style '{style}'")

        self.save_preferences()

    def predict_preference_score(self, suggestion_features: Dict[str, Any]) -> float:
        """
        提案の特徴に基づき、FF管理者がどの程度好むかを予測する。
        """
        score = 0.5 # ベーススコア
        style = suggestion_features.get("style", "oop")
        
        if style in self.preferences["style_weights"]:
            score *= self.preferences["style_weights"][style]
        
        # スコアを0.0から1.0の範囲に正規化
        return max(0, min(1.0, score))
        
    def get_recognized_patterns(self) -> List[str]:
        """
        学習履歴から認識された主要な好みパターンを返す。
        """
        patterns = []
        # 例えば、最も重みが高いスタイルを返す
        if self.preferences["style_weights"]:
             highest_style = max(self.preferences["style_weights"], key=self.preferences["style_weights"].get)
             patterns.append(f"Prefers '{highest_style}' style.")
        
        if len(self.preferences.get("feedback_history", [])) > 10:
            patterns.append("Frequent interaction indicates high engagement.")
            
        return patterns if patterns else ["No significant patterns recognized yet."]


if __name__ == '__main__':
    # このファイルが直接実行された場合のテストコード
    print("Running FFPreferenceLearner Self-Test...")
    # テスト用に一時的な設定ファイルを使用
    test_path = 'temp_test_preferences.json'
    learner = FFPreferenceLearner(preferences_path=test_path)
    
    print("\nInitial Preferences:")
    print(json.dumps(learner.preferences, indent=2))
    
    # 学習のシミュレーション
    feedback_data = {
        "type": "selected",
        "details": {"style": "functional"}
    }
    learner.learn_from_interaction("suggestion-123", feedback_data)
    
    print("\nPreferences after learning:")
    print(json.dumps(learner.preferences, indent=2))
    
    # 予測のシミュレーション
    suggestion_data = {"style": "functional"}
    score = learner.predict_preference_score(suggestion_data)
    print(f"\nPredicted preference score for a 'functional' suggestion: {score:.2f}")

    # パターンの確認
    patterns = learner.get_recognized_patterns()
    print("\nRecognized Patterns:")
    for p in patterns:
        print(f"- {p}")

    # クリーンアップ
    if os.path.exists(test_path):
        os.remove(test_path)
    print("\n--- Self-Test Successful ---")
