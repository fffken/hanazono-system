#!/bin/bash
# 全効率向上機能統合実行

echo "⚡ 効率向上機能統合実行開始: $(date)"

for booster in scripts/efficiency_boosters/booster_*.sh; do
    if [ -f "$booster" ]; then
        echo "🚀 実行中: $(basename $booster)"
        timeout 45 bash "$booster" &
    fi
done

wait
echo "✅ 効率向上機能統合実行完了: $(date)"
