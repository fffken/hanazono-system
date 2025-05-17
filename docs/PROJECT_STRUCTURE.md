# HANAZONOソーラー蓄電システム自動最適化プロジェクト - 文書体系

## 文書階層構造 [v1.0, 2025-05-03]

1. **基本文書（マスタードキュメント）**
   - `PROJECT_MASTER.md` - プロジェクト全体のマスタードキュメント（統合ロードマップ+がベース）
   - `CRITICAL_NOTES.md` - 最重要事項と引き継ぎ情報

2. **ガイドライン**
   - `guidelines/CODING_STANDARDS.md` - コーディング規約
   - `guidelines/DEVELOPMENT_WORKFLOW.md` - 開発フロー
   - `guidelines/VERSION_CONTROL.md` - バージョン管理ルール

3. **リファレンス文書**
   - `references/INVERTER_REGISTERS.md` - インバーターレジスタ詳細
   - `references/PARAMETER_SETTINGS.md` - パラメーター設定確認表
   - `references/IMPLEMENTATION_DETAILS.md` - 実装詳細（補足資料パックがベース）

4. **バージョン履歴**
   - `versions/CHANGELOG.md` - 変更履歴
   - `versions/vX.Y.Z/` - 各バージョンごとのスナップショット

## 更新ルール [v1.0, 2025-05-03]

1. **文書更新プロセス**
   - 各文書は必ずバージョン番号と日付を含める
   - 重要な変更は`CRITICAL_NOTES.md`に記録
   - 全ての変更は`CHANGELOG.md`に記録

2. **バージョニングルール**
   - メジャー.マイナー.パッチ形式（例: v1.2.3）を使用
   - メジャー: 互換性を破壊する変更
   - マイナー: 後方互換性のある機能追加
   - パッチ: バグ修正や小さな調整

## 変更履歴

- 2025-05-03: 初期バージョン作成
