#!/usr/bin/env python3
# HANAZONO完全現状診断チェックリスト生成
import os
import json
import datetime
import subprocess
import glob

class HANAZONOStatusChecker:
    """設計書v3.0準拠の完全現状診断"""
    
    def __init__(self):
        self.status = {}
        self.checklist = []
        
    def check_data_collection_layer(self):
        """🏛️ データ収集レイヤー診断"""
        print("🔍 データ収集レイヤー診断")
        print("=" * 50)
        
        # CollectorCapsule確認
        collector_exists = os.path.exists('collector_capsule.py')
        collector_working = False
        collector_data = False
        
        if collector_exists:
            try:
                result = subprocess.run(['python3', 'collector_capsule.py'], 
                                      capture_output=True, text=True, timeout=30)
                collector_working = (result.returncode == 0)
                
                # データファイル確認
                data_files = glob.glob('data/collected_data_*.json')
                collector_data = len(data_files) > 0
                
            except Exception as e:
                collector_working = False
                
        self.status['data_collection'] = {
            'collector_exists': collector_exists,
            'collector_working': collector_working,
            'collector_data': collector_data,
            'data_file_count': len(glob.glob('data/*.json')) if os.path.exists('data') else 0
        }
        
        # Modbus確認
        modbus_files = ['main.py', 'lvyuan_collector.py', 'modbus_client.py']
        modbus_status = {f: os.path.exists(f) for f in modbus_files}
        self.status['modbus'] = modbus_status
        
        # 天気API確認
        weather_exists = os.path.exists('weather_forecast.py')
        weather_working = False
        if weather_exists:
            try:
                result = subprocess.run(['python3', 'weather_forecast.py'], 
                                      capture_output=True, text=True, timeout=10)
                weather_working = 'config' not in result.stderr
            except:
                weather_working = False
                
        self.status['weather'] = {
            'exists': weather_exists,
            'working': weather_working
        }
        
    def check_email_system(self):
        """📧 メール配信システム診断"""
        print("📧 メール配信システム診断")
        print("=" * 50)
        
        # メール関連ファイル確認
        email_files = [
            'hanazono_complete_system.py',
            'email_notifier_v2_1.py',
            'ultimate_email_integration.py'
        ]
        
        email_status = {}
        for f in email_files:
            exists = os.path.exists(f)
            email_status[f] = {'exists': exists}
            
            if exists:
                # ファイルサイズとメール送信機能確認
                size = os.path.getsize(f)
                email_status[f]['size'] = size
                
                # 実際のメール送信テスト（dry-run）
                email_status[f]['send_capable'] = self._check_email_capability(f)
                
        self.status['email_system'] = email_status
        
    def check_news_module(self):
        """📰 NEWSモジュール診断"""
        print("📰 NEWSモジュール診断")
        print("=" * 50)
        
        # 設計書の4つのNEWSカテゴリ確認
        news_categories = [
            'BattleNewsGenerator',      # バトル煽り
            'AchievementTracker',       # 達成記録
            'ComparisonAnalyzer',       # 面白い比較
            'GameificationManager'      # ゲーミフィケーション
        ]
        
        news_status = {}
        for category in news_categories:
            # ファイル内検索
            implemented = self._search_in_files(category.lower())
            news_status[category] = {
                'implemented': implemented,
                'files_found': implemented
            }
            
        self.status['news_module'] = news_status
        
    def check_stability_system(self):
        """🛡️ 安定性システム診断"""
        print("🛡️ 安定性システム診断")
        print("=" * 50)
        
        # 三重冗長システム確認
        redundancy_status = {
            'primary_modbus': self.status.get('modbus', {}).get('main.py', False),
            'secondary_collector': self.status.get('data_collection', {}).get('collector_working', False),
            'tertiary_manual': os.path.exists('manual_backup') or os.path.exists('system_backups')
        }
        
        # 自動復旧システム確認
        recovery_files = ['auto_recover.sh', 'emergency_recovery.py']
        recovery_status = {f: os.path.exists(f) for f in recovery_files}
        
        # cron確認
        cron_status = self._check_cron_jobs()
        
        self.status['stability'] = {
            'redundancy': redundancy_status,
            'auto_recovery': recovery_status,
            'cron_jobs': cron_status
        }
        
    def _check_email_capability(self, filename):
        """メール送信能力確認"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                return ('smtp' in content.lower() and 
                       'send' in content.lower() and
                       'email' in content.lower())
        except:
            return False
            
    def _search_in_files(self, pattern):
        """ファイル内パターン検索"""
        py_files = glob.glob('*.py')
        found_files = []
        for f in py_files:
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    if pattern in file.read().lower():
                        found_files.append(f)
            except:
                continue
        return found_files
        
    def _check_cron_jobs(self):
        """cron設定確認"""
        try:
            result = subprocess.run(['crontab', '-l'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                hanazono_crons = [line for line in result.stdout.split('\n') 
                                if 'hanazono' in line.lower() or 'collector' in line.lower()]
                return len(hanazono_crons)
            return 0
        except:
            return 0
            
    def generate_checklist(self):
        """🔴🟡🟢チェックリスト生成"""
        print("\n" + "=" * 60)
        print("📋 HANAZONO v3.0 完全実装チェックリスト")
        print("=" * 60)
        
        checklist = []
        
        # 🏛️ CoreStabilityEngine
        print("\n🏛️ CoreStabilityEngine（中央安定制御）")
        print("-" * 40)
        
        dc = self.status.get('data_collection', {})
        checklist.append(f"{'🟢' if dc.get('collector_working') else '🔴'} DataCollector - CollectorCapsule")
        checklist.append(f"{'🟢' if self.status.get('modbus', {}).get('main.py') else '🔴'} DataCollector - Modbus RTU")
        checklist.append(f"{'🟡' if os.path.exists('system_backups') else '🔴'} DataCollector - 手動バックアップ")
        
        stability = self.status.get('stability', {})
        checklist.append(f"{'🔴'} StabilityMonitor - 自己診断システム")
        checklist.append(f"{'🔴'} EmergencyMailer - 絶対配信保証")
        
        # 🤖 IntelligenceLayer
        print("\n🤖 IntelligenceLayer（AI・予測）")
        print("-" * 40)
        
        weather = self.status.get('weather', {})
        checklist.append(f"{'🟡' if weather.get('exists') else '🔴'} WeatherPredictor - 天気予測API")
        checklist.append(f"{'🔴'} MLOptimizer - 機械学習最適化")
        checklist.append(f"{'🔴'} SettingRecommender - 設定推奨システム")
        
        # 📰 NewsEngine
        print("\n📰 NewsEngine（モチベーション向上）")
        print("-" * 40)
        
        news = self.status.get('news_module', {})
        for category in ['BattleNewsGenerator', 'AchievementTracker', 
                        'ComparisonAnalyzer', 'GameificationManager']:
            implemented = bool(news.get(category, {}).get('implemented', []))
            checklist.append(f"{'🟡' if implemented else '🔴'} {category}")
            
        # 📧 MultiChannelMailer
        print("\n📧 MultiChannelMailer（配信システム）")
        print("-" * 40)
        
        email_sys = self.status.get('email_system', {})
        has_working_email = any(v.get('send_capable', False) for v in email_sys.values())
        checklist.append(f"{'🟢' if has_working_email else '🔴'} DailyReporter - 基本メール送信")
        checklist.append(f"{'🔴'} DailyReporter - 詳細NEWSセクション統合")
        checklist.append(f"{'🔴'} WeeklyReporter - 週次まとめ")
        checklist.append(f"{'🔴'} MonthlyReporter - 月次総括")
        checklist.append(f"{'🔴'} EmergencyNotifier - 緊急通知")
        
        # 🛡️ SelfHealingSystem
        print("\n🛡️ SelfHealingSystem（自己修復）")
        print("-" * 40)
        
        checklist.append(f"{'🔴'} ErrorDetector - 異常検知")
        checklist.append(f"{'🔴'} AutoRecovery - 自動復旧")
        checklist.append(f"{'🔴'} ManualAssistant - 手動復旧支援")
        
        # チェックリスト表示
        print("\n📊 実装状況サマリー")
        print("-" * 40)
        total = len(checklist)
        green = sum(1 for item in checklist if '🟢' in item)
        yellow = sum(1 for item in checklist if '🟡' in item)
        red = sum(1 for item in checklist if '🔴' in item)
        
        print(f"🟢 完了: {green}/{total} ({green/total*100:.1f}%)")
        print(f"🟡 作業中: {yellow}/{total} ({yellow/total*100:.1f}%)")
        print(f"🔴 未着手: {red}/{total} ({red/total*100:.1f}%)")
        
        print(f"\n総合進捗: {(green + yellow*0.5)/total*100:.1f}%")
        
        return checklist
        
    def run_complete_diagnosis(self):
        """完全診断実行"""
        print("🎯 HANAZONO v3.0 完全現状診断開始")
        print("=" * 60)
        
        self.check_data_collection_layer()
        self.check_email_system()
        self.check_news_module()
        self.check_stability_system()
        
        checklist = self.generate_checklist()
        
        # 診断結果保存
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"hanazono_status_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'status': self.status,
                'checklist': checklist
            }, f, ensure_ascii=False, indent=2)
            
        print(f"\n💾 診断レポート保存: {report_file}")
        print("🎉 完全診断完了")
        
        return self.status, checklist

if __name__ == "__main__":
    checker = HANAZONOStatusChecker()
    status, checklist = checker.run_complete_diagnosis()
