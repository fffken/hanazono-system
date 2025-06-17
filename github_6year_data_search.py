#!/usr/bin/env python3
# GitHub6年分データ探索（完全非破壊的）
import datetime
import os
import subprocess
import json

def github_6year_data_search():
    """GitHub6年分データ探索"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 GitHub6年分データ探索開始 {timestamp}")
    print("=" * 70)
    
    github_url = "https://github.com/fffken/hanazono-system"
    
    # 1. GitHub認証情報確認
    print(f"🔐 GitHub認証情報確認:")
    
    github_config_file = "github_access.json"
    if os.path.exists(github_config_file):
        try:
            with open(github_config_file, 'r', encoding='utf-8') as f:
                github_config = json.load(f)
            
            print(f"  ✅ GitHub設定ファイル確認: {github_config_file}")
            
            # 設定内容確認（セキュア）
            if 'token' in github_config:
                token_preview = github_config['token'][:10] + "..." if len(github_config['token']) > 10 else "設定済み"
                print(f"  🔑 トークン: {token_preview}")
            
            if 'repository' in github_config:
                print(f"  📂 リポジトリ: {github_config['repository']}")
                
        except Exception as e:
            print(f"  ❌ GitHub設定読み取りエラー: {e}")
    else:
        print(f"  ⚠️ GitHub設定ファイル未発見")
    
    # 2. ローカルGitリポジトリ確認
    print(f"\n📂 ローカルGitリポジトリ確認:")
    
    try:
        # Git status確認
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Gitリポジトリ確認済み")
            
            # リモートURL確認
            remote_result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'hanazono-system' in remote_result.stdout:
                print(f"  ✅ hanazono-systemリポジトリ接続確認")
            else:
                print(f"  ⚠️ hanazono-systemリポジトリ未接続")
                
        else:
            print(f"  ❌ Gitリポジトリ未初期化")
            
    except Exception as e:
        print(f"  ❌ Git確認エラー: {e}")
    
    # 3. GitHub API経由でのデータ探索
    print(f"\n🌐 GitHub API データ探索:")
    
    try:
        import requests
        
        # GitHub API でファイル一覧取得
        api_url = "https://api.github.com/repos/fffken/hanazono-system/contents"
        
        # 認証ヘッダー準備
        headers = {}
        if os.path.exists(github_config_file):
            try:
                with open(github_config_file, 'r') as f:
                    config = json.load(f)
                if 'token' in config:
                    headers['Authorization'] = f"token {config['token']}"
            except:
                pass
        
        print(f"  🚀 GitHub API アクセス: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            files = response.json()
            print(f"  ✅ GitHub ファイル一覧取得成功: {len(files)}ファイル")
            
            # データファイル候補探索
            data_candidates = []
            for file_info in files:
                file_name = file_info['name']
                file_size = file_info.get('size', 0)
                
                # データファイル候補判定
                if any(keyword in file_name.lower() for keyword in [
                    'data', 'historical', '6year', 'database', 'backup', 'archive'
                ]):
                    data_candidates.append({
                        'name': file_name,
                        'size': file_size,
                        'type': file_info['type'],
                        'download_url': file_info.get('download_url', '')
                    })
            
            if data_candidates:
                print(f"  🎯 データファイル候補発見: {len(data_candidates)}個")
                for candidate in data_candidates:
                    print(f"    📄 {candidate['name']}: {candidate['size']:,}バイト ({candidate['type']})")
            else:
                print(f"  ⚠️ データファイル候補未発見")
                
        else:
            print(f"  ❌ GitHub API エラー: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"  ❌ GitHub API 接続エラー: {e}")
    except ImportError:
        print(f"  ❌ requests ライブラリ未インストール")
    
    # 4. Git履歴からの大型ファイル探索
    print(f"\n📚 Git履歴大型ファイル探索:")
    
    try:
        # Git log で大型ファイルのコミット履歴確認
        log_result = subprocess.run([
            'git', 'log', '--name-only', '--oneline', '--since=6.years.ago'
        ], capture_output=True, text=True, timeout=15)
        
        if log_result.returncode == 0:
            log_lines = log_result.stdout.split('\n')
            
            # データファイル関連のコミット抽出
            data_commits = []
            for line in log_lines:
                if any(keyword in line.lower() for keyword in [
                    'data', 'db', '.json', '.csv', 'historical', 'backup'
                ]):
                    data_commits.append(line)
            
            if data_commits:
                print(f"  📋 データ関連コミット: {len(data_commits)}個")
                for commit in data_commits[:10]:  # 最初の10個
                    print(f"    📝 {commit}")
            else:
                print(f"  ⚠️ データ関連コミット未発見")
        else:
            print(f"  ❌ Git log エラー")
            
    except Exception as e:
        print(f"  ❌ Git履歴確認エラー: {e}")
    
    # 5. 推奨データ取得アクション
    print(f"\n" + "=" * 70)
    print(f"🎯 6年分データ取得推奨アクション:")
    print(f"=" * 70)
    
    if 'data_candidates' in locals() and data_candidates:
        print(f"🚀 GitHub直接ダウンロード推奨")
        actions = [
            "GitHub候補ファイルの詳細確認",
            "大型データファイルの選択的ダウンロード",
            "ローカル統合・機械学習システム連携"
        ]
    else:
        print(f"🔍 GitHub詳細探索継続")
        actions = [
            "GitHub全ディレクトリの再帰的探索",
            "Git LFS 大型ファイル確認",
            "コミット履歴からのデータファイル復元"
        ]
    
    for i, action in enumerate(actions, 1):
        print(f"   {i}. {action}")
    
    return {
        "github_accessible": response.status_code == 200 if 'response' in locals() else False,
        "data_candidates": data_candidates if 'data_candidates' in locals() else [],
        "git_available": True
    }

if __name__ == "__main__":
    github_6year_data_search()
