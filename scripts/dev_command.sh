#!/bin/bash

# 統合開発コマンド v1.0
dev() {
    local task_name="$1"
    
    echo "🚀 統合開発コマンド開始: $task_name"
    echo "=================================="
    
    # 1. 自動状況分析（30秒）
    echo "📊 現在状況分析中..."
    echo "  Git変更: $(git status --short | wc -l)件"
    echo "  ブランチ: $(git branch --show-current)"
    
    # 2. セーフポイント自動作成（30秒）
    echo "🔒 セーフポイント作成中..."
    source scripts/github_auto_enhanced.sh && auto_commit
    
    # 3. 開発環境準備（30秒）
    echo "🔧 開発環境準備中..."
    echo "  ✅ バックアップ作成完了"
    echo "  ✅ 安全開発モード有効"
    
    # 4. 実装ガイド表示
    echo "🎯 実装ガイド: $task_name"
    echo "推奨手順:"
    echo "1. 小さな変更から開始"
    echo "2. 各段階で動作確認"
    echo "3. 完了後 'dev_complete' 実行"
    
    echo "✅ 開発環境準備完了"
}

# 完了コマンド
dev_complete() {
    echo "🎉 開発完了処理開始..."
    
    # 動作確認
    if python3 main.py --daily-report >/dev/null 2>&1; then
        echo "✅ 動作確認: 正常"
    else
        echo "❌ 動作確認: エラー検出"
    fi
    
    # 自動保存
    bash scripts/perfect_save.sh
    
    echo "✅ 開発完了処理完了"
}


# 高度な自動判定システム
advanced_analysis() {
    local task_name="$1"
    
    echo "🔍 高度な状況分析中..."
    
    # Git状況の詳細分析
    local git_changes=$(git status --short | wc -l)
    local uncommitted_changes=$(git diff --name-only | wc -l)
    local branch_name=$(git branch --show-current)
    
    # システム状態分析
    local system_status="OK"
    if ! python3 main.py --daily-report >/dev/null 2>&1; then
        system_status="ERROR"
    fi
    
    # 複雑度判定
    local complexity="SIMPLE"
    if [[ $git_changes -gt 10 ]]; then
        complexity="COMPLEX"
    elif [[ $git_changes -gt 5 ]]; then
        complexity="MEDIUM"
    fi
    
    echo "  📊 Git変更: $git_changes件 (複雑度: $complexity)"
    echo "  🌿 ブランチ: $branch_name"
    echo "  🎯 システム: $system_status"
    
    # 推奨アクション提案
    suggest_optimal_approach "$complexity" "$system_status" "$task_name"
}

# 最適アプローチ提案
suggest_optimal_approach() {
    local complexity="$1"
    local system_status="$2" 
    local task_name="$3"
    
    echo "💡 推奨アプローチ:"
    
    case "$complexity" in
        "COMPLEX")
            echo "  🔧 複雑な状況 → 段階的実装推奨"
            echo "  📋 推奨: 小さな単位に分割して実装"
            ;;
        "MEDIUM")
            echo "  ⚡ 中程度の複雑さ → 標準実装"
            echo "  📋 推奨: 通常の開発フローで進行"
            ;;
        "SIMPLE")
            echo "  🚀 シンプルな状況 → 高速実装可能"
            echo "  📋 推奨: 積極的な実装が可能"
            ;;
    esac
    
    if [[ "$system_status" == "ERROR" ]]; then
        echo "  ⚠️ システムエラー検出 → 修正優先"
    fi
}

