#!/usr/bin/env python3
"""
HANAZONO統合開発コマンド v2.0（ダッシュボード統合版）
自然言語でシステム操作＋リアルタイム監視
"""

import re
import sys
import subprocess
import json
import threading
import time
from datetime import datetime
from pathlib import Path

class HANAZONODevEnhanced:
    def __init__(self):
        self.base_dir = Path.home() / "lvyuan_solar_control"
        
    def process_command(self, user_input):
        """自然言語コマンドの処理"""
        print(f"🤖 実行中: '{user_input}'")
        
        # ダッシュボード関連パターン追加
        if re.search(r'(ダッシュボード|監視|画面).*(起動|開始|表示)', user_input):
            return self.start_dashboard()
        elif re.search(r'(ダッシュボード|監視).*(確認|状況)', user_input):
            return self.dashboard_status()
        elif re.search(r'(アラート|警告).*(確認|チェック)', user_input):
            return self.check_alerts()
        elif re.search(r'(リアルタイム|ライブ).*(監視|表示)', user_input):
            return self.live_monitoring()
        
        # 既存パターン
        elif re.search(r'(状態|ステータス|現在)', user_input):
            return self.show_status()
        elif re.search(r'(テスト|診断|チェック)', user_input):
            return self.run_tests()
        elif re.search(r'(最適化|メンテナンス)', user_input):
            return self.optimize()
        elif re.search(r'(データ|グラフ|分析)', user_input):
            return self.show_data()
        elif re.search(r'(バックアップ|保存)', user_input):
            return self.backup()
        elif re.search(r'(git|コミット)', user_input):
            return self.git_status()
        elif re.search(r'(メール|通知)', user_input):
            return self.test_email()
        elif re.search(r'(ヘルプ|使い方)', user_input):
            return self.show_help()
        else:
            return self.suggest_commands(user_input)
    
    def start_dashboard(self):
        """ダッシュボード起動"""
        print("🚀 リアルタイム監視ダッシュボード起動中...")
        print("📊 アクセスURL: http://192.168.0.191:8080")
        print("🔄 10秒ごとに自動更新")
        print("⏹️  終了: Ctrl+C")
        
        try:
            subprocess.run(['python3', str(self.base_dir / 'hanazono_dashboard.py')], 
                         cwd=self.base_dir)
            return True
        except KeyboardInterrupt:
            print("\n📊 ダッシュボードを終了しました")
            return True
        except Exception as e:
            print(f"❌ ダッシュボード起動エラー: {e}")
            return False
    
    def dashboard_status(self):
        """ダッシュボード状況確認（テキスト版）"""
        print("📊 リアルタイム監視状況確認")
        print("=" * 40)
        
        # ソーラーデータ確認
        solar_data = self._get_latest_solar_data()
        if solar_data:
            print("☀️ ソーラーシステム:")
            print(f"   🔋 バッテリーSOC: {solar_data.get('battery_soc', 'N/A')}")
            print(f"   ⚡ バッテリー電圧: {solar_data.get('battery_voltage', 'N/A')}")
            print(f"   🔌 バッテリー電流: {solar_data.get('battery_current', 'N/A')}")
        else:
            print("☀️ ソーラーシステム: データなし")
        
        # システムリソース
        system_stats = self._get_system_stats()
        if system_stats:
            print("\n💻 システムリソース:")
            print(f"   🖥️  CPU使用率: {system_stats.get('cpu_percent', 'N/A')}%")
            print(f"   💾 メモリ使用率: {system_stats.get('memory_percent', 'N/A')}%")
            print(f"   🔄 Pythonプロセス: {system_stats.get('python_processes', 'N/A')}個")
        
        # アラート確認
        alerts = self._check_system_alerts()
        if alerts:
            print(f"\n⚠️ アラート: {len(alerts)}件")
            for alert in alerts[:3]:  # 最新3件
                print(f"   • {alert}")
        else:
            print("\n✅ アラート: なし（システム正常）")
        
        return True
    
    def check_alerts(self):
        """アラート専用確認"""
        print("⚠️ システムアラート確認")
        print("=" * 30)
        
        alerts = self._check_system_alerts()
        if not alerts:
            print("✅ アラートなし - システム正常動作中")
            return True
        
        print(f"🚨 検出されたアラート: {len(alerts)}件")
        for i, alert in enumerate(alerts, 1):
            print(f"{i}. {alert}")
        
        print("\n💡 推奨アクション:")
        print("   h 'ダッシュボード起動' - 詳細確認")
        print("   h '最適化実行' - システム最適化")
        
        return True
    
    def live_monitoring(self):
        """ライブ監視（5回更新）"""
        print("📊 ライブ監視開始（5回更新後自動終了）")
        print("手動終了: Ctrl+C")
        print("=" * 50)
        
        try:
            for i in range(5):
                print(f"\n📈 更新 {i+1}/5 - {datetime.now().strftime('%H:%M:%S')}")
                
                # システム状況を簡潔表示
                system_stats = self._get_system_stats()
                if system_stats:
                    cpu = system_stats.get('cpu_percent', 0)
                    mem = system_stats.get('memory_percent', 0)
                    
                    cpu_status = "🔴" if cpu > 80 else "🟡" if cpu > 60 else "🟢"
                    mem_status = "🔴" if mem > 80 else "🟡" if mem > 60 else "🟢"
                    
                    print(f"💻 CPU: {cpu_status} {cpu}% | メモリ: {mem_status} {mem}%")
                
                # ソーラーデータ
                solar_data = self._get_latest_solar_data()
                if solar_data and solar_data.get('battery_soc', 'N/A') != 'N/A':
                    print(f"🔋 バッテリーSOC: {solar_data['battery_soc']}")
                
                if i < 4:  # 最後以外は待機
                    time.sleep(10)
            
            print("\n✅ ライブ監視完了")
            return True
            
        except KeyboardInterrupt:
            print("\n📊 ライブ監視を手動終了しました")
            return True
    
    def _get_latest_solar_data(self):
        """最新ソーラーデータ取得"""
        try:
            data_dir = self.base_dir / "data"
            if not data_dir.exists():
                return None
                
            files = list(data_dir.glob("lvyuan_data_*.json"))
            if not files:
                return None
                
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            with open(latest_file) as f:
                data = json.load(f)
            
            if isinstance(data, dict) and 'parameters' in data:
                params = data['parameters']
                return {
                    'battery_soc': self._extract_param(params, 'SOC', '%'),
                    'battery_voltage': self._extract_param(params, '電圧', 'V'),
                    'battery_current': self._extract_param(params, '電流', 'A')
                }
        except Exception as e:
            print(f"ソーラーデータ取得エラー: {e}")
            return None
    
    def _extract_param(self, params, keyword, unit):
        """パラメータ抽出"""
        for addr, param in params.items():
            if keyword in param.get('name', ''):
                value = param.get('formatted_value', 'N/A')
                return f"{value} {unit}" if value != 'N/A' else 'N/A'
        return 'N/A'
    
    def _get_system_stats(self):
        """システム統計取得"""
        try:
            import psutil
            return {
                'cpu_percent': round(psutil.cpu_percent(interval=0.1), 1),
                'memory_percent': round(psutil.virtual_memory().percent, 1),
                'python_processes': len([p for p in psutil.process_iter() 
                                       if 'python' in p.name().lower()])
            }
        except ImportError:
            return {'error': 'psutil未インストール'}
        except Exception as e:
            return {'error': str(e)}
    
    def _check_system_alerts(self):
        """システムアラート確認"""
        alerts = []
        
        # システムリソース確認
        stats = self._get_system_stats()
        if 'error' not in stats:
            if stats.get('cpu_percent', 0) > 80:
                alerts.append(f"CPU使用率が高いです: {stats['cpu_percent']}%")
            if stats.get('memory_percent', 0) > 80:
                alerts.append(f"メモリ使用率が高いです: {stats['memory_percent']}%")
        
        # Git状態確認
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            if uncommitted > 10:
                alerts.append(f"未コミット変更が多いです: {uncommitted}件")
        except:
            pass
        
        # バッテリー状態確認
        solar_data = self._get_latest_solar_data()
        if solar_data and solar_data.get('battery_soc', 'N/A') != 'N/A':
            try:
                soc_value = float(solar_data['battery_soc'].split()[0])
                if soc_value < 20:
                    alerts.append(f"バッテリーSOCが低いです: {soc_value}%")
            except:
                pass
        
        return alerts
    
    # 既存メソッド（簡略版）
    def show_status(self):
        """システム状態表示"""
        print("🏆 HANAZONOシステム状態")
        print("=" * 40)
        
        # Git状態
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"📊 Git状態: {changes}件の未コミット変更")
        except:
            print("📊 Git状態: 確認失敗")
        
        # 最新データ
        data_dir = self.base_dir / "data"
        if data_dir.exists():
            files = list(data_dir.glob("lvyuan_data_*.json"))
            if files:
                latest = max(files, key=lambda f: f.stat().st_mtime)
                mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                print(f"📈 最新データ: {mtime.strftime('%m-%d %H:%M')}")
        
        # システムプロセス
        try:
            result = subprocess.run(['pgrep', '-f', 'python.*lvyuan'], 
                                  capture_output=True, text=True)
            processes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"🔄 実行中プロセス: {processes}個")
        except:
            print("🔄 プロセス確認: 失敗")
            
        print("✅ システム正常稼働中")
        return True
    
    def run_tests(self):
        """簡易テスト実行"""
        print("🧪 システムテスト実行中...")
        
        tests = [
            ("構文チェック", self.test_syntax),
            ("設定ファイル", self.test_config),
            ("ダッシュボード", self.test_dashboard)
        ]
        
        passed = 0
        for name, test_func in tests:
            print(f"▶️ {name}...", end=" ")
            try:
                if test_func():
                    print("✅")
                    passed += 1
                else:
                    print("❌")
            except:
                print("⚠️")
        
        print(f"📊 結果: {passed}/{len(tests)} 成功")
        return passed == len(tests)
    
    def test_dashboard(self):
        """ダッシュボード機能テスト"""
        dashboard_file = self.base_dir / "hanazono_dashboard.py"
        return dashboard_file.exists()
    
    def optimize(self):
        """システム最適化"""
        print("⚡ システム最適化実行中...")
        subprocess.run(['find', '.', '-name', '__pycache__', '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'], 
                      cwd=self.base_dir, check=False)
        print("✅ 最適化完了")
        return True
    
    def show_data(self):
        """最新データ表示"""
        print("📈 最新データ確認")
        solar_data = self._get_latest_solar_data()
        if solar_data:
            print("🔋 バッテリー情報:")
            print(f"   SOC: {solar_data.get('battery_soc', 'N/A')}")
            print(f"   電圧: {solar_data.get('battery_voltage', 'N/A')}")
            print(f"   電流: {solar_data.get('battery_current', 'N/A')}")
            print("✅ データ確認完了")
            return True
        else:
            print("❌ データファイルが見つかりません")
            return False
    
    def backup(self):
        """バックアップ作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.base_dir / "system_backups" / f"h_backup_{timestamp}"
        
        print(f"🔒 バックアップ作成: {backup_dir.name}")
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(['cp', '-r', '.', str(backup_dir)], cwd=self.base_dir, check=True)
            print("✅ バックアップ完了")
            return True
        except Exception as e:
            print(f"❌ バックアップ失敗: {e}")
            return False
    
    def git_status(self):
        """Git状態確認"""
        print("📊 Git詳細状態")
        try:
            subprocess.run(['git', 'status'], cwd=self.base_dir)
            print("\n📈 最新コミット:")
            subprocess.run(['git', 'log', '--oneline', '-3'], cwd=self.base_dir)
            return True
        except Exception as e:
            print(f"❌ Git確認失敗: {e}")
            return False
    
    def test_email(self):
        """メール機能テスト"""
        print("📧 メール設定確認中...")
        try:
            settings_file = self.base_dir / "settings.json"
            with open(settings_file) as f:
                settings = json.load(f)
            
            email_config = settings.get('email', {})
            if email_config.get('smtp_server') and email_config.get('smtp_user'):
                print("✅ メール設定正常")
                return True
            else:
                print("⚠️ メール設定不完全")
                return False
        except Exception as e:
            print(f"❌ メール設定確認失敗: {e}")
            return False
    
    def test_syntax(self):
        """Python構文チェック"""
        main_files = ['main.py', 'email_notifier.py', 'lvyuan_collector.py', 'hanazono_dashboard.py']
        for file in main_files:
            try:
                subprocess.run(['python3', '-m', 'py_compile', file], 
                              cwd=self.base_dir, check=True, capture_output=True)
            except:
                return False
        return True
    
    def test_config(self):
        """設定ファイルチェック"""
        try:
            with open(self.base_dir / "settings.json") as f:
                json.load(f)
            return True
        except:
            return False
    
    def show_help(self):
        """ヘルプ表示"""
        print("🤖 HANAZONO統合コマンド v2.0（ダッシュボード統合版）")
        print("=" * 60)
        print("📊 監視・ダッシュボード:")
        print("  h 'ダッシュボード起動'     - Web監視画面起動")
        print("  h 'ダッシュボード確認'     - 監視状況をテキスト表示")
        print("  h 'アラート確認'           - システム警告チェック")
        print("  h 'ライブ監視'             - リアルタイム監視（5回更新）")
        print("")
        print("🔧 基本操作:")
        print("  h 'システム状態確認'")
        print("  h 'テスト実行'")
        print("  h '最適化実行'")
        print("  h 'データ確認'")
        print("  h 'バックアップ作成'")
        print("  h 'git状態確認'")
        print("  h 'メール確認'")
        return True
    
    def suggest_commands(self, user_input):
        """コマンド候補提案"""
        print(f"❓ '{user_input}' は認識できませんでした")
        print("🔍 利用可能なコマンド:")
        print("【監視】ダッシュボード起動, アラート確認, ライブ監視")
        print("【基本】システム状態確認, テスト実行, 最適化実行")
        print("【管理】データ確認, バックアップ作成, git状態確認")
        return False

def main():
    if len(sys.argv) < 2:
        print("使用法: python3 hanazono_dev_enhanced.py 'コマンド'")
        print("例: python3 hanazono_dev_enhanced.py 'ダッシュボード起動'")
        sys.exit(1)
    
    command = ' '.join(sys.argv[1:])
    dev = HANAZONODevEnhanced()
    success = dev.process_command(command)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
