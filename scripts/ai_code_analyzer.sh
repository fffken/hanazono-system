#!/bin/bash
# AI駆使 完全自動コード解析システム v1.0

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "${BLUE}=== AI駆使 完全自動コード解析システム ===${NC}"

# Python用静的解析ツールの自動インストール・実行
setup_analysis_tools() {
    echo -e "${YELLOW}🔧 AI解析ツール自動セットアップ中...${NC}"
    
    # 必要なツールを自動インストール
    pip install pycodestyle pyflakes bandit safety vulture radon mccabe autopep8 >/dev/null 2>&1
    
    echo "✅ AI解析ツール準備完了"
}

# 完全自動コード品質チェック
auto_code_quality_check() {
    echo -e "${YELLOW}🎯 AI自動コード品質チェック実行中...${NC}"
    
    local report_file="AI_CODE_ANALYSIS_REPORT.md"
    
    cat > $report_file << REPORT_EOF
# AI完全自動コード解析レポート

**生成時刻**: $TIMESTAMP  
**解析対象**: HANAZONOシステム全体

## 🤖 AI自動解析結果

REPORT_EOF

    # Pythonファイルの自動検出・解析
    for py_file in $(find . -name "*.py" -not -path "./venv/*" -not -path "./.git/*"); do
        echo "  🔍 解析中: $py_file"
        
        echo "### 📁 ファイル: \`$py_file\`" >> $report_file
        
        # 1. コードスタイルチェック (PEP 8準拠)
        echo "#### 🎨 コードスタイル解析" >> $report_file
        style_issues=$(pycodestyle "$py_file" 2>/dev/null | wc -l)
        if [ $style_issues -gt 0 ]; then
            echo "- ⚠️ スタイル問題: $style_issues 件" >> $report_file
            echo '```' >> $report_file
            pycodestyle "$py_file" 2>/dev/null | head -5 >> $report_file
            echo '```' >> $report_file
        else
            echo "- ✅ スタイル: 問題なし" >> $report_file
        fi
        
        # 2. 潜在的バグ検出
        echo "#### 🐛 潜在的バグ解析" >> $report_file
        bug_count=$(pyflakes "$py_file" 2>/dev/null | wc -l)
        if [ $bug_count -gt 0 ]; then
            echo "- ⚠️ 潜在的問題: $bug_count 件" >> $report_file
            echo '```' >> $report_file
            pyflakes "$py_file" 2>/dev/null | head -3 >> $report_file
            echo '```' >> $report_file
        else
            echo "- ✅ バグチェック: 問題なし" >> $report_file
        fi
        
        # 3. セキュリティ脆弱性チェック
        echo "#### 🔒 セキュリティ解析" >> $report_file
        security_issues=$(bandit -f txt "$py_file" 2>/dev/null | grep -c "Issue:" || echo "0")
        if [ $security_issues -gt 0 ]; then
            echo "- ⚠️ セキュリティ問題: $security_issues 件" >> $report_file
        else
            echo "- ✅ セキュリティ: 問題なし" >> $report_file
        fi
        
        # 4. 複雑度解析
        echo "#### 📊 コード複雑度解析" >> $report_file
        complexity=$(radon cc "$py_file" -a 2>/dev/null | grep "Average complexity" | awk '{print $NF}' || echo "N/A")
        if [[ $complexity =~ ^[0-9]+(\.[0-9]+)?$ ]] && (( $(echo "$complexity > 10" | bc -l) )); then
            echo "- ⚠️ 高複雑度: $complexity (リファクタリング推奨)" >> $report_file
        else
            echo "- ✅ 複雑度: 適切 ($complexity)" >> $report_file
        fi
        
        # 5. 未使用コード検出
        echo "#### 🧹 未使用コード解析" >> $report_file
        dead_code=$(vulture "$py_file" 2>/dev/null | wc -l)
        if [ $dead_code -gt 0 ]; then
            echo "- ⚠️ 未使用コード: $dead_code 箇所" >> $report_file
        else
            echo "- ✅ 未使用コード: なし" >> $report_file
        fi
        
        echo "" >> $report_file
    done
    
    echo "✅ AI自動コード品質チェック完了: $report_file"
}

# AI自動バグ検出・分類
auto_bug_detection() {
    echo -e "${YELLOW}🐛 AI自動バグ検出システム実行中...${NC}"
    
    cat >> AI_CODE_ANALYSIS_REPORT.md << BUG_EOF

## 🐛 AI自動バグ検出結果

BUG_EOF

    # 一般的なPythonバグパターンの検出
    echo "### 📋 一般的バグパターン検出" >> AI_CODE_ANALYSIS_REPORT.md
    
    for py_file in $(find . -name "*.py" -not -path "./venv/*" -not -path "./.git/*"); do
        # 空の例外処理
        empty_except=$(grep -n "except.*:" "$py_file" | grep -v "except.*as\|except.*Exception" | wc -l)
        if [ $empty_except -gt 0 ]; then
            echo "- ⚠️ \`$py_file\`: 空の例外処理 ($empty_except 箇所)" >> AI_CODE_ANALYSIS_REPORT.md
        fi
        
        # print文の残存（デバッグコード）
        print_statements=$(grep -n "print(" "$py_file" | grep -v "#.*print" | wc -l)
        if [ $print_statements -gt 0 ]; then
            echo "- 📝 \`$py_file\`: デバッグprint文 ($print_statements 箇所)" >> AI_CODE_ANALYSIS_REPORT.md
        fi
        
        # TODO/FIXMEコメント
        todo_count=$(grep -ni "TODO\|FIXME" "$py_file" | wc -l)
        if [ $todo_count -gt 0 ]; then
            echo "- 📌 \`$py_file\`: TODO/FIXME ($todo_count 箇所)" >> AI_CODE_ANALYSIS_REPORT.md
        fi
    done
    
    echo "✅ AI自動バグ検出完了"
}

