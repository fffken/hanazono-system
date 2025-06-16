#!/usr/bin/env python3
# cron設定をアイコン修正完成版に切り替え（完全非破壊的）
import datetime
import subprocess
import os

def switch_to_icon_fixed_cron():
    """cronをアイコン修正完成版に切り替え"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔄 cronアイコン修正版切り替え開始 {timestamp}")
    
    # 1. 現在のcron設定バックアップ
    backup_file = f"crontab_before_icon_switch_{timestamp}.txt"
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""
        
        with open(backup_file, 'w') as f:
            f.write(current_crontab)
        print(f"✅ 現在のcronバックアップ: {backup_file}")
    except Exception as e:
        print(f"❌ cronバックアップエラー: {e}")
        return False
    
    # 2. 新しいcron設定作成（アイコン修正版使用）
    current_dir = os.getcwd()
    icon_fixed_file = "abc_integration_icon_fixed_20250615_223350.py"
    
    new_cron_jobs = [
        "",
        "# HANAZONOシステム アイコン修正完成版 自動配信",
        f"# 切り替え日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
        "",
        "# 日次統合レポート配信（アイコン修正完成版）",
        f"0 7 * * * cd {current_dir} && python3 {icon_fixed_file} > /tmp/hanazono_morning.log 2>&1",
        f"0 19 * * * cd {current_dir} && python3 {icon_fixed_file} > /tmp/hanazono_evening.log 2>&1",
        "",
        "# 週次システム状況レポート（日曜21:00）",
        f"0 21 * * 0 cd {current_dir} && python3 -c \"import datetime; import subprocess; import glob; print('🗓️ 週次システム状況レポート', datetime.datetime.now().strftime('%Y年%m月%d日')); logs = glob.glob('/tmp/hanazono_*.log'); print(f'📊 ログファイル: {{len(logs)}}個'); [print(f'✅ {{log}}: 正常') if 'メール送信成功' in open(log, 'r').read() else print(f'⚠️ {{log}}: 要確認') for log in logs[-7:] if os.path.exists(log)]; print('週次確認完了')\" > /tmp/hanazono_weekly.log 2>&1",
        "",
        "# 月次システムメンテナンス（月初8:00）",
        f"0 8 1 * * cd {current_dir} && python3 -c \"import datetime; import os; import glob; print('🔧 月次システムメンテナンス', datetime.datetime.now().strftime('%Y年%m月')); logs = glob.glob('/tmp/hanazono_*.log'); old_logs = [log for log in logs if os.path.getctime(log) < (datetime.datetime.now() - datetime.timedelta(days=30)).timestamp()]; [os.remove(log) for log in old_logs if os.path.exists(log)]; print(f'📊 ログ整理完了: {{len(old_logs)}}ファイル削除'); print('月次メンテナンス完了')\" > /tmp/hanazono_monthly.log 2>&1",
        "",
        "# エラー監視・通知（毎時15分）",
        f"15 * * * * cd {current_dir} && python3 -c \"import glob; import datetime; logs = glob.glob('/tmp/hanazono_*.log'); error_logs = [log for log in logs if '❌' in open(log, 'r').read() or 'エラー' in open(log, 'r').read() if os.path.exists(log)]; print(f'⚠️ エラー検知: {{len(error_logs)}}ファイル') if error_logs else print('✅ システム正常')\" > /tmp/hanazono_monitor.log 2>&1",
        ""
    ]
    
    # 3. 既存の非HANAZONO設定保持
    existing_lines = []
    if current_crontab.strip():
        for line in current_crontab.split('\n'):
            if 'HANAZONO' not in line and line.strip():
                existing_lines.append(line)
    
    # 4. 新しいcrontab内容作成
    final_crontab = existing_lines + new_cron_jobs
    
    # 5. 一時ファイルに保存
    temp_crontab_file = f"temp_icon_fixed_crontab_{timestamp}.txt"
    with open(temp_crontab_file, 'w') as f:
        f.write('\n'.join(final_crontab))
    
    print(f"📋 アイコン修正版cron設定準備完了")
    print(f"✅ 使用ファイル: {icon_fixed_file}")
    print(f"📊 crontab行数: {len(final_crontab)}行")
    
    # 6. crontab適用
    try:
        result = subprocess.run(['crontab', temp_crontab_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ アイコン修正版cron適用成功")
            
            # 適用確認
            verify_result = subprocess.run(['crontab', '-l'], 
                                         capture_output=True, text=True)
            if verify_result.returncode == 0 and icon_fixed_file in verify_result.stdout:
                print("✅ アイコン修正版cron適用確認済み")
                print(f"🎨 次回配信: 🟠🔵🟣🌻 アイコン対応版")
                
                # 一時ファイル削除
                os.remove(temp_crontab_file)
                
                print(f"\n🎉 切り替え完了！")
                print(f"📧 明日朝7時: アイコン修正完成版メール配信")
                print(f"🎨 絵文字: 🟠🔵🟣🌻 天気・季節別自動切り替え")
                print(f"🌤️ 天気: 3日分完璧データ + 絵文字レイアウト")
                print(f"📊 発電予測: 高い/中程度/低い 表示")
                
                return True
            else:
                print("❌ アイコン修正版cron適用確認失敗")
                return False
        else:
            print(f"❌ アイコン修正版cron適用失敗: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ cron適用エラー: {e}")
        return False
    
    print(f"\n🔄 復旧方法（問題発生時）:")
    print(f"crontab {backup_file}")

if __name__ == "__main__":
    switch_to_icon_fixed_cron()
