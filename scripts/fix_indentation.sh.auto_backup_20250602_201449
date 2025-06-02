#!/bin/bash

# インデント問題を検出し自動修正するスクリプト
# fix_indentation.sh

# バックアップ作成
echo "バックアップを作成しています..."
cp email_notifier.py email_notifier.py.bak.$(date +%Y%m%d%H%M%S)

# 必要なツールのインストール確認
if ! command -v pycodestyle &> /dev/null; then
    echo "pycodestyle をインストールしています..."
    pip install pycodestyle
fi

# インデント問題の特定
echo "インデント問題を検出しています..."
pycodestyle --select=E111,E114,E117,E121,E122,E123,E124,E125,E126,E127,E128,E129,E131 email_notifier.py > indent_issues.txt

# 問題行数のカウント
issue_count=$(wc -l < indent_issues.txt)
echo "検出されたインデント問題: $issue_count 箇所"

# 問題がない場合は終了
if [ $issue_count -eq 0 ]; then
    echo "インデント問題は見つかりませんでした。"
    rm indent_issues.txt
    exit 0
fi

# 一時ファイルの作成
cp email_notifier.py email_notifier.py.tmp

# 各問題行の処理
echo "インデント問題を修正しています..."
while read -r line; do
    # 行番号とエラータイプを抽出
    line_num=$(echo "$line" | grep -o 'email_notifier.py:[0-9]\+' | cut -d: -f2)
    error_type=$(echo "$line" | grep -o 'E[0-9]\+' | head -1)
    
    echo "処理中: 行 $line_num, エラー $error_type"
    
    # エラータイプに応じた修正
    case "$error_type" in
        E111|E114|E117) # インデントはスペース4つでないといけない
            # 行の内容を取得
            line_content=$(sed -n "${line_num}p" email_notifier.py.tmp)
            # 行頭スペースを数える
            leading_spaces=$(echo "$line_content" | grep -o '^ *' | wc -c)
            # 正しいインデントレベル計算（4の倍数に調整）
            correct_indent=$((($leading_spaces + 3) / 4 * 4))
            # 行の修正（行頭スペースを置換）
            sed -i "${line_num}s/^[ ]*/$(printf '%*s' $correct_indent '')/g" email_notifier.py.tmp
            ;;
        E121|E122|E123|E124|E125|E126|E127|E128|E129|E131) # 連続行のインデント問題
            # 前の行のインデントパターンを参照
            prev_line=$((line_num - 1))
            prev_content=$(sed -n "${prev_line}p" email_notifier.py.tmp)
            prev_spaces=$(echo "$prev_content" | grep -o '^ *' | wc -c)
            
            # 現在の行を取得
            curr_content=$(sed -n "${line_num}p" email_notifier.py.tmp)
            
            # 行の種類によってインデント調整
            if [[ "$curr_content" =~ ^\s*[\)\]}] ]]; then
                # 閉じ括弧類は1レベル下げる
                correct_indent=$((prev_spaces - 4))
                [ $correct_indent -lt 0 ] && correct_indent=0
            else
                # それ以外は同じか1レベル上げる
                if [[ "$prev_content" =~ [\(\[\{]$ ]]; then
                    correct_indent=$((prev_spaces + 4))
                else
                    correct_indent=$prev_spaces
                fi
            fi
            
            # 行の修正
            sed -i "${line_num}s/^[ ]*/$(printf '%*s' $correct_indent '')/g" email_notifier.py.tmp
            ;;
    esac
done < indent_issues.txt

# 修正後の検証
echo "修正結果を検証中..."
if python3 -m py_compile email_notifier.py.tmp 2>/dev/null; then
    echo "修正成功！インデントエラーが解消されました。"
    mv email_notifier.py.tmp email_notifier.py
    rm indent_issues.txt
else
    echo "修正が不完全です。まだPython構文エラーが残っています。"
    # エラー詳細の表示
    python3 -m py_compile email_notifier.py.tmp
    mv email_notifier.py.tmp email_notifier.py.fixed
    echo "部分的に修正したファイルを email_notifier.py.fixed として保存しました。"
    echo "さらなる修正が必要です。"
fi

echo "処理が完了しました。"
