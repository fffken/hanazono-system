#!/bin/bash
# ファイル変更前にバックアップを作成するスクリプト

if [ $# -eq 0 ]; then
  echo "使用方法: bash backup_file.sh <ファイル名>"
  exit 1
fi

FILENAME=$1
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -f "$FILENAME" ]; then
  cp "$FILENAME" "${FILENAME}.${TIMESTAMP}.bak"
  echo "「${FILENAME}」のバックアップを「${FILENAME}.${TIMESTAMP}.bak」に作成しました"
else
  echo "エラー: 「${FILENAME}」が見つかりません"
  exit 1
fi
