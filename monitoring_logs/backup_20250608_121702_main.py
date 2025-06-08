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
    # --debug フラグを --live との排他関係ではなく、単独のデバッグ情報表示フラグとして再定義
    parser.add_argument('--debug', action='store_true', help='デバッグ情報を追加表示します')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("デバッグモードで実行中")

    if args.daily_report:
        logger.info(f"司令塔: 日次レポート処理を開始します...(ライブモード: {args.live})")
        try:
            from email_notifier import EnhancedEmailNotifier
            
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)

            notifier = EnhancedEmailNotifier(settings, logger=logger)
            
            # --liveフラグがあれば本番送信、なければテストモード(ドライラン)
            success = notifier.send_daily_report({}, test_mode=not args.live)
            
            if success:
                logger.info("✅ 司令塔: 日次レポート処理、正常完了。")
            else:
                logger.error("❌ 司令塔: 日次レポート処理、失敗。")

        except Exception as e:
            logger.error(f"日次レポートの実行中に致命的なエラー: {e}", exc_info=True)

    elif args.run_hcqas:
        logger.info("司令塔: HCQAS提案機能カプセルを起動します...")
        subprocess.run([sys.executable, 'hcqas_capsule.py'])
        logger.info("司令塔: HCQAS提案機能カプセルの処理が完了しました。")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
