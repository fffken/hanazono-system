"""
AI学習データベースシステム v1.0
人間 vs AI対戦の実績データを蓄積・分析
"""
import sqlite3
import json
import datetime
from typing import Dict, Any, Optional

class AILearningDatabase:

    def __init__(self, db_path='data/ai_learning.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            CREATE TABLE IF NOT EXISTS battle_records (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                date TEXT NOT NULL,\n                timestamp TEXT NOT NULL,\n                weather_condition TEXT,\n                season TEXT,\n                human_id07 INTEGER,\n                human_id10 INTEGER,\n                human_id62 INTEGER,\n                human_reason TEXT,\n                ai_id07 INTEGER,\n                ai_id10 INTEGER,\n                ai_id62 INTEGER,\n                ai_reason TEXT,\n                ai_confidence REAL,\n                adopted_setting TEXT,\n                actual_savings REAL,\n                battery_efficiency REAL,\n                weather_accuracy REAL,\n                winner TEXT,\n                created_at TEXT DEFAULT CURRENT_TIMESTAMP\n            )\n        ')
        cursor.execute('\n            CREATE TABLE IF NOT EXISTS learning_data (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                weather_pattern TEXT,\n                season_type TEXT,\n                optimal_id07 INTEGER,\n                optimal_id10 INTEGER,\n                optimal_id62 INTEGER,\n                success_rate REAL,\n                avg_savings REAL,\n                confidence_level REAL,\n                sample_count INTEGER,\n                last_updated TEXT DEFAULT CURRENT_TIMESTAMP\n            )\n        ')
        conn.commit()
        conn.close()

    def record_battle(self, battle_data: Dict[str, Any]):
        """対戦記録を保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO battle_records (\n                date, timestamp, weather_condition, season,\n                human_id07, human_id10, human_id62, human_reason,\n                ai_id07, ai_id10, ai_id62, ai_reason, ai_confidence,\n                adopted_setting, actual_savings, battery_efficiency,\n                weather_accuracy, winner\n            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n        ', (battle_data.get('date'), battle_data.get('timestamp'), battle_data.get('weather_condition'), battle_data.get('season'), battle_data.get('human_id07'), battle_data.get('human_id10'), battle_data.get('human_id62'), battle_data.get('human_reason'), battle_data.get('ai_id07'), battle_data.get('ai_id10'), battle_data.get('ai_id62'), battle_data.get('ai_reason'), battle_data.get('ai_confidence'), battle_data.get('adopted_setting'), battle_data.get('actual_savings'), battle_data.get('battery_efficiency'), battle_data.get('weather_accuracy'), battle_data.get('winner')))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_battle_statistics(self):
        """対戦統計を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM battle_records')
        total_battles = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "human"')
        human_wins = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "ai"')
        ai_wins = cursor.fetchone()[0]
        human_win_rate = human_wins / total_battles * 100 if total_battles > 0 else 0
        ai_win_rate = ai_wins / total_battles * 100 if total_battles > 0 else 0
        cursor.execute('SELECT AVG(actual_savings) FROM battle_records')
        avg_savings = cursor.fetchone()[0] or 0
        conn.close()
        return {'total_battles': total_battles, 'human_wins': human_wins, 'ai_wins': ai_wins, 'human_win_rate': round(human_win_rate, 1), 'ai_win_rate': round(ai_win_rate, 1), 'avg_savings': int(round(avg_savings, 0))}

    def get_recent_battles(self, limit=5):
        """最近の対戦記録を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            SELECT date, weather_condition, human_id07, human_id10, human_id62,\n                   ai_id07, ai_id10, ai_id62, winner, actual_savings\n            FROM battle_records\n            ORDER BY id DESC LIMIT ?\n        ', (limit,))
        battles = cursor.fetchall()
        conn.close()
        return battles

    def get_battle_statistics(self):
        """対戦統計を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM battle_records')
        total_battles = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "human"')
        human_wins = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "ai"')
        ai_wins = cursor.fetchone()[0]
        human_win_rate = human_wins / total_battles * 100 if total_battles > 0 else 0
        ai_win_rate = ai_wins / total_battles * 100 if total_battles > 0 else 0
        cursor.execute('SELECT AVG(actual_savings) FROM battle_records')
        avg_savings = cursor.fetchone()[0] or 0
        conn.close()
        return {'total_battles': total_battles, 'human_wins': human_wins, 'ai_wins': ai_wins, 'human_win_rate': round(human_win_rate, 1), 'ai_win_rate': round(ai_win_rate, 1), 'avg_savings': int(round(avg_savings, 0))}

    def get_recent_battles(self, limit=5):
        """最近の対戦記録を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            SELECT date, weather_condition, human_id07, human_id10, human_id62,\n                   ai_id07, ai_id10, ai_id62, winner, actual_savings\n            FROM battle_records\n            ORDER BY id DESC LIMIT ?\n        ', (limit,))
        battles = cursor.fetchall()
        conn.close()
        return battles