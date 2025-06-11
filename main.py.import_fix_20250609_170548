import sys
import argparse
import json
import logging

# プロジェクトルートをパスに追加
sys.path.append('.') 

# 修正：ここで必要なモジュールをインポートする
try:
    from email_notifier import EnhancedEmailNotifier
except ImportError as e:
    print(f"FATAL: email_notifier.py の読み込みに失敗しました。循環参照または依存関係の問題の可能性があります: {e}")
    sys.exit(1)
try:
    from config import get_settings
except ImportError as e:
    print(f"FATAL: config.py の読み込みに失敗しました: {e}")
    sys.exit(1)


def main():
    """
    HANAZONOシステムの主要な機能（日次レポート）を呼び出す司令塔。
    """
    # ロガー設定
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("HANAZONO_MAIN")

    parser = argparse.ArgumentParser(description="HANAZONOシステム 司令塔")
    parser.add_argument('--daily-report', action='store_true', help='日次レポート機能を実行します')
    parser.add_argument('--live', action='store_true', help='実際にメールを送信するライブモードで実行します')
    parser.add_argument('--debug', action='store_true', help='デバッグ情報を追加表示します')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("デバッグモードで実行中")

    if not args.daily_report:
        parser.print_help()
        sys.exit(0)

    # --- 日次レポート機能の実行 ---
    logger.info(f"司令塔: 日次レポート処理を開始します...(ライブモード: {args.live})")
    try:
        # 1. 設定司令塔から設定を取得
        settings = get_settings()
        
        # 2. 設定をメール担当に手渡しして初期化
        notifier = EnhancedEmailNotifier(config=settings['notification']['email'], logger=logger)
        
        # 3. レポート送信を指示。--liveがなければテストモード
        # データ収集
        from collector_capsule import CollectorCapsule
        collector = CollectorCapsule()
        data = collector.collect_lvyuan_data()
        
        # メール送信
        success = notifier.send_daily_report(data, test_mode=False)  # 実データモード強制
        
        if success:
            logger.info("✅ 司令塔: 日次レポート処理、正常完了。")
        else:
            logger.error("❌ 司令塔: 日次レポート処理、失敗。")

    except Exception as e:
        logger.error(f"日次レポートの実行中に致命的なエラーが発生しました。", exc_info=True)


if __name__ == "__main__":
    main()
