import sys
import argparse
import subprocess

def main():
    """
    各機能カプセルを安全に呼び出すための司令塔。
    """
    parser = argparse.ArgumentParser(description="HANAZONOシステム司令塔")
    parser.add_argument('--daily-report', action='store_true', help='メールレポート機能カプセルを起動します')
    parser.add_argument('--run-hcqas', action='store_true', help='HCQAS提案機能カプセルを起動します')
    args = parser.parse_args()

    # 使用するPythonのパスを特定
    python_executable = sys.executable

    if args.daily_report:
        print("司令塔: メール機能カプセルを起動します...")
        subprocess.run([python_executable, 'email_capsule.py'])
        print("司令塔: メール機能カプセルの処理が完了しました。")

    elif args.run_hcqas:
        print("司令塔: HCQAS提案機能カプセルを起動します...")
        subprocess.run([python_executable, 'hcqas_capsule.py'])
        print("司令塔: HCQAS提案機能カプセルの処理が完了しました。")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
