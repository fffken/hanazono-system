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
advanced_problem_detection() {
    echo "🔍 高度な問題検出システム実行中..."
    
    local issues_found=0
    local warnings=()
    local errors=()
    
    # 1. ファイル整合性チェック
    echo "  📁 ファイル整合性チェック中..."
    check_file_integrity warnings errors issues_found
    
    # 2. 設定整合性チェック
    echo "  ⚙️ 設定整合性チェック中..."
    check_configuration_integrity warnings errors issues_found
    
    # 3. 依存関係チェック
    echo "  🔗 依存関係チェック中..."
    check_dependencies warnings errors issues_found
    
    # 4. セキュリティチェック
    echo "  🔒 セキュリティチェック中..."
    check_security_issues warnings errors issues_found
    
    # 結果レポート
    generate_problem_report "$issues_found" warnings errors
}

# ファイル整合性チェック
check_file_integrity() {
    local -n warnings_ref=$1
    local -n errors_ref=$2
    local -n issues_count_ref=$3
    
    # 重要ファイルの存在確認
    local critical_files=(
        "HANDOVER_PROMPT.md"
        "EFFICIENCY_PRIORITY_ROADMAP.md"
        "settings.json"
        "scripts/hanazono_start.sh"
        "scripts/dev_command.sh"
    )
    
    for file in "${critical_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            errors_ref+=("重要ファイル欠損: $file")
            issues_count_ref=$((issues_count_ref + 1))
        fi
    done
    
    # ファイルサイズ異常チェック
    if [[ -f "settings.json" ]]; then
        local size=$(stat -f%z "settings.json" 2>/dev/null || stat -c%s "settings.json" 2>/dev/null)
        if [[ $size -lt 100 ]]; then
            warnings_ref+=("settings.json のサイズが異常に小さい: ${size}bytes")
            issues_count_ref=$((issues_count_ref + 1))
        fi
    fi
}

# 設定整合性チェック
check_configuration_integrity() {
    local -n warnings_ref=$1
    local -n errors_ref=$2
    local -n issues_count_ref=$3
    
    # settings.jsonの構文チェック
    if [[ -f "settings.json" ]]; then
        if ! python3 -m json.tool settings.json >/dev/null 2>&1; then
            errors_ref+=("settings.json の JSON構文エラー")
            issues_count_ref=$((issues_count_ref + 1))
        fi
    fi
    
    # Python構文エラーチェック
    local python_errors=0
    for file in *.py; do
        if [[ -f "$file" && ! "$file" =~ (test_|_test\.py|.*_old\.py)$ ]]; then
            if ! python3 -m py_compile "$file" 2>/dev/null; then
                warnings_ref+=("Python構文エラー: $file")
                python_errors=$((python_errors + 1))
            fi
        fi
    done
    
    if [[ $python_errors -gt 0 ]]; then
        issues_count_ref=$((issues_count_ref + python_errors))
    fi
}

# 依存関係チェック
check_dependencies() {
    local -n warnings_ref=$1
    local -n errors_ref=$2
    local -n issues_count_ref=$3
    
    # 必要なPythonパッケージチェック
    local required_packages=("requests" "json" "datetime")
    
    for package in "${required_packages[@]}"; do
        if ! python3 -c "import $package" 2>/dev/null; then
            warnings_ref+=("Pythonパッケージ不足: $package")
            issues_count_ref=$((issues_count_ref + 1))
        fi
    done
    
    # Git設定チェック
    if ! git config user.name >/dev/null; then
        warnings_ref+=("Git user.name が未設定")
        issues_count_ref=$((issues_count_ref + 1))
    fi
}

# セキュリティチェック
check_security_issues() {
    local -n warnings_ref=$1
    local -n errors_ref=$2
    local -n issues_count_ref=$3
    
    # パスワード・秘密情報の露出チェック
    if grep -r "password.*=" --include="*.py" --include="*.json" . 2>/dev/null | grep -v "smtp_password"; then
        warnings_ref+=("パスワード情報が平文で保存されている可能性")
        issues_count_ref=$((issues_count_ref + 1))
    fi
    
    # 実行権限の過度な付与チェック
    local executable_files=$(find . -type f -perm +111 | grep -v ".git" | wc -l)
    if [[ $executable_files -gt 20 ]]; then
        warnings_ref+=("実行権限付きファイルが多数存在: $executable_files個")
        issues_count_ref=$((issues_count_ref + 1))
    fi
}

