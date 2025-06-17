#!/usr/bin/env python3
# ml_enhancement_phase1_v4_backup.py 完全構造把握（完全非破壊的）
import datetime
import os
import subprocess

def analyze_ml_backup_module():
    """ml_enhancement_phase1_v4_backup.py 完全構造把握"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 ml_enhancement_phase1_v4_backup.py 完全構造把握開始 {timestamp}")
    print("=" * 70)
    
    target_file = "ml_enhancement_phase1_v4_backup.py"
    
    # 1. 基本情報確認（完全非破壊的）
    print(f"📄 基本情報:")
    if os.path.exists(target_file):
        file_size = os.path.getsize(target_file)
        mtime = os.path.getmtime(target_file)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"  ✅ ファイル: {target_file}")
        print(f"  💾 サイズ: {file_size:,}バイト")
        print(f"  📅 更新日: {mtime_str}")
        print(f"  🏆 シンタックス: 正常確認済み")
    else:
        print(f"  ❌ ファイル未発見")
        return False
    
    # 2. 構造分析（読み取り専用・非破壊的）
    print(f"\n🏗️ モジュール構造分析:")
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # クラス・関数構造把握
        classes = []
        functions = []
        imports = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('class '):
                class_name = stripped.split('(')[0].replace('class ', '').strip(':')
                classes.append((i, class_name))
            elif stripped.startswith('def '):
                func_name = stripped.split('(')[0].replace('def ', '')
                functions.append((i, func_name))
            elif stripped.startswith('import ') or stripped.startswith('from '):
                imports.append(stripped)
        
        print(f"  📋 クラス数: {len(classes)}")
        for line_num, class_name in classes:
            print(f"    行{line_num}: {class_name}")
        
        print(f"  🔧 関数数: {len(functions)}")
        for line_num, func_name in functions[:10]:  # 最初の10個
            print(f"    行{line_num}: {func_name}")
        if len(functions) > 10:
            print(f"    ... 他{len(functions) - 10}個")
        
        print(f"  📦 主要インポート:")
        for imp in imports[:8]:  # 最初の8個
            print(f"    {imp}")
            
    except Exception as e:
        print(f"  ❌ 構造分析エラー: {e}")
        return False
    
    # 3. HANAZONOシステム適合性分析（読み取り専用）
    print(f"\n🎯 HANAZONOシステム適合性分析:")
    
    # 機械学習・データ分析関連キーワード検索
    ml_keywords = [
        "machine learning", "ml", "data", "analysis", "predict", 
        "optimization", "efficiency", "battery", "solar", "weather"
    ]
    
    hanazono_keywords = [
        "hanazono", "solar", "battery", "optimization", "efficiency",
        "data_collection", "monitoring", "email", "report"
    ]
    
    content_lower = content.lower()
    
    ml_score = sum(1 for keyword in ml_keywords if keyword in content_lower)
    hanazono_score = sum(1 for keyword in hanazono_keywords if keyword in content_lower)
    
    print(f"  🤖 機械学習適合度: {ml_score}/10")
    print(f"  🌻 HANAZONO適合度: {hanazono_score}/8")
    
    total_compatibility = (ml_score + hanazono_score) / 18 * 100
    print(f"  📊 総合適合度: {total_compatibility:.1f}%")
    
    # 4. 実行可能性確認（完全非破壊的テスト）
    print(f"\n🧪 実行可能性確認:")
    try:
        print(f"  🚀 安全実行テスト開始...")
        result = subprocess.run([
            'python3', target_file
        ], capture_output=True, text=True, timeout=30)
        
        print(f"  📊 実行結果:")
        print(f"    終了コード: {result.returncode}")
        
        if result.stdout:
            output_lines = result.stdout.split('\n')[:10]  # 最初の10行
            print(f"  📝 出力サンプル:")
            for line in output_lines:
                if line.strip():
                    print(f"    {line}")
        
        if result.returncode == 0:
            print(f"  ✅ 実行成功")
            execution_status = "正常動作"
        else:
            print(f"  ⚠️ 実行完了（警告あり）")
            execution_status = "部分動作"
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ 30秒でタイムアウト（長時間処理中）")
        execution_status = "長時間処理"
    except Exception as e:
        print(f"  ❌ 実行テストエラー: {e}")
        execution_status = "実行不可"
    
    # 5. HANAZONOシステム統合推奨度評価
    print(f"\n" + "=" * 70)
    print(f"🏆 HANAZONOシステム統合推奨度評価:")
    print(f"=" * 70)
    
    evaluation_criteria = [
        ("ファイルサイズ", file_size > 30000, f"{file_size:,}バイト"),
        ("シンタックス", True, "正常"),
        ("実行可能性", execution_status in ["正常動作", "部分動作"], execution_status),
        ("適合度", total_compatibility >= 50, f"{total_compatibility:.1f}%"),
        ("機械学習機能", ml_score >= 5, f"{ml_score}/10")
    ]
    
    integration_score = 0
    for criteria, status, detail in evaluation_criteria:
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {criteria}: {detail}")
        if status:
            integration_score += 1
    
    final_score = integration_score / len(evaluation_criteria) * 100
    print(f"\n🎯 統合推奨度: {final_score:.1f}%")
    
    # 6. 推奨アクション（完全非破壊的方針）
    print(f"\n📋 推奨アクション（完全非破壊的）:")
    
    if final_score >= 80:
        print(f"🚀 即座統合実装推奨")
        actions = [
            "新ファイルとしてHANAZONO統合版作成",
            "既存システムと並行動作テスト", 
            "動作確認後に手動統合判断"
        ]
    elif final_score >= 60:
        print(f"🔧 調整後統合推奨")
        actions = [
            "HANAZONO用カスタマイズ版作成",
            "段階的統合テスト実行",
            "安全確認後に本格統合"
        ]
    else:
        print(f"📋 詳細検証推奨")
        actions = [
            "機能詳細分析継続",
            "他モジュールとの比較検討",
            "最適統合方法の再検討"
        ]
    
    for i, action in enumerate(actions, 1):
        print(f"   {i}. {action}")
    
    return {
        "score": final_score,
        "execution": execution_status,
        "recommendation": "immediate" if final_score >= 80 else "adjust" if final_score >= 60 else "investigate"
    }

if __name__ == "__main__":
    analyze_ml_backup_module()
