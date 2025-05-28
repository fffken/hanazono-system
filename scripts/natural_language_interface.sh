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
    
    # パターンマッチング解析
    case "$input" in
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"天気"*"絵文字"*|*"weather"*"emoji"*)
            echo "🌤️ 解釈: 天気絵文字機能の改善"
            execute_weather_emoji_task
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"メール"*"テスト"*|*"email"*"test"*)
            echo "📧 解釈: メール機能のテスト実行"
            execute_email_test
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"統合"*"開発"*|*"dev"*"command"*)
            echo "🔧 解釈: 統合開発コマンドの改善"
            execute_dev_command_improvement
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
            ;;
        *"引き継ぎ"*|*"handover"*)
            echo "📋 解釈: 引き継ぎシステムの確認"
            execute_handover_check
            ;;
        *"保存"*|*"save"*|*"セーブ"*)
            echo "💾 解釈: プロジェクトの保存"
            execute_save
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
    dev "統合開発コマンド改善"
}

execute_handover_check() {
    echo "📋 引き継ぎシステムを確認します"
    hanazono
}

# 利用可能コマンド表示
show_available_commands() {
    echo "💡 利用可能な自然言語コマンド:"
    echo "  '天気絵文字を改善して' - 天気絵文字機能の改善"
    echo "  'メールをテストして' - メール機能のテスト"
    echo "  '統合開発コマンドを改善して' - 開発コマンドの改善"
    echo "  '引き継ぎを確認して' - 引き継ぎシステムの確認"
    echo ""
  '保存して' - プロジェクトの保存
    echo "例: ask '天気絵文字を改善して'"
}


# 保存実行関数
execute_save() {
    echo "💾 保存処理を実行します"
    bash scripts/perfect_save.sh
}
