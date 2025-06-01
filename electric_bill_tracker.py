#!/usr/bin/env python3
"""
四国電力 実電気代連携システム v1.0
HANAZONOシステム用実用電気代計算・追跡システム
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from pathlib import Path

class ElectricBillTracker:
    def __init__(self, db_path="data/hanazono_analysis.db"):
        self.db_path = db_path
        self.logger = self._setup_logger()
        self.init_database()
        
        # 四国電力「季節別時間帯別電灯」料金表
        self.yonden_rates = {
            "basic_charge": 1650,  # 基本料金（円/月）
            "rates": {
                "night": 26.00,      # 夜間料金 23:00-07:00（円/kWh）
                "day_other": 37.34,  # 昼間その他季料金（円/kWh）
                "day_summer": 42.76  # 昼間夏季料金 7-9月（円/kWh）
            },
            "fuel_adjustment": {
                "current_rate": 2.3,  # 燃料費調整額（円/kWh）2025年6月現在
                "renewable_levy": 1.4  # 再エネ賦課金（円/kWh）
            }
        }
        
        # 月別夏季判定
        self.summer_months = [7, 8, 9]
    
    def _setup_logger(self):
        """ログシステム初期化"""
        logger = logging.getLogger('electric_bill_tracker')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def init_database(self):
        """電気代データベース初期化"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 月次電気代テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_bills (
                billing_month TEXT PRIMARY KEY,  -- YYYY-MM形式
                total_amount INTEGER,             -- 総請求額（円）
                kwh_consumption REAL,             -- 総消費電力（kWh）
                night_kwh REAL,                   -- 夜間消費（kWh）
                day_kwh REAL,                     -- 昼間消費（kWh）
                basic_charge INTEGER,             -- 基本料金（円）
                energy_charge INTEGER,            -- 電力量料金（円）
                fuel_adjustment INTEGER,          -- 燃料費調整額（円）
                renewable_levy INTEGER,           -- 再エネ賦課金（円）
                grid_dependency_rate REAL,        -- グリッド依存度（%）
                solar_self_consumption REAL,      -- 太陽光自家消費（kWh）
                battery_efficiency REAL,          -- バッテリー効率（%）
                estimated_without_solar INTEGER,  -- ソーラーなし想定額（円）
                actual_savings INTEGER,           -- 実際の節約額（円）
                created_at TEXT,                  -- 登録日時
                data_source TEXT                  -- データソース（manual/api）
            )
        ''')
        
        # 日次電力使用量推定テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_power_estimate (
                date TEXT PRIMARY KEY,            -- YYYY-MM-DD形式
                grid_consumption REAL,            -- グリッド消費推定（kWh）
                solar_generation REAL,            -- 太陽光発電推定（kWh）
                battery_charge REAL,              -- バッテリー充電（kWh）
                battery_discharge REAL,           -- バッテリー放電（kWh）
                total_consumption REAL,           -- 総消費電力（kWh）
                night_consumption REAL,           -- 夜間消費（kWh）
                day_consumption REAL,             -- 昼間消費（kWh）
                estimated_cost REAL,              -- 推定電気代（円）
                weather_condition TEXT,           -- 天気条件
                season TEXT                       -- 季節
            )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("電気代データベースを初期化しました")
    
    def add_monthly_bill(self, bill_data):
        """
        月次請求書データを追加
        
        Args:
            bill_data: {
                "billing_month": "2025-05",
                "total_amount": 12580,
                "kwh_consumption": 285,
                "night_kwh": 165,
                "day_kwh": 120,
                "basic_charge": 1650,
                "energy_charge": 10930,
                "fuel_adjustment": 230,
                "renewable_levy": 180
            }
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 推定節約額を計算
            estimated_without_solar = self._estimate_cost_without_solar(bill_data)
            actual_savings = estimated_without_solar - bill_data["total_amount"]
            
            # グリッド依存度を計算
            grid_dependency = self._calculate_grid_dependency(bill_data)
            
            cursor.execute('''
                INSERT OR REPLACE INTO monthly_bills 
                (billing_month, total_amount, kwh_consumption, night_kwh, day_kwh,
                 basic_charge, energy_charge, fuel_adjustment, renewable_levy,
                 grid_dependency_rate, estimated_without_solar, actual_savings,
                 created_at, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bill_data["billing_month"],
                bill_data["total_amount"],
                bill_data["kwh_consumption"],
                bill_data.get("night_kwh", 0),
                bill_data.get("day_kwh", 0),
                bill_data.get("basic_charge", self.yonden_rates["basic_charge"]),
                bill_data.get("energy_charge", 0),
                bill_data.get("fuel_adjustment", 0),
                bill_data.get("renewable_levy", 0),
                grid_dependency,
                estimated_without_solar,
                actual_savings,
                datetime.now().isoformat(),
                "manual"
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"月次請求書データを追加: {bill_data['billing_month']}")
            return True
            
        except Exception as e:
            self.logger.error(f"月次請求書追加エラー: {e}")
            return False
    
    def _estimate_cost_without_solar(self, bill_data):
        """ソーラーシステムなしの場合の推定電気代を計算"""
        # 現在の消費量をベースに、ソーラー自家消費分を加算
        current_consumption = bill_data["kwh_consumption"]
        
        # ソーラー自家消費量を推定（簡易計算）
        # 実際のシステムデータから月間発電量を取得して計算
        estimated_solar_generation = self._get_monthly_solar_generation(bill_data["billing_month"])
        
        # ソーラーなしの場合の総消費量
        estimated_total_consumption = current_consumption + estimated_solar_generation
        
        # 四国電力料金で計算
        month = int(bill_data["billing_month"].split("-")[1])
        is_summer = month in self.summer_months
        
        # 夜間・昼間の消費配分を推定
        night_ratio = 0.45  # 夜間消費比率（深夜電力活用）
        estimated_night_consumption = estimated_total_consumption * night_ratio
        estimated_day_consumption = estimated_total_consumption * (1 - night_ratio)
        
        # 料金計算
        basic_charge = self.yonden_rates["basic_charge"]
        night_charge = estimated_night_consumption * self.yonden_rates["rates"]["night"]
        
        if is_summer:
            day_charge = estimated_day_consumption * self.yonden_rates["rates"]["day_summer"]
        else:
            day_charge = estimated_day_consumption * self.yonden_rates["rates"]["day_other"]
        
        # 燃料費調整・再エネ賦課金
        fuel_adj = estimated_total_consumption * self.yonden_rates["fuel_adjustment"]["current_rate"]
        renewable_levy = estimated_total_consumption * self.yonden_rates["fuel_adjustment"]["renewable_levy"]
        
        total_estimated = basic_charge + night_charge + day_charge + fuel_adj + renewable_levy
        
        return int(total_estimated)
    
    def _get_monthly_solar_generation(self, billing_month):
        """月間太陽光発電量を取得（システムデータから）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 該当月のデータを取得
            year, month = billing_month.split("-")
            
            cursor.execute('''
                SELECT COUNT(*) * 0.25 as estimated_generation_kwh
                FROM system_data 
                WHERE strftime('%Y-%m', datetime) = ?
                AND battery_soc IS NOT NULL
            ''', (billing_month,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                # 15分毎データから月間発電量を推定
                # 1日平均10kWh発電と仮定
                days_in_month = 30
                estimated_daily_generation = 10  # kWh/日
                return estimated_daily_generation * days_in_month
            
            return 300  # デフォルト値（月間300kWh）
            
        except Exception as e:
            self.logger.error(f"月間発電量取得エラー: {e}")
            return 300
    
    def _calculate_grid_dependency(self, bill_data):
        """グリッド依存度を計算"""
        total_consumption = bill_data["kwh_consumption"]
        estimated_solar = self._get_monthly_solar_generation(bill_data["billing_month"])
        
        # グリッド依存度 = グリッド消費 / (グリッド消費 + ソーラー自家消費)
        total_energy_used = total_consumption + estimated_solar
        grid_dependency = (total_consumption / total_energy_used) * 100
        
        return min(100, max(0, grid_dependency))
    
    def calculate_daily_cost(self, date_str):
        """日次電気代を計算"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 該当日のシステムデータを取得
            cursor.execute('''
                SELECT 
                    AVG(battery_soc) as avg_soc,
                    COUNT(*) as data_points,
                    MIN(battery_soc) as min_soc,
                    MAX(battery_soc) as max_soc
                FROM system_data 
                WHERE DATE(datetime) = ?
                AND battery_soc IS NOT NULL
            ''', (date_str,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                avg_soc, data_points, min_soc, max_soc = result
                
                # 簡易計算による日次電気代推定
                # バッテリー効率から電力使用パターンを推定
                battery_efficiency = min(100, (data_points / 96) * 100)  # 15分毎96回/日
                soc_variation = max_soc - min_soc
                
                # 基本的な日次消費量（家庭平均）
                base_daily_consumption = 9.5  # kWh/日
                
                # ソーラー・バッテリー効果による削減
                solar_reduction = (avg_soc / 100) * 0.7  # SOCに応じた削減効果
                grid_consumption = base_daily_consumption * (1 - solar_reduction)
                
                # 時間帯別消費配分
                night_consumption = grid_consumption * 0.4  # 夜間40%
                day_consumption = grid_consumption * 0.6    # 昼間60%
                
                # 料金計算
                month = int(date_str.split("-")[1])
                is_summer = month in self.summer_months
                
                night_cost = night_consumption * self.yonden_rates["rates"]["night"]
                if is_summer:
                    day_cost = day_consumption * self.yonden_rates["rates"]["day_summer"]
                else:
                    day_cost = day_consumption * self.yonden_rates["rates"]["day_other"]
                
                # 燃料費調整・再エネ賦課金（日割り）
                total_kwh = night_consumption + day_consumption
                fuel_adj = total_kwh * self.yonden_rates["fuel_adjustment"]["current_rate"]
                renewable_levy = total_kwh * self.yonden_rates["fuel_adjustment"]["renewable_levy"]
                basic_daily = self.yonden_rates["basic_charge"] / 30  # 日割り基本料金
                
                total_daily_cost = night_cost + day_cost + fuel_adj + renewable_levy + basic_daily
                
                return {
                    "date": date_str,
                    "estimated_cost": round(total_daily_cost),
                    "grid_consumption": round(grid_consumption, 2),
                    "night_consumption": round(night_consumption, 2),
                    "day_consumption": round(day_consumption, 2),
                    "solar_reduction_rate": round(solar_reduction * 100, 1),
                    "battery_efficiency": round(battery_efficiency, 1)
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"日次電気代計算エラー: {e}")
            return None
    
    def get_monthly_summary(self, billing_month):
        """月次サマリーを取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM monthly_bills 
                WHERE billing_month = ?
            ''', (billing_month,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                columns = [
                    'billing_month', 'total_amount', 'kwh_consumption', 'night_kwh', 'day_kwh',
                    'basic_charge', 'energy_charge', 'fuel_adjustment', 'renewable_levy',
                    'grid_dependency_rate', 'solar_self_consumption', 'battery_efficiency',
                    'estimated_without_solar', 'actual_savings', 'created_at', 'data_source'
                ]
                
                return dict(zip(columns, result))
            
            return None
            
        except Exception as e:
            self.logger.error(f"月次サマリー取得エラー: {e}")
            return None
    
    def get_yearly_analysis(self, year):
        """年間分析データを取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as months_recorded,
                    SUM(total_amount) as total_cost,
                    SUM(kwh_consumption) as total_kwh,
                    SUM(actual_savings) as total_savings,
                    AVG(grid_dependency_rate) as avg_grid_dependency,
                    MIN(total_amount) as min_monthly_cost,
                    MAX(total_amount) as max_monthly_cost
                FROM monthly_bills 
                WHERE billing_month LIKE ?
            ''', (f"{year}-%",))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                columns = [
                    'months_recorded', 'total_cost', 'total_kwh', 'total_savings',
                    'avg_grid_dependency', 'min_monthly_cost', 'max_monthly_cost'
                ]
                
                analysis = dict(zip(columns, result))
                
                # 年間予測計算
                if analysis['months_recorded'] > 0:
                    avg_monthly_cost = analysis['total_cost'] / analysis['months_recorded']
                    avg_monthly_savings = analysis['total_savings'] / analysis['months_recorded']
                    
                    analysis['projected_annual_cost'] = int(avg_monthly_cost * 12)
                    analysis['projected_annual_savings'] = int(avg_monthly_savings * 12)
                
                return analysis
            
            return None
            
        except Exception as e:
            self.logger.error(f"年間分析エラー: {e}")
            return None

def test_bill_tracker():
    """電気代トラッカーのテスト"""
    print("💰 四国電力 実電気代連携システム テスト開始")
    print("=" * 60)
    
    tracker = ElectricBillTracker()
    
    # テスト用月次データ
    test_bill = {
        "billing_month": "2025-05",
        "total_amount": 12580,
        "kwh_consumption": 285,
        "night_kwh": 165,
        "day_kwh": 120,
        "basic_charge": 1650,
        "energy_charge": 10200,
        "fuel_adjustment": 456,
        "renewable_levy": 274
    }
    
    print("📊 テスト用月次データ追加:")
    success = tracker.add_monthly_bill(test_bill)
    if success:
        print("✅ 月次データ追加成功")
    else:
        print("❌ 月次データ追加失敗")
    
    print("\n📈 月次サマリー取得:")
    summary = tracker.get_monthly_summary("2025-05")
    if summary:
        print(f"請求額: ¥{summary['total_amount']:,}")
        print(f"消費電力: {summary['kwh_consumption']}kWh")
        print(f"推定節約額: ¥{summary['actual_savings']:,}")
        print(f"グリッド依存度: {summary['grid_dependency_rate']:.1f}%")
    
    print("\n💡 日次電気代計算:")
    daily_cost = tracker.calculate_daily_cost("2025-06-01")
    if daily_cost:
        print(f"推定日次電気代: ¥{daily_cost['estimated_cost']}")
        print(f"グリッド消費: {daily_cost['grid_consumption']}kWh")
        print(f"ソーラー削減率: {daily_cost['solar_reduction_rate']}%")
    
    print("\n✅ 電気代トラッカーテスト完了")

if __name__ == "__main__":
    test_bill_tracker()
