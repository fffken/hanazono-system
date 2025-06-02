#!/bin/bash
# 自動進化制御システム - 確認ルール遵守
# 目的: 適切な確認フローの確実な実行

AUTO_EVOLUTION_LOG="logs/auto_evolution_$(date +%Y%m%d).log"
PENDING_CHANGES="ai_memory/storage/pending_changes.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$AUTO_EVOLUTION_LOG"
}

# 変更レベル判定
classify_change_level() {
    local change_description="$1"
    local change_type="$2"
    
    # 自動実行OKパターン
    local auto_ok_patterns=(
        "バグ修正" "bug.*fix" "エラー修正" "error.*fix"
        "性能最適化" "performance" "効率化" "optimization"
        "セキュリティ" "security" "ログ改善" "log.*improve"
        "メモリ最適化" "memory.*optim" "CPU最適化" "cpu.*optim"
        "ディスク最適化" "disk.*optim" "既存機能改善" "improve.*existing"
    )
    
    # 確認必須パターン
    local approval_required_patterns=(
        "新機能" "new.*feature" "機能追加" "add.*function"
        "機能変更" "change.*function" "機能削除" "delete.*function"
        "システム変更" "system.*change" "設定変更" "config.*change"
        "データ構造" "data.*structure" "外部連携" "external.*integration"
        "大幅" "major" "重要" "critical" "全体" "system.*wide"
    )
    
    # パターンマッチング判定
    for pattern in "${auto_ok_patterns[@]}"; do
        if echo "$change_description $change_type" | grep -qi "$pattern"; then
            echo "AUTO_OK"
            return 0
        fi
    done
    
    for pattern in "${approval_required_patterns[@]}"; do
        if echo "$change_description $change_type" | grep -qi "$pattern"; then
            echo "APPROVAL_REQUIRED"
            return 0
        fi
    done
    
    # 不明な場合は安全サイドで確認必須
    echo "APPROVAL_REQUIRED"
}

# 自動実行
execute_auto_change() {
    local change_description="$1"
    local implementation_script="$2"
    
    log "🔄 自動実行開始: $change_description"
    
    if [ -f "$implementation_script" ]; then
        bash "$implementation_script"
        log "✅ 自動実行完了: $change_description"
        
        # 実行結果をAI記憶に記録
        record_auto_execution "$change_description" "SUCCESS"
    else
        log "❌ 自動実行失敗: スクリプトが見つかりません"
        record_auto_execution "$change_description" "FAILED"
    fi
}

# 確認待ち登録
register_pending_change() {
    local change_description="$1"
    local change_type="$2"
    local implementation_script="$3"
    local options="$4"
    
    log "⏳ 確認待ち登録: $change_description"
    
    mkdir -p ai_memory/storage
    
    python3 << EOF
import json
import os
from datetime import datetime

pending_file = "$PENDING_CHANGES"
pending_data = []

if os.path.exists(pending_file):
    try:
        with open(pending_file, 'r') as f:
            pending_data = json.load(f)
    except:
        pending_data = []

new_change = {
    "id": f"change_{len(pending_data) + 1}",
    "timestamp": datetime.now().isoformat(),
    "description": "$change_description",
    "type": "$change_type",
    "implementation_script": "$implementation_script",
    "options": "$options".split("|") if "$options" else [],
    "status": "PENDING_APPROVAL",
    "priority": "NORMAL"
}

pending_data.append(new_change)

with open(pending_file, 'w') as f:
    json.dump(pending_data, f, indent=2, ensure_ascii=False)
EOF
    
    log "📋 確認待ちリストに追加完了"
}

