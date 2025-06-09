#!/usr/bin/env python3
"""
Past Email Recovery Search Script
目的: 6月5日〜7日の最終進化版メール内容・設定を検索
原則: 読み取り専用・非破壊的・即座削除対象
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def search_email_content_in_logs():
    """ログファイルから過去のメール内容検索"""
    print("📧 ログファイルからメール内容検索...")
    
    log_patterns = [
        "logs/*.log",
        "logs/cron.log*",
        "logs/email*.log*"
    ]
    
    target_keywords = [
        "1年前比較バトル",
        "HANAZONOシステム効果", 
        "24時間蓄電量変化",
        "HTML時はグラフ表示",
        "グラフ表示"
    ]
    
    found_content = []
    
    for pattern in log_patterns:
        for log_file in Path(".").glob(pattern):
            if log_file.is_file():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 6月5日〜7日のメール関連内容検索
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if any(keyword in line for keyword in target_keywords):
                            found_content.append({
                                "file": str(log_file),
                                "line": i + 1,
                                "content": line.strip(),
                                "context": lines[max(0, i-2):i+3]  # 前後2行
                            })
                            
                except Exception as e:
                    print(f"   ❌ {log_file} 読み取りエラー: {e}")
    
    return found_content

def search_email_templates():
    """メールテンプレート・設定ファイル検索"""
    print("📧 メールテンプレート・設定検索...")
    
    # バックアップファイル検索
    backup_patterns = [
        "email_notifier*backup*.py",
        "email_notifier*20250605*.py",
        "email_notifier*20250606*.py", 
        "email_notifier*20250607*.py",
        "settings*backup*.json",
        "settings*20250605*.json"
    ]
    
    found_files = []
    
    for pattern in backup_patterns:
        for file in Path(".").glob(pattern):
            if file.is_file():
                stat = file.stat()
                found_files.append({
                    "path": str(file),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
    
    # 日付でソート
    found_files.sort(key=lambda x: x["modified"], reverse=True)
    
    return found_files

def search_settings_in_files():
    """ファイル内からSMTP設定検索"""
    print("📧 ファイル内SMTP設定検索...")
    
    search_files = [
        "email_notifier_v2_1.py",
        "email_capsule.py",
        "main.py"
    ] + [str(f) for f in Path(".").glob("email_notifier*.py")]
    
    smtp_settings = []
    
    for file_path in search_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # SMTP設定パターン検索
                smtp_patterns = [
                    r'smtp_server.*?=.*?["\']([^"\']+)["\']',
                    r'smtp_port.*?=.*?(\d+)',
                    r'sender_email.*?=.*?["\']([^"\']+)["\']',
                    r'receiver_email.*?=.*?["\']([^"\']+)["\']'
                ]
                
                found_settings = {}
                for pattern in smtp_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        key = pattern.split('.*?')[0]
                        found_settings[key] = matches[0]
                
                if found_settings:
                    smtp_settings.append({
                        "file": file_path,
                        "settings": found_settings
                    })
                    
            except Exception as e:
                print(f"   ❌ {file_path} 検索エラー: {e}")
    
    return smtp_settings

def analyze_current_email_notifier():
    """現在のemail_notifier_v2_1.py分析"""
    print("📧 現在のemail_notifier_v2_1.py分析...")
    
    if Path("email_notifier_v2_1.py").exists():
        try:
            with open("email_notifier_v2_1.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # __init__メソッドの引数確認
            init_match = re.search(r'def __init__\(([^)]+)\)', content)
            if init_match:
                init_args = init_match.group(1)
                print(f"   📋 __init__引数: {init_args}")
            
            # メール内容生成メソッド確認
            if "1年前比較バトル" in content:
                print("   ✅ 1年前比較バトル: 含まれている")
            else:
                print("   ❌ 1年前比較バトル: 含まれていない")
                
            if "24時間蓄電量変化" in content:
                print("   ✅ 24時間蓄電量変化: 含まれている")
            else:
                print("   ❌ 24時間蓄電量変化: 含まれていない")
            
            return content
            
        except Exception as e:
            print(f"   ❌ 分析エラー: {e}")
            return None
    else:
        print("   ❌ ファイル不存在")
        return None

def main():
    print("📧 Past Email Recovery Search")
    print(f"実行時刻: {datetime.now()}")
    print("目的: 6月5日〜7日の最終進化版メール内容・設定を検索")
    
    print("\n" + "="*60)
    print(" Phase 1: ログファイルからメール内容検索")
    print("="*60)
    found_content = search_email_content_in_logs()
    
    if found_content:
        print(f"📊 発見件数: {len(found_content)}件")
        for item in found_content[:5]:  # 最初の5件表示
            print(f"   📄 {item['file']}:{item['line']}")
            print(f"      {item['content'][:100]}...")
    else:
        print("⚠️ ログ内にメール内容なし")
    
    print("\n" + "="*60)
    print(" Phase 2: メールテンプレート・設定検索")
    print("="*60)
    found_files = search_email_templates()
    
    if found_files:
        print(f"📊 発見ファイル: {len(found_files)}個")
        for file in found_files[:10]:  # 最初の10個表示
            print(f"   📄 {file['path']}")
            print(f"      サイズ: {file['size']:,}バイト, 更新: {file['modified']}")
    else:
        print("⚠️ バックアップファイルなし")
    
    print("\n" + "="*60)
    print(" Phase 3: ファイル内SMTP設定検索")
    print("="*60)
    smtp_settings = search_settings_in_files()
    
    if smtp_settings:
        print(f"📊 設定発見: {len(smtp_settings)}ファイル")
        for setting in smtp_settings:
            print(f"   📄 {setting['file']}:")
            for key, value in setting['settings'].items():
                print(f"      {key}: {value}")
    else:
        print("⚠️ SMTP設定なし")
    
    print("\n" + "="*60)
    print(" Phase 4: 現在のemail_notifier分析")
    print("="*60)
    current_content = analyze_current_email_notifier()
    
    print("\n" + "="*60)
    print(" 🎯 検索結果まとめ")
    print("="*60)
    print("📋 次のステップ:")
    
    if found_files:
        print("1. 最新バックアップファイルの内容確認")
        print("2. 最終進化版コードの復旧")
    
    if smtp_settings:
        print("3. SMTP設定の復元")
    
    print("4. コード互換性修復")
    print("5. プレビュー確認・テスト送信")

if __name__ == "__main__":
    main()
