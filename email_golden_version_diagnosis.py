#!/usr/bin/env python3
"""
Email Golden Version Diagnosis Script
目的: email_notifier_v2_1.py黄金バージョン不一致問題の詳細診断
原則: 読み取り専用・非破壊的・即座削除対象
"""

import os
import json
from pathlib import Path
from datetime import datetime

def find_email_versions():
    """システム内の全email_notifierバージョンを検索"""
    versions = []
    
    # 検索パターン
    patterns = [
        "email_notifier*.py",
        "**/email_notifier*.py",
        "**/*email*.py"
    ]
    
    search_paths = [
        Path("."),
        Path("system_backups"),
        Path("ai_memory"),
        Path("kioku_backup_*")
    ]
    
    for search_path in search_paths:
        if search_path.exists():
            for pattern in patterns:
                for file in search_path.rglob(pattern):
                    if file.is_file():
                        stat = file.stat()
                        versions.append({
                            "path": str(file),
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        })
    
    return versions

def analyze_kioku_expectation():
    """kiokuシステムの期待値を確認"""
    expectation = {}
    
    # ai_memory内の記録確認
    golden_versions_file = Path("ai_memory/storage/permanent/golden_versions.json")
    if golden_versions_file.exists():
        with open(golden_versions_file, 'r') as f:
            golden_data = json.load(f)
        
        for file, info in golden_data.items():
            if "email_notifier_v2_1.py" in file:
                expectation["golden_record"] = {
                    "expected_size": info.get("size"),
                    "version": info.get("version"),
                    "recorded_path": file
                }
    
    return expectation

def compare_content_structure():
    """現在ファイルの内容構造分析"""
    current_file = Path("email_notifier_v2_1.py")
    
    if not current_file.exists():
        return {"error": "ファイル不存在"}
    
    with open(current_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    analysis = {
        "total_lines": len(content.splitlines()),
        "total_chars": len(content),
        "functions": content.count("def "),
        "classes": content.count("class "),
        "imports": content.count("import "),
        "comments": content.count("#"),
        "docstrings": content.count('"""'),
        "has_main": "__main__" in content,
        "last_100_chars": content[-100:] if len(content) >= 100 else content
    }
    
    return analysis

def main():
    print("🔍 Email Golden Version Diagnosis")
    print(f"実行時刻: {datetime.now()}")
    print("目的: email_notifier_v2_1.py黄金バージョン不一致問題の詳細診断")
    
    print("\n" + "="*60)
    print(" Phase 1: 全email_notifierバージョン検索")
    print("="*60)
    
    versions = find_email_versions()
    print(f"📊 発見されたバージョン: {len(versions)}個")
    
    # サイズ別ソート
    versions.sort(key=lambda x: x["size"], reverse=True)
    
    target_size = 26331
    current_size = 25792
    
    print(f"\n🎯 期待サイズ: {target_size}バイト")
    print(f"🔍 現在サイズ: {current_size}バイト")
    print(f"📊 差分: {target_size - current_size}バイト不足")
    
    print(f"\n📋 発見されたバージョン一覧:")
    for i, version in enumerate(versions[:10], 1):  # 上位10個表示
        size_status = ""
        if version["size"] == target_size:
            size_status = " ⭐ 期待サイズ一致!"
        elif version["size"] == current_size:
            size_status = " 📍 現在と同サイズ"
        
        print(f"   {i:2d}. {version['path']}")
        print(f"       サイズ: {version['size']:,}バイト{size_status}")
        print(f"       更新日: {version['modified']}")
    
    print("\n" + "="*60)
    print(" Phase 2: kioku期待値確認")
    print("="*60)
    
    expectation = analyze_kioku_expectation()
    if expectation:
        print("📊 kiokuシステム記録:")
        for key, value in expectation.items():
            print(f"   {key}: {value}")
    else:
        print("⚠️ kioku記録データなし")
    
    print("\n" + "="*60)
    print(" Phase 3: 現在ファイル構造分析")
    print("="*60)
    
    structure = compare_content_structure()
    print("📊 現在ファイル分析:")
    for key, value in structure.items():
        if key != "last_100_chars":
            print(f"   {key}: {value}")
    
    print(f"\n📄 ファイル末尾100文字:")
    print(f"   {repr(structure.get('last_100_chars', ''))}")
    
    print("\n" + "="*60)
    print(" 🎯 診断結果・推奨アクション")
    print("="*60)
    
    # 期待サイズのファイルがあるかチェック
    matching_versions = [v for v in versions if v["size"] == target_size]
    
    if matching_versions:
        print(f"✅ 期待サイズ({target_size}バイト)のファイル発見: {len(matching_versions)}個")
        print("📋 推奨アクション:")
        print("1. 期待サイズファイルの内容確認")
        print("2. 現在ファイルとの差分確認")
        print("3. 必要に応じて黄金バージョン復旧")
        
        for match in matching_versions[:3]:  # 上位3個
            print(f"\n🎯 候補: {match['path']} ({match['modified']})")
    else:
        print(f"⚠️ 期待サイズ({target_size}バイト)のファイル未発見")
        print("📋 推奨アクション:")
        print("1. 現在ファイルが最新版として使用")
        print("2. kioku期待値の更新")
        print("3. 機能テストによる動作確認")

if __name__ == "__main__":
    main()
