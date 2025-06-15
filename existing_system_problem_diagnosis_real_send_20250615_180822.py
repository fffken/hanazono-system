#!/usr/bin/env python3
# 既存システム問題箇所特定診断
import os
import subprocess

class ExistingSystemDiagnosis:
    """既存システムの問題箇所特定"""
    
    def __init__(self):
        self.issues = []
        
    def check_weather_system(self):
        """天気システム診断"""
        print("🌤️ 天気システム診断")
        print("=" * 50)
        
        # 1. weather_forecast.py実行テスト
        try:
            result = subprocess.run(['python3', 'weather_forecast.py'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ weather_forecast.py: 実行成功")
                if "今日" in result.stdout or "tomorrow" in result.stdout:
                    print("✅ 天気データ出力: OK")
                else:
                    print("❌ 天気データ出力: 固定値またはエラー")
                    self.issues.append("天気データが動的でない")
            else:
                print(f"❌ weather_forecast.py: 実行失敗")
                print(f"エラー: {result.stderr}")
                self.issues.append("weather_forecast.py実行エラー")
        except Exception as e:
            print(f"❌ weather_forecast.py: {e}")
            self.issues.append(f"weather_forecast.py例外: {e}")
            
    def check_settings_system(self):
        """推奨設定システム診断"""
        print("\n🔧 推奨設定システム診断")
        print("=" * 50)
        
        # GitHub設定ガイド取得テスト
        try:
            import requests
            url = "https://raw.githubusercontent.com/fffken/hanazono-system/refs/heads/main/docs/HANAZONO-SYSTEM-SETTINGS.md"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ GitHub設定ガイド: 取得成功")
                if "ID" in response.text and "62" in response.text:
                    print("✅ 設定内容: ID62など確認済み")
                else:
                    print("❌ 設定内容: 期待する内容なし")
                    self.issues.append("GitHub設定ガイド内容不備")
            else:
                print(f"❌ GitHub設定ガイド: HTTP {response.status_code}")
                self.issues.append("GitHub設定ガイド取得失敗")
        except Exception as e:
            print(f"❌ GitHub設定ガイド: {e}")
            self.issues.append(f"GitHub設定ガイド例外: {e}")
            
    def check_ml_optimization(self):
        """ML最適化システム診断"""
        print("\n🤖 ML最適化システム診断")  
        print("=" * 50)
        
        # 既存MLシステム確認
        ml_files = ['ml_optimizer.py', 'hanazono_ml.py', 'optimization_engine.py']
        found_ml = False
        
        for ml_file in ml_files:
            if os.path.exists(ml_file):
                print(f"✅ {ml_file}: 存在")
                found_ml = True
                
                # ML実行テスト
                try:
                    result = subprocess.run(['python3', ml_file], 
                                          capture_output=True, text=True, timeout=15)
                    if result.returncode == 0:
                        print(f"✅ {ml_file}: 実行成功")
                    else:
                        print(f"❌ {ml_file}: 実行失敗")
                        self.issues.append(f"{ml_file}実行エラー")
                except Exception as e:
                    print(f"❌ {ml_file}: {e}")
                    self.issues.append(f"{ml_file}例外: {e}")
            else:
                print(f"❌ {ml_file}: 未発見")
                
        if not found_ml:
            print("❌ MLシステム: 未実装")
            self.issues.append("MLシステム未実装")
            
    def check_main_system_integration(self):
        """メインシステム統合診断"""
        print("\n🏗️ メインシステム統合診断")
        print("=" * 50)
        
        # 現在のメインシステム実行
        try:
            result = subprocess.run(['python3', 'hanazono_complete_system.py'], 
                                  capture_output=True, text=True, timeout=30)
            
            output = result.stdout + result.stderr
            
            # 問題箇所チェック
            if "シミュレーション" in output:
                print("❌ メインシステム: 実送信モード")
                self.issues.append("メインシステムが実送信モード")
            
            if "フォールバック" in output:
                print("❌ メインシステム: フォールバックデータ使用")
                self.issues.append("フォールバックデータ使用")
                
            if "固定値" in output or "固定" in output:
                print("❌ メインシステム: 固定値使用")
                self.issues.append("固定値使用")
                
            if "API" not in output:
                print("❌ メインシステム: API連携なし")
                self.issues.append("API連携なし")
                
        except Exception as e:
            print(f"❌ メインシステム: {e}")
            self.issues.append(f"メインシステム例外: {e}")
            
    def generate_problem_report(self):
        """問題レポート生成"""
        print(f"\n" + "=" * 60)
        print("🚨 問題箇所特定レポート")
        print("=" * 60)
        
        if not self.issues:
            print("✅ 問題なし: 全システム正常動作")
        else:
            print(f"❌ 検出問題数: {len(self.issues)}")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
                
        print(f"\n🎯 修正が必要な箇所:")
        priority_issues = [issue for issue in self.issues if any(keyword in issue for keyword in ["シミュレーション", "固定値", "API"])]
        
        if priority_issues:
            for issue in priority_issues:
                print(f"   🔧 {issue}")
        else:
            print("   ✅ 高優先度問題なし")
            
        return self.issues
        
    def run_diagnosis(self):
        """完全診断実行"""
        print("🎯 既存システム問題箇所特定診断開始")
        print("=" * 60)
        
        self.check_weather_system()
        self.check_settings_system()
        self.check_ml_optimization()
        self.check_main_system_integration()
        
        issues = self.generate_problem_report()
        
        print(f"\n🎉 診断完了")
        return issues

if __name__ == "__main__":
    diagnosis = ExistingSystemDiagnosis()
    diagnosis.run_diagnosis()
