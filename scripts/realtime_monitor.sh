#!/bin/bash
# HANAZONOシステム リアルタイム監視システム v1.0
# 常時監視・異常検知・自動対応

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 設定
MONITOR_INTERVAL=30  # 30秒間隔での監視
LOG_DIR="monitoring_logs"
ALERT_LOG="$LOG_DIR/alerts.log"
SYSTEM_LOG="$LOG_DIR/system_monitor.log"
PID_FILE="/tmp/hanazono_monitor.pid"

# 監視対象設定
declare -a CRITICAL_FILES=("main.py" "email_notifier.py" "settings.json" "lvyuan_collector.py")
declare -a CRITICAL_PROCESSES=("python3")
declare -A THRESHOLDS=(
    ["cpu_usage"]=80
    ["memory_usage"]=85
    ["disk_usage"]=90
    ["temperature"]=70
)

echo -e "${PURPLE}=== HANAZONOシステム リアルタイム監視システム v1.0 ===${NC}"

# 初期化
initialize_monitor() {
    echo -e "${BLUE}🔧 リアルタイム監視システム初期化中...${NC}"
    
    # ログディレクトリ作成
    mkdir -p $LOG_DIR
    
    # 監視開始ログ
    echo "$(date '+%Y-%m-%d %H:%M:%S') - リアルタイム監視システム開始" >> $SYSTEM_LOG
    
    # PIDファイル作成
    echo $$ > $PID_FILE
    
    echo -e "${GREEN}✅ 初期化完了${NC}"
}

# システムリソース監視
monitor_system_resources() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # CPU使用率
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    cpu_usage=${cpu_usage%.*}  # 小数点削除
    
    # メモリ使用率
    local memory_usage=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
    
    # ディスク使用率
    local disk_usage=$(df -h . | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    
    # 温度（Raspberry Pi用）
    local temperature="N/A"
    if [ -f "/sys/class/thermal/thermal_zone0/temp" ]; then
        temperature=$(($(cat /sys/class/thermal/thermal_zone0/temp) / 1000))
    fi
    
    # ログ記録
    echo "$timestamp,CPU:${cpu_usage}%,MEM:${memory_usage}%,DISK:${disk_usage}%,TEMP:${temperature}°C" >> $SYSTEM_LOG
    
    # 閾値チェック
    check_thresholds "$cpu_usage" "$memory_usage" "$disk_usage" "$temperature"
    
    # リアルタイム表示
    printf "\r${CYAN}📊 %s | CPU:%s%% MEM:%s%% DISK:%s%% TEMP:%s°C${NC}" \
           "$(date '+%H:%M:%S')" "$cpu_usage" "$memory_usage" "$disk_usage" "$temperature"
}

# 閾値チェック・アラート
check_thresholds() {
    local cpu=$1 memory=$2 disk=$3 temp=$4
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local alerts=()
    
    # CPU使用率チェック
    if [ "$cpu" -gt "${THRESHOLDS[cpu_usage]}" ]; then
        alerts+=("🔥 CPU使用率異常: ${cpu}% (閾値: ${THRESHOLDS[cpu_usage]}%)")
        trigger_auto_response "high_cpu" "$cpu"
    fi
    
    # メモリ使用率チェック
    if [ "$memory" -gt "${THRESHOLDS[memory_usage]}" ]; then
        alerts+=("💾 メモリ使用率異常: ${memory}% (閾値: ${THRESHOLDS[memory_usage]}%)")
        trigger_auto_response "high_memory" "$memory"
    fi
    
    # ディスク使用率チェック
    if [ "$disk" -gt "${THRESHOLDS[disk_usage]}" ]; then
        alerts+=("🗂️ ディスク使用率異常: ${disk}% (閾値: ${THRESHOLDS[disk_usage]}%)")
        trigger_auto_response "high_disk" "$disk"
    fi
    
    # 温度チェック（数値の場合のみ）
    if [[ "$temp" =~ ^[0-9]+$ ]] && [ "$temp" -gt "${THRESHOLDS[temperature]}" ]; then
        alerts+=("🌡️ 温度異常: ${temp}°C (閾値: ${THRESHOLDS[temperature]}°C)")
        trigger_auto_response "high_temperature" "$temp"
    fi
    
    # アラート出力
    for alert in "${alerts[@]}"; do
        echo -e "\n${RED}🚨 $timestamp - $alert${NC}"
        echo "$timestamp - $alert" >> $ALERT_LOG
    done
}

