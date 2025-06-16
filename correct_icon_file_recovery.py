#!/usr/bin/env python3
# 正しいアイコン修正版ファイル復旧（完全非破壊的）
import datetime
import os
import shutil

def recover_correct_icon_fixed_file():
    """正しいアイコン修正版ファイル復旧"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔧 正しいアイコン修正版ファイル復旧開始 {timestamp}")
    print("=" * 60)
    
    target_file = "abc_integration_icon_fixed_20250615_223350.py"
    source_file = "abc_integration_icon_fixed_20250615_223341.py"
    
    # 1. 現在の間違ったファイルバックアップ
    wrong_backup = f"wrong_file_backup_{timestamp}.py"
    if os.path.exists(target_file):
        shutil.copy2(target_file, wrong_backup)
        print(f"📋 間違ったファイルバックアップ: {wrong_backup}")
    
    # 2. 正しいソースファイル確認
    if os.path.exists(source_file):
        print(f"✅ 正しいソースファイル発見: {source_file}")
        
        # 3. ソースファイル内容確認（アイコン修正版の特徴確認）
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # メール送信システムの特徴確認
            has_mail_features = all([
                "send_icon_fixed_email" in content,
                "ABCIntegrationIconFixed" in content,
                "smtp.gmail.com" in content,
                "recommendation_icon" in content
            ])
            
            print(f"メール機能確認: {'✅ 完備' if has_mail_features else '❌ 不完全'}")
            
            if has_mail_features:
                # 4. 正しいファイルを目標ファイル名にコピー
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ 正しいアイコン修正版ファイル復旧成功")
                print(f"復旧ファイル: {target_file}")
                
                # 5. 復旧確認
                if os.path.exists(target_file):
                    file_size = os.path.getsize(target_file)
                    print(f"✅ 復旧確認: {target_file} ({file_size}バイト)")
                    
                    # 6. 内容再確認
                    with open(target_file, 'r', encoding='utf-8') as f:
                        new_content = f.read()
                    
                    if "run_icon_fixed_test" in new_content:
                        print(f"✅ メール送信機能確認済み")
                        print(f"\n🧪 正しいテスト実行準備完了:")
                        print(f"python3 {target_file}")
                        return True
                    else:
                        print(f"❌ メール送信機能確認失敗")
                        return False
                else:
                    print(f"❌ 復旧確認失敗")
                    return False
            else:
                print(f"❌ ソースファイルにメール機能不完全")
                return False
                
        except Exception as e:
            print(f"❌ ファイル内容確認エラー: {e}")
            return False
    else:
        print(f"❌ 正しいソースファイル未発見: {source_file}")
        print(f"🔧 利用可能ファイル一覧:")
        
        import glob
        all_files = glob.glob("abc_integration*.py")
        for f in all_files:
            print(f"  - {f}")
        
        return False

if __name__ == "__main__":
    recover_correct_icon_fixed_file()
