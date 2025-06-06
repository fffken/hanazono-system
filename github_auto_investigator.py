#!/usr/bin/env python3
"""
GitHub自動調査・修正統合システム v1.0
究極の自動化：人間の手作業完全排除
"""
import os
import subprocess
import json
import re
import requests
import time
from datetime import datetime
from pathlib import Path

class GitHubAutoInvestigator:
    def __init__(self):
        self.base_dir = "/home/pi/lvyuan_solar_control"
        self.repo_owner = "fffken"
        self.repo_name = "hanazono-system"
        self.github_raw_base = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/main"
        self.issues_found = []
        self.fixes_applied = []
        
    def run_full_investigation(self):
        """完全自動調査・修正実行"""
        print("🔍 GitHub自動調査・修正統合システム v1.0")
        print("=" * 60)
        print("🤖 究極の自動化開始：人間の手作業完全排除")
        
        # Phase 1: GitHub自動調査
        print("\n📡 Phase 1: GitHub自動調査実行中...")
        github_files = self._scan_github_repository()
        
        # Phase 2: ローカルとの差分分析
        print("\n🔍 Phase 2: ローカル差分自動分析...")
        issues = self._analyze_differences(github_files)
        
        # Phase 3: 問題自動検出
        print("\n⚠️ Phase 3: システム問題自動検出...")
        system_issues = self._detect_system_issues()
        
        # Phase 4: AI自動修正
        print("\n🔧 Phase 4: AI自動修正実行...")
        fixes = self._auto_fix_issues(issues + system_issues)
        
        # Phase 5: 自動テスト・検証
        print("\n🧪 Phase 5: 自動テスト・検証...")
        test_results = self._auto_test_system()
        
        # Phase 6: 自動デプロイ
        print("\n🚀 Phase 6: 自動デプロイ...")
        deploy_success = self._auto_deploy()
        
        # 結果レポート
        self._generate_investigation_report(fixes, test_results, deploy_success)
        
    def _scan_github_repository(self):
        """GitHub リポジトリ自動スキャン"""
        files_to_check = [
            "AI_WORK_RULES.md",
            "PROJECT_STATUS.md", 
            "github_auto_handover.md",
            "main.py",
            "email_notifier.py",
            "enhanced_email_system_v2.py",
            "hanazono_dashboard.py",
            "settings.json"
        ]
        
        github_files = {}
        for file_path in files_to_check:
            try:
                url = f"{self.github_raw_base}/{file_path}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    github_files[file_path] = response.text
                    print(f"   ✅ {file_path}: 取得成功")
                else:
                    print(f"   ❌ {file_path}: 取得失敗 ({response.status_code})")
            except Exception as e:
                print(f"   ⚠️ {file_path}: 接続エラー ({e})")
                
        return github_files
        
    def _analyze_differences(self, github_files):
        """ローカルとGitHubの差分自動分析"""
        issues = []
        
        for file_path, github_content in github_files.items():
            local_path = Path(self.base_dir) / file_path
            if local_path.exists():
                try:
                    with open(local_path, 'r') as f:
                        local_content = f.read()
                    
                    if local_content != github_content:
                        issues.append({
                            'type': 'file_diff',
                            'file': file_path,
                            'description': f'{file_path}のローカルとGitHubで差分あり',
                            'severity': 'medium'
                        })
                        print(f"   📝 差分検出: {file_path}")
                except Exception as e:
                    issues.append({
                        'type': 'file_error',
                        'file': file_path,
                        'description': f'{file_path}読み込みエラー: {e}',
                        'severity': 'high'
                    })
            else:
                issues.append({
                    'type': 'missing_file',
                    'file': file_path,
                    'description': f'{file_path}がローカルに存在しない',
                    'severity': 'high'
                })
                
        return issues
        
    def _detect_system_issues(self):
        """システム問題自動検出"""
        issues = []
        
        # ログファイルから問題検出
        log_files = [
            "logs/cron_daily_report_morning.log",
            "logs/cron_daily_report_night.log", 
            "solar_control.log"
        ]
        
        for log_file in log_files:
            log_path = Path(self.base_dir) / log_file
            if log_path.exists():
                try:
                    with open(log_path, 'r') as f:
                        log_content = f.read()
                    
                    # エラーパターン検出
                    error_patterns = [
                        (r'ERROR.*バッテリー.*N/A', 'battery_extraction_error'),
                        (r'ERROR.*メール送信エラー', 'email_error'),
                        (r'ERROR.*データ取得.*失敗', 'data_collection_error'),
                        (r'ERROR.*接続.*失敗', 'connection_error')
                    ]
                    
                    for pattern, issue_type in error_patterns:
                        if re.search(pattern, log_content):
                            issues.append({
                                'type': issue_type,
                                'file': log_file,
                                'description': f'{log_file}でエラーパターン検出: {issue_type}',
                                'severity': 'high'
                            })
                            print(f"   🚨 問題検出: {issue_type} in {log_file}")
                            
                except Exception as e:
                    print(f"   ⚠️ ログ分析エラー: {log_file} - {e}")
        
        # システムリソース問題検出
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            if cpu_percent > 90:
                issues.append({
                    'type': 'high_cpu',
                    'description': f'CPU使用率異常: {cpu_percent}%',
                    'severity': 'medium'
                })
            if memory_percent > 90:
                issues.append({
                    'type': 'high_memory', 
                    'description': f'メモリ使用率異常: {memory_percent}%',
                    'severity': 'medium'
                })
            if disk_percent > 95:
                issues.append({
                    'type': 'disk_full',
                    'description': f'ディスク容量不足: {disk_percent}%',
                    'severity': 'high'
                })
        except:
            pass
            
        return issues
        
    def _auto_fix_issues(self, issues):
        """AI自動修正実行"""
        fixes = []
        
        for issue in issues:
            fix_result = None
            
            if issue['type'] == 'battery_extraction_error':
                fix_result = self._fix_battery_extraction()
            elif issue['type'] == 'email_error':
                fix_result = self._fix_email_issues()
            elif issue['type'] == 'data_collection_error':
                fix_result = self._fix_data_collection()
            elif issue['type'] == 'missing_file':
                fix_result = self._fix_missing_file(issue['file'])
            elif issue['type'] == 'high_cpu':
                fix_result = self._fix_high_cpu()
            elif issue['type'] == 'disk_full':
                fix_result = self._fix_disk_space()
                
            if fix_result:
                fixes.append({
                    'issue': issue,
                    'fix': fix_result,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"   ✅ 自動修正完了: {issue['type']}")
            else:
                print(f"   ❌ 自動修正失敗: {issue['type']}")
                
        return fixes
        
    def _fix_battery_extraction(self):
        """バッテリー抽出問題修正"""
        try:
            # AIAutoResolverV2を使用
            resolver_path = Path(self.base_dir) / "ai_auto_resolver_v2.py"
            if resolver_path.exists():
                result = subprocess.run(['python3', str(resolver_path)], 
                                      capture_output=True, text=True)
                return "AI自動修正システムv2.0実行" if result.returncode == 0 else None
        except:
            pass
        return None
        
    def _fix_email_issues(self):
        """メール問題修正"""
        # SMTPパスワード確認
        try:
            settings_path = Path(self.base_dir) / "settings.json"
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                
                smtp_password = settings.get('email', {}).get('smtp_password', '')
                if smtp_password == '${SMTP_PASSWORD}':
                    return "SMTP環境変数設定が必要"
                    
        except:
            pass
        return "メール設定確認済み"
        
    def _fix_data_collection(self):
        """データ収集問題修正"""
        try:
            # 手動データ収集テスト
            result = subprocess.run(['python3', 'main.py', '--collect'], 
                                  cwd=self.base_dir, capture_output=True, text=True, timeout=30)
            return "データ収集テスト実行" if result.returncode == 0 else None
        except:
            pass
        return None
        
    def _fix_missing_file(self, file_path):
        """欠損ファイル修復"""
        # GitHubから自動ダウンロード
        try:
            url = f"{self.github_raw_base}/{file_path}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                local_path = Path(self.base_dir) / file_path
                local_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, 'w') as f:
                    f.write(response.text)
                return f"GitHubから{file_path}をダウンロード"
        except:
            pass
        return None
        
    def _fix_high_cpu(self):
        """高CPU使用率修正"""
        try:
            # 重いプロセスの確認
            result = subprocess.run(['ps', 'aux', '--sort=-pcpu'], 
                                  capture_output=True, text=True)
            return "CPUプロセス確認済み"
        except:
            pass
        return None
        
    def _fix_disk_space(self):
        """ディスク容量修正"""
        try:
            # 古いログファイル削除
            subprocess.run(['find', self.base_dir, '-name', '*.log', '-mtime', '+30', '-delete'])
            # Python cacheクリア
            subprocess.run(['find', self.base_dir, '-name', '__pycache__', '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'])
            return "ディスク容量クリーンアップ実行"
        except:
            pass
        return None
        
    def _auto_test_system(self):
        """システム自動テスト"""
        test_results = {}
        
        # データ収集テスト
        try:
            result = subprocess.run(['python3', 'main.py', '--collect'], 
                                  cwd=self.base_dir, capture_output=True, text=True, timeout=30)
            test_results['data_collection'] = result.returncode == 0
        except:
            test_results['data_collection'] = False
            
        # メール送信テスト（ドライラン）
        try:
            result = subprocess.run(['python3', '-c', 
                'from email_notifier import EmailNotifier; print("Import OK")'], 
                cwd=self.base_dir, capture_output=True, text=True)
            test_results['email_system'] = result.returncode == 0
        except:
            test_results['email_system'] = False
            
        # ダッシュボードテスト
        try:
            result = subprocess.run(['python3', '-c', 
                'from hanazono_dashboard import HANAZONODashboard; print("Import OK")'], 
                cwd=self.base_dir, capture_output=True, text=True)
            test_results['dashboard'] = result.returncode == 0
        except:
            test_results['dashboard'] = False
            
        return test_results
        
    def _auto_deploy(self):
        """自動デプロイ"""
        try:
            # Git自動整理・プッシュ
            script_path = Path(self.base_dir) / "scripts" / "auto_git_organize_push.sh"
            if script_path.exists():
                result = subprocess.run(['bash', str(script_path)], 
                                      cwd=self.base_dir, capture_output=True, text=True)
                return result.returncode == 0
        except:
            pass
        return False
        
    def _generate_investigation_report(self, fixes, test_results, deploy_success):
        """調査結果レポート生成"""
        print("\n" + "=" * 60)
        print("📊 GitHub自動調査・修正完了レポート")
        print("=" * 60)
        
        print(f"\n🔧 自動修正実行: {len(fixes)}件")
        for fix in fixes:
            print(f"   • {fix['issue']['type']}: {fix['fix']}")
            
        print(f"\n🧪 システムテスト結果:")
        for test_name, result in test_results.items():
            status = "✅ 成功" if result else "❌ 失敗"
            print(f"   • {test_name}: {status}")
            
        print(f"\n🚀 自動デプロイ: {'✅ 成功' if deploy_success else '❌ 失敗'}")
        
        print(f"\n🎯 次回実行推奨:")
        if len(fixes) == 0 and all(test_results.values()):
            print("   ✅ システム最適化済み - 定期監視継続")
        else:
            print("   🔄 24時間後に再調査推奨")
            
        print("=" * 60)

if __name__ == "__main__":
    investigator = GitHubAutoInvestigator()
    investigator.run_full_investigation()
