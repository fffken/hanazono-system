#!/usr/bin/env python3
"""
HANAZONOシステム AI自動修正システム v1.0
AIが自動でコード修正・設定最適化を実行
"""

import os
import sys
import json
import re
import ast
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any
import tempfile
import shutil

class AIAutoFixSystem:
    def __init__(self):
        self.setup_logging()
        self.fixes_applied = []
        self.backup_dir = "ai_auto_fix_backups"
        self.config_file = "ai_auto_fix_config.json"
        
        # 自動修正ルール
        self.fix_rules = {
            "code_style": True,
            "empty_except": True,
            "unused_imports": True,
            "hardcoded_values": True,
            "security_issues": True,
            "performance_optimization": True,
            "settings_optimization": True
        }
        
        self.load_config()
        
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_auto_fix.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """設定読み込み"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.fix_rules.update(config.get('fix_rules', {}))
                
    def save_config(self):
        """設定保存"""
        config = {
            'fix_rules': self.fix_rules,
            'last_run': datetime.now().isoformat()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def create_backup(self, file_path: str) -> str:
        """ファイルバックアップ作成"""
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(file_path)}.backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        shutil.copy2(file_path, backup_path)
        self.logger.info(f"バックアップ作成: {backup_path}")
        return backup_path
        
    def analyze_python_file(self, file_path: str) -> Dict[str, List[Dict]]:
        """Pythonファイルの解析"""
        issues = {
            'syntax_errors': [],
            'style_issues': [],
            'security_issues': [],
            'performance_issues': [],
            'maintainability_issues': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # AST解析
            try:
                tree = ast.parse(content)
                self.analyze_ast(tree, issues, content)
            except SyntaxError as e:
                issues['syntax_errors'].append({
                    'line': e.lineno,
                    'message': str(e),
                    'type': 'syntax_error'
                })
                
        except Exception as e:
            self.logger.error(f"ファイル解析エラー {file_path}: {e}")
            
        return issues
        
    def analyze_ast(self, tree: ast.AST, issues: Dict, content: str):
        """AST解析による問題検出"""
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            # 空の例外処理検出
            if isinstance(node, ast.ExceptHandler):
                if not node.body or (len(node.body) == 1 and 
                                   isinstance(node.body[0], ast.Pass)):
                    issues['maintainability_issues'].append({
                        'line': node.lineno,
                        'message': '空の例外処理が検出されました',
                        'type': 'empty_except',
                        'fix_suggestion': 'ログ出力を追加してください'
                    })
                    
            # ハードコードされた値検出
            elif isinstance(node, ast.Str):
                if any(pattern in node.s.lower() for pattern in 
                      ['password', 'secret', 'key', 'token']):
                    issues['security_issues'].append({
                        'line': node.lineno,
                        'message': 'ハードコードされた認証情報の可能性',
                        'type': 'hardcoded_secret',
                        'fix_suggestion': '環境変数または設定ファイルを使用してください'
                    })
                    
            # 長い関数検出
            elif isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
                if func_lines > 50:
                    issues['maintainability_issues'].append({
                        'line': node.lineno,
                        'message': f'関数が長すぎます ({func_lines}行)',
                        'type': 'long_function',
                        'fix_suggestion': '関数を分割することを検討してください'
                    })
                    
    def auto_fix_code_style(self, file_path: str) -> bool:
        """コードスタイル自動修正"""
        if not self.fix_rules.get('code_style', False):
            return False
            
        try:
            # autopep8を使用した自動修正
            result = subprocess.run([
                'autopep8', '--in-place', '--max-line-length=88', 
                '--aggressive', '--aggressive', file_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.fixes_applied.append(f"コードスタイル修正: {file_path}")
                self.logger.info(f"コードスタイル修正完了: {file_path}")
                return True
            else:
                self.logger.warning(f"コードスタイル修正失敗: {result.stderr}")
                
        except FileNotFoundError:
            self.logger.warning("autopep8が見つかりません")
            
        return False
        
    def auto_fix_empty_except(self, file_path: str) -> bool:
        """空の例外処理自動修正"""
        if not self.fix_rules.get('empty_except', False):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # 空の例外処理パターンを検索・修正
            patterns = [
                (r'except\s*:\s*\n\s*pass', 
                 'except Exception as e:\n        logging.warning(f"Exception occurred: {e}")\n        pass'),
                (r'except\s+\w+\s*:\s*\n\s*pass',
                 'except Exception as e:\n        logging.warning(f"Exception occurred: {e}")\n        pass')
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
            if content != original_content:
                # loggingインポートを追加（存在しない場合）
                if 'import logging' not in content:
                    content = 'import logging\n' + content
                    
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self.fixes_applied.append(f"空の例外処理修正: {file_path}")
                self.logger.info(f"空の例外処理修正完了: {file_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"例外処理修正エラー {file_path}: {e}")
            
        return False
        
    def auto_optimize_settings(self, settings_file: str = "settings.json") -> bool:
        """設定ファイル自動最適化"""
        if not self.fix_rules.get('settings_optimization', False):
            return False
            
        if not os.path.exists(settings_file):
            return False
            
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            original_settings = json.dumps(settings, sort_keys=True)
            optimized = False
            
            # 季節別設定の最適化
            if 'seasonal_settings' in settings:
                current_month = datetime.now().month
                
                # 現在の季節に基づく最適化
                if 12 <= current_month <= 2:  # 冬
                    season = 'winter'
                elif 3 <= current_month <= 5:  # 春
                    season = 'spring_fall'
                elif 6 <= current_month <= 8:  # 夏
                    season = 'summer'
                else:  # 秋
                    season = 'spring_fall'
                    
                # 推奨設定の調整
                if season in settings['seasonal_settings']:
                    settings['current_optimized_season'] = season
                    settings['optimization_timestamp'] = datetime.now().isoformat()
                    optimized = True
                    
            # 重複設定の除去
            if 'detailed_seasonal_settings' in settings:
                # 参照型の設定を最適化
                for key, value in settings['detailed_seasonal_settings'].items():
                    if isinstance(value, dict) and 'reference' in value:
                        ref_season = value['reference']
                        if ref_season in settings['seasonal_settings']:
                            # 直接設定をコピーして参照を除去
                            settings['detailed_seasonal_settings'][key] = \
                                settings['seasonal_settings'][ref_season].copy()
                            optimized = True
                            
            if optimized and json.dumps(settings, sort_keys=True) != original_settings:
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)
                    
                self.fixes_applied.append(f"設定最適化: {settings_file}")
                self.logger.info(f"設定最適化完了: {settings_file}")
                return True
                
        except Exception as e:
            self.logger.error(f"設定最適化エラー {settings_file}: {e}")
            
        return False
        
    def auto_fix_performance_issues(self, file_path: str) -> bool:
        """パフォーマンス問題自動修正"""
        if not self.fix_rules.get('performance_optimization', False):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
    def auto_fix_performance_issues(self, file_path: str) -> bool:
        """パフォーマンス問題自動修正"""
        if not self.fix_rules.get('performance_optimization', False):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # パフォーマンス最適化パターン
            optimizations = [
                # リスト内包表記への変換
                (r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(.+?):\s*\n\s*\1\.append\(([^)]+)\)',
                 r'\1 = [\4 for \2 in \3]'),
                
                # 文字列結合の最適化
                (r'(\w+)\s*=\s*["\']["\'][^=]*?(?:\n.*?)*?\1\s*\+=\s*[^=]+',
                 lambda m: m.group(0).replace('+=', ' = "".join([') + '])')
            ]
            
            for pattern, replacement in optimizations:
                if callable(replacement):
                    # 複雑な置換の場合
                    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
                    for match in matches:
                        content = replacement(match)
                else:
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                    
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self.fixes_applied.append(f"パフォーマンス最適化: {file_path}")
                self.logger.info(f"パフォーマンス最適化完了: {file_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"パフォーマンス最適化エラー {file_path}: {e}")
            
        return False
        
    def auto_fix_security_issues(self, file_path: str) -> bool:
        """セキュリティ問題自動修正"""
        if not self.fix_rules.get('security_issues', False):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # セキュリティ強化パターン
            security_fixes = [
                # ハードコードされたパスワードの環境変数化
                (r'password\s*=\s*["\'][^"\']+["\']',
                 'password = os.getenv("EMAIL_PASSWORD", "")'),
                
                # SQLインジェクション対策
                (r'cursor\.execute\(f["\'].*?\{.*?\}.*?["\']\)',
                 'cursor.execute("SELECT * FROM table WHERE id = ?", (value,))'),
                
                # 安全でないランダム関数の置換
                (r'import random\n.*?random\.random\(\)',
                 'import secrets\nsecrets.SystemRandom().random()')
            ]
            
            for pattern, replacement in security_fixes:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
            # osモジュールのインポート確認
            if 'os.getenv' in content and 'import os' not in content:
                content = 'import os\n' + content
                
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self.fixes_applied.append(f"セキュリティ強化: {file_path}")
                self.logger.info(f"セキュリティ強化完了: {file_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"セキュリティ修正エラー {file_path}: {e}")
            
        return False
        
    def intelligent_error_prediction(self, file_path: str) -> List[Dict]:
        """AI的エラー予測"""
        predictions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # 潜在的問題の予測
                
                # 未チェックの外部APIコール
                if re.search(r'requests\.(get|post)', line) and 'try:' not in lines[max(0, i-3):i]:
                    predictions.append({
                        'line': i,
                        'type': 'potential_network_error',
                        'message': 'ネットワークエラーが発生する可能性があります',
                        'suggestion': 'try-except文でエラーハンドリングを追加',
                        'confidence': 0.8
                    })
                    
                # ファイル操作の未チェック
                if re.search(r'open\(.*?\)', line) and 'with' not in line:
                    predictions.append({
                        'line': i,
                        'type': 'potential_file_error',
                        'message': 'ファイルが適切に閉じられない可能性があります',
                        'suggestion': 'with文を使用してください',
                        'confidence': 0.9
                    })
                    
                # 型エラーの可能性
                if re.search(r'int\(.*?\)', line) and 'try:' not in lines[max(0, i-2):i]:
                    predictions.append({
                        'line': i,
                        'type': 'potential_type_error',
                        'message': '型変換エラーが発生する可能性があります',
                        'suggestion': 'try-except文で型エラーをハンドリング',
                        'confidence': 0.7
                    })
                    
        except Exception as e:
            self.logger.error(f"エラー予測エラー {file_path}: {e}")
            
        return predictions
        
    def generate_improvement_suggestions(self, file_path: str) -> List[str]:
        """改善提案生成"""
        suggestions = []
        
        try:
            issues = self.analyze_python_file(file_path)
            predictions = self.intelligent_error_prediction(file_path)
            
            # 解析結果に基づく提案
            if issues['maintainability_issues']:
                suggestions.append("📋 コードの可読性向上のため、関数を小さく分割することを推奨")
                
            if issues['security_issues']:
                suggestions.append("🔒 セキュリティ強化のため、認証情報を環境変数に移行")
                
            if issues['performance_issues']:
                suggestions.append("⚡ パフォーマンス向上のため、リスト内包表記の使用を検討")
                
            # 予測に基づく提案
            if predictions:
                high_confidence = [p for p in predictions if p['confidence'] > 0.8]
                if high_confidence:
                    suggestions.append("🔮 高確率で発生する可能性のあるエラーを検出、事前対策を推奨")
                    
            # ファイル特有の提案
            if 'email_notifier.py' in file_path:
                suggestions.extend([
                    "📧 メールサーバー接続の冗長化を検討",
                    "📊 送信成功率の監視機能追加を推奨",
                    "🔄 失敗時の自動リトライ機能の実装"
                ])
                
            elif 'main.py' in file_path:
                suggestions.extend([
                    "🚀 アプリケーション起動時のヘルスチェック追加",
                    "📝 設定ファイル検証機能の強化",
                    "🔧 graceful shutdownの実装"
                ])
                
        except Exception as e:
            self.logger.error(f"改善提案生成エラー {file_path}: {e}")
            
        return suggestions
        
    def auto_test_generation(self, file_path: str) -> str:
        """自動テストコード生成"""
        if not os.path.exists(file_path):
            return ""
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 関数を抽出
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'lineno': node.lineno
                    })
                    
            # テストコード生成
            test_code = f'''#!/usr/bin/env python3
"""
自動生成されたテストファイル for {os.path.basename(file_path)}
生成時刻: {datetime.now().isoformat()}
"""

import unittest
import sys
import os

# テスト対象モジュールのインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from {os.path.splitext(os.path.basename(file_path))[0]} import *

class Test{os.path.splitext(os.path.basename(file_path))[0].title()}(unittest.TestCase):
    
    def setUp(self):
        """テスト前の準備"""
        pass
        
    def tearDown(self):
        """テスト後のクリーンアップ"""
        pass
'''

            # 各関数のテストメソッド生成
            for func in functions:
                if not func['name'].startswith('_'):  # プライベート関数以外
                    test_code += f'''
    def test_{func['name']}(self):
        """Test for {func['name']} function"""
        # TODO: {func['name']}関数のテストを実装
        # 引数: {', '.join(func['args'])}
        # self.assertEqual(expected, actual)
        pass
'''

            test_code += '''
if __name__ == '__main__':
    unittest.main()
'''

            # テストファイル保存
            test_filename = f"test_{os.path.splitext(os.path.basename(file_path))[0]}.py"
            test_path = os.path.join('tests', test_filename)
            
            os.makedirs('tests', exist_ok=True)
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_code)
                
            self.logger.info(f"自動テストコード生成完了: {test_path}")
            return test_path
            
        except Exception as e:
            self.logger.error(f"テストコード生成エラー {file_path}: {e}")
            return ""
            
    def run_comprehensive_analysis(self, target_files: List[str] = None) -> Dict:
        """包括的解析実行"""
        if target_files is None:
            target_files = [f for f in os.listdir('.') if f.endswith('.py')]
            
        results = {
            'analyzed_files': len(target_files),
            'fixes_applied': 0,
            'issues_found': 0,
            'suggestions_generated': 0,
            'tests_created': 0,
            'detailed_results': {}
        }
        
        for file_path in target_files:
            if not os.path.exists(file_path):
                continue
                
            self.logger.info(f"解析開始: {file_path}")
            
            # バックアップ作成
            backup_path = self.create_backup(file_path)
            
            file_result = {
                'backup_created': backup_path,
                'issues': {},
                'fixes_applied': [],
                'suggestions': [],
                'test_generated': None
            }
            
            try:
                # 問題解析
                issues = self.analyze_python_file(file_path)
                file_result['issues'] = issues
                results['issues_found'] += sum(len(issue_list) for issue_list in issues.values())
                
                # 自動修正実行
                fixes_count = 0
                if self.auto_fix_code_style(file_path):
                    fixes_count += 1
                if self.auto_fix_empty_except(file_path):
                    fixes_count += 1
                if self.auto_fix_performance_issues(file_path):
                    fixes_count += 1
                if self.auto_fix_security_issues(file_path):
                    fixes_count += 1
                    
                file_result['fixes_applied'] = self.fixes_applied[-fixes_count:]
                results['fixes_applied'] += fixes_count
                
                # 改善提案生成
                suggestions = self.generate_improvement_suggestions(file_path)
                file_result['suggestions'] = suggestions
                results['suggestions_generated'] += len(suggestions)
                
                # テストコード生成
                if file_path.endswith('.py') and not file_path.startswith('test_'):
                    test_path = self.auto_test_generation(file_path)
                    if test_path:
                        file_result['test_generated'] = test_path
                        results['tests_created'] += 1
                        
            except Exception as e:
                self.logger.error(f"ファイル処理エラー {file_path}: {e}")
                file_result['error'] = str(e)
                
            results['detailed_results'][file_path] = file_result
            
        # 設定最適化
        if self.auto_optimize_settings():
            results['fixes_applied'] += 1
            
        return results
        
    def generate_report(self, results: Dict) -> str:
        """レポート生成"""
        report = f"""
