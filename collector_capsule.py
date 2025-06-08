#!/usr/bin/env python3
"""
Collector Capsule Recreation Script
目的: 欠損したcollector_capsule.pyを緊急復旧
機能: lvyuan_collector.pyの統合管理・エラーハンドリング
"""

import sys
import os
import logging
import json
from datetime import datetime

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/lvyuan_solar_control/logs/collector_capsule.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CollectorCapsule:
    """データ収集統合管理カプセル"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def collect_lvyuan_data(self):
        """LVYUANインバーターデータ収集"""
        try:
            # lvyuan_collector.pyのインポートと実行
            sys.path.append(self.base_dir)
            
            # 動的インポート
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "lvyuan_collector", 
                os.path.join(self.base_dir, "lvyuan_collector.py")
            )
            lvyuan_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lvyuan_module)
            
            # LVYUANCollectorの実行
            collector = lvyuan_module.LVYUANCollector()
            data = collector.collect_data()
            
            logger.info("LVYUANデータ収集成功")
            return data
            
        except ImportError as e:
            logger.error(f"lvyuan_collector.pyのインポートに失敗しました: {e}")
            return None
        except Exception as e:
            logger.error(f"LVYUANデータ収集中にエラー: {e}")
            return None
    
    def save_collected_data(self, data):
        """収集データの保存"""
        if data is None:
            logger.warning("保存するデータがありません")
            return False
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"collected_data_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"データ保存成功: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"データ保存中にエラー: {e}")
            return False
    
    def run_collection_cycle(self):
        """データ収集サイクル実行"""
        logger.info("データ収集サイクル開始")
        
        try:
            # LVYUANデータ収集
            lvyuan_data = self.collect_lvyuan_data()
            
            if lvyuan_data:
                # データ保存
                self.save_collected_data(lvyuan_data)
                logger.info("データ収集サイクル完了")
                return True
            else:
                logger.warning("データ収集に失敗しました")
                return False
                
        except Exception as e:
            logger.error(f"収集サイクル中にエラー: {e}")
            return False

def main():
    """メイン実行関数"""
    logger.info("Collector Capsule 開始")
    
    try:
        capsule = CollectorCapsule()
        success = capsule.run_collection_cycle()
        
        if success:
            logger.info("Collector Capsule 正常終了")
            print("✅ データ収集完了")
        else:
            logger.warning("Collector Capsule 警告終了")
            print("⚠️ データ収集に問題がありました")
            
    except Exception as e:
        logger.error(f"Collector Capsule 実行中にエラー: {e}")
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
