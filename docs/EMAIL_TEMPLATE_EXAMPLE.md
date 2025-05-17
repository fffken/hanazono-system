# メール通知テンプレート例（5月10日成功バージョン）

## メールタイトル
HANAZONOシステム状態レポート 2025年5月10日(土) (23時)

## メール本文（HTML）
```html
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; }
    th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    .power-info { background-color: #f2f2f2; padding: 10px; }
  </style>
</head>
<body>
  <h2>HANAZONOシステム状態レポート</h2>
  <p>2025年5月10日(土) 23時00分</p>
  
  <h3>電力情報</h3>
  <div class="power-info">
    <table>
      <tr><td>バッテリーSOC</td><td>78%</td></tr>
      <tr><td>発電電力</td><td>0W</td></tr>
      <tr><td>消費電力</td><td>420W</td></tr>
      <tr><td>グリッド電力</td><td>0W</td></tr>
    </table>
  </div>
  
  <h3>天気予報</h3>
  <p>🌙 今日: 晴れ 15℃/22℃</p>
  <p>☀️ 明日: 晴れ 16℃/24℃</p>
  
  <h3>システム状態</h3>
  <p>正常運用中</p>
</body>
</html>