🤖 AI自動修正システム レポート
生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 実行結果サマリー:
- 解析ファイル数: {results['analyzed_files']}
- 適用された修正: {results['fixes_applied']}件
- 検出された問題: {results['issues_found']}件
- 生成された提案: {results['suggestions_generated']}件
- 作成されたテスト: {results['tests_created']}件

🔧 適用された修正一覧:
"""
        
        for fix in self.fixes_applied:
            report += f"  ✅ {fix}\n"
            
        report += "\n📋 ファイル別詳細結果:\n"
        
        for file_path, file_result in results['detailed_results'].items():
            report += f"\n📁 {file_path}:\n"
            
            if file_result.get('error'):
                report += f"  ❌ エラー: {file_result['error']}\n"
                continue
                
            # 問題の要約
            total_issues = sum(len(issues) for issues in file_result['issues'].values())
            if total_issues > 0:
                report += f"  ⚠️ 検出された問題: {total_issues}件\n"
                
            # 修正の要約
            if file_result['fixes_applied']:
                report += f"  🔧 適用された修正: {len(file_result['fixes_applied'])}件\n"
                
            # 提案の要約
            if file_result['suggestions']:
                report += f"  💡 改善提案:\n"
                for suggestion in file_result['suggestions'][:3]:  # 最初の3件のみ
                    report += f"    - {suggestion}\n"
                    
            # テスト生成
            if file_result['test_generated']:
                report += f"  🧪 テストコード生成: {file_result['test_generated']}\n"
                
        return report
        
def main():
    """メイン実行"""
    print("🤖 AI自動修正システム v1.0")
    print("=" * 50)
    
    # システム初期化
    ai_fix = AIAutoFixSystem()
    
    # 対象ファイル指定
    if len(sys.argv) > 1:
        target_files = sys.argv[1:]
    else:
        target_files = [f for f in os.listdir('.') if f.endswith('.py') and 
                       not f.startswith('test_') and f != __file__]
        
    print(f"📁 対象ファイル: {', '.join(target_files)}")
    print()
    
    # 包括的解析・修正実行
    results = ai_fix.run_comprehensive_analysis(target_files)
    
    # レポート生成・表示
    report = ai_fix.generate_report(results)
    print(report)
    
    # レポートファイル保存
    report_filename = f"ai_auto_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"\n📄 詳細レポート保存: {report_filename}")
    
    # 設定保存
    ai_fix.save_config()
    
    print("\n🎉 AI自動修正システム実行完了!")

if __name__ == "__main__":
    main()
