#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム 完全版メールシステム
美しいテンプレート + 達成率評価 + コスト計算
"""

from datetime import datetime, timedelta
import json
import logging

class EnhancedEmailSystem:
    def __init__(self, settings_manager, logger=None):
        self.settings = settings_manager
        self.logger = logger or logging.getLogger(__name__)
        
        # 絵文字定義
        self.weather_emojis = {
            '晴れ': '☀️', '曇り': '☁️', '雨': '🌧️', '雪': '❄️',
            '雷': '⛈️', '霧': '🌫️', 'クリア': '🌤️'
        }
        
        self.season_emojis = {
            '春': '🌸', '夏': '🌻', '秋': '🍂', '冬': '❄️'
        }
        
        self.achievement_emojis = {
            'perfect': '🏆', 'excellent': '🥇', 'good': '🥈', 
            'fair': '🥉', 'poor': '📈', 'improving': '⬆️'
        }
        
        self.battery_emojis = {
            'high': '🔋', 'medium': '🔶', 'low': '🔻', 'charging': '⚡'
        }
        
        # 目標設定
        self.daily_targets = {
            'solar_generation': 12.0,    # kWh
            'battery_efficiency': 85.0,  # %
            'cost_savings': 400.0        # 円/日
        }
    
    def generate_complete_report(self, solar_data, weather_data, battery_info):
        """完全版レポート生成"""
        timestamp = datetime.now()
        
        # 達成率計算
        achievements = self._calculate_daily_achievements(solar_data)
        
        # コスト計算
        cost_analysis = self._calculate_cost_savings(solar_data)
        
        # 天気予報分析
        weather_analysis = self._analyze_weather(weather_data)
        
        # 推奨設定生成
        recommendations = self._generate_recommendations(weather_data, achievements)
        
        # HTMLレポート生成
        html_report = self._generate_html_report(
            timestamp, solar_data, weather_data, 
            battery_info, achievements, cost_analysis,
            weather_analysis, recommendations
        )
        
        return html_report
    
    def _calculate_daily_achievements(self, solar_data):
        """日次達成率計算"""
        achievements = {}
        
        # 太陽光発電達成率
        generation = self._extract_solar_generation(solar_data)
        solar_rate = min(100, (generation / self.daily_targets['solar_generation']) * 100)
        
        achievements['solar'] = {
            'value': generation,
            'target': self.daily_targets['solar_generation'],
            'rate': solar_rate,
            'emoji': self._get_achievement_emoji(solar_rate / 100),
            'grade': self._get_grade(solar_rate),
            'message': f"{generation:.1f}kWh / {self.daily_targets['solar_generation']:.1f}kWh"
        }
        
        # バッテリー効率
        battery_eff = self._calculate_battery_efficiency(solar_data)
        achievements['battery'] = {
            'value': battery_eff,
            'target': self.daily_targets['battery_efficiency'],
            'rate': min(100, (battery_eff / self.daily_targets['battery_efficiency']) * 100),
            'emoji': self._get_achievement_emoji(battery_eff / self.daily_targets['battery_efficiency']),
            'grade': self._get_grade(battery_eff),
            'message': f"{battery_eff:.1f}% 効率"
        }
        
        return achievements
    
    def _calculate_cost_savings(self, solar_data):
        """コスト節約計算"""
        # 電力料金設定（関西電力従量電灯A想定）
        electricity_rates = {
            'day': 25.80,    # 円/kWh (昼間)
            'night': 22.67   # 円/kWh (夜間)
        }
        
        generation = self._extract_solar_generation(solar_data)
        consumption = self._extract_consumption(solar_data)
        
        # 節約金額計算
        solar_savings = generation * electricity_rates['day']
        battery_savings = self._calculate_battery_savings(solar_data)
        
        total_savings = solar_savings + battery_savings
        monthly_projection = total_savings * 30
        yearly_projection = total_savings * 365
        
        return {
            'daily_savings': total_savings,
            'monthly_projection': monthly_projection,
            'yearly_projection': yearly_projection,
            'solar_contribution': solar_savings,
            'battery_contribution': battery_savings,
            'achievement_rate': min(100, (total_savings / self.daily_targets['cost_savings']) * 100),
            'emoji': '💰' if total_savings >= self.daily_targets['cost_savings'] else '💵'
        }
    
    def _analyze_weather(self, weather_data):
        """天気予報分析"""
        if not weather_data:
            return {'status': 'no_data', 'emoji': '❓', 'message': '天気データなし'}
        
        today = weather_data.get('today', {})
        tomorrow = weather_data.get('tomorrow', {})
        
        today_weather = today.get('weather', '不明')
        tomorrow_weather = tomorrow.get('weather', '不明')
        
        # 天気に基づく推奨度分析
        solar_forecast = self._calculate_solar_forecast(today_weather, tomorrow_weather)
        
        return {
            'today': {
                'weather': today_weather,
                'emoji': self.weather_emojis.get(today_weather, '🌤️'),
                'solar_potential': solar_forecast['today']
            },
            'tomorrow': {
                'weather': tomorrow_weather,
                'emoji': self.weather_emojis.get(tomorrow_weather, '🌤️'),
                'solar_potential': solar_forecast['tomorrow']
            },
            'recommendation': solar_forecast['recommendation']
        }
    
    def _generate_recommendations(self, weather_data, achievements):
        """天気と達成率に基づく推奨設定"""
        recommendations = []
        
        # 天気に基づく推奨
        if weather_data:
            today_weather = weather_data.get('today', {}).get('weather', '')
            if '晴れ' in today_weather:
                recommendations.append({
                    'parameter': 'charge_current',
                    'value': 15,
                    'unit': 'A',
                    'reason': '☀️ 晴天予報のため充電電流を増加',
                    'param_id': '07',
                    'priority': 'high',
                    'emoji': '⚡'
                })
            elif '雨' in today_weather:
                recommendations.append({
                    'parameter': 'discharge_cutoff',
                    'value': 40,
                    'unit': '%',
                    'reason': '🌧️ 雨天予報のため放電を控えめに',
                    'param_id': '62',
                    'priority': 'medium',
                    'emoji': '🔋'
                })
        
        # 達成率に基づく推奨
        if achievements.get('solar', {}).get('rate', 0) < 80:
            recommendations.append({
                'parameter': 'boost_charge_time',
                'value': 60,
                'unit': '分',
                'reason': '📈 発電量向上のためブースト充電時間延長',
                'param_id': '10',
                'priority': 'medium',
                'emoji': '⚡'
            })
        
        return recommendations
    
    def _generate_html_report(self, timestamp, solar_data, weather_data, battery_info, achievements, cost_analysis, weather_analysis, recommendations):
        """美しいHTMLレポート生成"""
        
        # 全体的な評価
        overall_grade = self._calculate_overall_grade(achievements, cost_analysis)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>HANAZONOシステム 最適化レポート</title>
            <style>
                .achievement-bar {{
                    background: #e0e0e0;
                    border-radius: 10px;
                    height: 20px;
                    margin: 5px 0;
                    overflow: hidden;
                }}
                .achievement-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #4CAF50, #45a049);
                    transition: width 0.3s ease;
                }}
                .recommendation-item {{
                    background: #f8f9fa;
                    border-left: 4px solid #4CAF50;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                }}
                .high-priority {{ border-left-color: #FF5722; }}
                .medium-priority {{ border-left-color: #FF9800; }}
            </style>
        </head>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); overflow: hidden;">
                
                <!-- ヘッダー -->
                <div style="background: linear-gradient(90deg, #4CAF50, #45a049); color: white; padding: 25px; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">🌻 HANAZONOシステム</h1>
                    <h2 style="margin: 5px 0 0 0; font-size: 18px; opacity: 0.9;">最適化レポート</h2>
                    <p style="margin: 5px 0 0 0; opacity: 0.8;">{timestamp.strftime('%Y年%m月%d日 %H:%M')}</p>
                </div>
                
                <!-- 総合評価 -->
                <div style="padding: 20px; text-align: center; background: #f8f9fa;">
                    <h3 style="margin: 0 0 10px 0; color: #333;">📊 今日の総合評価</h3>
                    <div style="font-size: 48px; margin: 10px 0;">{overall_grade['emoji']}</div>
                    <div style="font-size: 20px; font-weight: bold; color: {overall_grade['color']};">{overall_grade['grade']}</div>
                    <div style="font-size: 14px; color: #666; margin-top: 5px;">{overall_grade['message']}</div>
                </div>
                
                <!-- バッテリー状況 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333; display: flex; align-items: center;">
                        🔋 現在のバッテリー状況
                    </h3>
                    <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; font-family: monospace;">
                        {battery_info}
                    </div>
                </div>
                
                <!-- 達成率セクション -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">🎯 今日の達成状況</h3>
                    
                    <!-- 太陽光発電 -->
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <span style="font-weight: bold;">{achievements['solar']['emoji']} 太陽光発電</span>
                            <span style="color: #666;">{achievements['solar']['message']}</span>
                        </div>
                        <div class="achievement-bar">
                            <div class="achievement-fill" style="width: {achievements['solar']['rate']:.1f}%;"></div>
                        </div>
                        <div style="font-size: 12px; color: #666; text-align: right;">{achievements['solar']['rate']:.1f}% - {achievements['solar']['grade']}</div>
                    </div>
                    
                    <!-- バッテリー効率 -->
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <span style="font-weight: bold;">{achievements['battery']['emoji']} バッテリー効率</span>
                            <span style="color: #666;">{achievements['battery']['message']}</span>
                        </div>
                        <div class="achievement-bar">
                            <div class="achievement-fill" style="width: {achievements['battery']['rate']:.1f}%;"></div>
                        </div>
                        <div style="font-size: 12px; color: #666; text-align: right;">{achievements['battery']['rate']:.1f}% - {achievements['battery']['grade']}</div>
                    </div>
                </div>
                
                <!-- コスト分析 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">{cost_analysis['emoji']} 電気代節約効果</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="text-align: center; background: #e8f5e8; padding: 15px; border-radius: 10px;">
                            <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">¥{cost_analysis['daily_savings']:.0f}</div>
                            <div style="font-size: 12px; color: #666;">今日の節約</div>
                        </div>
                        <div style="text-align: center; background: #e3f2fd; padding: 15px; border-radius: 10px;">
                            <div style="font-size: 24px; font-weight: bold; color: #2196F3;">¥{cost_analysis['monthly_projection']:.0f}</div>
                            <div style="font-size: 12px; color: #666;">月間予測</div>
                        </div>
                    </div>
                    <div style="margin-top: 15px; font-size: 14px; color: #666; text-align: center;">
                        年間予測節約額: <span style="font-weight: bold; color: #4CAF50;">¥{cost_analysis['yearly_projection']:,.0f}</span>
                    </div>
                </div>
                
                <!-- 天気予報 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">🌤️ 天気予報と発電予測</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                            <div style="font-size: 32px; margin-bottom: 5px;">{weather_analysis['today']['emoji']}</div>
                            <div style="font-weight: bold;">今日</div>
                            <div style="font-size: 14px; color: #666;">{weather_analysis['today']['weather']}</div>
                            <div style="font-size: 12px; color: #4CAF50;">発電予測: {weather_analysis['today']['solar_potential']}</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                            <div style="font-size: 32px; margin-bottom: 5px;">{weather_analysis['tomorrow']['emoji']}</div>
                            <div style="font-weight: bold;">明日</div>
                            <div style="font-size: 14px; color: #666;">{weather_analysis['tomorrow']['weather']}</div>
                            <div style="font-size: 12px; color: #4CAF50;">発電予測: {weather_analysis['tomorrow']['solar_potential']}</div>
                        </div>
                    </div>
                </div>
                
                <!-- 推奨設定 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">⚙️ 今日の推奨設定変更</h3>
                    {self._generate_recommendations_html(recommendations)}
                </div>
                
                <!-- フッター -->
                <div style="padding: 20px; text-align: center; background: #f8f9fa; color: #666;">
                    <p style="margin: 0; font-size: 12px;">🌻 HANAZONOシステム - 太陽光発電最適化AI</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px;">毎日の積み重ねで地球に優しい生活を実現 🌍</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_recommendations_html(self, recommendations):
        """推奨設定のHTML生成"""
        if not recommendations:
            return '<div style="text-align: center; color: #666; font-style: italic;">今日は設定変更の推奨はありません 👍</div>'
        
        html = ""
        for rec in recommendations:
            priority_class = f"{rec['priority']}-priority" if rec['priority'] in ['high', 'medium'] else ''
            html += f"""
            <div class="recommendation-item {priority_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span style="font-weight: bold;">{rec['emoji']} {rec['parameter']}</span>
                    <span style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                        ID: {rec['param_id']}
                    </span>
                </div>
                <div style="font-size: 18px; color: #4CAF50; font-weight: bold; margin: 5px 0;">
                    推奨値: {rec['value']} {rec['unit']}
                </div>
                <div style="font-size: 14px; color: #666;">
                    理由: {rec['reason']}
                </div>
            </div>
            """
        
        return html
    
    # ヘルパーメソッド群
    def _extract_solar_generation(self, solar_data):
        """太陽光発電量を抽出（ダミーデータ）"""
        # 実際のデータから抽出ロジックを実装
        return 10.5  # kWh
    
    def _extract_consumption(self, solar_data):
        """消費電力を抽出（ダミーデータ）"""
        return 8.2  # kWh
    
    def _calculate_battery_efficiency(self, solar_data):
        """バッテリー効率を計算（ダミーデータ）"""
        return 87.5  # %
    
    def _calculate_battery_savings(self, solar_data):
        """バッテリー節約効果を計算（ダミーデータ）"""
        return 150.0  # 円
    
    def _calculate_solar_forecast(self, today_weather, tomorrow_weather):
        """太陽光発電予測"""
        def get_potential(weather):
            if '晴れ' in weather:
                return '高い ☀️'
            elif '曇り' in weather:
                return '普通 ☁️'
            elif '雨' in weather:
                return '低い 🌧️'
            else:
                return '普通 🌤️'
        
        return {
            'today': get_potential(today_weather),
            'tomorrow': get_potential(tomorrow_weather),
            'recommendation': '晴天を活用した充電がおすすめ' if '晴れ' in today_weather else '雨天に備えた節電を推奨'
        }
    
    def _get_achievement_emoji(self, rate):
        """達成率に基づく絵文字取得"""
        if rate >= 1.0:
            return '🏆'
        elif rate >= 0.9:
            return '🥇'
        elif rate >= 0.8:
            return '🥈'
        elif rate >= 0.7:
            return '🥉'
        else:
            return '📈'
    
    def _get_grade(self, rate):
        """達成率に基づくグレード取得"""
        if rate >= 95:
            return 'PERFECT'
        elif rate >= 85:
            return 'EXCELLENT'
        elif rate >= 75:
            return 'GOOD'
        elif rate >= 65:
            return 'FAIR'
        else:
            return 'NEEDS IMPROVEMENT'
    
    def _calculate_overall_grade(self, achievements, cost_analysis):
        """総合評価計算"""
        solar_rate = achievements.get('solar', {}).get('rate', 0)
        battery_rate = achievements.get('battery', {}).get('rate', 0)
        cost_rate = cost_analysis.get('achievement_rate', 0)
        
        overall_rate = (solar_rate + battery_rate + cost_rate) / 3
        
        if overall_rate >= 90:
            return {'emoji': '🏆', 'grade': 'PERFECT', 'color': '#FFD700', 'message': '素晴らしい！完璧な一日でした'}
        elif overall_rate >= 80:
            return {'emoji': '🥇', 'grade': 'EXCELLENT', 'color': '#4CAF50', 'message': '優秀！とても良い結果です'}
        elif overall_rate >= 70:
            return {'emoji': '🥈', 'grade': 'GOOD', 'color': '#2196F3', 'message': '良好！順調に進歩しています'}
        elif overall_rate >= 60:
            return {'emoji': '🥉', 'grade': 'FAIR', 'color': '#FF9800', 'message': '普通！改善の余地があります'}
        else:
            return {'emoji': '📈', 'grade': 'IMPROVING', 'color': '#f44336', 'message': '頑張って！明日はもっと良くなります'}
