#!/usr/bin/env python3
"""
HANAZONOシステム データ分析システム v1.0
機械学習用データ準備・分析
"""

import json
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import glob

class DataAnalyzer:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "hanazono_analysis.db"
        self.init_database()
    
    def init_database(self):
        """分析用データベース初期化"""
        self.data_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_data (
                timestamp TEXT PRIMARY KEY,
                datetime TEXT,
                battery_soc INTEGER,
                battery_voltage REAL,
                battery_current REAL,
                pv_power REAL,
                load_power REAL,
                grid_power REAL,
                temperature REAL,
                weather_condition TEXT,
                season TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_existing_data(self):
        """既存JSONデータをデータベースに統合"""
        json_files = glob.glob(str(self.data_dir / "lvyuan_data_*.json"))
        
        conn = sqlite3.connect(self.db_path)
        imported_count = 0
        
        for file_path in json_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list) and len(data) > 0:
                    data = data[0]  # 最初の要素を使用
                
                # データ抽出
                timestamp = data.get('timestamp')
                datetime_str = data.get('datetime')
                parameters = data.get('parameters', {})
                
                # バッテリーデータ抽出
                battery_soc = None
                battery_voltage = None
                battery_current = None
                
                for key, param in parameters.items():
                    if 'SOC' in param.get('name', ''):
                        battery_soc = param.get('value')
                    elif '電圧' in param.get('name', ''):
                        battery_voltage = param.get('value')
                    elif '電流' in param.get('name', ''):
                        battery_current = param.get('value')
                
                # データベースに挿入
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO system_data 
                    (timestamp, datetime, battery_soc, battery_voltage, battery_current)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp, datetime_str, battery_soc, battery_voltage, battery_current))
                
                imported_count += 1
                
            except Exception as e:
                print(f"⚠️ ファイル処理エラー {file_path}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ {imported_count}件のデータをインポートしました")
        return imported_count
    
    def get_daily_summary(self, days=7):
        """日次サマリー取得"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                DATE(datetime) as date,
                AVG(battery_soc) as avg_soc,
                MIN(battery_soc) as min_soc,
                MAX(battery_soc) as max_soc,
                COUNT(*) as data_points
            FROM system_data 
            WHERE datetime > datetime('now', '-{} days')
            GROUP BY DATE(datetime)
            ORDER BY date DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def analyze_performance(self):
        """システム性能分析"""
        conn = sqlite3.connect(self.db_path)
        
        # 基本統計
        stats_query = '''
            SELECT 
                COUNT(*) as total_records,
                AVG(battery_soc) as avg_soc,
                MIN(battery_soc) as min_soc,
                MAX(battery_soc) as max_soc,
                AVG(battery_voltage) as avg_voltage,
                MIN(datetime) as first_record,
                MAX(datetime) as last_record
            FROM system_data
        '''
        
        stats = pd.read_sql_query(stats_query, conn)
        conn.close()
        
        print("📊 システム性能分析結果:")
        print("=" * 50)
        print(f"総レコード数: {stats['total_records'].iloc[0]:,}")
        print(f"平均SOC: {stats['avg_soc'].iloc[0]:.1f}%")
        print(f"最低SOC: {stats['min_soc'].iloc[0]:.1f}%")
        print(f"最高SOC: {stats['max_soc'].iloc[0]:.1f}%")
        print(f"平均電圧: {stats['avg_voltage'].iloc[0]:.1f}V")
        print(f"データ期間: {stats['first_record'].iloc[0]} 〜 {stats['last_record'].iloc[0]}")
        
        return stats

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    
    print("🚀 データ分析システム開始...")
    print("1. 既存データインポート中...")
    imported = analyzer.import_existing_data()
    
    print("2. システム性能分析中...")
    analyzer.analyze_performance()
    
    print("3. 日次サマリー生成中...")
    summary = analyzer.get_daily_summary()
    print(summary)
    
    print("✅ データ分析完了")
