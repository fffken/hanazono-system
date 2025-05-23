#!/usr/bin/env python3
"""レポート生成モジュール"""

import os
import json
import time
import datetime
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class ReportGenerator:
    def __init__(self, data_dir=None):
        # データディレクトリの設定
        if data_dir is None:
            self.data_dir = os.path.join(os.path.expanduser(
                '~'), 'lvyuan_solar_control', 'data')
        else:
            self.data_dir = data_dir

        # レポート保存ディレクトリ
        self.reports_dir = os.path.join(self.data_dir, 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

        # グラフ保存ディレクトリ
        self.charts_dir = os.path.join(self.data_dir, 'charts')
        os.makedirs(self.charts_dir, exist_ok=True)

        # ロガー設定
        self.logger = logging.getLogger("report_generator")

    def _load_data_for_date(self, date_str):
        """指定した日付のデータを読み込む"""
        filename = os.path.join(self.data_dir, f"data_{date_str}.json")
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"日付 {date_str} のデータ読み込みエラー: {e}")
            return []

    def _get_date_range(self, days=1, end_date=None):
        """日付範囲を取得"""
        if end_date is None:
            end_date = datetime.date.today()
        elif isinstance(end_date, str):
            # YYYYMMDD形式の文字列から日付オブジェクトに変換
            end_date = datetime.datetime.strptime(end_date, "%Y%m%d").date()

        dates = [(end_date - datetime.timedelta(days=i)).strftime("%Y%m%d")
                 for i in range(days)]
        return dates

    def _get_value_at_time(self, timestamps, values, target_hour):
        """特定の時間に最も近い値を取得"""
        if not timestamps or not values:
            return None

        best_diff = float('inf')
        best_value = None

        for t, v in zip(timestamps, values):
            dt = datetime.datetime.fromtimestamp(
                t) if isinstance(t, (int, float)) else t
            if dt.hour == target_hour:
                diff = abs(dt.minute * 60 + dt.second)
                if diff < best_diff:
                    best_diff = diff
                    best_value = v

        # 該当する時間のデータがない場合は最も近い値を探す
        if best_value is None:
            for t, v in zip(timestamps, values):
                dt = datetime.datetime.fromtimestamp(
                    t) if isinstance(t, (int, float)) else t
                diff = abs((dt.hour - target_hour) * 3600 +
                           dt.minute * 60 + dt.second)
                if diff < best_diff:
                    best_diff = diff
                    best_value = v

        return best_value

    def generate_daily_report(self, date_str=None):
        """日次レポートを生成"""
        if date_str is None:
            # 前日の日付
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            date_str = yesterday.strftime("%Y%m%d")

        self.logger.info(f"日付 {date_str} のレポートを生成します")

        # データ読み込み
        data = self._load_data_for_date(date_str)
        if not data:
            self.logger.warning(f"日付 {date_str} のデータが見つかりません")
            return None

        # データの整理
        timestamps = []
        soc_values = []
        voltage_values = []
        current_values = []

        for entry in data:
            if "battery" in entry and entry["battery"] is not None:
                ts = entry.get("timestamp")
                if ts:
                    timestamps.append(ts)
                    soc_values.append(entry["battery"].get("soc", 0))
                    voltage_values.append(entry["battery"].get("voltage", 0))
                    current_values.append(entry["battery"].get("current", 0))

        if not timestamps:
            self.logger.warning(f"日付 {date_str} のバッテリーデータが見つかりません")
            return None

        # タイムスタンプをdatetimeオブジェクトに変換
        dt_timestamps = [datetime.datetime.fromtimestamp(
            ts) for ts in timestamps]

        # レポートデータの準備
        first_entry = data[0]
        last_entry = data[-1]

        # 朝7時と夜23時のデータを近似値から算出
        morning_soc = self._get_value_at_time(timestamps, soc_values, 7)
        night_soc = self._get_value_at_time(timestamps, soc_values, 23)

        # 日付の整形（YYYYMMDD→YYYY年MM月DD日）
        formatted_date = f"{date_str[:4]}年{date_str[4:6]}月{date_str[6:8]}日"

        report = {
            "date": date_str,
            "formatted_date": formatted_date,
            "data_points": len(data),
            "first_timestamp": first_entry.get("datetime", ""),
            "last_timestamp": last_entry.get("datetime", ""),
            "soc_morning": morning_soc,
            "soc_night": night_soc,
            "soc_min": min(soc_values) if soc_values else 0,
            "soc_max": max(soc_values) if soc_values else 0,
            "voltage_avg": sum(voltage_values) / len(voltage_values) if voltage_values else 0,
            "current_avg": sum(current_values) / len(current_values) if current_values else 0
        }

        # グラフ生成
        self._generate_daily_charts(
            date_str, formatted_date, dt_timestamps, soc_values, voltage_values, current_values)

        # レポートの保存
        report_filename = os.path.join(
            self.reports_dir, f"daily_report_{date_str}.json")
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"日次レポートを {report_filename} に保存しました")

        return report

    def _generate_daily_charts(self, date_str, formatted_date, timestamps, soc_values, voltage_values, current_values):
        """日次グラフを生成"""
        # 日本語フォント設定（必要に応じて）
        plt.rcParams['font.family'] = 'IPAexGothic'

        # SOCグラフ
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, soc_values, 'b-',
                 marker='o', label='バッテリーSOC (%)')
        plt.title(f"{formatted_date} バッテリーSOC推移")
        plt.xlabel('時刻')
        plt.ylabel('SOC (%)')
        plt.grid(True)
        plt.legend()

        # x軸の時間表示を調整
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.gcf().autofmt_xdate()  # 日付ラベルを見やすく

        # Y軸の範囲を0-100%に設定
        plt.ylim(0, 100)

        soc_chart_path = os.path.join(self.charts_dir, f"soc_{date_str}.png")
        plt.savefig(soc_chart_path)
        plt.close()
        self.logger.debug(f"SOCグラフを {soc_chart_path} に保存しました")

        # 電圧/電流グラフ
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 電圧（左軸）
        ax1.set_xlabel('時刻')
        ax1.set_ylabel('電圧 (V)', color='b')
        ax1.plot(timestamps, voltage_values, 'b-', marker='o', label='電圧 (V)')
        ax1.tick_params(axis='y', labelcolor='b')

        # 電流（右軸）
        ax2 = ax1.twinx()
        ax2.set_ylabel('電流 (A)', color='r')
        ax2.plot(timestamps, current_values, 'r-', marker='x', label='電流 (A)')
        ax2.tick_params(axis='y', labelcolor='r')

        # タイトルと凡例
        fig.suptitle(f"{formatted_date} バッテリー電圧/電流推移")
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # x軸の時間表示を調整
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))

        fig.tight_layout()
        plt.gcf().autofmt_xdate()  # 日付ラベルを見やすく

        voltage_current_chart_path = os.path.join(
            self.charts_dir, f"voltage_current_{date_str}.png")
        plt.savefig(voltage_current_chart_path)
        plt.close()
        self.logger.debug(f"電圧/電流グラフを {voltage_current_chart_path} に保存しました")

    def generate_weekly_report(self, end_date=None):
        """週次レポートを生成"""
        # 過去7日間のデータを対象
        dates = self._get_date_range(7, end_date)

        self.logger.info(f"週間レポート ({dates[-1]}～{dates[0]}) を生成します")

        daily_reports = []
        for date_str in dates:
            report = self.generate_daily_report(date_str)
            if report:
                daily_reports.append(report)

        if not daily_reports:
            self.logger.warning("週次レポートを生成するためのデータが不足しています")
            return None

        # 週間の統計データを計算
        valid_morning_soc = [r["soc_morning"]
                             for r in daily_reports if r["soc_morning"] is not None]
        valid_night_soc = [r["soc_night"]
                           for r in daily_reports if r["soc_night"] is not None]

        soc_morning_avg = sum(valid_morning_soc) / \
            len(valid_morning_soc) if valid_morning_soc else 0
        soc_night_avg = sum(valid_night_soc) / \
            len(valid_night_soc) if valid_night_soc else 0

        weekly_report = {
            "period": f"{dates[-1]} - {dates[0]}",
            "formatted_period": f"{dates[-1][:4]}年{dates[-1][4:6]}月{dates[-1][6:8]}日～{dates[0][:4]}年{dates[0][4:6]}月{dates[0][6:8]}日",
            "days_count": len(daily_reports),
            "soc_morning_avg": soc_morning_avg,
            "soc_night_avg": soc_night_avg,
            "daily_reports": daily_reports
        }

        # グラフ生成
        self._generate_weekly_charts(weekly_report)

        # レポートの保存
        timestamp = time.strftime("%Y%m%d")
        report_filename = os.path.join(
            self.reports_dir, f"weekly_report_{timestamp}.json")
        with open(report_filename, "w") as f:
            json.dump(weekly_report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"週次レポートを {report_filename} に保存しました")

        return weekly_report

    def _generate_weekly_charts(self, weekly_report):
        """週次グラフを生成"""
        # 日本語フォント設定（必要に応じて）
        plt.rcParams['font.family'] = 'IPAexGothic'

        # データ準備
        dates = [r["formatted_date"] for r in weekly_report["daily_reports"]]
        morning_soc = [r["soc_morning"]
                       for r in weekly_report["daily_reports"]]
        night_soc = [r["soc_night"] for r in weekly_report["daily_reports"]]

        # 日付を逆順に（最新を右に）
        dates.reverse()
        morning_soc.reverse()
        night_soc.reverse()

        # SOCグラフ
        plt.figure(figsize=(12, 6))
        plt.bar(dates, morning_soc, width=0.4, align='edge',
                color='skyblue', label='朝7時 SOC')
        plt.bar([d for d in dates], night_soc, width=-0.4,
                align='edge', color='navy', label='夜23時 SOC')
        plt.title(f"週間 SOC推移 ({weekly_report['formatted_period']})")
        plt.xlabel('日付')
        plt.ylabel('SOC (%)')
        plt.grid(True, axis='y')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Y軸の範囲を0-100%に設定
        plt.ylim(0, 100)

        timestamp = time.strftime("%Y%m%d")
        weekly_chart_path = os.path.join(
            self.charts_dir, f"weekly_soc_{timestamp}.png")
        plt.savefig(weekly_chart_path)
        plt.close()
        self.logger.debug(f"週間SOCグラフを {weekly_chart_path} に保存しました")

    def generate_monthly_report(self, end_date=None):
        """月次レポートを生成"""
        # 過去30日間のデータを対象
        dates = self._get_date_range(30, end_date)

        self.logger.info(f"月間レポート ({dates[-1]}～{dates[0]}) を生成します")

        daily_reports = []
        for date_str in dates:
            report = self.generate_daily_report(date_str)
            if report:
                daily_reports.append(report)

        if not daily_reports:
            self.logger.warning("月次レポートを生成するためのデータが不足しています")
            return None

        # 月間の統計データを計算
        valid_morning_soc = [r["soc_morning"]
                             for r in daily_reports if r["soc_morning"] is not None]
        valid_night_soc = [r["soc_night"]
                           for r in daily_reports if r["soc_night"] is not None]

        soc_morning_avg = sum(valid_morning_soc) / \
            len(valid_morning_soc) if valid_morning_soc else 0
        soc_night_avg = sum(valid_night_soc) / \
            len(valid_night_soc) if valid_night_soc else 0

        monthly_report = {
            "period": f"{dates[-1]} - {dates[0]}",
            "formatted_period": f"{dates[-1][:4]}年{dates[-1][4:6]}月{dates[-1][6:8]}日～{dates[0][:4]}年{dates[0][4:6]}月{dates[0][6:8]}日",
            "days_count": len(daily_reports),
            "soc_morning_avg": soc_morning_avg,
            "soc_night_avg": soc_night_avg,
            "daily_reports": daily_reports
        }

        # グラフ生成
        self._generate_monthly_charts(monthly_report)

        # レポートの保存
        timestamp = time.strftime("%Y%m%d")
        report_filename = os.path.join(
            self.reports_dir, f"monthly_report_{timestamp}.json")
        with open(report_filename, "w") as f:
            json.dump(monthly_report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"月次レポートを {report_filename} に保存しました")

        return monthly_report

    def _generate_monthly_charts(self, monthly_report):
        """月次グラフを生成"""
        # 日本語フォント設定（必要に応じて）
        plt.rcParams['font.family'] = 'IPAexGothic'

        # データ準備
        dates = [r["formatted_date"] for r in monthly_report["daily_reports"]]
        morning_soc = [r["soc_morning"]
                       for r in monthly_report["daily_reports"]]
        night_soc = [r["soc_night"] for r in monthly_report["daily_reports"]]

        # 日付を逆順に（最新を右に）
        dates.reverse()
        morning_soc.reverse()
        night_soc.reverse()

        # SOCグラフ（線グラフで表示）
        plt.figure(figsize=(14, 6))
        plt.plot(dates, morning_soc, 'o-', color='skyblue', label='朝7時 SOC')
        plt.plot(dates, night_soc, 'o-', color='navy', label='夜23時 SOC')
        plt.title(f"月間 SOC推移 ({monthly_report['formatted_period']})")
        plt.xlabel('日付')
        plt.ylabel('SOC (%)')
        plt.grid(True)
        plt.legend()

        # Y軸の範囲を0-100%に設定
        plt.ylim(0, 100)

        # x軸のラベルを間引く（5日ごと）
        plt.xticks([dates[i] for i in range(0, len(dates), 5)], rotation=45)

        plt.tight_layout()
        timestamp = time.strftime("%Y%m%d")
        monthly_chart_path = os.path.join(
            self.charts_dir, f"monthly_soc_{timestamp}.png")
        plt.savefig(monthly_chart_path)
        plt.close()
        self.logger.debug(f"月間SOCグラフを {monthly_chart_path} に保存しました")


# メイン処理（直接実行時のテスト用）
if __name__ == "__main__":
    import argparse

    # ロギング設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='LVYUANインバーターレポート生成')
    parser.add_argument('--daily', help='日次レポートを生成 (YYYYMMDD形式、省略時は前日)')
    parser.add_argument('--weekly', action='store_true', help='週次レポートを生成')
    parser.add_argument('--monthly', action='store_true', help='月次レポートを生成')
    parser.add_argument('--data-dir', help='データディレクトリのパス')

    args = parser.parse_args()

    report_gen = ReportGenerator(args.data_dir)

    if args.daily:
        report = report_gen.generate_daily_report(args.daily)
        if report:
            print(f"日次レポートを生成しました: {report['formatted_date']}")
    elif args.weekly:
        report = report_gen.generate_weekly_report()
        if report:
            print(f"週次レポートを生成しました: {report['formatted_period']}")
    elif args.monthly:
        report = report_gen.generate_monthly_report()
        if report:
            print(f"月次レポートを生成しました: {report['formatted_period']}")
    else:
        print("レポートタイプを指定してください: --daily [YYYYMMDD], --weekly, または --monthly")
