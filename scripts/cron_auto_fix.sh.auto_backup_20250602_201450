#!/bin/bash
# cron構文自動修正システム v1.0
# 既存のauto_fix_systemと連携

source scripts/auto_fix_system.sh

cron_auto_fix() {
    echo "🔧 cron構文自動修正開始"
    
    # 現在のcrontabをバックアップ
    BACKUP_FILE="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S)"
    crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "" > "$BACKUP_FILE"
    echo "📁 バックアップ: $BACKUP_FILE"
    
    # 修正版生成
    FIXED_FILE="/tmp/crontab_fixed_$(date +%Y%m%d_%H%M%S)"
    
    # cron修正ルール適用
    while IFS= read -r line; do
        if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
            echo "$line" >> "$FIXED_FILE"
        else
            # 修正適用
            fixed_line="$line"
            fixed_line=$(echo "$fixed_line" | sed 's/\*\*\*/\*/g')
            fixed_line=$(echo "$fixed_line" | sed 's/\*\*/\*/g')
            fixed_line=$(echo "$fixed_line" | sed 's/\*cd/ \* cd/g')
            fixed_line=$(echo "$fixed_line" | sed 's/  \+/ /g')
            echo "$fixed_line" >> "$FIXED_FILE"
        fi
    done < "$BACKUP_FILE"
    
    # 修正版を適用
    crontab "$FIXED_FILE"
    echo "✅ cron修正完了"
    
    # 確認
    echo "📋 修正後のcron設定:"
    crontab -l | head -5
}

# 実行
cron_auto_fix
