# HANAZONOシステム 重要ルール・ポリシー集 v1.0

**最終更新**: 2025-06-01
**バージョン**: 1.0
**ルール追加方法**: 最下部の「新規ルール追加テンプレート」を使用

## 🚨 絶対遵守ルール（Lv.5 - 最重要）

### Rule-001: 黄金バージョン保護の法則
- **作業前に必ず黄金バージョン確保**
- email_notifier_v2_1.py (26331バイト) は絶対変更禁止
- 機能テスト実行後に変更適用
- サイズ不一致時は即座復旧

### Rule-002: AI記憶継続の法則
- 新AIセッション開始時は `kioku` 実行必須
- 記憶システムの破損は最優先修復
- セッション間の文脈断絶を根絶

### Rule-003: 非破壊的作業の法則
- **新変更前に必ず現在状態を保存**
- 途中保存の自動化実装
- 保存なしの変更作業を物理的に禁止
- バックアップなしでの作業開始禁止

## ⚡ 高優先ルール（Lv.4 - 重要）

### Rule-004: プロジェクト根幹理解の法則
- **ソーラー蓄電システム設定**: `docs/HANAZONO-SYSTEM-SETTINGS.md` 必読
- **プロジェクトロードマップ**: `docs/ROADMAP_COMPLETE.md` 必読
- 根幹理解なしでの機能変更禁止

### Rule-005: Git管理の法則
- Git状態確認は作業開始の必須条件
- 大規模変更前の自動バックアップ
- コミットメッセージに絵文字必須

### Rule-006: コピペ最適化の法則
- **━━━ ここからコピー ━━━** と **━━━ ここまでコピー ━━━** 必須
- ターミナル直接: 30-40行以内
- nanoエディター: 40行超過時
- 人力修正作業の完全排除

## 🔧 技術ルール（Lv.3 - 標準）

### Rule-007: 季節設定管理の法則
- タイプB（省管理型）を基本運用
- 冬季/春秋季/夏季の3区分設定
- インバーターパラメーター: ID 07,10,62

### Rule-008: GitHub連携の法則
- リモート同期の確実実行
- raw.githubusercontent.com接続保証
- 自動fetch・push機能維持

### Rule-009: 自動化優先の法則
- 手動作業は自動化対象
- 「時短」「効率」による判断
- ゼロ思考負荷の実現

## 🎯 開発哲学（Lv.2 - 指針）

### Rule-010: ゼロ思考負荷の法則
- 人間は「何をしたいか」のみ伝達
- システムが「どうやるか」を自動判断
- 創造性と判断力に完全集中

### Rule-011: 完全継承の法則
- AIの記憶喪失問題根絶
- プロジェクト断絶の永久防止
- 累積学習による進化継続

## 📋 ルール管理システム

### ルール追加プロセス
1. 最下部テンプレートを使用
2. 重要度レベル設定（Lv.1-5）
3. Rule-XXX番号を採番
4. 即座に`kioku`で記憶更新

### ルール優先度
- **Lv.5**: 絶対遵守（違反でシステム破綻）
- **Lv.4**: 高優先（違反で重大影響）
- **Lv.3**: 標準（違反で品質低下）
- **Lv.2**: 指針（推奨事項）
- **Lv.1**: 補助（参考情報）

---

## 🆕 新規ルール追加テンプレート

```markdown
### Rule-XXX: [ルール名]
**重要度**: Lv.X
**分類**: [絶対遵守/高優先/技術/哲学]
**内容**: 
- [ルール詳細1]
- [ルール詳細2]
**理由**: [なぜこのルールが必要か]
**違反時の影響**: [違反した場合の問題]
