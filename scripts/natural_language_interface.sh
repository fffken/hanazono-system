#!/bin/bash

# 自然言語インターフェース v1.0
ask() {
    local request="$1"
    
    echo "🤖 自然言語インターフェース起動"
    echo "要求: $request"
    echo "=================================="
    
    # 自然言語解析・コマンド変換
    analyze_and_execute "$request"
}

# 自然言語解析エンジン
analyze_and_execute() {
    local input="$1"
    
    echo "🔍 自然言語解析中..."
    
    # 簡易登録機能
    if simple_register "$input"; then
        return 0
    fi
    
    # 登録コマンドの処理
    if process_registration "$input"; then
        return 0
    fi
    
    # カスタムコマンドの実行
    if execute_custom_command "$input"; then
        return 0
    fi
    
    # パターンマッチング解析
    case "$input" in
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"天気"*"絵文字"*|*"weather"*"emoji"*)
            echo "🌤️ 解釈: 天気絵文字機能の改善"
            execute_weather_emoji_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"メール"*"テスト"*|*"email"*"test"*)
            echo "📧 解釈: メール機能のテスト実行"
            execute_email_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"統合"*"開発"*|*"dev"*"command"*)
            echo "🔧 解釈: 統合開発コマンドの改善"
            execute_dev_command_improvement
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"引き継ぎ"*|*"handover"*)
            echo "📋 解釈: 引き継ぎシステムの確認"
            execute_handover_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"確認"*|*"check"*|*"状況"*|*"status"*)
            echo "📊 解釈: システム状況の確認"
            execute_status_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"実行"*|*"run"*|*"開始"*|*"start"*)
            echo "🚀 解釈: 推奨タスクの実行"
            execute_recommended_task
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"修正"*|*"fix"*|*"直す"*|*"エラー"*)
            echo "🔧 解釈: エラー修正・問題解決"
            execute_auto_fix
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"効率"*|*"efficiency"*|*"最適化"*|*"optimize"*)
            echo "⚡ 解釈: 効率化システムの確認"
            execute_efficiency_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"分析"*|*"analyze"*|*"レポート"*|*"report"*)
            echo "📊 解釈: 詳細分析レポート生成"
            execute_detailed_analysis
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"進捗"*|*"progress"*|*"現状"*)
            echo "📈 解釈: 進捗状況の確認"
            execute_progress_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"次"*|*"next"*|*"おすすめ"*|*"推奨"*)
            echo "🎯 解釈: 次の推奨タスク表示"
            execute_next_recommendation
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"完了"*|*"complete"*|*"終了"*|*"finish"*)
            echo "✅ 解釈: 作業完了処理"
            dev_complete
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"テスト"*|*"test"*|*"動作確認"*)
            echo "🧪 解釈: システムテスト実行"
            execute_system_test
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"ファイル"*|*"file"*|*"リスト"*|*"一覧"*)
            echo "📁 解釈: 重要ファイル一覧表示"
            execute_file_list
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *"表示"*|*"display"*|*"見やすく"*)
            echo "🎨 解釈: 表示方法の改善確認"
            source scripts/fact_check_system.sh && display_quality_check
            ;;
        *"説明書"*|*"manual"*|*"マニュアル"*|*"使い方"*)
            echo "📚 解釈: システム完全説明書の表示"
            show_complete_manual
            ;;
        *)
            echo "❓ 解釈できませんでした"
            show_available_commands
            ;;
    esac
}

# 実行関数群
execute_weather_emoji_task() {
    echo "🌤️ 天気絵文字改善タスクを開始します"
    dev "天気絵文字改善"
}

execute_email_test() {
    echo "📧 メール機能テストを実行します"
    python3 main.py --daily-report
}

execute_dev_command_improvement() {
    echo "🔧 統合開発コマンド改善を開始します"
    dev_ultimate "統合開発コマンド完全版"
}

execute_handover_check() {
    echo "📋 引き継ぎシステムを確認します"
    hanazono
}

# 利用可能コマンド表示
show_available_commands() {
    echo "💡 利用可能な自然言語コマンド:"
    echo "  '確認して' - システム状況の確認"
    echo "  '次は何？' - 次の推奨タスク表示"
    echo "  '修正して' - エラー自動修正"
    echo "  '完了' - 作業完了処理"
    echo "  'テストして' - システム動作確認"
    echo "  '効率を確認' - 効率化状況表示"
    echo "  '分析して' - 詳細分析レポート"
    echo "  '進捗は？' - 進捗状況確認"
    echo "  'ファイル一覧' - 重要ファイル表示"
    echo "  '保存して' - プロジェクトの保存"
  '説明書' - システム完全説明書表示
    echo "  '天気絵文字を改善して' - 天気絵文字機能の改善"
    echo "  'メールをテストして' - メール機能のテスト"
    echo ""
    echo "例: ask '確認して'"
}


