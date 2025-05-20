# v4_HANAZONOシステム／詳細引き継ぎプロンプト-20250519

## プロジェクト全体概要
HANAZONOシステムは、Raspberry Pi Zero 2 W上で動作するソーラー蓄電システム(LVYUAN SPI-10K-U)の自動最適化ソリューションです。GitHub(https://github.com/fffken/hanazono-system)で管理されている Python プロジェクトで、15分ごとのデータ収集と1日2回（7時・23時）のレポートメール送信機能を提供します。現在は$(date +%Y-%m-%d)に注力しています。

## 開発経緯と直面してきた課題
このプロジェクトでは、特にメール通知機能において「何度も何度も感性に近づいてはダメになり…を繰り返して」きた歴史があります。具体的には：
- 5月10日：正常に動作するメールテンプレートが完成
- 5月13日：変更が加えられ、メールテンプレートが「データなし」しか表示しなくなった
- 5月17日：開発プロセス改善と5月10日バージョンへの復元を開始
- 基本的なデータ収集システムの構築
- メール通知の基本機能実装
- 効率的な引き継ぎシステムの構築

この経験から、変更管理の徹底と、プロジェクトの状態を完全に把握できる仕組みの構築が最優先課題と認識しています。

## 依頼者の意図と優先事項
**最優先事項は、GitHub連携を通じてクレジット消費を抑制しながら効率的に開発を進める仕組みの構築です。** 具体的なコード修正や機能追加よりも、まずは以下を優先します：


## GitHub効率連携の具体的方法
現状のGitHubリポジトリを最大限活用するための具体的アプローチ：

### 1. 効率的な情報参照方法
```bash
# 開始時に実行する基本コマンド群
cd ~/lvyuan_solar_control
git pull  # 最新状態に更新
ls -la  # ファイル一覧確認
bash scripts/github_efficiency.sh  # 効率的な状態確認
cat PROJECT_STATUS.md  # 現在状態の確認
cat CHANGELOG.md  # 変更履歴の確認
```

### 2. 特定ファイル/コミットの参照方法
```bash
# 特定ファイルの状態確認
git show origin/main:email_notifier.py > current_email_notifier.py
git show <特定のコミットハッシュ>:email_notifier.py > specific_email_notifier.py
diff -u specific_email_notifier.py current_email_notifier.py | less
```

### 3. プロジェクト状態確認コマンド（AI利用時に実行）
```bash
# 状態確認と情報収集
bash scripts/project_status.sh
bash scripts/github_efficiency.sh
bash scripts/generate_handover.sh  # 引き継ぎプロンプト生成
```

## プロジェクトの現在の構成
現在の主要ファイル：

- main.py: システムのエントリーポイント
- email_notifier.py: メール通知機能（5月10日バージョンに復元済み）
- settings_manager.py: 設定管理クラス
- scripts/: ユーティリティスクリプト
  - project_status.sh: 状態確認スクリプト
  - github_efficiency.sh: GitHub効率連携スクリプト
  - generate_handover.sh: 引き継ぎプロンプト生成
  - organize_files.sh: ファイル整理スクリプト
- docs/: プロジェクトドキュメント

## 進行中のタスク
  1. email_notifier.pyのデバッグと安定化
  2. ドキュメント整備とGitHub管理
  

## 次のステップ詳細（優先順）


## 即時対応が必要な課題


## 対話進行方法（重要）
1. 各セッション開始時:
   * 必ずscripts/github_efficiency.shを実行し結果を共有
   * 前回からの変更や新たに発生した問題を報告

2. 変更管理の徹底:
   * すべての変更前にバックアップを作成
   * 変更はCHANGELOG.mdに記録
   * コミットには必ず意図と結果を記載

3. 問題発生時の対応:
   * 即座にバックアップから復元
   * 失敗した変更の原因を分析し記録
   * 段階的に修正を適用

次回以降のセッションでは、この引き継ぎプロンプトを使用して新しい対話を開始し、最初にGitHubの状態確認コマンドを実行することで、効率的にプロジェクト状況を把握してから作業を進めることを強く推奨します。クレジット消費を抑制しながら効率的に開発を進めるため、この方法を遵守してください。
