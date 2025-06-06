#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム 6年分データ統合分析システム v1.0
2018年〜2024年の電力使用データを統合分析

データソース:
- 月別詳細: 2018年5月〜2022年4月 (4年分)
- 日別詳細: 2022年5月〜2024年4月 (2年分)
- 実績データ: 2024年6月〜2025年5月 (PDF)
"""

import pandas as pd
import numpy as np
import sqlite3
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class ComprehensiveDataIntegrator:
    """6年分電力データ統合分析システム"""
    
    def __init__(self, db_path="data/comprehensive_electric_data.db"):
        self.db_path = db_path
        self.logger = self.setup_logger()
        self.init_database()
        
        # データ期間定義
        self.data_periods = {
            "monthly_detail": {
                "period": "2018-05 to 2022-04",
                "description": "月別詳細データ（昼夜分離・電気料金含む）",
                "sources": [
                    "tsukibetsuShiyoryo_201805-201904.txt",
                    "tsukibetsuShiyoryo_201905-202004.txt", 
                    "tsukibetsuShiyoryo_202005-202104.txt",
                    "tsukibetsuShiyoryo_202105-202204.txt"
                ]
            },
            "daily_detail": {
                "period": "2022-05 to 2024-04", 
                "description": "日別詳細データ（天気・気温・日照時間含む）",
                "sources": [
                    "hibetsuShiyoryo_202205-202304.txt",
                    "hibetsuShiyoryo_202305-202404.txt"
                ]
            },
            "hanazono_effect": {
                "period": "2024-06 to 2025-05",
                "description": "HANAZONOシステム効果期間",
                "sources": ["PDF月別電気料金表"]
            }
        }
    
    def setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('ComprehensiveDataIntegrator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('logs/comprehensive_data_integration.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def init_database(self):
        """統合データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 統合月次データテーブル
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comprehensive_monthly (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    usage_kwh REAL NOT NULL,
                    cost_yen INTEGER,
                    daytime_kwh REAL,
                    nighttime_kwh REAL,
                    avg_temp_high REAL,
                    avg_temp_low REAL,
                    co2_kg REAL,
                    data_source TEXT NOT NULL,
                    phase TEXT NOT NULL, -- baseline, covid, price_hike, pre_hanazono, hanazono
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(year, month)
                )
            ''')
            
            # 統合日次データテーブル  
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comprehensive_daily (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    weekday TEXT NOT NULL,
                    usage_kwh REAL NOT NULL,
                    weather TEXT,
                    sunshine_hours REAL,
                    temp_high REAL,
                    temp_low REAL,
                    data_source TEXT NOT NULL,
                    phase TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 進化フェーズ定義テーブル
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS evolution_phases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phase_name TEXT NOT NULL UNIQUE,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    key_events TEXT -- JSON format
                )
            ''')
            
            conn.commit()
        
        self.logger.info("統合データベース初期化完了")
    
    def register_evolution_phases(self):
        """進化フェーズの登録"""
        phases = [
            {
                "phase_name": "baseline",
                "start_date": "2018-05-01",
                "end_date": "2019-12-31", 
                "description": "ベースライン期（コロナ前の通常生活）",
                "key_events": json.dumps(["通常の電力消費パターン確立", "季節変動の基準値設定"])
            },
            {
                "phase_name": "covid",
                "start_date": "2020-01-01",
                "end_date": "2021-12-31",
                "description": "コロナ影響期（在宅勤務・行動制限）", 
                "key_events": json.dumps(["緊急事態宣言", "在宅勤務増加", "外出自粛"])
            },
            {
                "phase_name": "price_hike", 
                "start_date": "2022-01-01",
                "end_date": "2024-07-31",
                "description": "電気料金高騰対応期",
                "key_events": json.dumps(["電気料金高騰", "節電意識向上", "ウクライナ情勢影響"])
            },
            {
                "phase_name": "pre_hanazono",
                "start_date": "2024-06-01", 
                "end_date": "2024-08-24",
                "description": "HANAZONOシステム導入準備期",
                "key_events": json.dumps(["システム導入検討", "設備準備"])
            },
            {
                "phase_name": "hanazono",
                "start_date": "2024-08-25",
                "end_date": "2025-12-31",
                "description": "HANAZONOシステム効果期",
                "key_events": json.dumps(["ソーラー+蓄電池導入", "自動最適化開始", "劇的削減効果"])
            }
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for phase in phases:
                cursor.execute('''
                    INSERT OR REPLACE INTO evolution_phases 
                    (phase_name, start_date, end_date, description, key_events)
                    VALUES (?, ?, ?, ?, ?)
                ''', (phase["phase_name"], phase["start_date"], phase["end_date"], 
                      phase["description"], phase["key_events"]))
            
            conn.commit()
        
        self.logger.info("進化フェーズ登録完了")
    
    def determine_phase(self, date_str: str) -> str:
        """日付からフェーズを判定"""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        if date < datetime(2020, 1, 1):
            return "baseline"
        elif date < datetime(2022, 1, 1):
            return "covid" 
        elif date < datetime(2024, 8, 25):
            return "price_hike"
        elif date < datetime(2024, 8, 25):
            return "pre_hanazono"
        else:
            return "hanazono"
    
    def process_monthly_data(self, file_content: str, source_file: str):
        """月別データの処理"""
        lines = file_content.strip().split('\n')
        
        # ヘッダー行を探す
        header_line = None
        for i, line in enumerate(lines):
            if '月分' in line and '使用量' in line:
                header_line = i
                break
        
        if header_line is None:
            self.logger.error(f"ヘッダー行が見つかりません: {source_file}")
            return
        
        # データ行を処理
        for line in lines[header_line + 1:]:
            if not line.strip() or line.startswith('"ご契約番号'):
                continue
                
            try:
                # CSV行をパース
                fields = self.parse_csv_line(line)
                
                if len(fields) < 7:
                    continue
                
                # 年月分を解析
                year_month = fields[0].replace('年', '-').replace('月分', '')
                year, month = map(int, year_month.split('-'))
                
                usage_kwh = float(fields[6]) if fields[6] else 0
                cost_yen = int(fields[10]) if fields[10] else 0
                
                # 昼間・夜間使用量
                daytime_kwh = float(fields[7]) if len(fields) > 7 and fields[7] else None
                nighttime_kwh = float(fields[9]) if len(fields) > 9 and fields[9] else None
                
                # 気温データ
                avg_temp_high = float(fields[12]) if len(fields) > 12 and fields[12] else None
                avg_temp_low = float(fields[13]) if len(fields) > 13 and fields[13] else None
                
                # CO2排出量
                co2_kg = float(fields[14]) if len(fields) > 14 and fields[14] else None
                
                date_str = f"{year:04d}-{month:02d}-01"
                phase = self.determine_phase(date_str)
                
                # データベースに挿入
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT OR REPLACE INTO comprehensive_monthly
                        (year, month, usage_kwh, cost_yen, daytime_kwh, nighttime_kwh,
                         avg_temp_high, avg_temp_low, co2_kg, data_source, phase)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (year, month, usage_kwh, cost_yen, daytime_kwh, nighttime_kwh,
                          avg_temp_high, avg_temp_low, co2_kg, source_file, phase))
                
                self.logger.info(f"月次データ登録: {year}年{month}月 {usage_kwh}kWh")
                
            except Exception as e:
                self.logger.error(f"月次データ処理エラー: {line[:50]}... - {e}")
    
    def process_daily_data(self, file_content: str, source_file: str):
        """日別データの処理"""
        lines = file_content.strip().split('\n')
        
        # ヘッダー行を探す
        header_line = None
        for i, line in enumerate(lines):
            if '日付' in line and '使用量' in line:
                header_line = i
                break
        
        if header_line is None:
            self.logger.error(f"ヘッダー行が見つかりません: {source_file}")
            return
        
        # データ行を処理
        for line in lines[header_line + 1:]:
            if not line.strip() or line.startswith('"ご契約番号'):
                continue
                
            try:
                fields = self.parse_csv_line(line)
                
                if len(fields) < 7:
                    continue
                
                date_str = fields[0]
                weekday = fields[1]
                usage_kwh = float(fields[2]) if fields[2] else 0
                weather = fields[3] if len(fields) > 3 else None
                sunshine_hours = float(fields[4]) if len(fields) > 4 and fields[4] else None
                temp_high = float(fields[5]) if len(fields) > 5 and fields[5] else None  
                temp_low = float(fields[6]) if len(fields) > 6 and fields[6] else None
                
                # 日付を標準形式に変換
                date_parts = date_str.split('/')
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)
                    standard_date = f"{year:04d}-{month:02d}-{day:02d}"
                    phase = self.determine_phase(standard_date)
                    
                    # データベースに挿入
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT OR REPLACE INTO comprehensive_daily
                            (date, year, month, day, weekday, usage_kwh, weather,
                             sunshine_hours, temp_high, temp_low, data_source, phase)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (standard_date, year, month, day, weekday, usage_kwh,
                              weather, sunshine_hours, temp_high, temp_low, source_file, phase))
                    
                    self.logger.info(f"日次データ登録: {standard_date} {usage_kwh}kWh")
                
            except Exception as e:
                self.logger.error(f"日次データ処理エラー: {line[:50]}... - {e}")
    
    def parse_csv_line(self, line: str) -> List[str]:
        """CSV行をパース（カンマ区切り、ダブルクォート対応）"""
        fields = []
        current_field = ""
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                fields.append(current_field.strip())
                current_field = ""
            else:
                current_field += char
        
        fields.append(current_field.strip())
        return fields
    
    def analyze_6year_evolution(self) -> Dict:
        """6年間の進化分析"""
        with sqlite3.connect(self.db_path) as conn:
            # フェーズ別年間使用量
            phase_analysis = pd.read_sql_query('''
                SELECT phase, 
                       COUNT(*) as months,
                       AVG(usage_kwh) as avg_monthly_usage,
                       SUM(usage_kwh) as total_usage,
                       AVG(cost_yen) as avg_monthly_cost
                FROM comprehensive_monthly 
                WHERE usage_kwh > 0 
                GROUP BY phase 
                ORDER BY MIN(year), MIN(month)
            ''', conn)
            
            # 年別トレンド
            yearly_trend = pd.read_sql_query('''
                SELECT year,
                       SUM(usage_kwh) as annual_usage,
                       AVG(usage_kwh) as avg_monthly_usage,
                       SUM(cost_yen) as annual_cost,
                       phase
                FROM comprehensive_monthly 
                WHERE usage_kwh > 0
                GROUP BY year 
                ORDER BY year
            ''', conn)
            
            return {
                "phase_analysis": phase_analysis.to_dict('records'),
                "yearly_trend": yearly_trend.to_dict('records'),
                "data_summary": {
                    "total_months": len(phase_analysis),
                    "analysis_period": "2018-2025 (7年間)",
                    "phases_covered": phase_analysis['phase'].tolist()
                }
            }
    
    def generate_comprehensive_report(self) -> str:
        """総合分析レポート生成"""
        analysis = self.analyze_6year_evolution()
        
        report = "# HANAZONOシステム 6年間データ統合分析レポート\n\n"
        report += f"**分析期間**: {analysis['data_summary']['analysis_period']}\n"
        report += f"**対象月数**: {analysis['data_summary']['total_months']}ヶ月\n\n"
        
        report += "## フェーズ別分析\n\n"
        for phase in analysis["phase_analysis"]:
            report += f"### {phase['phase']}期\n"
            report += f"- 期間: {phase['months']}ヶ月\n"
            report += f"- 月平均使用量: {phase['avg_monthly_usage']:.1f}kWh\n"
            report += f"- 月平均電気代: ¥{phase['avg_monthly_cost']:,.0f}\n\n"
        
        report += "## 年別推移\n\n"
        for year in analysis["yearly_trend"]:
            report += f"**{year['year']}年** ({year['phase']}期): "
            report += f"{year['annual_usage']:,.0f}kWh (月平均{year['avg_monthly_usage']:.1f}kWh)\n"
        
        return report

# 使用例
def main():
    integrator = ComprehensiveDataIntegrator()
    integrator.register_evolution_phases()
    
    # 分析レポート生成
    report = integrator.generate_comprehensive_report()
    print(report)
    
    print("✅ 6年分データ統合システム準備完了")
    print("📊 世界最高レベルの電力使用分析が可能になりました！")

if __name__ == "__main__":
    main()