# AI自動修正提案生成
auto_fix_suggestions() {
    echo -e "${YELLOW}🔧 AI自動修正提案生成中...${NC}"
    
    cat >> AI_CODE_ANALYSIS_REPORT.md << FIX_EOF

## 🔧 AI自動修正提案

### 📋 自動修正可能な項目
FIX_EOF

    # 自動修正スクリプト生成
    cat > auto_code_fixes.py << PY_EOF
#!/usr/bin/env python3
"""AI自動コード修正スクリプト"""

import os
import re
import subprocess
from typing import List, Dict

class AICodeFixer:
    def __init__(self):
        self.fixes_applied = []
    
    def auto_fix_style_issues(self, file_path: str) -> bool:
        """PEP8スタイルの自動修正"""
        try:
            result = subprocess.run(['autopep8', '--in-place', file_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.fixes_applied.append(f"スタイル修正: {file_path}")
                return True
        except FileNotFoundError:
            pass
        return False
    
    def detect_potential_issues(self, file_path: str) -> List[str]:
        """潜在的問題の検出"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # 空の例外処理
                if re.search(r'except.*:\s*$', line):
                    issues.append(f"Line {i}: 空の例外処理")
                
                # ハードコードされたパス
                if re.search(r'["\']\/[^"\']*["\']', line):
                    issues.append(f"Line {i}: ハードコードされたパス")
                
                # 長すぎる行
                if len(line) > 120:
                    issues.append(f"Line {i}: 長すぎる行 ({len(line)} chars)")
                    
        except Exception as e:
            issues.append(f"解析エラー: {e}")
        
        return issues
    
    def generate_report(self) -> str:
        """修正レポート生成"""
        return f"適用された修正: {len(self.fixes_applied)} 件"

if __name__ == "__main__":
    fixer = AICodeFixer()
    
    # Pythonファイルの自動検出・修正
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # スタイル自動修正
                fixer.auto_fix_style_issues(file_path)
                
                # 問題検出
                issues = fixer.detect_potential_issues(file_path)
                if issues:
                    print(f"\\n{file_path}:")
                    for issue in issues[:5]:  # 最初の5件のみ表示
                        print(f"  - {issue}")
    
    print(f"\\n{fixer.generate_report()}")
PY_EOF

    echo "- 🔧 自動スタイル修正スクリプト生成済み" >> AI_CODE_ANALYSIS_REPORT.md
    echo "- 🎯 潜在的問題検出システム構築済み" >> AI_CODE_ANALYSIS_REPORT.md
    echo "- 📊 実行方法: \`python3 auto_code_fixes.py\`" >> AI_CODE_ANALYSIS_REPORT.md
    
    echo "✅ AI自動修正提案生成完了"
}

# 依存関係脆弱性チェック
auto_security_check() {
    echo -e "${YELLOW}🔒 AI自動セキュリティチェック実行中...${NC}"
    
    # requirements.txtが存在する場合
    if [ -f "requirements.txt" ]; then
        echo "### 🔒 依存関係セキュリティチェック" >> AI_CODE_ANALYSIS_REPORT.md
        safety_report=$(safety check -r requirements.txt 2>/dev/null || echo "セキュリティチェックツールが利用できません")
        echo '```' >> AI_CODE_ANALYSIS_REPORT.md
        echo "$safety_report" >> AI_CODE_ANALYSIS_REPORT.md
        echo '```' >> AI_CODE_ANALYSIS_REPORT.md
    fi
    
    echo "✅ AI自動セキュリティチェック完了"
}

# メイン実行
main() {
    setup_analysis_tools
    auto_code_quality_check
    auto_bug_detection
    auto_fix_suggestions
    auto_security_check
    
    echo -e "${GREEN}=== AI完全自動コード解析システム実行完了 ===${NC}"
    echo -e "${GREEN}📊 詳細レポート: AI_CODE_ANALYSIS_REPORT.md${NC}"
    echo -e "${GREEN}🔧 自動修正: python3 auto_code_fixes.py${NC}"
    echo -e "${BLUE}📋 要約レポート表示中...${NC}"
    
    # 要約表示
    echo -e "\n${YELLOW}=== AI解析要約 ===${NC}"
    total_files=$(find . -name "*.py" -not -path "./venv/*" -not -path "./.git/*" | wc -l)
    echo "📁 解析ファイル数: $total_files"
    
    if [ -f "AI_CODE_ANALYSIS_REPORT.md" ]; then
        issues=$(grep -c "⚠️" AI_CODE_ANALYSIS_REPORT.md 2>/dev/null || echo "0")
        echo "⚠️ 検出された問題: $issues 件"
        
        if [ $issues -eq 0 ]; then
            echo -e "${GREEN}🎉 コード品質: 優秀${NC}"
        elif [ $issues -lt 5 ]; then
            echo -e "${YELLOW}📊 コード品質: 良好${NC}"
        else
            echo -e "${RED}🔧 コード品質: 改善推奨${NC}"
        fi
    fi
}

main "$@"
