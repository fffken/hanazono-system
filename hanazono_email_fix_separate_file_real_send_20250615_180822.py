#!/usr/bin/env python3
# HANAZONO完全非破壊的メール修正 - 別ファイル作成方式
import os
import shutil
import datetime

def create_fixed_version():
    """元ファイルを変更せず、修正版を別ファイルとして作成"""
    
    print("🎯 HANAZONO完全非破壊的メール修正開始")
    print("=" * 50)
    
    # 1. 元ファイルの安全性確認
    if not os.path.exists("hanazono_complete_system.py"):
        print("❌ 元ファイルが存在しません")
        return False
    
    print("✅ 元ファイル存在確認")
    
    # 2. 元ファイル読み込み（変更しない）
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        original_content = f.read()
    
    print(f"✅ 元ファイル読み込み完了（{len(original_content)}文字）")
    
    # 3. 修正版内容作成（メモリ内で）
    print("📋 修正版内容作成中...")
    
    # run_daily_optimization内のemail_hub_ml部分を特定
    old_email_block = '''if "email_hub_ml" in self.modules:
            email_result = self.modules["email_hub_ml"].send_daily_report()
            results["email_report"] = {"success": email_result, "timestamp": datetime.now().isoformat()}
            print(f"📧 メールレポート: {'✅ 成功' if email_result else '❌ 失敗'}")'''
    
    # 実際のメール送信に置換
    new_email_block = '''# 実際のメール送信実行
        try:
            email_subject = f"最適化レポート {datetime.now().strftime('%Y年%m月%d日')}"
            email_body = f"""HANAZONOシステム日次最適化レポート
🌅 実行時刻: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}
🎯 最適化結果: 成功
📊 システム状態: OPERATIONAL
⚡ 6パラメーター最適化実行中
--- HANAZONOシステム自動レポート ---"""
            
            email_result_obj = self.send_actual_email(email_subject, email_body)
            email_success = email_result_obj.get('success', False)
            results["email_report"] = {"success": email_success, "timestamp": datetime.now().isoformat()}
            
            if email_success:
                if email_result_obj.get('mode') == 'actual':
                    print("📧 メールレポート: ✅ 実際送信成功")
                else:
                    print("📧 メールレポート: ✅ シミュレーション")
            else:
                print(f"📧 メールレポート: ❌ 送信失敗")
                
        except Exception as email_error:
            print(f"📧 メール送信エラー: {email_error}")
            results["email_report"] = {"success": False, "error": str(email_error), "timestamp": datetime.now().isoformat()}'''
    
    # 修正版内容作成
    if old_email_block in original_content:
        fixed_content = original_content.replace(old_email_block, new_email_block)
        print("✅ メール送信部分の修正版作成完了")
    else:
        print("❌ 対象部分が見つかりません")
        return False
    
    # 4. 修正版を別ファイルとして保存
    fixed_filename = f"hanazono_complete_system_fixed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    with open(fixed_filename, "w", encoding="utf-8") as f:
        f.write(fixed_content)
    
    print(f"✅ 修正版作成完了: {fixed_filename}")
    
    # 5. 修正版の構文チェック
    print("📋 修正版構文チェック...")
    try:
        import ast
        ast.parse(fixed_content)
        print("✅ 構文チェック: 正常")
    except SyntaxError as e:
        print(f"❌ 構文エラー: {e}")
        os.remove(fixed_filename)
        return False
    
    # 6. テスト手順案内
    print("\n📋 テスト手順案内")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 修正版テスト手順:")
    print(f"1. 元ファイルバックアップ: cp hanazono_complete_system.py hanazono_original_backup.py")
    print(f"2. 修正版テスト適用: cp {fixed_filename} hanazono_complete_system.py")
    print("3. テスト実行: python3 -c \"from hanazono_complete_system import HANAZONOCompleteSystem; system=HANAZONOCompleteSystem(); result=system.run_daily_optimization(); print('結果:', result.get('success'))\"")
    print("4. 問題時の復旧: cp hanazono_original_backup.py hanazono_complete_system.py")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\n🎉 完全非破壊的修正版作成完了")
    print(f"📁 修正版ファイル: {fixed_filename}")
    print(f"📁 元ファイル: hanazono_complete_system.py（無変更）")
    
    return fixed_filename

if __name__ == "__main__":
    result = create_fixed_version()
    if result:
        print(f"\n✅ 成功: {result}")
        print("📋 次: 上記テスト手順を実行してください")
    else:
        print("\n❌ 失敗: 修正版作成に失敗しました")
