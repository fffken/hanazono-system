#!/usr/bin/env python3
"""
Hanazono System Analysis Script - Non-Destructive Investigation
目的: hanazono_auto_master.sh の機能・役割・問題箇所を非破壊的に分析
原則: 読み取り専用、システムへの影響ゼロ、理解優先
作成: 一時使用目的（分析完了後削除）
"""

import os
import subprocess
import sys
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def run_command(cmd, description="", ignore_error=True):
    print(f"🔍 {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            print(f"Output:\n{result.stdout.strip()}")
        if result.stderr.strip() and not ignore_error:
            print(f"Error:\n{result.stderr.strip()}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False, "", str(e)

def safe_read_file(filepath, description=""):
    """ファイルを安全に読み取り専用で確認"""
    print(f"📖 {description}: {filepath}")
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"📄 ファイルサイズ: {len(content)} 文字")
                print(f"📄 内容:\n{'-'*40}")
                print(content[:2000])  # 最初の2000文字のみ表示
                if len(content) > 2000:
                    print(f"\n... (残り {len(content)-2000} 文字)")
                print(f"{'-'*40}")
                return content
        else:
            print(f"⚠️ ファイルが存在しません: {filepath}")
            return None
    except Exception as e:
        print(f"❌ 読み取りエラー: {e}")
        return None

def analyze_script_purpose(content):
    """スクリプトの目的・機能を分析"""
    print(f"\n🧠 スクリプト機能分析:")
    
    if not content:
        print("❌ 分析対象なし")
        return
    
    # キーワード分析
    keywords = {
        'venv': content.count('venv'),
        'pip': content.count('pip'),
        'python': content.count('python'),
        'install': content.count('install'),
        'activate': content.count('activate'),
        'rm -rf': content.count('rm -rf'),
        'sleep': content.count('sleep'),
        'while': content.count('while'),
        'cron': content.count('cron'),
        'loop': content.count('loop')
    }
    
    print("📊 キーワード出現回数:")
    for keyword, count in keywords.items():
        if count > 0:
            print(f"  - {keyword}: {count}回")
    
    # 危険操作の確認
    dangerous_ops = ['rm -rf', 'sudo rm', 'format', 'delete']
    found_dangerous = [op for op in dangerous_ops if op in content]
    
    if found_dangerous:
        print(f"⚠️ 注意が必要な操作: {found_dangerous}")
    else:
        print("✅ 危険な操作は検出されませんでした")

def main():
    print(f"🔍 HANAZONO システム分析 - 非破壊的調査")
    print(f"Time: {datetime.now()}")
    print(f"目的: システムの理解・問題特定・改善提案")
    
    print_section("Phase 1: 現在の稼働状況確認")
    
    # プロセス確認（読み取り専用）
    success, output, _ = run_command(
        "ps aux | grep hanazono | grep -v grep",
        "稼働プロセス確認"
    )
    
    if "hanazono_auto_master.sh" in output:
        print("📊 稼働状況: ACTIVE")
        # プロセス詳細確認
        run_command("ps -fp $(pgrep -f hanazono)", "プロセス詳細情報")
    else:
        print("📊 稼働状況: STOPPED")
    
    print_section("Phase 2: スクリプトファイル分析")
    
    # 現在のスクリプト確認
    hanazono_files = [
        "hanazono_auto_master.sh",
        "hanazono_auto_master.sh.DISABLED_1825",
        "start_persistent_ultimate.sh"
    ]
    
    for filename in hanazono_files:
        if os.path.exists(filename):
            content = safe_read_file(filename, f"HANAZONOスクリプト分析")
            if content:
                analyze_script_purpose(content)
    
    print_section("Phase 3: システム設定確認")
    
    # cron設定確認
    run_command("crontab -l", "ユーザーcron確認")
    
    # systemd確認
    run_command("systemctl --user list-units | grep -i hanazono", "ユーザーサービス確認")
    
    # 起動スクリプト確認
    run_command("grep -r hanazono /etc/rc* 2>/dev/null", "システム起動スクリプト確認")
    
    print_section("Phase 4: 環境への影響分析")
    
    # venv状態確認
    if os.path.exists("venv"):
        print("📁 現在のvenv状態:")
        run_command("ls -la venv/", "venv構造確認")
        run_command("venv/bin/pip list", "インストール済みパッケージ確認")
    
    # ログファイル確認
    log_files = ["hanazono.log", "hanazono_kill.log", "error.log"]
    for log_file in log_files:
        if os.path.exists(log_file):
            safe_read_file(log_file, "ログファイル確認")
    
    print_section("Phase 5: 問題箇所特定・改善提案")
    
    print("🎯 分析結果サマリー:")
    print("1. システムの本来の目的・役割")
    print("2. 現在発生している問題")
    print("3. 問題の根本原因")
    print("4. 非破壊的改善案")
    print("5. 復旧・再開手順")
    
    print(f"\n📋 次のステップ:")
    print("1. 分析結果の確認・検討")
    print("2. 必要に応じた設定調整案の作成")
    print("3. テスト環境での検証")
    print("4. 段階的復旧実行")
    print("5. 正常稼働の確認")
    
    print(f"\n🛡️ 非破壊的原則遵守:")
    print("✅ 読み取り専用操作")
    print("✅ システムへの影響ゼロ")
    print("✅ 理解・改善優先")
    print("✅ 協調的アプローチ")

if __name__ == "__main__":
    main()