# ファイル変更監視
monitor_file_changes() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    for file in "${CRITICAL_FILES[@]}"; do
        if [ -f "$file" ]; then
            # ファイルのハッシュを計算
            local current_hash=$(md5sum "$file" | cut -d' ' -f1)
            local hash_file="$LOG_DIR/hash_${file//\//_}"
            
            if [ -f "$hash_file" ]; then
                local previous_hash=$(cat "$hash_file")
                if [ "$current_hash" != "$previous_hash" ]; then
                    echo -e "\n${YELLOW}📝 $timestamp - ファイル変更検出: $file${NC}"
                    echo "$timestamp - ファイル変更検出: $file" >> $ALERT_LOG
                    
                    # 自動バックアップトリガー
                    trigger_auto_response "file_changed" "$file"
                fi
            fi
            
            # 現在のハッシュを保存
            echo "$current_hash" > "$hash_file"
        fi
    done
}

# プロセス監視
monitor_processes() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    for process in "${CRITICAL_PROCESSES[@]}"; do
        local process_count=$(pgrep -c "$process")
        local process_file="$LOG_DIR/process_${process}"
        
        # プロセース数の変化をチェック
        if [ -f "$process_file" ]; then
            local previous_count=$(cat "$process_file")
            if [ "$process_count" -ne "$previous_count" ]; then
                if [ "$process_count" -eq 0 ]; then
                    echo -e "\n${RED}💀 $timestamp - 重要プロセス停止: $process${NC}"
                    echo "$timestamp - 重要プロセス停止: $process" >> $ALERT_LOG
                    trigger_auto_response "process_stopped" "$process"
                elif [ "$process_count" -gt "$previous_count" ]; then
                    echo -e "\n${GREEN}🚀 $timestamp - プロセス開始: $process (数: $process_count)${NC}"
                    echo "$timestamp - プロセス開始: $process (数: $process_count)" >> $ALERT_LOG
                fi
            fi
        fi
        
        # プロセス数を保存
        echo "$process_count" > "$process_file"
    done
}

# Git変更監視
monitor_git_changes() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local changes=$(git status --porcelain | wc -l)
    local git_file="$LOG_DIR/git_changes"
    
    if [ -f "$git_file" ]; then
        local previous_changes=$(cat "$git_file")
        if [ "$changes" -ne "$previous_changes" ]; then
            if [ "$changes" -gt "$previous_changes" ]; then
                echo -e "\n${BLUE}📋 $timestamp - Git変更増加: $previous_changes → $changes 件${NC}"
                echo "$timestamp - Git変更増加: $previous_changes → $changes 件" >> $ALERT_LOG
                
                # 変更が多すぎる場合の警告
                if [ "$changes" -gt 20 ]; then
                    trigger_auto_response "too_many_git_changes" "$changes"
                fi
            fi
        fi
    fi
    
    echo "$changes" > "$git_file"
}

# 自動対応システム
trigger_auto_response() {
    local issue_type=$1
    local value=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo -e "\n${PURPLE}🤖 $timestamp - 自動対応システム起動: $issue_type${NC}"
    
    case $issue_type in
        "high_cpu")
            # CPU使用率が高い場合の自動対応
            echo "  📊 CPU使用率分析中..."
            ps aux --sort=-%cpu | head -5 >> $ALERT_LOG
            
            # 必要に応じて重いプロセスを特定
            local heavy_process=$(ps aux --sort=-%cpu | head -2 | tail -1 | awk '{print $11}')
            echo "  🎯 最も重いプロセス: $heavy_process"
            ;;
            
        "high_memory")
            # メモリ使用率が高い場合の自動対応
            echo "  💾 メモリ使用状況分析中..."
            ps aux --sort=-%mem | head -5 >> $ALERT_LOG
            
            # ガベージコレクション実行の提案
            echo "  🧹 システムクリーンアップ推奨"
            ;;
            
        "high_disk")
            # ディスク使用率が高い場合の自動対応
            echo "  🗂️ ディスク使用状況分析中..."
            du -h . | sort -hr | head -10 >> $ALERT_LOG
            
            # 一時ファイルの自動クリーンアップ
            find . -name "*.tmp" -delete 2>/dev/null
            find . -name "*.backup_*" -mtime +7 -delete 2>/dev/null
            echo "  🧹 一時ファイル自動削除完了"
            ;;
            
        "high_temperature")
            # 温度が高い場合の自動対応
            echo "  🌡️ 温度監視強化モード開始"
            # CPUクロック制限やファン制御の提案
            ;;
            
        "file_changed")
            # ファイル変更の自動対応
            echo "  📝 ファイル変更: $value"
            echo "  💾 自動バックアップ実行中..."
            
            # 自動バックアップ実行
            backup_file="backup_$(date +%Y%m%d_%H%M%S)_$(basename $value)"
            cp "$value" "$LOG_DIR/$backup_file"
            echo "  ✅ バックアップ完了: $backup_file"
            ;;
            
        "process_stopped")
            # プロセス停止の自動対応
            echo "  💀 プロセス停止検出: $value"
            echo "  🔄 自動再起動を検討中..."
            # 必要に応じて自動再起動ロジック
            ;;
            
        "too_many_git_changes")
            # Git変更が多すぎる場合
            echo "  📋 Git変更過多: $value 件"
            echo "  📊 変更内容分析中..."
            git status --short >> $ALERT_LOG
            echo "  💡 整理を推奨します"
            ;;
    esac
    
    echo "$timestamp - 自動対応完了: $issue_type" >> $ALERT_LOG
}

