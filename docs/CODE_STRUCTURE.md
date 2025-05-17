# HANAZONOシステム コード構造

## コアファイル
- **main.py**: メインエントリーポイント、引数処理、機能実行
- **email_notifier.py**: メール通知機能、レポート生成
- **lvyuan_collector.py**: ソーラーインバーターからのデータ収集
- **settings_manager.py**: 設定管理クラス

## ユーティリティ
- **logger_util.py**: ロギング機能
- **data_util.py**: データ変換・処理ユーティリティ

## その他
- **scripts/**: ユーティリティスクリプト
- **data/**: データファイル保存ディレクトリ
- **logs/**: ログファイル保存ディレクトリ

## データフロー
1. **データ収集**: `main.py --collect` → `lvyuan_collector.py` → `data/`
2. **レポート送信**: `main.py --daily-report` → `data/` → `email_notifier.py`
