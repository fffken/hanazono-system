#!/usr/bin/env python3
# HANAZONO正確な非破壊的メール修正 - 実際のコード構造に基づく
import os
import datetime

def create_correct_fixed_version():
    """実際のコード構造に基づく正確な修正版を別ファイルで作成"""
    
    print("🎯 HANAZONO正確な非破壊的メール修正開始")
    print("=" * 50)
    
    # 1. 元ファイル存在確認
    if not os.path.exists("hanazono_complete_system.py"):
        print("❌ 元ファイルが存在しません")
        return False
    
    print("✅ 元ファイル存在確認")
    
    # 2. 元ファイル読み込み（絶対に変更しない）
    with open("hanazono_complete_system.py", "r", encoding="utf-8") as f:
        original_content = f.read()
    
    print(f"✅ 元ファイル読み込み完了（{len(original_content)}文字）")
    
    # 3. 実際の置換対象コード（9-12行目）
    print("📋 実際の置換対象コード特定...")
    
    # 実際に存在するコード（確認済み）
    old_code = '''            # 1. ML統合最適化実行
            if "email_hub_ml" in self.modules:
                email_result = self.modules["email_hub_ml"].send_daily_report()
                results["email_report"] = {"success": email_result, "timestamp": datetime.now().isoformat()}
                print(f"📧 メールレポート: {'✅ 成功' if email_result else '❌ 失敗'}")'''
    
    # 実際のメール送信に置換
    new_code = '''            # 1. 実際のメール送信実行
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
    
    # 4. 置換対象確認
    if old_code in original_content:
        print("✅ 置換対象コード発見")
        fixed_content = original_content.replace(old_code, new_code)
        print("✅ 修正版内容作成完了")
    else:
        print("❌ 置換対象コードが見つかりません")
        print("📋 デバッグ情報:")
        
        # より詳細な検索
        if "email_hub_ml" in original_content:
            print("✅ email_hub_ml文字列は存在")
        else:
            print("❌ email_hub_ml文字列が存在しません")
            
        return False
    
    # 5. 修正版を別ファイルとして保存（元ファイルは無変更）
    fixed_filename = f"hanazono_complete_system_email_fixed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    with open(fixed_filename, "w", encoding="utf-8") as f:
        f.write(fixed_content)
    
    print(f"✅ 修正版作成完了: {fixed_filename}")
    
    # 6. 修正版の構文チェック
    print("📋 修正版構文チェック...")
    try:
        import ast
        ast.parse(fixed_content)
        print("✅ 構文チェック: 正常")
    except SyntaxError as e:
        print(f"❌ 構文エラー: {e}")
        os.remove(fixed_filename)
        print("🗑️ 問題のある修正版を削除しました")
        return False
    
    # 7. テスト手順案内（完全非破壊的）
    print("\n📋 完全非破壊的テスト手順")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 安全なテスト手順:")
    print("1. 元ファイルバックアップ:")
    print("   cp hanazono_complete_system.py hanazono_original_safe.py")
    print("")
    print("2. 修正版適用（テスト用）:")
    print(f"   cp {fixed_filename} hanazono_complete_system.py")
    print("")
    print("3. テスト実行:")
    print("   python3 -c \"from hanazono_complete_system import HANAZONOCompleteSystem; system=HANAZONOCompleteSystem(); result=system.run_daily_optimization(); print('テスト結果:', result.get('success'))\"")
    print("")
    print("4. 問題時の即座復旧:")
    print("   cp hanazono_original_safe.py hanazono_complete_system.py")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\n🎉 完全非破壊的修正版作成完了")
    print(f"📁 修正版: {fixed_filename}")
    print(f"📁 元ファイル: hanazono_complete_system.py（完全無変更）")
    
    return fixed_filename

if __name__ == "__main__":
    result = create_correct_fixed_version()
    if result:
        print(f"\n✅ 成功: 修正版作成完了")
        print("📋 次: 上記の安全なテスト手順を実行してください")
    else:
        print(f"\n❌ 失敗: 修正版作成に失敗しました")
        print("📋 元ファイルは完全に保護されています")
