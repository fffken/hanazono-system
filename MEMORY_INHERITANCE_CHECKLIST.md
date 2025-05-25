# 新AI向け必須確認事項

## 安全開発システム
- 天気絵文字実装失敗の教訓理解
- `scripts/safe_dev.sh` 存在確認

## 開発時必須ルール
- 実装前: `bash scripts/safe_dev.sh "機能名"`
- 編集: nanoエディター使用
- 緊急時: `source scripts/savepoint.sh && restore`

## 禁止事項
- `cat >>` でのPythonファイル編集禁止
- 時間切れ近くでの実装禁止
