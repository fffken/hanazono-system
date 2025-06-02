#!/bin/bash
# 自己進化システムエンジン v2.0 - 改良版
# 目的: より精密な学習・進化・完璧化システム

set -e

EVOLUTION_DIR="system_evolution"
LEARNING_DB="$EVOLUTION_DIR/learning_database_v2.json"
EVOLUTION_LOG="logs/evolution_v2_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$EVOLUTION_DIR" logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$EVOLUTION_LOG"
}

log "🧬 自己進化システムv2.0開始"

# 改良版：成功パターン検出システム
detect_success_patterns() {
    log "🎯 成功パターン検出v2.0開始"
    
    local success_patterns=()
    
    # 最近の成功ログを分析
    local recent_logs=$(find logs/ -name "*.log" -newermt "2 hours ago" 2>/dev/null)
    
    # 成功パターンの検出
    for logfile in $recent_logs; do
        if grep -q "✅\|成功\|完了\|SUCCESS" "$logfile" 2>/dev/null; then
            # 成功に至った処理を抽出
            local success_actions=$(grep -B3 -A1 "✅\|成功\|完了" "$logfile" | grep -E "(実行|処理|修正|生成)" | head -5)
            
            while IFS= read -r action; do
                if [[ ! -z "$action" ]]; then
                    local pattern_type=$(classify_success_pattern "$action")
                    if [[ ! -z "$pattern_type" ]]; then
                        success_patterns+=("$pattern_type:$action")
                        log "📊 成功パターン検出: $pattern_type"
                    fi
                fi
            done <<< "$success_actions"
        fi
    done
    
    echo "${success_patterns[@]}"
}

# 成功パターン分類システム
classify_success_pattern() {
    local action="$1"
    
    case "$action" in
        *"cron"*|*"crontab"*)
            echo "cron_management"
            ;;
        *"git"*|*"commit"*|*"push"*)
            echo "version_control"
            ;;
        *"chmod"*|*"権限"*)
            echo "permission_fix"
            ;;
        *"nano"*|*"修正"*|*"編集"*)
            echo "file_editing"
            ;;
        *"自動"*|*"auto"*)
            echo "automation_enhancement"
            ;;
        *"記憶"*|*"memory"*)
            echo "memory_system"
            ;;
        *)
            echo "general_success"
            ;;
    esac
}

# 改良版：問題解決能力評価システム
evaluate_problem_solving() {
    log "🔍 問題解決能力評価中..."
    
    local solving_score=0
    
    # 最近の問題解決事例をカウント
    local recent_problem_solving=$(find logs/ -name "*.log" -newermt "24 hours ago" -exec grep -l "❌.*✅\|エラー.*成功\|失敗.*完了" {} \; 2>/dev/null | wc -l)
    
    if [ $recent_problem_solving -gt 0 ]; then
        solving_score=$((solving_score + 30))
        log "📈 問題解決実績: ${recent_problem_solving}件"
    fi
    
    # 自動化システム数
    local automation_count=$(find scripts/ -name "auto_*.sh" 2>/dev/null | wc -l)
    if [ $automation_count -ge 10 ]; then
        solving_score=$((solving_score + 25))
    elif [ $automation_count -ge 5 ]; then
        solving_score=$((solving_score + 15))
    fi
    
    # システム稼働状況
    if pgrep -f "python3.*main.py" > /dev/null; then
        solving_score=$((solving_score + 20))
    fi
    
    # 記憶システム完全性
    if [ -f "ai_memory/storage/permanent/github_system_memory.json" ] && [ -f "ai_memory/storage/permanent/self_evolution_memory.json" ]; then
        solving_score=$((solving_score + 25))
    fi
    
    log "🎯 問題解決能力: ${solving_score}%"
    return $solving_score
}

# 改良版：次世代機能生成システム
generate_next_gen_feature() {
    local pattern_info="$1"
    local pattern_type=$(echo "$pattern_info" | cut -d: -f1)
    local pattern_action=$(echo "$pattern_info" | cut -d: -f2-)
    
    log "🛠️ 次世代機能生成: $pattern_type"
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local feature_script="scripts/auto_generated/nextgen_${pattern_type}_${timestamp}.sh"
    
    case "$pattern_type" in
        "cron_management")
            generate_advanced_cron_feature "$feature_script"
            ;;
        "version_control")
            generate_smart_git_feature "$feature_script"
            ;;
        "automation_enhancement")
            generate_meta_automation_feature "$feature_script"
            ;;
        "memory_system")
            generate_enhanced_memory_feature "$feature_script"
            ;;
        *)
            generate_adaptive_feature "$feature_script" "$pattern_type"
            ;;
    esac
    
    chmod +x "$feature_script"
    log "✅ 次世代機能生成完了: $feature_script"
}

