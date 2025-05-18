# HANAZONOシステム 引き継ぎパック
作成日時: Sat 17 May 21:19:28 JST 2025

## 1. 基本引き継ぎ情報
# HANAZONOシステム引き継ぎ情報

## 基本情報
- **プロジェクト**: HANAZONOシステム
- **目的**: Raspberry Pi Zero 2 WでLVYUAN SPI-10K-Uを自動最適化
- **主要機能**: 15分毎データ収集、1日2回レポートメール送信

## 引き継ぎ手順
1. 新しいチャットセッションを開始
2. このファイル(PROJECT_HANDOVER.md)の内容を共有
3. `bash scripts/github_efficiency.sh`の実行結果を共有
4. 上記情報をもとに作業を開始

## プロジェクト優先事項
1. GitHub効率連携によるクレジット消費抑制
2. 変更管理プロセス徹底
3. 完全な引き継ぎシステム構築

## 引き継ぎツール使用方法

### 基本のプロジェクト状態確認
bash scripts/github_efficiency.sh


### ファイルへの直接リンク生成
bash scripts/generate_raw_links.sh


### ファイル変更前のバックアップ
bash scripts/backup_file.sh <ファイル名>


## AIとの効率的な連携方法
1. 新しいチャットセッションを開始
2. PROJECT_HANDOVER.mdの内容を共有
3. github_efficiency.shの実行結果を共有
4. 必要に応じてgenerate_raw_links.shの結果も共有

## 容量監視と自動引き継ぎプロンプト

AIとの対話において、チャット容量を効率的に管理し、円滑な引き継ぎを実現するためのルール：

1. 50%以上の容量使用時には、すべての回答の最後に使用率と時刻を表示
2. 容量使用率に応じた警告表示：
   - 50%以上：（タスクリスト使用率：約〜% | ℹ️ 半分を超えました）
   - 70%以上：（タスクリスト使用率：約〜% | ⚠️ 容量の70%を超えています）
   - 80%以上：（タスクリスト使用率：約〜% | ⚠️ 容量が80%を超えています）
   - 85%以上：（タスクリスト使用率：約〜% | 🚨 警告：容量が85%を超えています）
   - 90%以上：自動的に引き継ぎプロンプトを生成し、新しい対話の開始を促す
   - 95%以上：緊急警告と即時の引き継ぎプロンプト生成

この仕組みにより、対話が中断されることなく、継続的な作業が可能になります。

## 2. GitHub状態情報
=== HANAZONOシステム GitHub効率連携 Sat 17 May 21:19:28 JST 2025 ===
## 基本リポジトリ情報
origin	git@github.com:fffken/hanazono-system.git (fetch)
origin	git@github.com:fffken/hanazono-system.git (push)
* main 28f0d51 更新: Raw URL生成スクリプト（重要ドキュメント追加）
## 最新の変更を確認
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   email_notifier.py
	modified:   main.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.github/
	.gitignore
	CONTRIBUTING.md
	HANDOVER_PROMPT.md
	HANDOVER_PROMPT_FINAL.md
	HANDOVER_PROMPT_v2.md
	add_extract_battery_data.py
	ast_fix_indentation.py
	backup_and_change.sh
	collect_daily_data.py
	config.py
	current_email_notifier.py
	data/
	data_util.py
	email_notification.py
	email_notification_new.py
	email_notifier_may10.py
	handover_pack.md
	logger.py
	lvyuan_registers.py
	main.py.20250503
	main.py.20250503_settings_complete
	meta_issue_template.md
	modules/
	raw_links.md
	report_generator.py
	run_daily_report.sh
	scripts/fix_dates.sh
	scripts/fix_docstring_and_indent.py
	scripts/fix_email_notifier.sh
	scripts/fix_email_step1.sh
	scripts/fix_email_step2.py
	scripts/fix_email_step3.py
	scripts/fix_indentation.sh
	scripts/fix_script.sh
	scripts/fix_weather_methods.sh
	scripts/generate_handover.sh
	scripts/handover/
	scripts/handover_part1.sh
	scripts/handover_part2.sh
	scripts/organize_files.sh
	scripts/project_status.sh
	scripts/restore_email_template.sh
	season_detector.py
	settings.json
	settings_editor.py
	settings_recommender.py
	setup.py
	solar_control_scheduler.py
	specs/modbus/lvyuan_spi_10k_registers.md
	specs/modbus/srne_registers_clean.md
	start.sh
	tests/
	write_and_verify.py

