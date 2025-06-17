#!/usr/bin/env python3
# 重要3ファイルピンポイント確認（完全非破壊的）
import os
import re

def pinpoint_check_battle_function():
    """重要3ファイルピンポイント確認"""
    print("🎯 重要3ファイルピンポイント確認開始")
    print("=" * 50)
    
    # 重要ファイル3つに絞る
    target_files = [
        "integrate_battle_to_mail.py",
        "fix_mail_formatting.py", 
        "battle_news_generator.py"
    ]
    
    target_function = "format_battle_section"
    
    for file_path in target_files:
        print(f"\n📄 {file_path} 確認:")
        
        if not os.path.exists(file_path):
            print(f"  ❌ ファイル不存在")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # format_battle_section確認
            if target_function in content:
                print(f"  ✅ {target_function} 発見!")
                
                # 該当行を抽出
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if target_function in line:
                        print(f"    行{i+1}: {line.strip()}")
                        # 前後2行も表示
                        for j in range(max(0, i-1), min(len(lines), i+3)):
                            prefix = "  → " if j == i else "    "
                            print(f"    {prefix}{j+1}: {lines[j].strip()}")
                        break
                        
                # この関数が完全に定義されているか確認
                func_pattern = r'def\s+format_battle_section\s*\([^)]*\):'
                if re.search(func_pattern, content):
                    print(f"  ✅ 完全な関数定義あり")
                    
                    # 関数の内容確認（最初の10行）
                    match = re.search(func_pattern, content)
                    if match:
                        start_pos = match.end()
                        after_def = content[start_pos:]
                        function_lines = after_def.split('\n')[:10]
                        
                        print(f"  📋 関数内容（最初の10行）:")
                        for idx, func_line in enumerate(function_lines):
                            if func_line.strip():
                                print(f"    {idx+1}: {func_line}")
                else:
                    print(f"  ⚠️ 関数定義不完全（参照のみ）")
            else:
                print(f"  ❌ {target_function} なし")
                
                # 代替バトル関数があるか確認
                battle_functions = re.findall(r'def\s+([a-zA-Z_]*battle[a-zA-Z_]*)', content, re.IGNORECASE)
                if battle_functions:
                    print(f"  📋 バトル関連関数: {', '.join(battle_functions)}")
                    
        except Exception as e:
            print(f"  ❌ 読み取りエラー: {e}")
    
    print(f"\n🎯 結論:")
    print(f"format_battle_section の所在を特定します")

if __name__ == "__main__":
    pinpoint_check_battle_function()
