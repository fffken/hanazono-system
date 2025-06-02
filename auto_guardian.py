import os,subprocess,sys
def check_and_fix():
    if not os.path.exists("venv/bin/python3"):
        print("🔧 venv再作成中...")
        subprocess.run(["python3", "-m", "venv", "venv"])
    
    # パッケージ確認
    try:
        # venv内のpipを直接使用
        pip_path = "./venv/bin/pip"
        python_path = "./venv/bin/python3"
        
        if os.path.exists(pip_path):
            subprocess.run([pip_path, "install", "pysolarmanv5", "requests", "urllib3"], check=True)
            result = subprocess.run([python_path, "-c", "import pysolarmanv5"], capture_output=True)
            if result.returncode == 0:
                print("✅ 自動修復成功")
                return True
    except Exception as e:
        print(f"修復エラー: {e}")
    
    print("❌ 自動修復失敗")
    return False

if __name__ == "__main__":
    sys.exit(0 if check_and_fix() else 1)
