#!/usr/bin/env python3
"""
Integrated Safety Assessment and Monitoring System
目的: 自動化スクリプト安全性評価 + 競合検知アラートシステム統合
機能: 段階的復旧 + リアルタイム監視 + 予防的アラート
作成: 一時使用目的（評価完了後削除）
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

class IntegratedSystemMonitor:
    """統合システム監視・アラート機能"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.alerts = []
        self.conflicts = []
        self.safety_report = {}
        
    def load_disabled_scripts(self):
        """無効化された自動化スクリプト一覧取得"""
        try:
            with open("automation_emergency_control.json", "r") as f:
                control_data = json.load(f)
                return control_data.get("disabled_scripts", [])
        except FileNotFoundError:
            print("⚠️ automation_emergency_control.json が見つかりません")
            return []
    
    def analyze_script_safety(self, filepath, content):
        """スクリプト安全性分析（競合検知機能付き）"""
        safety_score = 100
        issues = []
        conflict_risks = []
        
        # 危険操作パターン
        high_risk_patterns = {
            r'rm\s+-rf\s+(?![\$"])': -50,  # rm -rf (変数以外)
            r'pkill\s+-9': -30,
            r'while\s+true.*:': -25,
            r'sudo\s+': -20,
            r'exec\s*\(': -30,
            r'eval\s*\(': -30
        }
        
        # 競合リスクパターン
        conflict_patterns = {
            r'venv.*activate': "venv環境競合リスク",
            r'pip\s+install': "パッケージ競合リスク", 
            r'crontab\s+-[el]': "cron競合リスク",
            r'systemctl.*start': "サービス競合リスク",
            r'git\s+': "Git操作競合リスク",
            r'collector.*\.py': "データ収集競合リスク",
            r'email.*send': "メール送信競合リスク"
        }
        
        import re
        
        # 危険操作検出
        for pattern, score_change in high_risk_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                safety_score += score_change
                issues.append(f"危険操作: {pattern}")
        
        # 競合リスク検出
        for pattern, risk_desc in conflict_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                conflict_risks.append(risk_desc)
        
        # 機能推測
        purpose = self._guess_script_purpose(filepath, content)
        
        return {
            "safety_score": max(0, min(100, safety_score)),
            "risk_level": self._calculate_risk_level(safety_score),
            "purpose": purpose,
            "issues": issues,
            "conflict_risks": conflict_risks,
            "file_size": len(content),
            "complexity": len(content.splitlines())
        }
    
    def _guess_script_purpose(self, filepath, content):
        """スクリプト目的推測"""
        filepath_lower = filepath.lower()
        content_lower = content.lower()
        
        if "git" in filepath_lower or "git" in content_lower:
            return "Git操作・バックアップ"
        elif "cron" in filepath_lower or "cron" in content_lower:
            return "Cron管理・スケジュール"
        elif "backup" in filepath_lower or "backup" in content_lower:
            return "バックアップ・保存"
        elif "fix" in filepath_lower or "fix" in content_lower:
            return "システム修復・メンテナンス"
        elif "auto" in filepath_lower:
            return "汎用自動化処理"
        elif "evolution" in filepath_lower or "ultimate" in filepath_lower:
            return "高度自動化・進化系"
        else:
            return "汎用スクリプト"
    
    def _calculate_risk_level(self, safety_score):
        """リスクレベル算出"""
        if safety_score >= 80:
            return "低リスク"
        elif safety_score >= 60:
            return "中リスク"
        elif safety_score >= 40:
            return "高リスク"
        else:
            return "危険"
    
    def detect_system_conflicts(self):
        """システム競合検知"""
        print("🔍 システム競合検知実行中...")
        
        conflicts = []
        
        # 1. 重複プロセス検知
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
            process_lines = result.stdout.splitlines()
            
            python_processes = [line for line in process_lines if 'python' in line]
            if len(python_processes) > 10:
                conflicts.append({
                    "type": "プロセス過多",
                    "severity": "中",
                    "detail": f"Python プロセス {len(python_processes)}個実行中"
                })
        except:
            pass
        
        # 2. cron重複ジョブ検知
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                cron_lines = [line for line in result.stdout.splitlines() 
                             if line.strip() and not line.startswith('#')]
                
                # 同じスクリプトの重複実行検知
                script_counts = {}
                for line in cron_lines:
                    if '.py' in line:
                        script_name = line.split('.py')[0].split()[-1] + '.py'
                        script_counts[script_name] = script_counts.get(script_name, 0) + 1
                
                for script, count in script_counts.items():
                    if count > 1:
                        conflicts.append({
                            "type": "cron重複",
                            "severity": "高",
                            "detail": f"{script} が {count}回 cron登録"
                        })
        except:
            pass
        
        # 3. ポート競合検知
        common_ports = [587, 25, 80, 443, 22]
        for port in common_ports:
            try:
                result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=5)
                if f":{port}" in result.stdout:
                    port_count = result.stdout.count(f":{port}")
                    if port_count > 2:
                        conflicts.append({
                            "type": "ポート競合疑い",
                            "severity": "中", 
                            "detail": f"ポート {port} で {port_count}個の接続"
                        })
            except:
                pass
        
        return conflicts
    
    def generate_recovery_priority(self, safety_analyses):
        """復旧優先度生成"""
        print("📊 復旧優先度算出中...")
        
        # 優先度キーワード
        high_priority_keywords = ["backup", "git", "save", "monitor"]
        medium_priority_keywords = ["cron", "fix", "system", "auto"]
        low_priority_keywords = ["evolution", "ultimate", "enhanced", "master"]
        
        prioritized_scripts = []
        
        for script_path, analysis in safety_analyses.items():
            priority_score = analysis["safety_score"]
            
            # キーワードボーナス
            script_lower = script_path.lower()
            if any(kw in script_lower for kw in high_priority_keywords):
                priority_score += 20
            elif any(kw in script_lower for kw in medium_priority_keywords):
                priority_score += 10
            elif any(kw in script_lower for kw in low_priority_keywords):
                priority_score -= 10
            
            # 競合リスクペナルティ
            priority_score -= len(analysis["conflict_risks"]) * 5
            
            prioritized_scripts.append({
                "script": script_path,
                "priority_score": priority_score,
                "safety_score": analysis["safety_score"],
                "risk_level": analysis["risk_level"],
                "purpose": analysis["purpose"],
                "conflict_risks": analysis["conflict_risks"]
            })
        
        # ソート
        prioritized_scripts.sort(key=lambda x: x["priority_score"], reverse=True)
        return prioritized_scripts
    
    def generate_alert_report(self, conflicts, safety_analyses, prioritized_scripts):
        """統合アラートレポート生成"""
        alert_report = {
            "timestamp": datetime.now().isoformat(),
            "system_health": "良好" if len(conflicts) < 3 else "注意" if len(conflicts) < 6 else "警告",
            "total_conflicts": len(conflicts),
            "conflicts": conflicts,
            "script_analysis": {
                "total_scripts": len(safety_analyses),
                "safe_scripts": len([s for s in safety_analyses.values() if s["safety_score"] >= 80]),
                "risky_scripts": len([s for s in safety_analyses.values() if s["safety_score"] < 60])
            },
            "immediate_actions": [],
            "recovery_recommendations": prioritized_scripts[:5]  # トップ5
        }
        
        # 即座対応が必要なアクション生成
        if conflicts:
            for conflict in conflicts:
                if conflict["severity"] == "高":
                    alert_report["immediate_actions"].append(f"緊急: {conflict['detail']}")
        
        if alert_report["script_analysis"]["risky_scripts"] > 5:
            alert_report["immediate_actions"].append("危険スクリプト5個以上 - 復旧前詳細確認必要")
        
        return alert_report
    
    def run_integrated_assessment(self):
        """統合評価実行"""
        print("🔍 統合システム評価・監視実行")
        print(f"実行時刻: {datetime.now()}")
        
        print_section("Phase 1: 無効化スクリプト安全性分析")
        
        disabled_scripts = self.load_disabled_scripts()
        safety_analyses = {}
        
        if disabled_scripts:
            print(f"📋 分析対象: {len(disabled_scripts)}個のスクリプト")
            
            for script_info in disabled_scripts:
                disabled_path = script_info["disabled"]
                original_path = script_info["original"]
                
                if os.path.exists(disabled_path):
                    try:
                        with open(disabled_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        analysis = self.analyze_script_safety(original_path, content)
                        safety_analyses[original_path] = analysis
                        
                        print(f"✅ {original_path}: {analysis['risk_level']} (安全度{analysis['safety_score']}/100)")
                        if analysis['conflict_risks']:
                            print(f"   ⚠️ 競合リスク: {', '.join(analysis['conflict_risks'])}")
                        
                    except Exception as e:
                        print(f"❌ {original_path}: 分析エラー - {e}")
        
        print_section("Phase 2: システム競合検知")
        
        conflicts = self.detect_system_conflicts()
        if conflicts:
            print(f"🚨 検知された競合: {len(conflicts)}件")
            for conflict in conflicts:
                print(f"   {conflict['severity']}: {conflict['detail']}")
        else:
            print("✅ システム競合なし")
        
        print_section("Phase 3: 復旧優先度算出")
        
        prioritized_scripts = self.generate_recovery_priority(safety_analyses)
        
        print("🎯 復旧推奨順序 (トップ5):")
        for i, script in enumerate(prioritized_scripts[:5], 1):
            print(f"{i}. {script['script']}")
            print(f"   優先度: {script['priority_score']}/100, 安全度: {script['safety_score']}/100")
            print(f"   目的: {script['purpose']}, リスク: {script['risk_level']}")
            if script['conflict_risks']:
                print(f"   競合注意: {', '.join(script['conflict_risks'])}")
        
        print_section("Phase 4: 統合アラートレポート生成")
        
        alert_report = self.generate_alert_report(conflicts, safety_analyses, prioritized_scripts)
        
        # レポート保存
        report_filename = f"integrated_system_report_{self.timestamp}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(alert_report, f, indent=2, ensure_ascii=False)
        
        print_section("🎯 統合評価結果")
        
        print(f"📊 システム健全性: {alert_report['system_health']}")
        print(f"🔧 競合件数: {alert_report['total_conflicts']}")
        print(f"✅ 安全スクリプト: {alert_report['script_analysis']['safe_scripts']}個")
        print(f"⚠️ 危険スクリプト: {alert_report['script_analysis']['risky_scripts']}個")
        
        if alert_report["immediate_actions"]:
            print(f"\n🚨 即座対応必要:")
            for action in alert_report["immediate_actions"]:
                print(f"   - {action}")
        
        print(f"\n📄 詳細レポート: {report_filename}")
        
        print(f"\n📋 推奨次ステップ:")
        print("1. トップ5スクリプトから段階的復旧開始")
        print("2. 競合リスクの事前確認")
        print("3. 復旧後のシステム監視継続")
        
        return alert_report

def main():
    monitor = IntegratedSystemMonitor()
    report = monitor.run_integrated_assessment()
    
    print(f"\n🎉 統合システム評価・監視完了")
    print(f"⚡ 次フェーズ: 安全確認済みスクリプトの段階的復旧")

if __name__ == "__main__":
    main()
