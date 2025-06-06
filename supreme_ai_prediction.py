#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム 世界最高レベルAI予測エンジン v1.0
6年間の歴史データを活用した超高精度予測システム

Prediction Features:
1. 🔮 Daily Usage Prediction (日別使用量予測)
2. 📊 Monthly Battle Prediction (月次バトル結果予測)
3. ⚡ Optimization Recommendation (最適化提案)
4. 🎯 ROI Prediction (投資回収予測)
5. 🌟 Seasonal Pattern Learning (季節パターン学習)
"""

import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import logging
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

class SupremeAIPrediction:
    """世界最高レベルAI予測エンジン"""
    
    def __init__(self, db_path="data/comprehensive_electric_data.db"):
        self.db_path = db_path
        self.logger = self.setup_logger()
        
        # 機械学習モデル
        self.daily_model = None
        self.monthly_model = None
        self.scaler = StandardScaler()
        
        # 天気コード変換
        self.weather_codes = {
            "快晴": 0, "晴れ": 1, "曇り": 2, "にわか雨": 3, "雨": 4, 
            "雷": 5, "雨強し": 6, "みぞれ": 7, "雪": 8
        }
        
        # 季節パターン
        self.seasonal_patterns = {}
        
        # HANAZONOシステム設定効果
        self.hanazono_settings_effect = {
            "春秋季": {"charge_current": 50, "charge_time": 45, "output_soc": 45, "efficiency": 0.85},
            "夏季": {"charge_current": 35, "charge_time": 30, "output_soc": 35, "efficiency": 0.90},
            "冬季": {"charge_current": 60, "charge_time": 60, "output_soc": 60, "efficiency": 0.80}
        }
    
    def setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('SupremeAIPrediction')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('logs/ai_prediction.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_training_data(self) -> pd.DataFrame:
        """訓練データの読み込み"""
        with sqlite3.connect(self.db_path) as conn:
            # 日別データと月別データを結合
            query = '''
                SELECT d.date, d.usage_kwh, d.weather, d.sunshine_hours,
                       d.temp_high, d.temp_low, d.weekday, d.phase,
                       m.cost_yen, m.daytime_kwh, m.nighttime_kwh
                FROM comprehensive_daily d
                LEFT JOIN comprehensive_monthly m 
                    ON d.year = m.year AND d.month = m.month
                WHERE d.usage_kwh > 0
                ORDER BY d.date
            '''
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            self.logger.warning("訓練データが見つかりません")
            return pd.DataFrame()
        
        # 特徴量エンジニアリング
        df = self.engineer_features(df)
        
        self.logger.info(f"訓練データ読み込み完了: {len(df)}日分")
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """特徴量エンジニアリング"""
        # 日付特徴量
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_year'] = df['date'].dt.dayofyear
        df['month'] = df['date'].dt.month
        df['season'] = df['month'].apply(self.get_season)
        df['is_weekend'] = df['weekday'].isin(['土', '日']).astype(int)
        
        # 天気特徴量
        df['weather_code'] = df['weather'].map(self.weather_codes).fillna(2)  # デフォルト曇り
        
        # 気温特徴量
        df['temp_avg'] = (df['temp_high'] + df['temp_low']) / 2
        df['temp_range'] = df['temp_high'] - df['temp_low']
        
        # 冷暖房需要予測
        df['cooling_demand'] = np.maximum(df['temp_high'] - 25, 0)  # 25度以上で冷房需要
        df['heating_demand'] = np.maximum(18 - df['temp_low'], 0)   # 18度以下で暖房需要
        
        # フェーズ特徴量
        phase_mapping = {"baseline": 0, "covid": 1, "price_hike": 2, "pre_hanazono": 3, "hanazono": 4}
        df['phase_code'] = df['phase'].map(phase_mapping)
        
        # 移動平均特徴量（過去3日、7日）
        df['usage_ma3'] = df['usage_kwh'].rolling(window=3, min_periods=1).mean()
        df['usage_ma7'] = df['usage_kwh'].rolling(window=7, min_periods=1).mean()
        df['temp_ma3'] = df['temp_avg'].rolling(window=3, min_periods=1).mean()
        
        # ラグ特徴量（前日、前週同曜日）
        df['usage_lag1'] = df['usage_kwh'].shift(1)
        df['usage_lag7'] = df['usage_kwh'].shift(7)
        
        # 欠損値補完
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        return df
    
    def get_season(self, month: int) -> str:
        """季節判定"""
        if month in [12, 1, 2, 3]:
            return "冬季"
        elif month in [4, 5, 6, 10, 11]:
            return "春秋季"
        else:  # 7, 8, 9
            return "夏季"
    
    def train_models(self):
        """機械学習モデルの訓練"""
        df = self.load_training_data()
        
        if df.empty:
            self.logger.error("訓練データが不足しています")
            return
        
        # 特徴量選択
        feature_columns = [
            'day_of_year', 'month', 'is_weekend', 'weather_code',
            'temp_high', 'temp_low', 'temp_avg', 'temp_range',
            'sunshine_hours', 'cooling_demand', 'heating_demand',
            'phase_code', 'usage_ma3', 'usage_ma7', 'temp_ma3',
            'usage_lag1', 'usage_lag7'
        ]
        
        # 特徴量とターゲットを分離
        X = df[feature_columns].dropna()
        y = df.loc[X.index, 'usage_kwh']
        
        # 正規化
        X_scaled = self.scaler.fit_transform(X)
        
        # 訓練・テストデータ分割
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # 日別予測モデル訓練（Random Forest + Gradient Boosting）
        self.daily_model = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=42),
            'gbr': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        for name, model in self.daily_model.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.logger.info(f"{name}モデル性能: MAE={mae:.2f}, R²={r2:.3f}")
        
        # 特徴量重要度を記録
        feature_importance = list(zip(feature_columns, 
                                    self.daily_model['rf'].feature_importances_))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        self.logger.info("重要特徴量トップ5:")
        for feature, importance in feature_importance[:5]:
            self.logger.info(f"  {feature}: {importance:.3f}")
        
        # 季節パターン学習
        self.learn_seasonal_patterns(df)
        
        self.logger.info("機械学習モデル訓練完了")
    
    def learn_seasonal_patterns(self, df: pd.DataFrame):
        """季節パターンの学習"""
        for season in ["春秋季", "夏季", "冬季"]:
            season_data = df[df['season'] == season]
            if not season_data.empty:
                self.seasonal_patterns[season] = {
                    "avg_usage": season_data['usage_kwh'].mean(),
                    "std_usage": season_data['usage_kwh'].std(),
                    "avg_temp": season_data['temp_avg'].mean(),
                    "peak_months": season_data.groupby('month')['usage_kwh'].mean().to_dict()
                }
        
        self.logger.info("季節パターン学習完了")
    
    def predict_daily_usage(self, date: str, weather: str, temp_high: float, 
                          temp_low: float, sunshine_hours: float = None) -> Dict:
        """🔮 日別使用量予測"""
        if self.daily_model is None:
            return {"error": "モデルが訓練されていません"}
        
        try:
            # 特徴量作成
            pred_date = pd.to_datetime(date)
            features = self.create_prediction_features(
                pred_date, weather, temp_high, temp_low, sunshine_hours
            )
            
            # 予測実行
            features_scaled = self.scaler.transform([features])
            
            # アンサンブル予測
            rf_pred = self.daily_model['rf'].predict(features_scaled)[0]
            gbr_pred = self.daily_model['gbr'].predict(features_scaled)[0]
            ensemble_pred = (rf_pred + gbr_pred) / 2
            
            # 季節補正
            season = self.get_season(pred_date.month)
            if season in self.seasonal_patterns:
                seasonal_factor = self.seasonal_patterns[season]["avg_usage"] / 25.0  # ベースライン
                ensemble_pred *= seasonal_factor
            
            # HANAZONOシステム効果適用
            if pred_date >= pd.to_datetime("2024-08-25"):
                hanazono_effect = self.calculate_hanazono_effect(season, weather, temp_high)
                ensemble_pred *= (1 - hanazono_effect)
            
            # 信頼区間計算
            confidence_interval = self.calculate_confidence_interval(ensemble_pred, season)
            
            return {
                "predicted_usage": round(ensemble_pred, 2),
                "confidence_low": round(confidence_interval[0], 2),
                "confidence_high": round(confidence_interval[1], 2),
                "season": season,
                "weather_impact": self.analyze_weather_impact(weather, temp_high, temp_low),
                "prediction_summary": f"{date}: {ensemble_pred:.1f}kWh予測 ({season})"
            }
            
        except Exception as e:
            self.logger.error(f"予測エラー: {e}")
            return {"error": f"予測に失敗しました: {e}"}
    
    def create_prediction_features(self, date: pd.Timestamp, weather: str, 
                                 temp_high: float, temp_low: float, 
                                 sunshine_hours: float = None) -> List[float]:
        """予測用特徴量作成"""
        temp_avg = (temp_high + temp_low) / 2
        temp_range = temp_high - temp_low
        
        # 過去データから移動平均・ラグ特徴量を取得
        historical_data = self.get_historical_context(date)
        
        features = [
            date.dayofyear,  # day_of_year
            date.month,      # month
            1 if date.weekday() >= 5 else 0,  # is_weekend
            self.weather_codes.get(weather, 2),  # weather_code
            temp_high,       # temp_high
            temp_low,        # temp_low
            temp_avg,        # temp_avg
            temp_range,      # temp_range
            sunshine_hours if sunshine_hours else 8.0,  # sunshine_hours (デフォルト8時間)
            max(temp_high - 25, 0),  # cooling_demand
            max(18 - temp_low, 0),   # heating_demand
            4 if date >= pd.to_datetime("2024-08-25") else 2,  # phase_code
            historical_data.get("usage_ma3", 22.0),   # usage_ma3
            historical_data.get("usage_ma7", 22.0),   # usage_ma7
            historical_data.get("temp_ma3", temp_avg), # temp_ma3
            historical_data.get("usage_lag1", 22.0),  # usage_lag1
            historical_data.get("usage_lag7", 22.0)   # usage_lag7
        ]
        
        return features
    
    def get_historical_context(self, date: pd.Timestamp) -> Dict:
        """過去データのコンテキスト取得"""
        with sqlite3.connect(self.db_path) as conn:
            # 過去30日のデータを取得
            start_date = (date - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
            
            query = '''
                SELECT usage_kwh, temp_high, temp_low
                FROM comprehensive_daily
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            
            if df.empty:
                return {}
            
            df['temp_avg'] = (df['temp_high'] + df['temp_low']) / 2
            
            return {
                "usage_ma3": df['usage_kwh'].head(3).mean(),
                "usage_ma7": df['usage_kwh'].head(7).mean(),
                "temp_ma3": df['temp_avg'].head(3).mean(),
                "usage_lag1": df['usage_kwh'].iloc[0] if len(df) > 0 else None,
                "usage_lag7": df['usage_kwh'].iloc[6] if len(df) > 6 else None
            }
    
    def calculate_hanazono_effect(self, season: str, weather: str, temp_high: float) -> float:
        """HANAZONOシステム効果計算"""
        base_efficiency = self.hanazono_settings_effect.get(season, {}).get("efficiency", 0.85)
        
        # 天気による調整
        weather_factor = {
            "快晴": 1.2, "晴れ": 1.1, "曇り": 1.0, "にわか雨": 0.9, "雨": 0.8
        }.get(weather, 1.0)
        
        # 気温による調整（最適温度域での効率向上）
        if 20 <= temp_high <= 30:
            temp_factor = 1.1
        elif temp_high > 35 or temp_high < 0:
            temp_factor = 0.9
        else:
            temp_factor = 1.0
        
        return min(base_efficiency * weather_factor * temp_factor, 0.95)  # 最大95%削減
    
    def calculate_confidence_interval(self, prediction: float, season: str) -> Tuple[float, float]:
        """信頼区間計算"""
        if season in self.seasonal_patterns:
            std = self.seasonal_patterns[season]["std_usage"]
        else:
            std = 5.0  # デフォルト標準偏差
        
        # 95%信頼区間
        margin = 1.96 * std
        return (max(prediction - margin, 0), prediction + margin)
    
    def analyze_weather_impact(self, weather: str, temp_high: float, temp_low: float) -> Dict:
        """天気影響分析"""
        impact_level = "normal"
        impact_description = "通常の使用量"
        
        # 冷暖房需要分析
        if temp_high > 30:
            impact_level = "high"
            impact_description = f"猛暑日(最高{temp_high}℃) - 冷房需要増加"
        elif temp_low < 5:
            impact_level = "high" 
            impact_description = f"厳寒日(最低{temp_low}℃) - 暖房需要増加"
        elif weather in ["雨", "雨強し"]:
            impact_level = "medium"
            impact_description = "雨天 - 在宅時間増加により使用量やや増加"
        elif weather in ["快晴", "晴れ"]:
            impact_level = "low"
            impact_description = "晴天 - 外出増加により使用量やや減少"
        
        return {
            "impact_level": impact_level,
            "description": impact_description,
            "cooling_demand": max(temp_high - 25, 0),
            "heating_demand": max(18 - temp_low, 0)
        }
    
    def predict_monthly_battle(self, year: int, month: int) -> Dict:
        """📊 月次バトル結果予測"""
        try:
            # 当月の日々の予測を積み上げ
            month_start = pd.to_datetime(f"{year}-{month:02d}-01")
            
            if month == 12:
                month_end = pd.to_datetime(f"{year+1}-01-01") - timedelta(days=1)
            else:
                month_end = pd.to_datetime(f"{year}-{month+1:02d}-01") - timedelta(days=1)
            
            # 簡易的な月間予測（実際の実装では日々の予測を積み上げ）
            season = self.get_season(month)
            base_usage = self.seasonal_patterns.get(season, {}).get("avg_usage", 25.0)
            
            # 月の日数分を積算
            days_in_month = (month_end - month_start).days + 1
            predicted_monthly_usage = base_usage * days_in_month
            
            # HANAZONOシステム効果適用
            if year >= 2024 and month >= 8:
                hanazono_effect = self.calculate_hanazono_effect(season, "曇り", 25.0)
                predicted_monthly_usage *= (1 - hanazono_effect)
            
            # 前年同月との比較
            previous_year_usage = self.get_historical_monthly_usage(year - 1, month)
            
            if previous_year_usage:
                battle_result = "勝利" if predicted_monthly_usage < previous_year_usage else "敗北"
                improvement = ((previous_year_usage - predicted_monthly_usage) / previous_year_usage) * 100
            else:
                battle_result = "データ不足"
                improvement = 0
            
            return {
                "predicted_usage": round(predicted_monthly_usage, 1),
                "previous_year_usage": previous_year_usage,
                "predicted_battle_result": battle_result,
                "predicted_improvement": round(improvement, 1),
                "confidence": "high" if abs(improvement) > 10 else "medium",
                "battle_summary": f"{year}年{month}月予測: {improvement:+.1f}% ({battle_result})"
            }
            
        except Exception as e:
            self.logger.error(f"月次バトル予測エラー: {e}")
            return {"error": f"予測に失敗しました: {e}"}
    
    def get_historical_monthly_usage(self, year: int, month: int) -> Optional[float]:
        """過去の月間使用量取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT usage_kwh FROM comprehensive_monthly
                WHERE year = ? AND month = ?
            ''', (year, month))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def recommend_optimization(self, weather_forecast: List[Dict]) -> Dict:
        """⚡ 最適化提案"""
        recommendations = []
        total_savings = 0
        
        for day_forecast in weather_forecast[:7]:  # 1週間分
            date = day_forecast["date"]
            weather = day_forecast["weather"]
            temp_high = day_forecast["temp_high"]
            temp_low = day_forecast["temp_low"]
            
            # 使用量予測
            prediction = self.predict_daily_usage(date, weather, temp_high, temp_low)
            
            if "error" not in prediction:
                # 最適設定提案
                season = prediction["season"]
                optimal_settings = self.hanazono_settings_effect.get(season, {})
                
                # 天気別微調整
                if weather in ["快晴", "晴れ"]:
                    adjustment = "☀️ 晴天設定: 充電電流-10A（発電量豊富のため）"
                    savings_boost = 0.05
                elif weather in ["雨", "雨強し"]:
                    adjustment = "🌧️ 雨天設定: 充電電流+10A（発電量不足のため）"
                    savings_boost = -0.02
                else:
                    adjustment = "☁️ 標準設定: 推奨設定を維持"
                    savings_boost = 0
                
                daily_savings = prediction["predicted_usage"] * savings_boost * 30  # 電気代換算
                total_savings += daily_savings
                
                recommendations.append({
                    "date": date,
                    "predicted_usage": prediction["predicted_usage"],
                    "optimal_settings": optimal_settings,
                    "adjustment": adjustment,
                    "estimated_savings": round(daily_savings, 0)
                })
        
        return {
            "weekly_recommendations": recommendations,
            "total_weekly_savings": round(total_savings, 0),
            "optimization_summary": f"1週間の最適化で約¥{total_savings:,.0f}の追加削減可能"
        }
    
    def predict_roi(self, investment_amount: float, years: int = 10) -> Dict:
        """🎯 ROI予測"""
        try:
            # 年間削減額の予測（現在の実績ベース）
            current_annual_savings = 32266  # 実績値
            
            # 将来の削減額予測（システム学習効果込み）
            future_savings = []
            for year in range(1, years + 1):
                # 学習効果による改善（年2%向上）
                learning_factor = 1 + (0.02 * year)
                
                # 電気料金上昇（年3%）
                price_inflation = 1 + (0.03 * year)
                
                # 設備劣化（年0.5%効率低下）
                degradation_factor = 1 - (0.005 * year)
                
                annual_savings = current_annual_savings * learning_factor * price_inflation * degradation_factor
                future_savings.append(annual_savings)
            
            # ROI計算
            total_savings = sum(future_savings)
            roi_percentage = ((total_savings - investment_amount) / investment_amount) * 100
            payback_period = investment_amount / current_annual_savings
            
            return {
                "investment_amount": investment_amount,
                "analysis_period": years,
                "annual_savings_year1": round(future_savings[0], 0),
                "total_savings": round(total_savings, 0),
                "net_profit": round(total_savings - investment_amount, 0),
                "roi_percentage": round(roi_percentage, 1),
                "payback_period": round(payback_period, 1),
                "roi_summary": f"{years}年間ROI: {roi_percentage:.1f}% (投資回収期間: {payback_period:.1f}年)"
            }
            
        except Exception as e:
            self.logger.error(f"ROI予測エラー: {e}")
            return {"error": f"ROI予測に失敗しました: {e}"}

def main():
    """メイン処理"""
    ai_engine = SupremeAIPrediction()
    
    print("🧠 世界最高レベルAI予測エンジン起動！")
    print("==========================================")
    
    # モデル訓練
    print("📚 機械学習モデル訓練中...")
    ai_engine.train_models()
    
    # 明日の予測例
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    prediction = ai_engine.predict_daily_usage(tomorrow, "曇り", 25.0, 15.0, 8.0)
    
    if "error" not in prediction:
        print(f"\n🔮 明日の予測: {prediction['prediction_summary']}")
        print(f"   信頼区間: {prediction['confidence_low']}-{prediction['confidence_high']}kWh")
    
    # 今月のバトル予測
    now = datetime.now()
    battle_pred = ai_engine.predict_monthly_battle(now.year, now.month)
    
    if "error" not in battle_pred:
        print(f"\n📊 今月のバトル予測: {battle_pred['battle_summary']}")
    
    # ROI予測
    roi = ai_engine.predict_roi(1000000, 10)  # 100万円投資の10年ROI
    if "error" not in roi:
        print(f"\n💰 投資回収予測: {roi['roi_summary']}")
    
    print("\n✅ 世界最高レベルAI予測エンジン準備完了！")

if __name__ == "__main__":
    main()
