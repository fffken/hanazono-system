from enhanced_email_system import EnhancedEmailSystem
from settings_recommender import SettingsRecommender
from season_detector import get_current_season, get_detailed_season
from weather_forecast import get_weather_forecast
import datetime
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

def strip_html_tags(html_content):
    """HTMLタグを除去してテキストに変換"""
    import re
    text = re.sub('<[^>]+>', '', html_content)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = re.sub('\\n\\s*\\n', '\n\n', text)
    return text.strip()

class EmailNotifier:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.settings_recommender = SettingsRecommender()
        self.enhanced_system = EnhancedEmailSystem(None, self.logger)

    def send_daily_report(self, data):
        try:
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error('メール設定が不完全です')
                return False
            now = datetime.datetime.now()
            time_suffix = '(07時)' if 5 <= now.hour < 12 else '(23時)'
            date_str = now.strftime('%Y年%m月%d日')
            subject = f'HANAZONOシステム最適化レポート {date_str} {time_suffix}'
            text_content = self._generate_intelligent_report(data)
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            text_content = strip_html_tags(text_content)
            msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            self.logger.info(f'最適化レポートを送信しました: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}')
            return False

    def _generate_intelligent_report(self, data):
        try:
            from weather_forecast import get_weather_forecast
            weather_data = get_weather_forecast()
            battery_info = self._extract_battery_info(data)
            html_report = self.enhanced_system.generate_complete_report(data, weather_data, battery_info)
            import re
            text_report = re.sub('<[^>]+>', '', html_report)
            text_report = text_report.replace('&nbsp;', ' ')
            text_report = re.sub('\\n\\s*\\n', '\n\n', text_report)
            return text_report.strip()
        except Exception as e:
            self.logger.error(f'Enhanced report error: {e}')
            return 'Enhanced report generation failed'

    def _generate_fallback_report(self, data):
        report = '=== HANAZONOシステム 最適化レポート ===\n'
        try:
            self.logger.info('天気予報を取得中...')
            weather = get_weather_forecast()
            season = get_current_season()
            detailed_season = get_detailed_season()
            battery_info = self._extract_battery_info(data)
            report += f'\n■ 現在の状態'
            report += f'\n{battery_info}\n'
            report += f'\n■ 天気予報分析'
            if weather:
                today_weather = weather.get('today', {})
                tomorrow_weather = weather.get('tomorrow', {})
                report += f"\n今日: {today_weather.get('weather', 'データなし')}"
                report += f"\n明日: {tomorrow_weather.get('weather', 'データなし')}\n"
                try:
                    season_detail, setting_type, params = self.settings_recommender.recommend_settings(weather)
                    report += f'\n■ 推奨設定'
                    report += f'\ntypeA（標準設定）'
                    report += f'\n設定項目\t推奨値\tパラメータID'
                    report += f"\n充電電流\t{params.get('charge_current', 'N/A')} A\t07"
                    report += f"\n充電時間\t{params.get('charge_time', 'N/A')} 分\t10"
                    report += f"\nSOC設定\t{params.get('soc', 'N/A')} %\t62\n"
                except Exception as e:
                    report += f'■ 推奨設定\n推奨設定取得エラー: {e}\n'
                recommendations = self._generate_recommendations(weather, season, battery_info)
            else:
                report += '\n天気データ取得失敗\n'
                report += f'■ 最適化推奨'
                report += '\n天気データなしのため基本推奨を適用\n'
            report += f'\n■ システム情報'
            report += f'\n季節判定: {season} ({detailed_season})'
            report += f"\nデータ更新: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        except Exception as e:
            self.logger.error(f'レポート生成エラー: {e}')
            report += f'レポート生成中にエラーが発生しました: {e}\n'
        report += '\n--- HANAZONOシステム 自動最適化 ---'
        return report

    def _extract_battery_info(self, data):
        """バッテリー情報を抽出（修正版）"""
        try:
            if isinstance(data, tuple) and len(data) > 0:
                actual_data = data[0]
            elif isinstance(data, dict):
                actual_data = data
            else:
                return 'バッテリー情報: データ形式エラー'
            if 'parameters' in actual_data:
                params = actual_data['parameters']
                soc_value = params.get('0x0100', {}).get('value', 'N/A')
                voltage_value = params.get('0x0101', {}).get('value', 'N/A')
                current_value = params.get('0x0102', {}).get('value', 'N/A')
                timestamp = actual_data.get('datetime', 'N/A')
                return f'🔋 バッテリー残量: {soc_value}% (取得時刻: {timestamp})\n⚡ 電圧: {voltage_value}V 🔌 電流: {current_value}A'
            else:
                return 'バッテリー情報: parametersが見つかりません'
        except Exception as e:
            return f'バッテリー情報取得エラー: {e}'

    def _generate_recommendations(self, weather, season, battery_info):
        """天気予報と季節に基づく最適化推奨を生成"""
        recommendations = []
        try:
            if weather:
                tomorrow = weather.get('tomorrow', {})
                condition = tomorrow.get('weather', '')
                if '雨' in condition or '曇' in condition:
                    recommendations.append('☔ 明日は発電量低下予想')
                    recommendations.append('→ 今夜の放電を控えめに設定推奨')
                    recommendations.append('→ バッテリー残量80%以上を維持')
                elif '晴' in condition:
                    recommendations.append('☀️ 明日は好天で高発電予想')
                    recommendations.append('→ 今夜は積極的放電OK')
                    recommendations.append('→ バッテリー残量50%程度まで使用可能')
                if season == '夏':
                    recommendations.append('🌞 夏期間: 午後の高温による効率低下注意')
                elif season == '冬':
                    recommendations.append('❄️ 冬期間: 朝の霜・積雪チェック推奨')
            return '\n'.join(recommendations) if recommendations else '標準運用を継続'
        except Exception as e:
            return f'推奨生成エラー: {e}'