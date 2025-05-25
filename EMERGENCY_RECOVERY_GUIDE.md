# 緊急時完全復旧ガイド

## 🚨 システム停止時
```bash
git reset --hard HEAD
python3 main.py --daily-report
🚨 ファイル破損時
Copygit checkout HEAD -- *.py
bash scripts/perfect_save.sh
🚨 完全混乱時
Copygit log --oneline | head -5
git reset --hard [正常なコミットID]
🎯 復旧確認
Copypython3 main.py --daily-report
# "✅ メール送信成功" が表示されれば復旧完了
