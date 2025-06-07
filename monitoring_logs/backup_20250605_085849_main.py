#!/usr/bin/env python3
"""
HANAZONOシステム自動最適化メインプログラム - 強化版
完全構文エラーフリー設計
"""
import os
import sys
import json
import logging
import time
import argparse
from datetime import datetime, timedelta

# グローバルロガーインスタンス
_hanazono_logger_instance = None

def setup_logger():
    """ロガー設定"""
    logger = logging.getLogger('hanazono_main')
    logger.setLevel(logging.INFO)
    
    # ハンドラーが既に存在する場合は追加しない
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def collect_data():
    """データ収集機能"""
    logger = _hanazono_logger_instance
    logger.info("データ収集を開始します")
    
    try:
        from lvyuan_collector import LVYUANCollector
        collector = LVYUANCollector()
        data, ip_changed = collector.collect_data()
        
        if data:
            logger.info("データ収集が成功しました")
            if ip_changed:
                logger.info("インバーターIPアドレスが変更されました")
            return True
        else:
            logger.error("データ収集に失敗しました")
            return False
            
    except ImportError:
        logger.warning("lvyuan_collector import失敗")
        return False
    except Exception as e:
        logger.error(f"データ収集エラー: {e}")
        return False

def daily_report():
    """日次レポート機能（実装版）"""
    logger = _hanazono_logger_instance
    logger.info("日次レポート送信開始")
    
    try:
        from email_notifier import EnhancedEmailNotifier
        import json
        from datetime import datetime
        
        # 設定読み込み
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        email_config = settings.get('email', {})
        
        # メール送信
        notifier = EnhancedEmailNotifier(email_config)
        report_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_status': 'operational'
        }
        
        result = notifier.send_daily_report(report_data, test_mode=False)
        
        if result:
            logger.info("✅ 日次レポート送信成功")
            return True
        else:
            logger.error("❌ 日次レポート送信失敗")
            return False
            
    except Exception as e:
        logger.error(f"❌ 日次レポートエラー: {e}")
        return False

def check_cron():
    """cron設定確認"""
    logger = _hanazono_logger_instance
    logger.info("cron設定確認機能")
    
    try:
        import subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("cron設定が確認できました")
            print("現在のcron設定:")
            print(result.stdout)
        else:
            logger.warning("cron設定の確認に失敗しました")
            print("cron設定が見つかりません")
    except Exception as e:
        logger.error(f"cron確認エラー: {e}")

def main():
    """メイン処理"""
    global _hanazono_logger_instance
    _hanazono_logger_instance = setup_logger()
    logger = _hanazono_logger_instance
    
    logger.info("HANAZONOシステム自動最適化を開始します")
    
    parser = argparse.ArgumentParser(description="HANAZONO自動最適化システム")
    parser.add_argument('--collect', action='store_true', help='データを収集します')
    parser.add_argument('--daily-report', action='store_true', help='日次レポートを生成します')
    parser.add_argument('--check-cron', action='store_true', help='cron設定を確認します')
    parser.add_argument('--debug', action='store_true', help='デバッグモードで実行します')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("デバッグモードで実行中")
    
    try:
        if args.collect:
            success = collect_data()
            if success:
                logger.info("データ収集処理が正常に完了しました")
            else:
                logger.error("データ収集処理が失敗しました")
        elif args.daily_report:
            success = daily_report()
            if success:
                logger.info("日次レポート処理が正常に完了しました")
            else:
                logger.error("日次レポート処理が失敗しました")
        elif args.check_cron:
            check_cron()
        else:
            logger.info("システム状況を確認中...")
            
            # 基本的な動作確認
            logger.info("設定ファイルを確認中...")
            if os.path.exists('settings.json'):
                logger.info("✅ settings.json: 存在")
            else:
                logger.warning("⚠️ settings.json: 見つかりません")
            
            logger.info("システム初期化完了")
            print("使用方法:")
            print("  python3 main.py --collect       # データ収集")
            print("  python3 main.py --daily-report  # 日次レポート送信")
            print("  python3 main.py --check-cron    # cron設定確認")
            print("  python3 main.py --debug         # デバッグモード")
    
    except KeyboardInterrupt:
        logger.info("ユーザーによって処理が中断されました")
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
