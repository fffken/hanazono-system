import sys
import logging

# プロジェクトルートをパスに追加
sys.path.append('.') 

def run_collection():
    """データ収集を実行する自己完結型関数"""
    logging.basicConfig(filename='logs/collector_capsule.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    
    try:
        from lvyuan_collector import LVYUANCollector
        logging.info("データ収集カプセル起動。")
        collector = LVYUANCollector()
        data, _ = collector.collect_data()
        if data:
            logging.info(f"データ収集成功: {len(data.get('parameters', []))}パラメーター")
            return True
        else:
            logging.error("データ収集失敗。コレクターからの戻り値がありません。")
            return False
    except ImportError:
        logging.error("lvyuan_collector.pyのインポートに失敗しました。")
        return False
    except Exception as e:
        logging.error(f'データ収集カプセルの実行中にエラー: {e}', exc_info=True)
        return False

if __name__ == "__main__":
    run_collection()
