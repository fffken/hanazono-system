#!/bin/bash
# 構文エラー自動修正システム

TARGET_FILE="$1"
if [ -z "$TARGET_FILE" ]; then
    echo "使用方法: bash scripts/syntax_error_auto_fixer.sh ファイル名"
    exit 1
fi

echo "🔧 構文エラー自動修正開始: $TARGET_FILE"

# よくある構文エラーパターンの自動修正
sed -i 's/\*\*\([^*]*\)\*\*::/echo "\1:"/' "$TARGET_FILE"
sed -i 's/\*\*\([^*]*\)\*\*:/echo "\1:"/' "$TARGET_FILE"
sed -i 's/^##\s*\([^#]*\)$/echo "## \1"/' "$TARGET_FILE"

# 構文チェック実行
if bash -n "$TARGET_FILE" 2>/dev/null; then
    echo "✅ 構文エラー修正完了: $TARGET_FILE"
else
    echo "⚠️ 追加修正が必要: $TARGET_FILE"
    bash -n "$TARGET_FILE"
fi

# 追加修正パターン
echo "🔧 追加修正パターン適用中..."

# クォート不足の修正
sed -i 's/echo "システム:" \(.*\)/echo "システム: \1"/' "$TARGET_FILE"
sed -i 's/echo "\([^"]*\)" \([^"]*\)$/echo "\1 \2"/' "$TARGET_FILE"

# 再度構文チェック
echo "🧪 再構文チェック実行..."
if bash -n "$TARGET_FILE" 2>/dev/null; then
    echo "✅ 全ての構文エラー修正完了"
else
    echo "⚠️ 残存エラー詳細:"
    bash -n "$TARGET_FILE"
fi
