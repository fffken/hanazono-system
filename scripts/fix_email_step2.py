import re

# 追加するコード
new_function = '''
    def find_latest_data_file(self, target_date=None):
        """
        指定された日付のデータファイルを検索し、ない場合は最新のファイルを返す
        
        Args:
            target_date: 検索する日付（YYYYMMDD形式、Noneの場合は前日）
            
        Returns:
            ファイルパスと日付
        """
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.exists(data_dir):
            self.logger.error(f"データディレクトリが存在しません: {data_dir}")
            return None, None
        
        # 対象日付の設定（指定がなければ前日）
        if target_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime("%Y%m%d")
        
        # 指定日のファイル検索
        target_file = os.path.join(data_dir, f"data_{target_date}.json")
        if os.path.exists(target_file):
            return target_file, target_date
        
        # 指定日のファイルがない場合、全データファイルをリストアップ
        self.logger.warning(f"日付 {target_date} のデータファイルが見つかりません: {target_file}")
        
        data_files = []
        for file in os.listdir(data_dir):
            if file.startswith("data_") and file.endswith(".json"):
                try:
                    date_str = file[5:-5]  # "data_YYYYMMDD.json" から日付部分を抽出
                    # 日付形式が有効かチェック
                    datetime.strptime(date_str, "%Y%m%d")
                    data_files.append((file, date_str))
                except ValueError:
                    # 日付形式が無効な場合はスキップ
                    continue
        
        if not data_files:
            self.logger.error("利用可能なデータファイルがありません")
            return None, None
        
        # 日付でソートして最新のものを取得
        data_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = os.path.join(data_dir, data_files[0][0])
        latest_date = data_files[0][1]
        
        self.logger.warning(f"最新の利用可能なデータを使用します: {latest_date}")
        return latest_file, latest_date
'''

# ファイル読み込み
with open('email_notifier.py', 'r') as f:
    content = f.read()

# クラス定義の後に関数を追加
class_pattern = r'class EmailNotifier:'
modified_content = re.sub(
    class_pattern, f'class EmailNotifier:{new_function}', content)

# 修正内容を保存
with open('email_notifier.py', 'w') as f:
    f.write(modified_content)

print("データファイル検索関数を追加しました")
