#!/usr/bin/env python3
# format_battle_section 徹底検索（完全非破壊的）
import os
import glob
import re

def thorough_search_format_battle():
    """format_battle_section 徹底検索"""
    print("🔍 format_battle_section 徹底検索開始")
    print("=" * 70)
    
    # 1. 全Pythonファイル検索
    python_files = glob.glob("*.py")
    print(f"📁 検索対象Pythonファイル: {len(python_files)}個")
    
    # 2. 検索パターン定義
    search_patterns = [
        r"def format_battle_section",
        r"format_battle_section",
        r"def.*battle.*section",
        r"battle.*section",
        r"format.*battle",
        r"def format_.*battle",
        r"class.*Battle.*",
        r"BattleNews"
    ]
    
    found_results = {}
    
    # 3. 各ファイルを詳細検索
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            file_results = []
            
            # 各パターンで検索
            for pattern in search_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # 該当行番号を特定
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = lines[line_num - 1].strip()
                    
                    file_results.append({
                        'pattern': pattern,
                        'line_num': line_num,
                        'line_content': line_content,
                        'match': match.group()
                    })
            
            if file_results:
                found_results[file_path] = file_results
                
        except Exception as e:
            print(f"⚠️ {file_path} 読み取りエラー: {e}")
    
    # 4. 検索結果詳細表示
    print(f"\n🔍 詳細検索結果:")
    
    if found_results:
        for file_path, results in found_results.items():
            print(f"\n📄 {file_path}:")
            file_size = os.path.getsize(file_path)
            print(f"  サイズ: {file_size}バイト")
            
            for result in results:
                print(f"  行{result['line_num']}: {result['pattern']}")
                print(f"    → {result['line_content']}")
                print(f"    マッチ: '{result['match']}'")
    else:
        print("❌ format_battle_section関連の定義は見つかりませんでした")
    
    # 5. 特に詳しく調べるべきファイル特定
    suspicious_files = []
    for file_path in python_files:
        if any(keyword in file_path.lower() for keyword in ['battle', 'integration', 'mail', 'format']):
            suspicious_files.append(file_path)
    
    print(f"\n🎯 バトル・統合関連ファイル詳細調査:")
    for file_path in suspicious_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"  📄 {file_path}: {file_size}バイト ({mtime_str})")
            
            # ファイル内容の関数一覧
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 関数定義を抽出
                function_matches = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                if function_matches:
                    print(f"    関数: {', '.join(function_matches[:10])}")  # 最初の10個
                    if len(function_matches) > 10:
                        print(f"    ... 他{len(function_matches) - 10}個")
                
                # クラス定義を抽出
                class_matches = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                if class_matches:
                    print(f"    クラス: {', '.join(class_matches)}")
                
            except Exception as e:
                print(f"    ❌ 読み取りエラー: {e}")
    
    # 6. 最新のバトル関連ファイル特定
    print(f"\n🕐 最新更新ファイル（バトル関連）:")
    recent_files = []
    
    for file_path in python_files:
        if any(keyword in file_path.lower() for keyword in ['battle', 'integration', 'format', 'mail']) or any(keyword in file_path for keyword in ['20250617', '20250616']):
            if os.path.exists(file_path):
                mtime = os.path.getmtime(file_path)
                recent_files.append((file_path, mtime))
    
    # 更新時刻順でソート
    recent_files.sort(key=lambda x: x[1], reverse=True)
    
    for file_path, mtime in recent_files[:5]:  # 最新5個
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_size = os.path.getsize(file_path)
        print(f"  📄 {file_path}: {file_size}バイト ({mtime_str})")
    
    return found_results

if __name__ == "__main__":
    import datetime
    thorough_search_format_battle()
