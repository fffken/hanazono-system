#!/usr/bin/env python3
# HANAZONO完全レポート解析v2 - 正確なパターン検索
import os
import datetime

def analyze_complete_report_v2():
    """より正確な検索で完全レポート版を作成"""
    
    print("🔍 HANAZONO完全レポート解析v2開始")
    print("=" * 50)
    
    # 1. 元ファイル確認
    if not os.path.exists("hanazono_original_safe.py"):
        print("❌ 元ファイルバックアップが存在しません")
        return False
    
    print("✅ 元ファイルバックアップ確認")
    
    # 2. 元ファイルの詳細解析
    with open("hanazono_original_safe.py", "r", encoding="utf-8") as f:
        original_content = f.read()
    
    print("✅ 元ファイル読み込み完了")
    
    # 3. 実際のrun_daily_optimizationメソッド検索
    print("📋 run_daily_optimizationメソッド検索...")
    
    # より柔軟な検索パターン
    lines = original_content.splitlines()
    method_start = -1
    method_end = -1
    
    for i, line in enumerate(lines):
        if "def run_daily_optimization" in line:
            method_start = i
            print(f"✅ メソッド開始: {i+1}行目")
            break
    
    if method_start == -1:
        print("❌ run_daily_optimizationメソッドが見つかりません")
        return False
    
    # メソッド終了位置を検索
    indent_level = len(lines[method_start]) - len(lines[method_start].lstrip())
    for i in range(method_start + 1, len(lines)):
        line = lines[i]
        if line.strip() and (len(line) - len(line.lstrip())) <= indent_level and not line.lstrip().startswith('#'):
            method_end = i
            break
    
    if method_end == -1:
        method_end = len(lines)
    
    print(f"✅ メソッド終了: {method_end}行目")
    
    # 4. メソッド内容抽出
    method_lines = lines[method_start:method_end]
    method_content = "\n".join(method_lines)
    
    print(f"✅ メソッド内容抽出完了 ({len(method_lines)}行)")
    
    # 5. 詳細レポート部分検索
    print("📋 詳細レポート部分検索...")
    
    # メソッド内容を表示して確認
    print("📊 メソッド内容確認（最初20行）:")
    for i, line in enumerate(method_lines[:20]):
        print(f"  {i+1:2d}: {line}")
    
    # 長いレポート表示部分を検索
    report_start = -1
    report_end = -1
    
    for i, line in enumerate(method_lines):
        if "📧" in line and ("メール" in line or "シミュレーション" in line):
            report_start = i
            print(f"✅ レポート開始: メソッド内{i+1}行目")
            break
    
    if report_start != -1:
        # レポート終了を検索
        for i in range(report_start + 1, len(method_lines)):
            line = method_lines[i]
            if "Enhanced Email System" in line or "メールレポート:" in line:
                report_end = i + 1
                print(f"✅ レポート終了: メソッド内{i+1}行目")
                break
        
        if report_end == -1:
            report_end = len(method_lines)
        
        # レポート内容抽出
        report_lines = method_lines[report_start:report_end]
        detailed_report = "\n".join(report_lines)
        
        print(f"✅ 詳細レポート抽出完了 ({len(report_lines)}行)")
        print("📊 詳細レポート内容確認（最初10行）:")
        for i, line in enumerate(report_lines[:10]):
            print(f"  {i+1:2d}: {line}")
    else:
        print("❌ 詳細レポート部分が見つかりません")
        return False
    
    # 6. 現在の修正版読み込み
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        current_content = f.read()
    
    # 7. 現在の簡易レポート部分を詳細レポートに置換
    print("📋 完全レポート版作成...")
    
    # 現在の簡易email_body部分を検索
    import re
    simple_pattern = r'email_body = f"""HANAZONOシステム日次最適化レポート.*?--- HANAZONOシステム自動レポート ---"""'
    
    # 詳細レポートをemail_bodyとして設定
    detailed_email_body = f'''email_body = f"""{detailed_report.strip()}"""'''
    
    # 置換実行
    if re.search(simple_pattern, current_content, re.DOTALL):
        modified_content = re.sub(simple_pattern, detailed_email_body, current_content, flags=re.DOTALL)
        print("✅ 簡易レポート→詳細レポート置換完了")
    else:
        print("❌ 簡易レポート部分が見つかりません")
        return False
    
    # 8. 完全版ファイル保存
    complete_filename = f"hanazono_complete_system_detailed_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    with open(complete_filename, "w", encoding="utf-8") as f:
        f.write(modified_content)
    
    print(f"✅ 完全レポート版作成: {complete_filename}")
    
    # 9. 構文チェック
    try:
        import ast
        ast.parse(modified_content)
        print("✅ 構文チェック: 正常")
    except SyntaxError as e:
        print(f"❌ 構文エラー: {e}")
        os.remove(complete_filename)
        return False
    
    # 10. テスト手順案内
    print("\n📋 完全非破壊的テスト手順")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 詳細レポート版テスト:")
    print("1. 現状バックアップ:")
    print("   cp hanazono_complete_system.py hanazono_simple_backup.py")
    print("")
    print("2. 詳細レポート版適用:")
    print(f"   cp {complete_filename} hanazono_complete_system.py")
    print("")
    print("3. テスト実行:")
    print("   python3 -c \"from hanazono_complete_system import HANAZONOCompleteSystem; system=HANAZONOCompleteSystem(); system.run_daily_optimization()\"")
    print("")
    print("4. 復旧方法:")
    print("   cp hanazono_simple_backup.py hanazono_complete_system.py")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\n🎉 完全非破壊的詳細レポート版作成完了")
    return complete_filename

if __name__ == "__main__":
    result = analyze_complete_report_v2()
    if result:
        print(f"\n✅ 成功: {result}")
        print("📋 次: テスト手順を実行してください")
    else:
        print(f"\n❌ 失敗: 全ファイル保護済み")
