#!/usr/bin/env python3
"""
AI自動問題解決システム v2.0（改良版）
より安全で確実な修正・テスト・復旧機能
"""
import os
import subprocess
import shutil
from datetime import datetime

class AIAutoResolverV2:
    def __init__(self):
        self.base_dir = "/home/pi/lvyuan_solar_control"
        self.backup_dir = f"{self.base_dir}/ai_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def solve_email_battery_issue(self):
        """メールバッテリー情報問題の完全自動解決（改良版）"""
        print("🤖 AI自動問題解決v2.0開始：メールバッテリー情報修正")
        
        # Step 1: 自動バックアップ
        backup_file = self._create_backup('enhanced_email_system_v2.py')
        print(f"💾 自動バックアップ: {backup_file}")
        
        try:
            # Step 2: 新しい修正された関数を追加
            if self._add_fixed_function():
                print("✅ 修正関数追加成功")
                
                # Step 3: 自動構文チェック
                if self._syntax_check('enhanced_email_system_v2.py'):
                    print("✅ 構文チェック成功")
                    
                    # Step 4: 自動テスト
                    if self._test_email_system():
                        print("✅ 完全自動解決成功！")
                        return True
                    else:
                        print("❌ テスト失敗")
                else:
                    print("❌ 構文エラー検出")
            else:
                print("❌ 修正関数追加失敗")
                
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
        
        # Step 5: 自動復旧
        print("🔄 自動復旧実行中...")
        self._restore_from_backup(backup_file)
        print("✅ 自動復旧完了")
        return False
    
    def _create_backup(self, filename):
        """自動バックアップ作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/{filename}.backup_{timestamp}"
        shutil.copy(f"{self.base_dir}/{filename}", backup_path)
        return backup_path
    
    def _add_fixed_function(self):
        """修正された関数を安全に追加"""
        try:
            file_path = f"{self.base_dir}/enhanced_email_system_v2.py"
            
            # 現在のファイルを読み込み
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # _extract_battery_info関数を探して置き換え
            new_lines = []
            in_function = False
            function_indent = 0
            
            for line in lines:
                if 'def _extract_battery_info(self, data):' in line:
                    # 関数開始 - 新しい関数に置き換え
                    in_function = True
                    function_indent = len(line) - len(line.lstrip())
                    
                    # 新しい関数を追加
                    new_lines.extend([
                        line,  # 関数定義行
                        ' ' * (function_indent + 4) + '"""バッテリー情報を抽出（report_data形式対応版）"""\n',
                        ' ' * (function_indent + 4) + 'try:\n',
                        ' ' * (function_indent + 8) + '# report_data形式の場合\n',
                        ' ' * (function_indent + 8) + 'if isinstance(data, dict) and "solar_data" in data:\n',
                        ' ' * (function_indent + 12) + 'solar_data = data["solar_data"]\n',
                        ' ' * (function_indent + 12) + 'if isinstance(solar_data, list) and len(solar_data) > 0:\n',
                        ' ' * (function_indent + 16) + 'actual_data = solar_data[0]\n',
                        ' ' * (function_indent + 12) + 'else:\n',
                        ' ' * (function_indent + 16) + 'actual_data = solar_data\n',
                        ' ' * (function_indent + 8) + 'elif isinstance(data, list) and len(data) > 0:\n',
                        ' ' * (function_indent + 12) + 'actual_data = data[0]\n',
                        ' ' * (function_indent + 8) + 'elif isinstance(data, dict):\n',
                        ' ' * (function_indent + 12) + 'actual_data = data\n',
                        ' ' * (function_indent + 8) + 'else:\n',
                        ' ' * (function_indent + 12) + 'return {"soc": "N/A", "voltage": "N/A", "current": "N/A"}\n',
                        ' ' * (function_indent + 8) + '\n',
                        ' ' * (function_indent + 8) + 'if isinstance(actual_data, dict) and "parameters" in actual_data:\n',
                        ' ' * (function_indent + 12) + 'params = actual_data["parameters"]\n',
                        ' ' * (function_indent + 12) + 'soc = "N/A"\n',
                        ' ' * (function_indent + 12) + 'voltage = "N/A"\n',
                        ' ' * (function_indent + 12) + 'current = "N/A"\n',
                        ' ' * (function_indent + 12) + '\n',
                        ' ' * (function_indent + 12) + 'if "0x0100" in params and isinstance(params["0x0100"], dict):\n',
                        ' ' * (function_indent + 16) + 'soc = params["0x0100"].get("value", "N/A")\n',
                        ' ' * (function_indent + 12) + 'if "0x0101" in params and isinstance(params["0x0101"], dict):\n',
                        ' ' * (function_indent + 16) + 'voltage_val = params["0x0101"].get("value", "N/A")\n',
                        ' ' * (function_indent + 16) + 'voltage = round(voltage_val, 1) if isinstance(voltage_val, (int, float)) else "N/A"\n',
                        ' ' * (function_indent + 12) + 'if "0x0102" in params and isinstance(params["0x0102"], dict):\n',
                        ' ' * (function_indent + 16) + 'current_val = params["0x0102"].get("value", "N/A")\n',
                        ' ' * (function_indent + 16) + 'current = round(current_val, 1) if isinstance(current_val, (int, float)) else "N/A"\n',
                        ' ' * (function_indent + 12) + '\n',
                        ' ' * (function_indent + 12) + 'return {"soc": soc, "voltage": voltage, "current": current}\n',
                        ' ' * (function_indent + 8) + 'else:\n',
                        ' ' * (function_indent + 12) + 'return {"soc": "N/A", "voltage": "N/A", "current": "N/A"}\n',
                        ' ' * (function_indent + 4) + 'except Exception as e:\n',
                        ' ' * (function_indent + 8) + 'return {"soc": "N/A", "voltage": "N/A", "current": "N/A"}\n'
                    ])
                    continue
                
                if in_function:
                    # 関数内部 - 次の関数定義まで飛ばす
                    if line.strip() and not line.startswith(' '):
                        # ファイル終端または新しいクラス/関数
                        in_function = False
                        new_lines.append(line)
                    elif line.strip().startswith('def ') and len(line) - len(line.lstrip()) <= function_indent:
                        # 同じまたは上位レベルの関数定義
                        in_function = False
                        new_lines.append(line)
                    # else: 関数内部なので飛ばす
                else:
                    new_lines.append(line)
            
            # ファイルに書き戻し
            with open(file_path, 'w') as f:
                f.writelines(new_lines)
            
            return True
        except Exception as e:
            print(f"関数追加エラー: {e}")
            return False
    
    def _syntax_check(self, filename):
        """自動構文チェック"""
        try:
            result = subprocess.run(['python3', '-m', 'py_compile', filename], 
                                  cwd=self.base_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"構文エラー詳細: {result.stderr}")
            return result.returncode == 0
        except Exception as e:
            print(f"構文チェックエラー: {e}")
            return False
    
    def _test_email_system(self):
        """メールシステム自動テスト"""
        try:
            result = subprocess.run(['python3', 'main.py', '--daily-report', '--debug'], 
                                  cwd=self.base_dir, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            
            # バッテリー情報が正常に抽出されているかチェック
            if "抽出されたバッテリー情報: {'soc': 'N/A'" in output:
                print("❌ バッテリー情報がN/Aのまま")
                return False
            elif "抽出されたバッテリー情報:" in output and "'soc':" in output:
                print("✅ バッテリー情報抽出成功を検出")
                return True
            else:
                print(f"⚠️ テスト結果が不明: {output[-200:]}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ テストタイムアウト")
            return False
        except Exception as e:
            print(f"テストエラー: {e}")
            return False
    
    def _restore_from_backup(self, backup_path):
        """自動復旧"""
        try:
            shutil.copy(backup_path, f"{self.base_dir}/enhanced_email_system_v2.py")
            print("✅ バックアップからの復旧完了")
            return True
        except Exception as e:
            print(f"復旧エラー: {e}")
            return False

if __name__ == "__main__":
    resolver = AIAutoResolverV2()
    resolver.solve_email_battery_issue()
