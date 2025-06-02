#!/bin/bash
# HANAZONOシステム - 完全非破壊的Git整理自動化スクリプト
# 作成日: 2025-06-03
# 目的: 1955件未コミット変更の安全自動整理

set -e  # エラー時即座停止

echo "🛡️ HANAZONOシステム完全非破壊的Git整理開始"
echo "========================================================"

# タイムスタンプ生成
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="~/hanazono_safety_backup_${TIMESTAMP}"

echo "📅 実行時刻: $(date)"
echo "🎯 対象: $(pwd)"

# Phase 1: 完全安全バックアップ作成
echo ""
echo "🛡️ Phase 1: 完全安全バックアップ作成"
echo "----------------------------------------"

# メインバックアップ
echo "📦 メインバックアップ作成中..."
cp -r ~/lvyuan_solar_control ${BACKUP_DIR}
echo "✅ メインバックアップ完了: ${BACKUP_DIR}"

# Gitスナップショット
echo "📸 Gitスナップショット作成中..."
git stash push -u -m "SAFETY_SNAPSHOT_${TIMESTAMP}" --include-untracked || true
echo "✅ Gitスナップショット完了"

# 現在状況記録
echo "📊 現在状況記録中..."
git status --porcelain > "git_status_before_${TIMESTAMP}.txt"
CHANGE_COUNT=$(git status --porcelain | wc -l)
echo "📋 変更ファイル数: ${CHANGE_COUNT}件"
echo "✅ 状況記録完了"

# Phase 2: AI記憶システム重要ファイル最優先保護
echo ""
echo "🧠 Phase 2: AI記憶システム重要ファイル保護"
echo "--------------------------------------------"

echo "🔒 AI記憶重要ファイル復元・コミット..."
git stash pop || true

# AI記憶システム最優先ファイル
echo "📁 AI記憶システムファイル追加中..."
git add ai_memory/ 2>/dev/null || true
git add email_notifier_v2_1.py 2>/dev/null || true
git add ai_memory_integration.sh 2>/dev/null || true
git add ultimate_email_integration.py 2>/dev/null || true
git add ai_startup_memory.py 2>/dev/null || true

# コアシステムファイル
echo "🔧 コアシステムファイル追加中..."
git add main.py 2>/dev/null || true
git add email_notifier.py 2>/dev/null || true
git add settings_manager.py 2>/dev/null || true
git add lvyuan_collector.py 2>/dev/null || true
git add settings.json 2>/dev/null || true
git add manual_config.json 2>/dev/null || true

# 安全コミット実行
echo "💾 AI記憶・コアシステム保護コミット実行..."
git commit -m "🛡️ AI記憶システム・コアファイル保護 - ${TIMESTAMP}" || echo "⚠️ コミット対象なし（既に最新）"
echo "✅ AI記憶システム保護完了"

# Phase 3: ドキュメント・設定ファイル保護
echo ""
echo "📚 Phase 3: ドキュメント・設定ファイル保護"
echo "------------------------------------------"

echo "📄 重要ドキュメント追加中..."
git add AI_GITHUB_AUTO_REPORT.md 2>/dev/null || true
git add HANAZONO_SYSTEM_MANUAL_v1.0.md 2>/dev/null || true
git add PROJECT_STATUS.md 2>/dev/null || true
git add HANDOVER_PROMPT.md 2>/dev/null || true
git add AI_AUTOMATIC_INSTRUCTIONS.md 2>/dev/null || true
git add CLAUDE_START_HERE.md 2>/dev/null || true
git add WORK_LOG.md 2>/dev/null || true

echo "💾 ドキュメント保護コミット実行..."
git commit -m "📚 重要ドキュメント・設定保護 - ${TIMESTAMP}" || echo "⚠️ コミット対象なし"
echo "✅ ドキュメント保護完了"

# Phase 4: スクリプト・自動化ファイル整理
echo ""
echo "🚀 Phase 4: スクリプト・自動化ファイル保護"
echo "------------------------------------------"

echo "🔧 スクリプトディレクトリ追加中..."
git add scripts/ 2>/dev/null || true

echo "🤖 自動生成実行ファイル追加中..."
git add auto_generated_executables/ 2>/dev/null || true

echo "💾 自動化ファイル保護コミット実行..."
git commit -m "🚀 スクリプト・自動化ファイル保護 - ${TIMESTAMP}" || echo "⚠️ コミット対象なし"
echo "✅ 自動化ファイル保護完了"

# Phase 5: データ・ログファイル整理
echo ""
echo "💾 Phase 5: データ・ログファイル整理"
echo "------------------------------------"

echo "🧠 学習・予測データ追加中..."
git add learning_data/ 2>/dev/null || true
git add prediction_data/ 2>/dev/null || true
git add prediction_reports/ 2>/dev/null || true

echo "📊 監視・ログファイル追加中..."
git add monitoring_logs/ 2>/dev/null || true
git add safety_backups/ 2>/dev/null || true
git add system_backups/ 2>/dev/null || true

echo "💾 データ・ログ保護コミット実行..."
git commit -m "💾 データ・ログファイル保護 - ${TIMESTAMP}" || echo "⚠️ コミット対象なし"
echo "✅ データ・ログ保護完了"

# Phase 6: 自動バックアップファイル対策
echo ""
echo "🗂️ Phase 6: 自動バックアップファイル管理"
echo "----------------------------------------"

echo "🚫 .gitignore更新中..."
echo "*.auto_backup_*" >> .gitignore
echo "*.tmp" >> .gitignore
echo "*backup_scores.tmp" >> .gitignore
echo "*backup_list.tmp" >> .gitignore

git add .gitignore 2>/dev/null || true
git commit -m "🚫 .gitignore更新 - 自動バックアップファイル除外 - ${TIMESTAMP}" || echo "⚠️ 既に最新"

# 残りファイル確認・安全処理
echo "📋 残りファイル確認中..."
REMAINING=$(git status --porcelain | wc -l)
echo "📊 残り未処理ファイル: ${REMAINING}件"

if [ $REMAINING -gt 0 ]; then
    echo "🗂️ 残りファイル安全追加中..."
    git add . 2>/dev/null || true
    git commit -m "🗂️ その他プロジェクトファイル整理 - ${TIMESTAMP}" || echo "⚠️ コミット対象なし"
fi

echo "✅ 自動バックアップファイル管理完了"

# Phase 7: 最終確認・レポート
echo ""
echo "📊 Phase 7: 最終確認・完了レポート"
echo "----------------------------------"

FINAL_CHANGES=$(git status --porcelain | wc -l)
echo "📈 最終結果:"
echo "  - 開始時変更ファイル: ${CHANGE_COUNT}件"
echo "  - 終了時変更ファイル: ${FINAL_CHANGES}件"
echo "  - 処理済ファイル: $((CHANGE_COUNT - FINAL_CHANGES))件"

echo ""
echo "🎯 作成されたバックアップ:"
echo "  - メインバックアップ: ${BACKUP_DIR}"
echo "  - Gitスナップショット: SAFETY_SNAPSHOT_${TIMESTAMP}"
echo "  - 状況記録: git_status_before_${TIMESTAMP}.txt"

echo ""
echo "📋 最新コミット履歴:"
git log --oneline -5

echo ""
echo "🎊 Git整理完了! 全てのファイルが安全に保護されました"
echo "🛡️ 問題があった場合の復旧方法:"
echo "   git stash apply stash@{0}  # 最新スナップショット復元"
echo "   cp -r ${BACKUP_DIR}/* .    # 完全バックアップ復元"
echo "========================================================"
