#!/usr/bin/env python3
import subprocess,json,time,os
class AIAutoDecision:
    def __init__(self):
        self.priority_matrix = {"corruption": 10, "missing": 8, "performance": 5}
    def detect_issues(self):
        issues = []
        try:
            result = subprocess.run(["python3", "auto_guardian.py"], capture_output=True)
            if result.returncode != 0: issues.append(("corruption", 10))
        except: issues.append(("system_error", 9))
        try:
            subprocess.run(["python3", "main.py", "--check-cron"], capture_output=True, timeout=10)
        except: issues.append(("hanazono_down", 10))
        return sorted(issues, key=lambda x: x[1], reverse=True)
    def auto_execute_fix(self, issue_type):
        fixes = {
            "corruption": "rm -rf venv && python3 -m venv venv && source venv/bin/activate && pip install pysolarmanv5 requests urllib3 matplotlib numpy pandas pytz python-dateutil",
            "system_error": "bash scripts/version_manager.sh restore",
            "hanazono_down": "systemctl restart hanazono-guardian"
        }
        if issue_type in fixes:
            print(f"🤖 AI自動判断: {issue_type} -> 自動修復実行")
            os.system(fixes[issue_type])
            return True
        return False
    def run_autonomous_mode(self):
        issues = self.detect_issues()
        for issue_type, priority in issues:
            if priority >= 8:
                self.auto_execute_fix(issue_type)
                break
        print("✅ AI自動判断完了")
if __name__ == "__main__": AIAutoDecision().run_autonomous_mode()
