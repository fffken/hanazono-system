#!/bin/bash

# AI開発アシスタント v1.0
ai_assistant() {
    local request="$1"
    
    echo "🤖 AI開発アシスタント起動"
    echo "要求分析: $request"
    echo "=================================="
    
    # インテリジェント状況分析
    analyze_current_situation
    
    # 最適アクション提案
    suggest_optimal_actions "$request"
}

# インテリジェント状況分析
analyze_current_situation() {
    echo "🔍 インテリジェント状況分析中..."
    
    # Git状態分析
    local git_changes=$(git status --short | wc -l)
    local current_branch=$(git branch --show-current)
    local last_commit=$(git log -1 --oneline)
    
    # システム状態分析
    local system_status="OK"
    if ! python3 main.py --daily-report >/dev/null 2>&1; then
        system_status="ERROR"
    fi
    
    # プロジェクト進捗分析
    local completed_tasks=0
    local total_tasks=6
    
    # 完了タスクのカウント
    [[ -f "HANDOVER_PROMPT.md" ]] && completed_tasks=$((completed_tasks + 1))
    [[ -f "scripts/dev_command.sh" ]] && completed_tasks=$((completed_tasks + 1))
    [[ -f "scripts/natural_language_interface.sh" ]] && completed_tasks=$((completed_tasks + 1))
    [[ -f "scripts/github_auto_enhanced.sh" ]] && completed_tasks=$((completed_tasks + 1))
    [[ -f "scripts/fact_check_system.sh" ]] && completed_tasks=$((completed_tasks + 1))
    [[ -f "HANAZONO_DEVELOPMENT_PHILOSOPHY.md" ]] && completed_tasks=$((completed_tasks + 1))
    
    local progress_percentage=$((completed_tasks * 100 / total_tasks))
    
    echo "  📊 プロジェクト進捗: $completed_tasks/$total_tasks ($progress_percentage%)"
    echo "  🌿 現在ブランチ: $current_branch"
    echo "  📝 未コミット変更: $git_changes件"
    echo "  🎯 システム状態: $system_status"
    echo "  📅 最新コミット: $last_commit"
}

# 最適アクション提案システム
suggest_optimal_actions() {
    local request="$1"
    
    echo "💡 最適アクション提案中..."
    
    # 現在の状況に基づく判定
    local git_changes=$(git status --short | wc -l)
    local system_status="OK"
    if ! python3 main.py --daily-report >/dev/null 2>&1; then
        system_status="ERROR"
    fi
    
    # 緊急度判定
    local urgency="NORMAL"
    if [[ "$system_status" == "ERROR" ]]; then
        urgency="HIGH"
    elif [[ $git_changes -gt 10 ]]; then
        urgency="MEDIUM"
    fi
    
    echo "  🎯 緊急度: $urgency"
    
    # 状況別推奨アクション
    case "$urgency" in
        "HIGH")
            suggest_emergency_actions
            ;;
        "MEDIUM")
            suggest_maintenance_actions
            ;;
        "NORMAL")
            suggest_development_actions "$request"
            ;;
    esac
}

# 緊急時アクション
suggest_emergency_actions() {
    echo "🚨 緊急対応が必要です"
    echo "  1. システム修復: ask \"修正して\""
    echo "  2. 状況確認: ask \"確認して\""
    echo "  3. 緊急復旧: git reset --hard HEAD"
}

# メンテナンスアクション
suggest_maintenance_actions() {
    echo "🔧 メンテナンス推奨"
    echo "  1. 変更整理: ask \"保存して\""
    echo "  2. 詳細分析: ask \"分析して\""
    echo "  3. 進捗確認: ask \"進捗は？\""
}

