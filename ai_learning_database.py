"""
AI学習データベースシステム v1.0
人間 vs AI対戦の実績データを蓄積・分析
"""

import sqlite3
import json
import datetime
from typing import Dict, Any, Optional

class AILearningDatabase:
    def __init__(self, db_path="data/ai_learning.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 対戦記録テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battle_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                weather_condition TEXT,
                season TEXT,
                human_id07 INTEGER,
                human_id10 INTEGER,
                human_id62 INTEGER,
                human_reason TEXT,
                ai_id07 INTEGER,
                ai_id10 INTEGER,
                ai_id62 INTEGER,
                ai_reason TEXT,
                ai_confidence REAL,
                adopted_setting TEXT,
                actual_savings REAL,
                battery_efficiency REAL,
                weather_accuracy REAL,
                winner TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 学習データテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weather_pattern TEXT,
                season_type TEXT,
                optimal_id07 INTEGER,
                optimal_id10 INTEGER,
                optimal_id62 INTEGER,
                success_rate REAL,
                avg_savings REAL,
                confidence_level REAL,
                sample_count INTEGER,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_battle(self, battle_data: Dict[str, Any]):
        """対戦記録を保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO battle_records (
                date, timestamp, weather_condition, season,
                human_id07, human_id10, human_id62, human_reason,
                ai_id07, ai_id10, ai_id62, ai_reason, ai_confidence,
                adopted_setting, actual_savings, battery_efficiency,
                weather_accuracy, winner
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            battle_data.get('date'),
            battle_data.get('timestamp'),
            battle_data.get('weather_condition'),
            battle_data.get('season'),
            battle_data.get('human_id07'),
            battle_data.get('human_id10'),
            battle_data.get('human_id62'),
            battle_data.get('human_reason'),
            battle_data.get('ai_id07'),
            battle_data.get('ai_id10'),
            battle_data.get('ai_id62'),
            battle_data.get('ai_reason'),
            battle_data.get('ai_confidence'),
            battle_data.get('adopted_setting'),
            battle_data.get('actual_savings'),
            battle_data.get('battery_efficiency'),
            battle_data.get('weather_accuracy'),
            battle_data.get('winner')
        ))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_battle_statistics(self):
        """対戦統計を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 基本統計
        cursor.execute('SELECT COUNT(*) FROM battle_records')
        total_battles = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "human"')
        human_wins = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM battle_records WHERE winner = "ai"')
        ai_wins = cursor.fetchone()[0]
        
        # 勝率計算
        human_win_rate = (human_wins / total_battles * 100) if total_battles > 0 else 0
        ai_win_rate = (ai_wins / total_battles * 100) if total_battles > 0 else 0
        
        # 平均節約額
        cursor.execute('SELECT AVG(actual_savings) FROM battle_records')
        avg_savings = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_battles': total_battles,
            'human_wins': human_wins,
            'ai_wins': ai_wins,
            'human_win_rate': round(human_win_rate, 1),
            'ai_win_rate': round(ai_win_rate, 1),
            'avg_savings': int(round(avg_savings, 0))
        }

    def get_recent_battles(self, limit=5):
        """最近の対戦記録を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, weather_condition, human_id07, human_id10, human_id62,
                   ai_id07, ai_id10, ai_id62, winner, actual_savings
            FROM battle_records 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        
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
        
        human_win_rate = (human_wins / total_battles * 100) if total_battles > 0 else 0
        ai_win_rate = (ai_wins / total_battles * 100) if total_battles > 0 else 0
        
        cursor.execute('SELECT AVG(actual_savings) FROM battle_records')
        avg_savings = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_battles': total_battles, 'human_wins': human_wins, 'ai_wins': ai_wins,
            'human_win_rate': round(human_win_rate, 1), 'ai_win_rate': round(ai_win_rate, 1),
            'avg_savings': int(round(avg_savings, 0))
        }

    def get_recent_battles(self, limit=5):
        """最近の対戦記録を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, weather_condition, human_id07, human_id10, human_id62,
                   ai_id07, ai_id10, ai_id62, winner, actual_savings
            FROM battle_records 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        
        battles = cursor.fetchall()
        conn.close()
        return battles
