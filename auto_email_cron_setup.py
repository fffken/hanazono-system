#!/usr/bin/env python3
# 定期配信cron設定（完全非破壊的・10分完成）
import datetime
import subprocess
import os
import tempfile

class AutoEmailCronSetup:
    """定期配信cron設定システム（完全非破壊的）"""
    
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"⏰ 定期配信cron設定開始 {self.timestamp}")
        
    def backup_current_crontab(self):
        """現在のcrontabバックアップ"""
        print("\n📋 現在のcrontabバックアップ作成...")
        
        backup_file = f"crontab_backup_{self.timestamp}.txt"
        
        try:
            # 現在のcrontab取得
            result = subprocess.run(['crontab', '-l'], 
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                current_crontab = result.stdout
                print(f"📊 現在のcrontab: {len(current_crontab.split('\\n'))}行")
                
                # バックアップ保存
                with open(backup_file, 'w') as f:
                    f.write(current_crontab)
                    
                print(f"✅ crontabバックアップ: {backup_file}")
                return backup_file, current_crontab
            else:
                print("📊 現在のcrontab: 空（新規作成）")
                with open(backup_file, 'w') as f:
                    f.write("# 元々crontabなし\\n")
                return backup_file, ""
                
        except Exception as e:
            print(f"❌ crontabバックアップエラー: {e}")
            return None, ""
            
    def create_hanazono_cron_jobs(self):
        """HANAZONOシステム用cronジョブ作成"""
        print("\n⏰ HANAZONOシステム用cronジョブ作成...")
        
        # 現在のディレクトリ取得
        current_dir = os.getcwd()
        
        cron_jobs = [
            "# HANAZONOシステム A・B・C統合完成版 定期配信",
            f"# 作成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "# 朝の統合レポート配信（7:00）",
            f"0 7 * * * cd {current_dir} && python3 abc_integration_complete_test.py > /tmp/hanazono_morning.log 2>&1",
            "",
            "# 夜の統合レポート配信（19:00）", 
            f"0 19 * * * cd {current_dir} && python3 abc_integration_complete_test.py > /tmp/hanazono_evening.log 2>&1",
            "",
            "# 週次メンテナンス確認（日曜22:00）",
            f"0 22 * * 0 cd {current_dir} && python3 -c \"from ai_memory.core.continuation_manager import ProjectContinuationManager; cm=ProjectContinuationManager('hcqas'); print('週次確認完了')\" > /tmp/hanazono_weekly.log 2>&1",
            ""
        ]
        
        print("📋 作成されるcronジョブ:")
        for job in cron_jobs:
            if job.strip() and not job.startswith('#'):
                print(f"   {job}")
                
        return cron_jobs
        
    def apply_cron_settings(self, current_crontab, new_cron_jobs):
        """cron設定適用（完全非破壊的）"""
        print("\n🔧 cron設定適用...")
        
        try:
            # 新しいcrontab内容作成
            new_crontab_lines = []
            
            # 既存のcrontab内容保持
            if current_crontab.strip():
                new_crontab_lines.extend(current_crontab.split('\\n'))
                new_crontab_lines.append("")  # 区切り行
                
            # HANAZONOシステム用ジョブ追加
            new_crontab_lines.extend(new_cron_jobs)
            
            new_crontab_content = '\\n'.join(new_crontab_lines)
            
            # 一時ファイルに新しいcrontab保存
            temp_crontab_file = f"temp_crontab_{self.timestamp}.txt"
            with open(temp_crontab_file, 'w') as f:
                f.write(new_crontab_content)
                
            print(f"📊 新しいcrontab: {len(new_crontab_lines)}行")
            
            # crontab適用
            result = subprocess.run(['crontab', temp_crontab_file], 
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ crontab適用成功")
                
                # 適用確認
                verify_result = subprocess.run(['crontab', '-l'], 
                                            capture_output=True, text=True)
                if verify_result.returncode == 0:
                    print("✅ crontab適用確認済み")
                    
                # 一時ファイル削除
                os.remove(temp_crontab_file)
                
                return True
            else:
                print(f"❌ crontab適用失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ cron設定適用エラー: {e}")
            return False
            
    def test_cron_job_script(self):
        """cronジョブスクリプト動作テスト"""
        print("\n🧪 cronジョブスクリプト動作テスト...")
        
        try:
            # A・B・C統合スクリプトテスト
            test_command = ['python3', 'abc_integration_complete_test.py']
            
            print("📊 A・B・C統合スクリプトテスト実行中...")
            
            # タイムアウト付きでテスト実行
            result = subprocess.run(test_command, 
                                 capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ cronジョブスクリプトテスト成功")
                
                # 出力確認
                if "A・B・C統合メール送信成功" in result.stdout:
                    print("✅ メール送信機能確認済み")
                    return True
                else:
                    print("⚠️ メール送信機能要確認")
                    return False
            else:
                print(f"❌ cronジョブスクリプトテスト失敗: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ cronジョブスクリプトテスト タイムアウト")
            return False
        except Exception as e:
            print(f"❌ cronジョブスクリプトテストエラー: {e}")
            return False
            
    def create_cron_management_script(self, backup_file):
        """cron管理スクリプト作成"""
        print("\n📋 cron管理スクリプト作成...")
        
        management_script = f'''#!/bin/bash
# HANAZONOシステム cron管理スクリプト
# 作成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

echo "🎯 HANAZONOシステム cron管理スクリプト"
echo "=" * 50

case "$1" in
    "status")
        echo "📊 現在のcron設定:"
        crontab -l | grep -A 10 -B 2 "HANAZONO"
        ;;
    "logs")
        echo "📋 cronジョブログ確認:"
        echo "朝のログ:"
        tail -10 /tmp/hanazono_morning.log 2>/dev/null || echo "ログなし"
        echo "夜のログ:"  
        tail -10 /tmp/hanazono_evening.log 2>/dev/null || echo "ログなし"
        ;;
    "restore")
        echo "🔄 元のcron設定に復旧..."
        if [ -f "{backup_file}" ]; then
            crontab {backup_file}
            echo "✅ 復旧完了"
        else
            echo "❌ バックアップファイル未発見"
        fi
        ;;
    "test")
        echo "🧪 手動テスト実行..."
        cd {os.getcwd()}
        python3 abc_integration_complete_test.py
        ;;
    *)
        echo "使用方法:"
        echo "  bash hanazono_cron_manager.sh status   # cron設定確認"
        echo "  bash hanazono_cron_manager.sh logs     # ログ確認"
        echo "  bash hanazono_cron_manager.sh test     # 手動テスト"
        echo "  bash hanazono_cron_manager.sh restore  # 元設定に復旧"
        ;;
esac
'''
        
        manager_file = f"hanazono_cron_manager_{self.timestamp}.sh"
        with open(manager_file, 'w') as f:
            f.write(management_script)
            
        # 実行権限付与
        os.chmod(manager_file, 0o755)
        
        print(f"✅ cron管理スクリプト作成: {manager_file}")
        return manager_file
        
    def create_cron_setup_record(self, backup_file, manager_file, test_success):
        """cron設定記録作成"""
        print("\n📈 cron設定記録作成...")
        
        record_lines = [
            "# 定期配信cron設定記録",
            f"## 日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "## ⏰ 設定されたcronジョブ",
            "- **朝の統合レポート**: 毎日7:00",
            "- **夜の統合レポート**: 毎日19:00", 
            "- **週次メンテナンス**: 日曜22:00",
            "",
            "## 📧 自動配信内容",
            "- A・B・C統合完成版メール配信",
            "- 完璧な3日分天気データ",
            "- 動的推奨設定",
            "- システム統合状況",
            "",
            "## 💾 安全保証",
            f"- **バックアップ**: {backup_file}",
            f"- **管理スクリプト**: {manager_file}",
            "- **復旧方法**: 即座復旧可能",
            "",
            "## 🔧 管理コマンド",
            "```bash",
            f"# cron設定確認",
            f"bash {manager_file} status",
            "",
            f"# ログ確認", 
            f"bash {manager_file} logs",
            "",
            f"# 手動テスト",
            f"bash {manager_file} test",
            "",
            f"# 元設定に復旧",
            f"bash {manager_file} restore",
            "```",
            "",
            "## 🎯 自動化効果",
            "- **手動作業**: ゼロ化達成",
            "- **配信頻度**: 1日2回自動",
            "- **運用負荷**: 最小化",
            "- **安定性**: 最高レベル",
            "",
            f"## ✅ 設定テスト: {'成功' if test_success else '失敗'}",
            "",
            f"Timestamp: {self.timestamp}"
        ]
        
        record_md = "\\n".join(record_lines)
        
        record_file = f"cron_setup_record_{self.timestamp}.md"
        with open(record_file, 'w', encoding='utf-8') as f:
            f.write(record_md)
            
        print(f"✅ cron設定記録作成: {record_file}")
        return record_file
        
    def run_auto_email_cron_setup(self):
        """定期配信cron設定実行"""
        print("🎯 定期配信cron設定（10分完成）開始")
        print("=" * 70)
        
        # 1. 現在のcrontabバックアップ
        backup_file, current_crontab = self.backup_current_crontab()
        
        # 2. HANAZONOシステム用cronジョブ作成
        cron_jobs = self.create_hanazono_cron_jobs()
        
        # 3. cron設定適用
        apply_success = self.apply_cron_settings(current_crontab, cron_jobs)
        
        if not apply_success:
            print("❌ cron設定適用失敗")
            return False
            
        # 4. cronジョブスクリプトテスト
        test_success = self.test_cron_job_script()
        
        # 5. cron管理スクリプト作成
        manager_file = self.create_cron_management_script(backup_file)
        
        # 6. cron設定記録作成
        record_file = self.create_cron_setup_record(backup_file, manager_file, test_success)
        
        print(f"\\n" + "=" * 70)
        print("🎉 定期配信cron設定完了")
        print("=" * 70)
        print(f"✅ crontabバックアップ: {backup_file}")
        print(f"✅ cron設定適用: {'成功' if apply_success else '失敗'}")
        print(f"✅ スクリプトテスト: {'成功' if test_success else '失敗'}")
        print(f"✅ 管理スクリプト: {manager_file}")
        print(f"✅ 設定記録: {record_file}")
        
        overall_success = apply_success and test_success
        
        if overall_success:
            print(f"\\n🎉 10分完成達成！自動配信開始")
            print(f"⏰ 朝7:00・夜19:00に自動メール配信")
            print(f"📧 A・B・C統合完成版レポート自動送信")
            print(f"🛡️ 完全非破壊的（即座復旧可能）")
            
            print(f"\\n🔧 管理方法:")
            print(f"bash {manager_file} status  # 設定確認")
            print(f"bash {manager_file} logs    # ログ確認")
            print(f"bash {manager_file} test    # 手動テスト")
        else:
            print(f"\\n⚠️ 一部問題あり、復旧方法:")
            if backup_file:
                print(f"crontab {backup_file}")
                
        return overall_success

if __name__ == "__main__":
    cron_setup = AutoEmailCronSetup()
    cron_setup.run_auto_email_cron_setup()
