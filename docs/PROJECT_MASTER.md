# HANAZONOソーラー蓄電システム自動最適化プロジェクト - マスタードキュメント

Version: 1.0.0
Last Updated: 2025-05-03
Based on: 「HANAZONOシステム自動最適化プロジェクト - 統合ロードマップ+」

## 1. プロジェクト概要 [v1.0.0]

### 1.1 システム基本構成
- 制御システム: Raspberry Pi Zero 2 W
- オペレーティングシステム: Linux (Raspbian)
- プログラミング言語: Python 3.11
- ソーラー蓄電システム: LVYUAN製
- インバーター: SPI-10K-U (10kW)
- バッテリー: FLCD16-10048 × 4台（合計20.48kWh）
- ソーラーパネル: 現在6枚稼働（追加6枚は保管中、将来拡張予定）
- 通信モジュール: LSW-5A8153-RS485 WiFiモジュール (Modbus対応)
- 通信仕様: ボーレート9600bps、データビット8bit、チェックビットNone、ストップビット1bit

### 1.2 電力プラン・料金体系
- 契約: 四国電力「季節別時間帯別電灯」
- 料金区分:
  - 夜間(23:00〜翌7:00): 26.00円/kWh
  - 昼間その他季: 37.34円/kWh
  - 昼間夏季(7〜9月): 42.76円/kWh

### 1.3 運用基本方針
- 基本運用方式: タイプB（省管理型・年3回設定）
  - 冬季(12-3月): 充電電流60A、充電時間60分、出力切替SOC 60%
  - 春秋季(4-6月,10-11月): 充電電流50A、充電時間45分、出力切替SOC 45%
  - 夏季(7-9月): 充電電流35A、充電時間30分、出力切替SOC 35%
- 補助運用方式: タイプA（変動型）...特殊気象条件時や特別な需要パターン時のみ一時的に手動切替

## 2. 現在の実装状況 [v1.0.0]

### 2.1 コアモジュール（進行状況）
- lvyuan_collector.py: インバーターデータ収集（完了）
- email_notifier.py: 日次レポート送信（部分完了、エラー対応中）
- settings_manager.py: 設定管理（完了）
- logger_util.py: ロギング機能（設計段階）
- main.py: 制御統合（完了）

### 2.2 実装済みの機能詳細
- 15分ごとインバーターから各種パラメータ自動収集
- 日次レポート（日々グラフ付きで8時に送信）、異常検出時自動アラート
- Tailscaleによるセキュアなリモートアクセス

## 3. 開発フェーズと優先タスク [v1.0.0]

### 3.1 フェーズ1：基盤強化とモジュール化（1-2週間）
- メール送信問題の修正（前日データ不足時。現在進行中）
- ロギング機能強化と統合（未着手）
- ディレクトリ構造整理（未着手）
- バージョン管理システムの実装（進行中）

### 3.2 フェーズ2：データベース実装（2-3週間）
- SQLiteデータベース設計（未着手、高優先度）
- JSONデータのSQLite移行ツール（未着手、高優先度）
- データベースクエリとレポート機能（未着手）

### 3.3 フェーズ3：予測・分析エンジン（3-4週間）
- 天気API連携（未着手、高優先度）
- 気温と発電効率の相関分析（未着手）
- 翌日の発電量予測モデル（未着手）
- 7日先までの運用最適化（未着手）

## 4. 実装ルールとガイドライン [v1.0.0]

### 4.1 コーディング規約
- PEP 8に準拠
- ドキュメント文字列は全ての関数・メソッドに記載
- 変更履歴をコメントとして残す

### 4.2 バージョン管理
- 各ファイルにバージョン情報を含める
- メジャー.マイナー.パッチ形式を使用
- 変更内容はCHANGELOG.mdに記録

### 4.3 季節・天候別の推奨設定値（タイプB）
- 冬季(12-3月): 充電電流 60A, 充電時間 60分, 出力切替SOC 60%
- 春秋季(4-6月,10-11月): 充電電流 50A, 充電時間 45分, 出力切替SOC 45%
- 夏季(7-9月): 充電電流 35A, 充電時間 30分, 出力切替SOC 35%

## 変更履歴
- 2025-05-03: 初期バージョン作成（統合ロードマップ+を基に）
