#!/bin/bash
# 自動作業支援システム v3.0（オプション機能）
# 既存システムを一切変更しない独立型

echo "🤖 自動作業支援システム（オプション機能）"
echo "====================================="
echo ""

# 設定ファイル確認（自動化レベル制御）
AUTO_CONFIG=".auto_work_config"
if [ ! -f "$AUTO_CONFIG" ]; then
    echo "📋 初回起動：自動化レベルを選択してください"
    echo "1) 無効（手動のみ）"
    echo "2) 部分自動（確認付き）"
    echo "3) 完全自動（推奨）"
    read -p "選択 (1-3): " choice
    echo "auto_level=$choice" > "$AUTO_CONFIG"
    echo "✅ 設定保存完了"
fi

# 設定読み込み
source "$AUTO_CONFIG"

case $auto_level in
    1)
        echo "🔧 手動モード：何も実行しません"
        ;;
    2)
        echo "🔍 部分自動モード：確認付きで実行"
        if [ -f "check_work_environment_universal.sh" ]; then
            read -p "環境確認を実行しますか？ (y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                ./check_work_environment_universal.sh
            fi
        fi
        ;;
    3)
        echo "🚀 完全自動モード：環境確認を自動実行"
        if [ -f "check_work_environment_universal.sh" ]; then
            ./check_work_environment_universal.sh
        fi
        ;;
esac

echo ""
echo "💡 設定変更: nano .auto_work_config"
echo "💡 無効化: rm .auto_work_config"
