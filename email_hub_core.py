#!/usr/bin/env python3
"""
HANAZONOメールハブ v3.0 - 超安定メインシステム
設計思想: 最小限・堅牢・アップデート耐性
"""

import json
import logging
import smtplib
import importlib
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHubCore:
    """メインハブ - 最小限機能のみ"""
    
    def __init__(self, config_path="hub_config.json"):
        self.config_path = config_path
        self.config = {}
        self.modules = {}
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """ログ設定 - シンプル"""
        logger = logging.getLogger('EmailHub')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
        
    def load_config(self):
        """設定読み込み - 安全"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.logger.info("設定読み込み完了")
            return True
        except Exception as e:
            self.logger.error(f"設定読み込み失敗: {e}")
            return False
    
    def load_module(self, module_name):
        """モジュール動的読み込み - 安全"""
        try:
            module = importlib.import_module(f"modules.{module_name}")
            self.modules[module_name] = module
            self.logger.info(f"モジュール読み込み完了: {module_name}")
            return True
        except Exception as e:
            self.logger.warning(f"モジュール読み込み失敗: {module_name} - {e}")
            return False
    
    def send_basic_email(self, subject, body, html_body=None):
        """基本メール送信 - 堅牢"""
        try:
            email_config = self.config.get('email', {})
            
            # 必須設定確認
            required = ['smtp_server', 'smtp_port', 'sender_email', 'receiver_email', 'sender_password']
            for key in required:
                if not email_config.get(key):
                    raise ValueError(f"必須設定が不足: {key}")
            
            # メール作成
            msg = MIMEMultipart('alternative')
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']
            msg['Subject'] = subject
            
            # テキスト部分
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # HTML部分（オプション）
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # SMTP送信
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                if email_config.get('use_tls', True):
                    server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            self.logger.info("メール送信成功")
            return True
            
        except Exception as e:
            self.logger.error(f"メール送信失敗: {e}")
            return False
    
    def generate_report(self, report_type="daily"):
        """レポート生成 - モジュラー"""
        content_sections = []
        
        # 設定からアクティブモジュールを取得
        active_modules = self.config.get('active_modules', [])
        
        for module_name in active_modules:
            if module_name in self.modules:
                try:
                    module = self.modules[module_name]
                    if hasattr(module, 'generate_content'):
                        section = module.generate_content(report_type)
                        if section:
                            content_sections.append(section)
                except Exception as e:
                    self.logger.warning(f"モジュール実行エラー: {module_name} - {e}")
        
        # レポート組み立て
        report_body = self._assemble_report(content_sections, report_type)
        return report_body
    
    def _assemble_report(self, sections, report_type):
        """レポート組み立て - シンプル"""
        header = f"HANAZONOシステム {report_type} レポート {datetime.now().strftime('%Y年%m月%d日')}"
        separator = "=" * 80
        
        report_parts = [
            header,
            separator,
            ""
        ]
        
        for section in sections:
            report_parts.append(section)
            report_parts.append("")
        
        footer = [
            separator,
            "HANAZONOメールハブ v3.0",
            f"生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        report_parts.extend(footer)
        return "\n".join(report_parts)
    
    def run_daily_report(self):
        """日次レポート実行 - メイン機能"""
        try:
            # 設定読み込み
            if not self.load_config():
                return False
            
            # アクティブモジュール読み込み
            active_modules = self.config.get('active_modules', [])
            for module_name in active_modules:
                self.load_module(module_name)
            
            # レポート生成
            report_body = self.generate_report("daily")
            
            # メール送信
            subject = f"HANAZONOシステム日次レポート - {datetime.now().strftime('%Y/%m/%d')}"
            success = self.send_basic_email(subject, report_body)
            
            return success
            
        except Exception as e:
            self.logger.error(f"日次レポート実行エラー: {e}")
            return False


def main():
    """メイン実行"""
    hub = EmailHubCore()
    
    # テスト実行
    print("📧 HANAZONOメールハブ v3.0 テスト実行")
    success = hub.run_daily_report()
    
    if success:
        print("✅ 日次レポート送信成功")
    else:
        print("❌ 日次レポート送信失敗")


if __name__ == "__main__":
    main()
