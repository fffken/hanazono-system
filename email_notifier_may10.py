#!/usr/bin/env python3
"""拡張版メール通知モジュール"""

import os
import smtplib
import logging
import json
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate  # この行を追加
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import glob


class EmailNotifier:
    def __init__(self, settings_file=None):
        # 設定ファイルのパス
        if settings_file is None:
            self.settings_file = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'settings.json')
        else:
            self.settings_file = settings_file

        # 設定の読み込み
        self.settings = self._load_settings()

        # データディレクトリ
        self.data_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data')

        # 画像ディレクトリ
        self.charts_dir = os.path.join(self.data_dir, 'charts')
        os.makedirs(self.charts_dir, exist_ok=True)

        # ロガー設定
        self.logger = logging.getLogger("email_notifier")
        self._setup_logging()

        # 注記リスト初期化
        self.notes = []

    def _load_settings(self):
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)

                # メール設定がない場合は追加
                if "email" not in settings:
                    settings["email"] = {
                        "smtp_server": "",
                        "smtp_port": 587,
                        "smtp_user": "",
                        "smtp_password": "",
                        "sender": "",
                        "recipients": []
                    }

                    # 設定保存
                    with open(self.settings_file, 'w') as f:
                        json.dump(settings, f, indent=2)

                return settings
            else:
                self.logger.error(f"設定ファイルが見つかりません: {self.settings_file}")
                return {}
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {e}")
            return {}

    def _setup_logging(self):
        """ロギング設定"""
        log_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir, f'email_{datetime.now().strftime("%Y%m%d")}.log')

        # 既存のハンドラをクリア
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # ハンドラをロガーに追加
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def _is_unknown_status(self, status):
        """バッテリーの状態が「不明」かどうかを判定する"""
        if status is None:
            return True
        return status.startswith("不明") or "unknown" in status.lower() or "不明" in status

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
            # グラフ保存先
            chart_file = os.path.join(
                self.charts_dir, f"battery_soc_{date_str}.png")

            # すでにファイルが存在する場合はそれを返す
            if os.path.exists(chart_file):
                self.logger.info(f"既存のバッテリーSOCグラフを使用します: {chart_file}")
                return chart_file

            # データからSOC値を取得
            times = []
            soc_values = []

            # データ形式に応じた処理
            if isinstance(data, list):
                # リスト形式データの処理
                for item in data:
                    if "timestamp" in item and "parameters" in item:
                        # タイムスタンプを日時形式に変換
                        if "datetime" in item:
                            dt = datetime.strptime(
                                item["datetime"], "%Y-%m-%d %H:%M:%S")
                        else:
                            dt = datetime.fromtimestamp(item["timestamp"])

                        # SOC値を取得
                        if "0x0100" in item["parameters"]:
                            soc = item["parameters"]["0x0100"].get("value")
                            if soc is not None:
                                times.append(dt)
                                soc_values.append(soc)

            elif isinstance(data, dict) and "parameters" in data:
                # ディクショナリ形式データの処理
                for param in data["parameters"]:
                    if isinstance(param, dict) and param.get("name") == "battery_soc" and "timestamp" in param:
                        soc = float(param.get("value", 0))
                        try:
                            # ISOフォーマットのタイムスタンプ処理
                            timestamp = param.get(
                                "timestamp").replace("Z", "+00:00")
                            dt = datetime.fromisoformat(timestamp)
                            times.append(dt)
                            soc_values.append(soc)
                        except (ValueError, AttributeError) as e:
                            self.logger.warning(f"タイムスタンプ解析エラー: {e}")

            # データがない場合や不十分な場合
            if not soc_values:
                self.logger.warning(f"グラフ生成: SOCデータが存在しません")
                return None
            elif len(soc_values) == 1:
                # データが1つしかない場合、同じ値で2つ目のポイントを作成（1時間後）
                self.logger.info(f"グラフ生成: SOCデータが1つしかないため、同じ値のポイントを追加します")
                times.append(times[0] + timedelta(hours=1))
                soc_values.append(soc_values[0])

            # グラフ作成
            plt.figure(figsize=(10, 6))
            plt.plot(times, soc_values, 'b-', marker='o',
                     markersize=4, linewidth=1.5)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.fill_between(times, 0, soc_values, alpha=0.1,
                             color='blue')  # 塗りつぶし効果を追加
            plt.title(
                f"バッテリーSOC推移 ({self._format_date_jp(date_str)})", fontsize=14)
            plt.xlabel("時刻", fontsize=12)
            plt.ylabel("SOC (%)", fontsize=12)
            plt.ylim(0, 100)

            # X軸の日時フォーマット
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.gcf().autofmt_xdate()

            # レイアウト調整
            plt.tight_layout()

            # 保存
            plt.savefig(chart_file, dpi=100, bbox_inches='tight')
            plt.close()

            self.logger.info(f"バッテリーSOCグラフを保存しました: {chart_file}")
            return chart_file

        except Exception as e:
            self.logger.error(f"グラフ生成エラー: {e}")
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
        data_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data")
        if not os.path.exists(data_dir):
            self.logger.error(f"データディレクトリが存在しません: {data_dir}")
            return None, None

        # 対象日付の設定（指定がなければ前日）
        if target_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime("%Y%m%d")

        # ファイル名プレフィックスの取得（settings.jsonから）
        file_prefix = self.settings.get(
            'files', {}).get('data_prefix', 'data_')

        # 指定日のファイル検索
        target_file = os.path.join(
            data_dir, f"{file_prefix}{target_date}.json")
        if os.path.exists(target_file):
            return target_file, target_date

        # 指定日のファイルがない場合、全データファイルをリストアップ
        self.logger.warning(
            f"日付 {target_date} のデータファイルが見つかりません: {target_file}")

        data_files = []
        file_pattern = os.path.join(data_dir, f"{file_prefix}*.json")
        for file in glob.glob(file_pattern):
            try:
                file_name = os.path.basename(file)
                # ファイル名から日付部分を抽出
                date_str = file_name[len(file_prefix):-5]
                # 日付形式が有効かチェック
                datetime.strptime(date_str, "%Y%m%d")
                data_files.append((file, date_str))
            except ValueError:
                # 日付形式が無効な場合はスキップ
                continue

        if not data_files:
            self.logger.error("利用可能なデータファイルがありません")
            return None, None

        # 日付でソートして最新のものを取得
        data_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = data_files[0][0]
        latest_date = data_files[0][1]

        self.logger.warning(f"最新の利用可能なデータを使用します: {latest_date}")
        return latest_file, latest_date

    def _format_date_jp(self, date_str):
        """YYYYMMDD形式の日付を日本語表記に変換"""
        try:
            d = datetime.strptime(date_str, "%Y%m%d")
            return f"{d.year}年{d.month}月{d.day}日"
        except:
            return date_str

    def send_daily_report(self, date=None):
        """日次レポートを送信する"""
        try:
            self.logger.info(f"日次レポート送信を開始します（日付: {date or '前日'}）")

            # データファイルの特定（フォールバックあり）
            data_file, actual_date = self.find_latest_data_file(date)
            if data_file is None:
                self.logger.error("レポート用データが見つかりません")
                return False

            # データ読み込み
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                self.logger.error(f"データファイル読み込みエラー: {e}")
                return False

            # バッテリー状態データの抽出
            battery_data = self._extract_battery_data(data)

            # 季節判定
            season_info = self._determine_season()

            # 天気予報取得
            weather_data = self._get_weather_forecast()

            # 推奨設定の計算
            recommended_settings = self._calculate_recommended_settings(
                season_info, weather_data)

            # グラフ生成
            chart_path = self._generate_battery_soc_chart(data, actual_date)

            # メール件名
            # 今日の日付（レポート生成日）
            # 時間帯判定（12時を境に朝/夜と判断）
            current_hour = datetime.now().hour
            time_period = "(07時)" if current_hour < 12 else "(23時)"
            today_formatted = datetime.now().strftime("%Y年%m月%d日")
            subject = f"🌸 HANAZONOシステム 日次レポート {today_formatted} {time_period}"

            # レポート本文の生成
            body_text = self._generate_text_report(
                actual_date, battery_data, season_info, recommended_settings, weather_data
            )

            # テスト用ログ出力
            # 最初の100文字だけログ出力
            self.logger.info(f"生成されたテキストレポート: {body_text[:100]}...")

            # テキスト内容の修正
            # タイトル修正
            body_text = body_text.replace(
                'HANAZONOシステム日次レポート', 'HANAZONOシステム 日次レポート')

            # 時間から秒を削除
            import re
            body_text = re.sub(
                r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}):\d{2}', r'\1', body_text)

            # 小数点以下切り捨て（気温）
            body_text = re.sub(
                r'気温: (\d+)\.(\d+)℃ 〜 (\d+)\.(\d+)℃', r'気温: \1℃ 〜 \3℃', body_text)

            # 電圧小数点調整
            body_text = re.sub(
                r'電圧\t([\d\.]+)000+(\d) V', r'電圧\t\1\2 V', body_text)
            body_text = re.sub(
                r'電圧\t(\d+\.\d{1,2})\d* V', r'電圧\t\1 V', body_text)

            # 不明状態の非表示
            body_text = re.sub(r'状態\t不明\(\d+\)\n', '', body_text)

            body_html = self._generate_html_report(
                actual_date, battery_data, season_info, recommended_settings, weather_data
            )

            # 添付ファイル
            attachments = []
            if chart_path:
                attachments.append(chart_path)

            # メール送信
            result = self._send_email(
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                attachments=attachments
            )

            if result:
                self.logger.info(f"日次レポート送信成功: {actual_date}")
            else:
                self.logger.error(f"日次レポート送信失敗: {actual_date}")

            return result

        except Exception as e:
            self.logger.error(f"レポート送信エラー: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False

    def append_note(self, note_text):
        """
        レポートに注記を追加する

        Args:
            note_text: 追加する注記テキスト
        """
        if not hasattr(self, 'notes'):
            self.notes = []
        self.notes.append(note_text)
        self.logger.info(f"レポート注記を追加: {note_text}")

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
        # 初期値として全てのデータ項目をNoneに設定
        battery_data = {
            "soc": None,
            "voltage": None,
            "current": None,
            "power": None,
            "status": None
        }

        try:
            # データ形式の確認とパラメータへのアクセス
            if isinstance(data, list) and len(data) > 0:
                # リスト形式の場合は最初の項目を使用
                data_item = data[0]
                if "parameters" in data_item and isinstance(data_item["parameters"], dict):
                    params = data_item["parameters"]

                    # SOC
                    if "0x0100" in params:
                        battery_data["soc"] = params["0x0100"].get("value")

                    # 電圧
                    if "0x0101" in params:
                        battery_data["voltage"] = params["0x0101"].get("value")

                    # 電流
                    if "0x0102" in params:
                        battery_data["current"] = params["0x0102"].get("value")

                    # 状態（もし利用可能なら）
                    if "0x020E" in params:
                        battery_data["status"] = params["0x020E"].get(
                            "formatted_value")

                    # 電力は電圧×電流で計算（電流データが異常値でなければ）
                    if battery_data["voltage"] is not None and battery_data["current"] is not None:
                        current = battery_data["current"]
                        # 電流の値が異常に大きい場合は計算しない
                        if -1000 <= current <= 1000:  # 妥当な範囲内のみ
                            battery_data["power"] = battery_data["voltage"] * current

            # 処理結果のログ出力（デバッグ用）
            self.logger.debug(f"バッテリーデータ抽出結果: {battery_data}")

            return battery_data

        except Exception as e:
            # 例外発生時はエラーをログに記録して初期値を返す
            self.logger.error(f"バッテリーデータ抽出中にエラーが発生しました: {e}")
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

        # 月に基づく季節判定
        if month == 12 or 1 <= month <= 3:
            season_name = "冬季"
            season_emoji = "❄️"
            season_code = "winter"
        elif 4 <= month <= 6:
            season_name = "春季"
            season_emoji = "🌸"
            season_code = "spring"
        elif 7 <= month <= 9:
            season_name = "夏季"
            season_emoji = "☀️"
            season_code = "summer"
        else:  # 10-11月
            season_name = "秋季"
            season_emoji = "🍁"
            season_code = "autumn"

        self.logger.debug(f"季節判定結果: {season_name}({season_code})")

        return {
            "name": season_name,
            "emoji": season_emoji,
            "code": season_code
        }

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
            # APIキーと位置情報の取得（settings.jsonから）
            api_key = self.settings.get(
                'openweathermap', {}).get('api_key', '')
            location = self.settings.get(
                'openweathermap', {}).get('location', '高松市')

            if not api_key:
                self.logger.warning(
                    "OpenWeatherMap APIキーが設定されていません。モックデータを使用します。")
                return self._get_mock_weather_data()

            # OpenWeatherMap APIリクエストURLの構築
            base_url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': location,
                'appid': api_key,
                'units': 'metric',  # 摂氏温度を使用
                'lang': 'ja'        # 日本語の天気説明
            }

            # APIリクエストの送信
            import requests
            response = requests.get(base_url, params=params)

            if response.status_code != 200:
                self.logger.error(
                    f"天気予報の取得に失敗: {response.status_code} - {response.text}")
                return self._get_mock_weather_data()

            # レスポンスデータの解析
            forecast_data = response.json()

            # 現在時刻と日付
            now = datetime.now()
            today = now.date()
            tomorrow = today + timedelta(days=1)
            day_after = today + timedelta(days=2)

            # 日付ごとの予報データ収集
            daily_forecasts = {
                'today': {'condition': '', 'max_temp': -100, 'min_temp': 100},
                'tomorrow': {'condition': '', 'max_temp': -100, 'min_temp': 100},
                'day_after': {'condition': '', 'max_temp': -100, 'min_temp': 100}
            }

            # 各予報データを処理
            for item in forecast_data.get('list', []):
                forecast_dt = datetime.fromtimestamp(item['dt'])
                forecast_date = forecast_dt.date()

                # 気温と天気の取得
                temp = item['main']['temp']
                condition = item['weather'][0]['description']

                # 日付に応じてデータを格納
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

                    # 昼間（12時頃）の天気を優先的に使用
                    if forecast_dt.hour in [11, 12, 13, 14] and not target_dict['condition']:
                        target_dict['condition'] = condition

            # 未設定の天気条件を先頭のデータで補完
            for day, data in daily_forecasts.items():
                if not data['condition'] and forecast_data.get('list'):
                    data['condition'] = forecast_data['list'][0]['weather'][0]['description']

            # 未設定の天気条件と極端な温度値を現在の値で補完
            if daily_forecasts['today']['max_temp'] == -100 or daily_forecasts['today']['min_temp'] == 100:
                if forecast_data.get('list'):
                    current_temp = forecast_data['list'][0]['main']['temp']
                    daily_forecasts['today']['max_temp'] = max(
                        daily_forecasts['today']['max_temp'], current_temp)
                    daily_forecasts['today']['min_temp'] = min(
                        daily_forecasts['today']['min_temp'], current_temp)
                    if not daily_forecasts['today']['condition']:
                        daily_forecasts['today']['condition'] = forecast_data['list'][0]['weather'][0]['description']

            # 結果を整形
            result = {
                'current': {
                    'date': today.strftime('%Y-%m-%d'),
                    'condition': daily_forecasts['today']['condition'],
                    'temp': forecast_data['list'][0]['main']['temp'] if forecast_data.get('list') else 20,
                    'humidity': forecast_data['list'][0]['main']['humidity'] if forecast_data.get('list') else 65
                },
                'forecast': {
                    'today': {
                        'condition': daily_forecasts['today']['condition'],
                        'max_temp': daily_forecasts['today']['max_temp'],
                        'min_temp': daily_forecasts['today']['min_temp']
                    },
                    'tomorrow': {
                        'condition': daily_forecasts['tomorrow']['condition'],
                        'max_temp': daily_forecasts['tomorrow']['max_temp'],
                        'min_temp': daily_forecasts['tomorrow']['min_temp']
                    },
                    'day_after': {
                        'condition': daily_forecasts['day_after']['condition'],
                        'max_temp': daily_forecasts['day_after']['max_temp'],
                        'min_temp': daily_forecasts['day_after']['min_temp']
                    }
                }
            }

            # 天気条件の日数をカウント
            sunny_days = sum(1 for day in daily_forecasts.values()
                             if '晴' in day['condition'])
            rainy_days = sum(1 for day in daily_forecasts.values()
                             if '雨' in day['condition'])
            result['forecast']['sunny_days'] = sunny_days
            result['forecast']['rainy_days'] = rainy_days

            self.logger.debug(f"天気予報データを取得しました: {location}")
            return result

        except Exception as e:
            self.logger.error(f"天気予報データの取得中にエラーが発生しました: {e}")
            self.logger.debug(traceback.format_exc())
            return self._get_mock_weather_data()

    def _get_mock_weather_data(self):
        """
        APIキーがない場合や取得に失敗した場合に使用するモックデータを生成

        Returns:
            dict: モック天気予報データ
        """
        now = datetime.now()

        return {
            'current': {
                'date': now.strftime('%Y-%m-%d'),
                'condition': '晴れ',
                'temp': 22,
                'humidity': 65
            },
            'forecast': {
                'today': {
                    'condition': '晴れ',
                    'max_temp': 25,
                    'min_temp': 18
                },
                'tomorrow': {
                    'condition': '曇り',
                    'max_temp': 24,
                    'min_temp': 17
                },
                'day_after': {
                    'condition': '雨',
                    'max_temp': 22,
                    'min_temp': 16
                },
                'sunny_days': 1,
                'rainy_days': 1
            }
        }

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
        # 基本設定（季節ごと）- タイプB（省管理型）
        base_settings = {
            "winter": {
                "charge_current": 60,  # A
                "charge_time": 60,     # 分
                "output_soc": 60,      # %
                "type": "B"            # 運用タイプ
            },
            "spring": {
                "charge_current": 50,
                "charge_time": 45,
                "output_soc": 45,
                "type": "B"
            },
            "summer": {
                "charge_current": 35,
                "charge_time": 30,
                "output_soc": 35,
                "type": "B"
            },
            "autumn": {
                "charge_current": 50,
                "charge_time": 45,
                "output_soc": 45,
                "type": "B"
            }
        }

        # 季節コードから基本設定を取得
        season_code = season_info["code"]
        settings = base_settings.get(season_code, base_settings["spring"])

        # 天気データに基づく調整（実装例）
        if weather_data and "forecast" in weather_data:
            forecast = weather_data["forecast"]

            # 3日以上の晴天予報時
            if forecast.get("sunny_days", 0) >= 3:
                settings["charge_current"] -= 5
                settings["charge_time"] -= 5
                settings["output_soc"] -= 5
                settings["weather_note"] = "晴天が続くため、パラメーターを下方調整"

            # 3日以上の雨天予報時
            elif forecast.get("rainy_days", 0) >= 3:
                settings["charge_current"] += 5
                settings["charge_time"] += 10
                settings["output_soc"] += 10
                settings["weather_note"] = "雨天が続くため、パラメーターを上方調整"

            # 猛暑日予報時（最高気温35℃以上）
            elif forecast.get("today", {}).get("max_temp", 0) >= 35:
                settings["charge_current"] -= 10
                settings["charge_time"] -= 10
                settings["output_soc"] -= 10
                settings["weather_note"] = "猛暑日予報のため、パラメーターを下方調整"

        return settings

    def _generate_text_report(self, date_str, battery_data, season_info, recommended_settings, weather_data):
        """テキスト形式のレポートを生成する"""
        # 対象日付と現在時刻（タイトルと同じフォーマットを使用）
        formatted_date = datetime.now().strftime("%Y年%m月%d日")
        current_time = datetime.now().strftime("%H:%M")

        # レポートタイトル
        text = f"HANAZONOシステム 日次レポート\n{formatted_date} {current_time}\n\n"

        # 天気予報のセクション
        text += "■天気予報\n"
        if weather_data and 'forecast' in weather_data:
            forecast = weather_data['forecast']

            # 今日の天気
            if 'today' in forecast:
                today = datetime.now().date()
                today_weather = forecast['today']
                weather_info = self._parse_weather_condition(
                    today_weather["condition"])
                text += f"【今日】{today.month}月{today.day}日({self._get_weekday(today)}):\n{weather_info["emoji_line"]}\n{weather_info["text_line"]}\n\n"

    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []

        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word

        if current_part:
            parts.append({"condition": current_part.strip()})

        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }

        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""

        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "

        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                text += f"気温: {int(round(today_weather['min_temp']))}℃ 〜 {int(round(today_weather['max_temp']))}℃\n\n"

            # 明日の天気
            if 'tomorrow' in forecast:
                tomorrow = today + timedelta(days=1)
                tomorrow_weather = forecast['tomorrow']
                weather_info = self._parse_weather_condition(tomorrow_weather["condition"])
                text += f"【明日】{tomorrow.month}月{tomorrow.day}日({self._get_weekday(tomorrow)}):\n{weather_info["emoji_line"]}\n{weather_info["text_line"]}\n\n"
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                text += f"気温: {int(round(tomorrow_weather['min_temp']))}℃ 〜 {int(round(tomorrow_weather['max_temp']))}℃\n\n"
            
            # 明後日の天気
            if 'day_after' in forecast:
                day_after = today + timedelta(days=2)
                day_after_weather = forecast['day_after']
                weather_info = self._parse_weather_condition(day_after_weather["condition"])
                text += f"【明後日】{day_after.month}月{day_after.day}日({self._get_weekday(day_after)}):\n{weather_info["emoji_line"]}\n{weather_info["text_line"]}\n\n"
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                text += f"気温: {int(round(day_after_weather['min_temp']))}℃ 〜 {int(round(day_after_weather['max_temp']))}℃\n\n"
        else:
            text += "天気予報データがありません\n\n"
            
        # 季節情報のセクション
        text += "\n■季節判定\n"
        text += f"{season_info['emoji']} {season_info['name']}\n\n"
        
        # 推奨設定のセクション
        text += "\n■推奨設定\n"
        if 'type' in recommended_settings:
            text += f"⚡ タイプ{recommended_settings['type']}（標準設定）\n\n"
        
        # パラメータID
        charge_current_id = self.settings.get('inverter_parameters', {}).get('charge_current_id', '07')
        charge_time_id = self.settings.get('inverter_parameters', {}).get('charge_time_id', '10')
        soc_setting_id = self.settings.get('inverter_parameters', {}).get('soc_setting_id', '62')
        
        # 充電設定の表示
        charge_current = recommended_settings.get('charge_current', 'N/A')
        text += f"充電電流\t{charge_current}A (パラメータID: {charge_current_id})\n"
        
        charge_time = recommended_settings.get('charge_time', 'N/A')
        text += f"充電時間\t{charge_time}分 (パラメータID: {charge_time_id})\n"
        
        soc = recommended_settings.get('output_soc', recommended_settings.get('cutoff_soc', 'N/A'))
        text += f"SOC設定\t{soc}% (パラメータID: {soc_setting_id})\n"
        
        # 天気による調整がある場合
        if "weather_note" in recommended_settings:
            text += f"\n※ {recommended_settings['weather_note']}\n"
            
        # バッテリー状態のセクション
        text += "\n\n■バッテリー状態\n"
        if any([battery_data.get(key) is not None for key in battery_data]):
            if battery_data.get("soc") is not None:
                text += f"SOC\t{battery_data['soc']}%\n"
            if battery_data.get("voltage") is not None:
                # 小数点以下1桁までに丸める
                voltage = int(battery_data['voltage'] * 10) / 10
                text += f"電圧\t{voltage} V\n"
            if battery_data.get("current") is not None:
                # 小数点以下1桁までに丸める
                current = int(battery_data['current'] * 10) / 10
                text += f"電流\t{current} A\n"
            if battery_data.get("power") is not None:
                # 小数点以下1桁までに丸める
                power = int(battery_data['power'] * 10) / 10
                text += f"電力\t{power} W\n"
            # 不明状態は表示しない
            if battery_data.get("status") is not None and not self._is_unknown_status(battery_data["status"]):
                text += f"状態\t{battery_data['status']}\n"
        else:
            text += "バッテリーデータがありません\n"
        
        # 注記セクション
        if hasattr(self, 'notes') and self.notes:
            text += "\n\n■注記\n"
            for note in self.notes:
                text += f"{note}\n\n"
        
        # フッター
        footer_text = self.settings.get('notification', {}).get('email', {}).get('template', {}).get('footer', 
            "この設定は天気予報と季節に基づいて自動的に計算されています。\n\n実際の設定変更は手動で行う必要があります。\n\n本メールは自動送信されています。")
        text += f"\n{footer_text}"
        
        return text

    def _get_weekday(self, date):
        """曜日を返す"""
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        return weekdays[date.weekday()]
        
    def _get_weather_emoji(self, condition):
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
        """天気に合わせた絵文字を返す"""
        weather_icons = self.settings.get("weather_icons", {
            "晴": "☀️", "晴れ": "☀️", "晴天": "☀️",
            "曇": "☁️", "曇り": "☁️", "曇天": "☁️", "曇りがち": "⛅", "厚い雲": "☁️",
            "雨": "🌧️", "小雨": "🌦️",
            "雪": "❄️",
            "霧": "🌫️",
            "雷": "⚡", "雷雨": "⛈️"
                    "晴": "☀️", "晴れ": "☀️", "快晴": "☀️", "晴天": "☀️",
            "曇": "☁️", "曇り": "☁️", "薄曇": "🌤️", "薄曇り": "🌤️", "曇りがち": "🌥️",
            "厚い雲": "☁️",
            "雨": "🌧️", "大雨": "🌧️", "小雨": "🌦️", "霧雨": "🌦️", "にわか雨": "🌦️",
            "雪": "❄️", "大雪": "❄️", "小雪": "🌨️", "みぞれ": "🌨️",
            "霧": "🌫️", "濃霧": "🌫️",
            "雷": "⚡", "雷雨": "⛈️", "雷を伴う": "⛈️",
            "台風": "🌀", "暴風": "🌪️",
            "データなし": "🌐"
        })
        
        return weather_icons.get(condition, "🌈")

    def _generate_html_report(self, date_str, battery_data, season_info, recommended_settings, weather_data):
        """
        HTML形式のレポート本文を生成します。
        
        Args:
            date_str (str): レポート対象日付（YYYYMMDD形式）
            battery_data (dict): バッテリー状態データ
            season_info (dict): 季節情報
            recommended_settings (dict): 推奨設定情報
            weather_data (dict): 天気予報データ
            
        Returns:
            str: HTML形式のレポート本文
        """
        formatted_date = datetime.now().strftime("%Y年%m月%d日")
        formatted_date = datetime.now().strftime("%Y年%m月%d日")
        current_time = datetime.now().strftime("%H:%M")
        
        # 曜日の表示用
        weekday_names = ["月", "火", "水", "木", "金", "土", "日"]
        
        # HTML本文のヘッダー部分 - 波括弧をエスケープするために二重波括弧を使用
        html = """
        <html>
        <head>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ width: 100%; max-width: 800px; margin: 0 auto; }}
                .section {{ margin-bottom: 25px; padding: 15px; background: #f9f9f9; border-radius: 5px; }}
                .section-header {{ font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
                .item-label {{ font-weight: bold; }}
                .item-value {{ margin-left: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 10px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .weather-icon {{ font-size: 24px; margin-right: 10px; vertical-align: middle; }}
                .note {{ color: #FF6600; font-style: italic; }}
                .footer {{ margin-top: 25px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>HANAZONOシステム 日次レポート</h2>
                <p>{0}</p>
        """.format(formatted_date + " " + current_time)
        
        # 天気予報セクション
        if weather_data and 'forecast' in weather_data:
            html += """
                <div class="section">
                    <div class="section-header">■天気予報</div>
                    <table>
                        <tr>
                            <th>日付</th>
                            <th>天気</th>
                            <th>気温</th>
                        </tr>
            """
            
            forecast = weather_data['forecast']
            today = datetime.now().date()
            
            # 今日の天気
            if 'today' in forecast:
                today_weather = forecast['today']
                html += f"""
                        <tr>
                            <td>今日 ({today.month}月{today.day}日, {self._get_weekday(today)})</td>
                            <td><span class="weather-icon">{self._get_weather_emoji(today_weather['condition'])}</span> {today_weather['condition']}</td>
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                            <td>{int(round(today_weather['min_temp']))}℃ 〜 {int(round(today_weather['max_temp']))}℃</td>
                        </tr>
                """
            
            # 明日の天気
            if 'tomorrow' in forecast:
                tomorrow = today + timedelta(days=1)
                tomorrow_weather = forecast['tomorrow']
                html += f"""
                        <tr>
                            <td>明日 ({tomorrow.month}月{tomorrow.day}日, {self._get_weekday(tomorrow)})</td>
                            <td><span class="weather-icon">{self._get_weather_emoji(tomorrow_weather['condition'])}</span> {tomorrow_weather['condition']}</td>
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                            <td>{int(round(tomorrow_weather['min_temp']))}℃ 〜 {int(round(tomorrow_weather['max_temp']))}℃</td>
                        </tr>
                """
            
            # 明後日の天気
            if 'day_after' in forecast:
                day_after = today + timedelta(days=2)
                day_after_weather = forecast['day_after']
                html += f"""
                        <tr>
                            <td>明後日 ({day_after.month}月{day_after.day}日, {self._get_weekday(day_after)})</td>
                            <td><span class="weather-icon">{self._get_weather_emoji(day_after_weather['condition'])}</span> {day_after_weather['condition']}</td>
    def _parse_weather_condition(self, condition):
        """
        複合的な天気条件を解析し、構造化データを返します。
        例: "晴れ 後 曇り" -> [{"condition": "晴れ"}, {"transition": "後"}, {"condition": "曇り"}]

        Args:
            condition (str): 天気条件の文字列

        Returns:
            dict: 解析結果
                - patterns: 天気パターンのリスト
                - emoji_line: 絵文字のみの行
                - text_line: テキストのみの行
        """
        if not condition or condition == "データなし":
            return {
                "patterns": [{"condition": "データなし"}],
                "emoji_line": "🌐",
                "text_line": "データなし"
            }

        # 基本的な天気パターンを抽出
        transitions = ["後", "のち", "から", "一時", "時々", "所により"]
        patterns = []
        
        # 複合的な天気条件を分割
        parts = []
        current_part = ""
        for word in condition.split():
            if word in transitions:
                if current_part:
                    parts.append({"condition": current_part.strip()})
                    current_part = ""
                parts.append({"transition": word})
            else:
                current_part += " " + word
        
        if current_part:
            parts.append({"condition": current_part.strip()})
        
        # 単純な天気条件の場合
        if len(parts) <= 1:
            emoji = self._get_weather_emoji(condition)
            return {
                "patterns": [{"condition": condition}],
                "emoji_line": emoji,
                "text_line": condition
            }
        
        # 複合的な天気条件の場合
        emoji_line = ""
        text_line = ""
        
        for i, part in enumerate(parts):
            if "condition" in part:
                emoji = self._get_weather_emoji(part["condition"])
                emoji_line += emoji
                text_line += part["condition"]
            elif "transition" in part:
                if i < len(parts) - 1:  # 最後の要素でなければ
                    emoji_line += " → "
                    text_line += f" {part['transition']} "
        
        return {
            "patterns": parts,
            "emoji_line": emoji_line,
            "text_line": text_line
        }
                            <td>{int(round(day_after_weather['min_temp']))}℃ 〜 {int(round(day_after_weather['max_temp']))}℃</td>
                        </tr>
                """
            
            html += """
                    </table>
                </div>
            """
        else:
            html += """
                <div class="section">
                    <div class="section-header">■天気予報</div>
                    <p>天気予報データがありません</p>
                </div>
            """
        
        # 季節情報セクション
        html += f"""
                <div class="section">
                    <div class="section-header">■季節判定</div>
                    <p><span style="font-size: 24px;">{season_info['emoji']}</span> <strong>{season_info['name']}</strong></p>
                </div>
        """
        
        # 推奨設定セクション
        html += """
                <div class="section">
                    <div class="section-header">■推奨設定</div>
        """
        
        if 'type' in recommended_settings:
            html += f"""
                    <p>⚡ タイプ{recommended_settings['type']}（標準設定）</p>
            """
        
        # パラメータID
        charge_current_id = self.settings.get('inverter_parameters', {}).get('charge_current_id', '07')
        charge_time_id = self.settings.get('inverter_parameters', {}).get('charge_time_id', '10')
        soc_setting_id = self.settings.get('inverter_parameters', {}).get('soc_setting_id', '62')
        
        html += """
                    <table>
                        <tr>
                            <th>設定項目</th>
                            <th>推奨値</th>
                            <th>パラメータID</th>
                        </tr>
        """
        
        # 充電設定の表示
        charge_current = recommended_settings.get('charge_current', 'N/A')
        html += f"""
                        <tr>
                            <td>充電電流</td>
                            <td>{charge_current} A</td>
                            <td>{charge_current_id}</td>
                        </tr>
        """
        
        charge_time = recommended_settings.get('charge_time', 'N/A')
        html += f"""
                        <tr>
                            <td>充電時間</td>
                            <td>{charge_time} 分</td>
                            <td>{charge_time_id}</td>
                        </tr>
        """
        
        soc = recommended_settings.get('output_soc', recommended_settings.get('cutoff_soc', 'N/A'))
        html += f"""
                        <tr>
                            <td>SOC設定</td>
                            <td>{soc} %</td>
                            <td>{soc_setting_id}</td>
                        </tr>
                    </table>
        """
        
        # 天気による調整がある場合
        if "weather_note" in recommended_settings:
            html += f"""
                    <p class="note">※ {recommended_settings['weather_note']}</p>
            """
        
        html += """
                </div>
        """
        
        # バッテリー状態セクション
        html += """
                <div class="section">
                    <div class="section-header">■バッテリー状態</div>
        """
        
        if any([battery_data.get(key) is not None for key in battery_data]):
            html += """
                    <table>
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
            """
            
            if battery_data.get("soc") is not None:
                html += f"""
                        <tr>
                            <td>SOC</td>
                            <td>{battery_data['soc']} %</td>
                        </tr>
                """
            
            if battery_data.get("voltage") is not None:
                # 小数点以下1桁までに丸める
                voltage = int(battery_data['voltage'] * 10) / 10
                html += f"""
                        <tr>
                            <td>電圧</td>
                            <td>{voltage} V</td>
                        </tr>
                """
            
            if battery_data.get("current") is not None:
                # 小数点以下1桁までに丸める
                current = int(battery_data['current'] * 10) / 10
                html += f"""
                        <tr>
                            <td>電流</td>
                            <td>{current} A</td>
                        </tr>
                """
            
            if battery_data.get("power") is not None:
                # 小数点以下1桁までに丸める
                power = int(battery_data['power'] * 10) / 10
                html += f"""
                        <tr>
                            <td>電力</td>
                            <td>{power} W</td>
                        </tr>
                """
            
            # 不明状態は表示しない
            if battery_data.get("status") is not None and not self._is_unknown_status(battery_data["status"]):
                html += f"""
                        <tr>
                            <td>状態</td>
                            <td>{battery_data['status']}</td>
                        </tr>
                """
            
            html += """
                    </table>
            """
        else:
            html += """
                    <p>バッテリーデータがありません</p>
            """
        
        html += """
                </div>
        """
        
        # 注記セクション
        notes_html = self._generate_notes_html()
        if notes_html:
            html += notes_html
        
        # フッター
        footer_text = self.settings.get('notification', {}).get('email', {}).get('template', {}).get('footer', 
            "この設定は天気予報と季節に基づいて自動的に計算されています。実際の設定変更は手動で行う必要があります。本メールは自動送信されています。")
        
        html += f"""
                <div class="footer">
                    {footer_text}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
        
    def _generate_notes_html(self):
        """注記からHTMLを生成する"""
        if hasattr(self, 'notes') and self.notes:
            html = "<hr><div style='color: #FF6600; font-style: italic; margin-top: 20px;'>"
            for note in self.notes:
                html += f"<p>※ {note}</p>"
            html += "</div>"
            
            # 注記を使用したら消去（次回用）
            notes_copy = self.notes.copy()
            self.notes = []
            
            return html
        return ""
        
    def send_ip_change_notification(self, old_ip, new_ip):
        """IPアドレス変更通知メールを送信"""
        if "email" not in self.settings or not self.settings["email"].get("smtp_server"):
            self.logger.warning("メール設定が構成されていません")
            return False
        
        subject = f"⚠️ LVYUANシステムIPアドレス変更通知"
        body_text = f"インバーターのIPアドレスが変更されました。\n\n旧IPアドレス: {old_ip}\n新IPアドレス: {new_ip}"
        body_html = f"""
        <html>
            <body>
                <h2>インバーターIPアドレス変更通知</h2>
                <p>インバーターのIPアドレスが変更されました。</p>
                <ul>
                    <li>旧IPアドレス: <b>{old_ip}</b></li>
                    <li>新IPアドレス: <b>{new_ip}</b></li>
                </ul>
                <p>設定が必要な場合は更新してください。</p>
            </body>
        </html>
        """
        
        return self._send_email(
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )
        
    def _send_email(self, subject, body_text, body_html=None, attachments=None, to_email=None):
        """
        メールを送信する
        
        Args:
            subject: メール件名
            body_text: テキスト本文
            body_html: HTML本文（オプション）
            attachments: 添付ファイルのパスリスト（オプション）
            to_email: 送信先メールアドレス（オプション、設定から取得）
            
        Returns:
            bool: 送信成功ならTrue
        """
        try:
            if "email" not in self.settings:
                self.logger.error("メール設定がありません")
                return False
                
            email_settings = self.settings["email"]
            
            # SMTPサーバー設定
            smtp_server = email_settings.get("smtp_server")
            smtp_port = email_settings.get("smtp_port", 587)
            smtp_user = email_settings.get("smtp_user")
            smtp_password = email_settings.get("smtp_password")
            
            # 送信元と送信先
            sender = email_settings.get("sender")
            recipients = to_email or email_settings.get("recipients", [])
            
            if not smtp_server or not sender or not recipients:
                self.logger.error("メール設定が不完全です")
                return False
                
            # メッセージの作成
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = ", ".join(recipients)
            msg["Date"] = formatdate()
            
            # テキスト本文を追加
            msg.attach(MIMEText(body_text, "plain", "utf-8"))
            
            # HTML本文があれば追加
            if body_html:
                msg.attach(MIMEText(body_html, "html", "utf-8"))
                
            # 添付ファイルがあれば追加
            if attachments:
                for attachment in attachments:
                    try:
                        if os.path.exists(attachment):
                            with open(attachment, "rb") as f:
                                img_data = f.read()
                                
                            img = MIMEImage(img_data)
                            img.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment))
                            msg.attach(img)
                    except Exception as e:
                        self.logger.error(f"添付ファイル追加エラー: {e}")
            
            # メール送信
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if smtp_port == 587:  # STARTTLS
                    server.starttls()
                    
                if smtp_user and smtp_password:
                    server.login(smtp_user, smtp_password)
                    
                # sendmailを使用（Pythonのバージョン互換性のため）
                server.sendmail(sender, recipients, msg.as_string())
                
            self.logger.info(f"メール送信成功: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"メール送信エラー: {e}")
            self.logger.debug(traceback.format_exc())
            return False
            
    def send_alert(self, subject, message, to_email=None):
        """
        アラートメールを送信する
        
        Args:
            subject: アラート件名
            message: アラートメッセージ
            to_email: 送信先（省略時は設定から取得）
            
        Returns:
            bool: 送信成功ならTrue
        """
        # 件名にアラートプレフィックスを追加
        subject = f"🚨 {subject}"
        body = f"【アラート】\n\n{message}\n\n発生時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.logger.info(f"アラートメール送信: {subject}")
        
        return self._send_email(
            to_email=to_email,
            subject=subject,
            body_text=body,
            body_html=f"<html><body><p>{body}</p></body></html>"
        )

# スタンドアロン実行時のサンプルコード
if __name__ == "__main__":
    # ロガー設定
    logging.basicConfig(level=logging.INFO)
    
    # 実行テスト
    notifier = EmailNotifier()
    
    # 日次レポート送信テスト
    notifier.send_daily_report()

