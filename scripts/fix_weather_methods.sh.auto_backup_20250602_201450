#!/bin/bash

# バックアップ作成
cp email_notifier.py email_notifier.py.bak.$(date +%Y%m%d%H%M%S)

# _get_weather_emojiメソッドを置き換え
# 開始行と次のメソッドの行を取得
start_line=$(grep -n "def _get_weather_emoji" email_notifier.py | cut -d: -f1)
next_method_line=$(grep -n "def _parse_weather_condition" email_notifier.py | cut -d: -f1)
end_line=$((next_method_line - 1))

# 古いメソッドを削除して新しいメソッドを挿入
sed -i "${start_line},${end_line}d" email_notifier.py
sed -i "${start_line}i\\    def _get_weather_emoji(self, weather_condition):\\n        \"\"\"\\n        天気状態に対応する絵文字を返す\\n        様々な天気条件に対応\\n        \"\"\"\\n        weather_map = {\\n            \"晴れ\": \"☀️\",\\n            \"晴\": \"☀️\",\\n            \"快晴\": \"☀️\",\\n            \"曇り\": \"☁️\",\\n            \"曇\": \"☁️\",\\n            \"くもり\": \"☁️\",\\n            \"雨\": \"🌧️\",\\n            \"大雨\": \"⛈️\",\\n            \"雷雨\": \"⛈️\",\\n            \"雪\": \"❄️\",\\n            \"霧\": \"🌫️\",\\n            \"霞\": \"🌫️\",\\n            \"不明\": \"❓\"\\n        }\\n\\n        # 完全一致の場合\\n        if weather_condition in weather_map:\\n            return weather_map[weather_condition]\\n            \\n        # 部分一致の場合\\n        for key in weather_map:\\n            if key in weather_condition:\\n                return weather_map[key]\\n                \\n        # 曇りがち等の特別な表現に対応\\n        if \"曇りがち\" in weather_condition or \"厚い雲\" in weather_condition:\\n            return \"☁️\"\\n        \\n        # その他のケース\\n        return \"🌈\"  # デフォルト：虹の絵文字" email_notifier.py

echo "_get_weather_emoji メソッドを修正しました"

# _parse_weather_conditionメソッドを置き換え
start_line=$(grep -n "def _parse_weather_condition" email_notifier.py | cut -d: -f1)
next_method_line=$(grep -n "def _generate_html_report" email_notifier.py | cut -d: -f1)
end_line=$((next_method_line - 1))

# 古いメソッドを削除して新しいメソッドを挿入
sed -i "${start_line},${end_line}d" email_notifier.py
sed -i "${start_line}i\\    def _parse_weather_condition(self, condition):\\n        \"\"\"\\n        複合的な天気条件を解析し,構造化データを返します.\\n        例: \"晴れ 後 曇り\" -> [{\"condition\": \"晴れ\"}, {\"transition\": \"後\"}, {\"condition\": \"曇り\"}]\\n        \"\"\"\\n        if not condition or condition == \"データなし\":\\n            return {\\n                \"patterns\": [{\"condition\": \"データなし\"}],\\n                \"emoji_line\": \"🌐\",\\n                \"text_line\": \"データなし\"\\n            }\\n\\n        # 基本的な天気パターンと優先順位\\n        weather_patterns = {\\n            \"雨\": 5,\\n            \"雪\": 5,\\n            \"曇\": 3,\\n            \"くもり\": 3,\\n            \"霧\": 3,\\n            \"晴れ\": 1,\\n            \"快晴\": 1,\\n            \"晴\": 1,\\n        }\\n        transitions = [\"後\", \"のち\", \"から\", \"一時\", \"時々\", \"所により\"]\\n        \\n        # 天気条件の構造化\\n        patterns = []\\n        parts = condition.split()\\n        current_condition = \"\"\\n        \\n        for part in parts:\\n            if part in transitions:\\n                if current_condition:\\n                    patterns.append({\"condition\": current_condition})\\n                    current_condition = \"\"\\n                patterns.append({\"transition\": part})\\n            else:\\n                if current_condition:\\n                    current_condition += \" \"\\n                current_condition += part\\n        \\n        if current_condition:\\n            patterns.append({\"condition\": current_condition})\\n            \\n        # 主要な天気を判定（優先度ベース）\\n        highest_priority = 0\\n        primary_condition = \"不明\"\\n        \\n        for pattern in patterns:\\n            if \"condition\" in pattern:\\n                for weather, priority in weather_patterns.items():\\n                    if weather in pattern[\"condition\"] and priority > highest_priority:\\n                        highest_priority = priority\\n                        if weather == \"くもり\":\\n                            primary_condition = \"曇り\"\\n                        else:\\n                            primary_condition = weather\\n        \\n        # 絵文字の決定\\n        emoji = self._get_weather_emoji(primary_condition)\\n        \\n        return {\\n            \"patterns\": patterns,\\n            \"emoji_line\": emoji,\\n            \"text_line\": condition\\n        }" email_notifier.py

echo "_parse_weather_condition メソッドを修正しました"

# 全角文字を半角に置換
sed -i 's/（/(/g; s/）/)/g; s/、/,/g; s/。/./g; s/：/:/g; s/；/;/g' email_notifier.py

echo "全ての修正が完了しました"
