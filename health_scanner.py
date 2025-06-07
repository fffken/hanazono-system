import subprocess
import sys
import os # 修正点：osモジュールをインポート

def run_command(command):
    """コマンドを実行し、標準出力と標準エラーを返す"""
    try:
        # venvが有効な状態で実行されることを前提とする
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            executable='/bin/bash'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"--- ERROR ---\n{e.stderr.strip()}"
    except FileNotFoundError as e:
        return f"--- ERROR: Command not found ---\n{e}"

def print_header(title):
    """診断項目のヘッダーを表示する"""
    print("\n" + "="*80)
    print(f"🔬 {title}")
    print("="*80)

def main():
    """システム健康診断を実行するメイン関数"""
    print("🚀 lvyuan_solar_controlプロジェクト 総合健康診断スキャナー起動...")

    # 1. バージョン管理の健全性
    print_header("1. バージョン管理の健全性 (Git Health)")
    print("調査方法: git status")
    print("--- 結果 ---")
    print(run_command("git status"))

    # 2. 依存関係の整合性
    print_header("2. 依存関係の整合性 (Dependency Health)")
    print("調査方法: pip freeze")
    print("--- 結果 ---")
    print(run_command("pip freeze"))

    # 3. 主要モジュールの静的解析
    print_header("3. 主要モジュールの静的解析 (Core Module Analysis)")
    key_files = [
        "main.py",
        "email_capsule.py",
        "hcqas_capsule.py",
        "collector_capsule.py",
        "weather_forecast.py",
        "lvyuan_collector.py",
        "settings_manager.py"
    ]
    # 存在するファイルのみを対象にする
    existing_key_files = [f for f in key_files if os.path.exists(f)]
    print(f"調査方法: python3 -m py_compile {' '.join(existing_key_files)}")
    print("--- 結果 ---")
    if not existing_key_files:
        print("⚠️ 主要な診断対象ファイルが見つかりませんでした。")
    else:
        compile_result = run_command(f"python3 -m py_compile {' '.join(existing_key_files)}")
        if not compile_result:
            print("✅ 全ての主要ファイルに文法的な問題はありませんでした。")
        else:
            print(compile_result)

    # 4. 自動実行システムの連携確認
    print_header("4. 自動実行システムの連携確認 (Automation & Cron Check)")
    print("調査方法: crontab -l")
    print("--- 結果 ---")
    print(run_command("crontab -l"))

    # 5. 設定ファイルの一貫性検証
    print_header("5. 設定ファイルの一貫性検証 (Configuration Check)")
    print("調査方法: python3 -m json.tool settings.json")
    print("--- 結果 ---")
    if not os.path.exists('settings.json'):
         print("⚠️ settings.jsonファイルが見つかりません。")
    else:
        json_check_command = "python3 -m json.tool settings.json > /dev/null 2>&1"
        result_code = subprocess.run(json_check_command, shell=True).returncode
        if result_code == 0:
            print("✅ settings.jsonは、正常なJSON形式です。")
        else:
            print("❌ settings.jsonの形式にエラーがあります。")
            print(run_command("python3 -m json.tool settings.json"))
    
    print("\n" + "="*80)
    print("✅ 健康診断スキャン完了")
    print("="*80)


if __name__ == "__main__":
    if 'VIRTUAL_ENV' not in os.environ:
        print("警告: 仮想環境(venv)が有効になっていない可能性があります。")
        print("source venv/bin/activate を実行してから、このスクリプトを起動してください。")
        sys.exit(1)
    main()
