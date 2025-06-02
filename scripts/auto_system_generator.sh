#!/bin/bash
# 自動化システム自動生成エンジン v1.0
# 目的: 修正作業を検出し、自動で自動化システムを生成

set -e

LOG_FILE="logs/auto_system_generator_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🤖 自動化システム自動生成エンジン開始"

# 作業パターン検出システム
detect_work_patterns() {
    log "🔍 手動作業パターン検出中..."
    
    # ログファイルから手動作業を分析
    RECENT_LOGS=$(find logs/ -name "*.log" -newermt "1 hour ago" 2>/dev/null)
    
    local patterns_found=()
    
    # パターン1: cron関連作業
    if grep -q "cron\|crontab" $RECENT_LOGS 2>/dev/null; then
        patterns_found+=("cron_management")
        log "📋 検出: cron管理作業パターン"
    fi
    
    # パターン2: 構文エラー修正
    if grep -q "構文エラー\|syntax.*error\|修正" $RECENT_LOGS 2>/dev/null; then
        patterns_found+=("syntax_fixing")
        log "📋 検出: 構文エラー修正パターン"
    fi
    
    # パターン3: ファイル修正作業
    if grep -q "nano\|修正\|fix" $RECENT_LOGS 2>/dev/null; then
        patterns_found+=("file_editing")
        log "📋 検出: ファイル編集パターン"
    fi
    
    # パターン4: 権限設定作業
    if grep -q "chmod\|permission\|権限" $RECENT_LOGS 2>/dev/null; then
        patterns_found+=("permission_management")
        log "📋 検出: 権限管理パターン"
    fi
    
    echo "${patterns_found[@]}"
}

# 自動化システム生成
generate_automation_system() {
    local pattern="$1"
    local script_name="auto_${pattern}_system.sh"
    local script_path="scripts/generated/${script_name}"
    
    mkdir -p scripts/generated
    
    log "🛠️ ${pattern}の自動化システム生成中..."
    
    case "$pattern" in
        "cron_management")
            generate_cron_auto_system "$script_path"
            ;;
        "syntax_fixing")
            generate_syntax_auto_system "$script_path"
            ;;
        "file_editing")
            generate_file_edit_auto_system "$script_path"
            ;;
        "permission_management")
            generate_permission_auto_system "$script_path"
            ;;
        *)
            generate_generic_auto_system "$script_path" "$pattern"
            ;;
    esac
    
    chmod +x "$script_path"
    log "✅ 自動化システム生成完了: $script_path"
}

# cron自動管理システム生成
generate_cron_auto_system() {
    local script_path="$1"
    
    cat << 'CRON_AUTO_END' > "$script_path"
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
CRON_AUTO_END
}

# 構文エラー自動修正システム生成
generate_syntax_auto_system() {
    local script_path="$1"
    
    cat << 'SYNTAX_AUTO_END' > "$script_path"
#!/bin/bash
# 自動生成: 構文エラー完全自動修正システム
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_syntax_fix_$(date +%Y%m%d).log"
}

# 構文エラー検出・修正
auto_fix_syntax() {
    local target_dir="${1:-.}"
    
    log "🔍 構文エラー検出中: $target_dir"
    
    # Python構文チェック
    find "$target_dir" -name "*.py" -exec python3 -m py_compile {} \; 2>/dev/null || {
        log "🔧 Python構文エラー修正中"
        # 基本的な構文修正パターン
        find "$target_dir" -name "*.py" -exec sed -i 's/print /print(/g; s/$/)/g' {} \;
    }
    
    # Bash構文チェック
    find "$target_dir" -name "*.sh" -exec bash -n {} \; 2>/dev/null || {
        log "🔧 Bash構文エラー修正中"
        # 基本的なBash修正パターン
        find "$target_dir" -name "*.sh" -exec sed -i 's/\*\*/*/g; s/\*\([a-z]\)/* \1/g' {} \;
    }
    
    log "✅ 構文エラー自動修正完了"
}

# メイン処理
auto_fix_syntax "$1"
SYNTAX_AUTO_END
}

# ファイル編集自動化システム生成
generate_file_edit_auto_system() {
    local script_path="$1"
    
    cat << 'FILE_AUTO_END' > "$script_path"
#!/bin/bash
# 自動生成: ファイル編集完全自動化システム
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_file_edit_$(date +%Y%m%d).log"
}

