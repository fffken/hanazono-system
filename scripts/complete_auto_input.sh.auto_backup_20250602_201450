#!/bin/bash
# 完全自動入力システム

TASK_NAME="$1"
DESCRIPTION="$2"

if [ -z "$TASK_NAME" ] || [ -z "$DESCRIPTION" ]; then
    echo "使用方法: bash scripts/complete_auto_input.sh 'タスク名' '説明'"
    exit 1
fi

# 自動入力実行
{
    echo "1"
    echo "$TASK_NAME"
    echo "$DESCRIPTION"
} | bash scripts/enhanced_auto_file_generator.sh
