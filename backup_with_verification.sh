#!/bin/bash
BACKUP_DIR="verified_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
echo "🔄 検証付きバックアップ開始: $TIMESTAMP"
# 仮想環境の完全性チェック
python3 file_corruption_detector.py
if [ $? -eq 0 ]; then
    tar -czf "$BACKUP_DIR/verified_venv_$TIMESTAMP.tar.gz" venv/
    echo "✅ 検証済みバックアップ完了: verified_venv_$TIMESTAMP.tar.gz"
    # 古いバックアップ削除（3日以上古い）
    find "$BACKUP_DIR" -name "verified_venv_*.tar.gz" -mtime +3 -delete
else
    echo "❌ 仮想環境破損のためバックアップ中止"
    exit 1
fi
