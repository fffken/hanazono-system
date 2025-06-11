#!/usr/bin/env python3
"""
HANAZONO Setting Change Detection & Savings Visualization System v1.0
手動設定変更検知 + 削減効果可視化システム

機能:
- Modbus設定値リアルタイム監視
- 手動変更検知・記録
- 変更前後効果測定
- 貯金型累積削減額表示
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

class SettingChangeDetector:
    """設定変更検知システム"""
    
    def __init__(self):
        self.version = "1.0.0-CHANGE-DETECTOR"
        
        # データベース初期化
        self.db_path = "data/setting_changes.db"
        self.savings_db_path = "data/savings_tracking.db"
        self._initialize_databases()
        
        # 監視対象パラメーター
        self.monitored_parameters = {
            "ID07": {"address": 0x07, "name": "充電電流", "unit": "A"},
            "ID10": {"address": 0x10, "name": "充電時間", "unit": "分"},
            "ID62": {"address": 0x62, "name": "出力SOC", "unit": "%"},
            "ID40": {"address": 0x40, "name": "充電開始時間", "unit": "時"},
            "ID41": {"address": 0x41, "name": "充電終了時間", "unit": "時"},
            "ID28": {"address": 0x28, "name": "低電圧保護", "unit": "V"}
        }
        
        # 現在の設定値キャッシュ
        self.current_settings = {}
        self.last_check_time = None
        
    def _initialize_databases(self):
        """データベース初期化"""
        # 設定変更記録DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setting_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                parameter_id TEXT NOT NULL,
                old_value INTEGER,
                new_value INTEGER,
                change_source TEXT DEFAULT 'manual',
                detection_method TEXT,
                weather_condition TEXT,
                season TEXT
            )
        ''')
        
        # 削減効果追跡DB
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                change_id INTEGER,
                measurement_date TEXT,
                period_type TEXT, -- daily, weekly, monthly
                baseline_cost REAL,
                actual_cost REAL,
                savings_amount REAL,
                cumulative_savings REAL,
                confidence_level REAL,
                FOREIGN KEY (change_id) REFERENCES setting_changes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def detect_setting_changes(self) -> List[Dict[str, Any]]:
        """設定変更検知メイン機能"""
        try:
            detected_changes = []
            current_time = datetime.now()
            
            # Modbusから現在の設定値取得
            current_values = self._read_current_settings()
            
            if not current_values:
                return []
            
            # 前回値との比較
            if self.current_settings:
                for param_id, param_info in self.monitored_parameters.items():
                    old_value = self.current_settings.get(param_id)
                    new_value = current_values.get(param_id)
                    
                    if old_value is not None and new_value != old_value:
                        # 変更検知！
                        change_record = {
                            "timestamp": current_time.isoformat(),
                            "parameter_id": param_id,
                            "parameter_name": param_info["name"],
                            "old_value": old_value,
                            "new_value": new_value,
                            "unit": param_info["unit"],
                            "change_source": self._determine_change_source(param_id, old_value, new_value),
                            "weather_condition": self._get_current_weather(),
                            "season": self._get_current_season()
                        }
                        
                        detected_changes.append(change_record)
                        
                        # データベースに記録
                        self._record_setting_change(change_record)
                        
                        print(f"🔍 設定変更検知: {param_info['name']} {old_value}{param_info['unit']} → {new_value}{param_info['unit']}")
            
            # 現在値を保存
            self.current_settings = current_values
            self.last_check_time = current_time
            
            return detected_changes
            
        except Exception as e:
            print(f"❌ 設定変更検知エラー: {e}")
            return []
    
    def _read_current_settings(self) -> Dict[str, int]:
        """Modbusから現在設定読み取り"""
        try:
            # 実装では実際のModbus通信を使用
            # ここではデモ用の値を生成
            import random
            
            # 前回値がある場合は小幅変動、ない場合は初期値
            if self.current_settings:
                return {
                    param_id: self.current_settings.get(param_id, 50) + random.randint(-1, 1)
                    for param_id in self.monitored_parameters.keys()
                }
            else:
                # 初期値設定
                return {
                    "ID07": 35,  # 充電電流
                    "ID10": 30,  # 充電時間
                    "ID62": 35,  # 出力SOC
                    "ID40": 23,  # 充電開始時間
                    "ID41": 3,   # 充電終了時間
                    "ID28": 48   # 低電圧保護
                }
                
        except Exception as e:
            print(f"❌ Modbus読み取りエラー: {e}")
            return {}
    
    def _determine_change_source(self, param_id: str, old_value: int, new_value: int) -> str:
        """変更ソース判定"""
        # ML推奨値との比較で自動/手動を判定
        # 実装では現在のML推奨値と比較
        
        # 簡易判定ロジック
        if abs(new_value - old_value) == 1:
            return "fine_tuning"  # 微調整
        elif abs(new_value - old_value) >= 10:
            return "manual_major"  # 大幅手動変更
        else:
            return "manual_minor"  # 小幅手動変更
    
    def _record_setting_change(self, change_record: Dict[str, Any]):
        """設定変更をデータベースに記録"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO setting_changes 
                (timestamp, parameter_id, old_value, new_value, change_source, weather_condition, season)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                change_record["timestamp"],
                change_record["parameter_id"],
                change_record["old_value"],
                change_record["new_value"],
                change_record["change_source"],
                change_record["weather_condition"],
                change_record["season"]
            ))
            
            conn.commit()
            conn.close()
            
            print(f"📝 設定変更記録保存: {change_record['parameter_id']}")
            
        except Exception as e:
            print(f"❌ 設定変更記録エラー: {e}")
    
    def calculate_savings_effect(self, days_back: int = 30) -> Dict[str, Any]:
        """削減効果計算"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 過去30日の設定変更取得
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            cursor.execute('''
                SELECT * FROM setting_changes 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC
            ''', (cutoff_date,))
            
            changes = cursor.fetchall()
            
            if not changes:
                return {"status": "no_changes", "total_savings": 0}
            
            # 各変更の効果を計算
            total_savings = 0
            change_effects = []
            
            for change in changes:
                effect = self._calculate_single_change_effect(change)
                change_effects.append(effect)
                total_savings += effect["savings_amount"]
            
            # 累積削減額更新
            cumulative_savings = self._update_cumulative_savings(total_savings)
            
            conn.close()
            
            return {
                "status": "calculated",
                "period_days": days_back,
                "total_changes": len(changes),
                "period_savings": total_savings,
                "cumulative_savings": cumulative_savings,
                "change_effects": change_effects,
                "average_daily_savings": total_savings / days_back
            }
            
        except Exception as e:
            print(f"❌ 削減効果計算エラー: {e}")
            return {"status": "error", "total_savings": 0}
    
    def _calculate_single_change_effect(self, change_record) -> Dict[str, Any]:
        """単一変更の効果計算"""
        try:
            # 実装では変更前後の実際の電力データを比較
            # ここではデモ用の効果計算
            
            timestamp, param_id, old_value, new_value, change_source = change_record[1:6]
            
            # パラメーター別効果係数
            effect_coefficients = {
                "ID07": 15,  # 充電電流: 1A変更で15円/日効果
                "ID10": 8,   # 充電時間: 1分変更で8円/日効果
                "ID62": 20,  # 出力SOC: 1%変更で20円/日効果
                "ID40": 5,   # 充電開始: 1時間変更で5円/日効果
                "ID41": 5,   # 充電終了: 1時間変更で5円/日効果
                "ID28": 3    # 低電圧保護: 1V変更で3円/日効果
            }
            
            coefficient = effect_coefficients.get(param_id, 10)
            value_change = abs(new_value - old_value)
            
            # 変更方向による効果補正
            if param_id in ["ID07", "ID10", "ID62"] and new_value < old_value:
                direction_multiplier = 1.2  # 削減方向は効果高
            else:
                direction_multiplier = 1.0
            
            daily_savings = coefficient * value_change * direction_multiplier
            
            return {
                "change_id": change_record[0],
                "parameter_id": param_id,
                "value_change": value_change,
                "daily_savings": daily_savings,
                "savings_amount": daily_savings * 7,  # 7日分として計算
                "confidence": 0.8
            }
            
        except Exception as e:
            print(f"❌ 単一変更効果計算エラー: {e}")
            return {"savings_amount": 0, "confidence": 0}
    
    def _update_cumulative_savings(self, additional_savings: float) -> float:
        """累積削減額更新"""
        try:
            conn = sqlite3.connect(self.savings_db_path)
            cursor = conn.cursor()
            
            # 累積削減額テーブル作成（存在しない場合）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cumulative_savings (
                    id INTEGER PRIMARY KEY,
                    total_savings REAL DEFAULT 0,
                    last_updated TEXT
                )
            ''')
            
            # 現在の累積額取得
            cursor.execute('SELECT total_savings FROM cumulative_savings WHERE id = 1')
            result = cursor.fetchone()
            
            if result:
                current_total = result[0]
            else:
                current_total = 0
                cursor.execute('INSERT INTO cumulative_savings (id, total_savings) VALUES (1, 0)')
            
            # 新しい累積額
            new_total = current_total + additional_savings
            
            # 更新
            cursor.execute('''
                UPDATE cumulative_savings 
                SET total_savings = ?, last_updated = ?
                WHERE id = 1
            ''', (new_total, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return new_total
            
        except Exception as e:
            print(f"❌ 累積削減額更新エラー: {e}")
            return 0
    
    def get_savings_visualization_data(self) -> Dict[str, Any]:
        """削減効果可視化データ取得"""
        try:
            # 期間別削減効果
            daily_effect = self.calculate_savings_effect(1)
            weekly_effect = self.calculate_savings_effect(7)
            monthly_effect = self.calculate_savings_effect(30)
            yearly_effect = self.calculate_savings_effect(365)
            
            # 貯金型表示データ
            cumulative_savings = self._get_cumulative_savings()
            
            # 進捗率計算
            yearly_target = 150000  # 15万円目標
            progress_rate = min(100, (cumulative_savings / yearly_target) * 100)
            
            visualization_data = {
                "cumulative_savings": {
                    "total": cumulative_savings,
                    "formatted": f"¥{cumulative_savings:,.0f}",
                    "progress_rate": progress_rate,
                    "target": yearly_target,
                    "remaining": max(0, yearly_target - cumulative_savings)
                },
                "period_savings": {
                    "daily": daily_effect.get("period_savings", 0),
                    "weekly": weekly_effect.get("period_savings", 0),
                    "monthly": monthly_effect.get("period_savings", 0),
                    "yearly_pace": yearly_effect.get("period_savings", 0)
                },
                "change_statistics": {
                    "daily_changes": daily_effect.get("total_changes", 0),
                    "weekly_changes": weekly_effect.get("total_changes", 0),
                    "monthly_changes": monthly_effect.get("total_changes", 0)
                },
                "savings_trend": self._calculate_savings_trend(),
                "achievement_level": self._get_achievement_level(cumulative_savings)
            }
            
            return visualization_data
            
        except Exception as e:
            print(f"❌ 可視化データ取得エラー: {e}")
            return {}
    
    def _get_cumulative_savings(self) -> float:
        """累積削減額取得"""
        try:
            conn = sqlite3.connect(self.savings_db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT total_savings FROM cumulative_savings WHERE id = 1')
            result = cursor.fetchone()
            
            conn.close()
            
            return result[0] if result else 0
            
        except Exception:
            return 0
    
    def _calculate_savings_trend(self) -> List[Dict[str, Any]]:
        """削減トレンド計算"""
        # 過去12ヶ月の月別削減額を計算
        trend_data = []
        
        for i in range(12):
            month_start = datetime.now() - timedelta(days=30*(i+1))
            month_savings = self.calculate_savings_effect(30)
            
            trend_data.append({
                "month": month_start.strftime("%Y-%m"),
                "savings": month_savings.get("period_savings", 0)
            })
        
        return list(reversed(trend_data))
    
    def _get_achievement_level(self, cumulative_savings: float) -> Dict[str, Any]:
        """達成レベル判定"""
        levels = [
            {"threshold": 0, "level": "スタート", "emoji": "🌱", "next_target": 50000},
            {"threshold": 50000, "level": "ブロンズ", "emoji": "🥉", "next_target": 100000},
            {"threshold": 100000, "level": "シルバー", "emoji": "🥈", "next_target": 150000},
            {"threshold": 150000, "level": "ゴールド", "emoji": "🥇", "next_target": 200000},
            {"threshold": 200000, "level": "プラチナ", "emoji": "💎", "next_target": 300000},
            {"threshold": 300000, "level": "レジェンド", "emoji": "👑", "next_target": None}
        ]
        
        current_level = levels[0]
        for level in levels:
            if cumulative_savings >= level["threshold"]:
                current_level = level
            else:
                break
        
        return current_level
    
    def _get_current_weather(self) -> str:
        """現在の天気取得"""
        # 実装では天気APIから取得
        return "晴れ"
    
    def _get_current_season(self) -> str:
        """現在の季節取得"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"


