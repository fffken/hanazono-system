#!/usr/bin/env python3
"""
HANAZONO Parameter Manager v1.0
HANAZONO-SYSTEM-SETTINGS.md完全制御システム

設計思想: 全65パラメーターの安全な最適化・更新制御
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

class ParameterManager:
    """HANAZONO全パラメーター統合管理"""
    
    def __init__(self, core_engine):
        self.core = core_engine
        self.version = "1.0.0-HANAZONO-INTEGRATION"
        
        # HANAZONO設定ファイルパス
        self.hanazono_settings_path = "docs/HANAZONO-SYSTEM-SETTINGS.md"
        self.settings_backup_dir = Path("settings_backups")
        self.settings_backup_dir.mkdir(exist_ok=True)
        
        # パラメーター分類
        self.parameter_categories = {
            "primary": ["ID07", "ID10", "ID62"],  # 最重要（ML最適化対象）
            "secondary": ["ID41", "ID40", "ID42", "ID43"],  # 時間設定
            "advanced": ["ID28", "ID04", "ID05", "ID06"],  # 上級設定
            "monitoring": ["ID01", "ID02", "ID03"],  # 監視系
            "experimental": []  # 実験的最適化（将来拡張）
        }
        
        # 安全範囲定義
        self.safe_ranges = {
            "ID07": {"min": 25, "max": 70, "unit": "A", "name": "充電電流"},
            "ID10": {"min": 15, "max": 75, "unit": "分", "name": "充電時間"},
            "ID62": {"min": 25, "max": 70, "unit": "%", "name": "出力SOC"},
            "ID41": {"min": 0, "max": 23, "unit": "時", "name": "第1充電終了時間"},
            "ID40": {"min": 0, "max": 23, "unit": "時", "name": "第1充電開始時間"},
            "ID42": {"min": 0, "max": 23, "unit": "時", "name": "第2充電開始時間"},
            "ID43": {"min": 0, "max": 23, "unit": "時", "name": "第2充電終了時間"}
        }
        
        self._load_current_settings()
        
    def _load_current_settings(self):
        """現在のHANAZONO設定読み込み"""
        try:
            if Path(self.hanazono_settings_path).exists():
                with open(self.hanazono_settings_path, 'r', encoding='utf-8') as f:
                    self.hanazono_content = f.read()
                
                self.current_settings = self._parse_hanazono_settings()
                self.core.logger.info(f"HANAZONO設定読み込み成功: {len(self.current_settings)}パラメーター")
            else:
                self.core.logger.warning("HANAZONO設定ファイルが見つかりません")
                self.hanazono_content = ""
                self.current_settings = {}
                
        except Exception as e:
            self.core.logger.error(f"HANAZONO設定読み込みエラー: {e}")
            self.hanazono_content = ""
            self.current_settings = {}
    
    def _parse_hanazono_settings(self):
        """HANAZONO-SYSTEM-SETTINGS.mdパース"""
        try:
            settings = {}
            
            # 季節別設定表の抽出
            # タイプB設定表のパターン
            type_b_pattern = r'\|\s*(\w+季)\s*\|[^|]*\|\s*(\d+)分\s*\|\s*(\d+)A\s*\|\s*(\d+)%\s*\|'
            
            matches = re.findall(type_b_pattern, self.hanazono_content)
            for match in matches:
                season, charge_time, charge_current, output_soc = match
                settings[f"{season}_typeB"] = {
                    "ID07": int(charge_current),
                    "ID10": int(charge_time), 
                    "ID62": int(output_soc),
                    "season": season
                }
            
            # ML最適化設定の抽出
            ml_pattern = r'ML最適充電時間[^|]*\|\s*(\d+)分[^|]*ML最適充電電流[^|]*\|\s*(\d+)A[^|]*ML最適SOC設定[^|]*\|\s*(\d+)%'
            ml_matches = re.findall(ml_pattern, self.hanazono_content)
            
            if ml_matches:
                charge_time, charge_current, output_soc = ml_matches[0]
                settings["ML_current"] = {
                    "ID07": int(charge_current),
                    "ID10": int(charge_time),
                    "ID62": int(output_soc)
                }
            
            return settings
            
        except Exception as e:
            self.core.logger.error(f"HANAZONO設定パースエラー: {e}")
            return {}
    
    def update_hanazono_settings(self, optimized_params: Dict[str, Any]):
        """HANAZONO設定安全更新"""
        try:
            # 1. 現在設定のバックアップ
            backup_result = self._create_settings_backup()
            if not backup_result["success"]:
                return {"success": False, "error": "バックアップ失敗"}
            
            # 2. パラメーター検証
            validated_params = self._validate_parameters(optimized_params)
            if not validated_params["valid"]:
                return {"success": False, "error": f"パラメーター検証失敗: {validated_params['errors']}"}
            
            # 3. HANAZONO設定更新
            update_result = self._update_hanazono_content(validated_params["params"])
            if not update_result["success"]:
                return {"success": False, "error": f"設定更新失敗: {update_result['error']}"}
            
            # 4. 変更ログ記録
            self._log_settings_change(validated_params["params"], backup_result["backup_file"])
            
            self.core.logger.info(f"HANAZONO設定更新成功: {validated_params['params']}")
            
            return {
                "success": True,
                "updated_params": validated_params["params"],
                "backup_file": backup_result["backup_file"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.core.logger.error(f"HANAZONO設定更新エラー: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_settings_backup(self):
        """設定ファイルバックアップ作成"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"HANAZONO-SYSTEM-SETTINGS_backup_{timestamp}.md"
            backup_path = self.settings_backup_dir / backup_filename
            
            if Path(self.hanazono_settings_path).exists():
                # 元ファイルをバックアップディレクトリにコピー
                import shutil
                shutil.copy2(self.hanazono_settings_path, backup_path)
                
                self.core.logger.info(f"設定バックアップ作成: {backup_path}")
                return {"success": True, "backup_file": str(backup_path)}
            else:
                return {"success": False, "error": "元ファイルが存在しません"}
                
        except Exception as e:
            self.core.logger.error(f"バックアップ作成エラー: {e}")
            return {"success": False, "error": str(e)}
    
    def _validate_parameters(self, params: Dict[str, Any]):
        """パラメーター安全性検証"""
        try:
            validated = {}
            errors = []
            
            for param_id, value in params.items():
                if param_id in self.safe_ranges:
                    range_info = self.safe_ranges[param_id]
                    
                    # 数値変換
                    try:
                        numeric_value = int(value)
                    except (ValueError, TypeError):
                        errors.append(f"{param_id}: 数値変換失敗 ({value})")
                        continue
                    
                    # 範囲チェック
                    if range_info["min"] <= numeric_value <= range_info["max"]:
                        validated[param_id] = numeric_value
                    else:
                        # 範囲外の場合は安全値にクランプ
                        clamped_value = max(range_info["min"], min(range_info["max"], numeric_value))
                        validated[param_id] = clamped_value
                        self.core.logger.warning(f"{param_id}: 範囲外値を調整 {numeric_value} -> {clamped_value}")
                else:
                    # 未定義パラメーターは警告のみ
                    self.core.logger.warning(f"未定義パラメーター: {param_id} = {value}")
            
            return {
                "valid": len(errors) == 0,
                "params": validated,
                "errors": errors
            }
            
        except Exception as e:
            return {"valid": False, "params": {}, "errors": [str(e)]}
    
    def _update_hanazono_content(self, validated_params: Dict[str, int]):
        """HANAZONO設定ファイル内容更新"""
        try:
            updated_content = self.hanazono_content
            
            # ML最適化設定セクションの更新
            if "ID07" in validated_params and "ID10" in validated_params and "ID62" in validated_params:
                # ML設定テーブルのパターンマッチングと置換
                ml_table_pattern = r'(\|\s*春秋季\s*\|[^|]*\|\s*)(\d+)(分\s*\|\s*)(\d+)(A\s*\|\s*)(\d+)(%\s*\|[^|]*\|[^|]*\|)'
                
                def ml_replace(match):
                    return (match.group(1) + str(validated_params["ID10"]) + 
                           match.group(3) + str(validated_params["ID07"]) + 
                           match.group(5) + str(validated_params["ID62"]) + match.group(7))
                
                updated_content = re.sub(ml_table_pattern, ml_replace, updated_content)
            
            # 最終更新時刻の更新
            timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M')
            timestamp_pattern = r'(\*🤖 機械学習による動的更新システム 最終更新: )([^*]*)'
            updated_content = re.sub(timestamp_pattern, f'\\1{timestamp}', updated_content)
            
            # ファイル書き込み
            with open(self.hanazono_settings_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.core.logger.info("HANAZONO設定ファイル更新完了")
            return {"success": True}
            
        except Exception as e:
            self.core.logger.error(f"設定ファイル更新エラー: {e}")
            return {"success": False, "error": str(e)}
    
    def _log_settings_change(self, params: Dict[str, int], backup_file: str):
        """設定変更ログ記録"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "changed_parameters": params,
                "backup_file": backup_file,
                "change_source": "ML_optimization",
                "validation": "passed"
            }
            
            # 変更履歴ファイルに追記
            log_file = self.settings_backup_dir / "settings_change_history.json"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(log_entry)
            
            # 最新100件のみ保持
            if len(history) > 100:
                history = history[-100:]
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            self.core.logger.info(f"設定変更ログ記録完了")
            
        except Exception as e:
            self.core.logger.warning(f"設定変更ログ記録エラー: {e}")
    
    def get_current_optimization_settings(self):
        """現在の最適化設定取得"""
        try:
            primary_settings = {}
            
            for param_id in self.parameter_categories["primary"]:
                if param_id in self.current_settings.get("ML_current", {}):
                    primary_settings[param_id] = self.current_settings["ML_current"][param_id]
                else:
                    # フォールバック: 春秋季設定
                    spring_settings = self.current_settings.get("春秋季_typeB", {})
                    if param_id in spring_settings:
                        primary_settings[param_id] = spring_settings[param_id]
            
            return {
                "current_settings": primary_settings,
                "available_categories": list(self.parameter_categories.keys()),
                "total_parameters": sum(len(params) for params in self.parameter_categories.values())
            }
            
        except Exception as e:
            self.core.logger.error(f"現在設定取得エラー: {e}")
            return {"error": str(e)}
    
    def rollback_settings(self, backup_file: str):
        """設定ロールバック"""
        try:
            backup_path = Path(backup_file)
            if backup_path.exists():
                import shutil
                shutil.copy2(backup_path, self.hanazono_settings_path)
                
                self._load_current_settings()  # 設定再読み込み
                
                self.core.logger.info(f"設定ロールバック完了: {backup_file}")
                return {"success": True, "restored_from": backup_file}
            else:
                return {"success": False, "error": "バックアップファイルが見つかりません"}
                
        except Exception as e:
            self.core.logger.error(f"設定ロールバックエラー: {e}")
            return {"success": False, "error": str(e)}


def main():
    """Parameter Manager テスト"""
    print("🔧 HANAZONO Parameter Manager テスト")
    print("=" * 60)
    
    class TestCore:
        class logger:
            @staticmethod
            def info(msg): print(f"INFO: {msg}")
            @staticmethod
            def warning(msg): print(f"WARNING: {msg}")
            @staticmethod
            def error(msg): print(f"ERROR: {msg}")
    
    # Parameter Manager初期化
    pm = ParameterManager(TestCore())
    
    print("📋 現在の最適化設定:")
    current = pm.get_current_optimization_settings()
    print(f"  {current}")
    
    print("\n🔧 テスト用パラメーター更新:")
    test_params = {"ID07": 42, "ID10": 38, "ID62": 38}
    print(f"  テスト値: {test_params}")
    
    # 実際の更新はテストモードでスキップ
    print("  （実際の更新はスキップ - テストモード）")
    
    print("\n✅ Parameter Manager テスト完了")


if __name__ == "__main__":
    main()
