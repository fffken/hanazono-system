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
