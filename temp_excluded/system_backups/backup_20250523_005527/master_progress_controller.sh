#!/bin/bash
# HANAZONOシステム 完全自動進行管理システム v1.0
# 更新日: 2025-05-21

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_ONLY=$(date '+%Y-%m-%d')
SESSION_ID=$(date '+%Y%m%d_%H%M%S')

echo -e "${BLUE}=== HANAZONOシステム 進行管理システム v1.0 ===${NC}"
echo -e "${BLUE}実行時刻: ${TIMESTAMP}${NC}"

# Git状態取得
get_git_status() {
    git_changes=$(git status --porcelain | wc -l)
    latest_commit=$(git log -1 --pretty=format:'%h %s' 2>/dev/null || echo "コミットなし")
    
    if [ ${git_changes} -gt 0 ]; then
        current_phase="開発作業中（未コミット: ${git_changes}件）"
    else
        current_phase="安定運用中"
    fi
}

# PROJECT_STATUS.md更新
update_project_status() {
    echo -e "${YELLOW}PROJECT_STATUS.md を更新中...${NC}"
    
    cat > PROJECT_STATUS.md << STATUS_EOF
# HANAZONOシステム プロジェクト状態 (自動生成)

*最終更新*: ${TIMESTAMP}
*現在のフェーズ*: ${current_phase}

## システム概要
- *プロジェクト名*: HANAZONOシステム
- *目的*: LVYUAN太陽光蓄電システムの天気予報ベース自動最適化
- *Git状態*: ${git_changes} files changed
- *最新コミット*: ${latest_commit}

## 完了タスク
1. メール通知フォーマット完全修正（電流小数点表示、行間調整）
2. settings.json重複削除完了
3. main.py設定読み込み処理重複修正完了
4. EmailNotifier初期化パラメータ修正完了
5. 自動引き継ぎシステム基本構築完了
6. GitHub Personal Access Token生成・設定完了

## 進行中タスク
1. AIセッション間完全記憶継承システムの構築
2. リアルタイム状態追跡の自動化実装
3. 引き継ぎプロンプト自動生成システムの完成

## 次のアクション
1. PROJECT_STATUS.mdベースの完全引き継ぎシステム完成
2. メール通知の核心機能（天気予報連携・推奨パラメータ計算）復元
3. 天気予報データ取得機能の確認/再実装
4. 季節判定ロジックの確認/再実装

## 緊急課題
1. AIセッション間の記憶喪失問題の完全解決
2. 引き継ぎプロンプトのリアルタイム更新システム完成
3. GitHub連携による効率的な進行管理の実現
STATUS_EOF
    
    echo "✅ PROJECT_STATUS.md 更新完了"
}

