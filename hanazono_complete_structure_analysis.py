#!/usr/bin/env python3
# HANAZONO完全構造解析スクリプト - 修正前の完全把握
import os
import inspect
import ast
import datetime

def complete_structure_analysis():
    """HANAZONOシステムの完全構造解析"""
    
    print("🔍 HANAZONO完全構造解析開始")
    print("=" * 50)
    
    # 1. ファイル構造解析
    print("📋 1. ファイル構造解析")
    try:
        with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"📊 ファイルサイズ: {len(content)} 文字")
        print(f"📊 行数: {len(content.splitlines())} 行")
        
        # クラス構造解析
        tree = ast.parse(content)
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        print(f"📊 クラス数: {len(classes)}")
        print(f"📊 関数数: {len(functions)}")
        
        for cls in classes:
            print(f"  📁 クラス: {cls.name}")
            methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
            print(f"    📊 メソッド数: {len(methods)}")
            for method in methods:
                print(f"      🔧 {method.name}")
        
    except Exception as e:
        print(f"❌ ファイル解析エラー: {e}")
    
    # 2. run_daily_optimizationメソッド詳細解析
    print("\n📋 2. run_daily_optimizationメソッド詳細解析")
    try:
        from hanazono_complete_system import HANAZONOCompleteSystem
        system = HANAZONOCompleteSystem()
        
        # メソッドのソースコード取得
        source = inspect.getsource(system.run_daily_optimization)
        lines = source.splitlines()
        
        print(f"📊 メソッド行数: {len(lines)}")
        print("📊 メソッド構造:")
        
        # 重要な行を抽出
        important_lines = []
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['email', 'mail', 'send', 'smtp', 'return', 'print']):
                important_lines.append((i+1, line.strip()))
        
        print("📊 メール・送信関連行:")
        for line_num, line in important_lines:
            print(f"  {line_num:3d}: {line}")
        
        # メソッドの終了パターン確認
        print("\n📊 メソッド終了部分（最後10行）:")
        for i, line in enumerate(lines[-10:], len(lines)-9):
            print(f"  {i:3d}: {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ メソッド解析エラー: {e}")
    
    # 3. メール関連機能の現状確認
    print("\n📋 3. メール関連機能現状確認")
    try:
        from hanazono_complete_system import HANAZONOCompleteSystem
        system = HANAZONOCompleteSystem()
        
        # 利用可能なメソッド確認
        methods = [method for method in dir(system) if 'mail' in method.lower() or 'email' in method.lower()]
        print(f"📊 メール関連メソッド: {methods}")
        
        # send_actual_emailメソッドの詳細
        if hasattr(system, 'send_actual_email'):
            email_source = inspect.getsource(system.send_actual_email)
            print(f"📊 send_actual_email行数: {len(email_source.splitlines())}")
            print("📊 send_actual_emailの先頭5行:")
            for i, line in enumerate(email_source.splitlines()[:5]):
                print(f"  {i+1}: {line}")
        
    except Exception as e:
        print(f"❌ メール機能確認エラー: {e}")
    
    # 4. email_configファイル解析
    print("\n📋 4. email_configファイル解析")
    try:
        import email_config
        config_attrs = [attr for attr in dir(email_config) if not attr.startswith('_')]
        print(f"📊 設定項目: {config_attrs}")
        
        for attr in config_attrs:
            value = getattr(email_config, attr)
            if 'password' in attr.lower():
                print(f"  {attr}: {'設定済み' if value != 'YOUR_APP_PASSWORD_HERE' else '未設定'}")
            else:
                print(f"  {attr}: {value}")
                
    except Exception as e:
        print(f"❌ 設定確認エラー: {e}")
    
    # 5. 修正方針策定
    print("\n📋 5. 修正方針策定")
    print("🎯 解析結果に基づく修正方針:")
    print("1. run_daily_optimizationメソッドの正確な終了位置特定")
    print("2. email_content変数のスコープ確認")
    print("3. 適切な位置への実際メール送信コード挿入")
    print("4. 構文エラーを避ける安全な挿入方法")
    print("5. テスト実行による動作確認")
    
    # 6. 次回修正案の提示
    print("\n📋 6. 推奨修正案")
    print("🔧 段階的修正手順:")
    print("Step1: email_content変数の正確な位置特定")
    print("Step2: return文の正確な位置特定")
    print("Step3: 安全な挿入ポイントの決定")
    print("Step4: 最小限のコード挿入")
    print("Step5: 段階的テスト実行")
    
    print(f"\n🎉 完全構造解析完了 - {datetime.datetime.now()}")
    
    # 5分後に自動削除
    import threading
    def cleanup():
        import time
        time.sleep(300)
        try:
            os.remove(__file__)
        except:
            pass
    threading.Thread(target=cleanup, daemon=True).start()

if __name__ == "__main__":
    complete_structure_analysis()