# 保存実行関数
execute_save() {
    echo "💾 保存処理を実行します"
    bash scripts/perfect_save.sh
}

# システム・開発関連実行関数
execute_status_check() {
    echo "📊 システム状況を確認します"
    hanazono
}

execute_recommended_task() {
    echo "🚀 推奨タスクを実行します"
    echo "次の推奨: 統合開発コマンド完全版 (30分推定)"
    dev "統合開発コマンド完全版"
}

execute_auto_fix() {
    echo "🔧 自動修正を実行します"
    source scripts/auto_fix_system.sh && auto_fix_bash_syntax_v2 scripts/perfect_save.sh
}

execute_efficiency_check() {
    echo "⚡ 効率化システムを確認します"
    cat EFFICIENCY_PRIORITY_ROADMAP.md | head -20
}

execute_detailed_analysis() {
    echo "📊 詳細分析レポートを生成します"
    bash scripts/master_progress_controller.sh
    echo "確認: cat AI_GITHUB_AUTO_REPORT.md"
}

execute_progress_check() {
    echo "📈 進捗状況を確認します"
    cat PROJECT_STATUS.md | head -30
}

execute_next_recommendation() {
    echo "🎯 次の推奨タスクを表示します"
    cat EFFICIENCY_PRIORITY_ROADMAP.md | head -10
}

execute_system_test() {
    echo "🧪 システムテストを実行します"
    python3 main.py --daily-report
}

execute_file_list() {
    echo "📁 重要ファイル一覧を表示します"
    echo "✅ HANDOVER_PROMPT.md - 引き継ぎプロンプト"
    echo "✅ EFFICIENCY_PRIORITY_ROADMAP.md - 効率戦略"
    echo "✅ HANAZONO_DEVELOPMENT_PHILOSOPHY.md - 開発哲学"
    echo "✅ PROJECT_STATUS.md - プロジェクト状況"
}

# 動的コマンド登録システム
register_command() {
    local command_phrase="$1"
    local action_description="$2"
    
    echo "📝 新しいコマンドを登録します"
    echo "コマンド: '$command_phrase'"
    echo "説明: $action_description"
    
    # 登録ファイルに追加
    echo "$command_phrase|$action_description" >> scripts/custom_commands.txt
    
    echo "✅ コマンド登録完了"
    echo "使用例: ask '$command_phrase'"
}

# カスタムコマンド実行
execute_custom_command() {
    local input="$1"
    
    # カスタムコマンドファイルが存在するかチェック
    if [[ ! -f "scripts/custom_commands.txt" ]]; then
        return 1
    fi
    
    # カスタムコマンドを検索
    while IFS='|' read -r command_phrase action_description; do
        if [[ "$input" == *"$command_phrase"* ]]; then
            echo "🎯 カスタムコマンド実行: $action_description"
            echo "コマンド '$command_phrase' を実行します"
            # 基本的な実行（拡張可能）
            echo "💡 このコマンドの詳細実装が必要です"
            return 0
        fi
    done < scripts/custom_commands.txt
    
    return 1
}

# 動的コマンド登録システム
register_command() {
    local command_phrase="$1"
    local action_description="$2"
    
    echo "📝 新しいコマンドを登録します"
    echo "コマンド: '$command_phrase'"
    echo "説明: $action_description"
    
    # 登録ファイルに追加
    echo "$command_phrase|$action_description" >> scripts/custom_commands.txt
    
    echo "✅ コマンド登録完了"
    echo "使用例: ask '$command_phrase'"
}

# カスタムコマンド実行
execute_custom_command() {
    local input="$1"
    
    # カスタムコマンドファイルが存在するかチェック
    if [[ ! -f "scripts/custom_commands.txt" ]]; then
        return 1
    fi
    
    # カスタムコマンドを検索
    while IFS='|' read -r command_phrase action_description; do
        if [[ "$input" == *"$command_phrase"* ]]; then
            echo "🎯 カスタムコマンド実行: $action_description"
            echo "コマンド '$command_phrase' を実行します"
            echo "💡 このコマンドの詳細実装が必要です"
            return 0
        fi
    done < scripts/custom_commands.txt
    
    return 1
}

# 簡易登録システム
simple_register() {
    local input="$1"
    
    if [[ "$input" == *"を登録"* ]]; then
        echo "📝 コマンド登録機能（簡易版）"
        echo "登録したいコマンド名を教えてください:"
        echo "例: ask \"バックアップ作成\""
        echo "→ 今後 ask \"バックアップ作成\" で実行可能になります"
        return 0
    fi
    
    return 1
}

