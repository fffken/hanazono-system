# 安全開発ガイド

## 基本コマンド
```bash
# 1. 安全な実装開始
bash scripts/safe_dev.sh "機能名"

# 2. 安全なファイル編集
bash scripts/safe_edit.sh ファイル名 編集コマンド

# 3. セーフポイント作成
source scripts/savepoint.sh && save "説明"

# 4. 緊急復旧
source scripts/savepoint.sh && restore
天気絵文字改善の正しい手順
Copy# 1. 安全開発開始
bash scripts/safe_dev.sh "天気絵文字改善"

# 2. nanoで手動編集
nano enhanced_email_system_v2.py

# 3. 完了確認後Enterキー
