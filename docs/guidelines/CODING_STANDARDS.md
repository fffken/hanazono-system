# コーディング規約

Version: 1.0.0
Last Updated: 2025-05-03

## Python コーディングスタイル [v1.0.0]

### 1. 基本ルール
- PEP 8に準拠する: https://peps.python.org/pep-0008/
- インデントはスペース4つ
- 最大行長は100文字
- 関数間には2行の空行
- メソッド間には1行の空行

### 2. 命名規則
- クラス: UpperCamelCase
- 関数・メソッド: snake_case
- 変数: snake_case
- 定数: UPPER_SNAKE_CASE
- プライベートメンバー: _leading_underscore

### 3. ドキュメント
- 全てのモジュール、クラス、関数にdocstringを記載
- docstringはGoogle形式を推奨

例:
```python
def function_name(param1, param2):
    """関数の概要説明

    詳細な説明（必要に応じて）

    Args:
        param1 (型): 説明
        param2 (型): 説明

    Returns:
        戻り値の型: 説明

    Raises:
        例外型: 説明
    """

### 4. バージョン管理
- 各ファイルにバージョン情報を含める