# 高度cron管理機能
generate_advanced_cron_feature() {
    local script_path="$1"
    
    cat << 'ADVANCED_CRON_END' > "$script_path"
#!/bin/bash
# 次世代: 高度cron管理システム
# 自動生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/nextgen_cron_$(date +%Y%m%d).log"
}

# 高度cron健全性チェック
advanced_cron_check() {
    log "🔍 高度cron分析開始"
    
    # cron実行履歴分析
    local cron_success_rate=0
    local total_cron_jobs=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
    
    if [ $total_cron_jobs -gt 0 ]; then
        # 各cronジョブの実行状況を確認
        local successful_jobs=0
        
        # データ収集cronの確認
        if find data/ -name "lvyuan_data_*.json" -newermt "30 minutes ago" 2>/dev/null | grep -q .; then
            successful_jobs=$((successful_jobs + 1))
            log "✅ データ収集cron正常稼働"
        fi
        
        # Git保存cronの確認
        if find logs/ -name "*auto_git_save*.log" -newermt "2 hours ago" 2>/dev/null | grep -q .; then
            successful_jobs=$((successful_jobs + 1))
            log "✅ Git保存cron正常稼働"
        fi
        
        cron_success_rate=$((successful_jobs * 100 / total_cron_jobs))
        log "📊 cron成功率: ${cron_success_rate}%"
        
        # 成功率が低い場合の自動修復
        if [ $cron_success_rate -lt 80 ]; then
            log "🔧 cron自動修復開始"
            
            # マスターcron設定を再適用
            cat << 'MASTER_CRON_V2' | crontab -
*/15 * * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --collect" > /dev/null 2>&1
0 7 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_morning.log 2>&1
0 23 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_night.log 2>&1
0 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_git_save_system.sh >> logs/auto_git_save.log 2>&1
0 */2 * * * cd /home/pi/lvyuan_solar_control && bash scripts/self_evolution_engine_v2.sh >> logs/self_evolution_v2.log 2>&1
0 */4 * * * cd /home/pi/lvyuan_solar_control && bash scripts/run_evolved_systems.sh >> logs/evolved_systems.log 2>&1
MASTER_CRON_V2
            
            log "✅ マスターcron再適用完了"
        fi
    fi
}

# メイン処理
advanced_cron_check
ADVANCED_CRON_END
}

# スマートGit機能
generate_smart_git_feature() {
    local script_path="$1"
    
    cat << 'SMART_GIT_END' > "$script_path"
#!/bin/bash
# 次世代: スマートGit管理システム
# 自動生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/nextgen_git_$(date +%Y%m%d).log"
}

