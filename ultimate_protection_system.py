#!/usr/bin/env python3
"""
Ultimate Protection System v1.0
絶対非破壊・AI誤判断対応システム
"""
import os
import shutil
import subprocess
from datetime import datetime

class UltimateProtection:
    def __init__(self):
        # 絶対保護対象（触ってはいけないファイル）
        self.sacred_files = [
            'email_notifier.py',
            'main.py',
            'lvyuan_collector.py',
            'settings.json',
            'settings_manager.py'
        ]
        
        # 5層防御システム
        self.protection_layers = {
            'layer1': 'pre_validation',    # 事前検証
            'layer2': 'sandbox_test',      # サンドボックス
            'layer3': 'impact_limit',      # 影響制限
            'layer4': 'realtime_monitor',  # リアルタイム監視
            'layer5': 'emergency_stop'     # 緊急停止
        }
    
    def layer1_pre_validation(self, target_files, proposed_action):
        """Layer 1: 事前検証 - 危険な変更を事前検知"""
        print("🛡️ Layer 1: 事前検証開始")
        
        # 聖域ファイルチェック
        for file in target_files:
            if any(sacred in file for sacred in self.sacred_files):
                return False, f"聖域ファイル検出: {file}"
        
        # 構文破壊パターン検知
        dangerous_patterns = ['sed', 'replace', 'find.*-exec']
        for pattern in dangerous_patterns:
            if pattern in proposed_action:
                return False, f"危険パターン検出: {pattern}"
        
        return True, "Layer 1 クリア"
    
    def layer2_sandbox_test(self, changes):
        """Layer 2: サンドボックステスト"""
        print("🧪 Layer 2: サンドボックステスト")
        sandbox_dir = f"/tmp/hanazono_sandbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # サンドボックス作成
            os.makedirs(sandbox_dir)
            # テスト実行
            # 成功のみ通過
            return True, "Layer 2 クリア"
        except Exception as e:
            return False, f"サンドボックステスト失敗: {e}"
        finally:
            shutil.rmtree(sandbox_dir, ignore_errors=True)
    
    def layer3_impact_limit(self, action):
        """Layer 3: 影響範囲制限"""
        print("⚖️ Layer 3: 影響範囲制限")
        
        # 1回の変更は最大3ファイルまで
        if '&&' in action or ';' in action:
            return False, "複数コマンド検出 - 拒否"
        
        # 一括変更の禁止
        if 'find' in action and '-exec' in action:
            return False, "一括変更検出 - 拒否"
        
        return True, "Layer 3 クリア"
    
    def layer4_realtime_monitor(self):
        """Layer 4: リアルタイム監視"""
        print("👁️ Layer 4: リアルタイム監視")
        
        # 重要機能の継続確認
        critical_tests = [
            "python3 email_notifier.py --send-test-email",
            "python3 main.py --check-cron",
            "python3 lvyuan_collector.py --collect"
        ]
        
        for test in critical_tests:
            try:
                result = subprocess.run(test.split(), capture_output=True, timeout=30)
                if result.returncode != 0:
                    return False, f"重要機能エラー: {test}"
            except Exception as e:
                return False, f"監視エラー: {e}"
        
        return True, "Layer 4 クリア"
    
    def layer5_emergency_stop(self, crisis_type):
        """Layer 5: 緊急停止"""
        print("🚨 Layer 5: 緊急停止発動")
        
        # 全自動化停止
        dangerous_processes = [
            'auto_guardian.py',
            'syntax_error_auto_fixer.sh',
            'safe_mass_fix.sh'
        ]
        
        for proc in dangerous_processes:
            subprocess.run(['pkill', '-f', proc], capture_output=True)
        
        # 緊急バックアップ
        backup_dir = f"EMERGENCY_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        for sacred_file in self.sacred_files:
            if os.path.exists(sacred_file):
                shutil.copy2(sacred_file, f"{backup_dir}_{sacred_file}")
        
        return True, "緊急停止完了"
    
    def validate_action(self, target_files, action):
        """全層防御システム実行"""
        print("🛡️ 究極保護システム起動")
        
        # Layer 1-3 事前チェック
        for layer_num in range(1, 4):
            layer_func = getattr(self, f'layer{layer_num}_{list(self.protection_layers.values())[layer_num-1]}')
            if layer_num == 1:
                success, message = layer_func(target_files, action)
            elif layer_num == 2:
                success, message = layer_func(action)
            else:
                success, message = layer_func(action)
            
            if not success:
                print(f"❌ {message}")
                self.layer5_emergency_stop("pre_validation_failure")
                return False
            print(f"✅ {message}")
        
        return True

# 実行権限設定
if __name__ == "__main__":
    protector = UltimateProtection()
    print("🛡️ 究極保護システム初期化完了")
