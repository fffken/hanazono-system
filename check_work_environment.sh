#!/bin/bash
# 作業環境確認スクリプト v1.0
# 目的: 作業開始前の必須確認で時間ロスを防止

echo "🔍 HANAZONOシステム作業環境確認スクリプト v1.0"
echo "=================================================="
echo ""

# Step 1: main.pyのimport確認
echo "📋 main.pyの参照ファイル確認:"
echo "----------------------------"
if [ -f "main.py" ]; then
    grep -n "from.*email_notifier\|import.*email_notifier" main.py || echo "⚠️ email_notifier関連のimportが見つかりません"
else
    echo "❌ main.pyが見つかりません"
fi

echo ""

# Step 2: email_notifier関連ファイル確認
echo "📁 email_notifier関連ファイル一覧（サイズ順）:"
echo "--------------------------------------------"
ls -la email_notifier*.py 2>/dev/null | head -10 || echo "⚠️ email_notifier関連ファイルが見つかりません"

echo ""

# Step 3: 実際に使用されるファイル確認
echo "🎯 実際にmain.pyが使用するファイル:"
echo "--------------------------------"
python3 -c "
try:
    import email_notifier
    import inspect
    file_path = inspect.getfile(email_notifier.EnhancedEmailNotifier)
    print(f'✅ 使用ファイル: {file_path}')
    
    import os
    size = os.path.getsize(file_path)
    print(f'📊 ファイルサイズ: {size:,}バイト')
    
    # ファイル更新時刻
    import datetime
    mtime = os.path.getmtime(file_path)
    update_time = datetime.datetime.fromtimestamp(mtime)
    print(f'🕐 最終更新: {update_time.strftime(\"%Y-%m-%d %H:%M:%S\")}')
    
except Exception as e:
    print(f'❌ ファイル確認エラー: {e}')
" 2>/dev/null

echo ""

# Step 4: 重要な確認事項
echo "⚠️  重要な確認事項:"
echo "-------------------"
echo "1. 上記の「使用ファイル」が作業対象ファイルと一致していることを確認"
echo "2. 作業前に必ずバックアップを作成"
echo "3. nanoエディター使用時は保存確認を徹底"
echo "4. 作業完了後は必ずテスト実行で確認"

echo ""

# Step 5: よく使うコマンド
echo "🚀 よく使うコマンド:"
echo "------------------"
echo "バックアップ作成: cp email_notifier.py email_notifier.py.backup_\$(date +%Y%m%d_%H%M%S)"
echo "テスト実行: python3 main.py --daily-report"
echo "キャッシュクリア: find . -name \"*.pyc\" -delete && find . -name \"__pycache__\" -type d -exec rm -rf {} + 2>/dev/null || true"

echo ""
echo "✅ 確認完了 - 上記の情報を必ず確認してから作業開始してください"
echo "💡 問題があれば作業を中止し、ファイル参照を修正してください"
