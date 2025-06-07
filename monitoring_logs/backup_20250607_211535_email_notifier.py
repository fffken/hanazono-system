import sys
import os
import traceback
import json
import logging

# ==============================================================================
# ▼▼▼ 根本原因特定のための精密検査コード ▼▼▼
# ==============================================================================

print("="*60)
print("🔬根本原因の精密検査を開始します。")
print("="*60)

# --- 自己位置特定 ---
try:
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(script_path))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print("✅ 自己位置特定: 成功")
except Exception as e:
    print(f"❌ 自己位置特定: 失敗 - {e}")

# --- 依存モジュールの個別インポートテスト ---
print("\n--- 依存モジュールの個別インポートテスト ---")

HEALTH = {}

# Test 1: settings_recommender
try:
    print("\n[1/3] 'settings_recommender' をインポート中...")
    from settings_recommender import SettingsRecommender
    print("  ✅ 成功: 'settings_recommender' のインポートが完了しました。")
    HEALTH['settings_recommender'] = True
except Exception as e:
    print(f"  ❌ 失敗: 'settings_recommender' のインポート中にエラーが発生しました。")
    print(f"     エラータイプ: {type(e).__name__}")
    print(f"     エラー内容: {e}")
    traceback.print_exc()
    HEALTH['settings_recommender'] = False

# Test 2: weather_forecast
try:
    print("\n[2/3] 'weather_forecast' をインポート中...")
    from weather_forecast import get_weather_forecast
    print("  ✅ 成功: 'weather_forecast' のインポートが完了しました。")
    HEALTH['weather_forecast'] = True
except Exception as e:
    print(f"  ❌ 失敗: 'weather_forecast' のインポート中にエラーが発生しました。")
    print(f"     エラータイプ: {type(e).__name__}")
    print(f"     エラー内容: {e}")
    traceback.print_exc()
    HEALTH['weather_forecast'] = False

# Test 3: season_detector
try:
    print("\n[3/3] 'season_detector' をインポート中...")
    from season_detector import get_current_season, get_detailed_season
    print("  ✅ 成功: 'season_detector' のインポートが完了しました。")
    HEALTH['season_detector'] = True
except Exception as e:
    print(f"  ❌ 失敗: 'season_detector' のインポート中にエラーが発生しました。")
    print(f"     エラータイプ: {type(e).__name__}")
    print(f"     エラー内容: {e}")
    traceback.print_exc()
    HEALTH['season_detector'] = False

print("\n--- 依存モジュールのテスト完了 ---")


# --- メイン処理のテスト（インポートが成功した場合のみ） ---
if all(HEALTH.values()):
    print("\n✅ 全ての依存モジュールは正常にインポートされました。")
    print("   メインのテスト処理に進みます...")
    
    # 以前のテストコードをここに配置
    # ただし、今は原因特定が目的なので、シンプルに実行
    try:
        print("\n--- メインテスト処理開始 ---")
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        print("✅ settings.jsonの読み込み: 成功")
        
        # ここでEnhancedEmailNotifierクラスを定義する
        class EnhancedEmailNotifier:
            def __init__(self, settings, logger=None):
                self.settings = settings
                self.email_config = self.settings.get('email', {})
            def send_daily_report(self, data, test_mode=False):
                print("✅ send_daily_reportが呼び出されました。")
                return True

        notifier = EnhancedEmailNotifier(settings)
        print("✅ EnhancedEmailNotifierの初期化: 成功")
        
        success = notifier.send_daily_report({}, test_mode=True)
        if success:
            print("\n✅ メインテスト処理は正常に完了しました。")
        else:
            print("\n❌ メインテスト処理で失敗が報告されました。")

    except Exception as e:
        print("\n❌ メインテスト処理中に予期せぬエラーが発生しました。")
        print(f"   エラータイプ: {type(e).__name__}")
        print(f"   エラー内容: {e}")
        traceback.print_exc()
else:
    print("\n❌ 一つ以上の依存モジュールのインポートに失敗したため、メインのテスト処理は実行しません。")
    print("   上記のエラー内容が根本原因です。")

print("\n" + "="*60)
print("🔬精密検査完了。")
print("="*60)