# 開発アクション
suggest_development_actions() {
    local request="$1"
    
    echo "🚀 開発推奨アクション"
    
    # EFFICIENCY_PRIORITY_ROADMAPに基づく提案
    echo "  📋 効率最優先順序:"
    echo "  1. AI開発アシスタント完成 (90分残り推定)"
    echo "  2. 予測型システム実装 (150分推定)"
    echo "  3. 完全自動化システム (180分推定)"
    
    # 具体的実行コマンド
    echo ""
    echo "  ⚡ 即座実行可能:"
    echo "  - dev_ultimate \"AI開発アシスタント完成\""
    echo "  - ask \"次は何？\""
    echo "  - ask \"効率を確認\""
}


# 高度な問題検出システム

# [v2.1 新機能] 構造的整合性チェック - 関数の開始/終了が対応しているか検証
check_structural_integrity_v2_1() {
    local -n warnings_ref=$1
    local -n issues_count_ref=$2
    
    local func_starts=$(grep -c "^[a-zA-Z_][a-zA-Z0-9_]*() {" scripts/ai_development_assistant.sh)
    local func_ends=$(grep -c "^}" scripts/ai_development_assistant.sh)

    if [[ "$func_starts" -ne "$func_ends" ]]; then
        warnings_ref+=("🚨 重大警告: 関数定義の開始({)と終了(})の数が一致しません。($func_starts 対 $func_ends) ファイルが破損している可能性があります。")
        issues_count_ref=$((issues_count_ref + 1))
    fi
}

# [v2.1 新機能] 論理整合性チェック - 危険な検索ロジックを警告
check_logic_consistency_v2_1() {
    local -n warnings_ref=$1
    local -n issues_count_ref=$2

    # venv等を除外しない広範囲なgrep -rを検出する
    if grep -q 'grep -r .* --include=.* .' scripts/ai_development_assistant.sh && ! grep -q 'grep -r .* --exclude-dir="venv"' scripts/ai_development_assistant.sh; then
        warnings_ref+=("⚠️ 論理的警告: venvを除外しない 'grep -r' が使用されています。誤検出の可能性があります。")
        issues_count_ref=$((issues_count_ref + 1))
    fi
}

# 既存の advanced_problem_detection 関数をv2.1にアップグレード
upgrade_to_v2_1() {
    # 元の関数をバックアップ（念のため）
    eval "$(declare -f advanced_problem_detection | sed 's/advanced_problem_detection/advanced_problem_detection_v2_0/')"
    
    # v2.1版の新しい関数を定義
    advanced_problem_detection() {
        echo "✅ v2.1 高速アップデート適用済み"
        echo "🔍 次世代問題検出システム実行中..."
        
        local issues_found=0
        local warnings=()
        local errors=()

        # [v2.1] 新しいチェック機能を追加
        check_structural_integrity_v2_1 warnings issues_found
        check_logic_consistency_v2_1 warnings issues_found
        
        # v2.0の既存チェックも実行
        advanced_problem_detection_v2_0

        # レポート生成は既存のものを利用
    }
}

# --- v2.1 高速アップデートパッチ ここまで ---

# --- v2.2 高速アップデートパッチ ここから ---

# [v2.2 新機能] 静的解析チェック - shellcheckで専門的な問題を検出
check_static_analysis_v2_2() {
    local -n warnings_ref=$1
    local -n issues_count_ref=$2
    local target_script="scripts/ai_development_assistant.sh"
    local report_file="/tmp/shellcheck_report.txt"

    if command -v shellcheck &> /dev/null; then
        # SC2154: 変数が未定義の可能性, SC2034: 変数が未使用, など一般的な警告は除外
        if ! shellcheck -e SC2154,SC2034 "$target_script" > "$report_file" 2>&1; then
            if [ -s "$report_file" ]; then
                warnings_ref+=("🤖 shellcheckによる静的解析で問題が指摘されました (詳細は ${report_file} )")
                issues_count_ref=$((issues_count_ref + 1))
            fi
        else
             rm -f "$report_file"
        fi
    fi
}

