#!/usr/bin/env python3
import os,re,sys
def check_syntax_errors():
    errors = []
    venv_path = "venv/lib/python3.11/site-packages"
    critical_packages = ["urllib3", "requests", "pysolarmanv5"]
    for pkg in critical_packages:
        pkg_path = os.path.join(venv_path, pkg)
        if os.path.exists(pkg_path):
            for root,dirs,files in os.walk(pkg_path):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r') as f:
                                content = f.read()
                            if re.search(r'\(\s*=', content):
                                errors.append(f"破損検出: {filepath} - 疑わしい構文")
                            compile(content, filepath, 'exec')
                        except SyntaxError as e:
                            errors.append(f"構文エラー: {filepath} - {e}")
    return errors
if __name__ == "__main__":
    errors = check_syntax_errors()
    if errors:
        for error in errors: print(error)
        sys.exit(1)
    else:
        print("✅ ファイル完全性確認済み")
