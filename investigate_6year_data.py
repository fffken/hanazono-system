#!/usr/bin/env python3
# 6年分データ徹底調査（完全非破壊的）
import datetime
import os
import glob
import json

def investigate_6year_data():
    """6年分データ徹底調査"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 6年分データ徹底調査開始 {timestamp}")
    print("=" * 70)
    
    # 1. 全データソース探索
    print(f"📁 全データソース探索:")
    
    # データ格納場所候補
    data_locations = [
        "data/",
        "historical_data/",
        "backup_data/", 
        "archive/",
        "6year_data/",
        "past_data/",
        "github_data/",
        "./",
        "../"
    ]
    
    found_data = {}
    
    for location in data_locations:
        if os.path.exists(location):
            print(f"  📂 {location}: 存在確認")
            
            # JSON、CSV、SQLiteファイル探索
            patterns = ["*.json", "*.csv", "*.db", "*.sqlite", "*historical*", "*6year*"]
            
            for pattern in patterns:
                files = glob.glob(os.path.join(location, pattern))
                if files:
                    found_data[location] = found_data.get(location, []) + files
        else:
            print(f"  ❌ {location}: 未発見")
    
    # 2. 発見されたデータファイル詳細分析
    print(f"\n📊 発見データファイル詳細分析:")
    
    total_files = 0
    total_size = 0
    oldest_date = None
    newest_date = None
    
    for location, files in found_data.items():
        print(f"\n📂 {location}:")
        location_files = len(files)
        location_size = 0
        
        for file_path in files[:10]:  # 最初の10個を詳細確認
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                mtime_date = datetime.datetime.fromtimestamp(mtime)
                
                location_size += file_size
                total_files += 1
                total_size += file_size
                
                if oldest_date is None or mtime_date < oldest_date:
                    oldest_date = mtime_date
                if newest_date is None or mtime_date > newest_date:
                    newest_date = mtime_date
                
                print(f"    📄 {os.path.basename(file_path)}: {file_size:,}バイト ({mtime_date.strftime('%Y-%m-%d')})")
        
        if location_files > 10:
            print(f"    ... 他{location_files - 10}個")
        
        print(f"    📊 小計: {location_files}ファイル, {location_size:,}バイト")
    
    # 3. 歴史データ期間確認
    print(f"\n📅 歴史データ期間確認:")
    if oldest_date and newest_date:
        duration = (newest_date - oldest_date).days
        duration_years = duration / 365.25
        
        print(f"  📊 最古データ: {oldest_date.strftime('%Y-%m-%d')}")
        print(f"  📊 最新データ: {newest_date.strftime('%Y-%m-%d')}")
        print(f"  📊 データ期間: {duration}日間 ({duration_years:.1f}年)")
        print(f"  📊 総ファイル数: {total_files}")
        print(f"  📊 総データ量: {total_size:,}バイト")
        
        if duration_years >= 5:
            print(f"  🎉 6年分相当データ発見！")
        else:
            print(f"  ⚠️ 6年分データ不足: {duration_years:.1f}年分のみ")
    else:
        print(f"  ❌ データ期間特定不可")
    
    # 4. GitHub・外部データ探索
    print(f"\n🔍 GitHub・外部データ探索:")
    
    # GitHub関連ファイル確認
    github_patterns = [
        "*github*",
        "*git*",
        "*.git",
        "README*",
        "*history*",
        "*backup*"
    ]
    
    github_files = []
    for pattern in github_patterns:
        github_files.extend(glob.glob(pattern))
    
    if github_files:
        print(f"  📂 GitHub関連ファイル:")
        for gfile in github_files[:5]:
            print(f"    📄 {gfile}")
    else:
        print(f"  ❌ GitHub関連ファイル未発見")
    
    # 5. SQLiteデータベース確認
    print(f"\n🗄️ SQLiteデータベース確認:")
    db_files = glob.glob("*.db") + glob.glob("*.sqlite") + glob.glob("*/*.db") + glob.glob("*/*.sqlite")
    
    if db_files:
        for db_file in db_files:
            if os.path.exists(db_file):
                db_size = os.path.getsize(db_file)
                print(f"  📊 {db_file}: {db_size:,}バイト")
                
                # SQLiteテーブル確認
                try:
                    import sqlite3
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    
                    if tables:
                        print(f"    📋 テーブル: {[t[0] for t in tables]}")
                    else:
                        print(f"    ❌ テーブルなし")
                except Exception as e:
                    print(f"    ❌ DB確認エラー: {e}")
    else:
        print(f"  ❌ SQLiteデータベース未発見")
    
    # 6. 機械学習システムのデータパス確認
    print(f"\n🤖 機械学習システムデータパス確認:")
    
    ml_file = "hanazono_ml_enhancement_20250617_234033.py"
    if os.path.exists(ml_file):
        try:
            with open(ml_file, 'r', encoding='utf-8') as f:
                ml_content = f.read()
            
            # データパス検索
            data_paths = []
            lines = ml_content.split('\n')
            for line in lines:
                if 'data' in line.lower() and ('.json' in line or '.csv' in line or '.db' in line):
                    data_paths.append(line.strip())
            
            if data_paths:
                print(f"  📋 ML設定データパス:")
                for path in data_paths[:5]:
                    print(f"    {path}")
            else:
                print(f"  ❌ MLデータパス未確認")
                
        except Exception as e:
            print(f"  ❌ ML確認エラー: {e}")
    
    # 7. 推奨解決策
    print(f"\n" + "=" * 70)
    print(f"🎯 6年分データ活用解決策:")
    print(f"=" * 70)
    
    if duration_years >= 5 if 'duration_years' in locals() else False:
        print(f"✅ 解決策: 既存データをML系に統合")
        solutions = [
            "機械学習システムのデータパス修正",
            "歴史データの統一フォーマット変換",
            "MLシステムによる6年分データ分析実行"
        ]
    else:
        print(f"🔍 解決策: 6年分データ所在特定")
        solutions = [
            "GitHub履歴からのデータ復旧",
            "バックアップシステムからの復元",
            "外部ストレージからのデータ取得",
            "手動データ統合作業"
        ]
    
    for i, solution in enumerate(solutions, 1):
        print(f"   {i}. {solution}")
    
    return {
        "total_files": total_files,
        "duration_years": duration_years if 'duration_years' in locals() else 0,
        "data_locations": list(found_data.keys()),
        "needs_data_integration": duration_years < 5 if 'duration_years' in locals() else True
    }

if __name__ == "__main__":
    investigate_6year_data()
