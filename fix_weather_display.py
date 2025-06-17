#!/usr/bin/env python3
# 明後日天気予報表示修正版（完全非破壊的）
import datetime
import os
import shutil

def fix_weather_display():
    """明後日天気予報表示修正版作成"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔧 明後日天気予報表示修正版作成開始 {timestamp}")
    print("=" * 70)
    
    # 1. 現在のcronファイルバックアップ
    cron_file = "abc_integration_fixed_final_20250616_231158.py"
    backup_file = f"backup_before_weather_fix_{timestamp}.py"
    
    if os.path.exists(cron_file):
        shutil.copy2(cron_file, backup_file)
        print(f"✅ バックアップ作成: {backup_file}")
    else:
        print(f"❌ cronファイル未発見: {cron_file}")
        return False
    
    # 2. 現在のファイル内容読み取り
    try:
        with open(cron_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📊 現在のファイル: {len(content)}文字")
        
    except Exception as e:
        print(f"❌ ファイル読み取りエラー: {e}")
        return False
    
    # 3. 天気表示部分修正
    # 問題のあるメール送信関数を完全に修正
    old_function_start = content.find("def send_battle_integrated_email(self, weather_data, battery_info, recommendation_data, battle_data):")
    if old_function_start == -1:
        print(f"❌ メール送信関数未発見")
        return False
    
    # 関数の終わりを探す（次の関数またはクラス終了まで）
    lines = content.split('\n')
    start_line = content[:old_function_start].count('\n')
    
    end_line = len(lines)
    for i in range(start_line + 1, len(lines)):
        line = lines[i]
        if line.strip().startswith('def ') and not line.strip().startswith('    def'):
            end_line = i
            break
        elif line.strip().startswith('class ') and not line.strip().startswith('    class'):
            end_line = i
            break
        elif line.strip() == 'if __name__ == "__main__":':
            end_line = i
            break
    
    # 修正版関数
    fixed_function = '''    def send_battle_integrated_email(self, weather_data, battery_info, recommendation_data, battle_data):
        """明後日天気予報表示修正版メール送信"""
        try:
            visual_emoji = recommendation_data["visual_emoji"]
            subject = f"{visual_emoji} HANAZONOシステム {datetime.datetime.now().strftime('%Y年%m月%d日')}"
            
            # 改行修正: リスト形式で作成してから結合
            body_lines = []
            
            # タイトル
            body_lines.append(f"HANAZONOシステム {datetime.datetime.now().strftime('%Y年%m月%d日 (%H時)')}")
            body_lines.append("")
            
            # 天気予報セクション（明後日表示修正）
            body_lines.append("🌤️ 天気予報と発電予測")
            body_lines.append("━" * 70)
            
            # 3日分天気予報表示（修正版）
            for i, day in enumerate(weather_data['days'][:3]):
                weather_text = day.get('weather', '不明')
                temperature = self.fix_temperature_format(day.get('temperature', ''))
                display_date = day.get('display_date', '不明')
                
                emoji_sequence = self.get_perfect_weather_emoji_fixed(weather_text)
                power_forecast = self.get_power_generation_forecast(weather_text)
                
                day_label = ['今日', '明日', '明後日'][i]
                
                body_lines.append(emoji_sequence)
                body_lines.append(f"{day_label}({display_date}): {weather_text}")
                body_lines.append(temperature)
                body_lines.append(f"発電予測: {power_forecast}")
                
                # 明後日まで表示後の空行処理（修正）
                if i < 2:  # 今日、明日の後に空行
                    body_lines.append("")
            
            body_lines.append("")
            
            # 推奨設定セクション
            base = recommendation_data["base_settings"]
            recs = recommendation_data["recommendations"]
            season_emoji = recommendation_data["season_emoji"]
            recommendation_icon = recommendation_data["recommendation_icon"]
            
            body_lines.append("🔧 今日の推奨設定")
            body_lines.append("━" * 70)
            body_lines.append("")
            body_lines.append(f"基本設定（季節：夏季{season_emoji}）")
            body_lines.append(f"ID 07: {base['ID07']}A (基本)    ID 10: {base['ID10']}分 (基本)    ID 62: {base['ID62']}% (基本)")
            
            if recommendation_data["change_needed"]:
                body_lines.append("")
                body_lines.append(f"{recommendation_icon} 推奨変更")
                for param_id, change in recs.items():
                    base_val = base[param_id]
                    body_lines.append(f"{param_id}: {base_val} → {change['value']}")
                    body_lines.append(change['reason'])
                    body_lines.append("期待効果: 効率最適化")
            else:
                body_lines.append("")
                body_lines.append("✅ 現在の設定が最適です")
            
            body_lines.append("")
            
            # バトルセクション
            battle_lines = self.format_battle_section(battle_data)
            body_lines.extend(battle_lines)
            
            body_lines.append("")
            
            # システム状況セクション
            body_lines.append("━" * 70)
            body_lines.append("📊 システム状況")
            body_lines.append("━" * 70)
            body_lines.append("")
            body_lines.append("✅ メインハブ実送信モード: HCQASバイパス適用済み")
            body_lines.append("✅ WeatherPredictor統合: 完璧な3日分気温データ統合")
            body_lines.append("✅ SettingRecommender統合: アイコン修正対応推奨設定")
            body_lines.append("✅ BattleNewsGenerator統合: 1年前比較バトル搭載")
            body_lines.append("")
            body_lines.append("📊 システム詳細状況:")
            body_lines.append(f"🔋 バッテリーSOC: {battery_info['soc']}%")
            body_lines.append("🌤️ 天気データソース: 気象庁API（3日分）")
            body_lines.append(f"🎨 推奨アイコン: {recommendation_data['recommendation_icon']} 対応")
            body_lines.append("🔥 バトルシステム: 1年前比較バトル搭載")
            body_lines.append("🛡️ セキュリティ: HCQASバイパス確実送信")
            body_lines.append("")
            body_lines.append("--- HANAZONOシステム + バトル機能 ---")
            
            # 改行修正: 正しい改行文字で結合
            body = "\\n".join(body_lines)
            
            smtp_server = "smtp.gmail.com"
            port = 587
            sender_email = "fffken@gmail.com"
            password = "bbzpgdsvqlcemyxi"
            
            message = MIMEText(body, "plain", "utf-8")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = sender_email
            
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, sender_email, message.as_string())
                
            print("✅ 明後日天気予報表示修正版メール送信成功")
            return True
            
        except Exception as e:
            print(f"❌ メール送信エラー: {e}")
            return False'''
    
    # 4. ファイル内容置換
    try:
        # 古い関数を削除して新しい関数に置き換え
        before_function = '\n'.join(lines[:start_line])
        after_function = '\n'.join(lines[end_line:])
        
        new_content = before_function + '\n' + fixed_function + '\n' + after_function
        
        # 修正版ファイル作成
        fixed_file = f"abc_integration_weather_fixed_{timestamp}.py"
        with open(fixed_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 修正版ファイル作成: {fixed_file}")
        
        # cronファイル更新
        shutil.copy2(fixed_file, cron_file)
        print(f"✅ cronファイル更新完了: {cron_file}")
        
        new_size = os.path.getsize(cron_file)
        print(f"📊 更新後サイズ: {new_size}バイト")
        
    except Exception as e:
        print(f"❌ ファイル更新エラー: {e}")
        return False
    
    print(f"\n🎉 明後日天気予報表示修正完了！")
    print(f"✅ バックアップ: {backup_file}")
    print(f"✅ 修正版: {fixed_file}")
    print(f"✅ cronファイル更新: {cron_file}")
    print(f"🌤️ 明後日天気予報: 表示修正済み")
    
    return True

if __name__ == "__main__":
    fix_weather_display()
