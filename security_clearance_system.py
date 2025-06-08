#!/usr/bin/env python3
"""
Security Clearance and Ticket System
目的: 全自動化スクリプトに対する身体検査・診断書・実行チケット発行システム
原則: 認証なしでは一切実行不可・完全トレーサビリティ
作成: 一時使用目的（システム構築後削除）
"""

import os
import json
import hashlib
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path

class SecurityClearanceSystem:
    """セキュリティクリアランス・チケットシステム"""
    
    def __init__(self):
        self.clearance_dir = Path("security_clearance")
        self.clearance_dir.mkdir(exist_ok=True)
        
        self.certificates_dir = self.clearance_dir / "certificates"
        self.tickets_dir = self.clearance_dir / "execution_tickets"
        self.quarantine_dir = self.clearance_dir / "quarantine"
        
        for dir_path in [self.certificates_dir, self.tickets_dir, self.quarantine_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # セキュリティレベル定義
        self.security_levels = {
            "GREEN": {"score_min": 90, "auto_approve": True, "ticket_duration": 30},
            "YELLOW": {"score_min": 70, "auto_approve": False, "ticket_duration": 7},
            "ORANGE": {"score_min": 50, "auto_approve": False, "ticket_duration": 1},
            "RED": {"score_min": 0, "auto_approve": False, "ticket_duration": 0}
        }
    
    def conduct_full_security_inspection(self, script_path):
        """完全セキュリティ身体検査"""
        print(f"🔍 セキュリティ身体検査開始: {script_path}")
        
        if not os.path.exists(script_path):
            return {"status": "FAILED", "reason": "ファイル不存在"}
        
        # ファイル内容読み込み
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {"status": "FAILED", "reason": f"読み込みエラー: {e}"}
        
        # 身体検査項目
        inspection_result = {
            "script_path": script_path,
            "inspection_timestamp": datetime.now().isoformat(),
            "file_hash": hashlib.sha256(content.encode()).hexdigest(),
            "file_size": len(content),
            "security_violations": [],
            "risk_factors": [],
            "safety_score": 100,
            "clearance_level": "GREEN"
        }
        
        # 危険操作パターン検査
        critical_violations = {
            r'rm\s+-rf\s+(?![\$"''`])': {"penalty": -50, "description": "危険なファイル削除"},
            r'sudo\s+rm': {"penalty": -60, "description": "管理者権限での削除"},
            r'format\s+': {"penalty": -70, "description": "フォーマット操作"},
            r'mkfs\.': {"penalty": -70, "description": "ファイルシステム作成"},
            r'dd\s+if=.*of=/dev/': {"penalty": -80, "description": "デバイス直接書き込み"},
            r'pkill\s+-9': {"penalty": -30, "description": "強制プロセス終了"},
            r'kill\s+-9': {"penalty": -25, "description": "強制プロセス終了"},
            r'while\s+true.*:.*(?!break)': {"penalty": -40, "description": "無限ループ"},
            r'exec\s*\([^)]*\)': {"penalty": -35, "description": "動的実行"},
            r'eval\s*\([^)]*\)': {"penalty": -35, "description": "動的評価"},
            r'subprocess\.call\s*\([^)]*shell\s*=\s*True': {"penalty": -25, "description": "シェル実行"}
        }
        
        # 中リスク操作パターン
        moderate_risks = {
            r'pip\s+install': {"penalty": -10, "description": "パッケージインストール"},
            r'apt\s+install': {"penalty": -15, "description": "システムパッケージインストール"},
            r'crontab\s+-[el]': {"penalty": -15, "description": "cron設定変更"},
            r'systemctl': {"penalty": -20, "description": "システムサービス操作"},
            r'chmod\s+[0-7]{3}': {"penalty": -10, "description": "ファイル権限変更"},
            r'wget\s+.*\|\s*bash': {"penalty": -30, "description": "ダウンロード即実行"},
            r'curl\s+.*\|\s*bash': {"penalty": -30, "description": "ダウンロード即実行"}
        }
        
        # 競合リスク要因
        conflict_risks = {
            r'venv.*activate': "venv環境競合",
            r'collector.*\.py': "データ収集競合",
            r'email.*send': "メール送信競合",
            r'git\s+': "Git操作競合"
        }
        
        # パターンマッチング実行
        for pattern, violation in critical_violations.items():
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                inspection_result["security_violations"].append({
                    "type": "CRITICAL",
                    "pattern": pattern,
                    "description": violation["description"],
                    "penalty": violation["penalty"]
                })
                inspection_result["safety_score"] += violation["penalty"]
        
        for pattern, risk in moderate_risks.items():
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                inspection_result["risk_factors"].append({
                    "type": "MODERATE",
                    "pattern": pattern,
                    "description": risk["description"],
                    "penalty": risk["penalty"]
                })
                inspection_result["safety_score"] += risk["penalty"]
        
        for pattern, risk_desc in conflict_risks.items():
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                inspection_result["risk_factors"].append({
                    "type": "CONFLICT",
                    "description": risk_desc
                })
        
        # 安全スコア調整
        inspection_result["safety_score"] = max(0, min(100, inspection_result["safety_score"]))
        
        # クリアランスレベル決定
        for level, criteria in self.security_levels.items():
            if inspection_result["safety_score"] >= criteria["score_min"]:
                inspection_result["clearance_level"] = level
                break
        
        return inspection_result
    
    def issue_security_certificate(self, inspection_result):
        """セキュリティ診断書発行"""
        script_name = Path(inspection_result["script_path"]).name
        cert_filename = f"cert_{script_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        cert_path = self.certificates_dir / cert_filename
        
        certificate = {
            "certificate_id": hashlib.md5(f"{script_name}{inspection_result['inspection_timestamp']}".encode()).hexdigest(),
            "script_path": inspection_result["script_path"],
            "script_hash": inspection_result["file_hash"],
            "inspection_timestamp": inspection_result["inspection_timestamp"],
            "inspector": "SecurityClearanceSystem v1.0",
            "clearance_level": inspection_result["clearance_level"],
            "safety_score": inspection_result["safety_score"],
            "violations_count": len(inspection_result["security_violations"]),
            "risk_factors_count": len(inspection_result["risk_factors"]),
            "certificate_status": "VALID",
            "expiry_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "detailed_inspection": inspection_result
        }
        
        # 診断書保存
        with open(cert_path, 'w', encoding='utf-8') as f:
            json.dump(certificate, f, indent=2, ensure_ascii=False)
        
        print(f"📋 セキュリティ診断書発行: {cert_filename}")
        return certificate
    
    def issue_execution_ticket(self, certificate):
        """実行チケット発行"""
        clearance_level = certificate["clearance_level"]
        criteria = self.security_levels[clearance_level]
        
        # 自動承認判定
        if not criteria["auto_approve"]:
            print(f"🚨 {clearance_level}レベル: 手動承認が必要です")
            approval = input(f"実行を承認しますか？ (yes/no): ")
            if approval.lower() != 'yes':
                print("❌ 実行チケット発行拒否")
                return None
        
        # チケット生成
        script_name = Path(certificate["script_path"]).name
        ticket_id = hashlib.sha256(f"{certificate['certificate_id']}{datetime.now()}".encode()).hexdigest()[:16]
        
        ticket = {
            "ticket_id": ticket_id,
            "certificate_id": certificate["certificate_id"],
            "script_path": certificate["script_path"],
            "script_hash": certificate["script_hash"],
            "clearance_level": clearance_level,
            "issue_timestamp": datetime.now().isoformat(),
            "expiry_timestamp": (datetime.now() + timedelta(days=criteria["ticket_duration"])).isoformat(),
            "execution_count": 0,
            "max_executions": 10 if clearance_level == "GREEN" else 3 if clearance_level == "YELLOW" else 1,
            "ticket_status": "ACTIVE"
        }
        
        # チケット保存
        ticket_filename = f"ticket_{script_name}_{ticket_id}.json"
        ticket_path = self.tickets_dir / ticket_filename
        
        with open(ticket_path, 'w', encoding='utf-8') as f:
            json.dump(ticket, f, indent=2, ensure_ascii=False)
        
        print(f"🎫 実行チケット発行: {ticket_filename}")
        print(f"   レベル: {clearance_level}")
        print(f"   有効期限: {criteria['ticket_duration']}日")
        print(f"   最大実行回数: {ticket['max_executions']}回")
        
        return ticket
    
    def create_security_wrapper(self, script_path, ticket):
        """セキュリティラッパー作成"""
        script_name = Path(script_path).stem
        wrapper_name = f"{script_name}_secured.py"
        
        wrapper_code = f'''#!/usr/bin/env python3
"""
Security Wrapper for {script_path}
自動生成セキュリティラッパー - 直接実行禁止
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path

def verify_ticket():
    """チケット検証"""
    ticket_file = Path("security_clearance/execution_tickets/ticket_{script_name}_{ticket['ticket_id']}.json")
    
    if not ticket_file.exists():
        print("❌ 実行チケットが見つかりません")
        return False
    
    with open(ticket_file, 'r') as f:
        ticket_data = json.load(f)
    
    # 有効期限確認
    expiry = datetime.fromisoformat(ticket_data['expiry_timestamp'])
    if datetime.now() > expiry:
        print("❌ 実行チケットが期限切れです")
        return False
    
    # 実行回数確認
    if ticket_data['execution_count'] >= ticket_data['max_executions']:
        print("❌ 実行回数上限に達しています")
        return False
    
    # スクリプト整合性確認
    with open("{script_path}", 'r') as f:
        current_hash = hashlib.sha256(f.read().encode()).hexdigest()
    
    if current_hash != ticket_data['script_hash']:
        print("❌ スクリプトが変更されています。再検査が必要です")
        return False
    
    # 実行回数更新
    ticket_data['execution_count'] += 1
    with open(ticket_file, 'w') as f:
        json.dump(ticket_data, f, indent=2)
    
    print(f"✅ セキュリティチケット検証成功 (残り{{ticket_data['max_executions'] - ticket_data['execution_count']}}回)")
    return True

def main():
    """メイン実行（セキュリティチェック後）"""
    if not verify_ticket():
        exit(1)
    
    print(f"🔐 セキュアモードで {{script_path}} を実行")
    
    # 元スクリプト実行
    import subprocess
    result = subprocess.run(['python3', '{script_path}'], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"エラー: {{result.stderr}}")
    
    return result.returncode

if __name__ == "__main__":
    exit(main())
'''
        
        with open(wrapper_name, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
        
        os.chmod(wrapper_name, 0o755)
        
        print(f"🔐 セキュリティラッパー作成: {wrapper_name}")
        return wrapper_name
    
    def process_script(self, script_path):
        """スクリプトの完全セキュリティ処理"""
        print(f"\n🛡️ セキュリティ処理開始: {script_path}")
        
        # 1. 身体検査
        inspection = self.conduct_full_security_inspection(script_path)
        if inspection.get("status") == "FAILED":
            print(f"❌ 身体検査失敗: {inspection['reason']}")
            return None
        
        # 2. 診断書発行
        certificate = self.issue_security_certificate(inspection)
        
        # 3. セキュリティレベル表示
        print(f"📊 セキュリティ評価:")
        print(f"   安全スコア: {inspection['safety_score']}/100")
        print(f"   クリアランスレベル: {inspection['clearance_level']}")
        print(f"   重大違反: {len(inspection['security_violations'])}件")
        print(f"   リスク要因: {len(inspection['risk_factors'])}件")
        
        # 4. 詳細表示
        if inspection['security_violations']:
            print(f"🚨 セキュリティ違反:")
            for violation in inspection['security_violations']:
                print(f"   - {violation['description']} (ペナルティ: {violation['penalty']})")
        
        if inspection['risk_factors']:
            print(f"⚠️ リスク要因:")
            for risk in inspection['risk_factors']:
                print(f"   - {risk['description']}")
        
        # 5. 実行チケット発行判定
        if inspection['clearance_level'] == 'RED':
            print(f"🚫 REDレベル: 実行禁止")
            # 隔離エリアに移動
            quarantine_path = self.quarantine_dir / Path(script_path).name
            os.rename(script_path, quarantine_path)
            print(f"🔒 隔離完了: {quarantine_path}")
            return None
        
        # 6. チケット発行
        ticket = self.issue_execution_ticket(certificate)
        if not ticket:
            return None
        
        # 7. セキュリティラッパー作成
        wrapper = self.create_security_wrapper(script_path, ticket)
        
        print(f"✅ セキュリティ処理完了")
        print(f"🎫 実行方法: python3 {wrapper}")
        
        return {
            "certificate": certificate,
            "ticket": ticket,
            "wrapper": wrapper
        }

def main():
    """メインセキュリティ処理"""
    print("🛡️ セキュリティクリアランス・チケットシステム")
    print("=" * 60)
    
    system = SecurityClearanceSystem()
    
    # 復旧済みスクリプトの処理
    scripts_to_process = [
        "auto_code_fixes.py",
        "scripts/auto_evolution_controller.sh"
    ]
    
    for script in scripts_to_process:
        if os.path.exists(script):
            result = system.process_script(script)
            if result:
                print(f"🎉 {script}: セキュリティクリアランス取得")
            else:
                print(f"❌ {script}: セキュリティクリアランス失敗")
        else:
            print(f"⚠️ {script}: ファイルが見つかりません")
    
    print(f"\n📁 セキュリティファイル:")
    print(f"   診断書: security_clearance/certificates/")
    print(f"   実行チケット: security_clearance/execution_tickets/")
    print(f"   隔離エリア: security_clearance/quarantine/")

if __name__ == "__main__":
    main()
