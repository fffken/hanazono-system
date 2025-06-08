#!/bin/bash
# 究極のcron自動修正システム v1.0
# 目的: 人間の関与なしに完全自動でcron構文を修正

set -e

LOG_FILE="logs/ultimate_cron_fix_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🤖 究極のcron自動修正システム開始"

# 正しいcron設定のマスターテンプレート
create_perfect_cron() {
    cat << 'PERFECT_CRON_END' > /tmp/perfect_cron_master.txt
*/15 * * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --collect" > /dev/null 2>&1
0 7 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_morning.log 2>&1
0 23 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_night.log 2>&1
0 0 * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_update/update_handover.sh
0 7,19 * * * cd /home/pi/lvyuan_solar_control && python3 -c 'from system_health_monitor import run_controlled_health_check; run_controlled_health_check()' >> logs/daily_health.log 2>&1
0 3 * * * cd /home/pi/lvyuan_solar_control && python3 hanazono_optimizer.py standard >> logs/auto_optimize.log 2>&1
0 6 * * * cd /home/pi/lvyuan_solar_control && python3 hanazono_optimizer.py health >> logs/auto_health.log 2>&1
5 0 * * * cd /home/pi/lvyuan_solar_control && bash scripts/backup_handover_generator.sh >> logs/backup_handover.log 2>&1
0 */2 * * * python3 self_evolving_ai_v3.py --auto-evolve
*/15 * * * * python3 self_evolving_ai_v3.py --health-check
0 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_git_save_system.sh >> logs/auto_git_save.log 2>&1
PERFECT_CRON_END
}

# cron構文エラー検出
detect_cron_errors() {
    local error_count=0
    
    log "🔍 cron構文エラー検出中..."
    
    # 現在のcronを取得
    crontab -l > /tmp/current_cron.txt 2>/dev/null || echo "" > /tmp/current_cron.txt
    
    # エラーパターンをチェック
    while IFS= read -r line; do
        if [[ ! -z "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
            # 5フィールドチェック
            field_count=$(echo "$line" | awk '{for(i=1;i<=5;i++) if($i~/[0-9\*\/,-]+/) count++} END{print count+0}')
            
            # 一般的なエラーパターン
            if [[ "$line" =~ \*\* ]] || [[ "$line" =~ \*cd ]] || [ $field_count -lt 5 ]; then
                error_count=$((error_count + 1))
                log "❌ エラー検出: $line"
            fi
        fi
    done < /tmp/current_cron.txt
    
    return $error_count
}

# 自動修正実行
auto_fix_cron() {
    log "🔧 自動修正実行中..."
    
    # バックアップ
    BACKUP_FILE="/tmp/cron_backup_$(date +%Y%m%d_%H%M%S).txt"
    crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "" > "$BACKUP_FILE"
    log "📁 バックアップ作成: $BACKUP_FILE"
    
    # 完璧なcronを生成
    create_perfect_cron
    
    # 適用
    crontab /tmp/perfect_cron_master.txt
    log "✅ 完璧なcron設定を適用"
    
    # 検証
    if detect_cron_errors; then
        log "❌ 修正後もエラーが残存 - システム問題の可能性"
        return 1
    else
        log "✅ cron修正完了"
        return 0
    fi
}

# メイン処理
main() {
    if detect_cron_errors; then
        log "🚨 cron構文エラーを検出 - 自動修正を開始"
        auto_fix_cron
    else
        log "✅ cron構文は正常です"
    fi
    
    # 動作テスト
    log "🧪 cron動作テスト実行"
    echo "$(date +%M | awk '{print ($1+2)%60}') * * * * echo 'Auto-fix test: $(date)' >> /tmp/cron_autofix_test.log" | crontab -
    
    log "🎉 究極のcron自動修正システム完了"
}

# 実行
main
