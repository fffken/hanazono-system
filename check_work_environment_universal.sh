#!/bin/bash
# 汎用作業環境確認スクリプト v2.0
# 目的: あらゆるPythonプロジェクトの作業開始前確認で時間ロスを防止
# 使用方法: ./check_work_environment_universal.sh [対象モジュール名]

TARGET_MODULE=${1:-"email_notifier"}

echo "🔍 HANAZONOシステム汎用作業環境確認スクリプト v2.0"
echo "=================================================="
echo "🎯 対象モジュール: $TARGET_MODULE"
echo ""

# Step 1: main.pyの存在確認
if [ ! -f "main.py" ]; then
    echo "❌ main.pyが見つかりません"
    echo "💡 現在のディレクトリを確認してください: $(pwd)"
    exit 1
fi

# Step 2: main.pyのimport確認
echo "📋 main.pyの「$TARGET_MODULE」参照確認:"
echo "----------------------------------------"
import_lines=$(grep -n "from.*$TARGET_MODULE\|import.*$TARGET_MODULE" main.py)
if [ -n "$import_lines" ]; then
    echo "$import_lines"
    
    # 具体的なimport文を抽出
    actual_import=$(echo "$import_lines" | head -1 | cut -d: -f2-)
    echo "🎯 検出されたimport文: $actual_import"
else
    echo "⚠️ 「$TARGET_MODULE」関連のimportが見つかりません"
    echo "💡 利用可能なimport一覧:"
    grep -n "from.*import\|import.*" main.py | head -5
fi

echo ""

# Step 3: 関連ファイル一覧（サイズと更新時刻付き）
echo "📁 「$TARGET_MODULE」関連ファイル一覧:"
echo "------------------------------------"
related_files=$(ls ${TARGET_MODULE}*.py 2>/dev/null)
if [ -n "$related_files" ]; then
    # ファイルサイズと更新時刻も表示
    ls -la ${TARGET_MODULE}*.py | head -10
    echo ""
    echo "📊 ファイル数: $(echo "$related_files" | wc -l)個"
else
    echo "⚠️ 「$TARGET_MODULE」関連ファイルが見つかりません"
fi

echo ""

# Step 4: 実際に使用されるファイル確認
echo "🎯 実際にmain.pyが使用するファイル詳細:"
echo "---------------------------------------"
python3 -c "
import sys
import os

try:
    # モジュールをインポート
    module = __import__('$TARGET_MODULE')
    
    # モジュールファイルパス
    if hasattr(module, '__file__'):
        file_path = module.__file__
        print(f'✅ 使用ファイル: {file_path}')
        
        # ファイルサイズ
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f'📊 ファイルサイズ: {size:,}バイト')
            
            # 最終更新時刻
            import datetime
            mtime = os.path.getmtime(file_path)
            update_time = datetime.datetime.fromtimestamp(mtime)
            print(f'🕐 最終更新: {update_time.strftime(\"%Y-%m-%d %H:%M:%S\")}')
            
            # ファイル行数
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = len(f.readlines())
            print(f'📄 行数: {line_count:,}行')
        else:
            print(f'⚠️ ファイルが存在しません: {file_path}')
    else:
        print(f'⚠️ モジュール「$TARGET_MODULE」のファイルパスを取得できません')
    
    # 利用可能なクラス・関数一覧
    public_items = [item for item in dir(module) if not item.startswith('_')]
    if public_items:
        print(f'🔧 利用可能な要素: {len(public_items)}個')
        print(f'   主要要素: {public_items[:5]}' + ('...' if len(public_items) > 5 else ''))
    
except ImportError as e:
    print(f'❌ インポートエラー: {e}')
    print(f'💡 モジュール「$TARGET_MODULE」が存在しない可能性があります')
except Exception as e:
    print(f'❌ 確認エラー: {e}')
" 2>/dev/null

echo ""

# Step 5: 重要な確認事項（汎用版）
echo "⚠️  重要な確認事項:"
echo "-------------------"
echo "1. 上記の「使用ファイル」が作業対象ファイルと一致していることを確認"
echo "2. 作業前に必ずバックアップを作成"
echo "3. nanoエディター使用時は Ctrl+O → Enter → Ctrl+X で確実保存"
echo "4. 作業完了後は必ずテスト実行で動作確認"
echo "5. 複数の同名ファイルがある場合は import先を特定"

echo ""

# Step 6: よく使うコマンド（汎用版）
echo "🚀 よく使うコマンド:"
echo "------------------"
echo "バックアップ作成:"
echo "  cp $TARGET_MODULE.py $TARGET_MODULE.py.backup_\$(date +%Y%m%d_%H%M%S)"
echo ""
echo "テスト実行:"
echo "  python3 main.py --daily-report  # メイン機能テスト"
echo "  python3 $TARGET_MODULE.py       # モジュール単体テスト"
echo ""
echo "キャッシュクリア:"
echo "  find . -name \"*.pyc\" -delete && find . -name \"__pycache__\" -type d -exec rm -rf {} + 2>/dev/null || true"
echo ""
echo "構文チェック:"
echo "  python3 -m py_compile $TARGET_MODULE.py"

echo ""

# Step 7: 作業開始前チェックリスト
echo "📋 作業開始前チェックリスト:"
echo "---------------------------"
echo "□ 使用ファイルパスを確認済み"
echo "□ バックアップを作成済み"
echo "□ 作業対象ファイルを特定済み"
echo "□ テスト方法を確認済み"

echo ""
echo "✅ 確認完了 - 上記の情報を必ず確認してから作業開始してください"
echo "💡 問題があれば作業を中止し、ファイル参照を修正してください"
echo ""
echo "🔧 使用例:"
echo "  ./check_work_environment_universal.sh settings_manager"
echo "  ./check_work_environment_universal.sh lvyuan_collector"
echo "  ./check_work_environment_universal.sh weather_forecast"
