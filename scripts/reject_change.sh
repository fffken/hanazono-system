#!/bin/bash
# 変更却下システム

change_id="$1"

if [ -z "$change_id" ]; then
    echo "使用法: $0 <変更ID>"
    exit 1
fi

echo "❌ 変更却下: $change_id"
echo "📋 却下完了"
