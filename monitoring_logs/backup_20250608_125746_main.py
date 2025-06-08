import argparse
import logging
import sys

# プロジェクトルートをパスに追加
sys.path.append('.') 

def main():
    """
    HANAZONOシステムの主要な機能（日次レポート）を呼び出す司令塔。
    """
    # ロガー設定
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("HANAZONO_MAIN")

    parser = argparse.ArgumentParser(description="HANAZONOシステム 司令塔")
    parser.add_argument('--daily-report', action='store_true', help='日次レポート機能を実行します')
    parser.add_argument('--debug', action='store_true', help='デバッグモード。メールを送信せず内容をコンソールに表示します')
    args = parser.parse_args()

    if not args.daily_report:
        parser.print_help()
        sys.exit(0)

    # --- 日次レポート機能の実行 ---
    if args.daily_report:
        logger.info("日次レポート処理を開始します...")
        try:
            # 必要なモジュールをここでインポート
            from config import settings
            from email_notifier import EnhancedEmailNotifier

            # クラスを初期化し、設定オブジェクトを渡す
            notifier = EnhancedEmailNotifier(settings_object=settings, logger=logger)
            
            # メソッドを実行。--debugフラグの有無でtest_modeを制御
            success = notifier.send_daily_report(test_mode=args.debug)
            
            if success:
                logger.info("✅ 日次レポート処理、正常完了。")
            else:
                logger.error("❌ 日次レポート処理、失敗。")

        except Exception as e:
            logger.error(f"日次レポートの実行中に致命的なエラーが発生しました。", exc_info=True)


if __name__ == "__main__":
    main()
