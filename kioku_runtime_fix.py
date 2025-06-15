#!/usr/bin/env python3
"""
kioku_precision_system.py 実行時エラー修正スクリプト
問題: NameError: name 'summary' is not defined (320行目)
"""

def fix_runtime_error():
    """実行時エラー自動修正"""
    print("🔧 kioku_precision_system.py 実行時エラー修正開始")
    
    # 1. ファイル読み込み
    try:
        with open('kioku_precision_system.py', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ ファイル読み込み完了")
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return False
    
    # 2. 問題箇所修正（インデント問題）
    # _generate_quick_summary関数のインデント修正
    fixed_content = content.replace(
        '    def _generate_quick_summary(self):\n        """AI即座理解用軽量サマリー"""\n        summary = f"""',
        '    def _generate_quick_summary(self):\n        """AI即座理解用軽量サマリー"""\n        summary = f"""'
    )
    
    # summary変数定義の問題を修正
    # クラス内のメソッドでsummary変数が正しく定義されるように修正
    if 'f.write(summary)' in fixed_content and 'summary = f"""' not in fixed_content:
        # summary変数の定義を追加
        fixed_content = fixed_content.replace(
            'def _generate_quick_summary(self):',
            '''def _generate_quick_summary(self):
        """AI即座理解用軽量サマリー"""
        summary = f"""# 🎯 HANAZONO即座理解サマリー

**現在状況（3行要約）**:
1. HANAZONOシステムv4.0完成、6年間データ統合済み (hanazono_master_data.db)
2. メールシステム (email_notifier.py 25,792バイト) 実装完了
3. 次のアクション: システム動作確認 → ML予測機能実装

**最重要ファイル**:
- email_notifier.py: メインシステム
- data/hanazono_master_data.db: 6年間データ
- main.py: 統合制御

**即座実行コマンド**:
```bash
python3 email_notifier.py  # メールシステムテスト
ls -la data/hanazono_master_data.db  # データ確認
git status  # 変更状況確認
"""''' )

# 3. 修正版保存
try:
    with open('kioku_precision_system.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("✅ 修正版保存完了")
except Exception as e:
    print(f"❌ 保存エラー: {e}")
    return False

# 4. 構文チェック
import subprocess
try:
    result = subprocess.run(['python3', '-m', 'py_compile', 'kioku_precision_system.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 構文チェック: 正常")
    else:
        print(f"❌ 構文エラー: {result.stderr}")
        return False
except Exception as e:
    print(f"⚠️ 構文チェックエラー: {e}")

return True
def create_minimal_working_version(): """最小動作版作成（フォールバック）""" print("\n🔧 最小動作版作成:")

minimal_code = '''#!/usr/bin/env python3
""" HANAZONO継承精度向上システム v1.0 (最小動作版) """

import os import json import subprocess from datetime import datetime from pathlib import Path

class KiokuPrecisionSystem: def init(self): self.version = "1.0.0-MINIMAL"

def analyze_and_generate_precision_handover(self):
    print("🧠 HANAZONO継承精度向上システム実行開始")
    print("=" * 60)
    
    # Git情報取得
    git_info = self._get_git_info()
    
    # ファイル状況確認
    file_status = self._check_files()
    
    # 継承ドキュメント生成
    self._generate_handover(git_info, file_status)
    
    print("🎯 継承精度向上システム実行完了")
    return True

def _get_git_info(self):
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        changes = len(result.stdout.strip().split('\\n')) if result.stdout.strip() else 0
        
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        branch = result.stdout.strip()
        
        return {'branch': branch, 'changes': changes}
    except:
        return {'branch': 'unknown', 'changes': 0}

def _check_files(self):
    key_files = ['email_notifier.py', 'main.py', 'data/hanazono_master_data.db']
    status = {}
    
    for file in key_files:
        if os.path.exists(file):
            stat = os.stat(file)
            status[file] = {'exists': True, 'size': stat.st_size}
        else:
            status[file] = {'exists': False}
    
    return status

def _generate_handover(self, git_info, file_status):
    content = f"""# 🧠 HANAZONO AI継承ドキュメント v2.0
生成時刻: {datetime.now().isoformat()}

🚨 CRITICAL_IMMEDIATE
1. システム状況
Git ブランチ: {git_info['branch']}
未コミット変更: {git_info['changes']}件
2. 重要ファイル状況
"""

    for file, info in file_status.items():
        if info['exists']:
            content += f"- ✅ {file}: {info['size']}バイト\\n"
        else:
            content += f"- ❌ {file}: 未存在\\n"
    
    content += """
🎯 AI次回必須アクション
システム動作確認: python3 email_notifier.py
データ確認: ls -la data/hanazono_master_data.db
Git状況確認: git status
継承精度向上システムv1.0により生成 """

    with open('KIOKU_PRECISION_HANDOVER.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 軽量版
    quick_summary = """# 🎯 HANAZONO即座理解サマリー
現在状況: HANAZONOシステムv4.0、6年間データ統合済み 次のアクション: python3 email_notifier.py でテスト実行 重要ファイル: email_notifier.py, data/hanazono_master_data.db """

    with open('KIOKU_QUICK_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(quick_summary)
    
    print("📋 継承ドキュメント生成完了")
def main(): print("🚀 実行時エラー修正スクリプト実行") print("=" * 40)

# まず修正を試行
if fix_runtime_error():
    print("✅ 修正完了、テスト実行...")
    
    # テスト実行
    import subprocess
    try:
        result = subprocess.run(['python3', 'kioku_precision_system.py'], 
                              capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            print("🎉 修正成功！正常実行完了")
            print(result.stdout)
        else:
            print("⚠️ まだエラーあり、最小動作版作成...")
            create_minimal_working_version()
            
            # 最小版テスト
            precision_system = KiokuPrecisionSystem()
            precision_system.analyze_and_generate_precision_handover()
            print("✅ 最小動作版で実行完了")
    except:
        print("⚠️ テスト失敗、最小動作版作成...")
        create_minimal_working_version()
else:
    print("❌ 修正失敗、最小動作版作成...")
    create_minimal_working_version()

# クリーンアップ
print("\\n🧹 クリーンアップ...")
import os
try:
    os.remove(__file__)
    print("✅ 一時スクリプト削除完了")
except:
    pass
if name == "main": main() '''

try:
    with open('kioku_precision_system_minimal.py', 'w', encoding='utf-8') as f:
        f.write(minimal_code)
    print("✅ 最小動作版作成完了")
    
    # 最小版実行
    exec(minimal_code)
    
except Exception as e:
    print(f"❌ 最小版作成エラー: {e}")
if name == "main": 
    main()
