"""拡張版メール通知モジュール"""
import os
import smtplib
import logging
import json
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class EmailNotifier:

    def _load_settings(self):
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                if 'email' not in settings:
                    settings['email'] = {'smtp_server': '', 'smtp_port': 587, 'smtp_user': '', 'smtp_password': '', 'sender': '', 'recipients': []}
                    with open(self.settings_file, 'w') as f:
                        json.dump(settings, f, indent=2)
                return settings
            else:
                self.logger.error(f'設定ファイルが見つかりません: {self.settings_file}')
                return {}
        except Exception as e:
            self.logger.error(f'設定ファイル読み込みエラー: {e}')
            return {}

    def __init__(self, settings_file=None):
        if settings_file is None:
            self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        else:
            self.settings_file = settings_file
        self.settings = self._load_settings()
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.charts_dir = os.path.join(self.data_dir, 'charts')
        os.makedirs(self.charts_dir, exist_ok=True)
        self.logger = logging.getLogger('email_notifier')
        self._setup_logging()
        self.notes = []

    def _setup_logging(self):
        """ロギング設定"""
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"email_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def _is_unknown_status(self, status):
        """バッテリーの状態が「不明」かどうかを判定する"""
        if status is None:
            return True
        return status.startswith('不明') or 'unknown' in status.lower() or '不明' in status
        log_file = os.path.join(log_dir, f"email_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

def _generate_battery_soc_chart(self, data, date_str):
    """
    バッテリーSOC推移グラフを生成します。

    データはリスト形式またはディクショナリ形式の両方に対応します。

    Args:
        data: JSON形式のデータ（リストまたはディクショナリ）
        date_str: 日付文字列（YYYYMMDD形式）

    Returns:
        str: 生成されたグラフファイルのパス、失敗した場合はNone
    """
    try:
        chart_file = os.path.join(self.charts_dir, f'battery_soc_{date_str}.png')
        if os.path.exists(chart_file):
            self.logger.info(f'既存のバッテリーSOCグラフを使用します: {chart_file}')
            return chart_file
        times = []
        soc_values = []
        if isinstance(data, list):
            for item in data:
                if 'timestamp' in item and 'parameters' in item:
                    if 'datetime' in item:
                        dt = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')
                    else:
                        dt = datetime.fromtimestamp(item['timestamp'])
                    if '0x0100' in item['parameters']:
                        soc = item['parameters']['0x0100'].get('value')
                        if soc is not None:
                            times.append(dt)
                            soc_values.append(soc)
        elif isinstance(data, dict) and 'parameters' in data:
            for param in data['parameters']:
                if isinstance(param, dict) and param.get('name') == 'battery_soc' and ('timestamp' in param):
                    soc = float(param.get('value', 0))
                    try:
                        timestamp = param.get('timestamp').replace('Z', '+00:00')
                        dt = datetime.fromisoformat(timestamp)
                        times.append(dt)
                        soc_values.append(soc)
                    except (ValueError, AttributeError) as e:
                        self.logger.warning(f'タイムスタンプ解析エラー: {e}')
        if not soc_values or len(soc_values) < 2:
            self.logger.warning(f'グラフ生成: SOCデータが不足しています（点数: {len(soc_values)}）')
            return None
        plt.figure(figsize=(10, 6))
        plt.plot(times, soc_values, 'b-', marker='o', markersize=4, linewidth=1.5)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.fill_between(times, 0, soc_values, alpha=0.1, color='blue')
        plt.title(f'バッテリーSOC推移 ({self._format_date_jp(date_str)})', fontsize=14)
        plt.xlabel('時刻', fontsize=12)
        plt.ylabel('SOC (%)', fontsize=12)
        plt.ylim(0, 100)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig(chart_file, dpi=100, bbox_inches='tight')
        plt.close()
        self.logger.info(f'バッテリーSOCグラフを保存しました: {chart_file}')
        return chart_file
    except Exception as e:
        self.logger.error(f'グラフ生成エラー: {e}')
        self.logger.debug(traceback.format_exc())
        return None

    def find_latest_data_file(self, target_date=None):
        """
        指定された日付のデータファイルを検索し、ない場合は最新のファイルを返す

        Args:
            target_date: 検索する日付（YYYYMMDD形式、Noneの場合は前日）

        Returns:
            ファイルパスと日付
        """
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(data_dir):
            self.logger.error(f'データディレクトリが存在しません: {data_dir}')
            return (None, None)
        if target_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime('%Y%m%d')
        file_prefix = self.settings.get('files', {}).get('data_prefix', 'data_')
        target_file = os.path.join(data_dir, f'{file_prefix}{target_date}.json')
        if os.path.exists(target_file):
            return (target_file, target_date)
        self.logger.warning(f'日付 {target_date} のデータファイルが見つかりません: {target_file}')
        data_files = []
        file_pattern = os.path.join(data_dir, f'{file_prefix}*.json')
        for file in glob.glob(file_pattern):
            try:
                file_name = os.path.basename(file)
                date_str = file_name[len(file_prefix):-5]
                datetime.strptime(date_str, '%Y%m%d')
                data_files.append((file, date_str))
            except ValueError:
                continue
        if not data_files:
            self.logger.error('利用可能なデータファイルがありません')
            return (None, None)
        data_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = data_files[0][0]
        latest_date = data_files[0][1]
        self.logger.warning(f'最新の利用可能なデータを使用します: {latest_date}')
        return (latest_file, latest_date)

    def _format_date_jp(self, date_str):
        """YYYYMMDD形式の日付を日本語表記に変換"""
        try:
            d = datetime.strptime(date_str, '%Y%m%d')
            return f'{d.year}年{d.month}月{d.day}日'
        except BaseException:
            return date_str

    def send_daily_report(self, date=None):
        """日次レポートを送信する"""
        try:
            self.logger.info(f"日次レポート送信を開始します（日付: {date or '前日'}）")
            data_file, actual_date = self.find_latest_data_file(date)
            if data_file is None:
                self.logger.error('レポート用データが見つかりません')
                return False
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                self.logger.error(f'データファイル読み込みエラー: {e}')
                return False
            battery_data = self._extract_battery_data(data)
            season_info = self._determine_season()
            weather_data = self._get_weather_forecast()
            recommended_settings = self._calculate_recommended_settings(season_info, weather_data)
            chart_path = self._generate_battery_soc_chart(data, actual_date)
            subject = f'🌸 HANAZONOシステム 日次レポート {self._format_date_jp(actual_date)}'
            body_text = self._generate_text_report(actual_date, battery_data, season_info, recommended_settings, weather_data)
            self.logger.info(f'生成されたテキストレポート: {body_text[:100]}...')
            body_text = body_text.replace('LVYUANソーラー蓄電システム日次レポート', 'HANAZONOシステム 日次レポート')
            import re
            body_text = re.sub('(\\d{4}年\\d{2}月\\d{2}日 \\d{2}:\\d{2}):\\d{2}', '\\1', body_text)
            body_text = re.sub('気温: (\\d+)\\.(\\d+)℃ 〜 (\\d+)\\.(\\d+)℃', '気温: \\1℃ 〜 \\3℃', body_text)
            body_text = re.sub('電圧\\t([\\d\\.]+)000+(\\d) V', '電圧\\t\\1\\2 V', body_text)
            body_text = re.sub('電圧\\t(\\d+\\.\\d{1,2})\\d* V', '電圧\\t\\1 V', body_text)
            body_text = re.sub('状態\\t不明\\(\\d+\\)\\n', '', body_text)
            body_html = self._generate_html_report(actual_date, battery_data, season_info, recommended_settings, weather_data)
            attachments = []
            if chart_path:
                attachments.append(chart_path)
            result = self._send_email(subject=subject, body_text=body_text, body_html=body_html, attachments=attachments)
            if result:
                self.logger.info(f'日次レポート送信成功: {actual_date}')
            else:
                self.logger.error(f'日次レポート送信失敗: {actual_date}')
            return result
        except Exception as e:
            self.logger.error(f'レポート送信エラー: {e}')
            import traceback
            self.logger.error(traceback.format_exc())
            return False

    def send_ip_change_notification(self, old_ip, new_ip):
        """IPアドレス変更通知メールを送信"""
        if 'email' not in self.settings or not self.settings['email'].get('smtp_server'):
            self.logger.warning('メール設定が構成されていません')
            return False
        subject = f'⚠️ LVYUANシステムIPアドレス変更通知'
        body_text = f'インバーターのIPアドレスが変更されました。\n\n旧IPアドレス: {old_ip}\n新IPアドレス: {new_ip}'
        body_html = f'\n        <html>\n            <body>\n                <h2>インバーターIPアドレス変更通知</h2>\n                <p>インバーターのIPアドレスが変更されました。</p>\n                <ul>\n                    <li>旧IPアドレス: <b>{old_ip}</b></li>\n                    <li>新IPアドレス: <b>{new_ip}</b></li>\n                </ul>\n                <p>設定が必要な場合は更新してください。</p>\n            </body>\n        </html>\n        '
        return self._send_email(subject=subject, body_text=body_text, body_html=body_html)

    def append_note(self, note_text):
        """
        レポートに注記を追加する

        Args:
            note_text: 追加する注記テキスト
        """
        if not hasattr(self, 'notes'):
            self.notes = []
        self.notes.append(note_text)
        self.logger.info(f'レポート注記を追加: {note_text}')

    def _generate_notes_html(self):
        """注記からHTMLを生成する"""
        if hasattr(self, 'notes') and self.notes:
            html = "<hr><div style='color: #FF6600; font-style: italic; margin-top: 20px;'>"
            for note in self.notes:
                html += f'<p>※ {note}</p>'
            html += '</div>'
            notes_copy = self.notes.copy()
            self.notes = []
            return html
        return ''

    def _extract_battery_data(self, data):
        """
        JSONデータからバッテリー状態情報を抽出します。

        データファイルのJSON構造に基づいて、バッテリーのSOC、電圧、電流などを
        抽出して辞書形式で返します。

        Args:
            data (dict/list): データファイルから読み込んだJSONデータ

        Returns:
            dict: 以下のキーを持つバッテリー情報辞書
                - soc: バッテリー残量(%)
                - voltage: バッテリー電圧(V)
                - current: バッテリー電流(A)
                - power: バッテリー電力(W)
                - status: バッテリー状態
        """
        battery_data = {'soc': None, 'voltage': None, 'current': None, 'power': None, 'status': None}
        try:
            if isinstance(data, list) and len(data) > 0:
                data_item = data[0]
                if 'parameters' in data_item and isinstance(data_item['parameters'], dict):
                    params = data_item['parameters']
                    if '0x0100' in params:
                        battery_data['soc'] = params['0x0100'].get('value')
                    if '0x0101' in params:
                        battery_data['voltage'] = params['0x0101'].get('value')
                    if '0x0102' in params:
                        battery_data['current'] = params['0x0102'].get('value')
                    if '0x020E' in params:
                        battery_data['status'] = params['0x020E'].get('formatted_value')
                    if battery_data['voltage'] is not None and battery_data['current'] is not None:
                        current = battery_data['current']
                        if -1000 <= current <= 1000:
                            battery_data['power'] = battery_data['voltage'] * current
            self.logger.debug(f'バッテリーデータ抽出結果: {battery_data}')
            return battery_data
        except Exception as e:
            self.logger.error(f'バッテリーデータ抽出中にエラーが発生しました: {e}')
            self.logger.debug(traceback.format_exc())
            return battery_data

    def _determine_season(self):
        """
        現在の日付から季節を判定します。

        季節区分：
        - 冬季(12-3月): 12月から3月まで
        - 春季(4-6月): 4月から6月まで
        - 夏季(7-9月): 7月から9月まで
        - 秋季(10-11月): 10月から11月まで

        Returns:
            dict: 季節情報の辞書
                - name: 季節名（日本語）
                - emoji: 季節を表す絵文字
                - code: 季節コード（英語）
        """
        now = datetime.now()
        month = now.month
        if month == 12 or 1 <= month <= 3:
            season_name = '冬季'
            season_emoji = '❄️'
            season_code = 'winter'
        elif 4 <= month <= 6:
            season_name = '春季'
            season_emoji = '🌸'
            season_code = 'spring'
        elif 7 <= month <= 9:
            season_name = '夏季'
            season_emoji = '☀️'
            season_code = 'summer'
        else:
            season_name = '秋季'
            season_emoji = '🍁'
            season_code = 'autumn'
        self.logger.debug(f'季節判定結果: {season_name}({season_code})')
        return {'name': season_name, 'emoji': season_emoji, 'code': season_code}

    def _get_weather_forecast(self):
        """
        OpenWeatherMapから天気予報データを取得します。

        config.jsonまたはsettings.jsonからAPIキーと位置情報を取得し、
        3日間の天気予報データを取得して返します。

        Returns:
            dict: 天気予報データを含む辞書
                - current: 現在の天気情報
                - forecast: 予報データ（今日、明日、明後日）
        """
        try:
            api_key = self.settings.get('openweathermap', {}).get('api_key', '')
            location = self.settings.get('openweathermap', {}).get('location', '高松市')
            if not api_key:
                self.logger.warning('OpenWeatherMap APIキーが設定されていません。モックデータを使用します。')
                return self._get_mock_weather_data()
            base_url = 'https://api.openweathermap.org/data/2.5/forecast'
            params = {'q': location, 'appid': api_key, 'units': 'metric', 'lang': 'ja'}
            import requests
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                self.logger.error(f'天気予報の取得に失敗: {response.status_code} - {response.text}')
                return self._get_mock_weather_data()
            forecast_data = response.json()
            now = datetime.now()
            today = now.date()
            tomorrow = today + timedelta(days=1)
            day_after = today + timedelta(days=2)
            daily_forecasts = {'today': {'condition': '', 'max_temp': -100, 'min_temp': 100}, 'tomorrow': {'condition': '', 'max_temp': -100, 'min_temp': 100}, 'day_after': {'condition': '', 'max_temp': -100, 'min_temp': 100}}
            for item in forecast_data.get('list', []):
                forecast_dt = datetime.fromtimestamp(item['dt'])
                forecast_date = forecast_dt.date()
                temp = item['main']['temp']
                condition = item['weather'][0]['description']
                target_dict = None
                if forecast_date == today:
                    target_dict = daily_forecasts['today']
                elif forecast_date == tomorrow:
                    target_dict = daily_forecasts['tomorrow']
                elif forecast_date == day_after:
                    target_dict = daily_forecasts['day_after']
                if target_dict:
                    if temp > target_dict['max_temp']:
                        target_dict['max_temp'] = temp
                    if temp < target_dict['min_temp']:
                        target_dict['min_temp'] = temp
                    if forecast_dt.hour in [11, 12, 13, 14] and (not target_dict['condition']):
                        target_dict['condition'] = condition
            for day, data in daily_forecasts.items():
                if not data['condition'] and forecast_data.get('list'):
                    data['condition'] = forecast_data['list'][0]['weather'][0]['description']
            if daily_forecasts['today']['max_temp'] == -100 or daily_forecasts['today']['min_temp'] == 100:
                if forecast_data.get('list'):
                    current_temp = forecast_data['list'][0]['main']['temp']
                    daily_forecasts['today']['max_temp'] = max(daily_forecasts['today']['max_temp'], current_temp)
                    daily_forecasts['today']['min_temp'] = min(daily_forecasts['today']['min_temp'], current_temp)
                    if not daily_forecasts['today']['condition']:
                        daily_forecasts['today']['condition'] = forecast_data['list'][0]['weather'][0]['description']
            result = {'current': {'date': today.strftime('%Y-%m-%d'), 'condition': daily_forecasts['today']['condition'], 'temp': forecast_data['list'][0]['main']['temp'] if forecast_data.get('list') else 20, 'humidity': forecast_data['list'][0]['main']['humidity'] if forecast_data.get('list') else 65}, 'forecast': {'today': {'condition': daily_forecasts['today']['condition'], 'max_temp': daily_forecasts['today']['max_temp'], 'min_temp': daily_forecasts['today']['min_temp']}, 'tomorrow': {'condition': daily_forecasts['tomorrow']['condition'], 'max_temp': daily_forecasts['tomorrow']['max_temp'], 'min_temp': daily_forecasts['tomorrow']['min_temp']}, 'day_after': {'condition': daily_forecasts['day_after']['condition'], 'max_temp': daily_forecasts['day_after']['max_temp'], 'min_temp': daily_forecasts['day_after']['min_temp']}}}
            sunny_days = sum((1 for day in daily_forecasts.values() if '晴' in day['condition']))
            rainy_days = sum((1 for day in daily_forecasts.values() if '雨' in day['condition']))
            result['forecast']['sunny_days'] = sunny_days
            result['forecast']['rainy_days'] = rainy_days
            self.logger.debug(f'天気予報データを取得しました: {location}')
            return result
        except Exception as e:
            self.logger.error(f'天気予報データの取得中にエラーが発生しました: {e}')
            self.logger.debug(traceback.format_exc())
            return self._get_mock_weather_data()

    def _get_mock_weather_data(self):
        """
        APIキーがない場合や取得に失敗した場合に使用するモックデータを生成

        Returns:
            dict: モック天気予報データ
        """
        now = datetime.now()
        return {'current': {'date': now.strftime('%Y-%m-%d'), 'condition': '晴れ', 'temp': 22, 'humidity': 65}, 'forecast': {'today': {'condition': '晴れ', 'max_temp': 25, 'min_temp': 18}, 'tomorrow': {'condition': '曇り', 'max_temp': 24, 'min_temp': 17}, 'day_after': {'condition': '雨', 'max_temp': 22, 'min_temp': 16}, 'sunny_days': 1, 'rainy_days': 1}}

    def _calculate_recommended_settings(self, season_info, weather_data=None):
        """
        季節と天気に基づいて推奨設定値を計算します。

        Args:
            season_info (dict): 季節情報（_determine_season()メソッドの戻り値）
            weather_data (dict): 天気予報データ（_get_weather_forecast()メソッドの戻り値）

        Returns:
            dict: 推奨設定情報の辞書
                - charge_current: 推奨充電電流(A)
                - charge_time: 推奨充電時間(分)
                - output_soc: 推奨出力切替SOC(%)
                - type: 運用タイプ（A:変動型/B:省管理型）
                - weather_note: 天気による調整があれば、その理由（オプション）
        """
        base_settings = {'winter': {'charge_current': 60, 'charge_time': 60, 'output_soc': 60, 'type': 'B'}, 'spring': {'charge_current': 50, 'charge_time': 45, 'output_soc': 45, 'type': 'B'}, 'summer': {'charge_current': 35, 'charge_time': 30, 'output_soc': 35, 'type': 'B'}, 'autumn': {'charge_current': 50, 'charge_time': 45, 'output_soc': 45, 'type': 'B'}}
        season_code = season_info['code']
        settings = base_settings.get(season_code, base_settings['spring'])
        if weather_data and 'forecast' in weather_data:
            forecast = weather_data['forecast']
            if forecast.get('sunny_days', 0) >= 3:
                settings['charge_current'] -= 5
                settings['charge_time'] -= 5
                settings['output_soc'] -= 5
                settings['weather_note'] = '晴天が続くため、パラメーターを下方調整'
            elif forecast.get('rainy_days', 0) >= 3:
                settings['charge_current'] += 5
                settings['charge_time'] += 10
                settings['output_soc'] += 10
                settings['weather_note'] = '雨天が続くため、パラメーターを上方調整'
            elif forecast.get('today', {}).get('max_temp', 0) >= 35:
                settings['charge_current'] -= 10
                settings['charge_time'] -= 10
                settings['output_soc'] -= 10
                settings['weather_note'] = '猛暑日予報のため、パラメーターを下方調整'
        return settings

    def _generate_text_report(self, date_str, battery_data, season_info, recommended_settings, weather_data):
        """テキスト形式のレポートを生成する"""
        now = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        text = f'HANAZONOシステム 日次レポート\n{now}\n\n'
        text += '■天気予報\n'
        if weather_data and 'forecast' in weather_data:
            forecast = weather_data['forecast']
            if 'today' in forecast:
                today = datetime.now().date()
                today_weather = forecast['today']
                text += f"【今日】{today.month}月{today.day}日({self._get_weekday(today)}): {self._get_weather_emoji(today_weather['condition'])} {today_weather['condition']}\n\n"
                text += f"気温: {int(round(today_weather['min_temp']))}℃ 〜 {int(round(today_weather['max_temp']))}℃\n\n"
            if 'tomorrow' in forecast:
                tomorrow = today + timedelta(days=1)
                tomorrow_weather = forecast['tomorrow']
                text += f"【明日】{tomorrow.month}月{tomorrow.day}日({self._get_weekday(tomorrow)}): {self._get_weather_emoji(tomorrow_weather['condition'])} {tomorrow_weather['condition']}\n\n"
                text += f"気温: {int(round(tomorrow_weather['min_temp']))}℃ 〜 {int(round(tomorrow_weather['max_temp']))}℃\n\n"
            if 'day_after' in forecast:
                day_after = today + timedelta(days=2)
                day_after_weather = forecast['day_after']
                text += f"【明後日】{day_after.month}月{day_after.day}日({self._get_weekday(day_after)}): {self._get_weather_emoji(day_after_weather['condition'])} {day_after_weather['condition']}\n\n"
                text += f"気温: {int(round(day_after_weather['min_temp']))}℃ 〜 {int(round(day_after_weather['max_temp']))}℃\n\n"
        else:
            text += '天気予報データがありません\n\n'
        text += '\n■季節判定\n'
        text += f"{season_info['emoji']} {season_info['name']}\n\n"
        text += '\n■推奨設定\n'
        if 'type' in recommended_settings:
            text += f"⚡ タイプ{recommended_settings['type']}（標準設定）\n\n"
        charge_current_id = self.settings.get('inverter_parameters', {}).get('charge_current_id', '07')
        charge_time_id = self.settings.get('inverter_parameters', {}).get('charge_time_id', '10')
        soc_setting_id = self.settings.get('inverter_parameters', {}).get('soc_setting_id', '62')
        charge_current = recommended_settings.get('charge_current', 'N/A')
        text += f'充電電流\t{charge_current}A (パラメータID: {charge_current_id})\n'
        charge_time = recommended_settings.get('charge_time', 'N/A')
        text += f'充電時間\t{charge_time}分 (パラメータID: {charge_time_id})\n'
        soc = recommended_settings.get('output_soc', recommended_settings.get('cutoff_soc', 'N/A'))
        text += f'SOC設定\t{soc}% (パラメータID: {soc_setting_id})\n'
        if 'weather_note' in recommended_settings:
            text += f"\n※ {recommended_settings['weather_note']}\n"
        text += '\n■バッテリー状態\n'
        if any([battery_data.get(key) is not None for key in battery_data]):
            if battery_data.get('soc') is not None:
                text += f"SOC\t{battery_data['soc']}%\n"
            if battery_data.get('voltage') is not None:
                text += f"電圧\t{round(battery_data['voltage'], 1)} V\n"
            if battery_data.get('current') is not None:
                text += f"電流\t{round(battery_data['current'], 1)} A\n"
            if battery_data.get('power') is not None:
                text += f"電力\t{round(battery_data['power'], 1)} W\n"
            if battery_data.get('status') is not None and (not self._is_unknown_status(battery_data['status'])):
                text += f"状態\t{battery_data['status']}\n"
        else:
            text += 'バッテリーデータがありません\n'
        if hasattr(self, 'notes') and self.notes:
            text += '\n■注記\n'
            for note in self.notes:
                text += f'{note}\n\n'
        footer_text = self.settings.get('notification', {}).get('email', {}).get('template', {}).get('footer', 'この設定は天気予報と季節に基づいて自動的に計算されています。\n\n実際の設定変更は手動で行う必要があります。\n\n本メールは自動送信されています。')
        text += f'\n{footer_text}'
        return text

    def _get_weekday(self, date):
        """曜日を返す"""
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        return weekdays[date.weekday()]

    def _get_weather_emoji(self, condition):
        """天気に合わせた絵文字を返す"""
        weather_icons = self.settings.get('weather_icons', {'晴': '☀️', '晴れ': '☀️', '晴天': '☀️', '曇': '☁️', '曇り': '☁️', '曇天': '☁️', '曇りがち': '⛅', '厚い雲': '☁️', '雨': '🌧️', '小雨': '🌦️', '雪': '❄️', '霧': '🌫️', '雷': '⚡', '雷雨': '⛈️'})
        return weather_icons.get(condition, '🌈')

    def _generate_html_report(self, date_str, battery_data, season_info, recommended_settings, weather_data, chart_path=None):
        """
        HTML形式のレポート本文を生成します。

        Args:
            date_str (str): レポート対象日付（YYYYMMDD形式）
            battery_data (dict): バッテリー状態データ
            season_info (dict): 季節情報
            recommended_settings (dict): 推奨設定情報
            weather_data (dict): 天気予報データ
            chart_path (str, optional): バッテリーSOCグラフのパス

        Returns:
            str: HTML形式のレポート本文
        """
        formatted_date = self._format_date_jp(date_str)
        now = datetime.now()
        weekday_names = ['月', '火', '水', '木', '金', '土', '日']
        html_template = '\n        <html>\n        <head>\n            <style>\n                body {{ font-family: \'Helvetica Neue\', Arial, sans-serif; line-height: 1.6; color: #333; }}\n                .container {{ width: 100%%; max-width: 800px; margin: 0 auto; }}\n                .section {{ margin-bottom: 25px; padding: 15px; background: #f9f9f9; border-radius: 5px; }}\n                .section-header {{ font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}\n                .item-label {{ font-weight: bold; }}\n                .item-value {{ margin-left: 10px; }}\n                table {{ border-collapse: collapse; width: 100%%; margin-bottom: 10px; }}\n                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}\n                th {{ background-color: #f2f2f2; }}\n                .weather-icon {{ font-size: 24px; margin-right: 10px; vertical-align: middle; }}\n                .note {{ color: #FF6600; font-style: italic; }}\n                .footer {{ margin-top: 25px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666; }}\n            </style>\n        </head>\n        <body>\n            <div class="container">\n                <h2>LVYUANソーラー蓄電システム日次レポート</h2>\n                <p><strong>実行日時:</strong> {0}</p>\n        '
        html = html_template.format(now.strftime('%Y年%m月%d日 %H:%M:%S'))
        if weather_data:
            html += '\n                <div class="section">\n                    <div class="section-header">■天気予報</div>\n            '
            today_date = datetime.now()
            tomorrow_date = today_date + timedelta(days=1)
            day_after_date = today_date + timedelta(days=2)

            def get_weather_emoji(condition):
                if '晴' in condition and ('曇' in condition or 'くもり' in condition):
                    return '⛅'
                elif '晴' in condition:
                    return '☀️'
                elif '雨' in condition:
                    return '🌧️'
                elif '曇' in condition or 'くもり' in condition:
                    return '☁️'
                elif '雪' in condition:
                    return '❄️'
                elif '雷' in condition:
                    return '⚡'
                else:
                    return '🌤️'
            today_weather = weather_data['forecast']['today']
            today_emoji = get_weather_emoji(today_weather['condition'])
            tomorrow_weather = weather_data['forecast']['tomorrow']
            tomorrow_emoji = get_weather_emoji(tomorrow_weather['condition'])
            day_after_weather = weather_data['forecast']['day_after']
            day_after_emoji = get_weather_emoji(day_after_weather['condition'])
            html += f"""\n                    <p><strong>【今日】</strong>{today_date.month}月{today_date.day}日({weekday_names[today_date.weekday()]}) <span class="weather-icon">{today_emoji}</span> {today_weather['condition']}</p>\n                    <p style="margin-left: 20px;">気温: {today_weather['min_temp']}℃ 〜 {today_weather['max_temp']}℃</p>\n                    <p><strong>【明日】</strong>{tomorrow_date.month}月{tomorrow_date.day}日({weekday_names[tomorrow_date.weekday()]}) <span class="weather-icon">{tomorrow_emoji}</span> {tomorrow_weather['condition']}</p>\n                    <p style="margin-left: 20px;">気温: {tomorrow_weather['min_temp']}℃ 〜 {tomorrow_weather['max_temp']}℃</p>\n                    <p><strong>【明後日】</strong>{day_after_date.month}月{day_after_date.day}日({weekday_names[day_after_date.weekday()]}) <span class="weather-icon">{day_after_emoji}</span> {day_after_weather['condition']}</p>\n                    <p style="margin-left: 20px;">気温: {day_after_weather['min_temp']}℃ 〜 {day_after_weather['max_temp']}℃</p>\n                </div>\n            """
        html += f"""\n                <div class="section">\n                    <div class="section-header">■季節判定</div>\n                    <p>{season_info['emoji']} {season_info['name']}</p>\n                </div>\n        """
        html += f"""\n                <div class="section">\n                    <div class="section-header">■推奨設定</div>\n                    <p><strong>⚡ タイプ{recommended_settings['type']}（標準設定）</strong></p>\n                    <table>\n                        <tr>\n                            <td class="item-label">充電電流</td>\n                            <td>{recommended_settings['charge_current']}A (パラメータID: 07)</td>\n                        </tr>\n                        <tr>\n                            <td class="item-label">充電時間</td>\n                            <td>{recommended_settings['charge_time']}分 (パラメータID: 10)</td>\n                        </tr>\n                        <tr>\n                            <td class="item-label">SOC設定</td>\n                            <td>{recommended_settings['output_soc']}% (パラメータID: 62)</td>\n                        </tr>\n                    </table>\n        """
        if 'weather_note' in recommended_settings:
            html += f"<p class='note'>※ {recommended_settings['weather_note']}</p>"
        html += '</div>'
        html += '\n                <div class="section">\n                    <div class="section-header">■バッテリー状態</div>\n        '
        if any([battery_data[key] is not None for key in battery_data]):
            html += '<table>'
            if battery_data['soc'] is not None:
                html += f"<tr><td class='item-label'>SOC</td><td>{battery_data['soc']}%</td></tr>"
            if battery_data['voltage'] is not None:
                html += f"<tr><td class='item-label'>電圧</td><td>{battery_data['voltage']} V</td></tr>"
            if battery_data['current'] is not None:
                html += f"<tr><td class='item-label'>電流</td><td>{battery_data['current']} A</td></tr>"
            if battery_data['power'] is not None:
                html += f"<tr><td class='item-label'>電力</td><td>{battery_data['power']} W</td></tr>"
            if battery_data['status'] is not None:
                html += f"<tr><td class='item-label'>状態</td><td>{battery_data['status']}</td></tr>"
            html += '</table>'
        else:
            html += '<p>バッテリーデータがありません</p>'
        html += '</div>'
        if chart_path:
            html += f'\n                <div class="section">\n                    <div class="section-header">■バッテリーSOC推移</div>\n                    <img src="cid:{os.path.basename(chart_path)}" width="100%" style="max-width: 800px;" />\n                </div>\n            '
        html += '\n                <div class="section">\n                    <div class="section-header">■注記</div>\n                    <p>この設定は天気予報と季節に基づいて自動的に計算されています。</p>\n                    <p>実際の設定変更は手動で行う必要があります。</p>\n        '
        if hasattr(self, 'notes') and self.notes:
            for note in self.notes:
                html += f"<p class='note'>※ {note}</p>"
        html += '\n                </div>\n\n                <div class="footer">\n                    <hr>\n                    <p>本メールは自動送信されています。</p>\n                </div>\n            </div>\n        </body>\n        </html>\n        '
        return html

    def _send_email(self, subject, body_text, body_html=None, to_email=None, attachments=None):
        """メールの送信"""
        if to_email is None:
            to_email = self.settings.get('email', {}).get('recipients', [])
            if not to_email:
                self.logger.error('送信先メールアドレスが設定されていません')
                return False
        if isinstance(to_email, str):
            to_email = [to_email]
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.settings.get('email', {}).get('sender', 'no-reply@example.com')
            msg['To'] = ', '.join(to_email)
            msg['Date'] = formatdate(localtime=True)
            if body_text:
                msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
            if body_html:
                msg.attach(MIMEText(body_html, 'html', 'utf-8'))
            if attachments:
                for attachment in attachments:
                    if attachment and os.path.exists(attachment):
                        with open(attachment, 'rb') as f:
                            part = MIMEImage(f.read())
                            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                            msg.attach(part)
            server = smtplib.SMTP(self.settings.get('email', {}).get('smtp_server', 'localhost'), self.settings.get('email', {}).get('smtp_port', 25))
            if self.settings.get('email', {}).get('use_tls', False):
                server.starttls()
            if self.settings.get('email', {}).get('smtp_user') and self.settings.get('email', {}).get('smtp_password'):
                server.login(self.settings.get('email', {}).get('smtp_user'), self.settings.get('email', {}).get('smtp_password'))
            server.sendmail(msg['From'], to_email, msg.as_string())
            server.quit()
            self.logger.info(f'メール送信成功: {subject}')
            return True
        except Exception as e:
            self.logger.error(f'メール送信エラー: {e}')
            import traceback
            self.logger.debug(traceback.format_exc())
            return False

    def send_alert(self, to_email=None, subject=None, body=None):
        """
        管理者向けアラートメールを送信する

        Args:
            to_email: アラート送信先（未指定時は設定ファイルから）
            subject: メール件名（未指定時はデフォルト）
            body: メール本文（未指定時はデフォルト）

        Returns:
            bool: 送信成功時はTrue、失敗時はFalse
        """
        if to_email is None:
            to_email = self.settings.get('admin_email', self.settings.get('email', {}).get('recipients', [''])[0])
        if subject is None:
            subject = '⚠️ LVYUANシステム警告：データ収集エラー'
        if body is None:
            body = 'レポート生成に必要なデータが見つかりません。データ収集プロセスを確認してください。'
        self.logger.info(f'アラートメール送信: {subject}')
        return self._send_email(to_email=to_email, subject=subject, body_text=body, body_html=f'<html><body><p>{body}</p></body></html>')
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    notifier = EmailNotifier()
    notifier.send_daily_report()