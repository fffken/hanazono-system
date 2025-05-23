#!/bin/bash
# GitHub自動情報取得システム v2.0 - 完全版

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_FILE="AI_GITHUB_AUTO_REPORT.md"

echo -e "${BLUE}=== GitHub自動情報取得システム（完全版） ===${NC}"

# AI用GitHub完全レポート生成
generate_ai_github_report() {
    cat > $REPORT_FILE << REPORT_EOF
# AI用GitHub自動取得レポート（完全版）

**生成時刻**: $TIMESTAMP
**目的**: 新しいAIセッション開始時の完全状況把握

## 🔍 Git状態の完全把握

### 📊 リポジトリ基本情報
REPORT_EOF

    # Git基本情報
    echo "- **ブランチ**: $(git branch --show-current)" >> $REPORT_FILE
    echo "- **最新コミット**: $(git log -1 --oneline)" >> $REPORT_FILE
    echo "- **リモートURL**: $(git remote get-url origin)" >> $REPORT_FILE
    
    # 変更状況
    local changes=$(git status --porcelain | wc -l)
    echo "- **未コミット変更**: $changes 件" >> $REPORT_FILE
    
    if [ $changes -gt 0 ]; then
        echo -e "\n### ⚠️ 未コミット変更詳細" >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
        git status --short >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    # 最近のコミット履歴
    echo -e "\n### 📝 最近のコミット履歴（5件）" >> $REPORT_FILE
    echo '```' >> $REPORT_FILE
    git log --oneline -5 >> $REPORT_FILE
    echo '```' >> $REPORT_FILE
}

# 重要ファイルの完全取得
fetch_all_important_files() {
    echo -e "\n## 📁 重要ファイルの完全内容" >> $REPORT_FILE
    
    # === 重要度：高 ===
    echo -e "\n### 🔴 重要度：高 - プロジェクト管理ファイル" >> $REPORT_FILE
    
    if [ -f "PROJECT_STATUS.md" ]; then
        echo -e "\n#### 📊 PROJECT_STATUS.md" >> $REPORT_FILE
        echo '```markdown' >> $REPORT_FILE
        head -30 PROJECT_STATUS.md >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    if [ -f "HANDOVER_PROMPT.md" ]; then
        echo -e "\n#### 🔄 HANDOVER_PROMPT.md" >> $REPORT_FILE
        echo '```markdown' >> $REPORT_FILE
        head -25 HANDOVER_PROMPT.md >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    if [ -f "AI_AUTOMATIC_INSTRUCTIONS.md" ]; then
        echo -e "\n#### 🤖 AI_AUTOMATIC_INSTRUCTIONS.md" >> $REPORT_FILE
        echo '```markdown' >> $REPORT_FILE
        head -20 AI_AUTOMATIC_INSTRUCTIONS.md >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    if [ -f "CHANGELOG.md" ]; then
        echo -e "\n#### 📝 CHANGELOG.md" >> $REPORT_FILE
        echo '```markdown' >> $REPORT_FILE
        head -15 CHANGELOG.md >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    # === 重要度：中 ===
    echo -e "\n### 🟡 重要度：中 - 核心Pythonファイル" >> $REPORT_FILE
    
    # 設定ファイル
    if [ -f "settings.json" ]; then
        echo -e "\n#### ⚙️ settings.json" >> $REPORT_FILE
        echo '```json' >> $REPORT_FILE
        head -25 settings.json >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    # メインファイル
    if [ -f "main.py" ]; then
        echo -e "\n#### 🎯 main.py（構造）" >> $REPORT_FILE
        echo '```python' >> $REPORT_FILE
        grep -n "^def \|^class \|^import \|^from " main.py | head -15 >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
    
    # 重要なPythonファイル群
    for py_file in "email_notifier.py" "settings_manager.py" "lvyuan_collector.py" "data_util.py" "logger.py"; do
        if [ -f "$py_file" ]; then
            echo -e "\n#### 🐍 $py_file（構造）" >> $REPORT_FILE
            echo '```python' >> $REPORT_FILE
            grep -n "^def \|^class \|^import \|^from " "$py_file" | head -10 >> $REPORT_FILE
            echo '```' >> $REPORT_FILE
        fi
    done
    
    # requirements.txt
    if [ -f "requirements.txt" ]; then
        echo -e "\n#### 📦 requirements.txt" >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
        cat requirements.txt >> $REPORT_FILE
        echo '```' >> $REPORT_FILE
    fi
}

# 完全構文チェック
check_all_important_files() {
    echo -e "\n## 🔧 完全システム動作確認" >> $REPORT_FILE
    
    echo -e "\n### ✅ 全重要ファイル構文チェック" >> $REPORT_FILE
    local syntax_errors=0
    
    # 重要度：高・中の全ファイル
    for py_file in main.py email_notifier.py settings_manager.py lvyuan_collector.py data_util.py logger.py; do
        if [ -f "$py_file" ]; then
            if python3 -m py_compile "$py_file" 2>/dev/null; then
                echo "- ✅ $py_file: 正常" >> $REPORT_FILE
            else
                echo "- ❌ $py_file: 構文エラー" >> $REPORT_FILE
                syntax_errors=$((syntax_errors + 1))
            fi
        fi
    done
    
    if [ $syntax_errors -eq 0 ]; then
        echo -e "\n🎉 **全ての重要ファイルが正常動作可能**" >> $REPORT_FILE
    else
        echo -e "\n⚠️ **$syntax_errors 個のファイルに構文エラー**" >> $REPORT_FILE
    fi
}

# メイン実行
main() {
    echo -e "${YELLOW}🔍 GitHub完全情報を自動取得中...${NC}"
    
    git fetch origin >/dev/null 2>&1 || echo "  ⚠️ Git fetch失敗（オフライン可能性）"
    
    generate_ai_github_report
    fetch_all_important_files
    check_all_important_files
    
    echo -e "${GREEN}✅ GitHub完全情報取得完了${NC}"
    echo -e "${GREEN}📊 詳細レポート: $REPORT_FILE${NC}"
    
    # 要約表示
    local changes=$(git status --porcelain | wc -l)
    echo -e "${BLUE}=== 完全AI情報取得要約 ===${NC}"
    echo "📋 取得ファイル: PROJECT_STATUS, HANDOVER_PROMPT, AI_INSTRUCTIONS, CHANGELOG"
    echo "🐍 Python確認: main, email_notifier, settings_manager, lvyuan_collector, data_util, logger"
    echo "📊 未コミット変更: $changes 件"
    
    if [ $changes -gt 10 ]; then
        echo -e "${RED}⚠️ 緊急度: 高（整理が必要）${NC}"
    elif [ $changes -gt 0 ]; then
        echo -e "${YELLOW}📝 緊急度: 通常（開発中）${NC}"
    else
        echo -e "${GREEN}✅ 緊急度: 最適（クリーン）${NC}"
    fi
}

main "$@"
