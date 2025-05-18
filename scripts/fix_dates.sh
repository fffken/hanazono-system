#!/bin/bash
# 1. _generate_text_report メソッドの修正
sed -i '/_generate_text_report/,+7c\
    def _generate_text_report(self, date_str, battery_data, season_info, recommended_settings, weather_data):\
        """テキスト形式のレポートを生成する"""\
        # 日付と現在時刻\
        formatted_date = self._format_date_jp(date_str)\
        current_time = datetime.now().strftime("%H:%M")\
\
        # レポートタイトル\
        text = f"HANAZONOシステム 日次レポート\\n{formatted_date} {current_time}\\n\\n"' email_notifier.py

# 2. _generate_html_report メソッドの修正
sed -i '/_generate_html_report/,+20{/now = datetime.now()/c\
        formatted_date = self._format_date_jp(date_str)\
        current_time = datetime.now().strftime("%H:%M")
}' email_notifier.py

# 3. HTML出力部分の修正
sed -i 's/now.strftime('\''%Y年%m月%d日 %H:%M'\'')  # "実行日時:" を削除/formatted_date + " " + current_time  # 日付フォーマット統一/' email_notifier.py

# 4. _determine_season メソッドの修正
sed -i '/_determine_season/,+5{/month = now.month/c\
        now = datetime.now()\
        month = now.month
}' email_notifier.py

# 5. _get_mock_weather_data メソッドの修正
sed -i '/def _get_mock_weather_data/a\
        now = datetime.now()' email_notifier.py

# 6. 天気予報処理部分の修正
sed -i '/\"現在時刻と日付\"/a\
            now = datetime.now()' email_notifier.py
