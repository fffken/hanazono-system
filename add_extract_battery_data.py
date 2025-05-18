#!/usr/bin/env python3
import re

# email_notifier.pyファイルを読み込む
with open('email_notifier.py', 'r') as f:
    content = f.read()

# _extract_battery_data メソッドの定義
extract_battery_data_method = '''
    def _extract_battery_data(self, data):
        """
        JSONデータからバッテリー状態情報を抽出します。
        
        データファイルのJSON構造に基づいて、バッテリーのSOC、電圧、電流などを
        抽出して辞書形式で返します。
        
        Args:
            data (dict/list): データファイルから読み込んだJSONデータ
            
        Returns:
            dict: 以下のキーを持つバッテリー情報辞書
                - soc: バッテリー残量(%)
                - voltage: バッテリー電圧(V)
                - current: バッテリー電流(A)
                - power: バッテリー電力(W)
                - status: バッテリー状態
        """
        # 初期値として全てのデータ項目をNoneに設定
        battery_data = {
            "soc": None,
            "voltage": None,
            "current": None,
            "power": None,
            "status": None
        }
        
        try:
            # データ形式の確認とパラメータへのアクセス
            if isinstance(data, list) and len(data) > 0:
                # リスト形式の場合は最初の項目を使用
                data_item = data[0]
                if "parameters" in data_item and isinstance(data_item["parameters"], dict):
                    params = data_item["parameters"]
                    
                    # SOC
                    if "0x0100" in params:
                        battery_data["soc"] = params["0x0100"].get("value")
                    
                    # 電圧
                    if "0x0101" in params:
                        battery_data["voltage"] = params["0x0101"].get("value")
                    
                    # 電流
                    if "0x0102" in params:
                        battery_data["current"] = params["0x0102"].get("value")
                    
                    # 状態（もし利用可能なら）
                    if "0x020E" in params:
                        battery_data["status"] = params["0x020E"].get("formatted_value")
                    
                    # 電力は電圧×電流で計算（電流データが異常値でなければ）
                    if battery_data["voltage"] is not None and battery_data["current"] is not None:
                        current = battery_data["current"]
                        # 電流の値が異常に大きい場合は計算しない
                        if -1000 <= current <= 1000:  # 妥当な範囲内のみ
                            battery_data["power"] = battery_data["voltage"] * current
            
            # 処理結果のログ出力（デバッグ用）
            self.logger.debug(f"バッテリーデータ抽出結果: {battery_data}")
            
            return battery_data
            
        except Exception as e:
            # 例外発生時はエラーをログに記録して初期値を返す
            self.logger.error(f"バッテリーデータ抽出中にエラーが発生しました: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return battery_data
'''

# _extract_battery_data メソッドがすでに存在するか確認
if "_extract_battery_data" in content:
    # 既存のメソッドを新しいものに置き換え
    pattern = r'def _extract_battery_data\(self, data\):.*?(?=\n    def |$)'
    content = re.sub(pattern, extract_battery_data_method.strip(), content, flags=re.DOTALL)
else:
    # クラス内の適切な位置に新しいメソッドを追加
    # 例えば、generate_notes_html メソッドの後に追加
    pattern = r'def _generate_notes_html\(self.*?\n        return ""\n'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, lambda m: m.group(0) + extract_battery_data_method, content, flags=re.DOTALL)
    else:
        # 別の位置を試す、クラスの最後
        pattern = r'(class EmailNotifier:.*?)$'
        content = re.sub(pattern, lambda m: m.group(1) + extract_battery_data_method, content, flags=re.DOTALL)

# 変更内容をファイルに書き込む
with open('email_notifier.py', 'w') as f:
    f.write(content)

print("_extract_battery_data メソッドが正常に追加/更新されました。")
