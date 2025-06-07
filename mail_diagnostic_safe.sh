#!/bin/bash
# HANAZONOシステム - 完全非破壊的メール診断スクリプト
# 作成日: 2025-06-03
# 目的: メール問題の安全診断（設定変更なし）

set -e  # エラー時即座停止

echo "📧 HANAZONOシステム完全非破壊的メール診断開始"
echo "========================================================"
echo "🛡️ 安全保証: 設定変更なし・システム停止なし・完全読み取り専用"
echo ""

# タイムスタンプ
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="mail_diagnostic_report_${TIMESTAMP}.txt"

echo "📅 診断実行時刻: $(date)" | tee ${REPORT_FILE}
echo "🎯 対象システム: $(pwd)" | tee -a ${REPORT_FILE}
echo "" | tee -a ${REPORT_FILE}

# Phase 1: cron設定確認（読み取り専用）
echo "📋 Phase 1: cron設定確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "----------------------------------------" | tee -a ${REPORT_FILE}

echo "🔍 現在のcronジョブ一覧:" | tee -a ${REPORT_FILE}
crontab -l | grep -E "(main.py|email|report)" 2>/dev/null | tee -a ${REPORT_FILE} || echo "⚠️ メール関連cronジョブが見つかりません" | tee -a ${REPORT_FILE}

echo "" | tee -a ${REPORT_FILE}
echo "⏰ cron実行履歴確認:" | tee -a ${REPORT_FILE}
sudo journalctl -u cron --since "3 days ago" | grep -E "(main.py|email|report)" | tail -10 | tee -a ${REPORT_FILE} || echo "⚠️ cron実行履歴が見つかりません" | tee -a ${REPORT_FILE}

# Phase 2: ログファイル確認（読み取り専用）
echo "" | tee -a ${REPORT_FILE}
echo "📊 Phase 2: ログファイル確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "--------------------------------------------" | tee -a ${REPORT_FILE}

echo "📁 ログディレクトリ内容:" | tee -a ${REPORT_FILE}
ls -la logs/ 2>/dev/null | tee -a ${REPORT_FILE} || echo "⚠️ logsディレクトリが見つかりません" | tee -a ${REPORT_FILE}

echo "" | tee -a ${REPORT_FILE}
echo "📧 メール関連ログ（最新10行）:" | tee -a ${REPORT_FILE}
find logs/ -name "*email*" -o -name "*mail*" -o -name "*cron*" 2>/dev/null | head -5 | while read logfile; do
  echo "📄 ${logfile}:" | tee -a ${REPORT_FILE}
  tail -10 "${logfile}" 2>/dev/null | tee -a ${REPORT_FILE} || echo "⚠️ ログ読み取りエラー" | tee -a ${REPORT_FILE}
  echo "" | tee -a ${REPORT_FILE}
done

# Phase 3: 設定ファイル確認（読み取り専用）
echo "⚙️ Phase 3: 設定ファイル確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "--------------------------------------------" | tee -a ${REPORT_FILE}

echo "📧 settings.json メール設定確認:" | tee -a ${REPORT_FILE}
if [ -f "settings.json" ]; then
  echo "✅ settings.json存在確認" | tee -a ${REPORT_FILE}
  python3 -c "
import json
try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    email_config = settings.get('email', {})
    print(f'📧 SMTP設定: {bool(email_config.get(\"smtp_server\"))}')
    print(f'📧 送信者設定: {bool(email_config.get(\"email_sender\"))}')
    print(f'📧 受信者設定: {bool(email_config.get(\"email_recipients\"))}')
    print(f'📧 認証設定: {bool(email_config.get(\"smtp_password\"))}')
    
    # 通知設定も確認
    notification = settings.get('notification', {})
    email_notif = notification.get('email', {})
    print(f'🔔 通知有効: {email_notif.get(\"enabled\", False)}')
except Exception as e:
    print(f'⚠️ 設定読み取りエラー: {e}')
" | tee -a ${REPORT_FILE}
else
  echo "❌ settings.json が見つかりません" | tee -a ${REPORT_FILE}
