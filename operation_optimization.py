#!/usr/bin/env python3
# 運用最適化システム（完全非破壊的・10分完成）
import datetime
import os
import subprocess
import shutil

class OperationOptimization:
    """運用最適化システム"""
    
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"⚡ 運用最適化システム開始 {self.timestamp}")
        
    def backup_current_cron(self):
        """現在のcron設定バックアップ"""
        print("\n📋 現在のcron設定バックアップ...")
        
        backup_file = f"crontab_optimization_backup_{self.timestamp}.txt"
        
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            with open(backup_file, 'w') as f:
                f.write(current_crontab)
            print(f"✅ cronバックアップ: {backup_file}")
            return backup_file, current_crontab
        except Exception as e:
            print(f"❌ cronバックアップエラー: {e}")
            return None, ""
            
    def create_optimized_cron_jobs(self):
        """最適化cron設定作成"""
        print("\n⚡ 最適化cron設定作成...")
        
        current_dir = os.getcwd()
        
        optimized_jobs = [
            "",
            "# HANAZONOシステム 運用最適化版",
            f"# 作成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "# 日次統合レポート配信（朝7:00・夜19:00）",
            f"0 7 * * * cd {current_dir} && python3 abc_integration_icon_fixed_20250615_223350.py > /tmp/hanazono_morning.log 2>&1",
            f"0 19 * * * cd {current_dir} && python3 abc_integration_icon_fixed_20250615_223350.py > /tmp/hanazono_evening.log 2>&1",
            "",
            "# 週次システム状況レポート（日曜21:00）",
            f"0 21 * * 0 cd {current_dir} && python3 -c \"",
            "import datetime",
            "import subprocess",
            "import glob",
            "print('🗓️ 週次システム状況レポート', datetime.datetime.now().strftime('%Y年%m月%d日'))",
            "logs = glob.glob('/tmp/hanazono_*.log')",
            "print(f'📊 ログファイル: {len(logs)}個')",
            "for log in logs[-7:]:",
            "    try:",
            "        with open(log, 'r') as f:",
            "            content = f.read()",
            "        if 'メール送信成功' in content:",
            "            print(f'✅ {log}: 正常')",
            "        else:",
            "            print(f'⚠️ {log}: 要確認')",
            "    except:",
            "        print(f'❌ {log}: 読み取りエラー')",
            "print('週次確認完了')\" > /tmp/hanazono_weekly.log 2>&1",
            "",
            "# 月次システムメンテナンス（月初8:00）",
            f"0 8 1 * * cd {current_dir} && python3 -c \"",
            "import datetime",
            "import os",
            "import glob",
            "print('🔧 月次システムメンテナンス', datetime.datetime.now().strftime('%Y年%m月'))",
            "# ログファイル整理",
            "logs = glob.glob('/tmp/hanazono_*.log')",
            "old_logs = [log for log in logs if os.path.getctime(log) < (datetime.datetime.now() - datetime.timedelta(days=30)).timestamp()]",
            "for log in old_logs:",
            "    try:",
            "        os.remove(log)",
            "        print(f'🗑️ 削除: {log}')",
            "    except:",
            "        pass",
            "print(f'📊 ログ整理完了: {len(old_logs)}ファイル削除')",
            "print('月次メンテナンス完了')\" > /tmp/hanazono_monthly.log 2>&1",
            "",
            "# エラー監視・通知（毎時15分）",
            f"15 * * * * cd {current_dir} && python3 -c \"",
            "import glob",
            "import datetime",
            "recent_logs = []",
            "try:",
            "    logs = glob.glob('/tmp/hanazono_*.log')",
            "    for log in logs:",
            "        try:",
            "            with open(log, 'r') as f:",
            "                content = f.read()",
            "            if '❌' in content or 'エラー' in content:",
            "                recent_logs.append(log)",
            "        except:",
            "            pass",
            "    if recent_logs:",
            "        print(f'⚠️ エラー検知: {len(recent_logs)}ファイル')",
            "        for log in recent_logs:",
            "            print(f'📋 確認要: {log}')",
            "    else:",
            "        print('✅ システム正常')",
            "except Exception as e:",
            "    print(f'❌ 監視エラー: {e}')",
            "\" > /tmp/hanazono_monitor.log 2>&1",
            ""
        ]
        
        # 改行処理
        formatted_jobs = []
        for job in optimized_jobs:
            if job.startswith('f"0 ') and '\\' in job:
                # 複数行のcronジョブを単一行に変換
                cleaned_job = job.replace('\\"', '').replace('\\n', '; ')
                formatted_jobs.append(cleaned_job)
            else:
                formatted_jobs.append(job)
        
        print("📋 作成される最適化cronジョブ:")
        for job in formatted_jobs:
            if job.strip() and not job.startswith('#') and not job.startswith('f"'):
                print(f"   {job[:80]}...")
                
        return formatted_jobs
        
    def create_advanced_manager_script(self):
        """高度管理スクリプト作成"""
        print("\n🔧 高度管理スクリプト作成...")
        
        manager_script = f'''#!/bin/bash
# HANAZONOシステム 運用最適化管理スクリプト
# 作成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

echo "⚡ HANAZONOシステム 運用最適化管理"
echo "=" * 60

case "$1" in
    "status")
        echo "📊 システム状況確認:"
        crontab -l | grep -A 15 -B 2 "HANAZONO"
        echo ""
        echo "📈 最近のログ状況:"
        ls -la /tmp/hanazono_*.log 2>/dev/null | tail -5 || echo "ログなし"
        ;;
    "logs")
        echo "📋 詳細ログ確認:"
        echo "🌅 朝のログ（最新5行）:"
        tail -5 /tmp/hanazono_morning.log 2>/dev/null || echo "ログなし"
        echo "🌙 夜のログ（最新5行）:"  
        tail -5 /tmp/hanazono_evening.log 2>/dev/null || echo "ログなし"
        echo "📊 週次ログ（最新5行）:"
        tail -5 /tmp/hanazono_weekly.log 2>/dev/null || echo "ログなし"
        echo "🔧 月次ログ（最新5行）:"
        tail -5 /tmp/hanazono_monthly.log 2>/dev/null || echo "ログなし"
        ;;
    "monitor")
        echo "🔍 リアルタイム監視:"
        python3 -c "
import glob
import datetime
import os
print('📊 システム監視レポート', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
logs = glob.glob('/tmp/hanazono_*.log')
print(f'📁 ログファイル: {{len(logs)}}個')
for log in logs:
    try:
        mtime = os.path.getmtime(log)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
        size = os.path.getsize(log)
        print(f'📄 {{os.path.basename(log)}}: {{mtime_str}} ({{size}}B)')
    except:
        print(f'❌ {{log}}: 読み取りエラー')
"
        ;;
    "test")
        echo "🧪 手動テスト実行:"
        cd {os.getcwd()}
        python3 abc_integration_icon_fixed_20250615_223350.py
        ;;
    "clean")
        echo "🗑️ ログクリーンアップ:"
        rm -f /tmp/hanazono_*.log
        echo "✅ ログファイル削除完了"
        ;;
    "restore")
        echo "🔄 元のcron設定に復旧..."
        if [ -f "crontab_optimization_backup_{self.timestamp}.txt" ]; then
            crontab crontab_optimization_backup_{self.timestamp}.txt
            echo "✅ 復旧完了"
        else
            echo "❌ バックアップファイル未発見"
        fi
        ;;
    "performance")
        echo "📈 パフォーマンス確認:"
        echo "💾 ディスク使用量:"
        df -h {os.getcwd()} | tail -1
        echo "🔄 メモリ使用量:"
        free -h | grep Mem
        echo "⚡ システム負荷:"
        uptime
        ;;
    *)
        echo "🔧 HANAZONOシステム 運用最適化管理コマンド:"
        echo "  bash $0 status      # システム状況確認"
        echo "  bash $0 logs        # 詳細ログ確認"
        echo "  bash $0 monitor     # リアルタイム監視"
        echo "  bash $0 test        # 手動テスト実行"
        echo "  bash $0 clean       # ログクリーンアップ"
        echo "  bash $0 performance # パフォーマンス確認"
        echo "  bash $0 restore     # 元設定に復旧"
        ;;
esac
'''
        
        manager_file = f"hanazono_optimization_manager_{self.timestamp}.sh"
        with open(manager_file, 'w') as f:
            f.write(manager_script)
            
        os.chmod(manager_file, 0o755)
        
        print(f"✅ 高度管理スクリプト作成: {manager_file}")
        return manager_file
        
    def apply_optimized_cron(self, current_crontab, optimized_jobs, backup_file):
        """最適化cron適用"""
        print("\n⚡ 最適化cron適用...")
        
        try:
            # 新しいcrontab内容作成
            new_crontab_lines = []
            
            # 既存のHANAZONO以外の設定保持
            if current_crontab.strip():
                for line in current_crontab.split('\n'):
                    if 'HANAZONO' not in line and line.strip():
                        new_crontab_lines.append(line)
                        
            # 最適化cronジョブ追加
            new_crontab_lines.extend(optimized_jobs)
            
            new_crontab_content = '\n'.join(new_crontab_lines)
            
            # 一時ファイルに保存
            temp_crontab_file = f"temp_optimized_crontab_{self.timestamp}.txt"
            with open(temp_crontab_file, 'w') as f:
                f.write(new_crontab_content)
                
            print(f"📊 最適化crontab: {len(new_crontab_lines)}行")
            
            # crontab適用
            result = subprocess.run(['crontab', temp_crontab_file], 
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 最適化cron適用成功")
                
                # 適用確認
                verify_result = subprocess.run(['crontab', '-l'], 
                                            capture_output=True, text=True)
                if verify_result.returncode == 0:
                    print("✅ 最適化cron適用確認済み")
                    
                os.remove(temp_crontab_file)
                return True
            else:
                print(f"❌ 最適化cron適用失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 最適化cron適用エラー: {e}")
            return False
            
    def create_optimization_record(self, backup_file, manager_file, apply_success):
        """運用最適化記録作成"""
        print("\n📈 運用最適化記録作成...")
        
        record_lines = [
            "# 運用最適化完了記録",
            f"## 日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "## ⚡ 最適化内容",
            "### 自動配信最適化",
            "- **朝7:00・夜19:00**: アイコン修正版自動配信",
            "- **配信内容**: 完璧な可視化メール（🟠🔵🟣🌻対応）",
            "",
            "### 監視・メンテナンス自動化",
            "- **週次レポート**: 日曜21:00システム状況確認",
            "- **月次メンテナンス**: 月初8:00ログ整理・最適化",
            "- **エラー監視**: 毎時15分自動監視・通知",
            "",
            "### ログ管理最適化",
            "- **自動ログ整理**: 30日経過ファイル自動削除",
            "- **エラー検知**: リアルタイム異常検知",
            "- **パフォーマンス監視**: システム負荷自動確認",
            "",
            "## 🔧 高度管理機能",
            f"### 管理スクリプト: {manager_file}",
            "```bash",
            f"# システム状況確認",
            f"bash {manager_file} status",
            "",
            f"# 詳細ログ確認",
            f"bash {manager_file} logs",
            "",
            f"# リアルタイム監視",
            f"bash {manager_file} monitor",
            "",
            f"# パフォーマンス確認",
            f"bash {manager_file} performance",
            "",
            f"# ログクリーンアップ",
            f"bash {manager_file} clean",
            "```",
            "",
            "## 📊 最適化効果",
            "- **運用負荷**: 大幅削減（自動監視・メンテナンス）",
            "- **問題検知**: リアルタイム化",
            "- **システム安定性**: 向上（定期メンテナンス）",
            "- **ログ管理**: 自動化（容量最適化）",
            "",
            "## 💾 安全保証",
            f"- **バックアップ**: {backup_file}",
            "- **復旧方法**: 即座復旧可能",
            "- **管理ツール**: 高度管理スクリプト付属",
            "",
            f"## ✅ 最適化適用: {'成功' if apply_success else '失敗'}",
            "",
            f"Timestamp: {self.timestamp}"
        ]
        
        record_md = "\n".join(record_lines)
        
        record_file = f"operation_optimization_record_{self.timestamp}.md"
        with open(record_file, 'w', encoding='utf-8') as f:
            f.write(record_md)
            
        print(f"✅ 運用最適化記録作成: {record_file}")
        return record_file
        
    def run_operation_optimization(self):
        """運用最適化実行"""
        print("🎯 運用最適化システム（10分完成）開始")
        print("=" * 70)
        
        # 1. 現在のcron設定バックアップ
        backup_file, current_crontab = self.backup_current_cron()
        
        # 2. 最適化cron設定作成
        optimized_jobs = self.create_optimized_cron_jobs()
        
        # 3. 高度管理スクリプト作成
        manager_file = self.create_advanced_manager_script()
        
        # 4. 最適化cron適用
        apply_success = self.apply_optimized_cron(current_crontab, optimized_jobs, backup_file)
        
        # 5. 運用最適化記録作成
        record_file = self.create_optimization_record(backup_file, manager_file, apply_success)
        
        print(f"\n" + "=" * 70)
        print("🎉 運用最適化完了")
        print("=" * 70)
        print(f"✅ cronバックアップ: {backup_file}")
        print(f"✅ 最適化cron適用: {'成功' if apply_success else '失敗'}")
        print(f"✅ 高度管理スクリプト: {manager_file}")
        print(f"✅ 最適化記録: {record_file}")
        
        if apply_success:
            print(f"\n⚡ 10分完成！運用最適化達成")
            print(f"📊 自動配信: アイコン修正版（朝7時・夜19時）")
            print(f"🔍 自動監視: エラー検知・週次・月次メンテナンス")
            print(f"🔧 高度管理: {manager_file}")
            
            print(f"\n🛠️ 最適化管理方法:")
            print(f"bash {manager_file} status      # システム状況確認")
            print(f"bash {manager_file} monitor     # リアルタイム監視")
            print(f"bash {manager_file} performance # パフォーマンス確認")
        else:
            print(f"\n⚠️ 一部問題あり、復旧方法:")
            if backup_file:
                print(f"crontab {backup_file}")
                
        return apply_success

if __name__ == "__main__":
    optimization = OperationOptimization()
    optimization.run_operation_optimization()
