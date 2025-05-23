#!/usr/bin/env python3
# ast_fix_indentation.py

import ast
import sys
import os
from datetime import datetime

try:
    import astor
except ImportError:
    print("astorモジュールをインストールします...")
    os.system("pip install astor")
    import astor


def fix_indentation(filename):
    """AST解析を使用してPythonファイルのインデント問題を修正する"""
    # バックアップ作成
    backup_name = f"{filename}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"バックアップを作成: {backup_name}")
    os.system(f"cp {filename} {backup_name}")

    try:
        # ファイルを読み込んで解析
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()

        try:
            # ASTとしてパース
            tree = ast.parse(source)

            # ASTから整形されたコードを生成
            formatted_code = astor.to_source(tree)

            # 整形結果を保存
            with open(f"{filename}.fixed", 'w', encoding='utf-8') as f:
                f.write(formatted_code)

            # 構文チェック
            compile_result = os.system(
                f"python3 -m py_compile {filename}.fixed")

            if compile_result == 0:
                print("修正成功！整形後のコードは構文的に正しいです。")
                os.system(f"mv {filename}.fixed {filename}")
                return True
            else:
                print("修正後もまだ構文エラーが残っています。")
                return False

        except SyntaxError as e:
            print(f"構文エラーのためASTの構築に失敗しました: {e}")
            print("行単位での部分的な修正を試みます...")
            return False

    except Exception as e:
        print(f"エラー発生: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"使用方法: {sys.argv[0]} <修正するPythonファイル>")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"エラー: ファイル '{filename}' が見つかりません")
        sys.exit(1)

    success = fix_indentation(filename)
    if success:
        print("インデント問題の修正が完了しました。")
    else:
        print("インデント問題の完全な修正ができませんでした。")
        print("シェルスクリプト版の fix_indentation.sh を試してください。")
        sys.exit(1)