# 既存の関数をv2.2にアップグレード
upgrade_to_v2_2() {
    type upgrade_to_v2_1 >/dev/null 2>&1 && upgrade_to_v2_1
    eval "$(declare -f advanced_problem_detection | sed 's/advanced_problem_detection/advanced_problem_detection_v2_1/')"
    
    advanced_problem_detection() {
        echo "✅ v2.2 AI能力向上アップデート適用済み"
        advanced_problem_detection_v2_1
        echo "  🧠 静的解析チェック中 (shellcheck)..."
        local issues_found=0
        local warnings=()
        check_static_analysis_v2_2 warnings issues_found
        if [[ "$issues_found" -gt 0 ]]; then
            echo ""
            echo "--- 静的解析レポート ---"
            for warning in "${warnings[@]}"; do
                echo "$warning"
            done
            echo "------------------------"
        fi
    }
}
# --- v2.2 高速アップデートパッチ ここまで ---

# --- v2.2 高速アップデートパッチ ここから ---
check_static_analysis_v2_2() {
    local -n warnings_ref=$1
    local -n issues_count_ref=$2
    local target_script="scripts/ai_development_assistant.sh"
    local report_file="/tmp/shellcheck_report.txt"
    if command -v shellcheck &> /dev/null; then
        if ! shellcheck -e SC2154,SC2034 "$target_script" > "$report_file" 2>&1; then
            if [ -s "$report_file" ]; then
                warnings_ref+=("🤖 shellcheckで問題が指摘されました (詳細は ${report_file} )")
                issues_count_ref=$((issues_count_ref + 1))
            fi
        else
             rm -f "$report_file"
        fi
    fi
}
upgrade_to_v2_2() {
    type upgrade_to_v2_1 >/dev/null 2>&1 && upgrade_to_v2_1
    eval "$(declare -f advanced_problem_detection | sed 's/advanced_problem_detection/advanced_problem_detection_v2_1/')"
    advanced_problem_detection() {
        echo "✅ v2.2 AI能力向上アップデート適用済み"
        advanced_problem_detection_v2_1
        echo "  🧠 静的解析チェック中 (shellcheck)..."
        local issues_found=0; local warnings=()
        check_static_analysis_v2_2 warnings issues_found
        if [[ "$issues_found" -gt 0 ]]; then
            echo ""
            echo "--- 静的解析レポート ---"
            for warning in "${warnings[@]}"; do echo "$warning"; done
            echo "------------------------"
        fi
    }
}
# --- v2.2 高速アップデートパッチ ここまで ---
# --- v2.3 改良版パッチ ここから ---
generate_intelligent_diagnostic_report() {
    local -n warnings_ref=$1
    echo ""
    echo "--- 💡 インテリジェント診断レポート ---"
    echo "  [検出された問題]:"
    for warning in "${warnings_ref[@]}"; do echo "    - $warning"; done
    if [[ -f "/tmp/shellcheck_report.txt" && -s "/tmp/shellcheck_report.txt" ]]; then
        echo "  [関連ログの抜粋 (shellcheck)]:"
        head -n 5 "/tmp/shellcheck_report.txt" | sed 's/^/    /'
    fi
    echo "  [直近のコミット履歴 (原因の可能性)]:"
    git log -n 3 --oneline --pretty=format:"    - %h %s (%cr)" 2>/dev/null || echo "    Git履歴を取得できませんでした。"
    echo "  [AI推奨アクション]:"
    echo "    - ask '詳細なログを表示して' または 'ask \"<コミットID> の変更内容を教えて\"' で深掘りできます。"
    echo "----------------------------------------"
}
advanced_problem_detection() {
    echo "✅ v2.3 診断能力向上アップデート適用済み"
    echo "🔍 次世代問題検出システム実行中..."
    local issues_found=0; local warnings=(); local errors=()
    check_structural_integrity_v2_1 warnings issues_found
    check_logic_consistency_v2_1 warnings issues_found
    advanced_problem_detection_v2_0 # v2.0のチェックも実行
    echo "  🧠 静的解析チェック中 (shellcheck)..."
    check_static_analysis_v2_2 warnings issues_found
    if [[ "$issues_found" -gt 0 ]]; then
        generate_intelligent_diagnostic_report warnings
    fi
}
# --- v2.3 改良版パッチ ここまで ---
