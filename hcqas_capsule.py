import sys
import logging

# HCQASモジュールのパス問題を解決
sys.path.append('.') 

def run_hcqas_suggestion():
    """HCQASの提案を生成する自己完結型関数"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('hcqas_capsule')
    
    try:
        from hcqas_implementation.ai_constraints.smart_suggestion_engine import SmartSuggestionEngine
        
        logger.info("HCQAS提案生成を開始します...")
        engine = SmartSuggestionEngine()
        request = "日次レポートに、前日との発電量比較を追加する機能"
        suggestion = engine.generate_suggestion(request)
        
        logger.info(f"HCQAS提案生成成功！品質スコア: {suggestion.quality_score.get('total')}")
        print("\n--- 🤖 HCQAS PROPOSAL ---")
        print(suggestion.implementation)
        print("--------------------------")
        return True

    except ImportError:
        logger.error("HCQASモジュールのインポートに失敗しました。パスを確認してください。")
        return False
    except Exception as e:
        logger.error(f'HCQASの実行中にエラー: {e}', exc_info=True)
        return False

if __name__ == "__main__":
    print("--- 🧠 HCQAS提案カプセル実行 ---")
    if run_hcqas_suggestion():
        print("✅ 正常に処理が完了しました。")
    else:
        print("❌ 処理中にエラーが発生しました。")
