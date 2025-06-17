#!/usr/bin/env python3
# 実装済み未活用モジュール発掘調査（完全非破壊的）
import datetime
import os
import glob
import re

def discover_ready_modules():
    """実装済み未活用モジュール発掘調査"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 実装済み未活用モジュール発掘調査開始 {timestamp}")
    print("=" * 70)
    
    # 1. 大型Pythonファイル詳細分析
    print(f"📊 大型実装済みモジュール分析:")
    print(f"=" * 50)
    
    large_files = []
    py_files = glob.glob("*.py")
    
    for py_file in py_files:
        file_size = os.path.getsize(py_file)
        if file_size > 5000:  # 5KB以上の大型ファイル
            large_files.append((py_file, file_size))
    
    # サイズ順でソート
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    discovered_modules = {}
    
    for file_path, file_size in large_files[:15]:  # 上位15個
        print(f"\n📄 {file_path} ({file_size:,}バイト)")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # クラス・関数・機能分析
            classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
            
            # 特定機能キーワード検索
            feature_keywords = {
                "メール送信": ["smtp", "send_email", "mail", "MIMEText"],
                "天気予報": ["weather", "forecast", "temperature", "天気"],
                "バトル機能": ["battle", "比較", "削減", "judgment"],
                "データ収集": ["collect", "data", "json", "parameters"],
                "アラート": ["alert", "warning", "緊急", "notification"],
                "レポート": ["report", "weekly", "monthly", "summary"],
                "自動制御": ["auto", "control", "setting", "adjust"],
                "UI/Web": ["html", "css", "web", "dashboard", "interface"],
                "API連携": ["api", "requests", "http", "webhook"],
                "ゲーム": ["game", "point", "score", "rank", "badge"],
                "AI/ML": ["tensorflow", "pytorch", "machine", "learning", "predict"],
                "監視": ["monitor", "log", "check", "status", "health"]
            }
            
            detected_features = {}
            for feature, keywords in feature_keywords.items():
                matches = sum(1 for keyword in keywords if keyword.lower() in content.lower())
                if matches > 0:
                    detected_features[feature] = matches
            
            # 完成度評価
            completion_indicators = [
                "if __name__ == \"__main__\":",
                "def main(",
                "def run_",
                "class.*System",
                "class.*Manager",
                "import.*完成"
            ]
            
            completion_score = sum(1 for indicator in completion_indicators 
                                 if re.search(indicator, content))
            
            # 実装状況判定
            if len(classes) > 0 and len(functions) > 5 and completion_score > 1:
                implementation_status = "🟢 ほぼ完成"
            elif len(functions) > 3 and completion_score > 0:
                implementation_status = "🟡 実装中"
            else:
                implementation_status = "🔴 初期段階"
            
            print(f"  📋 クラス: {len(classes)}個 - {', '.join(classes[:3])}")
            print(f"  🔧 関数: {len(functions)}個 - {', '.join(functions[:5])}")
            print(f"  🎯 検出機能: {', '.join(detected_features.keys())}")
            print(f"  📊 状況: {implementation_status}")
            
            # 特に注目すべきファイル判定
            if (len(classes) > 0 and len(functions) > 8 and 
                len(detected_features) > 2 and completion_score > 1):
                
                print(f"  ⭐ 注目: 実装済み高機能モジュール！")
                
                discovered_modules[file_path] = {
                    "size": file_size,
                    "classes": classes,
                    "functions": functions,
                    "features": detected_features,
                    "completion": implementation_status,
                    "priority": "高"
                }
                
                # 詳細機能解析
                print(f"  🔍 詳細機能解析:")
                
                # メイン実行部分確認
                main_patterns = [
                    r'if __name__ == "__main__":(.*?)(?=\n\n|\Z)',
                    r'def main\([^)]*\):(.*?)(?=\ndef|\nclass|\Z)',
                    r'def run_[^(]*\([^)]*\):(.*?)(?=\ndef|\nclass|\Z)'
                ]
                
                for pattern in main_patterns:
                    matches = re.findall(pattern, content, re.DOTALL)
                    if matches:
                        main_code = matches[0][:200]  # 最初の200文字
                        print(f"    🚀 実行部分: {main_code.strip()[:100]}...")
                        break
        
        except Exception as e:
            print(f"  ❌ 分析エラー: {e}")
    
    # 2. 特定機能別の完成度の高いモジュール特定
    print(f"\n" + "=" * 70)
    print(f"🎯 機能別実装済みモジュール:")
    print(f"=" * 70)
    
    # 特に注目すべきファイル名パターン
    notable_patterns = [
        ("*email*", "メール関連"),
        ("*weather*", "天気関連"),
        ("*battle*", "バトル関連"),
        ("*report*", "レポート関連"),
        ("*alert*", "アラート関連"),
        ("*monitor*", "監視関連"),
        ("*control*", "制御関連"),
        ("*dashboard*", "ダッシュボード関連"),
        ("*api*", "API関連"),
        ("*game*", "ゲーム関連")
    ]
    
    for pattern, category in notable_patterns:
        matching_files = glob.glob(pattern + ".py")
        if matching_files:
            print(f"\n📁 {category}:")
            for file_path in matching_files:
                file_size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
                
                if file_size > 3000:  # 3KB以上
                    print(f"  🟢 {file_path}: {file_size:,}バイト ({mtime_str})")
                elif file_size > 1000:  # 1KB以上
                    print(f"  🟡 {file_path}: {file_size:,}バイト ({mtime_str})")
    
    # 3. 黄金バージョン・完成版ファイル探索
    print(f"\n🏆 完成版・黄金バージョン探索:")
    print(f"=" * 50)
    
    golden_patterns = [
        "*golden*",
        "*final*", 
        "*complete*",
        "*perfect*",
        "*ultimate*",
        "*enhanced*",
        "*working*",
        "*fixed*"
    ]
    
    golden_files = []
    for pattern in golden_patterns:
        golden_files.extend(glob.glob(pattern + "*.py"))
    
    # 重複除去とサイズフィルタ
    golden_files = list(set(golden_files))
    golden_files = [f for f in golden_files if os.path.getsize(f) > 5000]
    golden_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
    
    for file_path in golden_files[:10]:  # 上位10個
        file_size = os.path.getsize(file_path)
        mtime = os.path.getmtime(file_path)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
        
        print(f"  ⭐ {file_path}: {file_size:,}バイト ({mtime_str})")
        
        # 簡易機能確認
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()[:1000]  # 最初の1000文字
            
            if "class" in content:
                classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                print(f"    📋 クラス: {', '.join(classes[:2])}")
        except:
            pass
    
    # 4. 推奨活用モジュール
    print(f"\n" + "=" * 70)
    print(f"🚀 活用推奨モジュール TOP5:")
    print(f"=" * 70)
    
    # discovered_modulesから上位5個を選出
    top_modules = sorted(discovered_modules.items(), 
                        key=lambda x: (len(x[1]['features']), x[1]['size']), 
                        reverse=True)[:5]
    
    for i, (file_path, info) in enumerate(top_modules, 1):
        print(f"{i}. 📄 {file_path}")
        print(f"   💾 サイズ: {info['size']:,}バイト")
        print(f"   📋 クラス: {len(info['classes'])}個")
        print(f"   🔧 関数: {len(info['functions'])}個")
        print(f"   🎯 機能: {', '.join(info['features'].keys())}")
        print(f"   📊 状況: {info['completion']}")
        print(f"   💡 推奨: 即座活用可能な高完成度モジュール")
        print()
    
    return discovered_modules

if __name__ == "__main__":
    discover_ready_modules()
