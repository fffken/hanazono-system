#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム 電力データ管理システム v1.0
実電気代データの自動管理・GitHub統合・月次データ要求機能

作成日: 2025-06-01
機能:
- 四国電力実績データの構造化保存
- GitHub自動コミット・プッシュ
- 月次データ要求アラート
- 前年同月バトル分析
- レジスタマップ更新可能構造
"""

import json
import os
import csv
import subprocess
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class ElectricDataManager:
    """電力データ管理システム"""
    
    def __init__(self, data_dir="data/electric_bills"):
        self.data_dir = data_dir
        self.db_path = f"{data_dir}/electric_bills.db"
        self.csv_path = f"{data_dir}/monthly_bills.csv"
        self.logger = self.setup_logger()
        
        # ディレクトリ作成
        os.makedirs(data_dir, exist_ok=True)
        
        # データベース初期化
        self.init_database()
        
        # 既存データの登録
        self.register_historical_data()
        
    def setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('ElectricDataManager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('logs/electric_data_manager.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def init_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 月次電気代テーブル
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_bills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    kwh_usage INTEGER NOT NULL,
                    total_cost INTEGER NOT NULL,
                    cost_per_kwh REAL NOT NULL,
                    solar_status TEXT NOT NULL, -- 'before' or 'after'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(year, month)
                )
            ''')
            
            # 設定変更履歴テーブル（将来のレジスタマップ対応）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS setting_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    parameter_name TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT NOT NULL,
                    register_address TEXT, -- 将来のレジスタマップ対応
                    change_reason TEXT,
                    manual_change BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 月次データ要求履歴
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    request_date TIMESTAMP NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_date TIMESTAMP,
                    UNIQUE(year, month)
                )
            ''')
            
            conn.commit()
        
        self.logger.info("データベース初期化完了")
    
    def register_historical_data(self):
        """既存の電力データを登録"""
        historical_data = [
            # ソーラー導入前（2023年6月〜2024年5月）
            (2023, 6, 578, 13210, "before"),
            (2023, 7, 628, 16614, "before"),
            (2023, 8, 649, 17051, "before"),
            (2023, 9, 699, 17577, "before"),
            (2023, 10, 699, 17136, "before"),
            (2023, 11, 869, 19989, "before"),
            (2023, 12, 795, 17610, "before"),
            (2024, 1, 1129, 24413, "before"),
            (2024, 2, 884, 19301, "before"),
            (2024, 3, 893, 18573, "before"),
            (2024, 4, 729, 15352, "before"),
            (2024, 5, 811, 19861, "before"),
            
            # ソーラー導入後（2024年6月〜2025年5月）
            (2024, 6, 633, 17157, "after"),
            (2024, 7, 685, 20431, "after"),
            (2024, 8, 858, 25595, "after"),
            (2024, 9, 571, 10825, "after"),
            (2024, 10, 523, 10443, "after"),
            (2024, 11, 545, 11709, "after"),
            (2024, 12, 655, 15732, "after"),
            (2025, 1, 1068, 23684, "after"),
            (2025, 2, 746, 14979, "after"),
            (2025, 3, 746, 14778, "after"),
            (2025, 4, 467, 10132, "after"),
            (2025, 5, 376, 8956, "after"),
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for year, month, kwh, cost, status in historical_data:
                cost_per_kwh = round(cost / kwh, 2)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO monthly_bills 
                    (year, month, kwh_usage, total_cost, cost_per_kwh, solar_status, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (year, month, kwh, cost, cost_per_kwh, status))
            
            conn.commit()
        
        # CSV出力
        self.export_to_csv()
        self.logger.info("過去データ登録完了")
    
    def export_to_csv(self):
        """CSVファイル出力"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT year, month, kwh_usage, total_cost, cost_per_kwh, solar_status, updated_at
                FROM monthly_bills 
                ORDER BY year, month
            ''')
            
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['年', '月', '使用量(kWh)', '電気代(円)', '単価(円/kWh)', 'ソーラー', '更新日時'])
                writer.writerows(cursor.fetchall())
    
    def add_monthly_data(self, year: int, month: int, kwh: int, cost: int):
        """月次データ追加"""
        solar_status = "after" if year >= 2024 and (year > 2024 or month >= 6) else "before"
        cost_per_kwh = round(cost / kwh, 2)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO monthly_bills 
                (year, month, kwh_usage, total_cost, cost_per_kwh, solar_status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (year, month, kwh, cost, cost_per_kwh, solar_status))
            
            conn.commit()
        
        self.export_to_csv()
        self.commit_to_github(f"📊 電力データ更新: {year}年{month}月分追加")
        self.logger.info(f"月次データ追加: {year}年{month}月 {kwh}kWh ¥{cost:,}")
    
    def get_battle_analysis(self, year: int, month: int) -> Dict:
        """前年同月バトル分析"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 当月データ
            cursor.execute('''
                SELECT kwh_usage, total_cost FROM monthly_bills 
                WHERE year = ? AND month = ?
            ''', (year, month))
            current_data = cursor.fetchone()
            
            # 前年同月データ
            cursor.execute('''
                SELECT kwh_usage, total_cost FROM monthly_bills 
                WHERE year = ? AND month = ?
            ''', (year - 1, month))
            previous_data = cursor.fetchone()
            
            if not current_data or not previous_data:
                return {"error": "比較データが不足しています"}
            
            current_kwh, current_cost = current_data
            previous_kwh, previous_cost = previous_data
            
            savings = previous_cost - current_cost
            savings_percent = round(savings / previous_cost * 100, 1)
            
            return {
                "year": year,
                "month": month,
                "current": {"kwh": current_kwh, "cost": current_cost},
                "previous": {"kwh": previous_kwh, "cost": previous_cost},
                "savings": savings,
                "savings_percent": savings_percent,
                "result": "勝利🏆" if savings > 0 else "敗北💔",
                "battle_summary": f"{year}年{month}月 vs {year-1}年{month}月: {abs(savings):,}円{('削減' if savings > 0 else '増加')} ({savings_percent:+.1f}%)"
            }
    
    def check_monthly_data_request(self) -> Optional[Dict]:
        """月次データ要求チェック"""
        now = datetime.now()
        
        # 月末から3日後にデータ要求
        if now.day != 3:
            return None
        
        # 前月のデータ要求
        last_month = now.replace(day=1) - timedelta(days=1)
        target_year = last_month.year
        target_month = last_month.month
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 既にデータがあるかチェック
            cursor.execute('''
                SELECT id FROM monthly_bills 
                WHERE year = ? AND month = ?
            ''', (target_year, target_month))
            
            if cursor.fetchone():
                return None  # データ既存
            
            # 要求履歴チェック
            cursor.execute('''
                SELECT id FROM data_requests 
                WHERE year = ? AND month = ? AND request_date >= ?
            ''', (target_year, target_month, now.replace(day=1)))
            
            if cursor.fetchone():
                return None  # 今月既に要求済み
            
            # 要求記録
            cursor.execute('''
                INSERT INTO data_requests (year, month, request_date)
                VALUES (?, ?, ?)
            ''', (target_year, target_month, now))
            
            conn.commit()
        
        return {
            "year": target_year,
            "month": target_month,
            "message": f"📊 {target_year}年{target_month}月の電気代データを共有してください",
            "details": f"四国電力の請求書から以下の情報をお教えください:\n- 使用量: ○○○kWh\n- 電気代: ○○,○○○円"
        }
    
    def commit_to_github(self, message: str):
        """GitHub自動コミット"""
        try:
            # Git add
            subprocess.run(['git', 'add', self.data_dir], check=True, cwd='.')
            
            # Git commit
            subprocess.run(['git', 'commit', '-m', message], check=True, cwd='.')
            
            # Git push
            subprocess.run(['git', 'push'], check=True, cwd='.')
            
            self.logger.info(f"GitHub更新成功: {message}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"GitHub更新失敗: {e}")
    
    def update_register_map(self, register_data: Dict):
        """レジスタマップ更新（将来対応）"""
        register_file = f"{self.data_dir}/register_map.json"
        
        with open(register_file, 'w', encoding='utf-8') as f:
            json.dump(register_data, f, ensure_ascii=False, indent=2)
        
        self.commit_to_github("🔧 レジスタマップ更新")
        self.logger.info("レジスタマップ更新完了")
    
    def record_setting_change(self, parameter: str, old_value: str, new_value: str, reason: str = "", register_address: str = None):
        """設定変更記録（将来のレジスタマップ対応）"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO setting_changes 
                (timestamp, parameter_name, old_value, new_value, register_address, change_reason, manual_change)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (datetime.now(), parameter, old_value, new_value, register_address, reason, True))
            
            conn.commit()
        
        self.logger.info(f"設定変更記録: {parameter} {old_value} → {new_value}")
    
    def generate_monthly_report_data(self) -> Dict:
        """月次レポート用データ生成"""
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        # 当月バトル分析
        battle_result = self.get_battle_analysis(current_year, current_month)
        
        # 年間累計
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 当年累計
            cursor.execute('''
                SELECT SUM(kwh_usage), SUM(total_cost) 
                FROM monthly_bills 
                WHERE year = ? AND solar_status = 'after'
            ''', (current_year,))
            current_year_total = cursor.fetchone()
            
            # 前年同期累計
            cursor.execute('''
                SELECT SUM(kwh_usage), SUM(total_cost) 
                FROM monthly_bills 
                WHERE year = ? AND month <= ? AND solar_status = 'before'
            ''', (current_year - 1, current_month))
            previous_year_total = cursor.fetchone()
        
        return {
            "battle_result": battle_result,
            "current_year_total": current_year_total,
            "previous_year_total": previous_year_total,
            "data_request": self.check_monthly_data_request()
        }

def main():
    """メイン処理"""
    manager = ElectricDataManager()
    
    # 月次データ要求チェック
    data_request = manager.check_monthly_data_request()
    if data_request:
        print(f"🔔 {data_request['message']}")
        print(data_request['details'])
    
    # バトル分析例
    battle = manager.get_battle_analysis(2025, 5)
    if "error" not in battle:
        print(f"\n🏆 {battle['battle_summary']}")
        print(f"結果: {battle['result']}")

if __name__ == "__main__":
    main()
