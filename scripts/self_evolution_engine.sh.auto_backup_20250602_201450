#!/bin/bash
# 自己進化システムエンジン v1.0
# 目的: 失敗→学習→進化→完璧化の自動サイクル

set -e

EVOLUTION_DIR="system_evolution"
LEARNING_DB="$EVOLUTION_DIR/learning_database.json"
EVOLUTION_LOG="logs/evolution_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$EVOLUTION_DIR" logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$EVOLUTION_LOG"
}

log "🧬 自己進化システムエンジン開始"

# 失敗検出システム
detect_failures() {
    log "🔍 システム失敗検出中..."
    
    local failures_found=()
    
    # エラーログから失敗を検出
    find logs/ -name "*.log" -newermt "1 hour ago" -exec grep -l "ERROR\|FAILED\|❌\|エラー\|失敗" {} \; 2>/dev/null | while read logfile; do
        local error_context=$(grep -A5 -B5 "ERROR\|FAILED\|❌\|エラー\|失敗" "$logfile" | tail -20)
        local failure_id=$(echo "$error_context" | md5sum | cut -d' ' -f1)
        
        # 学習データベースに記録
        record_failure "$failure_id" "$logfile" "$error_context"
        failures_found+=("$failure_id")
    done
    
    echo "${failures_found[@]}"
}

# 成功解決方法検出システム
detect_successful_solutions() {
    log "🎯 成功解決方法検出中..."
    
    # 最近のコマンド履歴から解決パターンを分析
    local recent_commands=$(history | tail -50)
    local solutions_found=()
    
    # 解決パターンの検出ルール
    while IFS= read -r cmd; do
        case "$cmd" in
            *"nano "*|*"chmod "*|*"sed "*|*"awk "*)
                local solution_type="file_modification"
                ;;
            *"crontab "*|*"systemctl "*|*"service "*)
                local solution_type="system_configuration"
                ;;
            *"find "*|*"grep "*|*"ps aux"*)
                local solution_type="system_diagnosis"
                ;;
            *"git "*|*"commit"*|*"push"*)
                local solution_type="version_control"
                ;;
            *)
                continue
                ;;
        esac
        
        # 解決方法を学習
        learn_solution "$solution_type" "$cmd"
        solutions_found+=("$solution_type")
    done < <(echo "$recent_commands")
    
    echo "${solutions_found[@]}"
}

# 失敗記録システム
record_failure() {
    local failure_id="$1"
    local logfile="$2"
    local error_context="$3"
    
    # 学習データベースに失敗情報を記録
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ ! -f "$LEARNING_DB" ]; then
        echo '{"failures": {}, "solutions": {}, "evolution_history": []}' > "$LEARNING_DB"
    fi
    
    # JSONに失敗情報を追加
    python3 << EOF
import json
import sys

try:
    with open('$LEARNING_DB', 'r') as f:
        data = json.load(f)
except:
    data = {"failures": {}, "solutions": {}, "evolution_history": []}

data['failures']['$failure_id'] = {
    "timestamp": "$timestamp",
    "logfile": "$logfile",
    "error_context": """$error_context""",
    "status": "unresolved"
}

with open('$LEARNING_DB', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
EOF
    
    log "📝 失敗記録: $failure_id"
}

# 解決方法学習システム
learn_solution() {
    local solution_type="$1"
    local command="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    python3 << EOF
import json

try:
    with open('$LEARNING_DB', 'r') as f:
        data = json.load(f)
except:
    data = {"failures": {}, "solutions": {}, "evolution_history": []}

if '$solution_type' not in data['solutions']:
    data['solutions']['$solution_type'] = []

data['solutions']['$solution_type'].append({
    "timestamp": "$timestamp",
    "command": """$command""",
    "success_frequency": 1
})

with open('$LEARNING_DB', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
EOF
    
    log "🧠 解決方法学習: $solution_type"
}

# 新機能自動生成システム
generate_new_feature() {
    local solution_type="$1"
    
    log "🛠️ 新機能自動生成: $solution_type"
    
    local feature_script="scripts/auto_generated/auto_${solution_type}_v$(date +%Y%m%d_%H%M%S).sh"
    mkdir -p scripts/auto_generated
    
    case "$solution_type" in
        "file_modification")
            generate_file_mod_feature "$feature_script"
            ;;
        "system_configuration")
            generate_system_config_feature "$feature_script"
            ;;
        "system_diagnosis")
            generate_diagnosis_feature "$feature_script"
            ;;
        "version_control")
            generate_version_control_feature "$feature_script"
            ;;
        *)
            generate_generic_feature "$feature_script" "$solution_type"
            ;;
    esac
    
    chmod +x "$feature_script"
    log "✅ 新機能生成完了: $feature_script"
}

