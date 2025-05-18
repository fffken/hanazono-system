#!/usr/bin/env python3

import re
import sys
import os
from datetime import datetime

def fix_docstring_and_indent(filename):
    """ドキュメント文字列の閉じ忘れとインデント問題を修正"""
    # バックアップ作成
    backup_name = f"{filename}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"バックアップを作成: {backup_name}")
    os.system(f"cp {filename} {backup_name}")
    
    # ファイルを読み込む
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 修正されたラインを格納
    fixed_lines = []
    
    # 三重引用符の状態を追跡
    in_triple_quotes = False
    triple_quotes_start_line = 0
    triple_quotes_indent = 0
    
    # 期待されるインデントレベル（クラスメソッド内部なら8スペース）
    expected_indent = 0
    
    # 行単位で処理
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 三重引用符のカウント
        triple_quotes_count = line.count('"""')
        
        # 三重引用符の開始と終了を追跡
        if not in_triple_quotes and '"""' in line and triple_quotes_count % 2 != 0:
            in_triple_quotes = True
            triple_quotes_start_line = i
            triple_quotes_indent = len(line) - len(line.lstrip())
        elif in_triple_quotes and '"""' in line and triple_quotes_count % 2 != 0:
            in_triple_quotes = False
        
        # 特定の問題行を修正
        if i == 1045:  # 問題のあるdocstringの前
            fixed_lines.append(line)
            if i+1 < len(lines) and '"""' in lines[i+1] and not '"""' in lines[i+1].rstrip()[3:]:
                # 次の行が閉じていない三重引用符を含む場合、閉じる
                indent = len(lines[i+1]) - len(lines[i+1].lstrip())
                fixed_lines.append(lines[i+1].rstrip() + '\n')  # 現在の行をそのまま追加
                # 同じインデントで閉じる三重引用符を追加
                fixed_lines.append(' ' * indent + '"""\n')
                i += 1  # 次の行は処理済み
        elif i == 962:  # 最初のインデントエラーの付近
            # インデントを修正（前後のコンテキストを考慮）
            current_indent = len(line) - len(line.lstrip())
            if current_indent != 8 and lines[i].strip().startswith('return'):
                # returnステートメントなら、前の行と同じインデントにする
                prev_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                fixed_lines.append(' ' * prev_indent + line.lstrip())
            else:
                fixed_lines.append(line)
        elif i == 982:  # 2番目のインデントエラーの付近
            # インデントを修正
            if line.strip().startswith('#') or line.strip().startswith('smtp_'):
                # メソッド内の通常のコードなら8スペース
                fixed_lines.append(' ' * 8 + line.lstrip())
            else:
                fixed_lines.append(line)
        elif i == 1055:  # 3番目のインデントエラーの付近
            # インデントを修正
            if line.strip().startswith('#') or line.strip().startswith('smtp_'):
                # メソッド内の通常のコードなら8スペース
                fixed_lines.append(' ' * 8 + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            # 他の行はそのまま追加
            fixed_lines.append(line)
        
        i += 1
    
    # 修正した内容をファイルに書き込む
    with open(f"{filename}.fixed", 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"修正完了！結果を {filename}.fixed に保存しました。")
    print("修正後のファイルをテストしてください:")
    print(f"python3 -m py_compile {filename}.fixed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"使用方法: {sys.argv[0]} <Pythonファイル>")
        sys.exit(1)
    
    filename = sys.argv[1]
    fix_docstring_and_indent(filename)
