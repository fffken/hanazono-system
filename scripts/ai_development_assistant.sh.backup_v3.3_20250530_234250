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

# --- v2.4 アップデートパッチ ここから ---

# [v2.4 新機能] Pythonファイルのコードスタイルを自動整形する
auto_format_python_files() {
    echo "🐍 Pythonコードの自動フォーマットを開始します..."
    echo "   整形対象: プロジェクト内の全 .py ファイル (venv除く)"

    # venvディレクトリを除外して.pyファイルを検索し、autopep8を適用
    # ファイル名にスペースがあっても安全なように-print0とxargs -0を使用
    find . -path ./venv -prune -o -name "*.py" -print0 | xargs -0 python3 -m autopep8 --in-place --aggressive

    echo "✅ フォーマットが完了しました。"
    echo "   git diff で変更内容を確認できます。"
}

# --- v2.4 アップデートパッチ ここまで ---
# --- v2.5 アップデートパッチ ここから ---
run_code_health_check() {
    echo "🩺 コードの健康診断を開始します..."
    echo "========================================"
    echo ""
    echo "--- 1. Pyflakes (未使用の変数/インポート等) ---"
    find . -path ./venv -prune -o -name "*.py" -exec python3 -m pyflakes {} +
    echo ""
    echo "--- 2. Vulture (デッドコード/到達不能コード) ---"
    python3 -m vulture --min-confidence 80 --exclude venv .
    echo ""
    echo "========================================"
    echo "✅ 健康診断が完了しました。"
}
# --- v2.5 アップデートパッチ ここまで ---
# --- v3.1 完成版パッチ ---
get_problem_count() {
    local issues_found=0
    if grep -r "os.popen" --include="*.py" . | grep -v "venv" >/dev/null 2>&1; then
        issues_found=$((issues_found + 1))
    fi
    echo "$issues_found"
}
fully_autonomous_system() {
    echo "🤖 完全自律実行システム v3.1 (最終版) 起動..."
    local max_loops=5; local loop_count=1
    while [[ $loop_count -le $max_loops ]]; do
        echo ""; echo "🔄 自律サイクル ${loop_count}/${max_loops} を開始..."
        local problem_count=$(get_problem_count)
        echo "  [1/3] 🔍 現在の問題数: ${problem_count}件"
        if [[ "$problem_count" -eq 0 ]]; then echo "🏆 問題0件。自律処理完了。"; break; fi
        echo "  [2/3] 🔧 自動修正(AST)を実行します..."
        run_ast_based_refactoring
        echo "  [3/3] ⚙️ 修正反映のため1秒待機..."; sleep 1
        ((loop_count++))
    done
    if [[ $loop_count -gt $max_loops ]]; then echo "⚠️ 最大ループ回数到達。"; fi
    echo "🏁 自律システム実行完了。"
}
# --- v3.1 完成版パッチここまで ---
# --- v3.2 アップデートパッチ ここから ---
check_for_remote_changes() {
    echo "📡 GitHubリモートリポジトリの変更を確認中..."
    local last_sha_file=".last_remote_sha"
    local previous_sha=""
    local current_sha=""

    if [ -f "$last_sha_file" ]; then
        previous_sha=$(cat "$last_sha_file")
    fi
    git fetch origin >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "❌エラー: 'git fetch origin' に失敗しました。ネットワーク接続を確認してください。"
        return 1
    fi
    current_sha=$(git rev-parse origin/main 2>/dev/null)
    if [ -z "$current_sha" ]; then
        echo "❌エラー: 'origin/main' のコミットIDを取得できませんでした。"
        return 1
    fi
    if [ "$current_sha" != "$previous_sha" ]; then
        echo "🎉 新しいリモートの変更を検出しました！"
        echo "   最新のコミットID: $current_sha"
        [ -n "$previous_sha" ] && echo "   前回のコミットID: $previous_sha"
        echo "$current_sha" > "$last_sha_file"
        echo "   (今後、この変更をトリガーに自動分析を開始します)"
        return 0 # 変更あり
    else
        echo "✅ リモートの変更はありません。 (最新: $current_sha)"
        return 1 # 変更なし
    fi
}
# --- v3.2 アップデートパッチ ここまで ---
