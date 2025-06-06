#!/usr/bin/env python3
"""
GitHub自動読み込みシステム v2.0
HANAZONOソーラー蓄電システム用
"""

import os
import sys
import requests
import base64
import json
from pathlib import Path
import subprocess
import time

# 設定
GITHUB_USER = "fffken"
GITHUB_REPO = "hanazono-system"
DEFAULT_BRANCH = "main"
CONFIG_FILE = "github_access.json"

def load_config():
    """設定ファイルを読み込む"""
    config_path = Path(CONFIG_FILE)
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "token": os.environ.get("GITHUB_TOKEN", ""),
        "last_sync": "",
        "cached_files": {}
    }

def save_config(config):
    """設定ファイルを保存する"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def fetch_github_content(path, branch=DEFAULT_BRANCH):
    """
    GitHubから直接コンテンツを取得する関数
    
    Args:
        path: ファイルパス
        branch: ブランチ名
        
    Returns:
        ファイルコンテンツ（文字列）
    """
    config = load_config()
    github_token = config.get("token", "")
    repo = f"{GITHUB_USER}/{GITHUB_REPO}"
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            content = response.json()
            if content.get("encoding") == "base64":
                return base64.b64decode(content["content"]).decode('utf-8')
            else:
                return content["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_github_content(path, branch=DEFAULT_BRANCH, use_cache=True):
    """
    複数の方法を試して確実にGitHubコンテンツを取得する
    
    Args:
        path: ファイルパス
        branch: ブランチ名
        use_cache: キャッシュを使用するかどうか
    
    Returns:
        ファイルコンテンツ（文字列）
    """
    config = load_config()
    
    # キャッシュをチェック
    if use_cache and path in config["cached_files"]:
        print(f"✅ キャッシュからファイルを読み込みました: {path}")
        return config["cached_files"][path]
    
    # 方法1: GitHub API
    content = fetch_github_content(path, branch)
    if not content.startswith("Error"):
        # キャッシュに保存
        config["cached_files"][path] = content
        save_config(config)
        print(f"✅ GitHub APIからファイルを取得しました: {path}")
        return content
    
    # 方法2: Raw URL直接アクセス
    repo = f"{GITHUB_USER}/{GITHUB_REPO}"
    raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    try:
        response = requests.get(raw_url)
        if response.status_code == 200:
            content = response.text
            # キャッシュに保存
            config["cached_files"][path] = content
            save_config(config)
            print(f"✅ Raw URLからファイルを取得しました: {path}")
            return content
    except Exception:
        pass
    
    print(f"❌ ファイル取得失敗: {path}")
    return f"すべての方法が失敗しました。リポジトリ設定を確認してください。"

def check_github_access():
    """GitHub接続テスト"""
    test_file = "README.md"  # 通常存在するファイル
    
    content = get_github_content(test_file, use_cache=False)
    if content.startswith("Error") or "失敗" in content:
        print("⚠️ GitHubアクセス設定に問題があります")
        print("1. 環境変数 GITHUB_TOKEN を設定してください")
        print("2. リポジトリが存在し、アクセス可能か確認してください")
        return False
    else:
        print("✅ GitHub接続テスト成功")
        return True

def fetch_multiple_files(file_paths):
    """
    複数のファイルを取得してまとめて返す
    
    Args:
        file_paths: ファイルパスのリスト
    
    Returns:
        ファイル内容の辞書 {パス: 内容}
    """
    results = {}
    for path in file_paths:
        content = get_github_content(path)
        results[path] = content
    return results

def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python github_access_system.py <コマンド> [引数...]")
        print("コマンド:")
        print("  test       - GitHub接続テスト")
        print("  get <path> - 指定したファイルを取得")
        print("  setup      - 初期設定")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        check_github_access()
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("ファイルパスを指定してください")
            return
        path = sys.argv[2]
        content = get_github_content(path)
        print(content)
    
    elif command == "setup":
        token = input("GitHub APIトークンを入力してください: ")
        config = load_config()
        config["token"] = token
        save_config(config)
        print("✅ 設定を保存しました")
        check_github_access()

if __name__ == "__main__":
    main()
