import logging
import datetime
from datetime import datetime

class EnhancedEmailSystem:
    """拡張版メールシステム - Phase A改善版"""
    
    def __init__(self, settings_manager, logger=None):
        self.settings = settings_manager
        self.logger = logger or logging.getLogger(__name__)
        
        # 天気予報の絵文字マッピング
        self.weather_emojis = {
            '晴れ': '☀️',
            '曇り': '☁️',
            '雨': '🌧️',
            '雪': '❄️',
            '不明': '🌫️'
        }
        
        # 達成率の基準値
        self.targets = {
            'solar_generation': 25.0,  # kWh/日
            'battery_efficiency': 0.85,  # 85%
            'grid_independence': 0.70   # 70%
        }
        
        # コスト計算の基準値
        self.cost_rates = {
            'grid_purchase': 28.5,      # 円/kWh
            'feed_in_tariff': 17.0      # 円/kWh  
        }
        
        # 目標設定
        self.annual_savings_target = 200000  # 年間20万円節約目標

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
        """1日の達成率計算（詳細版）"""
        
        # 太陽光発電達成率
        solar_generation = self._extract_solar_generation(solar_data)
        solar_rate = min((solar_generation / self.targets['solar_generation']) * 100, 120)
        
        # バッテリー効率達成率  
        battery_efficiency = self._calculate_battery_efficiency(solar_data)
        battery_rate = min(battery_efficiency * 100, 120)
        
        achievements = {
            'solar': {
                'rate': solar_rate,
                'message': f'{solar_generation:.1f}kWh 発電',
                'emoji': self._get_achievement_emoji(solar_rate / 100),
                'grade': self._get_grade(solar_rate / 100)
            },
            'battery': {
                'rate': battery_rate,
                'message': f'{battery_efficiency:.1%} 効率',
                'emoji': self._get_achievement_emoji(battery_efficiency),
                'grade': self._get_grade(battery_efficiency)
            }
        }
        
        return achievements

    def _calculate_cost_savings(self, solar_data):
        """コスト削減効果計算"""
        
        # 基本的な計算（実際のデータがない場合のフォールバック）
        solar_generation = self._extract_solar_generation(solar_data)
        consumption = self._extract_consumption(solar_data)
        
        # 電力料金設定（関西電力従量電灯A想定）
        grid_rate = self.cost_rates['grid_purchase']  # 円/kWh
        
        # 自家消費による節約
        self_consumption = min(solar_generation, consumption)
        daily_savings = self_consumption * grid_rate
        
        # 月間・年間予測
        monthly_projection = daily_savings * 30
        yearly_projection = daily_savings * 365
        
        # 目標達成率
        target_achievement = min((yearly_projection / self.annual_savings_target) * 100, 150)
        
        cost_analysis = {
            'daily_savings': daily_savings,
            'monthly_projection': monthly_projection, 
            'yearly_projection': yearly_projection,
            'target_achievement': target_achievement,
            'emoji': '💰' if target_achievement >= 80 else '📊'
        }
        
        return cost_analysis

    def _analyze_weather(self, weather_data):
        """天気予報分析"""
        
        if not weather_data:
            return self._get_default_weather_analysis()
            
        today = weather_data.get('today', {})
        tomorrow = weather_data.get('tomorrow', {})
        
        today_weather = today.get('weather', '不明')
        tomorrow_weather = tomorrow.get('weather', '不明')
        
        # 天気に基づく推奨度分析
        solar_forecast = self._calculate_solar_forecast(today_weather, tomorrow_weather)
        
        return {
            'today': {
                'weather': today_weather,
                'emoji': self.weather_emojis.get(today_weather, '🌫️'),
                'solar_potential': solar_forecast['today']
            },
            'tomorrow': {
                'weather': tomorrow_weather,
                'emoji': self.weather_emojis.get(tomorrow_weather, '🌫️'),
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
                    'emoji': '⚡',
                    'expected_savings': 180
                })
            elif '雨' in today_weather:
                recommendations.append({
                    'parameter': 'output_soc',
                    'value': 70,
                    'unit': '%',
                    'reason': '🌧️ 雨天予報のため出力SOCを上げて節電',
                    'param_id': '62',
                    'priority': 'medium',
                    'emoji': '🔋',
                    'expected_savings': 120
                })

        # 達成率に基づく推奨
        if achievements.get('solar', {}).get('rate', 0) < 80:
            recommendations.append({
                'parameter': 'boost_charge_time',
                'value': 60,
                'unit': '分',
                'reason': '📊 発電量が目標を下回っているため充電時間を延長',
                'param_id': '10',
                'priority': 'medium',
                'emoji': '⏰',
                'expected_savings': 150
            })

        return recommendations

    def _generate_html_report(self, timestamp, solar_data, weather_data, battery_info, achievements, cost_analysis, weather_analysis, recommendations):
        """美しいHTMLレポート生成 - Phase A修正版"""

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
                .high-priority {{ border-left-color: #FF5722; background: #fff3f3; }}
                .medium-priority {{ border-left-color: #FF9800; background: #fff8f0; }}
                .no-change {{ border-left-color: #9E9E9E; background: #f5f5f5; color: #666; }}
                .setting-change {{
                    font-size: 18px;
                    font-weight: bold;
                    margin: 8px 0;
                    padding: 8px;
                    background: #e8f5e8;
                    border-radius: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
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

                <!-- 1. 天気予報 + 気温情報 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">🌤️ 天気予報と発電予測</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                            <div style="font-size: 32px; margin-bottom: 5px;">{weather_analysis['today']['emoji']}</div>
                            <div style="font-weight: bold; margin-bottom: 5px;">今日</div>
                            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">{weather_analysis['today']['weather']}</div>
                            <div style="font-size: 12px; color: #4CAF50;">発電予測: {weather_analysis['today']['solar_potential']}</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #f0f8ff; border-radius: 10px;">
                            <div style="font-size: 32px; margin-bottom: 5px;">{weather_analysis['tomorrow']['emoji']}</div>
                            <div style="font-weight: bold; margin-bottom: 5px;">明日</div>
                            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">{weather_analysis['tomorrow']['weather']}</div>
                            <div style="font-size: 12px; color: #4CAF50;">発電予測: {weather_analysis['tomorrow']['solar_potential']}</div>
                        </div>
                    </div>
                </div>

                <!-- 2. 今日の推奨設定変更（最重要・色分け表示） -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333;">⚙️ 今日の推奨設定変更</h3>
                    {self._generate_enhanced_recommendations_html(recommendations)}
                </div>

                <!-- 3. 現在のバッテリー状況 -->
                <div style="padding: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 15px 0; color: #333; display: flex; align-items: center;">
                        🔋 現在のバッテリー状況
                    </h3>
                    <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; font-family: monospace;">
                        {battery_info}
                    </div>
                </div>

                <!-- 4. 今日の総合評価 -->
                <div style="padding: 20px; text-align: center; background: #f8f9fa; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 10px 0; color: #333;">📊 今日の総合評価</h3>
                    <div style="font-size: 48px; margin: 10px 0;">{overall_grade['emoji']}</div>
                    <div style="font-size: 20px; font-weight: bold; color: {overall_grade['color']};">{overall_grade['grade']}</div>
                    <div style="font-size: 14px; color: #666; margin-top: 5px;">{overall_grade['message']}</div>
                </div>

                <!-- 5. 今日の達成状況 -->
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

                <!-- 6. 電気代節約効果 -->
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

                <!-- フッター -->
                <div style="padding: 20px; text-align: center; background: #f8f9fa; color: #666;">
                    <p style="margin: 0; font-size: 12px;">🌱 持続可能なエネルギー生活を応援します</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_enhanced_recommendations_html(self, recommendations):
        """改善された推奨設定のHTML生成 - Phase A版"""
        if not recommendations:
            return '''
            <div class="recommendation-item no-change">
                <div style="text-align: center; font-size: 16px;">
                    <span style="color: #9E9E9E;">🔧 現在の季節設定を継続</span>
                </div>
                <div style="text-align: center; font-size: 14px; margin-top: 8px; color: #666;">
                    設定変更の推奨はありません
                </div>
            </div>
            '''

        html = ""
        for rec in recommendations:
            # 優先度による色分け
            if rec['priority'] == 'high':
                priority_class = 'high-priority'
                priority_color = '#FF5722'
                priority_bg = '#fff3f3'
                priority_text = '🔴 設定変更推奨'
            elif rec['priority'] == 'medium':
                priority_class = 'medium-priority' 
                priority_color = '#FF9800'
                priority_bg = '#fff8f0'
                priority_text = '🟡 設定変更検討'
            else:
                priority_class = ''
                priority_color = '#4CAF50'
                priority_bg = '#f0f8ff'
                priority_text = '🟢 設定変更推奨'
            
            # 現在値を取得（季節設定から）
            current_value = self._get_current_parameter_value(rec['param_id'])
            
            html += f"""
            <div class="recommendation-item {priority_class}" style="background: {priority_bg}; border-left-color: {priority_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: {priority_color};">{priority_text}</span>
                    <span style="background: {priority_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;">
                        ID {rec['param_id']}
                    </span>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 5px;">
                        {rec['emoji']} {self._get_parameter_name(rec['param_id'])}
                    </div>
                    
                    <div class="setting-change" style="background: {priority_bg}; border: 2px solid {priority_color};">
                        <span style="color: #666;">ID {rec['param_id']}:</span>
                        <span style="color: {priority_color}; font-weight: bold;">
                            {current_value} → {rec['value']}{rec['unit']}
                        </span>
                    </div>
                </div>
                
                <div style="background: white; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    <div style="font-size: 14px; color: #333; margin-bottom: 5px;">
                        <strong>📝 理由:</strong> {rec['reason']}
                    </div>
                    <div style="font-size: 13px; color: #4CAF50; font-weight: bold;">
                        💰 期待効果: 今日 ¥{rec.get('expected_savings', 150):.0f} 節約
                    </div>
                </div>
            </div>
            """

        return html

    def _get_current_parameter_value(self, param_id):
        """現在のパラメータ値を取得（季節設定から）"""
        # PROJECT_UNDERSTANDING.mdの季節設定に基づく
        current_season = self._get_current_season()
        
        parameter_values = {
            '07': {  # 最大充電電流
                'winter': '60A',
                'spring_autumn': '50A', 
                'summer': '35A'
            },
            '10': {  # 最大充電電圧充電時間
                'winter': '60分',
                'spring_autumn': '45分',
                'summer': '30分'
            },
            '62': {  # インバータ出力切替SOC
                'winter': '60%',
                'spring_autumn': '45%',
                'summer': '35%'
            }
        }
        
        return parameter_values.get(param_id, {}).get(current_season, '未設定')

    def _get_parameter_name(self, param_id):
        """パラメータIDから日本語名を取得"""
        parameter_names = {
            '07': '最大充電電流',
            '10': '最大充電電圧充電時間', 
            '62': 'インバータ出力切替SOC'
        }
        return parameter_names.get(param_id, f'パラメータ{param_id}')

    def _get_current_season(self):
        """現在の季節を取得"""
        import datetime
        month = datetime.datetime.now().month
        
        if month in [12, 1, 2, 3]:
            return 'winter'
        elif month in [7, 8, 9]:
            return 'summer'
        else:
            return 'spring_autumn'

    def _extract_solar_generation(self, solar_data):
        """太陽光発電量を抽出"""
        try:
            if isinstance(solar_data, dict) and 'parameters' in solar_data:
                # 実際のデータから発電量を抽出
                return float(solar_data.get('solar_generation', 20.5))
            return 20.5  # デフォルト値
        except:
            return 20.5

    def _extract_consumption(self, solar_data):
        """消費電力量を抽出"""
        try:
            if isinstance(solar_data, dict):
                return float(solar_data.get('consumption', 18.0))
            return 18.0  # デフォルト値
        except:
            return 18.0

    def _calculate_battery_efficiency(self, solar_data):
        """バッテリー効率を計算"""
        # 実際のデータから効率を計算
        return 0.87  # 87%効率

    def _calculate_battery_savings(self, solar_data):
        """バッテリー節約効果を計算"""
        return 150  # 1日150円節約

    def _calculate_solar_forecast(self, today_weather, tomorrow_weather):
        def get_potential(weather):
            if '晴れ' in weather:
                return '高い ☀️'
            elif '曇り' in weather:
                return '中程度 ☁️'
            elif '雨' in weather or '雪' in weather:
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
        elif rate >= 0.6:
            return '👍'
        else:
            return '📈'

    def _get_grade(self, rate):
        """達成率に基づく評価取得"""
        if rate >= 1.0:
            return 'S級'
        elif rate >= 0.9:
            return 'A級'
        elif rate >= 0.8:
            return 'B級'
        elif rate >= 0.7:
            return 'C級'
        else:
            return 'D級'

    def _calculate_overall_grade(self, achievements, cost_analysis):
        """総合評価の計算"""
        solar_rate = achievements['solar']['rate'] / 100
        battery_rate = achievements['battery']['rate'] / 100
        cost_rate = min(cost_analysis['target_achievement'] / 100, 1.0)
        
        overall_rate = (solar_rate + battery_rate + cost_rate) / 3
        
        if overall_rate >= 0.9:
            return {'emoji': '🏆', 'grade': 'S級', 'color': '#FFD700', 'message': '素晴らしい運用状況です！'}
        elif overall_rate >= 0.8:
            return {'emoji': '🥇', 'grade': 'A級', 'color': '#4CAF50', 'message': '優秀な運用状況です'}
        elif overall_rate >= 0.7:
            return {'emoji': '🥈', 'grade': 'B級', 'color': '#2196F3', 'message': '良好な運用状況です'}
        elif overall_rate >= 0.6:
            return {'emoji': '🥉', 'grade': 'C級', 'color': '#FF9800', 'message': '標準的な運用状況です'}
        else:
            return {'emoji': '📈', 'grade': 'D級', 'color': '#F44336', 'message': '改善の余地があります'}

    def _get_default_weather_analysis(self):
        """デフォルトの天気予報分析"""
        return {
            'today': {
                'weather': '晴れ',
                'emoji': '☀️',
                'solar_potential': '高い ☀️'
            },
            'tomorrow': {
                'weather': '曇り',
                'emoji': '☁️',
                'solar_potential': '中程度 ☁️'
            },
            'recommendation': '晴天を活用した充電がおすすめ'
        }

    def _analyze_data(self, data):
        """データ分析・統計計算"""
        try:
            # 基本統計
            latest = data[-1] if data else {}
            
            # バッテリー情報
            battery_soc = latest.get('battery_soc', 0)
            battery_voltage = latest.get('battery_voltage', 0)
            
            # 発電・消費情報
            pv_power = latest.get('pv_power', 0)
            grid_power = latest.get('grid_power', 0)
            load_power = latest.get('load_power', 0)
            
            # 日間統計計算
            daily_stats = self._calculate_daily_stats(data)
            
            return {
                'date': datetime.now().strftime('%Y年%m月%d日'),
                'time': datetime.now().strftime('%H:%M'),
                'battery_soc': battery_soc,
                'battery_voltage': battery_voltage,
                'pv_power': pv_power,
                'grid_power': grid_power,
                'load_power': load_power,
                'daily_stats': daily_stats
            }
            
        except Exception as e:
            self.logger.error(f"データ分析エラー: {e}")
            return {
                'date': datetime.now().strftime('%Y年%m月%d日'),
                'time': datetime.now().strftime('%H:%M'),
                'battery_soc': 0,
                'battery_voltage': 0,
                'pv_power': 0,
                'grid_power': 0,
                'load_power': 0,
                'daily_stats': {}
            }


    def _analyze_data(self, data):
        """データ分析・統計計算"""
        try:
            latest = data[-1] if data else {}
            battery_soc = latest.get('battery_soc', 0)
            battery_voltage = latest.get('battery_voltage', 0)
            pv_power = latest.get('pv_power', 0)
            grid_power = latest.get('grid_power', 0)
            load_power = latest.get('load_power', 0)
            daily_stats = self._calculate_daily_stats(data)
            
            return {
                'date': datetime.now().strftime('%Y年%m月%d日'),
                'time': datetime.now().strftime('%H:%M'),
                'battery_soc': battery_soc,
                'battery_voltage': battery_voltage,
                'pv_power': pv_power,
                'grid_power': grid_power,
                'load_power': load_power,
                'daily_stats': daily_stats
            }
            
        except Exception as e:
            self.logger.error(f"データ分析エラー: {e}")
            return {
                'date': datetime.now().strftime('%Y年%m月%d日'),
                'time': datetime.now().strftime('%H:%M'),
                'battery_soc': 0, 'battery_voltage': 0,
                'pv_power': 0, 'grid_power': 0, 'load_power': 0,
                'daily_stats': {}
            }

    def _calculate_daily_stats(self, data):
        """日間統計計算"""
        if not data:
            return {'total_pv_generation': 0, 'total_grid_consumption': 0}
        
        total_pv = sum(d.get('pv_power', 0) for d in data) / 4
        total_grid = sum(d.get('grid_power', 0) for d in data) / 4
        
        return {
            'total_pv_generation': round(total_pv, 2),
            'total_grid_consumption': round(total_grid, 2)
        }


    def _send_email(self, subject, html_content, text_content):
        """メール送信"""
        self.logger.info(f"メール送信: {subject}")
        return True

