#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム 革新的5段階バトルシステム v1.0
6年間の進化を5段階に分けた史上最強のゲーミフィケーション

Battle Types:
1. 🥉 Historic Battle: 過去vs過去（改善努力効果）
2. 🥈 Evolution Battle: フェーズ間比較（時代変化効果）
3. 🥇 Optimization Battle: 同フェーズ内最適化
4. 💎 Ultimate Battle: HANAZONOシステム効果
5. 🏆 Legendary Battle: 全期間統合バトル
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

class RevolutionaryBattleSystem:
    """革新的5段階バトルシステム"""
    
    def __init__(self, db_path="data/comprehensive_electric_data.db"):
        self.db_path = db_path
        self.logger = self.setup_logger()
        
        # バトルタイプ定義
        self.battle_types = {
            "historic": {
                "name": "🥉 Historic Battle",
                "description": "過去同士の比較（人間の改善努力効果）",
                "emoji": "🥉",
                "difficulty": 1
            },
            "evolution": {
                "name": "🥈 Evolution Battle", 
                "description": "フェーズ間変化（時代・環境変化効果）",
                "emoji": "🥈",
                "difficulty": 2
            },
            "optimization": {
                "name": "🥇 Optimization Battle",
                "description": "同フェーズ内最適化（学習効果）",
                "emoji": "🥇", 
                "difficulty": 3
            },
            "ultimate": {
                "name": "💎 Ultimate Battle",
                "description": "HANAZONOシステム効果（技術革新効果）",
                "emoji": "💎",
                "difficulty": 4
            },
            "legendary": {
                "name": "🏆 Legendary Battle",
                "description": "全期間統合バトル（総合進化効果）",
                "emoji": "🏆",
                "difficulty": 5
            }
        }
        
        # 実績システム定義
        self.achievements = {
            "first_victory": {"name": "初勝利", "description": "初めてのバトル勝利", "emoji": "🎉"},
            "winning_streak_5": {"name": "連勝記録", "description": "5連勝達成", "emoji": "🔥"},
            "phase_conqueror": {"name": "フェーズ制覇", "description": "全フェーズで勝利", "emoji": "👑"},
            "efficiency_master": {"name": "効率マスター", "description": "50%以上削減達成", "emoji": "⚡"},
            "legendary_champion": {"name": "伝説のチャンピオン", "description": "全バトルタイプで勝利", "emoji": "🌟"},
            "diamond_achiever": {"name": "ダイヤモンド到達", "description": "ダイヤモンドランク到達", "emoji": "💎"},
            "hanazono_hero": {"name": "HANAZONOヒーロー", "description": "年間¥50,000削減達成", "emoji": "🦸"}
        }
    
    def setup_logger(self):
        """ロガー設定"""
        logger = logging.getLogger('RevolutionaryBattleSystem')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('logs/battle_system.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def historic_battle(self, year1: int, month1: int, year2: int, month2: int) -> Dict:
        """🥉 Historic Battle: 過去同士の比較"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 両方のデータを取得
            cursor.execute('''
                SELECT usage_kwh, cost_yen, phase FROM comprehensive_monthly
                WHERE year = ? AND month = ?
            ''', (year1, month1))
            data1 = cursor.fetchone()
            
            cursor.execute('''
                SELECT usage_kwh, cost_yen, phase FROM comprehensive_monthly  
                WHERE year = ? AND month = ?
            ''', (year2, month2))
            data2 = cursor.fetchone()
            
            if not data1 or not data2:
                return {"error": "データが不足しています"}
            
            usage1, cost1, phase1 = data1
            usage2, cost2, phase2 = data2
            
            # バトル結果計算
            usage_improvement = ((usage1 - usage2) / usage1) * 100
            cost_improvement = ((cost1 - cost2) / cost1) * 100 if cost1 and cost2 else 0
            
            winner = "期間2" if usage_improvement > 0 else "期間1"
            
            return {
                "battle_type": "historic",
                "period1": f"{year1}年{month1}月 ({phase1}期)",
                "period2": f"{year2}年{month2}月 ({phase2}期)",
                "usage1": usage1,
                "usage2": usage2,
                "cost1": cost1,
                "cost2": cost2,
                "usage_improvement": usage_improvement,
                "cost_improvement": cost_improvement,
                "winner": winner,
                "result_emoji": "🏆" if usage_improvement > 0 else "💔",
                "battle_summary": f"{year1}年{month1}月 vs {year2}年{month2}月: {abs(usage_improvement):.1f}%{'改善' if usage_improvement > 0 else '悪化'}"
            }
    
    def evolution_battle(self, phase1: str, phase2: str) -> Dict:
        """🥈 Evolution Battle: フェーズ間比較"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 各フェーズの平均データを取得
            cursor.execute('''
                SELECT AVG(usage_kwh), AVG(cost_yen), COUNT(*) FROM comprehensive_monthly
                WHERE phase = ? AND usage_kwh > 0
            ''', (phase1,))
            data1 = cursor.fetchone()
            
            cursor.execute('''
                SELECT AVG(usage_kwh), AVG(cost_yen), COUNT(*) FROM comprehensive_monthly
                WHERE phase = ? AND usage_kwh > 0  
            ''', (phase2,))
            data2 = cursor.fetchone()
            
            if not data1[0] or not data2[0]:
                return {"error": "フェーズデータが不足しています"}
            
            avg_usage1, avg_cost1, months1 = data1
            avg_usage2, avg_cost2, months2 = data2
            
            # 改善率計算
            usage_evolution = ((avg_usage1 - avg_usage2) / avg_usage1) * 100
            cost_evolution = ((avg_cost1 - avg_cost2) / avg_cost1) * 100 if avg_cost1 and avg_cost2 else 0
            
            return {
                "battle_type": "evolution",
                "phase1": phase1,
                "phase2": phase2,
                "avg_usage1": avg_usage1,
                "avg_usage2": avg_usage2,
                "avg_cost1": avg_cost1,
                "avg_cost2": avg_cost2,
                "months1": months1,
                "months2": months2,
                "usage_evolution": usage_evolution,
                "cost_evolution": cost_evolution,
                "winner": phase2 if usage_evolution > 0 else phase1,
                "evolution_summary": f"{phase1}期 → {phase2}期: {abs(usage_evolution):.1f}%{'進化' if usage_evolution > 0 else '退化'}"
            }
    
    def ultimate_battle(self, year: int, month: int) -> Dict:
        """💎 Ultimate Battle: HANAZONOシステム効果"""
        # 前年同月との比較（HANAZONOシステム効果）
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # HANAZONOシステム導入後データ
            cursor.execute('''
                SELECT usage_kwh, cost_yen FROM comprehensive_monthly
                WHERE year = ? AND month = ? AND phase = 'hanazono'
            ''', (year, month))
            hanazono_data = cursor.fetchone()
            
            # 前年同月データ（pre_hanazono期）
            cursor.execute('''
                SELECT usage_kwh, cost_yen FROM comprehensive_monthly
                WHERE year = ? AND month = ? AND phase != 'hanazono'
                ORDER BY year DESC LIMIT 1
            ''', (year - 1, month))
            pre_data = cursor.fetchone()
            
            if not hanazono_data or not pre_data:
                return {"error": "比較データが不足しています"}
            
            hanazono_usage, hanazono_cost = hanazono_data
            pre_usage, pre_cost = pre_data
            
            # HANAZONOシステム効果計算
            hanazono_effect = ((pre_usage - hanazono_usage) / pre_usage) * 100
            cost_effect = ((pre_cost - hanazono_cost) / pre_cost) * 100 if pre_cost and hanazono_cost else 0
            
            # ランク判定
            if hanazono_effect >= 50:
                rank = "💎 ダイヤモンド"
            elif hanazono_effect >= 35:
                rank = "🏆 プラチナ"
            elif hanazono_effect >= 25:
                rank = "🥇 ゴールド"
            elif hanazono_effect >= 15:
                rank = "🥈 シルバー"
            elif hanazono_effect >= 5:
                rank = "🥉 ブロンズ"
            else:
                rank = "📉 チャレンジ"
            
            return {
                "battle_type": "ultimate",
                "hanazono_usage": hanazono_usage,
                "pre_usage": pre_usage,
                "hanazono_cost": hanazono_cost,
                "pre_cost": pre_cost,
                "hanazono_effect": hanazono_effect,
                "cost_effect": cost_effect,
                "rank": rank,
                "victory": hanazono_effect > 0,
                "ultimate_summary": f"HANAZONOシステム効果: {hanazono_effect:.1f}%削減 ({rank})"
            }
    
    def legendary_battle(self) -> Dict:
        """🏆 Legendary Battle: 全期間統合バトル"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 全フェーズの統計を取得
            cursor.execute('''
                SELECT phase, 
                       AVG(usage_kwh) as avg_usage,
                       AVG(cost_yen) as avg_cost,
                       COUNT(*) as months,
                       MIN(year) as start_year,
                       MAX(year) as end_year
                FROM comprehensive_monthly 
                WHERE usage_kwh > 0
                GROUP BY phase
                ORDER BY MIN(year), MIN(month)
            ''', ())
            
            phases_data = cursor.fetchall()
            
            if len(phases_data) < 2:
                return {"error": "比較可能なフェーズが不足しています"}
            
            # 最初のフェーズと最新のフェーズを比較
            first_phase = phases_data[0]
            latest_phase = phases_data[-1]
            
            first_usage = first_phase[1]
            latest_usage = latest_phase[1]
            
            # 全期間進化率
            total_evolution = ((first_usage - latest_usage) / first_usage) * 100
            
            # 各フェーズの改善率を計算
            phase_improvements = []
            for i in range(1, len(phases_data)):
                prev_usage = phases_data[i-1][1]
                curr_usage = phases_data[i][1]
                improvement = ((prev_usage - curr_usage) / prev_usage) * 100
                phase_improvements.append({
                    "from_phase": phases_data[i-1][0],
                    "to_phase": phases_data[i][0],
                    "improvement": improvement
                })
            
            # 伝説ランク判定
            if total_evolution >= 40:
                legendary_rank = "🌟 レジェンド"
            elif total_evolution >= 30:
                legendary_rank = "💎 マスター"
            elif total_evolution >= 20:
                legendary_rank = "🏆 エキスパート"
            elif total_evolution >= 10:
                legendary_rank = "🥇 アドバンス"
            else:
                legendary_rank = "🥈 ビギナー"
            
            return {
                "battle_type": "legendary",
                "analysis_period": f"{first_phase[4]}年〜{latest_phase[5]}年",
                "total_phases": len(phases_data),
                "first_phase_usage": first_usage,
                "latest_phase_usage": latest_usage,
                "total_evolution": total_evolution,
                "phase_improvements": phase_improvements,
                "legendary_rank": legendary_rank,
                "legendary_summary": f"6年間の総合進化: {total_evolution:.1f}%改善 ({legendary_rank})"
            }
    
    def generate_battle_report(self, year: int, month: int) -> str:
        """総合バトルレポート生成"""
        report = f"# 🏆 {year}年{month}月 革新的5段階バトルレポート\n\n"
        
        # 1. Historic Battle (前年同月)
        historic = self.historic_battle(year-1, month, year, month)
        if "error" not in historic:
            report += f"## {self.battle_types['historic']['emoji']} Historic Battle\n"
            report += f"**{historic['battle_summary']}**\n"
            report += f"結果: {historic['result_emoji']} {historic['winner']}の勝利\n\n"
        
        # 2. Ultimate Battle (HANAZONOシステム効果)
        ultimate = self.ultimate_battle(year, month)
        if "error" not in ultimate:
            report += f"## {self.battle_types['ultimate']['emoji']} Ultimate Battle\n"
            report += f"**{ultimate['ultimate_summary']}**\n"
            report += f"勝利: {'✅' if ultimate['victory'] else '❌'}\n\n"
        
        # 3. Legendary Battle (全期間統合)
        legendary = self.legendary_battle()
        if "error" not in legendary:
            report += f"## {self.battle_types['legendary']['emoji']} Legendary Battle\n"
            report += f"**{legendary['legendary_summary']}**\n"
            report += f"分析期間: {legendary['analysis_period']}\n\n"
        
        return report
    
    def get_current_achievements(self) -> List[Dict]:
        """現在の実績を取得"""
        # 実績判定ロジック（簡略版）
        achievements = []
        
        # Legendary Battleの結果から実績判定
        legendary = self.legendary_battle()
        if "error" not in legendary:
            if legendary["total_evolution"] >= 50:
                achievements.append(self.achievements["efficiency_master"])
            if legendary["legendary_rank"] == "🌟 レジェンド":
                achievements.append(self.achievements["legendary_champion"])
        
        return achievements

def main():
    """メイン処理"""
    battle_system = RevolutionaryBattleSystem()
    
    print("🔥 革新的5段階バトルシステム起動！")
    print("==========================================")
    
    # 現在の月でバトルレポート生成
    now = datetime.now()
    report = battle_system.generate_battle_report(now.year, now.month)
    print(report)
    
    # 実績確認
    achievements = battle_system.get_current_achievements()
    if achievements:
        print("🏅 獲得実績:")
        for achievement in achievements:
            print(f"  {achievement['emoji']} {achievement['name']}: {achievement['description']}")
    
    print("\n✅ 革新的5段階バトルシステム準備完了！")

if __name__ == "__main__":
    main()
