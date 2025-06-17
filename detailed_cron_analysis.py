#!/usr/bin/env python3
# cronファイル内部構造詳細確認（完全非破壊的）
import datetime
import os
import ast
import importlib.util

def detailed_cron_analysis():
    """cronファイル内部構造詳細確認"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 cronファイル内部構造詳細確認開始 {timestamp}")
    print("=" * 70)
    
    cron_file = "abc_integration_fixed_final_20250616_231158.py"
    
    if not os.path.exists(cron_file):
        print(f"❌ cronファイル未発見: {cron_file}")
        return False
    
    # 1. ファイル内容解析
    print(f"📄 ファイル内容解析:")
    try:
        with open(cron_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f"  📊 総行数: {len(lines)}")
        print(f"  📊 文字数: {len(content)}")
        
        # クラス定義検索
        class_lines = [i for i, line in enumerate(lines) if line.strip().startswith('class ')]
        print(f"  📋 クラス定義: {len(class_lines)}個")
        
        for i in class_lines:
            class_line = lines[i].strip()
            print(f"    行{i+1}: {class_line}")
        
        # 関数定義検索
        func_lines = [i for i, line in enumerate(lines) if line.strip().startswith('def ')]
        print(f"  📋 関数定義: {len(func_lines)}個")
        
        # メール関連関数詳細検索
        mail_functions = []
        for i in func_lines:
            func_line = lines[i].strip()
            if any(keyword in func_line.lower() for keyword in ['mail', 'send', 'email']):
                mail_functions.append((i+1, func_line))
        
        print(f"  📧 メール関連関数: {len(mail_functions)}個")
        for line_num, func_line in mail_functions:
            print(f"    行{line_num}: {func_line}")
        
    except Exception as e:
        print(f"  ❌ ファイル解析エラー: {e}")
        return False
    
    # 2. 実際の実行テスト（import試行）
    print(f"\n🧪 実行テスト:")
    try:
        # モジュールとして読み込み
        spec = importlib.util.spec_from_file_location("cron_test", cron_file)
        if spec is None:
            print(f"  ❌ モジュール仕様作成失敗")
            return False
        
        cron_module = importlib.util.module_from_spec(spec)
        
        print(f"  ✅ モジュール作成成功")
        
        # 実際に実行（エラー確認のみ）
        try:
            spec.loader.exec_module(cron_module)
            print(f"  ✅ モジュール実行成功")
            
            # 利用可能な要素確認
            module_items = dir(cron_module)
            classes = [item for item in module_items if not item.startswith('_')]
            print(f"  📋 利用可能要素: {len(classes)}個")
            
            # クラスと関数を分類
            actual_classes = []
            actual_functions = []
            
            for item in classes:
                try:
                    obj = getattr(cron_module, item)
                    if isinstance(obj, type):
                        actual_classes.append(item)
                    elif callable(obj):
                        actual_functions.append(item)
                except:
                    pass
            
            print(f"  📋 実際のクラス: {actual_classes}")
            print(f"  📋 実際の関数: {actual_functions}")
            
            # メール機能確認
            mail_related = []
            for item in classes:
                if any(keyword in item.lower() for keyword in ['mail', 'send', 'email']):
                    mail_related.append(item)
            
            print(f"  📧 メール関連要素: {mail_related}")
            
            # クラス内メソッド確認
            for class_name in actual_classes:
                try:
                    class_obj = getattr(cron_module, class_name)
                    methods = [method for method in dir(class_obj) 
                             if not method.startswith('_') and callable(getattr(class_obj, method))]
                    print(f"  🔧 {class_name}メソッド: {methods[:10]}")  # 最初の10個
                    
                    # メール関連メソッド確認
                    mail_methods = [method for method in methods 
                                  if any(keyword in method.lower() for keyword in ['mail', 'send', 'email'])]
                    if mail_methods:
                        print(f"    📧 メール関連: {mail_methods}")
                except Exception as e:
                    print(f"    ❌ {class_name}メソッド確認エラー: {e}")
            
        except Exception as e:
            print(f"  ❌ モジュール実行エラー: {e}")
            print(f"  📋 エラー詳細: {str(e)}")
            
            # シンタックスエラーの可能性確認
            try:
                compile(content, cron_file, 'exec')
                print(f"  ✅ シンタックス正常")
            except SyntaxError as syntax_error:
                print(f"  ❌ シンタックスエラー: {syntax_error}")
                print(f"    行{syntax_error.lineno}: {syntax_error.text}")
            
    except Exception as e:
        print(f"  ❌ 実行テスト例外: {e}")
    
    # 3. main部分確認
    print(f"\n🎯 main部分確認:")
    main_lines = [i for i, line in enumerate(lines) if '__main__' in line]
    if main_lines:
        print(f"  ✅ main部分発見: {len(main_lines)}箇所")
        for line_num in main_lines:
            # main周辺の数行を表示
            start = max(0, line_num - 2)
            end = min(len(lines), line_num + 5)
            print(f"  📋 行{line_num+1}周辺:")
            for i in range(start, end):
                prefix = "  → " if i == line_num else "    "
                print(f"    {prefix}{i+1}: {lines[i]}")
    else:
        print(f"  ❌ main部分未発見")
    
    print(f"\n" + "=" * 70)
    print(f"🎯 cronファイル構造分析完了")
    
    return True

if __name__ == "__main__":
    detailed_cron_analysis()