# 自動ファイル修正
auto_edit_files() {
    log "🔧 ファイル自動編集開始"
    
    # よくある問題パターンの自動修正
    find . -name "*.py" -o -name "*.sh" -o -name "*.json" | while read file; do
        # バックアップ作成
        cp "$file" "${file}.auto_backup_$(date +%Y%m%d_%H%M%S)"
        
        # 基本的な修正パターン適用
        case "$file" in
            *.py)
                # Python特有の修正
                sed -i 's/print /print(/g' "$file" 2>/dev/null || true
                ;;
            *.sh)
                # Bash特有の修正
                sed -i 's/\*\*/*/g' "$file" 2>/dev/null || true
                ;;
            *.json)
                # JSON整形
                python3 -m json.tool "$file" > "${file}.tmp" && mv "${file}.tmp" "$file" 2>/dev/null || true
                ;;
        esac
    done
    
    log "✅ ファイル自動編集完了"
}

# メイン処理
auto_edit_files
FILE_AUTO_END
}

# 権限管理自動化システム生成
generate_permission_auto_system() {
    local script_path="$1"
    
    cat << 'PERMISSION_AUTO_END' > "$script_path"
#!/bin/bash
# 自動生成: 権限管理完全自動化システム
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_permission_$(date +%Y%m%d).log"
}

# 権限自動設定
auto_set_permissions() {
    log "🔧 権限自動設定開始"
    
    # スクリプトファイルに実行権限
    find scripts/ -name "*.sh" -exec chmod +x {} \; 2>/dev/null
    
    # Pythonファイルに適切な権限
    find . -name "*.py" -exec chmod 644 {} \; 2>/dev/null
    
    # 設定ファイルに適切な権限
    find . -name "*.json" -o -name "*.conf" -o -name "*.cfg" -exec chmod 644 {} \; 2>/dev/null
    
    # ログディレクトリの権限
    find logs/ -type d -exec chmod 755 {} \; 2>/dev/null
    find logs/ -type f -exec chmod 644 {} \; 2>/dev/null
    
    log "✅ 権限自動設定完了"
}

# メイン処理
auto_set_permissions
PERMISSION_AUTO_END
}

# 汎用自動化システム生成
generate_generic_auto_system() {
    local script_path="$1"
    local pattern="$2"
    
    cat << GENERIC_AUTO_END > "$script_path"
#!/bin/bash
# 自動生成: ${pattern}自動化システム
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_${pattern}_$(date +%Y%m%d).log"
}

# ${pattern}自動処理
auto_handle_${pattern}() {
    log "🔧 ${pattern}自動処理開始"
    
    # パターン固有の処理をここに追加
    # 現在は基本的なシステムヘルスチェック
    
    # ディスク容量チェック
    if [ \$(df / | tail -1 | awk '{print \$5}' | sed 's/%//') -gt 80 ]; then
        log "⚠️ ディスク容量警告"
        # 自動クリーンアップ
        find /tmp -type f -mtime +7 -delete 2>/dev/null || true
    fi
    
    # メモリ使用量チェック
    if [ \$(free | grep Mem | awk '{print (\$3/\$2) * 100.0}' | cut -d. -f1) -gt 80 ]; then
        log "⚠️ メモリ使用量警告"
        # キャッシュクリア
        sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
    fi
    
    log "✅ ${pattern}自動処理完了"
}

# メイン処理
auto_handle_${pattern}
GENERIC_AUTO_END
}

# 自動化システム統合管理
integrate_automation_systems() {
    log "🔗 自動化システム統合中..."
    
    # 統合実行スクリプト生成
    cat << 'INTEGRATION_END' > scripts/run_all_automations.sh
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
INTEGRATION_END
    
    chmod +x scripts/run_all_automations.sh
    
    # cron統合
    if ! crontab -l 2>/dev/null | grep -q "run_all_automations"; then
        (crontab -l 2>/dev/null; echo "0 */6 * * * cd /home/pi/lvyuan_solar_control && bash scripts/run_all_automations.sh >> logs/all_automations.log 2>&1") | crontab -
        log "📅 6時間ごと自動実行をcronに追加"
    fi
}

# メイン処理
main() {
    local detected_patterns=($(detect_work_patterns))
    
    if [ ${#detected_patterns[@]} -eq 0 ]; then
        log "✅ 新しい手動作業パターンは検出されませんでした"
        return 0
    fi
    
    log "🎯 ${#detected_patterns[@]}個の作業パターンを検出"
    
    for pattern in "${detected_patterns[@]}"; do
        generate_automation_system "$pattern"
    done
    
    integrate_automation_systems
    
    log "🎉 自動化システム自動生成完了"
}

# 実行
main
