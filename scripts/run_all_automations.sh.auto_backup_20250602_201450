#!/bin/bash
# 全自動化システム統合実行
# 自動生成時刻: $(date)

echo "🤖 全自動化システム実行開始"

# 生成された全自動化システムを実行
for script in scripts/generated/auto_*.sh; do
    if [ -f "$script" ]; then
        echo "実行中: $script"
        bash "$script"
    fi
done

echo "✅ 全自動化システム実行完了"
