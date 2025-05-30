import re
import sys
import os
from datetime import datetime

def fix_docstring_and_indent(filename):
    """ドキュメント文字列の閉じ忘れとインデント問題を修正"""
    backup_name = f"{filename}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f'バックアップを作成: {backup_name}')
    os.system(f'cp {filename} {backup_name}')
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    fixed_lines = []
    in_triple_quotes = False
    triple_quotes_start_line = 0
    triple_quotes_indent = 0
    expected_indent = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        triple_quotes_count = line.count('"""')
        if not in_triple_quotes and '"""' in line and (triple_quotes_count % 2 != 0):
            in_triple_quotes = True
            triple_quotes_start_line = i
            triple_quotes_indent = len(line) - len(line.lstrip())
        elif in_triple_quotes and '"""' in line and (triple_quotes_count % 2 != 0):
            in_triple_quotes = False
        if i == 1045:
            fixed_lines.append(line)
            if i + 1 < len(lines) and '"""' in lines[i + 1] and (not '"""' in lines[i + 1].rstrip()[3:]):
                indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                fixed_lines.append(lines[i + 1].rstrip() + '\n')
                fixed_lines.append(' ' * indent + '"""\n')
                i += 1
        elif i == 962:
            current_indent = len(line) - len(line.lstrip())
            if current_indent != 8 and lines[i].strip().startswith('return'):
                prev_indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                fixed_lines.append(' ' * prev_indent + line.lstrip())
            else:
                fixed_lines.append(line)
        elif i == 982:
            if line.strip().startswith('#') or line.strip().startswith('smtp_'):
                fixed_lines.append(' ' * 8 + line.lstrip())
            else:
                fixed_lines.append(line)
        elif i == 1055:
            if line.strip().startswith('#') or line.strip().startswith('smtp_'):
                fixed_lines.append(' ' * 8 + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        i += 1
    with open(f'{filename}.fixed', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    print(f'修正完了！結果を {filename}.fixed に保存しました。')
    print('修正後のファイルをテストしてください:')
    print(f'python3 -m py_compile {filename}.fixed')
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'使用方法: {sys.argv[0]} <Pythonファイル>')
        sys.exit(1)
    filename = sys.argv[1]
    fix_docstring_and_indent(filename)