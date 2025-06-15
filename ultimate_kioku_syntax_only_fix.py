#!/usr/bin/env python3
import re

def fix_syntax_only():
    with open('ultimate_kioku_system_correct.py', 'r') as f:
        content = f.read()
    
    # 文字列終端問題修正
    content = re.sub(r'(\*[^*]+\*)\s*"""\s*return', r'\1\n"""\n        return', content)
    
    # f-string内の改行問題修正
    content = content.replace('f"""# 🧠', 'f"""# 🧠')
    content = content.replace('"""', '"""')
    
    # インデント統一
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if line.strip().startswith('def ') and not line.startswith('    def ') and not line.startswith('def '):
            fixed_lines.append('    ' + line.strip())
        elif line.strip() and 'CREATE TABLE' in line:
            fixed_lines.append('        ' + line.strip())
        else:
            fixed_lines.append(line)
    
    with open('ultimate_kioku_system_correct.py', 'w') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ 構文修正完了")

if __name__ == "__main__":
    fix_syntax_only()
