#!/bin/bash
# 進行管理システム バージョン管理ツール

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
BACKUP_DIR="system_backups"

create_backup() {
    echo -e "${YELLOW}システムバックアップを作成中...${NC}"
    
    mkdir -p $BACKUP_DIR
    backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR/$backup_name
    
    # 重要ファイルをバックアップ
    for file in scripts/master_progress_controller.sh scripts/setup_auto_update.sh PROGRESS_SYSTEM_VERSION.md; do
        if [ -f "$file" ]; then
            cp "$file" "$BACKUP_DIR/$backup_name/"
            echo "  ✅ $file をバックアップしました"
        fi
    done
    
    echo -e "${GREEN}バックアップ完了: $BACKUP_DIR/$backup_name${NC}"
    echo "$backup_name" > $BACKUP_DIR/latest_backup.txt
}

update_version() {
    echo -e "${YELLOW}バージョン情報を更新中...${NC}"
    
    # 現在のバージョンを取得
    if [ -f "PROGRESS_SYSTEM_VERSION.md" ]; then
        current_version=$(grep "現在のバージョン" PROGRESS_SYSTEM_VERSION.md | cut -d: -f2 | tr -d ' ')
        version_number=$(echo $current_version | cut -d. -f2)
        new_version="v1.$((version_number + 1))"
    else
        new_version="v1.0"
    fi
    
    # バージョンファイルを更新
    cat > PROGRESS_SYSTEM_VERSION.md << VERSION_EOF
# 進行管理システム バージョン情報

**現在のバージョン**: $new_version
**最終更新**: $TIMESTAMP
**作成者**: AI Assistant + User
**目的**: AIセッション間完全記憶継承システム

## バージョン履歴
- $new_version ($TIMESTAMP): システム更新
- v1.0 (2025-05-21): 初期バージョン作成

## システム構成
1. master_progress_controller.sh - メインコントローラー
2. setup_auto_update.sh - 自動更新設定  
3. update_system_manual.md - 更新マニュアル
4. version_manager.sh - バージョン管理

## 更新方法
詳細は docs/update_system_manual.md を参照してください
VERSION_EOF
    
    echo -e "${GREEN}バージョンを $new_version に更新しました${NC}"
}

restore_backup() {
    echo -e "${YELLOW}バックアップから復元中...${NC}"
    
    if [ ! -f "$BACKUP_DIR/latest_backup.txt" ]; then
        echo -e "${RED}復元可能なバックアップが見つかりません${NC}"
        return 1
    fi
    
    latest_backup=$(cat $BACKUP_DIR/latest_backup.txt)
    
    if [ -d "$BACKUP_DIR/$latest_backup" ]; then
        cp $BACKUP_DIR/$latest_backup/* ./ 2>/dev/null
        cp $BACKUP_DIR/$latest_backup/master_progress_controller.sh scripts/ 2>/dev/null
        cp $BACKUP_DIR/$latest_backup/setup_auto_update.sh scripts/ 2>/dev/null
        
        echo -e "${GREEN}バックアップ $latest_backup から復元完了${NC}"
    else
        echo -e "${RED}バックアップディレクトリが見つかりません${NC}"
        return 1
    fi
}

show_status() {
    echo -e "${BLUE}=== 進行管理システム 状態確認 ===${NC}"
    
    if [ -f "PROGRESS_SYSTEM_VERSION.md" ]; then
        echo -e "${GREEN}現在のバージョン:${NC}"
        grep "現在のバージョン" PROGRESS_SYSTEM_VERSION.md
        grep "最終更新" PROGRESS_SYSTEM_VERSION.md
    else
        echo -e "${RED}バージョン情報ファイルが見つかりません${NC}"
    fi
    
    echo -e "\n${GREEN}システムファイル状況:${NC}"
    for file in scripts/master_progress_controller.sh scripts/setup_auto_update.sh; do
        if [ -f "$file" ]; then
            echo "  ✅ $file"
        else
            echo "  ❌ $file (見つかりません)"
        fi
    done
    
    echo -e "\n${GREEN}利用可能なバックアップ:${NC}"
    if [ -d "$BACKUP_DIR" ]; then
        ls -1 $BACKUP_DIR/ | grep backup_ | tail -3
    else
        echo "  バックアップなし"
    fi
}

case "${1:-help}" in
    "backup")
        create_backup
        ;;
    "update")
        update_version
        ;;
    "restore")
        restore_backup
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        echo "使用方法:"
        echo "  $0 backup  - システムのバックアップを作成"
        echo "  $0 update  - バージョン情報を更新"
        echo "  $0 restore - 最新バックアップから復元"
        echo "  $0 status  - システム状態を確認"
        ;;
esac
