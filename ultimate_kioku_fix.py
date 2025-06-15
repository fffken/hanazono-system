#!/usr/bin/env python3
"""
究極kioku構文エラー修正スクリプト
"""

def fix_syntax_error():
    print("🔧 構文エラー修正開始")
    
    # ファイル読み込み
    with open('ultimate_kioku_system.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 問題箇所修正（文字列内の改行問題）
    fixed_content = content.replace(
        '*3秒継承完了 | 詳細: KIOKU_ULTIMATE_DETAIL.md*\n"""\n        return handover',
        '*3秒継承完了 | 詳細: KIOKU_ULTIMATE_DETAIL.md*\n"""\n        return handover'
    )
    
    # より確実な修正（該当行を直接置換）
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '3秒継承完了 | 詳細: KIOKU_ULTIMATE_DETAIL.md' in line and 'return handover' in line:
            # 正しい形式に分割
            fixed_lines.append('*3秒継承完了 | 詳細: KIOKU_ULTIMATE_DETAIL.md*')
            fixed_lines.append('"""')
            fixed_lines.append('        return handover')
        else:
            fixed_lines.append(line)
    
    # 修正版保存
    with open('ultimate_kioku_system.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ 構文エラー修正完了")

if __name__ == "__main__":
    fix_syntax_error()
