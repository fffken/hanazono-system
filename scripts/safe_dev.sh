#!/bin/bash
# 安全開発ワークフロー
source scripts/savepoint.sh
source scripts/safe_edit.sh

dev() {
    echo "🔒 実装前セーフポイント作成"
    save "$1"
    echo "🔧 実装実行: $1"
    echo "完了後 Enterキーを押してください"
    read
    if python3 main.py --daily-report >/dev/null 2>&1; then
        echo "✅ 実装成功"; save "$1完了"
    else
        echo "❌ 実装失敗"; restore
    fi
}
