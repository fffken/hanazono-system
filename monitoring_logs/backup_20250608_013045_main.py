import sys
import argparse
import json
import logging
import subprocess

# ロガー設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HANAZONO_SYSTEM")

def main():
    """メイン処理の司令塔"""
    parser = argparse.ArgumentParser(description="HANAZONO自動最適化システム")
    parser.add_argument('--daily-report', action='store_true', help='日次レポートを生成・送信します')
    parser.add_argument('--run-hcqas', action='store_true', help='HCQAS提案生成テストを実行します')
    parser.add_argument('--live', action='store_true', help='実際にメールを送信するライブモードで実行します')
    parser.add_argument('--debug', action='store_true', help='デバッグモードで実行します（メールは送信しない）')
    args = parser.parse_args()

    if args.daily_report:
        logger.info("司令塔: 日次レポート処理を開始します...")
        try:
            # 依存モジュールをここでインポート
            from email_notifier import EnhancedEmailNotifier

            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)

            notifier = EnhancedEmailNotifier(settings)

            # --liveフラグがあれば本番送信、なければテストモード
            success = notifier.send_daily_report({}, test_mode=not args.live)

            if success:
                logger.info("✅ 司令塔: 日次レポート処理、正常完了。")
            else:
                logger.error("❌ 司令塔: 日次レポート処理、失敗。")

        except Exception as e:
            logger.error(f"日次レポートの実行中に致命的なエラー: {e}", exc_info=True)

    elif args.run_hcqas:
        logger.info("司令塔: HCQAS提案機能カプセルを起動します...")
        # カプセルは分離したまま安全に実行
        subprocess.run([sys.executable, 'hcqas_capsule.py'])
        logger.info("司令塔: HCQAS提案機能カプセルの処理が完了しました。")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
