#!/bin/bash
# HANAZONOシステム 完全自動Git保存システム v1.0
# 目的: 人間の意識なしに適切なGit保存を自動実行

set -e

# ログ設定
LOG_DIR="logs/auto_git_save"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/auto_save_$(date +%Y%m%d_%H%M%S).log"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🤖 自動Git保存システム開始"

# 現在のディレクトリを確認
if [ ! -d ".git" ]; then
    log "❌ Gitリポジトリではありません"
    exit 1
fi

log "📊 変更状況確認中..."

# 変更ファイル数をカウント
MODIFIED_COUNT=$(git status --porcelain | grep "^ M" | wc -l)
UNTRACKED_COUNT=$(git status --porcelain | grep "^??" | wc -l)
TOTAL_CHANGES=$((MODIFIED_COUNT + UNTRACKED_COUNT))

log "📋 変更状況: 修正 ${MODIFIED_COUNT}件, 新規 ${UNTRACKED_COUNT}件, 合計 ${TOTAL_CHANGES}件"

# 変更がない場合は終了
if [ $TOTAL_CHANGES -eq 0 ]; then
    log "✅ 変更なし - 保存不要"
    exit 0
fi

# AI記憶システムファイルを優先追加
log "🧠 AI記憶システムファイル優先保存中..."
git add ai_memory/storage/permanent/ 2>/dev/null || true

# 重要ドキュメントを追加
log "📄 重要ドキュメント保存中..."
git add *.md 2>/dev/null || true
git add docs/ 2>/dev/null || true

# 設定ファイルを追加
log "⚙️ 設定ファイル保存中..."
git add *.json 2>/dev/null || true

# ログファイルを追加（選択的）
log "📝 ログファイル保存中..."
git add logs/ 2>/dev/null || true

# system_backupsは除外（容量対策）
log "🗂️ 大容量バックアップは除外..."

# コミットメッセージを自動生成
COMMIT_MSG="🤖 自動保存: $(date '+%Y-%m-%d %H:%M') - AI記憶システム更新 (${TOTAL_CHANGES}件)"

# コミット実行
log "💾 コミット実行中..."
if git commit -m "$COMMIT_MSG"; then
    log "✅ コミット成功: $COMMIT_MSG"
else
    log "⚠️ コミット失敗またはコミット対象なし"
    exit 0
fi

# プッシュ実行
log "🚀 GitHub保存中..."
if git push origin main; then
    log "✅ GitHub保存成功"
else
    log "❌ GitHub保存失敗"
    exit 1
fi

log "🎉 自動Git保存完了"
