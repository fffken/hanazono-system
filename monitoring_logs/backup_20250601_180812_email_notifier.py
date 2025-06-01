#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANAZONOシステム: メール通知機能 (環境変数展開対応版)
"""

import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import logging
import argparse

def strip_html_tags(html_content):
    """HTMLタグを除去してプレーンテキストに変換"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_content)

class EmailNotifier:
    """
    メール通知機能を提供するクラス (環境変数展開対応)
    """
    def __init__(self, config, logger):
        """
        初期化
        """
        self.config = config
        self.logger = logger
        
    def _get_weather_emoji(self, condition):
        """
        天気状態に対応する絵文字を返す
        """
        if not condition or condition == "データなし":
            return "🌐"
        elif "雨" in condition:
            return "🌧️"
        elif "雪" in condition:
            return "❄️"
        elif "曇" in condition or "くもり" in condition:
            return "☁️"
        elif "霧" in condition or "霞" in condition:
            return "🌫️"
        elif "晴" in condition:
            return "☀️"
        elif "曇りがち" in condition or "厚い雲" in condition:
            return "☁️"
        else:
            return "🌈"
    
    def _format_weather_emojis(self, weather_text):
        """
        天気情報を絵文字の連結に変換
        """
        if not weather_text or weather_text == "データなし":
            return "🌐"
        
        # 天気成分に分割
        components = []
        for delimiter in [" のち ", "のち", " 後 ", "後"]:
            if delimiter in weather_text:
                components = weather_text.split(delimiter)
                break
        
        if not components:
            components = [weather_text]
        
        # 各成分に対応する絵文字を取得
        emojis = [self._get_weather_emoji(comp.strip()) for comp in components]
        emoji_text = "→".join(emojis)
        
        return emoji_text
    
    def _format_date_jp(self, date_obj):
        """
        日付を日本語フォーマットに変換
        """
        weekday_jp = ["月", "火", "水", "木", "金", "土", "日"]
        weekday = weekday_jp[date_obj.weekday()]
        return f"{date_obj.year}年{date_obj.month}月{date_obj.day}日({weekday})"
    
    def _generate_text_report(self, data):
        """
        テキスト形式のレポートを生成
        """
        now = datetime.datetime.now()
        date_str = self._format_date_jp(now)
        
        report = f"===== HANAZONOシステム 革新レポート =====\n"
        report += f"日付: {date_str}\n\n"
        
        # 電力情報
        report += "■ 電力情報\n"
        if 'power_data' in data:
            power_data = data['power_data']
            report += f"バッテリー残量: {power_data.get('battery_level', 'N/A')}%\n"
            report += f"太陽光発電: {power_data.get('solar_generation', 'N/A')} W\n"
            report += f"消費電力: {power_data.get('consumption', 'N/A')} W\n"
        else:
            report += "データなし\n"
        
        report += "\n"
        
        # 天気予報
        report += "■ 天気予報\n"
        if 'weather' in data:
            weather = data['weather']
            weather_today = weather.get('today', 'データなし')
            weather_tomorrow = weather.get('tomorrow', 'データなし')
            
            today_emoji = self._format_weather_emojis(weather_today)
            tomorrow_emoji = self._format_weather_emojis(weather_tomorrow)
            
            report += f"今日: {today_emoji} {weather_today}\n"
            report += f"明日: {tomorrow_emoji} {weather_tomorrow}\n"
        else:
            report += "データなし\n"
        
        report += "\n"
        
        # システム状態
        report += "■ システム状態\n"
        if 'system_status' in data:
            status = data['system_status']
            report += f"動作モード: {status.get('mode', 'N/A')}\n"
            report += f"最終更新: {status.get('last_update', 'N/A')}\n"
            report += f"システム温度: {status.get('temperature', 'N/A')} °C\n"
        else:
            report += "データなし\n"
        
        # 高度分析結果
        if 'advanced_analysis' in data and data['advanced_analysis']:
            report += "\n■ 🚀 高度分析結果\n"
            advanced = data['advanced_analysis']
            for key, value in advanced.items():
                if value:
                    report += f"{key}: {value}\n"
        
        report += "\n🎯 HANAZONOシステム - 世界最高レベルの電力管理AI"
        report += "\n※ 本メールは自動生成されています"
            
        return report
    
    def send_daily_report(self, data):
        """
        日次レポートをメール送信 (環境変数展開対応)
        """
        try:
            # 現在の日時
            now = datetime.datetime.now()
            date_str = self._format_date_jp(now)
            
            # メール設定の取得
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            
            # 🔧 環境変数展開処理 (重要!)
            if password and password.startswith("${") and password.endswith("}"):
                env_var = password[2:-1]  # ${SMTP_PASSWORD} -> SMTP_PASSWORD
                password = os.getenv(env_var)
                self.logger.debug(f"環境変数 {env_var} から取得: {'設定済み' if password else '未設定'}")
            
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error("メール設定が不完全です")
                return False
            
            # 時間帯に応じたメール件名の構築
            time_suffix = "(07時)" if 5 <= now.hour < 12 else "(23時)"
            subject = f"🏆 HANAZONOシステム 革新レポート {date_str} {time_suffix}"
            
            # メッセージの作成
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ", ".join(recipients)
            
            # テキスト本文の追加
            text_content = self._generate_text_report(data)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # SMTP接続 (settings.json設定に対応)
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            self.logger.debug(f"SMTP DEBUG: User='{username}', Pass='{password[:4]}****{password[-4:] if len(password) > 8 else '****'}' (Length: {len(password)})")
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            
            self.logger.info(f"✅ レポートメールを送信しました: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ メール送信エラー: {e}")
            return False
    
    def send_alert(self, title, message, priority="中"):
        """
        アラートメールを送信
        """
        try:
            # 設定取得
            smtp_server = self.config.get('smtp_server')
            smtp_port = self.config.get('smtp_port')
            username = self.config.get('smtp_user')
            password = self.config.get('smtp_password')
            
            # 環境変数展開処理
            if password and password.startswith("${") and password.endswith("}"):
                env_var = password[2:-1]
                password = os.getenv(env_var)
            
            sender = self.config.get('email_sender')
            recipients = self.config.get('email_recipients')
            
            if not all([smtp_server, smtp_port, username, password, sender, recipients]):
                self.logger.error("アラートメール設定が不完全です")
                return False
            
            # 優先度に応じた絵文字
            priority_emoji = {
                "高": "⚠️",
                "中": "ℹ️",
                "低": "📝"
            }.get(priority, "ℹ️")
            
            # 現在の日時
            now = datetime.datetime.now()
            date_str = self._format_date_jp(now)
            time_str = now.strftime("%H:%M:%S")
            
            # メール件名
            subject = f"{priority_emoji} [HANAZONO] {title}"
            
            # メッセージの作成
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ", ".join(recipients)
            
            # テキスト本文
            text_content = f"""
===== HANAZONOシステム アラート =====
日時: {date_str} {time_str}
優先度: {priority} {priority_emoji}

{message}

---
このメールはHANAZONOシステムによって自動送信されています
"""
            
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # SMTP送信
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            
            self.logger.info(f"✅ アラートメールを送信しました: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ アラートメール送信エラー: {e}")
            return False

# テスト実行用コード
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HANAZONOシステム メール通知機能')
    parser.add_argument('--test', action='store_true', help='テストモードで実行')
    args = parser.parse_args()
    
    if args.test:
        print("🧪 email_notifier.py 環境変数展開対応版テスト実行中...")
        print("✅ 修正版読み込み完了")
        print("🎯 ultimate_email_integration.py --test で実際のテストを実行してください")
