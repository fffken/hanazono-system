#!/bin/bash
# GitHub自動読み込みシステムラッパースクリプト

# 設定
PYTHON_SCRIPT="github_access_system.py"
OUTPUT_DIR="github_files"

# 必要なディレクトリを作成
mkdir -p "$OUTPUT_DIR"

# 引数チェック
if [ $# -lt 1 ]; then
  echo "使用方法: $0 <コマンド> [引数...]"
  echo "コマンド:"
  echo "  test       - GitHub接続テスト"
  echo "  fetch      - 指定したファイルを取得"
  echo "  fetch_all  - 重要なファイルをすべて取得"
  echo "  setup      - 初期設定"
  exit 1
fi

COMMAND=$1
shift

# コマンド実行
case "$COMMAND" in
  test)
    python3 "$PYTHON_SCRIPT" test
    ;;
    
  fetch)
    if [ $# -lt 1 ]; then
      echo "ファイルパスを指定してください"
      exit 1
    fi
    FILE_PATH=$1
    OUTPUT_FILE="$OUTPUT_DIR/$(basename $FILE_PATH)"
    echo "📥 ファイル取得中: $FILE_PATH"
    python3 "$PYTHON_SCRIPT" get "$FILE_PATH" > "$OUTPUT_FILE"
    echo "✅ 保存完了: $OUTPUT_FILE"
    ;;
    
  fetch_all)
    echo "🚀 重要ファイルを一括取得します..."
    
    # 重要ファイルリスト
    FILES=(
      "AI_WORK_RULES.md"
      "PROJECT_STATUS.md"
      "github_auto_handover.md"
    )
    
    for FILE in "${FILES[@]}"; do
      OUTPUT_FILE="$OUTPUT_DIR/$FILE"
      echo "📥 ファイル取得中: $FILE"
      python3 "$PYTHON_SCRIPT" get "$FILE" > "$OUTPUT_FILE"
      echo "✅ 保存完了: $OUTPUT_FILE"
    done
    
    echo "🎉 すべてのファイルの取得が完了しました！"
    echo "📁 保存先ディレクトリ: $OUTPUT_DIR"
    ;;
    
  setup)
    python3 "$PYTHON_SCRIPT" setup
    ;;
    
  *)
    echo "不明なコマンド: $COMMAND"
    echo "使用方法: $0 <コマンド> [引数...]"
    exit 1
    ;;
esac
