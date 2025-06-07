import logging
from typing import Dict, Any
from .smart_suggestion_engine import SmartSuggestion

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def adapt_suggestion_data(suggestion: SmartSuggestion) -> Dict[str, Any]:
    """
    SmartSuggestionオブジェクトをUI表示用の辞書に変換するアダプター。
    """
    if not isinstance(suggestion, SmartSuggestion):
        logging.error("adapt_suggestion_data received an invalid object type.")
        # オブジェクトでない場合は、フォールバック用の空データを返す
        return {
            "quality_score": {"total": 0},
            "confidence_level": 0.0,
            "ff_alignment_score": 0.0,
            "implementation": "Error: Invalid suggestion data.",
            "generation_method": "error"
        }
        
    # オブジェクトの属性に直接アクセスする
    return {
        "quality_score": suggestion.quality_score,
        "confidence_level": suggestion.confidence_level,
        "ff_alignment_score": suggestion.ff_alignment_score,
        "implementation": suggestion.implementation,
        "generation_method": suggestion.generation_method,
        "suggestion_id": suggestion.suggestion_id
    }

class SmartProposalUI:
    """
    AIからの提案をユーザーに分かりやすく提示するためのUIロジック。
    """
    def __init__(self, presentation_style: str = 'traditional'):
        self.presentation_style = presentation_style
        logging.info(f"Smart Proposal UI initialized with style: {self.presentation_style}")

    def _generate_transparency_report(self, data: Dict[str, Any]) -> str:
        """提案の根拠を示す透明性レポートを生成する。"""
        report = (
            f"### AI提案の根拠開示 ###\n"
            f"- **品質スコア**: {data['quality_score'].get('total', 'N/A')}点\n"
            f"  - 可読性: {data['quality_score'].get('readability', 'N/A')}点\n"
            f"  - パフォーマンス: {data['quality_score'].get('performance', 'N/A')}点\n"
            f"  - セキュリティ: {data['quality_score'].get('security', 'N/A')}点\n"
            f"- **AI信頼度**: {data['confidence_level']:.1%}\n"
            f"- **FF管理者様との整合性**: {data['ff_alignment_score']:.1%}\n"
            f"- **生成方式**: {data['generation_method']}\n"
        )
        return report

    def generate_proposal(self, suggestion_data: SmartSuggestion) -> str:
        """
        SmartSuggestionオブジェクトを受け取り、完全な提案UIテキストを生成する。
        """
        logging.info(f"Generating proposal for suggestion {suggestion_data.suggestion_id if isinstance(suggestion_data, SmartSuggestion) else 'N/A'}")

        # アダプターを介して、オブジェクトを安全な辞書形式に変換
        adapted_data = adapt_suggestion_data(suggestion_data)
        
        # フォールバック処理
        if adapted_data["generation_method"] == "error":
            logging.error("Fallback to manual mode due to invalid suggestion data.")
            return self.generate_manual_proposal("無効な提案データを受け取ったため、手動モードで表示します。")

        try:
            transparency_report = self._generate_transparency_report(adapted_data)
            
            proposal_text = (
                "============================================================\n"
                "🤖 HCQAS AI スマート提案 🤖\n"
                "============================================================\n"
                f"{transparency_report}\n"
                "--- 提案コード ---\n"
                f"{adapted_data['implementation']}\n"
                "--------------------\n\n"
                "[アクションを選択してください: (1)承認 (2)代替案 (3)却下]\n"
            )
            return proposal_text
        except (KeyError, AttributeError) as e:
            logging.error(f"Error generating smart proposal: {e}. Falling back to manual mode.", exc_info=True)
            return self.generate_manual_proposal(f"提案の表示中にエラーが発生しました: {e}")

    def generate_manual_proposal(self, reason: str) -> str:
        """スマート提案が失敗した際のフォールバック用UI。"""
        proposal_text = (
            "============================================================\n"
            "⚠️ HCQAS 手動モード ⚠️\n"
            "============================================================\n"
            f"理由: {reason}\n\n"
            "現在、AIによる提案を自動生成できません。\n"
            "お手数ですが、手動でのご対応をお願いいたします。\n"
        )
        return proposal_text

if __name__ == '__main__':
    # このファイルが直接実行された場合のテストコード
    from .smart_suggestion_engine import SmartSuggestionEngine
    
    print("Running SmartProposalUI Self-Test...")
    
    # 1. 正常な提案を生成
    engine = SmartSuggestionEngine()
    good_suggestion = engine.generate_suggestion("Test a good suggestion")
    
    # 2. UIを生成
    ui = SmartProposalUI()
    proposal_output = ui.generate_proposal(good_suggestion)
    
    print("\n--- Generated Proposal (Success Case) ---")
    print(proposal_output)
    
    # 3. 不正なデータでテスト
    bad_data = {"some_key": "some_value"} # SmartSuggestionオブジェクトではない
    
    print("\n--- Generating Proposal (Failure Case) ---")
    # 不正なデータを渡しても、内部で処理されて手動モードになるはず
    # @ts-ignore
    proposal_output_bad = ui.generate_proposal(bad_data)
    print(proposal_output_bad)
    
    print("--- Self-Test Successful ---")