# ファイル修正機能生成
generate_file_mod_feature() {
    local script_path="$1"
    
    cat << 'FILE_MOD_END' > "$script_path"
#!/bin/bash
# 自動生成: ファイル修正完全自動化機能
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_file_mod_$(date +%Y%m%d).log"
}

# 学習した解決方法を適用
auto_file_modification() {
    log "🔧 学習済みファイル修正開始"
    
    # 学習データベースから成功パターンを取得
    local learned_commands=$(python3 -c "
import json
try:
    with open('system_evolution/learning_database.json', 'r') as f:
        data = json.load(f)
    solutions = data.get('solutions', {}).get('file_modification', [])
    for sol in solutions[-5:]:  # 最新5つ
        print(sol['command'].split('|')[0].strip())
except:
    pass
")
    
    # 学習したコマンドパターンを実行
    echo "$learned_commands" | while read cmd; do
        if [[ ! -z "$cmd" && "$cmd" =~ (nano|sed|awk|chmod) ]]; then
            log "🎯 学習パターン適用: $cmd"
            # 安全な範囲で自動実行
            eval "$cmd" 2>/dev/null || log "⚠️ パターン適用失敗: $cmd"
        fi
    done
    
    log "✅ 学習済みファイル修正完了"
}

# 実行
auto_file_modification
FILE_MOD_END
}

# システム設定機能生成
generate_system_config_feature() {
    local script_path="$1"
    
    cat << 'SYS_CONFIG_END' > "$script_path"
#!/bin/bash
# 自動生成: システム設定完全自動化機能
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_sys_config_$(date +%Y%m%d).log"
}

# 学習したシステム設定を適用
auto_system_configuration() {
    log "🔧 学習済みシステム設定開始"
    
    # cron健全性チェック・修正
    if ! crontab -l | grep -q "scripts/auto_git_save_system.sh"; then
        log "🎯 Git自動保存の再設定"
        (crontab -l 2>/dev/null; echo "0 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_git_save_system.sh >> logs/auto_git_save.log 2>&1") | crontab -
    fi
    
    # サービス状態チェック
    for service in cron ssh; do
        if ! systemctl is-active --quiet $service; then
            log "🎯 サービス再起動: $service"
            sudo systemctl restart $service 2>/dev/null || true
        fi
    done
    
    log "✅ 学習済みシステム設定完了"
}

# 実行
auto_system_configuration
SYS_CONFIG_END
}

# 診断機能生成
generate_diagnosis_feature() {
    local script_path="$1"
    
    cat << 'DIAGNOSIS_END' > "$script_path"
#!/bin/bash
# 自動生成: システム診断完全自動化機能
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_diagnosis_$(date +%Y%m%d).log"
}

# 学習した診断方法を実行
auto_system_diagnosis() {
    log "🔍 学習済みシステム診断開始"
    
    # プロセス診断
    local suspicious_processes=$(ps aux | awk 'NR>1 {if($3>80) print $2,$11}')
    if [[ ! -z "$suspicious_processes" ]]; then
        log "⚠️ 高CPU使用プロセス検出: $suspicious_processes"
    fi
    
    # ディスク使用量診断
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $disk_usage -gt 80 ]; then
        log "⚠️ ディスク使用量警告: ${disk_usage}%"
        # 自動クリーンアップ
        find /tmp -type f -mtime +7 -delete 2>/dev/null || true
        find logs/ -name "*.log" -mtime +30 -delete 2>/dev/null || true
    fi
    
    # メモリ使用量診断
    local mem_usage=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
    if [ $mem_usage -gt 80 ]; then
        log "⚠️ メモリ使用量警告: ${mem_usage}%"
        sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
    fi
    
    log "✅ 学習済みシステム診断完了"
}

