#!/bin/bash
# HANAZONO詳細起動システム

case "$1" in
  detail)
    echo "🔍 HANAZONO詳細情報表示"
    echo "======================="
    
    # 全ファイル内容を完全表示
    for file in github_files/*.md; do
      if [ -f "$file" ]; then
        echo ""
        echo "📄 ファイル: $(basename $file)"
        echo "================================"
        cat "$file"
        echo ""
      fi
    done
    ;;
    
  status)
    echo "📊 システム状態詳細確認"
    if [ -f "empire_dashboard.sh" ]; then
      bash empire_dashboard.sh
    fi
    ps aux | grep python3 | grep -v grep
    ;;
    
  *)
    bash hanazono_complete_startup.sh
    ;;
esac
