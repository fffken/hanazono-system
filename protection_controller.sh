#!/bin/bash
# Protection Controller - 鉄壁保護システム制御スクリプト

PROTECTION_DIR="/home/pi/lvyuan_solar_control"
LOG_FILE="$PROTECTION_DIR/logs/protection_system.log"

# ログ記録関数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 緊急停止関数
emergency_shutdown() {
    log_message "🚨 緊急停止発動: $1"
    
    # 危険な自動化プロセス全停止
    pkill -f "auto_" 2>/dev/null
    pkill -f "fix_" 2>/dev/null
    pkill -f "safe_mass_fix" 2>/dev/null
    
    # 緊急バックアップ
    BACKUP_DIR="$PROTECTION_DIR/EMERGENCY_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 聖域ファイル保護
    cp email_notifier.py "$BACKUP_DIR/" 2>/dev/null
    cp main.py "$BACKUP_DIR/" 2>/dev/null
    cp lvyuan_collector.py "$BACKUP_DIR/" 2>/dev/null
    cp settings.json "$BACKUP_DIR/" 2>/dev/null
    
    log_message "✅ 緊急バックアップ完了: $BACKUP_DIR"
}

# AI誤判断検知
detect_ai_errors() {
    # 危険なコマンドパターン検知
    if pgrep -f "find.*-exec.*sed" >/dev/null; then
        emergency_shutdown "AI一括sed実行検知"
        return 1
    fi
    
    if pgrep -f "while.*sed" >/dev/null; then
        emergency_shutdown "AIループsed実行検知"
        return 1
    fi
    
    return 0
}

# 重要機能監視
monitor_critical_functions() {
    cd "$PROTECTION_DIR" || exit 1
    
    # メール機能チェック
    if ! timeout 30 python3 email_notifier.py --send-test-email >/dev/null 2>&1; then
        log_message "❌ メール機能異常検知"
        emergency_shutdown "メール機能停止"
        return 1
    fi
    
    # データ収集チェック
    if ! timeout 30 python3 lvyuan_collector.py --collect >/dev/null 2>&1; then
        log_message "❌ データ収集異常検知"
        emergency_shutdown "データ収集停止"
        return 1
    fi
    
    # メインシステムチェック
    if ! timeout 30 python3 main.py --check-cron >/dev/null 2>&1; then
        log_message "❌ メインシステム異常検知"
        emergency_shutdown "メインシステム停止"
        return 1
    fi
    
    log_message "✅ 全重要機能正常"
    return 0
}

# メイン監視ループ
main_protection_loop() {
    log_message "🛡️ HANAZONO鉄壁保護システム開始"
    
    while true; do
        # AI誤判断検知
        if ! detect_ai_errors; then
            log_message "🚨 AI誤判断による緊急停止実行"
            break
        fi
        
        # 重要機能監視
        if ! monitor_critical_functions; then
            log_message "🚨 重要機能異常による緊急停止実行"
            break
        fi
        
        sleep 60  # 1分間隔監視
    done
}

# 引数処理
case "${1:-start}" in
    "start")
        main_protection_loop
        ;;
    "stop")
        log_message "🛡️ 保護システム手動停止"
        pkill -f "protection_controller"
        ;;
    "emergency")
        emergency_shutdown "手動緊急停止"
        ;;
    "test")
        log_message "🧪 保護システムテスト実行"
        monitor_critical_functions
        ;;
    *)
        echo "使用法: $0 {start|stop|emergency|test}"
        exit 1
        ;;
esac