# 実行
auto_system_diagnosis
DIAGNOSIS_END
}

# バージョン管理機能生成
generate_version_control_feature() {
    local script_path="$1"
    
    cat << 'VERSION_CONTROL_END' > "$script_path"
#!/bin/bash
# 自動生成: バージョン管理完全自動化機能
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_version_control_$(date +%Y%m%d).log"
}

# 学習したバージョン管理を実行
auto_version_control() {
    log "🔧 学習済みバージョン管理開始"
    
    # 変更検出
    if [ $(git status --porcelain | wc -l) -gt 0 ]; then
        log "🎯 変更検出 - 自動コミット実行"
        
        # AI記憶システムを優先保存
        git add ai_memory/storage/permanent/ 2>/dev/null || true
        git add *.md *.json 2>/dev/null || true
        git add scripts/auto_generated/ 2>/dev/null || true
        git add logs/ 2>/dev/null || true
        
        # 自動コミット
        local commit_msg="🤖 自己進化システム自動更新: $(date '+%Y-%m-%d %H:%M')"
        git commit -m "$commit_msg" 2>/dev/null || true
        
        # 自動プッシュ
        git push origin main 2>/dev/null || true
        
        log "✅ 自動バージョン管理完了"
    fi
}

# 実行
auto_version_control
VERSION_CONTROL_END
}

# 汎用機能生成
generate_generic_feature() {
    local script_path="$1"
    local solution_type="$2"
    
    cat << GENERIC_FEATURE_END > "$script_path"
#!/bin/bash
# 自動生成: ${solution_type}完全自動化機能
# 生成時刻: $(date)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "logs/auto_${solution_type}_$(date +%Y%m%d).log"
}

# 学習した${solution_type}方法を実行
auto_${solution_type}() {
    log "🔧 学習済み${solution_type}開始"
    
    # 学習データベースから該当する解決方法を取得・実行
    python3 << 'PYTHON_END'
import json
import subprocess
import sys

try:
    with open('system_evolution/learning_database.json', 'r') as f:
        data = json.load(f)
    
    solutions = data.get('solutions', {}).get('${solution_type}', [])
    
    for solution in solutions[-3:]:  # 最新3つの解決方法
        cmd = solution.get('command', '').strip()
        if cmd and not any(dangerous in cmd for dangerous in ['rm -rf', 'dd if=', 'mkfs']):
            print(f"実行中: {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"成功: {cmd}")
                else:
                    print(f"失敗: {cmd}")
            except Exception as e:
                print(f"エラー: {cmd} - {e}")
except Exception as e:
    print(f"学習データ読み込みエラー: {e}")
PYTHON_END
    
    log "✅ 学習済み${solution_type}完了"
}

# 実行
auto_${solution_type}
GENERIC_FEATURE_END
}

