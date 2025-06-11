#!/usr/bin/env python3
"""
HANAZONO ML依存関係インストール
Phase 2に必要なライブラリを安全にインストール
"""

import subprocess
import sys
import os
from datetime import datetime

def install_package(package_name):
    """パッケージ安全インストール"""
    try:
        print(f"📦 {package_name} インストール中...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"✅ {package_name} インストール成功")
            return True
        else:
            print(f"❌ {package_name} インストール失敗: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {package_name} インストールタイムアウト")
        return False
    except Exception as e:
        print(f"❌ {package_name} インストールエラー: {e}")
        return False

def main():
    print("🚀 HANAZONO ML依存関係インストール開始")
    print(f"📅 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 必要なパッケージリスト
    required_packages = [
        "numpy",
        "pandas", 
        "scikit-learn"
    ]
    
    # インストール実行
    success_count = 0
    for package in required_packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 インストール結果: {success_count}/{len(required_packages)} 成功")
    
    if success_count == len(required_packages):
        print("🎉 全依存関係インストール完了！")
        print("🚀 Phase 2 ML Predictor実行準備完了")
        return True
    else:
        print("⚠️ 一部インストール失敗")
        print("💡 手動インストール推奨:")
        for package in required_packages:
            print(f"  pip3 install {package}")
        return False

if __name__ == "__main__":
    main()
