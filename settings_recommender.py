#!/usr/bin/env python3
"""
HANAZONOシステム 設定推奨エンジン v1.0
天気予報データから最適設定を自動計算

HANAZONO-SYSTEM-SETTINGS.mdの設定表を完全実装
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

class SettingsRecommender:
    def __init__(self, settings_file="settings.json", db_path="data/hanazono_analysis.db"):
        self.settings_file = settings_file
        self.db_path = db_path
        self.load_settings()
        
        # HANAZONO-SYSTEM-SETTINGS.mdの設定表を完全実装
        self.base_settings = {
            "winter": {
                "season_period": "12月-3月",
                "typeB": {"ID07": 60, "ID10": 60, "ID41": "03:00", "ID62": 60},
                "typeA": {
                    "normal": {"ID07": 60, "ID10": 60, "ID41": "03:00", "ID62": 60},
                    "sunny_3days": {"ID07": 50, "ID10": 45, "ID41": "02:30", "ID62": 50},
                    "rainy_3days": {"ID07": 70, "ID10": 75, "ID41": "03:30", "ID62": 70}
                }
            },
            "spring_fall": {
                "season_period": "4月-6月, 10月-11月",
                "typeB": {"ID07": 50, "ID10": 45, "ID41": "03:00", "ID62": 45},
                "typeA": {
                    "normal": {"ID07": 50, "ID10": 45, "ID41": "03:00", "ID62": 35},
                    "sunny_3days": {"ID07": 40, "ID10": 30, "ID41": "02:30", "ID62": 35},
                    "rainy_3days": {"ID07": 60, "ID10": 60, "ID41": "03:30", "ID62": 55}
                }
            },
            "summer": {
                "season_period": "7月-9月",
                "typeB": {"ID07": 35, "ID10": 30, "ID41": "03:00", "ID62": 35},
                "typeA": {
                    "normal": {"ID07": 35, "ID10": 30, "ID41": "03:00", "ID62": 35},
                    "sunny_3days": {"ID07": 25, "ID10": 15, "ID41": "02:30", "ID62": 25},
                    "rainy_3days": {"ID07": 45, "ID10": 45, "ID41": "03:30", "ID62": 45}
                }
            }
        }
        
        # 天候判断ルール
        self.weather_rules = {
            "sunny_keywords": ["晴", "晴れ", "快晴"],
            "rainy_keywords": ["雨", "雷雨", "大雨", "小雨"],
            "cloudy_keywords": ["曇", "曇り", "くもり"],
            "threshold_days": 3  # 連続天候判断の日数
        }
    
    def load_settings(self):
        """既存設定読み込み"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.current_settings = json.load(f)
        except Exception as e:
            print(f"⚠️ 設定ファイル読み込みエラー: {e}")
            self.current_settings = {}
    
    def get_current_season(self):
        """現在の季節を判定"""
        month = datetime.now().month
        
        if month in [12, 1, 2, 3]:
            return "winter"
        elif month in [4, 5, 6, 10, 11]:
            return "spring_fall"
        elif month in [7, 8, 9]:
            return "summer"
        else:
            return "spring_fall"  # デフォルト
    
    def analyze_weather_pattern(self, weather_data):
        """
        3日間の天気パターンを分析
        
        Args:
            weather_data: {
                "today": {"weather": "晴れ", "temp_max": 25, "temp_min": 15},
                "tomorrow": {"weather": "曇り", "temp_max": 22, "temp_min": 14},
                "day_after_tomorrow": {"weather": "雨", "temp_max": 20, "temp_min": 12}
            }
        
        Returns:
            str: "sunny_3days", "rainy_3days", "normal"
        """
        if not weather_data:
            return "normal"
        
        days = ["today", "tomorrow", "day_after_tomorrow"]
        weather_conditions = []
        
        for day in days:
            if day in weather_data:
                weather = weather_data[day].get("weather", "")
                weather_conditions.append(weather)
        
        if len(weather_conditions) < 2:
            return "normal"
        
        # 3日間連続晴天判定
        sunny_count = sum(1 for w in weather_conditions 
                         if any(keyword in w for keyword in self.weather_rules["sunny_keywords"]))
        
        # 3日間連続雨天判定
        rainy_count = sum(1 for w in weather_conditions 
                         if any(keyword in w for keyword in self.weather_rules["rainy_keywords"]))
        
        if sunny_count >= 2:
            return "sunny_3days"
        elif rainy_count >= 2:
            return "rainy_3days"
        else:
            return "normal"
    
    def get_performance_data(self, days=7):
        """過去の性能データから補正値を計算"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT 
                    AVG(battery_soc) as avg_soc,
                    MIN(battery_soc) as min_soc,
                    MAX(battery_soc) as max_soc
                FROM system_data 
                WHERE datetime > datetime('now', '-{} days')
                AND battery_soc IS NOT NULL
            '''.format(days)
            
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                avg_soc, min_soc, max_soc = result
                return {
                    "avg_soc": avg_soc or 50,
                    "min_soc": min_soc or 20,
                    "max_soc": max_soc or 80,
                    "soc_range": (max_soc or 80) - (min_soc or 20)
                }
        except Exception as e:
            print(f"⚠️ 性能データ取得エラー: {e}")
        
        return {"avg_soc": 50, "min_soc": 20, "max_soc": 80, "soc_range": 60}
    
    def recommend_settings(self, weather_data, operation_mode="typeB"):
        """
        天気予報データから最適設定を計算
        
        Args:
            weather_data: 3日分の天気予報データ
            operation_mode: "typeB" (省管理型) or "typeA" (変動型)
            
        Returns:
            dict: 推奨設定値と詳細情報
        """
        season = self.get_current_season()
        weather_pattern = self.analyze_weather_pattern(weather_data)
        performance = self.get_performance_data()
        
        # 基本設定取得
        if operation_mode == "typeB":
            base_config = self.base_settings[season]["typeB"]
            change_type = "seasonal"
            change_reason = f"季節設定（{self.base_settings[season]['season_period']}）"
        else:
            base_config = self.base_settings[season]["typeA"][weather_pattern]
            change_type = weather_pattern
            
            if weather_pattern == "sunny_3days":
                change_reason = "☀️ 3日間晴天予報 - 発電量増加に備えて放電設定を控えめに"
            elif weather_pattern == "rainy_3days":
                change_reason = "🌧️ 3日間雨天予報 - 発電量減少に備えて蓄電設定を強化"
            else:
                change_reason = f"通常設定（{self.base_settings[season]['season_period']}）"
        
        # 性能データによる補正
        correction = self._calculate_performance_correction(performance, weather_pattern)
        
        # 最終設定値計算
        final_settings = {}
        for param, value in base_config.items():
            if param in correction:
                if isinstance(value, int):
                    final_settings[param] = max(0, value + correction[param])
                else:
                    final_settings[param] = value
            else:
                final_settings[param] = value
        
        # メールタイトル用の絵文字決定
        title_emoji = self._get_title_emoji(season, change_type)
        
        return {
            "settings": final_settings,
            "season": season,
            "weather_pattern": weather_pattern,
            "change_type": change_type,
            "change_reason": change_reason,
            "title_emoji": title_emoji,
            "operation_mode": operation_mode,
            "performance_data": performance,
            "is_changed": change_type != "seasonal",
            "confidence": self._calculate_confidence(weather_data, performance)
        }
    
    def _calculate_performance_correction(self, performance, weather_pattern):
        """性能データに基づく設定補正値を計算"""
        correction = {"ID07": 0, "ID10": 0, "ID62": 0}
        
        avg_soc = performance["avg_soc"]
        soc_range = performance["soc_range"]
        
        # SOCが低すぎる場合の補正
        if avg_soc < 30:
            correction["ID07"] += 5  # 充電電流増加
            correction["ID10"] += 5  # 充電時間延長
            correction["ID62"] += 5  # SOC設定上昇
        
        # SOCが高すぎる場合の補正
        elif avg_soc > 70:
            correction["ID07"] -= 3  # 充電電流減少
            correction["ID10"] -= 3  # 充電時間短縮
            correction["ID62"] -= 3  # SOC設定低下
        
        # 天候による追加補正
        if weather_pattern == "rainy_3days" and avg_soc < 40:
            correction["ID62"] += 10  # 雨天時は特に蓄電重視
        
        return correction
    
    def _get_title_emoji(self, season, change_type):
        """メールタイトル用絵文字を決定"""
        if change_type == "seasonal":
            season_emojis = {
                "winter": "❄️",
                "spring_fall": "🌸" if datetime.now().month <= 6 else "🍂",
                "summer": "🌻"
            }
            return season_emojis.get(season, "🌸")
        elif change_type == "sunny_3days":
            return "🟠"
        elif change_type == "rainy_3days":
            return "🔵"
        else:
            return "🟣"
    
    def _calculate_confidence(self, weather_data, performance):
        """推奨設定の信頼度を計算"""
        confidence = 5  # 基本信頼度
        
        # 天気データの完全性
        if weather_data and len(weather_data) >= 2:
            confidence += 2
        else:
            confidence -= 1
        
        # 性能データの安定性
        if performance["soc_range"] < 30:  # SOC変動が安定
            confidence += 1
        elif performance["soc_range"] > 50:  # SOC変動が激しい
            confidence -= 1
        
        return min(5, max(1, confidence))
    
    def compare_with_current(self, recommended):
        """現在の設定と推奨設定を比較"""
        try:
            # 現在の設定値を取得（簡易版）
            season = recommended["season"]
            current = self.base_settings[season]["typeB"]  # 基本設定と比較
            
            changes = {}
            for param, new_value in recommended["settings"].items():
                old_value = current.get(param)
                if old_value != new_value:
                    changes[param] = {
                        "old": old_value,
                        "new": new_value,
                        "change": f"{old_value} → {new_value}"
                    }
            
            return changes
        except Exception as e:
            print(f"⚠️ 設定比較エラー: {e}")
            return {}

def test_recommender():
    """設定推奨エンジンのテスト"""
    recommender = SettingsRecommender()
    
    # テスト用天気データ
    test_weather = {
        "today": {"weather": "晴れ", "temp_max": 25, "temp_min": 15},
        "tomorrow": {"weather": "晴れ", "temp_max": 27, "temp_min": 16},
        "day_after_tomorrow": {"weather": "晴れ", "temp_max": 26, "temp_min": 17}
    }
    
    print("🔧 設定推奨エンジン テスト開始")
    print("=" * 50)
    
    # タイプB（省管理型）テスト
    print("📋 タイプB（省管理型）設定:")
    result_b = recommender.recommend_settings(test_weather, "typeB")
    print(f"季節: {result_b['season']}")
    print(f"設定: {result_b['settings']}")
    print(f"理由: {result_b['change_reason']}")
    print(f"絵文字: {result_b['title_emoji']}")
    print(f"信頼度: {'⭐' * result_b['confidence']}")
    
    print()
    
    # タイプA（変動型）テスト
    print("🔄 タイプA（変動型）設定:")
    result_a = recommender.recommend_settings(test_weather, "typeA")
    print(f"天気パターン: {result_a['weather_pattern']}")
    print(f"設定: {result_a['settings']}")
    print(f"理由: {result_a['change_reason']}")
    print(f"絵文字: {result_a['title_emoji']}")
    print(f"信頼度: {'⭐' * result_a['confidence']}")
    
    # 設定変更確認
    changes = recommender.compare_with_current(result_a)
    if changes:
        print(f"\n🔄 設定変更:")
        for param, change in changes.items():
            print(f"  {param}: {change['change']}")
    else:
        print("\n✅ 設定変更なし")
    
    print("\n✅ テスト完了")

if __name__ == "__main__":
    test_recommender()
