#!/bin/bash
echo "=== GitHub設定自動セットアップ ==="
source ~/.bashrc
if [ -z "$GITHUB_TOKEN" ]; then
    source .github_config
    export GITHUB_TOKEN
    echo "✅ GitHubトークン設定完了"
else
    echo "✅ GitHubトークン既に設定済み"
fi
echo "リポジトリ: $GITHUB_REPO"
echo "APIベース: $GITHUB_API_BASE"
