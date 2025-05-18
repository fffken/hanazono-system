#!/bin/bash
# ファイル整理スクリプト

# スクリプトファイルを整理
echo "スクリプトファイルを整理します..."
for f in fix_*.sh fix_*.py restore_*.sh; do
  if [ -f "$f" ]; then
    echo "  $f → scripts/$f"
    mv "$f" "scripts/$f"
  fi
done

# バックアップファイルを整理
echo "バックアップファイルを整理します..."
mkdir -p backup/email_notifier
mkdir -p backup/main

count=0
for f in *.bak*; do
  if [[ $f == email_notifier* ]]; then
    echo "  $f → backup/email_notifier/$f"
    mv "$f" "backup/email_notifier/$f"
    ((count++))
  elif [[ $f == main* ]]; then
    echo "  $f → backup/main/$f"
    mv "$f" "backup/main/$f"
    ((count++))
  fi
done
echo "$count バックアップファイルを整理しました"


# ディレクトリ構造の作成
echo "## ディレクトリ構造の確認/作成"
mkdir -p backups docs/technical docs/guides tests modules scripts

# テストファイルの移動
echo "## テストファイルの整理"
find . -maxdepth 1 -name "test_*.py" -type f | while read file; do
  echo "移動: $file -> tests/"
  mv "$file" tests/ 2>/dev/null || echo "  スキップ: $file"
done

# ドキュメントファイルのインデックス作成
echo "## ドキュメントインデックスの作成"
ls -la docs/ > docs/INDEX.md
echo "ドキュメント一覧を docs/INDEX.md に作成しました"

echo "=== ファイル整理完了 ==="
