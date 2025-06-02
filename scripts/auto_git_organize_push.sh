#!/bin/bash
# HANAZONOシステム Git自動整理＋プッシュスクリプト
# 31件の未コミット変更を論理的に分類して効率的にコミット

echo "🚀 HANAZONOシステム Git自動整理開始..."

cd ~/lvyuan_solar_control

# 現在の状態確認
echo "📊 現在のGit状態:"
git status --porcelain | head -10
echo "..."
echo "総変更ファイル数: $(git status --porcelain | wc -l)件"

# バックアップ作成
echo "🔒 安全のため自動バックアップ作成中..."
timestamp=$(date +"%Y%m%d_%H%M%S")
mkdir -p system_backups/git_organize_$timestamp
cp -r . system_backups/git_organize_$timestamp/ 2>/dev/null

# 分類1: コアシステム（最重要）
echo "🔧 [1/5] コアシステムファイルをコミット..."
git add main.py email_notifier.py lvyuan_collector.py settings_manager.py settings.json 2>/dev/null
if [ $? -eq 0 ]; then
    git commit -m "🔧 core: メール・データ収集・設定管理の安定化 (v3.6)" 2>/dev/null
    echo "   ✅ コアシステム完了"
else
    echo "   ⚠️ コアシステム: 変更なし"
fi

# 分類2: AI記憶継承システム（100点満点システム）
echo "📚 [2/5] AI記憶継承システムをコミット..."
git add AI_*.md HANDOVER_PROMPT.md PROJECT_STATUS.md CLAUDE_START_HERE.md docs/ 2>/dev/null
if [ $? -eq 0 ]; then
    git commit -m "🧠 ai-memory: AI完全自動記憶継承システム100点満点達成" 2>/dev/null
    echo "   ✅ AI記憶継承システム完了"
else
    echo "   ⚠️ AI記憶継承: 変更なし"
fi

# 分類3: 自動化スクリプト群
echo "⚡ [3/5] 自動化スクリプトをコミット..."
git add scripts/ *.sh 2>/dev/null
if [ $? -eq 0 ]; then
    git commit -m "⚡ automation: 開発支援・自動化スクリプト群の拡張" 2>/dev/null
    echo "   ✅ 自動化スクリプト完了"
else
    echo "   ⚠️ 自動化スクリプト: 変更なし"
fi

# 分類4: バックアップ・ログファイル
echo "🗂️ [4/5] バックアップ・ログファイルをコミット..."
git add monitoring_logs/ system_backups/ logs/ *.backup* */backup_* 2>/dev/null
if [ $? -eq 0 ]; then
    git commit -m "🗂️ backup: 自動バックアップ・モニタリングログの整理" 2>/dev/null
    echo "   ✅ バックアップ・ログ完了"
else
    echo "   ⚠️ バックアップ・ログ: 変更なし"
fi

# 分類5: その他の変更
echo "📝 [5/5] その他の変更をコミット..."
git add . 2>/dev/null
if [ $? -eq 0 ]; then
    git commit -m "📝 misc: その他の設定・ドキュメント更新" 2>/dev/null
    echo "   ✅ その他の変更完了"
else
    echo "   ⚠️ その他: 変更なし"
fi

# GitHub自動プッシュ
echo "🌐 GitHub自動プッシュ実行中..."
git push origin main
if [ $? -eq 0 ]; then
    echo "   ✅ GitHub プッシュ成功"
else
    echo "   ❌ GitHub プッシュ失敗"
    echo "   手動確認が必要です: git push origin main"
fi

# 結果表示
echo ""
echo "🎉 Git自動整理完了！"
echo "📊 最新のコミット履歴:"
git log --oneline -5

echo ""
echo "🎯 次のステップ:"
echo "1. 統合開発コマンドシステム構築 (30分)"
echo "2. 自然言語インターフェース実装 (30分)"
echo "3. GitHub Actions自動化設定 (30分)"
