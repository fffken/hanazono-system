#!/bin/bash
# 自動生成: cron完全自動管理システム
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_cron_$(date +%Y%m%d).log"
}

# cron健全性チェック
check_cron_health() {
    local issues=0
    
    # 構文チェック
    while IFS= read -r line; do
        if [[ ! -z "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
            if [[ "$line" =~ \*\* ]] || [[ "$line" =~ \*[a-z] ]]; then
                issues=$((issues + 1))
            fi
        fi
    done < <(crontab -l 2>/dev/null)
    
    return $issues
}

# 自動修正実行
auto_fix_cron() {
    log "🔧 cron自動修正実行"
    
    # マスターcron適用
    cat << 'MASTER_CRON' | crontab -
*/15 * * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --collect" > /dev/null 2>&1
0 7 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_morning.log 2>&1
0 23 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_night.log 2>&1
0 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_git_save_system.sh >> logs/auto_git_save.log 2>&1
MASTER_CRON
    
    log "✅ cron自動修正完了"
}

# メイン処理
if check_cron_health; then
    log "🚨 cron問題検出 - 自動修正開始"
    auto_fix_cron
else
    log "✅ cron正常"
fi
