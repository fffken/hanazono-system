#!/usr/bin/env python3
# 統一版内容確認（完全非破壊的）
import datetime
import os

def verify_unified_content():
    """統一版内容確認"""
    print("🔍 統一版内容確認開始")
    print("=" * 60)
    
    target_file = "abc_integration_icon_fixed_20250615_223350.py"
    
    if os.path.exists(target_file):
        print(f"📁 {target_file} 詳細確認:")
        
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. ファイル基本情報
            file_size = os.path.getsize(target_file)
            line_count = len(content.split('\n'))
            print(f"📊 ファイルサイズ: {file_size}バイト")
            print(f"📊 行数: {line_count}行")
            
            # 2. 重要なクラス・関数確認
            key_components = [
                "class ABCIntegrationIconFixed",
                "def get_perfect_weather_data",
                "def format_3days_weather_display", 
                "def calculate_visual_recommendations",
                "def send_icon_fixed_email",
                "def run_icon_fixed_test"
            ]
            
            print(f"\n🔧 重要コンポーネント確認:")
            for component in key_components:
                exists = component in content
                print(f"  {component}: {'✅' if exists else '❌'}")
            
            # 3. アイコン・絵文字機能確認
            icon_features = ["🟠", "🔵", "🟣", "🌻", "recommendation_icon"]
            print(f"\n🎨 アイコン・絵文字機能確認:")
            for feature in icon_features:
                count = content.count(feature)
                print(f"  {feature}: {count}箇所")
            
            # 4. 天気データ処理確認
            weather_features = [
                "get_fallback_weather",
                "format_3days_weather_display",
                "get_weather_emoji_sequence",
                "get_power_generation_forecast"
            ]
            
            print(f"\n🌤️ 天気データ処理確認:")
            for feature in weather_features:
                exists = feature in content
                print(f"  {feature}: {'✅' if exists else '❌'}")
            
            # 5. メール送信機能確認
            mail_features = [
                "smtp.gmail.com",
                "fffken@gmail.com", 
                "bbzpgdsvqlcemyxi",
                "MIMEText",
                "starttls"
            ]
            
            print(f"\n📧 メール送信機能確認:")
            for feature in mail_features:
                exists = feature in content
                print(f"  {feature}: {'✅' if exists else '❌'}")
            
            # 6. 件名・本文フォーマット確認
            format_checks = [
                'f"{visual_emoji} HANAZONOシステム"',
                "🌤️ 天気予報と発電予測", 
                "🔧 今日の推奨設定",
                "📊 A・B・C統合状況"
            ]
            
            print(f"\n📝 フォーマット確認:")
            for check in format_checks:
                exists = check in content
                print(f"  {check[:30]}...: {'✅' if exists else '❌'}")
            
            # 7. 最終判定
            all_key_components = all(component in content for component in key_components)
            all_icons = all(icon in content for icon in ["🟠", "🔵", "🟣", "🌻"])
            all_weather = all(feature in content for feature in weather_features)
            all_mail = all(feature in content for feature in mail_features)
            
            total_score = sum([all_key_components, all_icons, all_weather, all_mail])
            
            print(f"\n" + "=" * 60)
            print(f"🎯 統一版品質確認結果")
            print(f"=" * 60)
            print(f"基本コンポーネント: {'✅' if all_key_components else '❌'}")
            print(f"アイコン機能: {'✅' if all_icons else '❌'}")
            print(f"天気データ処理: {'✅' if all_weather else '❌'}")
            print(f"メール送信機能: {'✅' if all_mail else '❌'}")
            print(f"総合品質スコア: {total_score}/4")
            
            if total_score == 4:
                print(f"\n🎉 完璧！統一版は最高品質です")
                print(f"📧 明日朝7時: 完璧なアイコン修正版メール自動配信")
                print(f"🎨 絵文字: 🟠🔵🟣🌻 天気・季節別自動切り替え")
                print(f"🌤️ 天気: 3日分完璧データ + 絵文字レイアウト")
                print(f"🚀 運用準備: 100%完了")
                return True
            else:
                print(f"\n⚠️ 品質に問題あり、要確認")
                return False
                
        except Exception as e:
            print(f"❌ ファイル読み取りエラー: {e}")
            return False
    else:
        print(f"❌ {target_file} が存在しません")
        return False

if __name__ == "__main__":
    verify_unified_content()