fi

# Phase 4: 環境変数確認（読み取り専用）
echo "" | tee -a ${REPORT_FILE}
echo "🌍 Phase 4: 環境変数確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "----------------------------------------" | tee -a ${REPORT_FILE}

echo "🔑 SMTP認証環境変数確認:" | tee -a ${REPORT_FILE}
if [ -n "$SMTP_PASSWORD" ]; then
  echo "✅ SMTP_PASSWORD環境変数設定済み" | tee -a ${REPORT_FILE}
else
  echo "⚠️ SMTP_PASSWORD環境変数が設定されていません" | tee -a ${REPORT_FILE}
fi

# Phase 5: プロセス確認（読み取り専用）
echo "" | tee -a ${REPORT_FILE}
echo "🔄 Phase 5: プロセス確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "--------------------------------------" | tee -a ${REPORT_FILE}

echo "🐍 Python関連プロセス:" | tee -a ${REPORT_FILE}
ps aux | grep -E "(main.py|email|python)" | grep -v grep | tee -a ${REPORT_FILE} || echo "⚠️ メール関連プロセスが見つかりません" | tee -a ${REPORT_FILE}

# Phase 6: ネットワーク接続確認（読み取り専用）
echo "" | tee -a ${REPORT_FILE}
echo "🌐 Phase 6: ネットワーク接続確認（読み取り専用）" | tee -a ${REPORT_FILE}
echo "----------------------------------------------" | tee -a ${REPORT_FILE}

echo "📧 SMTP接続テスト（Gmail）:" | tee -a ${REPORT_FILE}
timeout 5 python3 -c "
import socket
try:
    sock = socket.create_connection(('smtp.gmail.com', 587), timeout=3)
    sock.close()
    print('✅ Gmail SMTP接続成功')
except Exception as e:
    print(f'❌ Gmail SMTP接続エラー: {e}')
" | tee -a ${REPORT_FILE}

# Phase 7: 最近のメール送信履歴確認
echo "" | tee -a ${REPORT_FILE}
echo "📮 Phase 7: 最近のメール送信履歴確認" | tee -a ${REPORT_FILE}
echo "------------------------------------" | tee -a ${REPORT_FILE}

echo "📅 過去3日間のメール関連ログ検索:" | tee -a ${REPORT_FILE}
find . -name "*.log" -o -name "*.txt" 2>/dev/null | xargs grep -l -i "mail\|email\|smtp" 2>/dev/null | head -5 | while read logfile; do
  echo "📄 ${logfile} の最近のメール関連エントリ:" | tee -a ${REPORT_FILE}
  grep -i "mail\|email\|smtp" "${logfile}" 2>/dev/null | tail -5 | tee -a ${REPORT_FILE}
  echo "" | tee -a ${REPORT_FILE}
done

# 診断完了レポート
echo "" | tee -a ${REPORT_FILE}
echo "🎊 診断完了レポート" | tee -a ${REPORT_FILE}
echo "==================" | tee -a ${REPORT_FILE}
echo "📄 診断レポート保存先: ${REPORT_FILE}" | tee -a ${REPORT_FILE}
echo "🛡️ 実行内容: 完全読み取り専用・設定変更なし" | tee -a ${REPORT_FILE}
echo "📅 診断完了時刻: $(date)" | tee -a ${REPORT_FILE}
echo "" | tee -a ${REPORT_FILE}
echo "🎯 次のステップ推奨:" | tee -a ${REPORT_FILE}
echo "1. 診断結果レビュー" | tee -a ${REPORT_FILE}
echo "2. 問題特定" | tee -a ${REPORT_FILE}
echo "3. 安全修復案の提示" | tee -a ${REPORT_FILE}
echo "4. 修復実行（事前確認後）" | tee -a ${REPORT_FILE}

echo ""
echo "✅ 非破壊的診断完了！レポートを確認してください："
echo "   cat ${REPORT_FILE}"
echo ""
echo "📋 診断結果に基づいて、安全な修復方法を提案いたします。"
