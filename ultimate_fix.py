#!/usr/bin/env python3
"""
🔧 究極構文修復システム v2.0
全ての構文エラーパターンに対応
"""
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

class UltimateSyntaxFixer:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = f"ultimate_backup_{self.timestamp}"
        self.fixed_files = []
        self.error_files = []
        
        self.target_files = [
            'main.py', 'email_notifier.py', 'settings_manager.py',
            'lvyuan_collector.py', 'data_util.py', 'logger.py',
            'ai_memory/ai_startup_memory.py'
        ]
        
    def create_backup(self):
        """完全バックアップ作成"""
        print(f"💾 バックアップ作成: {self.backup_dir}")
        os.makedirs(self.backup_dir, exist_ok=True)
        
        for file_path in self.target_files:
            if os.path.exists(file_path):
                backup_path = os.path.join(self.backup_dir, file_path)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(file_path, backup_path)
                print(f"  ✅ {file_path}")
    
    def fix_content(self, content):
        """全構文エラーパターンの修復"""
        
        # 日本語句読点修復
        content = re.sub(r'、', ',', content)
        content = re.sub(r'。', '.', content)
        content = re.sub(r'：', ':', content)
        content = re.sub(r'（', '(', content)
        content = re.sub(r'）', ')', content)
        
        # 括弧不足修復
        content = re.sub(r'timedelta\(days=1$', 'timedelta(days=1)', content, flags=re.MULTILINE)
        content = re.sub(r'logging\.INFO$', 'logging.INFO)', content, flags=re.MULTILINE)
        content = re.sub(r'os\.chdir\(([^)]+)$', r'os.chdir(\1)', content, flags=re.MULTILINE)
        
        # docstring修復
        content = re.sub(r'bool: ([^,]+),([^\\n]+)', r'bool: \1, \2', content)
        
        # 辞書内包表記修復
        content = re.sub(r'\{k: ([^}]+) for k, v in ([^}]+)\.items\(\)\}', r'{k: \1) for k, v in \2.items()}', content)
        content = re.sub(r'return \{([^}]+) for ([^}]+)\}', r'return {\1) for \2}', content)
        
        # 一般的な括弧修復
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 行末の括弧不足を修復
            if line.strip().endswith('(') and not line.strip().endswith('()'):
                line = line + ')'
            elif '(' in line and line.count('(') > line.count(')'):
                missing_parens = line.count('(') - line.count(')')
                line = line + ')' * missing_parens
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def check_syntax(self, file_path):
        """構文チェック"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', file_path],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)
    
    def fix_file(self, file_path):
        """単一ファイル修復"""
        if not os.path.exists(file_path):
            print(f"⚠️ ファイル未発見: {file_path}")
            return False
            
        print(f"🔧 修復中: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ 読み込みエラー {file_path}: {e}")
            return False
        
        # 修復実行
        fixed_content = self.fix_content(original_content)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
        except Exception as e:
            print(f"❌ 書き込みエラー {file_path}: {e}")
            return False
        
        # 構文チェック
        is_valid, error_msg = self.check_syntax(file_path)
        if is_valid:
            print(f"✅ 修復成功: {file_path}")
            self.fixed_files.append(file_path)
            return True
        else:
            print(f"❌ 構文エラー残存 {file_path}")
            print(f"   {error_msg[:200]}")
            self.error_files.append(file_path)
            return False
    
    def run(self):
        """メイン処理"""
        print(f"🚀 究極構文修復開始: {datetime.now()}")
        
        self.create_backup()
        
        for file_path in self.target_files:
            self.fix_file(file_path)
        
        print(f"\n📊 修復結果:")
        print(f"  ✅ 成功: {len(self.fixed_files)}ファイル")
        print(f"  ❌ 失敗: {len(self.error_files)}ファイル")
        
        if self.fixed_files:
            print("  📝 修復成功:")
            for f in self.fixed_files:
                print(f"    - {f}")
        
        return len(self.error_files) == 0

if __name__ == "__main__":
    fixer = UltimateSyntaxFixer()
    success = fixer.run()
    
    if success:
        print("\n🎉 全ファイル修復成功！kioku動作準備完了")
    else:
        print("\n⚠️ 一部ファイルに問題残存")
    
    sys.exit(0 if success else 1)
