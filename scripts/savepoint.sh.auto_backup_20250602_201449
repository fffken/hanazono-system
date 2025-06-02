#!/bin/bash
save() {
    git add .; git commit -m "🔒 セーフポイント: $1 - $(date +%H:%M)"
    echo "✅ セーフポイント: $1"
}
restore() {
    git reset --hard HEAD; echo "🔄 復旧完了"
}
