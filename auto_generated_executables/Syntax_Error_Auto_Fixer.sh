#!/bin/bash

# 🚀 実行開始: Syntax_Error_Auto_Fixer
# 📝 説明: 構文エラー自動修正システム - インデントエラー・構文エラーの自動検出・修正

# === 構文エラー自動修正システム v1.0 ===
echo "🔧 構文エラー自動修正システム v1.0 開始..."

# 1. 構文エラー自動検出
function detect_syntax_errors() {
    local file="$1"
    echo "🔍 構文エラー検出中: $file"
    
    # Python構文チェック
    local error_output=$(python3 -m py_compile "$file" 2>&1)
    local exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo "❌ 構文エラー検出: $file"
        echo "$error_output"
        return 1
    else
        echo "✅ 構文チェック正常: $file"
        return 0
    fi
}

# 2. インデントエラー自動修正
function fix_indentation_errors() {
    local file="$1"
    echo "🔧 インデントエラー自動修正中: $file"
    
    # バックアップ作成
    cp "$file" "$file.backup_before_indent_fix"
    
    # インデント問題の一般的修正
    python3 << 'INDENT_FIX'
import sys
import re

file_path = sys.argv[1] if len(sys.argv) > 1 else 'enhanced_email_system.py'

with open(file_path, 'r') as f:
    content = f.read()

# 一般的なインデント問題を修正
lines = content.split('\n')
fixed_lines = []

for i, line in enumerate(lines):
    # 関数定義のインデント修正
    if 'def ' in line and line.startswith('        def '):
        line = line.replace('        def ', '    def ')
    elif 'def ' in line and line.startswith('            def '):
        line = line.replace('            def ', '    def ')
    
    fixed_lines.append(line)

with open(file_path, 'w') as f:
    f.write('\n'.join(fixed_lines))

print("✅ インデント自動修正完了")
INDENT_FIX
    
    echo "✅ インデント修正完了: $file"
}

# 3. 統合自動修正実行
function auto_fix_syntax_errors() {
    local file="$1"
    echo "🚀 統合自動修正実行: $file"
    
    # Step 1: 構文エラー検出
    if detect_syntax_errors "$file"; then
        echo "✅ 構文エラーなし: $file"
        return 0
    fi
    
    # Step 2: インデント修正試行
    fix_indentation_errors "$file"
    
    # Step 3: 修正後再検証
    if detect_syntax_errors "$file"; then
        echo "✅ 自動修正成功: $file"
        return 0
    else
        echo "❌ 自動修正失敗: $file"
        # バックアップから復元
        cp "$file.backup_before_indent_fix" "$file"
        return 1
    fi
}

# 4. 実行関数
function execute_syntax_fixer() {
    local target_file="${1:-enhanced_email_system.py}"
    echo "🎯 構文エラー自動修正対象: $target_file"
    auto_fix_syntax_errors "$target_file"
}

# enhanced_email_system.pyの自動修正実行
execute_syntax_fixer "enhanced_email_system.py"