# 引き継ぎプロンプト生成
generate_handover() {
    echo -e "${YELLOW}引き継ぎプロンプトを生成中...${NC}"
    
    # バージョン番号決定
    if [ -f "HANDOVER_PROMPT.md" ]; then
        prev_version=$(grep -o "v[0-9]\+" HANDOVER_PROMPT.md | head -n 1 | tr -d 'v')
        VERSION=$((prev_version + 1))
    else
        VERSION=1
    fi
    
    cat > HANDOVER_PROMPT.md << HANDOVER_EOF
# v${VERSION}_HANAZONOシステム／完全記憶継承プロンプト-${DATE_ONLY}

*自動生成*: ${TIMESTAMP}

## ⚡ 新セッション開始必須手順

### STEP 1: システム状態確認
\`\`\`bash
cd ~/lvyuan_solar_control
bash scripts/master_progress_controller.sh
\`\`\`

### STEP 2: 前回セッション継承
\`\`\`bash
cat docs/WORK_LOG.md | tail -5 2>/dev/null || echo "新規セッション"
\`\`\`

## 📊 プロジェクト現状

*現在のフェーズ*: ${current_phase}
*Git状態*: ${git_changes} files changed
*最新コミット*: ${latest_commit}

## 🎯 プロジェクト本質
- *目的*: LVYUAN太陽光蓄電システムの天気予報ベース自動最適化
- *核心機能*: 天気予報→季節判定→最適パラメータ計算→メール通知→手動設定変更
- *ハードウェア*: Raspberry Pi Zero 2W + LVYUAN SPI-10K-U + FLCD16-10048×4台

## 📋 現在のタスク状況

$(cat PROJECT_STATUS.md | grep -A 20 "## 完了タスク")

## 🛠️ 緊急時対応
\`\`\`bash
# システム動作確認
python3 main.py --check-cron

# メール送信テスト  
python3 main.py --daily-report --debug
\`\`\`

---
*🎯 目標*: 新AIセッションで前回の記憶を100%継承
HANDOVER_EOF
    
    echo "✅ 引き継ぎプロンプト v${VERSION} 生成完了"
}

# 作業ログ更新
update_work_log() {
    echo -e "${YELLOW}作業ログを更新中...${NC}"
    
    mkdir -p docs
    
    if [ ! -f "docs/WORK_LOG.md" ]; then
        echo "# HANAZONOシステム 作業ログ" > docs/WORK_LOG.md
        echo "" >> docs/WORK_LOG.md
    fi
    
    echo "[${TIMESTAMP}] 進行管理システム実行" >> docs/WORK_LOG.md
    echo "  - フェーズ: ${current_phase}" >> docs/WORK_LOG.md
    echo "  - Git状態: ${git_changes} files changed" >> docs/WORK_LOG.md
    echo "" >> docs/WORK_LOG.md
    
    echo "✅ 作業ログ更新完了"
}

# CLAUDE_START_HERE.md更新
update_start_guide() {
    echo -e "${YELLOW}CLAUDE_START_HERE.md を更新中...${NC}"
    
    mkdir -p docs/navigation
    
    cat > docs/navigation/CLAUDE_START_HERE.md << START_EOF
# 🚀 Claude専用 - 完全記憶継承スタートガイド v2.0

*最終自動更新*: ${TIMESTAMP}

## ⚡ 新セッション開始手順

### STEP 1: 進行管理システム実行
\`\`\`bash
cd ~/lvyuan_solar_control
bash scripts/master_progress_controller.sh
\`\`\`

### STEP 2: 引き継ぎプロンプト確認
\`\`\`bash
cat HANDOVER_PROMPT.md
\`\`\`

## 📊 現在の状況（自動更新）

- *フェーズ*: ${current_phase}
- *Git変更*: ${git_changes} files
- *最新コミット*: ${latest_commit}

## 🎯 最優先事項
1. 前回セッションからの継続作業確認
2. システム動作状態の確認
3. 未コミット変更の処理

## 📞 緊急時コマンド
\`\`\`bash
# システム確認
python3 main.py --check-cron

# メール送信テスト
python3 main.py --daily-report --debug
\`\`\`

---
*完全記憶継承*: 新AIセッションで前回状態を100%復元
START_EOF
    
    echo "✅ CLAUDE_START_HERE.md 更新完了"
}

# メイン処理
main() {
    get_git_status
    
    case "${1:-full}" in
        "status-only")
            echo -e "${GREEN}現在のフェーズ: ${current_phase}${NC}"
            echo -e "${GREEN}Git状態: ${git_changes} files changed${NC}"
            echo -e "${GREEN}最新コミット: ${latest_commit}${NC}"
            ;;
        "full"|"")
            update_project_status
            generate_handover
            update_work_log
            update_start_guide
            
            echo -e "${GREEN}=== 進行管理システム実行完了 ===${NC}"
            echo -e "${GREEN}次回セッション開始時は以下を実行:${NC}"
            echo -e "${BLUE}bash scripts/master_progress_controller.sh${NC}"
            ;;
        *)
            echo "使用方法: $0 [full|status-only]"
            exit 1
            ;;
    esac
}

main "$@"
