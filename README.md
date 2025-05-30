# HANAZONOシステム

HANAZONOシステムは、Raspberry Pi Zero 2 W上で動作するソーラー蓄電システム(LVYUAN SPI-10K-U)の自動最適化ソリューションです。

## 機能
- 15分ごとのデータ収集
- 1日2回（7時・23時）のレポートメール送信
- ソーラー発電・消費の最適化

## プロジェクト状態
最新のプロジェクト状態は以下のコマンドで確認できます：
bash scripts/github_efficiency.sh


## 引き継ぎプロセス
新しい開発セッションを開始する際は、以下の手順でスムーズに引き継ぎを行えます：
1. PROJECT_HANDOVER.mdの内容をAIに共有
2. github_efficiency.shの実行結果を共有
3. 必要に応じてgenerate_raw_links.shの結果も共有

## ドキュメント
詳細なドキュメントは「docs」ディレクトリに保存されています。

## 🤖 AI引き継ぎ用クイックスタート

新しいAIセッション開始時は、以下のコマンドを実行してください：

\`\`\`bash
# 完全引き継ぎ情報取得
bash scripts/ai_handover_complete.sh
\`\`\`

### GitHub API利用方法
\`\`\`python
from github_auto_fetch import GitHubAutoFetch
fetcher = GitHubAutoFetch()
content = fetcher.get_file_content('ファイル名')
\`\`\`

### 重要設定
- GitHubトークン: 自動設定済み
- API権限: プライベートリポジトリアクセス可能
- 有効期限: 2025年8月19日

## 🤖 AI引き継ぎ用クイックスタート

新しいAIセッション開始時は、以下のコマンドを実行してください：

bash scripts/ai_handover_complete.sh

### GitHub API利用方法
Python環境で以下を実行：
from github_auto_fetch import GitHubAutoFetch
fetcher = GitHubAutoFetch()

### 重要設定
- GitHubトークン: 自動設定済み
- API権限: プライベートリポジトリアクセス可能

## 🤖 AI引き継ぎ用クイックスタート

新しいAIセッション開始時は、以下のコマンドを実行してください：

bash scripts/ai_handover_complete.sh

### GitHub API利用方法
Python環境で以下を実行：
from github_auto_fetch import GitHubAutoFetch
fetcher = GitHubAutoFetch()

### 重要設定
- GitHubトークン: 自動設定済み
- API権限: プライベートリポジトリアクセス可能

### GitHub API利用方法
Python環境で以下を実行：
from github_auto_fetch import GitHubAutoFetch
fetcher = GitHubAutoFetch()

### 重要設定
- GitHubトークン: 自動設定済み
- API権限: プライベートリポジトリアクセス可能

- Gitフックの動作テストコミット at Fri 30 May 22:48:16 JST 2025