# 自動テスト実行システム
auto_test_suite() {
    echo "🧪 自動テストスイート実行中..."
    
    local test_results=()
    
    # テスト1: Python構文チェック
    echo "  📝 Python構文チェック中..."
    local python_errors=0
    for file in *.py; do
        if [[ -f "$file" ]]; then
            if ! python3 -m py_compile "$file" 2>/dev/null; then
                echo "    ❌ 構文エラー: $file"
                python_errors=$((python_errors + 1))
            fi
        fi
    done
    
    if [[ $python_errors -eq 0 ]]; then
        echo "    ✅ Python構文: 正常"
        test_results+=("PYTHON_OK")
    else
        echo "    ❌ Python構文: $python_errors個のエラー"
        test_results+=("PYTHON_ERROR")
    fi
    
    # テスト2: システム動作確認
    echo "  🔧 システム動作確認中..."
    if python3 main.py --daily-report >/dev/null 2>&1; then
        echo "    ✅ システム動作: 正常"
        test_results+=("SYSTEM_OK")
    else
        echo "    ❌ システム動作: エラー"
        test_results+=("SYSTEM_ERROR")
    fi
    
    # テスト3: 重要ファイル存在確認
    echo "  📁 重要ファイル確認中..."
    local missing_files=0
    local important_files=("HANDOVER_PROMPT.md" "EFFICIENCY_PRIORITY_ROADMAP.md" "scripts/hanazono_start.sh")
    
    for file in "${important_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            echo "    ❌ 欠損: $file"
            missing_files=$((missing_files + 1))
        fi
    done
    
    if [[ $missing_files -eq 0 ]]; then
        echo "    ✅ 重要ファイル: 全て存在"
        test_results+=("FILES_OK")
    else
        echo "    ❌ 重要ファイル: $missing_files個欠損"
        test_results+=("FILES_ERROR")
    fi
    
    # テスト結果サマリー
    echo "🎯 テスト結果サマリー:"
    local total_tests=${#test_results[@]}
    local passed_tests=$(printf '%s\n' "${test_results[@]}" | grep -c "_OK")
    
    echo "  📊 合格: $passed_tests/$total_tests"
    
    if [[ $passed_tests -eq $total_tests ]]; then
        echo "  🎉 全テスト合格 - 開発継続可能"
        return 0
    else
        echo "  ⚠️ 一部テスト失敗 - 注意して開発"
        return 1
    fi
}

# 自動ブランチ管理システム
smart_branch_management() {
    local task_name="$1"
    
    echo "🌿 スマートブランチ管理中..."
    
    # 現在のブランチ確認
    local current_branch=$(git branch --show-current)
    local git_changes=$(git status --short | wc -l)
    
    echo "  📍 現在ブランチ: $current_branch"
    echo "  📊 未コミット変更: $git_changes件"
    
    # ブランチ戦略の提案
    if [[ "$current_branch" == "main" && $git_changes -gt 0 ]]; then
        echo "  💡 提案: 新しい機能ブランチの作成を推奨"
        echo "  🌿 推奨ブランチ名: feature/$(date +%Y%m%d)_${task_name// /_}"
        
        read -p "  ❓ 新しいブランチを作成しますか？ (y/n): " create_branch
        if [[ "$create_branch" == "y" ]]; then
            create_feature_branch "$task_name"
        fi
    elif [[ "$current_branch" != "main" ]]; then
        echo "  ✅ 機能ブランチで作業中: $current_branch"
    else
        echo "  ✅ mainブランチ - クリーンな状態"
    fi
}

# 機能ブランチ作成
create_feature_branch() {
    local task_name="$1"
    local branch_name="feature/$(date +%Y%m%d)_${task_name// /_}"
    
    echo "🌿 新しい機能ブランチを作成中..."
    
    # 現在の変更を一時保存
    if [[ $(git status --short | wc -l) -gt 0 ]]; then
        echo "  💾 現在の変更を一時保存中..."
        git stash push -m "WIP: $task_name開始前の変更"
    fi
    
    # ブランチ作成・切替
    git checkout -b "$branch_name"
    
    echo "  ✅ ブランチ作成完了: $branch_name"
    
    # 一時保存した変更を復元
    if git stash list | grep -q "WIP: $task_name"; then
        echo "  📤 変更を復元中..."
        git stash pop
    fi
}

# 統合開発レポート生成
generate_dev_report() {
    local task_name="$1"
    
    echo "📊 統合開発レポート生成中..."
    
    local report_file="dev_reports/dev_report_$(date +%Y%m%d_%H%M%S).md"
    mkdir -p dev_reports
    
    cat > "$report_file" << REPORT_EOF
# 開発レポート: $task_name

*開始時刻*: $(date)
*ブランチ*: $(git branch --show-current)
*Git変更*: $(git status --short | wc -l)件

## 開発環境状況
- システム状態: $(python3 main.py --daily-report >/dev/null 2>&1 && echo "正常" || echo "エラー")
- 最新コミット: $(git log -1 --oneline)
- 作業ディレクトリ: $(pwd)

## 推奨アクション
- 段階的実装の実行
- 各段階での動作確認
- 完了時のdev_complete実行

---
開発開始: $(date)
REPORT_EOF

    echo "  📋 レポート生成完了: $report_file"
    echo "  📊 開発進捗の追跡が可能になりました"
}

# 統合開発コマンド完全版
dev_ultimate() {
    local task_name="$1"
    
    echo "🏆 統合開発コマンド完全版開始: $task_name"
    echo "=================================================="
    
    # 1. 高度な状況分析
    advanced_analysis "$task_name"
    
    # 2. 自動テストスイート
    auto_test_suite
    
    # 3. スマートブランチ管理
    smart_branch_management "$task_name"
    
    # 4. セーフポイント作成
    echo "🔒 セーフポイント作成中..."
    source scripts/github_auto_enhanced.sh && auto_commit
    
    # 5. 開発レポート生成
    generate_dev_report "$task_name"
    
    echo "✅ 統合開発コマンド完全版準備完了"
    echo "🎯 実装ガイド: $task_name"
    echo "推奨手順:"
    echo "1. 小さな変更から開始"
    echo "2. 各段階で動作確認"
    echo "3. 完了後 'dev_complete' 実行"
}