# インテリジェントGit操作
smart_git_operation() {
    log "🧠 スマートGit操作開始"
    
    # 変更の重要度分析
    local change_importance="medium"
    local changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    if [ $changes -eq 0 ]; then
        log "✅ 変更なし - Git操作不要"
        return 0
    fi
    
    # AI記憶システムファイルの変更チェック
    if git status --porcelain | grep -q "ai_memory/"; then
        change_importance="high"
        log "🧠 AI記憶システム変更検出 - 高優先度"
    fi
    
    # 新機能ファイルの変更チェック
    if git status --porcelain | grep -q "scripts/.*auto.*\.sh"; then
        change_importance="high"
        log "🤖 自動化システム変更検出 - 高優先度"
    fi
    
    # 重要度に応じたコミット戦略
    case "$change_importance" in
        "high")
            log "🚀 高優先度変更 - 即座コミット・プッシュ"
            git add ai_memory/ scripts/auto_generated/ scripts/*auto*.sh *.md 2>/dev/null || true
            git commit -m "🧬 自己進化システム重要更新: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
            git push origin main 2>/dev/null || true
            ;;
        "medium")
            log "📦 中優先度変更 - バッチコミット"
            git add logs/ *.json 2>/dev/null || true
            git commit -m "📊 システム更新: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
            ;;
        *)
            log "📝 低優先度変更 - 記録のみ"
            ;;
    esac
    
    log "✅ スマートGit操作完了"
}

# メイン処理
smart_git_operation
SMART_GIT_END
}

# メタ自動化機能
generate_meta_automation_feature() {
    local script_path="$1"
    
    cat << 'META_AUTO_END' > "$script_path"
#!/bin/bash
# 次世代: メタ自動化システム（自動化を自動化）
# 自動生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/nextgen_meta_$(date +%Y%m%d).log"
}

# 自動化の自動化
meta_automation() {
    log "🤖 メタ自動化開始"
    
    # 手動作業パターンの検出
    local manual_patterns=$(grep -r "nano\|vi\|手動\|manual" logs/ 2>/dev/null | grep -v "自動" | wc -l)
    
    if [ $manual_patterns -gt 3 ]; then
        log "🎯 手動作業パターン検出: ${manual_patterns}件"
        
        # 新しい自動化スクリプトを生成
        local new_auto_script="scripts/auto_generated/meta_generated_$(date +%Y%m%d_%H%M%S).sh"
        
        cat << 'NEW_AUTO_SCRIPT' > "$new_auto_script"
#!/bin/bash
# メタ自動化により生成された自動化スクリプト

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/meta_generated_$(date +%Y%m%d).log"
}

# 検出された手動作業を自動化
auto_handle_manual_tasks() {
    log "🔧 手動作業自動化開始"
    
    # ファイル権限の自動設定
    find scripts/ -name "*.sh" -type f ! -perm -u+x -exec chmod +x {} \; 2>/dev/null
    
    # ログファイルのローテーション
    find logs/ -name "*.log" -size +10M -exec gzip {} \; 2>/dev/null
    
    # 一時ファイルのクリーンアップ
    find /tmp -name "*cron*" -o -name "*temp*" -mtime +1 -delete 2>/dev/null || true
    
    log "✅ 手動作業自動化完了"
}

# 実行
auto_handle_manual_tasks
NEW_AUTO_SCRIPT
        
        chmod +x "$new_auto_script"
        log "✅ 新自動化スクリプト生成: $new_auto_script"
    fi
    
    log "✅ メタ自動化完了"
}

# メイン処理
meta_automation
META_AUTO_END
}

# 拡張記憶機能
generate_enhanced_memory_feature() {
    local script_path="$1"
    
    cat << 'ENHANCED_MEMORY_END' > "$script_path"
#!/bin/bash
# 次世代: 拡張AI記憶システム
# 自動生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/nextgen_memory_$(date +%Y%m%d).log"
}

# 拡張記憶システム
enhanced_memory_system() {
    log "🧠 拡張記憶システム開始"
    
    # パフォーマンス記憶の記録
    local performance_data=$(cat << PERF_DATA
{
  "performance_memory": {
    "記録時刻": "$(date '+%Y-%m-%d %H:%M:%S')",
    "システム稼働時間": "$(uptime -p)",
    "メモリ使用率": "$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')",
    "ディスク使用率": "$(df / | tail -1 | awk '{print $5}')",
    "CPU負荷": "$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')",
    "実行中プロセス数": "$(ps aux | wc -l)",
    "自動化スクリプト数": "$(find scripts/ -name 'auto_*.sh' | wc -l)",
    "記憶ファイル数": "$(find ai_memory/ -name '*.json' | wc -l)"
  }
}
PERF_DATA
)
    
    echo "$performance_data" > "ai_memory/storage/permanent/performance_memory_$(date +%Y%m%d_%H%M%S).json"
    
    # 学習効率の分析と記録
    local learning_efficiency=$(find scripts/auto_generated/ -name "*.sh" -newermt "24 hours ago" | wc -l)
    
    local learning_data=$(cat << LEARN_DATA
{
  "learning_memory": {
    "記録時刻": "$(date '+%Y-%m-%d %H:%M:%S')",
    "24時間学習数": "$learning_efficiency",
    "累積学習数": "$(find scripts/auto_generated/ -name '*.sh' | wc -l)",
    "進化サイクル数": "$(find logs/ -name '*evolution*.log' | wc -l)",
    "解決済み問題数": "$(grep -r "✅.*完了" logs/ 2>/dev/null | wc -l)",
    "学習効率": "$(echo "scale=2; $learning_efficiency / 24" | bc -l 2>/dev/null || echo "0.00")"
  }
}
LEARN_DATA
)
    
    echo "$learning_data" > "ai_memory/storage/permanent/learning_efficiency_$(date +%Y%m%d_%H%M%S).json"
    
    log "✅ 拡張記憶システム完了"
}

# メイン処理
enhanced_memory_system
ENHANCED_MEMORY_END
}

# 適応型機能生成
generate_adaptive_feature() {
    local script_path="$1"
    local pattern_type="$2"
    
    cat << ADAPTIVE_END > "$script_path"
#!/bin/bash
# 次世代: 適応型${pattern_type}システム
# 自動生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/nextgen_adaptive_$(date +%Y%m%d).log"
}

# 適応型処理
adaptive_${pattern_type}() {
    log "🔄 適応型${pattern_type}開始"
    
    # 環境適応分析
    local system_load=$(uptime | awk -F'load average:' '{print \$2}' | awk '{print \$1}' | sed 's/,//' | awk '{print int(\$1)}')
    local memory_usage=$(free | grep Mem | awk '{print int(\$3/\$2 * 100)}')
    
    # 負荷に応じた適応的処理
    if [ \$system_load -gt 2 ] || [ \$memory_usage -gt 80 ]; then
        log "⚡ 高負荷モード - 軽量処理実行"
        # 軽量処理のみ実行
        find /tmp -name "*.tmp" -delete 2>/dev/null || true
    else
        log "🚀 通常モード - 完全処理実行"
        # フル機能実行
        
        # ${pattern_type}特有の処理
        case "${pattern_type}" in
            *"success"*)
                # 成功パターンの強化学習
                grep -r "✅" logs/ 2>/dev/null | tail -10 > "system_evolution/success_patterns_\$(date +%Y%m%d).log"
                ;;
            *"general"*)
                # 汎用システム最適化
                sync && echo 1 > /proc/sys/vm/drop_caches 2>/dev/null || true
                ;;
        esac
    fi
    
    log "✅ 適応型${pattern_type}完了"
}

# メイン処理
adaptive_${pattern_type}
ADAPTIVE_END
}

# 進化統計システム
generate_evolution_statistics() {
    log "📊 進化統計生成中..."
    
    local stats_file="system_evolution/evolution_statistics_$(date +%Y%m%d_%H%M%S).json"
    
    local total_automations=$(find scripts/ -name "auto_*.sh" -o -name "nextgen_*.sh" | wc -l)
    local recent_generations=$(find scripts/auto_generated/ -name "*.sh" -newermt "24 hours ago" | wc -l)
    local memory_files=$(find ai_memory/ -name "*.json" | wc -l)
    local evolution_cycles=$(find logs/ -name "*evolution*.log" | wc -l)
    
    cat << STATS_END > "$stats_file"
{
  "evolution_statistics": {
    "統計生成時刻": "$(date '+%Y-%m-%d %H:%M:%S')",
    "総自動化スクリプト数": $total_automations,
    "24時間新規生成数": $recent_generations,
    "AI記憶ファイル数": $memory_files,
    "進化サイクル実行回数": $evolution_cycles,
    "システム稼働日数": "$(echo "($(date +%s) - $(stat -c %Y ai_memory/storage/permanent/core_knowledge.json 2>/dev/null || echo $(date +%s))) / 86400" | bc -l 2>/dev/null || echo "1")",
    "進化効率": "$(echo "scale=2; $recent_generations / 24" | bc -l 2>/dev/null || echo "0.00")",
    "記憶蓄積率": "$(echo "scale=2; $memory_files / $evolution_cycles" | bc -l 2>/dev/null || echo "1.00")"
  }
}
STATS_END
    
    log "📈 進化統計完了: $stats_file"
}

# メイン進化サイクルv2.0
main_evolution_cycle_v2() {
    log "🧬 自己進化サイクルv2.0開始"
    
    # 1. 成功パターン検出
    local success_patterns=($(detect_success_patterns))
    
    # 2. 問題解決能力評価
    local solving_score
    evaluate_problem_solving
    solving_score=$?
    
    # 3. 次世代機能生成
    local generated_count=0
    for pattern in "${success_patterns[@]}"; do
        if [[ ! -z "$pattern" && "$pattern" =~ ^[a-zA-Z_]+: ]]; then
            generate_next_gen_feature "$pattern"
            generated_count=$((generated_count + 1))
        fi
    done
    
    # 4. 進化統計生成
    generate_evolution_statistics
    
    # 5. AI記憶システム更新
    cat << MEMORY_UPDATE > "ai_memory/storage/permanent/evolution_status_v2.json"
{
  "evolution_status_v2": {
    "更新時刻": "$(date '+%Y-%m-%d %H:%M:%S')",
    "問題解決能力": "${solving_score}%",
    "今回生成機能数": $generated_count,
    "累積自動化数": $(find scripts/ -name "auto_*.sh" -o -name "nextgen_*.sh" | wc -l),
    "進化レベル": "v2.0",
    "次回進化予定": "$(date -d '+2 hours' '+%Y-%m-%d %H:%M:%S')"
  }
}
MEMORY_UPDATE
    
    log "🎯 進化サイクルv2.0完了 - 問題解決能力: ${solving_score}%, 新機能: ${generated_count}個"
}

# 実行
main_evolution_cycle_v2

log "🧬 自己進化システムv2.0完了"