# 問題レポート生成
generate_problem_report() {
    local issues_count=$1
    local -n warnings_ref=$2
    local -n errors_ref=$3
    
    echo ""
    echo "📋 問題検出レポート"
    echo "=================================="
    
    if [[ $issues_count -eq 0 ]]; then
        echo "✅ 問題なし - システム正常"
        return 0
    fi
    
    echo "🚨 検出された問題: $issues_count件"
    echo ""
    
    # エラー表示
    if [[ ${#errors_ref[@]} -gt 0 ]]; then
        echo "❌ エラー (要対応):"
        for error in "${errors_ref[@]}"; do
            echo "  - $error"
        done
        echo ""
    fi
    
    # 警告表示
    if [[ ${#warnings_ref[@]} -gt 0 ]]; then
        echo "⚠️ 警告 (推奨対応):"
        for warning in "${warnings_ref[@]}"; do
            echo "  - $warning"
        done
        echo ""
    fi
    
    # 対応提案
    echo "💡 推奨対応アクション:"
    suggest_problem_solutions "$issues_count" errors_ref warnings_ref
}

# 問題解決提案

# 進捗自動追跡システム
advanced_progress_tracking() {
    echo "📊 進捗自動追跡システム実行中..."
    
    local total_score=0
    local max_score=0
    
    # 1. 機能実装進捗
    echo "  🚀 機能実装進捗分析中..."
    track_feature_progress total_score max_score
    
    # 2. コード品質進捗
    echo "  💎 コード品質進捗分析中..."
    track_code_quality total_score max_score
    
    # 3. 自動化レベル進捗
    echo "  🤖 自動化レベル分析中..."
    track_automation_level total_score max_score
    
    # 4. 効率化進捗
    echo "  ⚡ 効率化進捗分析中..."
    track_efficiency_progress total_score max_score
    
    # 総合進捗レポート
    generate_progress_report "$total_score" "$max_score"
}

# 機能実装進捗追跡
track_feature_progress() {
    local -n total_ref=$1
    local -n max_ref=$2
    
    local feature_score=0
    local feature_max=100
    
    # Phase 1機能チェック（60点満点）
    [[ -f "HANDOVER_PROMPT.md" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/dev_command.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/natural_language_interface.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/github_auto_enhanced.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/fact_check_system.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/ai_development_assistant.sh" ]] && feature_score=$((feature_score + 10))
    
    # Phase 2機能チェック（40点満点）
    if [[ -f "scripts/ai_development_assistant.sh" ]]; then
        if grep -q "advanced_problem_detection" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "advanced_progress_tracking" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "implementation_proposal" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "learning_system" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
    fi
    
    echo "    機能実装進捗: $feature_score/$feature_max ($(( feature_score * 100 / feature_max ))%)"
    
    total_ref=$((total_ref + feature_score))
    max_ref=$((max_ref + feature_max))
}

# 進捗自動追跡システム
advanced_progress_tracking() {
    echo "📊 進捗自動追跡システム実行中..."
    
    local total_score=0
    local max_score=0
    
    # 1. 機能実装進捗
    echo "  🚀 機能実装進捗分析中..."
    track_feature_progress total_score max_score
    
    # 2. コード品質進捗
    echo "  💎 コード品質進捗分析中..."
    track_code_quality total_score max_score
    
    # 3. 自動化レベル進捗
    echo "  🤖 自動化レベル分析中..."
    track_automation_level total_score max_score
    
    # 4. 効率化進捗
    echo "  ⚡ 効率化進捗分析中..."
    track_efficiency_progress total_score max_score
    
    # 総合進捗レポート
    generate_progress_report "$total_score" "$max_score"
}

# 機能実装進捗追跡
track_feature_progress() {
    local -n total_ref=$1
    local -n max_ref=$2
    
    local feature_score=0
    local feature_max=100
    
    # Phase 1機能チェック（60点満点）
    [[ -f "HANDOVER_PROMPT.md" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/dev_command.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/natural_language_interface.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/github_auto_enhanced.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/fact_check_system.sh" ]] && feature_score=$((feature_score + 10))
    [[ -f "scripts/ai_development_assistant.sh" ]] && feature_score=$((feature_score + 10))
    
    # Phase 2機能チェック（40点満点）
    if [[ -f "scripts/ai_development_assistant.sh" ]]; then
        if grep -q "advanced_problem_detection" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "advanced_progress_tracking" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "implementation_proposal" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
        if grep -q "learning_system" scripts/ai_development_assistant.sh; then
            feature_score=$((feature_score + 10))
        fi
    fi
    
    echo "    機能実装進捗: $feature_score/$feature_max ($(( feature_score * 100 / feature_max ))%)"
    
    total_ref=$((total_ref + feature_score))
    max_ref=$((max_ref + feature_max))
}

# コード品質進捗追跡
track_code_quality() {
    local -n total_ref=$1
    local -n max_ref=$2
    
    local quality_score=0
    local quality_max=100
    
    # 構文チェック（30点満点）
    local syntax_errors=0
    for file in *.py; do
        if [[ -f "$file" && ! "$file" =~ (test_|_test\.py|.*_old\.py)$ ]]; then
            if ! python3 -m py_compile "$file" 2>/dev/null; then
                syntax_errors=$((syntax_errors + 1))
            fi
        fi
    done
    
    if [[ $syntax_errors -eq 0 ]]; then
        quality_score=$((quality_score + 30))
    elif [[ $syntax_errors -le 2 ]]; then
        quality_score=$((quality_score + 20))
    elif [[ $syntax_errors -le 5 ]]; then
        quality_score=$((quality_score + 10))
    fi
    
    # ドキュメント品質（30点満点）
    local doc_score=0
    [[ -f "README.md" ]] && doc_score=$((doc_score + 10))
    [[ -f "HANDOVER_PROMPT.md" ]] && doc_score=$((doc_score + 10))
    [[ -f "AI_GITHUB_AUTO_REPORT.md" ]] && doc_score=$((doc_score + 10))
    quality_score=$((quality_score + doc_score))
    
    # 設定ファイル品質（40点満点）
    local config_score=0
    if [[ -f "settings.json" ]]; then
        if python3 -m json.tool settings.json >/dev/null 2>&1; then
            config_score=$((config_score + 20))
        fi
        if grep -q "email" settings.json && grep -q "inverter" settings.json; then
            config_score=$((config_score + 20))
        fi
    fi
    quality_score=$((quality_score + config_score))
    
    echo "    コード品質進捗: $quality_score/$quality_max ($(( quality_score * 100 / quality_max ))%)"
    
    total_ref=$((total_ref + quality_score))
    max_ref=$((max_ref + quality_max))
}

# 自動化レベル追跡
track_automation_level() {
    local -n total_ref=$1
    local -n max_ref=$2
    
    local automation_score=0
    local automation_max=100
    
    # Cron自動化（40点満点）
    local cron_jobs=$(crontab -l 2>/dev/null | grep -v "^#" | wc -l)
    if [[ $cron_jobs -ge 5 ]]; then
        automation_score=$((automation_score + 40))
    elif [[ $cron_jobs -ge 3 ]]; then
        automation_score=$((automation_score + 30))
    elif [[ $cron_jobs -ge 1 ]]; then
        automation_score=$((automation_score + 20))
    fi
    
    # スクリプト自動化（30点満点）
    local script_count=$(find scripts/ -name "*.sh" -executable 2>/dev/null | wc -l)
    if [[ $script_count -ge 20 ]]; then
        automation_score=$((automation_score + 30))
    elif [[ $script_count -ge 10 ]]; then
        automation_score=$((automation_score + 20))
    elif [[ $script_count -ge 5 ]]; then
        automation_score=$((automation_score + 10))
    fi
    
    # 自然言語インターフェース（30点満点）
    if [[ -f "scripts/natural_language_interface.sh" ]]; then
        local nl_commands=$(grep -c "echo.*解釈:" scripts/natural_language_interface.sh 2>/dev/null || echo 0)
        if [[ $nl_commands -ge 10 ]]; then
            automation_score=$((automation_score + 30))
        elif [[ $nl_commands -ge 5 ]]; then
            automation_score=$((automation_score + 20))
        elif [[ $nl_commands -ge 1 ]]; then
            automation_score=$((automation_score + 10))
        fi
    fi
    
    echo "    自動化レベル進捗: $automation_score/$automation_max ($(( automation_score * 100 / automation_max ))%)"
    
    total_ref=$((total_ref + automation_score))
    max_ref=$((max_ref + automation_max))
}

# 効率化進捗追跡
track_efficiency_progress() {
    local -n total_ref=$1
    local -n max_ref=$2
    
    local efficiency_score=0
    local efficiency_max=100
    
    # Git効率化（30点満点）
    local git_commits=$(git log --oneline --since="1 week ago" | wc -l)
    if [[ $git_commits -ge 20 ]]; then
        efficiency_score=$((efficiency_score + 30))
    elif [[ $git_commits -ge 10 ]]; then
        efficiency_score=$((efficiency_score + 20))
    elif [[ $git_commits -ge 5 ]]; then
        efficiency_score=$((efficiency_score + 10))
    fi
    
    # AI開発支援（70点満点）
    local ai_features=0
    [[ -f "scripts/ai_development_assistant.sh" ]] && ai_features=$((ai_features + 20))
    [[ -f "scripts/fact_check_system.sh" ]] && ai_features=$((ai_features + 15))
    [[ -f "HANDOVER_PROMPT.md" ]] && ai_features=$((ai_features + 15))
    [[ -f "AI_GITHUB_AUTO_REPORT.md" ]] && ai_features=$((ai_features + 20))
    efficiency_score=$((efficiency_score + ai_features))
    
    echo "    効率化進捗: $efficiency_score/$efficiency_max ($(( efficiency_score * 100 / efficiency_max ))%)"
    
    total_ref=$((total_ref + efficiency_score))
    max_ref=$((max_ref + efficiency_max))
}

# 総合進捗レポート生成
generate_progress_report() {
    local total_score=$1
    local max_score=$2
    
    local progress_percentage=$((total_score * 100 / max_score))
    
    echo ""
    echo "📈 総合進捗レポート"
    echo "=================================="
    echo "総合進捗: $total_score/$max_score ($progress_percentage%)"
    echo ""
    
    # 進捗レベル判定
    if [[ $progress_percentage -ge 90 ]]; then
        echo "🏆 進捗レベル: 優秀 (90%以上)"
        echo "💡 状況: プロジェクトは非常に順調に進行しています"
    elif [[ $progress_percentage -ge 75 ]]; then
        echo "🎯 進捗レベル: 良好 (75-89%)"
        echo "💡 状況: プロジェクトは順調に進行しています"
    elif [[ $progress_percentage -ge 60 ]]; then
        echo "⚠️ 進捗レベル: 普通 (60-74%)"
        echo "💡 状況: 改善の余地があります"
    else
        echo "🚨 進捗レベル: 要改善 (60%未満)"
        echo "💡 状況: 重点的な改善が必要です"
    fi
    
    echo ""
    echo "🎯 次のマイルストーン予測:"
    predict_next_milestone "$progress_percentage"
}

# 次のマイルストーン予測
predict_next_milestone() {
    local current_progress=$1
    
    if [[ $current_progress -ge 90 ]]; then
        echo "  🚀 Phase 3: 予測型システム実装準備完了"
        echo "  📅 推定完了時期: 即座実行可能"
    elif [[ $current_progress -ge 75 ]]; then
        echo "  🔧 AI開発アシスタント完成"
        echo "  📅 推定完了時期: 30-60分"
    elif [[ $current_progress -ge 60 ]]; then
        echo "  📊 基盤システム安定化"
        echo "  📅 推定完了時期: 1-2時間"
    else
        echo "  🛠️ 基本機能の実装・修正"
        echo "  📅 推定完了時期: 2-4時間"
    fi
}

# 問題解決提案（修正版）

# 問題解決提案（修正版）
suggest_problem_solutions() {
    local issues_count=$1
    local -n errors_array=$2
    local -n warnings_array=$3
    
    # エラー別の解決策
    if [[ ${#errors_array[@]} -gt 0 ]]; then
        for error in "${errors_array[@]}"; do
            case "$error" in
                *"ファイル欠損"*)
                    echo "  🔧 git reset --hard HEAD でファイル復旧"
                    ;;
                *"JSON構文エラー"*)
                    echo "  🔧 ask \"settings.jsonを修正して\""
                    ;;
            esac
        done
    fi
    
    # 警告別の解決策
    if [[ ${#warnings_array[@]} -gt 0 ]]; then
        for warning in "${warnings_array[@]}"; do
            case "$warning" in
                *"Python構文エラー"*)
                    echo "  🔧 ask \"Python構文エラーを修正して\""
                    ;;
                *"パッケージ不足"*)
                    echo "  🔧 pip install [パッケージ名]"
                    ;;
                *"Git user.name"*)
                    echo "  🔧 git config user.name \"HANAZONOシステム\""
                    ;;
                *"パスワード情報"*)
                    echo "  🔧 設定ファイルのパスワード情報を環境変数に移行"
                    ;;
            esac
        done
    fi
}
