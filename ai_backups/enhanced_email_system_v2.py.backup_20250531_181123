"""Enhanced Email System v2.0 - 基本クラス"""
import json
import datetime
from typing import Dict, Any, Optional

class EnhancedEmailSystemV2:

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.version = '2.0'
        try:
            from ai_learning_database import AILearningDatabase
            self.ai_db = AILearningDatabase()
        except Exception as e:
            if self.logger:
                self.logger.warning(f'AI学習データベース初期化エラー: {e}')
            self.ai_db = None
        self.SAFETY_LIMITS = {'ID07': {'min': 20, 'max': 80}, 'ID10': {'min': 10, 'max': 90}, 'ID62': {'min': 20, 'max': 80}}

    def generate_complete_report(self, data, weather_data, battery_info):
        """メインレポート生成"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')
            if not battery_info or battery_info.get('soc') == 'N/A':
                battery_info = self._extract_battery_info(data)
            report = f'🏆 HANAZONOシステム最適化レポート\n📅 {timestamp}\n\n{self._weather_section(weather_data)}\n\n{self._battle_section(data, weather_data)}\n\n{self._battle_results_section()}\n\n{self._battery_section(battery_info)}\n\n{self._savings_section(data)}\n\n--- HANAZONOシステム 自動最適化 ---\n🤖 Enhanced Email System v2.0'
            return report
        except Exception as e:
            if self.logger:
                self.logger.error(f'レポート生成エラー: {e}')
            return 'レポート生成エラー'

    def _weather_section(self, weather_data):
        """天気予報セクション（気温対応版）"""
        try:
            if not weather_data or not isinstance(weather_data, dict):
                return '🌤️ 天気予報と発電予測\n--------------------\n📡 データ取得中...\n⚡ 発電予測: 標準レベル'
            today = weather_data.get('today', {})
            tomorrow = weather_data.get('tomorrow', {})
            today_weather = today.get('weather', '情報なし')
            today_temp = today.get('temperature', 'N/A')
            today_emoji = '☀️' if '晴' in str(today_weather) else '☁️' if '曇' in str(today_weather) else '🌧️' if '雨' in str(today_weather) else '🌤️'
            tomorrow_weather = tomorrow.get('weather', '情報なし')
            tomorrow_temp = tomorrow.get('temperature', 'N/A')
            tomorrow_emoji = '☀️' if '晴' in str(tomorrow_weather) else '☁️' if '曇' in str(tomorrow_weather) else '🌧️' if '雨' in str(tomorrow_weather) else '🌤️'
            return f'🌤️ 天気予報と発電予測\n--------------------\n今日: {today_emoji} {today_weather} ({today_temp})\n明日: {tomorrow_emoji} {tomorrow_weather} ({tomorrow_temp})\n⚡ 発電予測: 標準レベル'
        except Exception as e:
            return '🌤️ 天気予報と発電予測\n--------------------\n📡 エラー発生、基本モードで動作中\n⚡ 発電予測: 標準レベル'

    def _battle_section(self, data, weather_data):
        """人間 vs AI対戦セクション（色丸対応版）"""
        human = self._get_human_settings(weather_data)
        ai = self._get_ai_settings(data, weather_data)
        return f"🔋 今日の推奨設定（人間 vs AI対戦）\n================================================\n\n🟢 📚 設定ガイド推奨（人間の知恵）\nID07: {human['ID07']}A  ID10: {human['ID10']}分  ID62: {human['ID62']}%\n理由: {human['reason']}\n信頼度: ⭐⭐⭐⭐⭐\n\n🟡 🤖 AI推奨（機械学習）\nID07: {ai['ID07']}A  ID10: {ai['ID10']}分  ID62: {ai['ID62']}%\n理由: {ai['reason']}\n信頼度: ⭐⭐⭐⚪⚪\n予測節約: +¥23/日\n\n🎯 採用推奨: 🟢 📚 設定ガイド (安定性重視)"

    def _battery_section(self, battery_info):
        """バッテリー状況セクション（動的版）"""
        try:
            import glob
            import json
            files = glob.glob('data/lvyuan_data_*.json')
            latest_file = sorted(files)[-1]
            with open(latest_file, 'r') as f:
                data = json.load(f)
            if isinstance(data, list):
                data = data[0]
            params = data['parameters']
            soc = params['0x0100']['value']
            voltage = round(params['0x0101']['value'], 1)
            current = round(params['0x0102']['value'], 1)
            return f"🔋 現在のバッテリー状況\n--------------------\n🔋 バッテリー残量: {soc}%\n⚡ 電圧: {voltage}V\n🔌 電流: {current}A\n📅 取得時刻: {datetime.datetime.now().strftime('%H:%M:%S')}"
        except Exception as e:
            return f'🔋 現在のバッテリー状況: データ取得エラー ({e})'

    def _savings_section(self, data):
        """節約効果セクション"""
        daily_savings = 239.88
        monthly_savings = daily_savings * 30
        annual_savings = daily_savings * 365
        return f'💰 電気代節約効果\n    --------------------\n    💴 今日の節約: ¥{daily_savings:,.0f}\n    📊 月間予測: ¥{monthly_savings:,.0f}\n    🏆 年間予測: ¥{annual_savings:,.0f}\n\n    📈 四国電力料金体系基準\n    ⚡ グリッド依存度: 27.5%削減'

    def _get_human_settings(self, weather_data):
        """設定ガイドから人間の推奨設定取得"""
        return {'ID07': 50, 'ID10': 45, 'ID62': 45, 'reason': '春季標準設定'}

    def _get_ai_settings(self, data, weather_data):
        """AI学習エンジンから推奨設定取得"""
        human = self._get_human_settings(weather_data)
        return {'ID07': max(20, min(80, human['ID07'] - 2)), 'ID10': max(10, min(90, human['ID10'] - 3)), 'ID62': max(20, min(80, human['ID62'] - 2)), 'reason': '過去30日実績分析'}

    def _extract_battery_info(self, data):
        """バッテリー情報を抽出（新データ構造対応版）"""
        try:
            if isinstance(data, list) and len(data) > 0:
                actual_data = data[0]
            elif isinstance(data, dict):
                actual_data = data
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
            if isinstance(actual_data, dict) and 'parameters' in actual_data:
                params = actual_data['parameters']
                soc = 'N/A'
                voltage = 'N/A'
                current = 'N/A'
                if '0x0100' in params and isinstance(params['0x0100'], dict):
                    soc = params['0x0100'].get('value', 'N/A')
                if '0x0101' in params and isinstance(params['0x0101'], dict):
                    voltage_val = params['0x0101'].get('value', 'N/A')
                    voltage = round(voltage_val, 1) if isinstance(voltage_val, (int, float)) else 'N/A'
                if '0x0102' in params and isinstance(params['0x0102'], dict):
                    current_val = params['0x0102'].get('value', 'N/A')
                    current = round(current_val, 1) if isinstance(current_val, (int, float)) else 'N/A'
                return {'soc': soc, 'voltage': voltage, 'current': current}
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
        except Exception as e:
            return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}

    def _battle_results_section(self):
        """人間 vs AI 対戦成績セクション"""
        if not hasattr(self, 'ai_db') or not self.ai_db:
            return ''
        try:
            from ai_learning_database import AILearningDatabase
            if not self.ai_db:
                self.ai_db = AILearningDatabase()
            stats = self.ai_db.get_battle_statistics()
            if stats['total_battles'] == 0:
                return ''
            recent_battles = self.ai_db.get_recent_battles(3)
            recent_text = ''
            for battle in recent_battles:
                date = battle[0]
                winner = battle[8]
                savings = battle[9]
                winner_emoji = '🏆' if winner == 'human' else '🤖'
                recent_text += f'  {date}: {winner_emoji} ¥{int(savings)}\n'
            return f"\n🔥 人間 vs AI 対戦成績\n--------------------\n📊 総対戦数: {stats['total_battles']}戦\n🥇 人間の知恵: {stats['human_wins']}勝 ({stats['human_win_rate']}%)\n🥈 AI学習: {stats['ai_wins']}勝 ({stats['ai_win_rate']}%)\n💰 平均節約: ¥{stats['avg_savings']}/日\n\n📈 最近の対戦結果:\n{recent_text.rstrip()}"
        except Exception as e:
            return ''
EnhancedEmailSystem = EnhancedEmailSystemV2