def main():
    """設定変更検知システムテスト"""
    print("🔍 HANAZONO Setting Change Detection System テスト")
    print("=" * 60)
    
    detector = SettingChangeDetector()
    
    # 設定変更検知テスト
    print("🔍 設定変更検知テスト:")
    changes = detector.detect_setting_changes()
    print(f"検知された変更: {len(changes)}件")
    
    # 2回目実行（変更検知テスト）
    print("\n🔄 2回目実行（変更あり想定）:")
    changes = detector.detect_setting_changes()
    if changes:
        for change in changes:
            print(f"  変更: {change['parameter_name']} {change['old_value']}{change['unit']} → {change['new_value']}{change['unit']}")
    
    # 削減効果計算テスト
    print("\n💰 削減効果計算テスト:")
    savings = detector.calculate_savings_effect(30)
    print(f"30日間削減効果: ¥{savings.get('period_savings', 0):,.0f}")
    print(f"累積削減額: ¥{savings.get('cumulative_savings', 0):,.0f}")
    
    # 可視化データテスト
    print("\n📊 可視化データテスト:")
    viz_data = detector.get_savings_visualization_data()
    if viz_data:
        cumulative = viz_data["cumulative_savings"]
        achievement = viz_data["achievement_level"]
        print(f"貯金額: {cumulative['formatted']}")
        print(f"進捗率: {cumulative['progress_rate']:.1f}%")
        print(f"達成レベル: {achievement['emoji']} {achievement['level']}")
    
    print("\n✅ 設定変更検知システムテスト完了")


if __name__ == "__main__":
    main()