# 進化履歴記録システム
record_evolution() {
    local evolution_type="$1"
    local description="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    python3 << EOF
import json

try:
    with open('$LEARNING_DB', 'r') as f:
        data = json.load(f)
except:
    data = {"failures": {}, "solutions": {}, "evolution_history": []}

data['evolution_history'].append({
    "timestamp": "$timestamp",
    "type": "$evolution_type",
    "description": "$description",
    "evolution_version": "$(date +%Y%m%d_%H%M%S)"
})

with open('$LEARNING_DB', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
EOF
    
    log "📚 進化履歴記録: $evolution_type - $description"
}

# 完璧性評価システム
evaluate_perfection() {
    log "🏆 システム完璧性評価中..."
    
    local perfection_score=0
    local total_checks=0
    
    # 失敗率チェック
    local failure_count=$(python3 -c "
import json
try:
    with open('$LEARNING_DB', 'r') as f:
        data = json.load(f)
    unresolved = sum(1 for f in data.get('failures', {}).values() if f.get('status') == 'unresolved')
    print(unresolved)
except:
    print(0)
")
    
    if [ $failure_count -eq 0 ]; then
        perfection_score=$((perfection_score + 25))
    fi
    total_checks=$((total_checks + 1))
    
    # システム稼働率チェック
    if pgrep -f "python3.*main.py" > /dev/null && crontab -l | grep -q "auto_git_save"; then
        perfection_score=$((perfection_score + 25))
    fi
    total_checks=$((total_checks + 1))
    
    # 自動化機能数チェック
    local automation_count=$(find scripts/auto_generated/ -name "*.sh" 2>/dev/null | wc -l)
    if [ $automation_count -ge 5 ]; then
        perfection_score=$((perfection_score + 25))
    fi
    total_checks=$((total_checks + 1))
    
    # 学習データ蓄積チェック
    local solution_types=$(python3 -c "
import json
try:
    with open('$LEARNING_DB', 'r') as f:
        data = json.load(f)
    print(len(data.get('solutions', {})))
except:
    print(0)
")
    
    if [ $solution_types -ge 3 ]; then
        perfection_score=$((perfection_score + 25))
    fi
    total_checks=$((total_checks + 1))
    
    local perfection_percentage=$((perfection_score))
    
    log "🎯 現在の完璧性: ${perfection_percentage}%"
    
    if [ $perfection_percentage -ge 90 ]; then
        log "🏆 システム完璧性達成！"
        record_evolution "perfection_milestone" "システム完璧性90%以上達成"
    fi
}

# メイン自己進化サイクル
main_evolution_cycle() {
    log "🧬 自己進化サイクル開始"
    
    # 1. 失敗検出
    local failures=($(detect_failures))
    
    # 2. 成功解決方法検出
    local solutions=($(detect_successful_solutions))
    
    # 3. 新機能生成
    for solution_type in "${solutions[@]}"; do
        if [[ ! -z "$solution_type" ]]; then
            generate_new_feature "$solution_type"
            record_evolution "feature_generation" "新機能生成: $solution_type"
        fi
    done
    
    # 4. 完璧性評価
    evaluate_perfection
    
    # 5. 進化システム自体の改良
    if [ ${#solutions[@]} -gt 0 ]; then
        log "🚀 進化加速: ${#solutions[@]}個の新機能を生成"
        
        # 統合実行スクリプト更新
        cat << 'INTEGRATION_END' > scripts/run_evolved_systems.sh
#!/bin/bash
# 進化したシステム統合実行
echo "🧬 進化システム統合実行開始: $(date)"

# 自動生成された全機能を実行
for script in scripts/auto_generated/auto_*.sh; do
    if [ -f "$script" ]; then
        echo "🎯 実行中: $(basename $script)"
        timeout 60 bash "$script" || echo "⚠️ タイムアウト: $script"
    fi
done

echo "✅ 進化システム統合実行完了: $(date)"
INTEGRATION_END
        
        chmod +x scripts/run_evolved_systems.sh
        
        # 進化システムを自動実行に追加
        if ! crontab -l 2>/dev/null | grep -q "run_evolved_systems"; then
            (crontab -l 2>/dev/null; echo "0 */4 * * * cd /home/pi/lvyuan_solar_control && bash scripts/run_evolved_systems.sh >> logs/evolved_systems.log 2>&1") | crontab -
            log "📅 進化システム4時間ごと自動実行を追加"
        fi
    fi
    
    log "🎉 自己進化サイクル完了"
}

# AI記憶システム統合
integrate_with_memory_system() {
    log "🧠 AI記憶システム統合中..."
    
    # 進化データをAI記憶に記録
    cat << EOF > ai_memory/storage/permanent/self_evolution_memory.json
{
  "self_evolution_system": {
    "記録日時": "$(date '+%Y-%m-%d %H:%M:%S')",
    "目的": "失敗→学習→進化→完璧化の自動サイクル",
    "進化データベース": "$LEARNING_DB",
    "進化ログ": "$EVOLUTION_LOG",
    "自動生成スクリプト保存場所": "scripts/auto_generated/",
    "完璧性評価システム": "有効",
    "学習能力": "全自動",
    "自己改善サイクル": "4時間ごと",
    "記憶統合": "完了"
  }
}
EOF
    
    log "✅ AI記憶システム統合完了"
}

# 実行
main_evolution_cycle
integrate_with_memory_system

log "🧬 自己進化システムエンジン完了"
