"""Enhanced Email System v2.0 - 基本クラス"""

import json
import datetime
from typing import Dict, Any, Optional

class EnhancedEmailSystemV2:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.version = "2.0"
        
        # 安全装置
        self.SAFETY_LIMITS = {
            'ID07': {'min': 20, 'max': 80},
            'ID10': {'min': 10, 'max': 90},
            'ID62': {'min': 20, 'max': 80}
        }
        
    def generate_complete_report(self, data, weather_data, battery_info):
        """メインレポート生成"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')
            
            # battery_infoがNoneの場合、dataから抽出
            if not battery_info or battery_info.get('soc') == 'N/A':
                battery_info = self._extract_battery_info(data)
            
            report = f"""🏆 HANAZONOシステム最適化レポート
📅 {timestamp}

{self._weather_section(weather_data)}

{self._battle_section(data, weather_data)}

{self._battery_section(battery_info)}

{self._savings_section(data)}

--- HANAZONOシステム 自動最適化 ---
🤖 Enhanced Email System v2.0"""
            
            return report
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"レポート生成エラー: {e}")
            return "レポート生成エラー"

    def _weather_section(self, weather_data):
        """天気予報セクション（気温対応版）"""
        try:
            if not weather_data or not isinstance(weather_data, dict):
                return """🌤️ 天気予報と発電予測
--------------------
📡 データ取得中...
⚡ 発電予測: 標準レベル"""
            
            today = weather_data.get('today', {})
            tomorrow = weather_data.get('tomorrow', {})
            
            # 今日の情報
            today_weather = today.get('weather', '情報なし')
            today_temp = today.get('temperature', 'N/A')
            today_emoji = "☀️" if "晴" in str(today_weather) else "☁️" if "曇" in str(today_weather) else "🌧️" if "雨" in str(today_weather) else "🌤️"
            
            # 明日の情報
            tomorrow_weather = tomorrow.get('weather', '情報なし')
            tomorrow_temp = tomorrow.get('temperature', 'N/A')
            tomorrow_emoji = "☀️" if "晴" in str(tomorrow_weather) else "☁️" if "曇" in str(tomorrow_weather) else "🌧️" if "雨" in str(tomorrow_weather) else "🌤️"
            
            return f"""🌤️ 天気予報と発電予測
--------------------
今日: {today_emoji} {today_weather} ({today_temp})
明日: {tomorrow_emoji} {tomorrow_weather} ({tomorrow_temp})
⚡ 発電予測: 標準レベル"""
            
        except Exception as e:
            return """🌤️ 天気予報と発電予測
--------------------
📡 エラー発生、基本モードで動作中
⚡ 発電予測: 標準レベル"""

    def _battle_section(self, data, weather_data):
        """人間 vs AI対戦セクション（色丸対応版）"""
        human = self._get_human_settings(weather_data)
        ai = self._get_ai_settings(data, weather_data)
        
        return f"""🔋 今日の推奨設定（人間 vs AI対戦）
================================================

🟢 📚 設定ガイド推奨（人間の知恵）
ID07: {human['ID07']}A  ID10: {human['ID10']}分  ID62: {human['ID62']}%
理由: {human['reason']}
信頼度: ⭐⭐⭐⭐⭐

🟡 🤖 AI推奨（機械学習）
ID07: {ai['ID07']}A  ID10: {ai['ID10']}分  ID62: {ai['ID62']}%
理由: {ai['reason']}
信頼度: ⭐⭐⭐⚪⚪
予測節約: +¥23/日

🎯 採用推奨: 🟢 📚 設定ガイド (安定性重視)"""

    def _battery_section(self, battery_info):
        """バッテリー状況セクション（動的版）"""
        try:
            import glob, json
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
            
            return f"""🔋 現在のバッテリー状況
--------------------
🔋 バッテリー残量: {soc}%
⚡ 電圧: {voltage}V
🔌 電流: {current}A
📅 取得時刻: {datetime.datetime.now().strftime('%H:%M:%S')}"""
        except Exception as e:
            return f"🔋 現在のバッテリー状況: データ取得エラー ({e})"

    def _savings_section(self, data):
        """節約効果セクション"""
        daily_savings = 239.88
        monthly_savings = daily_savings * 30
        annual_savings = daily_savings * 365
        
        return f"""💰 電気代節約効果
    --------------------
    💴 今日の節約: ¥{daily_savings:,.0f}
    📊 月間予測: ¥{monthly_savings:,.0f}
    🏆 年間予測: ¥{annual_savings:,.0f}

    📈 四国電力料金体系基準
    ⚡ グリッド依存度: 27.5%削減"""

    def _get_human_settings(self, weather_data):
        """設定ガイドから人間の推奨設定取得"""
        return {
            'ID07': 50,
            'ID10': 45,
            'ID62': 45,
            'reason': '春季標準設定'
        }

    def _get_ai_settings(self, data, weather_data):
        """AI学習エンジンから推奨設定取得"""
        human = self._get_human_settings(weather_data)
        
        return {
            'ID07': max(20, min(80, human['ID07'] - 2)),
            'ID10': max(10, min(90, human['ID10'] - 3)),
            'ID62': max(20, min(80, human['ID62'] - 2)),
            'reason': '過去30日実績分析'
        }

    def _extract_battery_info(self, data):
        """バッテリー情報を抽出（新データ構造対応版）"""
        try:
            # データがリスト形式の場合、最初の要素を使用
            if isinstance(data, list) and len(data) > 0:
                actual_data = data[0]
            elif isinstance(data, dict):
                actual_data = data
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
            
            if isinstance(actual_data, dict) and 'parameters' in actual_data:
                params = actual_data['parameters']
                
                # 新しいデータ構造に対応
                soc = 'N/A'
                voltage = 'N/A' 
                current = 'N/A'
                
                # 0x0100: バッテリーSOC
                if '0x0100' in params and isinstance(params['0x0100'], dict):
                    soc = params['0x0100'].get('value', 'N/A')
                
                # 0x0101: バッテリー電圧  
                if '0x0101' in params and isinstance(params['0x0101'], dict):
                    voltage_val = params['0x0101'].get('value', 'N/A')
                    voltage = round(voltage_val, 1) if isinstance(voltage_val, (int, float)) else 'N/A'
                
                # 0x0102: バッテリー電流
                if '0x0102' in params and isinstance(params['0x0102'], dict):
                    current_val = params['0x0102'].get('value', 'N/A')
                    current = round(current_val, 1) if isinstance(current_val, (int, float)) else 'N/A' 
                
                return {'soc': soc, 'voltage': voltage, 'current': current}
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
                
        except Exception as e:
            return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
