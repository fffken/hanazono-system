#!/bin/bash
# 5月10日の正常動作バージョンメール機能復元スクリプト

# バックアップ作成
DATE=$(date +%Y%m%d_%H%M%S)
cp email_notifier.py email_notifier.py.bak_${DATE}
echo "現在のバージョンをバックアップしました: email_notifier.py.bak_${DATE}"

# 5月10日のバージョンを確認
echo "利用可能な5月10日のバックアップファイル:"
ls -la email_notifier.py.bak_2025051*

# 利用するバックアップファイルの選択
read -p "復元に使用するバックアップファイル名を入力してください: " RESTORE_FILE

if [ ! -f "$RESTORE_FILE" ]; then
  echo "エラー: 指定されたファイルが存在しません"
  exit 1
fi

# 選択したファイルの内容を確認
echo "選択したファイルの先頭部分:"
head -n 20 "$RESTORE_FILE"

read -p "このファイルを復元しますか？ (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
  echo "復元をキャンセルしました"
  exit 0
fi

# ファイル復元
cp "$RESTORE_FILE" email_notifier.py
echo "復元が完了しました"

# テスト実行
read -p "テストを実行しますか？ (y/n): " RUN_TEST
if [ "$RUN_TEST" = "y" ]; then
  echo "テスト実行中..."
  python3 main.py --daily-report --debug
fi

echo "変更をコミットするには:"
echo "git add email_notifier.py"
echo "git commit -m \"HANA-EMAIL-001: メールテンプレートを5月10日バージョンに復元\""