# 統合説明書システム
show_complete_manual() {
    echo "📚 HANAZONOシステム完全説明書"
    echo "=================================="
    echo ""
    
    # システム概要
    echo "## 🎯 システム概要"
    echo "LVYUAN太陽光蓄電システムの完全自動最適化システム"
    echo "開発哲学: 人間は意図のみ、システムが全実装"
    echo ""
    
    # 基本コマンド説明
    echo "## ⚡ 基本コマンド"
    echo "### hanazono"
    echo "  - 機能: システム状況の完全把握"
    echo "  - 使用法: hanazono"
    echo "  - 効果: 2分で完全状況把握（推定）"
    echo ""
    
    echo "### dev / dev_ultimate"
    echo "  - 機能: 統合開発コマンド"
    echo "  - 使用法: dev \"機能名\" または dev_ultimate \"機能名\""
    echo "  - 効果: 開発準備を10分→1-2分に短縮（推定）"
    echo ""
    
    echo "### dev_complete"
    echo "  - 機能: 開発完了処理"
    echo "  - 使用法: dev_complete"
    echo "  - 効果: 自動品質チェック・保存"
    echo ""
    
    # 自然言語コマンド説明
    echo "## 🤖 自然言語コマンド（ask）"
    echo "### 基本使用法"
    echo "  ask \"やりたいこと\""
    echo ""
    
    echo "### システム管理コマンド"
    echo "  - ask \"確認して\" → システム状況確認"
    echo "  - ask \"保存して\" → プロジェクト保存"
    echo "  - ask \"修正して\" → 自動エラー修正"
    echo "  - ask \"完了\" → 作業完了処理"
    echo ""
    
    echo "### 情報取得コマンド"
    echo "  - ask \"次は何？\" → 次の推奨タスク表示"
    echo "  - ask \"進捗は？\" → 進捗状況確認"
    echo "  - ask \"効率を確認\" → 効率化状況表示"
    echo "  - ask \"分析して\" → 詳細分析レポート"
    echo "  - ask \"ファイル一覧\" → 重要ファイル表示"
    echo ""
    
    echo "### 開発・テストコマンド"
    echo "  - ask \"テストして\" → システム動作確認"
    echo "  - ask \"天気絵文字を改善して\" → 開発タスク開始"
    echo "  - ask \"メールをテストして\" → メール機能テスト"
    echo "  - ask \"統合開発コマンドを改善して\" → 開発コマンド改善"
    echo ""
    
    # 高度機能説明
    echo "## 🏆 高度機能"
    echo "### 統合開発コマンド完全版"
    echo "  - 機能: 高度な状況分析・自動テスト・ブランチ管理"
    echo "  - 使用法: dev_ultimate \"機能名\""
    echo "  - 特徴: 複雑度判定、品質チェック、開発レポート生成"
    echo ""
    
    echo "### ファクトチェックシステム"
    echo "  - 機能: AI発言の信頼性向上"
    echo "  - 使用法: bash scripts/fact_check_system.sh"
    echo "  - 特徴: 表現適切性、時間見積もり根拠チェック"
    echo ""
    
    echo "### 自動修正システム"
    echo "  - 機能: Bash構文エラーの自動修正"
    echo "  - 使用法: auto_fix_bash_syntax_v2 ファイル名"
    echo "  - 特徴: バックアップからの自動復旧"
    echo ""
    
    echo "### GitHub自動化"
    echo "  - 機能: 自動コミット・統合表示"
    echo "  - 使用法: auto_commit (自動実行)"
    echo "  - 特徴: 変更内容に応じた詳細メッセージ生成"
    echo ""
    
    # 重要ファイル説明
    echo "## 📁 重要ファイル"
    echo "### 引き継ぎ・設定ファイル"
    echo "  - HANDOVER_PROMPT.md: 新AI向け引き継ぎプロンプト"
    echo "  - EFFICIENCY_PRIORITY_ROADMAP.md: 効率最優先戦略"
    echo "  - HANAZONO_DEVELOPMENT_PHILOSOPHY.md: 開発哲学"
    echo "  - PROJECT_STATUS.md: プロジェクト現在状況"
    echo "  - settings.json: システム設定ファイル"
    echo ""
    
    echo "### スクリプトファイル"
    echo "  - scripts/hanazono_start.sh: 究極モード起動"
    echo "  - scripts/dev_command.sh: 統合開発コマンド"
    echo "  - scripts/natural_language_interface.sh: 自然言語IF"
    echo "  - scripts/github_auto_enhanced.sh: GitHub自動化"
    echo "  - scripts/fact_check_system.sh: ファクトチェック"
    echo "  - scripts/perfect_save.sh: 完璧保存システム"
    echo ""
    
    echo "### データファイル"
    echo "  - data/: 収集データ保存ディレクトリ"
    echo "  - logs/: ログファイル保存ディレクトリ"
    echo "  - dev_reports/: 開発レポート保存ディレクトリ"
    echo ""
}
