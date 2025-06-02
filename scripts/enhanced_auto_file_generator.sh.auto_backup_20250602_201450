#!/bin/bash
# Enhanced Auto-File Generator v1.0
# ターミナル制限問題の完全解決

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

EXEC_DIR="auto_generated_executables"
mkdir -p $EXEC_DIR

echo -e "${BLUE}=== Enhanced Auto-File Generator v1.0 ===${NC}"
echo "🎯 ターミナル制限問題完全解決システム"

generate_executable() {
    local task_name="$1"
    local description="$2"
    local filename="${task_name// /_}.sh"
    local filepath="$EXEC_DIR/$filename"
    
    cat > "$filepath" << HEADER_EOF
#!/bin/bash
# Auto-Generated Executable
# Task: $task_name
# Description: $description
# Generated: $(date)

set -e
echo "🚀 実行開始: $task_name"
echo "📝 説明: $description"
echo ""

HEADER_EOF

    chmod +x "$filepath"
    echo -e "${GREEN}✅ 生成完了: $filepath${NC}"
    echo "$filepath"
}

echo "1) 新しい実行可能ファイルを生成"
echo "2) 使用例を確認"
read -p "選択 (1-2): " choice

case $choice in
    1) 
        read -p "タスク名: " task_name
        read -p "説明: " description
        generate_executable "$task_name" "$description"
        ;;
    2)
        echo "使用例を生成中..."
        example_file=$(generate_executable "Test_Example" "テスト用サンプル")
        echo 'echo "Hello, Auto-File Generator!"' >> "$example_file"
        echo "📋 サンプル生成: $example_file"
        ;;
esac
