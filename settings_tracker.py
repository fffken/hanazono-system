#!/usr/bin/env python3
"""
設定変更履歴追跡システム v1.0
HANAZONO ソーラー蓄電システム用
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

class SettingsTracker:
    def __init__(self, db_path="data/settings_history.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベース初期化"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                change_type TEXT NOT NULL,
                reason TEXT,
                weather_condition TEXT,
                season TEXT,
                temperature REAL,
                previous_settings TEXT,
                new_settings TEXT,
                expected_benefit TEXT,
                actual_benefit REAL,
                changed_by TEXT DEFAULT 'user'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_change(self, previous_settings, new_settings, reason, weather_condition=None):
        """設定変更を記録"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 現在の季節を判定
        month = datetime.now().month
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "autumn"
        
        cursor.execute('''
            INSERT INTO settings_history 
            (timestamp, change_type, reason, weather_condition, season, 
             previous_settings, new_settings, expected_benefit, changed_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            "manual",
            reason,
            weather_condition,
            season,
            json.dumps(previous_settings),
            json.dumps(new_settings),
            "設定最適化による電気代削減",
            "user"
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 設定変更を記録しました: {reason}")
    
    def get_recent_changes(self, days=7):
        """最近の変更履歴を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM settings_history 
            WHERE datetime(timestamp) > datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days))
        
        results = cursor.fetchall()
        conn.close()
        return results

if __name__ == "__main__":
    tracker = SettingsTracker()
    print("✅ 設定変更履歴システム初期化完了")
