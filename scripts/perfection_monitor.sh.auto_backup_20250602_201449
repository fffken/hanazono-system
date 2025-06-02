#!/bin/bash
# 24時間完璧性監視システム

monitor_log="logs/perfection_monitor_$(date +%Y%m%d).log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🛡️ 完璧性監視開始" >> "$monitor_log"

# 重要システムのヘルスチェック
check_health() {
    local health_score=0
    
    # データ収集確認
    if find data/ -name "*.json" -newermt "20 minutes ago" | grep -q .; then
        health_score=$((health_score + 25))
    fi
    
    # Git保存確認
    if find logs/ -name "*auto_git_save*.log" -newermt "70 minutes ago" | grep -q .; then
        health_score=$((health_score + 25))
    fi
    
    # 進化システム確認
    if find logs/ -name "*evolution*.log" -newermt "3 hours ago" | grep -q .; then
        health_score=$((health_score + 25))
    fi
    
    # AI記憶システム確認
    if [ -f "ai_memory/storage/permanent/perfection_achievement.json" ]; then
        health_score=$((health_score + 25))
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❤️ システム健康度: ${health_score}%" >> "$monitor_log"
    
    # 健康度が低い場合の自動復旧
    if [ $health_score -lt 75 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔧 自動復旧開始" >> "$monitor_log"
        bash scripts/perfection_accelerator.sh >> "$monitor_log" 2>&1
    fi
}

# ヘルスチェック実行
check_health