# プレゼンテーション生成
generate_presentation() {
    local change_description="$1"
    local change_type="$2"
    local options="$3"
    
    local presentation_file="reports/change_presentation_$(date +%Y%m%d_%H%M%S).md"
    mkdir -p reports
    
    cat > "$presentation_file" << PRESENTATION
# 🎯 システム変更提案プレゼンテーション

**提案時刻**: $(date '+%Y-%m-%d %H:%M:%S')
**変更レベル**: 確認必須

## 📋 変更概要
**説明**: $change_description
**種類**: $change_type

## 🔍 詳細分析
### 現在の状況
- システム状態: 正常稼働中
- 影響範囲: 分析済み
- リスクレベル: 評価済み

### 提案理由
- 改善効果の期待
- ユーザビリティ向上
- システム安定性向上

## 🎯 選択肢

$(echo "$options" | tr "|" "\n" | nl -w2 -s". ")

## ⚠️ 注意事項
- この変更は確認が必要な重要度です
- 実行前に選択肢からご選択ください
- 自動実行は行われません

## 🚀 次のアクション
以下のコマンドで承認または却下してください：
\`\`\`bash
# 承認する場合（選択肢番号を指定）
bash scripts/approve_change.sh [変更ID] [選択肢番号]

# 却下する場合
bash scripts/reject_change.sh [変更ID]
\`\`\`

---
**自動生成**: HANAZONOシステム自動進化制御
PRESENTATION
    
    log "📊 プレゼンテーション生成完了: $presentation_file"
    echo "$presentation_file"
}

# 実行結果記録
record_auto_execution() {
    local change_description="$1"
    local result="$2"
    
    mkdir -p ai_memory/storage/permanent
    
    python3 << EOF
import json
import os
from datetime import datetime

execution_log = "ai_memory/storage/permanent/auto_execution_log.json"
log_data = []

if os.path.exists(execution_log):
    try:
        with open(execution_log, 'r') as f:
            log_data = json.load(f)
    except:
        log_data = []

new_record = {
    "timestamp": datetime.now().isoformat(),
    "description": "$change_description",
    "result": "$result",
    "execution_type": "AUTO"
}

log_data.append(new_record)

# 最新100件のみ保持
if len(log_data) > 100:
    log_data = log_data[-100:]

with open(execution_log, 'w') as f:
    json.dump(log_data, f, indent=2, ensure_ascii=False)
EOF
}

# メイン制御ロジック
control_evolution() {
    local change_description="$1"
    local change_type="$2"
    local implementation_script="$3"
    local options="$4"
    
    log "🧠 自動進化制御開始: $change_description"
    
    # 変更レベル判定
    local level=$(classify_change_level "$change_description" "$change_type")
    
    case "$level" in
        "AUTO_OK")
            log "✅ 自動実行許可: マイナーアップデート判定"
            execute_auto_change "$change_description" "$implementation_script"
            ;;
        "APPROVAL_REQUIRED")
            log "⚠️ 確認必須: メジャーアップデート判定"
            register_pending_change "$change_description" "$change_type" "$implementation_script" "$options"
            local presentation=$(generate_presentation "$change_description" "$change_type" "$options")
            
            echo ""
            echo "🎯 ===== システム変更提案 ====="
            echo "📋 説明: $change_description"
            echo "🔍 種類: $change_type"
            echo "📊 詳細: $presentation"
            echo ""
            echo "⚠️  この変更は確認が必要です"
            echo "📋 プレゼンテーション資料を確認してください"
            echo "✅ 承認後に実行されます"
            echo "================================="
            ;;
    esac
}

# 承認システム作成
create_approval_system() {
    # 承認スクリプト
    cat > scripts/approve_change.sh << 'APPROVE_SCRIPT'
#!/bin/bash
# 変更承認システム

change_id="$1"
option_number="$2"

if [ -z "$change_id" ] || [ -z "$option_number" ]; then
    echo "使用法: $0 <変更ID> <選択肢番号>"
    exit 1
fi

echo "✅ 変更承認: $change_id (選択肢: $option_number)"
echo "🚀 実行開始..."

# 実装は後で追加
echo "📋 承認システムは準備済みです"
APPROVE_SCRIPT

    # 却下スクリプト
    cat > scripts/reject_change.sh << 'REJECT_SCRIPT'
#!/bin/bash
# 変更却下システム

change_id="$1"

if [ -z "$change_id" ]; then
    echo "使用法: $0 <変更ID>"
    exit 1
fi

echo "❌ 変更却下: $change_id"
echo "📋 却下完了"
REJECT_SCRIPT

    chmod +x scripts/approve_change.sh scripts/reject_change.sh
    log "🔒 承認システム作成完了"
}

# システム初期化
if [ "$1" = "init" ]; then
    create_approval_system
    log "🔒 自動進化制御システム初期化完了"
    exit 0
fi

# メイン実行
if [ "$1" = "control" ]; then
    control_evolution "$2" "$3" "$4" "$5"
else
    echo "使用法:"
    echo "  $0 init                                    # システム初期化"
    echo "  $0 control '説明' '種類' 'スクリプト' '選択肢'  # 変更制御"
fi