no changes added to commit (use "git add" and/or "git commit -a")
## コアファイル情報
main.py: 最終更新 2025-05-13, 326 行
  主要関数:
    21:def collect_data():
    62:def send_daily_report():
    167:def check_cron_job():
    212:def setup_logger():
    257:def main():
email_notifier.py: 最終更新 2025-05-13, 600 行
  主要関数:
    20:    def __init__(self, config, logger):
    39:    def _get_weather_emoji(self, condition):
    66:    def _parse_weather_components(self, weather_text):
    92:    def _format_weather_emojis(self, weather_text):
    116:    def _format_weather_line(self, weather_text):
settings_manager.py: 最終更新 2025-05-10, 124 行
  主要関数:
    14:    def __new__(cls):
    21:    def _load_settings(self):
    35:    def save_settings(self):
    61:    def get_inverter_parameters(self):
    65:    def get_season_settings(self, season, setting_type):
## README概要
# HANAZONOシステム

HANAZONOシステムは、Raspberry Pi Zero 2 W上で動作するソーラー蓄電システム(LVYUAN SPI-10K-U)の自動最適化ソリューションです。

## 機能
- 15分ごとのデータ収集
- 1日2回（7時・23時）のレポートメール送信
- ソーラー発電・消費の最適化

## プロジェクト状態
## プロジェクト状態
# HANAZONOシステム プロジェクト状態

## 概要
- **プロジェクト名**: HANAZONOシステム
- **目的**: Raspberry Pi上でのソーラー蓄電システムの自動最適化
- **現在のフェーズ**: 開発プロセス改善・安定化フェーズ
- **最終更新**: $(date +%Y-%m-%d)

## 主要コンポーネント状態
| コンポーネント | 状態 | 最終更新 | 注意点 |
|--------------|------|---------|--------|
| main.py | 安定 | 2025-05-13 | コマンドライン引数処理完了 |
| email_notifier.py | 要改善 | 2025-05-17 | デバッグ出力追加中 |
| lvyuan_collector.py | 安定 | 2025-05-10 | データ収集モジュール |
| settings_manager.py | 安定 | 2025-05-10 | 設定管理クラス |

## 現在の開発状況
- **完了タスク**:
  1. 基本的なデータ収集システムの構築
  2. メール通知の基本機能実装
## 引き継ぎ情報 (PROJECT_HANDOVER.md)
引き継ぎ情報ファイルが存在します。新しいセッションでこのファイルを共有してください。
## プロジェクト履歴
28f0d51 更新: Raw URL生成スクリプト（重要ドキュメント追加）
8d48ceb 追加: 完全版ロードマップ文書（PDF代替）
eda23d5 追加: 重要プロジェクト情報抽出スクリプト
d5bd57c 追加: プロジェクトドキュメント
fe5f0fe 追加: 引き継ぎ情報一括生成スクリプト


このスクリプトの出力結果をコピーして、AIに共有することで効率的な支援を受けられます

## 3. 重要プロジェクト情報
以下の情報を取得するには:
```bash
bash scripts/get_essential_info.sh
```

## 4. ファイル直接リンク
# HANAZONOシステム 重要ファイル直接リンク

## コードファイル
- [main.py](https://github.com/fffken/hanazono-system/raw/main/main.py)
- [email_notifier.py](https://github.com/fffken/hanazono-system/raw/main/email_notifier.py)
- [settings_manager.py](https://github.com/fffken/hanazono-system/raw/main/settings_manager.py)

## 重要ドキュメント
- [完全版ロードマップ](https://github.com/fffken/hanazono-system/raw/main/docs/ROADMAP_COMPLETE.md)
- [プロジェクトマスター](https://github.com/fffken/hanazono-system/raw/main/docs/PROJECT_MASTER.md)
- [重要注意事項](https://github.com/fffken/hanazono-system/raw/main/docs/CRITICAL_NOTES.md)

## 引き継ぎリソース
- [プロジェクト状態](https://github.com/fffken/hanazono-system/raw/main/PROJECT_STATUS.md)
- [引き継ぎ情報](https://github.com/fffken/hanazono-system/raw/main/PROJECT_HANDOVER.md)
