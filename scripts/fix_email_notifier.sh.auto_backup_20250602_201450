#!/bin/bash

# バックアップを作成
cp email_notifier.py email_notifier.py.bak

# データファイル検索関数を追加
sed -i '/class EmailNotifier:/a \
    def find_latest_data_file(self, target_date=None):\
        """\
        指定された日付のデータファイルを検索し、ない場合は最新のファイルを返す\
        \
        Args:\
            target_date: 検索する日付（YYYYMMDD形式、Noneの場合は前日）\
        \
        Returns:\
            ファイルパスと日付\
        """\
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")\
        if not os.path.exists(data_dir):\
            self.logger.error(f"データディレクトリが存在しません: {data_dir}")\
            return None, None\
        \
        # 対象日付の設定（指定がなければ前日）\
        if target_date is None:\
            yesterday = datetime.now() - timedelta(days=1)\
            target_date = yesterday.strftime("%Y%m%d")\
        \
        # 指定日のファイル検索\
        target_file = os.path.join(data_dir, f"data_{target_date}.json")\
        if os.path.exists(target_file):\
            return target_file, target_date\
        \
        # 指定日のファイルがない場合、全データファイルをリストアップ\
        self.logger.warning(f"日付 {target_date} のデータファイルが見つかりません: {target_file}")\
        \
        data_files = []\
        for file in os.listdir(data_dir):\
            if file.startswith("data_") and file.endswith(".json"):\
                try:\
                    date_str = file[5:-5]  # "data_YYYYMMDD.json" から日付部分を抽出\
                    # 日付形式が有効かチェック\
                    datetime.strptime(date_str, "%Y%m%d")\
                    data_files.append((file, date_str))\
                except ValueError:\
                    # 日付形式が無効な場合はスキップ\
                    continue\
        \
        if not data_files:\
            self.logger.error("利用可能なデータファイルがありません")\
            return None, None\
        \
        # 日付でソートして最新のものを取得\
        data_files.sort(key=lambda x: x[1], reverse=True)\
        latest_file = os.path.join(data_dir, data_files[0][0])\
        latest_date = data_files[0][1]\
        \
        self.logger.warning(f"最新の利用可能なデータを使用します: {latest_date}")\
        return latest_file, latest_date' email_notifier.py

# send_daily_report関数を修正
sed -i '/def send_daily_report/,/data_file = /c\
    def send_daily_report(self, date=None):\
        """日次レポートを送信する"""\
        try:\
            # メール設定の確認\
            if "email" not in self.settings or not self.settings["email"].get("smtp_server"):\
                self.logger.error("メール設定が不足しています")\
                return False\
                \
            # 日付の設定\
            if date is None:\
                yesterday = datetime.now() - timedelta(days=1)\
                date = yesterday.strftime("%Y%m%d")\
                \
            # データファイルを探す（ない場合は最新のものを使用）\
            data_file, actual_date = self.find_latest_data_file(date)\
            if data_file is None:\
                self.logger.warning(f"日付 {date} のデータが見つかりません")\
                return False\
                \
            # 日付が異なる場合は通知\
            use_fallback = (actual_date != date)\
            if use_fallback:\
                self.logger.warning(f"指定された日付 {date} のデータがないため、日付 {actual_date} のデータを使用します")' email_notifier.py

# 件名変更部分を修正
sed -i '/subject =/c\
            subject = f"🟡 LVYUANソーラー日次レポート {self._format_date_jp(actual_date)}"\
            if use_fallback:\
                subject = f"⚠️ LVYUANソーラー日次レポート {self._format_date_jp(actual_date)} (最新データ使用)"' email_notifier.py

# 実行権限を付与
chmod +x fix_email_notifier.sh
