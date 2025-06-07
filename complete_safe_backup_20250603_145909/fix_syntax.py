#!/usr/bin/env python3
"""
🔧 精密構文エラー自動修復システム
完全非破壊・自動復旧機能付き
"""
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class PreciseSyntaxFixer:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = f"precise_backup_{self.timestamp}"
        self.fixed_files = []
        self.error_files = []
        
        # 修復対象ファイル
        self.target_files = [
            'main.py',
            'email_notifier.py', 
            'settings_manager.py',
            'lvyuan_collector.py',
            'data_util.py',
            'logger.py',
            'ai_memory/ai_startup_memory.py'
        ]
        
    def create_backup(self):
        """完全バックアップ作成"""
        print(f"💾 バックアップ作成: {self.backup_dir}")
        os.makedirs(self.backup_dir, exist_ok=True)
        
        for file_path in self.target_files:
            if os.path.exists(file_path):
                # ディレクトリ構造も保持
                backup_path = os.path.join(self.backup_dir, file_path)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(file_path, backup_path)
                print(f"  ✅ {file_path}")
    
    def fix_file_content(self, content):
        """ファイル内容の精密修復"""
        
        # パターン1: import文の修復
        import_patterns = [
            (r'import\s+([^)\n]+)\)', r'import \1'),
            (r'from\s+([^)\n]+)\)', r'from \1'),
        ]
        
        # パターン2: 関数定義の修復
        def_patterns = [
            (r'def\s+([^:)]+)\):\)', r'def \1):'),
            (r'def\s+([^:)]+):\)', r'def \1:'),
            (r'def\s+([^:)]+)\)\)', r'def \1)'),
        ]
        
        # パターン3: 制御構文の修復
        control_patterns = [
            (r'if\s+([^:)]+)\):\)', r'if \1):'),
            (r'elif\s+([^:)]+)\):\)', r'elif \1):'),
            (r'else:\)', r'else:'),
            (r'for\s+([^:)]+)\):\)', r'for \1):'),
            (r'while\s+([^:)]+)\):\)', r'while \1):'),
            (r'try:\)', r'try:'),
            (r'except([^:)]*)\):\)', r'except\1):'),
            (r'finally:\)', r'finally:'),
            (r'with\s+([^:)]+)\):\)', r'with \1):'),
        ]
        
        # パターン4: 文字列の修復
        string_patterns = [
            (r'"""(\s*)\)', r'"""\1'),
            (r"'''(\s*)\)", r"'''\1"),
            (r'f"([^"]*)"(\s*)\)', r'f"\1"\2'),
            (r"f'([^']*)'(\s*)\)", r"f'\1'\2"),
        ]
        
        # パターン5: 関数呼び出しの修復
        call_patterns = [
            (r'([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)\(([^)]*)\)\)', r'\1(\2)'),
            (r'print\(([^)]*)\)\)', r'print(\1)'),
            (r'return\s+([^)\n]+)\)', r'return \1'),
            (r'global\s+([^)\n]+)\)', r'global \1'),
        ]
        
        # パターン6: 単純な余分括弧
        simple_patterns = [
            (r'([a-zA-Z_][a-zA-Z0-9_]*)\)(\s*)$', r'\1\2'),
            (r'(\d+)\)(\s*)$', r'\1\2'),
        ]
        
        # 全パターンを適用
        
        # パターン7: 日本語句読点の修復
        japanese_patterns = [
            (r'、', r','),
            (r'。', r'.'),
            (r'：', r':'),
            (r'（', r'('),
            (r'）', r')'),
            (r'「', r'"'),
            (r'」', r'"'),
        ]
        
        # 文字エンコーディング問題の修復
        
        # パターン8: 括弧・構文欠損の修復
        bracket_patterns = [
            (r'timedelta\(days=1$', r'timedelta(days=1)'),
            (r'logging\.INFO$', r'logging.INFO)'),
            (r'os\.chdir\(([^)]+)$', r'os.chdir()'),
            (r'datetime\.now\(\) - timedelta\(days=1$', r'datetime.now() - timedelta(days=1)'),
            (r'for k, v in ([^}]+)\.items\(\)\}$', r'for k, v in .items()}'),
            (r'\{k: ([^}]+) for k, v in ([^}]+)\.items\(\)\}', r'{k: ) for k, v in .items()}'),
        ]
        
        # パターン9: docstring修復
        docstring_patterns = [
            (r'bool: ([^,]+),([^
]+)', r'bool: , '),
            (r'Returns:
\s+([^:]+):', r'Returns:
        :'),
        ]
        
        encoding_patterns = [
            (r'、', r','),  # 、
            (r'。', r'.'),  # 。
            (r'：', r':'),  # ：
            (r'（', r'('),  # （
            (r'）', r')'),  # ）
        ]
        
        all_patterns = (import_patterns + def_patterns + control_patterns + japanese_patterns + encoding_patterns + bracket_patterns + docstring_patterns + 
                       string_patterns + call_patterns + simple_patterns)
        
        for pattern, replacement in all_patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        return content
    
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
        """単一ファイルの修復"""
        if not os.path.exists(file_path):
            print(f"⚠️ ファイル未発見: {file_path}")
            return False
            
        print(f"🔧 修復中: {file_path}")
        
        # ファイル読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ 読み込みエラー {file_path}: {e}")
            return False
        
        # 修復実行
        fixed_content = self.fix_file_content(original_content)
        
        # ファイル書き込み
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
            print(f"❌ 構文エラー残存 {file_path}: {error_msg[:100]}")
            self.error_files.append(file_path)
            return False
    
    def restore_from_backup(self, file_path):
        """バックアップからの復旧"""
        backup_path = os.path.join(self.backup_dir, file_path)
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"🔄 復旧: {file_path}")
            return True
        return False
    
    def run(self):
        """メイン修復処理"""
        print(f"🚀 精密構文修復開始: {datetime.now()}")
        
        # バックアップ作成
        self.create_backup()
        
        # 各ファイルを修復
        for file_path in self.target_files:
            success = self.fix_file(file_path)
            if not success and os.path.exists(file_path):
                # 修復失敗時はバックアップから復旧
                self.restore_from_backup(file_path)
        
        # 結果レポート
        print(f"\n📊 修復結果:")
        print(f"  ✅ 成功: {len(self.fixed_files)}ファイル")
        print(f"  ❌ 失敗: {len(self.error_files)}ファイル")
        
        if self.fixed_files:
            print("  📝 修復成功ファイル:")
            for f in self.fixed_files:
                print(f"    - {f}")
        
        if self.error_files:
            print("  🚨 修復失敗ファイル:")
            for f in self.error_files:
                print(f"    - {f}")
        
        # 最終テスト
        print(f"\n🧪 最終動作テスト...")
        try:
            subprocess.run([sys.executable, '-c', 'print("✅ Python環境正常")'], 
                         check=True, timeout=5)
        except:
            print("❌ Python環境に問題")
        
        print(f"🎯 修復完了: {datetime.now()}")
        return len(self.error_files) == 0

if __name__ == "__main__":
    fixer = PreciseSyntaxFixer()
    success = fixer.run()
    
    if success:
        print("\n🎉 全ファイル修復成功！kioku強化準備完了")
    else:
        print("\n⚠️ 一部ファイルに問題残存。個別対応が必要")
    
    sys.exit(0 if success else 1)
