import subprocess
import sys
import os
import json
import traceback

def print_header(title, level=1):
    if level == 1:
        print("\n" + "="*80)
        print(f"🔬 {title}")
        print("="*80)
    else:
        print("\n" + "-"*60)
        print(f"📋 {title}")
        print("-"*60)

def check(description, function_to_run):
    """テストを実行し、成功/失敗/スキップを表示するヘルパー関数"""
    print(f"- {description}: ", end="")
    try:
        # 関数自体を実行
        result = function_to_run()
        
        # 結果の評価
        if result is True:
            print("✅ 正常")
            return True
        elif result == "SKIPPED":
            print("⚠️ スキップ")
            return True # スキップは失敗ではない
        else:
            # resultがFalseまたはNone、その他の予期せぬ値の場合
            print("❌ 失敗")
            return False
            
    except Exception as e:
        print("❌ 失敗 (例外発生)")
        # tracebackをログに出力する代わりにコンソールに表示
        print("\n--- エラー詳細 ---")
        traceback.print_exc()
        print("--------------------\n")
        return False

def main():
    print("🚀 HANAZONO統合システム 精密検査スキャナー起動...")
    
    # 総合評価用のフラグ
    all_systems_go = True

    # --- 1. メールシステムの精密検査 ---
    print_header("1. メールシステム 精密検査")

    # 1.1 設定ファイルの検証
    print_header("1.1 設定ファイルの検証", level=2)
    def test_config():
        global settings
        if not os.path.exists('settings.json'): return False
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return 'notification' in settings and 'email' in settings['notification']
    
    if not check("settings.jsonの読み込みと構造確認", test_config):
        all_systems_go = False

    # 1.2 依存関係の深掘り調査
    print_header("1.2 依存関係の深掘り調査", level=2)
    def test_weather_import():
        from weather_forecast import get_weather_forecast
        return True # インポートできれば成功
    
    if not check("天気予報モジュールのインポート", test_weather_import):
        all_systems_go = False

    # --- 2. HCQASシステムの精密検査 ---
    print_header("2. HCQASシステム 精密検査")
    def test_hcqas_import():
        # hcqas_capsuleではなく、本体をテストする
        from hcqas_implementation.ai_constraints.smart_suggestion_engine import SmartSuggestionEngine
        engine = SmartSuggestionEngine()
        suggestion = engine.generate_suggestion("test")
        return suggestion is not None

    if not check("HCQAS提案エンジンの初期化と実行", test_hcqas_import):
        all_systems_go = False

    # --- 3. 総合評価 ---
    print_header("3. 総合評価")
    if all_systems_go:
        print("✅✅✅ 結論: 主要システムの基礎的な連携・動作に問題は見つかりませんでした。")
    else:
        print("❌❌❌ 結論: システムの一部に、依然として解決すべき問題が残っています。")


if __name__ == "__main__":
    main()
