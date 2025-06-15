#!/usr/bin/env python3
"""
HANAZONO 6年間電力データ統合システム v1.0
2018-2024年の実電力データをシステムに統合してML学習可能にする
"""

import os
import csv
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

class DataIntegrationSystem:
    """6年間データ統合システム"""
    
    def __init__(self):
        self.version = "1.0.0-DATA-INTEGRATION"
        self.db_path = "data/hanazono_master_data.db"
        self.csv_files = []
        self.integrated_records = 0
        
    def integrate_all_data(self):
        """全データ統合メイン機能"""
        print("🚀 HANAZONO 6年間データ統合開始")
        print("=" * 60)
        
        # 1. CSVファイル検出
        self._detect_csv_files()
        
        # 2. データベース初期化
        self._initialize_master_database()
        
        # 3. 月次データ統合
        self._integrate_monthly_data()
        
        # 4. 日次データ統合
        self._integrate_daily_data()
        
        # 5. データ品質確認
        self._validate_integrated_data()
        
        # 6. ML学習用データ準備
        self._prepare_ml_dataset()
        
        print(f"\n🎯 統合完了: {self.integrated_records}レコード")
        return True
    
    def _detect_csv_files(self):
        """CSVファイル自動検出"""
        print("\n📁 6年間電力データCSVファイル検出:")
        
        # 想定されるファイルパターン
        patterns = [
            "tsukibetsuShiyoryo_*.txt",  # 月次データ
            "hibetsuShiyoryo_*.txt"      # 日次データ
        ]
        
        detected_files = []
        for pattern in patterns:
            import glob
            files = glob.glob(pattern)
            detected_files.extend(files)
        
        if detected_files:
            print(f"✅ 検出されたCSVファイル: {len(detected_files)}件")
            for file in detected_files:
                print(f"   📄 {file}")
                self.csv_files.append(file)
        else:
            print("⚠️ CSVファイルが見つかりません")
            print("📝 手動でファイルパスを確認してください:")
            print("   - tsukibetsuShiyoryo_*.txt")
            print("   - hibetsuShiyoryo_*.txt")
        
        return len(detected_files) > 0
    
    def _initialize_master_database(self):
        """マスターデータベース初期化"""
        print("\n🗄️ マスターデータベース初期化:")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 月次データテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_power_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                month INTEGER,
                usage_days INTEGER,
                total_kwh REAL,
                daytime_kwh REAL,
                nighttime_kwh REAL,
                summer_daytime_kwh REAL,
                cost_yen INTEGER,
                avg_max_temp REAL,
                avg_min_temp REAL,
                co2_kg REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 日次データテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_power_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                day_of_week TEXT,
                usage_kwh REAL,
                weather TEXT,
                sunshine_hours REAL,
                max_temp REAL,
                min_temp REAL,
                season TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ML学習用統合テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ml_training_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                usage_kwh REAL,
                weather_category TEXT,
                sunshine_hours REAL,
                temperature_avg REAL,
                season TEXT,
                month INTEGER,
                day_of_week INTEGER,
                is_weekend INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ マスターデータベース初期化完了")
    
    def _integrate_monthly_data(self):
        """月次データ統合"""
        print("\n📊 月次データ統合:")
        
        monthly_files = [f for f in self.csv_files if 'tsukibetsu' in f]
        
        if not monthly_files:
            print("⚠️ 月次データファイルが見つかりません")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        monthly_records = 0
        
        for file in monthly_files:
            print(f"📄 処理中: {file}")
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    
                    # ヘッダー検出
                    headers = []
                    data_started = False
                    
                    for row in reader:
                        if not data_started and len(row) > 0 and '月分' in row[0]:
                            headers = row
                            data_started = True
                            continue
                        
                        if data_started and len(row) >= 10:
                            try:
                                # データ解析
                                month_str = row[0]  # "2024年04月分"
                                year_month = self._parse_month_string(month_str)
                                
                                if year_month:
                                    year, month = year_month
                                    usage_days = int(row[4]) if row[4] else 0
                                    total_kwh = float(row[6]) if row[6] else 0
                                    cost_yen = int(row[10]) if row[10] else 0
                                    
                                    # 昼間・夜間の処理（データ構造により異なる）
                                    daytime_kwh = 0
                                    nighttime_kwh = 0
                                    summer_daytime_kwh = 0
                                    
                                    if len(row) > 7 and row[7]:
                                        if '昼間夏季' in str(headers):
                                            summer_daytime_kwh = float(row[7])
                                        else:
                                            daytime_kwh = float(row[7])
                                    
                                    if len(row) > 8 and row[8]:
                                        if '昼間その他季' in str(headers):
                                            daytime_kwh = float(row[8])
                                    
                                    if len(row) > 9 and row[9]:
                                        nighttime_kwh = float(row[9])
                                    
                                    # 気温データ
                                    avg_max_temp = float(row[12]) if len(row) > 12 and row[12] else 0
                                    avg_min_temp = float(row[13]) if len(row) > 13 and row[13] else 0
                                    co2_kg = float(row[14]) if len(row) > 14 and row[14] else 0
                                    
                                    # データベース挿入
                                    cursor.execute('''
                                        INSERT OR REPLACE INTO monthly_power_data 
                                        (year, month, usage_days, total_kwh, daytime_kwh, nighttime_kwh, 
                                         summer_daytime_kwh, cost_yen, avg_max_temp, avg_min_temp, co2_kg)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (year, month, usage_days, total_kwh, daytime_kwh, nighttime_kwh,
                                          summer_daytime_kwh, cost_yen, avg_max_temp, avg_min_temp, co2_kg))
                                    
                                    monthly_records += 1
                                    
                            except Exception as e:
                                print(f"⚠️ 行処理エラー: {e}")
                                continue
                
            except Exception as e:
                print(f"❌ ファイル処理エラー {file}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ 月次データ統合完了: {monthly_records}レコード")
        self.integrated_records += monthly_records
    
    def _integrate_daily_data(self):
        """日次データ統合"""
        print("\n📅 日次データ統合:")
        
        daily_files = [f for f in self.csv_files if 'hibetsu' in f]
        
        if not daily_files:
            print("⚠️ 日次データファイルが見つかりません")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        daily_records = 0
        
        for file in daily_files:
            print(f"📄 処理中: {file}")
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    
                    # ヘッダー検出
                    data_started = False
                    
                    for row in reader:
                        if not data_started and len(row) > 0 and '日付' in row[0]:
                            data_started = True
                            continue
                        
                        if data_started and len(row) >= 7:
                            try:
                                date_str = row[0]  # "2023/04/24"
                                day_of_week = row[1]
                                usage_kwh = float(row[2]) if row[2] else 0
                                weather = row[3] if row[3] else ""
                                sunshine_hours = float(row[4]) if row[4] else 0
                                max_temp = float(row[5]) if row[5] else 0
                                min_temp = float(row[6]) if row[6] else 0
                                
                                # 日付正規化
                                if date_str and usage_kwh > 0:
                                    normalized_date = self._normalize_date(date_str)
                                    season = self._determine_season(normalized_date)
                                    
                                    cursor.execute('''
                                        INSERT OR REPLACE INTO daily_power_data 
                                        (date, day_of_week, usage_kwh, weather, sunshine_hours, 
                                         max_temp, min_temp, season)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (normalized_date, day_of_week, usage_kwh, weather, 
                                          sunshine_hours, max_temp, min_temp, season))
                                    
                                    daily_records += 1
                                    
                            except Exception as e:
                                print(f"⚠️ 行処理エラー: {e}")
                                continue
                
            except Exception as e:
                print(f"❌ ファイル処理エラー {file}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ 日次データ統合完了: {daily_records}レコード")
        self.integrated_records += daily_records
    
    def _prepare_ml_dataset(self):
        """ML学習用データセット準備"""
        print("\n🤖 ML学習用データセット準備:")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 日次データをML用に変換
        cursor.execute('''
            INSERT OR REPLACE INTO ml_training_data 
            (date, usage_kwh, weather_category, sunshine_hours, temperature_avg, 
             season, month, day_of_week, is_weekend)
            SELECT 
                date,
                usage_kwh,
                CASE 
                    WHEN weather LIKE '%晴%' OR weather LIKE '%快晴%' THEN 'sunny'
                    WHEN weather LIKE '%曇%' THEN 'cloudy'
                    WHEN weather LIKE '%雨%' OR weather LIKE '%雷%' THEN 'rainy'
                    ELSE 'other'
                END as weather_category,
                sunshine_hours,
                (max_temp + min_temp) / 2.0 as temperature_avg,
                season,
                CAST(strftime('%m', date) AS INTEGER) as month,
                CASE day_of_week
                    WHEN '月' THEN 1 WHEN '火' THEN 2 WHEN '水' THEN 3 
                    WHEN '木' THEN 4 WHEN '金' THEN 5 WHEN '土' THEN 6 WHEN '日' THEN 0
                    ELSE 0
                END as day_of_week,
                CASE day_of_week
                    WHEN '土' THEN 1 WHEN '日' THEN 1 ELSE 0
                END as is_weekend
            FROM daily_power_data 
            WHERE usage_kwh > 0
        ''')
        
        conn.commit()
        
        # データ統計確認
        cursor.execute('SELECT COUNT(*) FROM ml_training_data')
        ml_records = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ ML学習データセット準備完了: {ml_records}レコード")
    
    def _parse_month_string(self, month_str):
        """月文字列解析"""
        # "2024年04月分" → (2024, 4)
        import re
        match = re.search(r'(\d{4})年(\d{1,2})月', month_str)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None
    
    def _normalize_date(self, date_str):
        """日付正規化"""
        # "2023/04/24" → "2023-04-24"
        try:
            parts = date_str.split('/')
            if len(parts) == 3:
                year, month, day = parts
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        except:
            pass
        return date_str
    
    def _determine_season(self, date_str):
        """季節判定"""
        try:
            month = int(date_str.split('-')[1])
            if month in [12, 1, 2]:
                return 'winter'
            elif month in [3, 4, 5]:
                return 'spring'
            elif month in [6, 7, 8]:
                return 'summer'
            else:
                return 'autumn'
        except:
            return 'unknown'
    
    def _validate_integrated_data(self):
        """統合データ検証"""
        print("\n🔍 統合データ検証:")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 月次データ確認
        cursor.execute('SELECT COUNT(*), MIN(year), MAX(year) FROM monthly_power_data')
        monthly_stats = cursor.fetchone()
        print(f"📊 月次データ: {monthly_stats[0]}レコード ({monthly_stats[1]}-{monthly_stats[2]}年)")
        
        # 日次データ確認
        cursor.execute('SELECT COUNT(*), MIN(date), MAX(date) FROM daily_power_data')
        daily_stats = cursor.fetchone()
        print(f"📅 日次データ: {daily_stats[0]}レコード ({daily_stats[1]} ～ {daily_stats[2]})")
        
        # ML学習データ確認
        cursor.execute('SELECT COUNT(*) FROM ml_training_data')
        ml_count = cursor.fetchone()[0]
        print(f"🤖 ML学習データ: {ml_count}レコード")
        
        conn.close()


def main():
    """データ統合実行"""
    integrator = DataIntegrationSystem()
    success = integrator.integrate_all_data()
    
    if success:
        print("\n🎉 6年間電力データ統合完了！")
        print("✅ HANAZONOシステムでML機能が使用可能になりました")
    else:
        print("\n❌ データ統合に問題が発生しました")
    
    return success

if __name__ == "__main__":
    main()
