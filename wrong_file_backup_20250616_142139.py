#!/usr/bin/env python3
# アイコン修正版ファイル復旧（完全非破壊的）
import datetime
import os
import glob

def recover_icon_fixed_file():
    """アイコン修正版ファイル復旧"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔧 アイコン修正版ファイル復旧開始 {timestamp}")
    print("=" * 60)
    
    target_file = "abc_integration_icon_fixed_20250615_223350.py"
    
    # 1. 現在のファイル状況確認
    print("📁 現在のファイル状況確認:")
    
    # アイコン関連ファイル検索
    icon_files = glob.glob("*icon_fixed*.py")
    abc_files = glob.glob("abc_integration*.py")
    
    print(f"アイコン関連ファイル: {len(icon_files)}個")
    for f in icon_files:
        print(f"  - {f}")
    
    print(f"ABC統合ファイル: {len(abc_files)}個")
    for f in abc_files[:5]:  # 最新5個まで表示
        print(f"  - {f}")
    
    # 2. 最新のアイコン修正版ファイル検索
    icon_candidates = [f for f in icon_files if "icon_fixed" in f and f.endswith(".py")]
    if icon_candidates:
        latest_icon_file = max(icon_candidates, key=lambda x: os.path.getctime(x))
        print(f"\n📋 最新アイコン修正版: {latest_icon_file}")
        
        # 3. ファイル内容確認（アイコン修正版の特徴確認）
        try:
            with open(latest_icon_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # アイコン修正版の特徴確認
            has_icon_features = all([
                "recommendation_icon" in content,
                "🟠" in content,
                "🔵" in content,
                "🟣" in content,
                "🌻" in content
            ])
            
            print(f"アイコン機能確認: {'✅ 完備' if has_icon_features else '❌ 不完全'}")
            
            if has_icon_features:
                # 4. 目標ファイル名にコピー
                try:
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ アイコン修正版ファイル復旧成功")
                    print(f"復旧ファイル: {target_file}")
                    
                    # 5. 復旧確認
                    if os.path.exists(target_file):
                        file_size = os.path.getsize(target_file)
                        print(f"✅ 復旧確認: {target_file} ({file_size}バイト)")
                        
                        # 6. 手動テスト実行準備
                        print(f"\n🧪 手動テスト準備完了:")
                        print(f"python3 {target_file}")
                        
                        return True
                    else:
                        print(f"❌ 復旧確認失敗")
                        return False
                        
                except Exception as e:
                    print(f"❌ ファイル復旧エラー: {e}")
                    return False
            else:
                print(f"❌ 最新ファイルにアイコン機能不完全")
                return False
                
        except Exception as e:
            print(f"❌ ファイル内容確認エラー: {e}")
            return False
    else:
        print(f"\n❌ アイコン修正版ファイル未発見")
        print(f"🔧 代替案: 最新のABC統合ファイルを使用")
        
        if abc_files:
            latest_abc_file = max(abc_files, key=lambda x: os.path.getctime(x))
            print(f"最新ABC統合ファイル: {latest_abc_file}")
            print(f"手動確認推奨: {latest_abc_file}")
        
        return False

if __name__ == "__main__":
    recover_icon_fixed_file()
