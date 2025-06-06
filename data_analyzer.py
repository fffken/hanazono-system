#!/usr/bin/env python3
"""
HANAZONOシステム データ分析システム v1.1（エラー耐性強化版）
機械学習用データ準備・分析
"""

import json
import pandas as pd
import sqlite3
import os
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
                season TEXT,
                file_source TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_file_structure(self, file_path):
        """ファイル構造を分析してエラーの原因を特定"""
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
            
            if not content:
                return "empty_file"
            
            data = json.loads(content)
            
            if data is None:
                return "null_content"
            elif isinstance(data, list):
                if len(data) == 0:
                    return "empty_list"
                elif data[0] is None:
                    return "null_first_element"
                else:
                    return "valid_list"
            elif isinstance(data, dict):
                return "valid_dict"
            else:
                return "unknown_structure"
                
        except json.JSONDecodeError:
            return "invalid_json"
        except Exception as e:
            return f"error_{type(e).__name__}"
    
    def import_existing_data(self, analyze_errors=True):
        """既存JSONデータをデータベースに統合（エラー分析付き）"""
        json_files = glob.glob(str(self.data_dir / "lvyuan_data_*.json"))
        
        conn = sqlite3.connect(self.db_path)
        imported_count = 0
        error_stats = {}
        
        print(f"📁 {len(json_files)}件のファイルを処理中...")
        
        for file_path in json_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                
                if not content:
                    if analyze_errors:
                        error_stats["empty_file"] = error_stats.get("empty_file", 0) + 1
                    continue
                
                data = json.loads(content)
                
                if data is None:
                    if analyze_errors:
                        error_stats["null_content"] = error_stats.get("null_content", 0) + 1
                    continue
                
                # リスト形式の場合
                if isinstance(data, list):
                    if len(data) == 0:
                        if analyze_errors:
                            error_stats["empty_list"] = error_stats.get("empty_list", 0) + 1
                        continue
                    data = data[0]
                
                # データがNoneの場合
                if data is None:
                    if analyze_errors:
                        error_stats["null_data_element"] = error_stats.get("null_data_element", 0) + 1
                    continue
                
                # データ抽出
                timestamp = data.get('timestamp')
                datetime_str = data.get('datetime')
                parameters = data.get('parameters', {})
                
                if not parameters:
                    if analyze_errors:
                        error_stats["no_parameters"] = error_stats.get("no_parameters", 0) + 1
                    continue
                
                # バッテリーデータ抽出
                battery_soc = None
                battery_voltage = None
                battery_current = None
                
                for key, param in parameters.items():
                    if param and isinstance(param, dict):
                        name = param.get('name', '')
                        if 'SOC' in name:
                            battery_soc = param.get('value')
                        elif '電圧' in name:
                            battery_voltage = param.get('value')
                        elif '電流' in name:
                            battery_current = param.get('value')
                
                # データベースに挿入
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO system_data 
                    (timestamp, datetime, battery_soc, battery_voltage, battery_current, file_source)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (timestamp, datetime_str, battery_soc, battery_voltage, battery_current, 
                      os.path.basename(file_path)))
                
                imported_count += 1
                
            except Exception as e:
                error_type = type(e).__name__
                if analyze_errors:
                    error_stats[f"exception_{error_type}"] = error_stats.get(f"exception_{error_type}", 0) + 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ {imported_count}件のデータをインポートしました")
        
        if analyze_errors and error_stats:
            print("\n📋 エラー分析結果:")
            print("=" * 40)
            for error_type, count in sorted(error_stats.items()):
                print(f"{error_type}: {count}件")
        
        return imported_count, error_stats
    
    def get_daily_summary(self, days=7):
        """日次サマリー取得"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                DATE(datetime) as date,
                AVG(battery_soc) as avg_soc,
                MIN(battery_soc) as min_soc,
                MAX(battery_soc) as max_soc,
                AVG(battery_voltage) as avg_voltage,
                COUNT(*) as data_points
            FROM system_data 
            WHERE datetime > datetime('now', '-{} days')
            AND battery_soc IS NOT NULL
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
                COUNT(CASE WHEN battery_soc IS NOT NULL THEN 1 END) as valid_soc_records,
                AVG(battery_soc) as avg_soc,
                MIN(battery_soc) as min_soc,
                MAX(battery_soc) as max_soc,
                AVG(battery_voltage) as avg_voltage,
                MIN(datetime) as first_record,
                MAX(datetime) as last_record
            FROM system_data
            WHERE battery_soc IS NOT NULL
        '''
        
        stats = pd.read_sql_query(stats_query, conn)
        
        # データ品質分析
        quality_query = '''
            SELECT 
                COUNT(*) as total_records,
                COUNT(CASE WHEN battery_soc IS NULL THEN 1 END) as missing_soc,
                COUNT(CASE WHEN battery_voltage IS NULL THEN 1 END) as missing_voltage,
                COUNT(CASE WHEN battery_current IS NULL THEN 1 END) as missing_current
            FROM system_data
        '''
        
        quality = pd.read_sql_query(quality_query, conn)
        conn.close()
        
        print("📊 システム性能分析結果:")
        print("=" * 50)
        print(f"総レコード数: {quality['total_records'].iloc[0]:,}")
        print(f"有効SOCレコード: {stats['valid_soc_records'].iloc[0]:,}")
        print(f"平均SOC: {stats['avg_soc'].iloc[0]:.1f}%")
        print(f"最低SOC: {stats['min_soc'].iloc[0]:.1f}%")
        print(f"最高SOC: {stats['max_soc'].iloc[0]:.1f}%")
        print(f"平均電圧: {stats['avg_voltage'].iloc[0]:.1f}V")
        print(f"データ期間: {stats['first_record'].iloc[0]} 〜 {stats['last_record'].iloc[0]}")
        
        print("\n📊 データ品質分析:")
        print("=" * 50)
        total = quality['total_records'].iloc[0]
        missing_soc = quality['missing_soc'].iloc[0]
        missing_voltage = quality['missing_voltage'].iloc[0]
        missing_current = quality['missing_current'].iloc[0]
        
        print(f"SOC欠損率: {(missing_soc/total*100):.1f}% ({missing_soc}件)")
        print(f"電圧欠損率: {(missing_voltage/total*100):.1f}% ({missing_voltage}件)")
        print(f"電流欠損率: {(missing_current/total*100):.1f}% ({missing_current}件)")
        
        return stats, quality
    
    def get_hourly_pattern(self):
        """時間別SOCパターン分析"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                strftime('%H', datetime) as hour,
                AVG(battery_soc) as avg_soc,
                COUNT(*) as data_points
            FROM system_data 
            WHERE battery_soc IS NOT NULL
            GROUP BY strftime('%H', datetime)
            ORDER BY hour
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print("\n⏰ 時間別SOCパターン:")
        print("=" * 30)
        for _, row in df.iterrows():
            hour = int(row['hour'])
            avg_soc = row['avg_soc']
            points = row['data_points']
            print(f"{hour:02d}時: {avg_soc:.1f}% ({points}件)")
        
        return df

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    
    print("🚀 改良版データ分析システム開始...")
    print("1. 既存データインポート中（エラー分析付き）...")
    imported, errors = analyzer.import_existing_data()
    
    print("\n2. システム性能分析中...")
    stats, quality = analyzer.analyze_performance()
    
    print("\n3. 日次サマリー生成中...")
    summary = analyzer.get_daily_summary()
    print(summary.to_string(index=False))
    
    print("\n4. 時間別パターン分析中...")
    hourly = analyzer.get_hourly_pattern()
    
    print("\n✅ 改良版データ分析完了")
    print(f"🎯 機械学習用データ準備完了: {imported}件の有効データ")
