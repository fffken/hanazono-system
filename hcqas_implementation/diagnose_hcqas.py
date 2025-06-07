import datetime
import logging
import traceback
import sys
import os

# ==============================================================================
# ▼▼▼ 自己認識能力の追加 ▼▼▼
# このスクリプトがどこにあっても、プロジェクトのルートディレクトリを見つけ出す
# ==============================================================================
try:
    script_path = os.path.abspath(__file__)
    # プロジェクトルートは、このファイルの2つ上のディレクトリ
    # 例: /home/pi/lvyuan_solar_control/hcqas_implementation/diagnose_hcqas.py -> /home/pi/lvyuan_solar_control
    project_root = os.path.dirname(os.path.dirname(script_path))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
except NameError:
    # インタラクティブモードなど、__file__ が定義されていない場合
    # カレントディレクトリをプロジェクトルートと仮定
    project_root = os.getcwd()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
# ==============================================================================

# --- 診断用設定 ---
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)

# --- 診断クラス ---
class SystemDiagnoser:
    def __init__(self):
        self.results = {
            "ff_preference_learner": {"status": "untested", "errors": []},
            "smart_suggestion_engine": {"status": "untested", "errors": []},
            "smart_proposal_ui": {"status": "untested", "errors": []},
            "integration_system": {"status": "untested", "errors": []},
            "health_monitoring": {"status": "untested", "errors": []},
        }
        self.critical_error_count = 0
        self.partial_dysfunction_count = 0
        self.minor_issue_count = 0
        self.healthy_count = 0

    def print_header(self, title):
        print("-" * 60)
        print(f"📋 {title}")
        print("-" * 60)

    def check(self, component, function_name, function_to_run):
        try:
            result = function_to_run()
            print(f"  ✅ {function_name}: 正常")
            return result
        except Exception as e:
            print(f"  ❌ {function_name}: 重大エラー")
            self.results[component]['status'] = 'critical_error'
            self.results[component]['errors'].append(str(e))
            logging.error(f"Error in [{component} - {function_name}]: {e}\n{traceback.format_exc()}")
            return None

    def run_diagnosis(self):
        print("=" * 80)
        print(f"🏥 HCQASシステム完全精密診断開始")
        print("=" * 80)
        print(f"診断日時: {datetime.datetime.now()}")
        print("=" * 80)

        self.print_header("1. 統合システム診断 (モジュールロード)")
        try:
            from hcqas_implementation.ai_constraints.smart_suggestion_engine import SmartSuggestionEngine, SmartSuggestion
            from hcqas_implementation.ai_constraints.ff_preference_learner import FFPreferenceLearner
            from hcqas_implementation.ai_constraints.smart_proposal_ui import SmartProposalUI
            print("  ✅ 全ての主要モジュールのインポートに成功")
            self.results['integration_system']['status'] = 'healthy'
        except Exception as e:
            print("  ❌ 主要モジュールのインポートに失敗。これ以降の診断は実行不可能です。")
            self.results['integration_system']['status'] = 'critical_error'
            self.results['integration_system']['errors'].append(str(e))
            self.print_summary()
            return

        # --- Smart Suggestion Engine 診断 ---
        self.print_header("2. Smart Suggestion Engine 完全診断")
        engine = self.check('smart_suggestion_engine', '初期化', lambda: SmartSuggestionEngine())
        if self.results['smart_suggestion_engine']['status'] != 'critical_error':
            suggestion = self.check('smart_suggestion_engine', '提案生成', lambda: engine.generate_suggestion("Test request for diagnosis"))
            if self.results['smart_suggestion_engine']['status'] != 'critical_error':
                self.results['smart_suggestion_engine']['status'] = 'healthy'

        # --- FF Preference Learner 診断 ---
        self.print_header("3. FF Preference Learner 完全診断")
        temp_pref_path = 'ai_memory/temp_diag_prefs.json'
        learner = self.check('ff_preference_learner', '初期化', lambda: FFPreferenceLearner(preferences_path=temp_pref_path))
        if self.results['ff_preference_learner']['status'] != 'critical_error':
            self.check('ff_preference_learner', '学習機能', lambda: learner.learn_from_interaction("diag-123", {"type": "selected"}))
            self.check('ff_preference_learner', '設定保存', lambda: learner.save_preferences())
            if self.results['ff_preference_learner']['status'] != 'critical_error':
                self.results['ff_preference_learner']['status'] = 'healthy'
            if os.path.exists(temp_pref_path): os.remove(temp_pref_path)

        # --- Smart Proposal UI 診断 ---
        self.print_header("4. Smart Proposal UI 完全診断")
        ui = self.check('smart_proposal_ui', '初期化', lambda: SmartProposalUI())
        if self.results['smart_proposal_ui']['status'] != 'critical_error' and 'suggestion' in locals() and suggestion:
            proposal_text = self.check('smart_proposal_ui', 'スマート提案', lambda: ui.generate_proposal(suggestion))
            if proposal_text and "手動モード" not in proposal_text:
                print("  ✅ フォールバックなしで提案生成成功")
                if self.results['smart_proposal_ui']['status'] != 'critical_error':
                    self.results['smart_proposal_ui']['status'] = 'healthy'
            else:
                print("  ⚠️ スマート提案が手動モードにフォールバックしました")
                self.results['smart_proposal_ui']['status'] = 'partial_dysfunction'
                self.results['smart_proposal_ui']['errors'].append("Fallback to manual mode")
        
        # --- ヘルスモニタリング診断 ---
        self.print_header("5. ヘルスモニタリング診断")
        try:
            import psutil
            print("  ✅ psutilモジュール: インストール済み")
            self.results['health_monitoring']['status'] = 'healthy'
        except ImportError:
            print("  ⚠️ psutilモジュール: 未インストール")
            self.results['health_monitoring']['status'] = 'minor_issue'

        self.print_summary()

    def print_summary(self):
        self.healthy_count, self.critical_error_count, self.partial_dysfunction_count, self.minor_issue_count = 0, 0, 0, 0
        for status_info in self.results.values():
            status = status_info['status']
            if status == 'healthy': self.healthy_count += 1
            elif status == 'critical_error': self.critical_error_count += 1
            elif status == 'partial_dysfunction': self.partial_dysfunction_count +=1
            elif status == 'minor_issue': self.minor_issue_count += 1

        print("\n" + "=" * 80)
        print("🏥 診断結果サマリー")
        print("=" * 80)
        print(f"総システム数: {len(self.results)}")
        print(f"🟢 完全健康: {self.healthy_count}システム")
        if self.partial_dysfunction_count > 0: print(f"🟡 部分機能低下: {self.partial_dysfunction_count}システム")
        if self.critical_error_count > 0: print(f"🔴 重大エラー: {self.critical_error_count}システム")
        if self.minor_issue_count > 0: print(f"🟠 軽微な問題: {self.minor_issue_count}システム")
        
        print("-" * 80)
        if self.critical_error_count > 0: print("🎯 総合診断: 要治療")
        elif self.partial_dysfunction_count > 0: print("🎯 総合診断: 良好 (一部機能制限あり)")
        elif self.minor_issue_count > 0: print("🎯 総合診断: 良好 (軽微な問題あり)")
        else: print("🎯 総合診断: 完璧")
        print("=" * 80)
        print("🏥 完全精密診断完了")

if __name__ == "__main__":
    diagnoser = SystemDiagnoser()
    diagnoser.run_diagnosis()