# ヘルスチェック
health_check() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local health_score=100
    local issues=()
    
    # 各種チェック
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    cpu_usage=${cpu_usage%.*}
    
    if [ "$cpu_usage" -gt 80 ]; then
        health_score=$((health_score - 20))
        issues+=("CPU高負荷")
    fi
    
    # Pythonプロセスチェック
    if [ $(pgrep -c python3) -eq 0 ]; then
        health_score=$((health_score - 30))
        issues+=("Pythonプロセス未実行")
    fi
    
    # 重要ファイル存在チェック
    for file in "${CRITICAL_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            health_score=$((health_score - 15))
            issues+=("重要ファイル不存在: $file")
        fi
    done
    
    # ヘルススコア表示
    if [ $health_score -ge 90 ]; then
        echo -e "\n${GREEN}💚 システムヘルス: ${health_score}/100 (優秀)${NC}"
    elif [ $health_score -ge 70 ]; then
        echo -e "\n${YELLOW}💛 システムヘルス: ${health_score}/100 (良好)${NC}"
    else
        echo -e "\n${RED}❤️ システムヘルス: ${health_score}/100 (要注意)${NC}"
    fi
    
    # 問題がある場合
    if [ ${#issues[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️ 検出された問題:${NC}"
        for issue in "${issues[@]}"; do
            echo "  - $issue"
        done
    fi
    
    echo "$timestamp - ヘルススコア: $health_score" >> $SYSTEM_LOG
}

# メイン監視ループ
main_monitor_loop() {
    echo -e "${GREEN}🚀 リアルタイム監視開始 (間隔: ${MONITOR_INTERVAL}秒)${NC}"
    echo -e "${CYAN}📊 Ctrl+C で停止${NC}"
    
    local cycle_count=0
    
    while true; do
        cycle_count=$((cycle_count + 1))
        
        # 基本システム監視
        monitor_system_resources
        
        # 5分ごとの詳細チェック
        if [ $((cycle_count % 10)) -eq 0 ]; then
            echo -e "\n${BLUE}🔍 詳細チェック実行中...${NC}"
            monitor_file_changes
            monitor_processes
            monitor_git_changes
            health_check
        fi
        
        sleep $MONITOR_INTERVAL
    done
}

# 停止処理
cleanup() {
    echo -e "\n${YELLOW}🛑 リアルタイム監視停止中...${NC}"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - リアルタイム監視システム停止" >> $SYSTEM_LOG
    rm -f $PID_FILE
    echo -e "${GREEN}✅ 監視システム正常停止${NC}"
    exit 0
}

# シグナルハンドリング
trap cleanup SIGINT SIGTERM

# メイン実行
main() {
    # 重複起動チェック
    if [ -f $PID_FILE ]; then
        local existing_pid=$(cat $PID_FILE)
        if kill -0 $existing_pid 2>/dev/null; then
            echo -e "${RED}❌ 監視システムは既に実行中です (PID: $existing_pid)${NC}"
            exit 1
        else
            rm -f $PID_FILE
        fi
    fi
    
    initialize_monitor
    main_monitor_loop
}

# 引数チェック
case "${1:-start}" in
    "start")
        main
        ;;
    "stop")
        if [ -f $PID_FILE ]; then
            local pid=$(cat $PID_FILE)
            kill $pid 2>/dev/null && echo "監視システム停止" || echo "監視システムは実行されていません"
        else
            echo "監視システムは実行されていません"
        fi
        ;;
    "status")
        if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE) 2>/dev/null; then
            echo "監視システムは実行中です"
            tail -5 $SYSTEM_LOG
        else
            echo "監視システムは停止中です"
        fi
        ;;
    *)
        echo "使用方法: $0 [start|stop|status]"
        ;;
esac
