#!/usr/bin/env python3
"""
HANAZONO リアルタイム監視ダッシュボード v1.0
Webベース監視システム - 究極の可視化・効率化
アクセス: http://192.168.0.191:8080
"""

from flask import Flask, render_template_string, jsonify
import json
import psutil
import subprocess
import glob
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

app = Flask(__name__)

class HANAZONODashboard:
    def __init__(self):
        self.base_dir = Path.home() / "lvyuan_solar_control"
        self.latest_data = {}
        self.system_stats = {}
        self.alerts = []
        
    def get_latest_solar_data(self):
        """最新ソーラーデータ取得"""
        try:
            data_dir = self.base_dir / "data"
            if not data_dir.exists():
                return None
                
            files = list(data_dir.glob("lvyuan_data_*.json"))
            if not files:
                return None
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            with open(latest_file) as f:
                data = json.load(f)
                
            # リスト形式データの処理
            if isinstance(data, list) and len(data) > 0 and data[0] is not None:
                data = data[0]
            
            # データを整理
            if isinstance(data, dict) and 'parameters' in data:
                params = data['parameters']
                formatted_data = {
                    'timestamp': data.get('datetime', 'N/A'),
                    'battery_soc': self._extract_param(params, 'SOC', '%'),
                    'battery_voltage': self._extract_param(params, '電圧', 'V'),
                    'battery_current': self._extract_param(params, '電流', 'A'),
                    'pv_power': self._extract_param(params, 'PV', 'W'),
                    'load_power': self._extract_param(params, '負荷', 'W')
                }
                return formatted_data
        except Exception as e:
            print(f"ソーラーデータ取得エラー: {e}")
            return None
    
    def _extract_param(self, params, keyword, unit):
        """パラメータ抽出"""
        for addr, param in params.items():
            if keyword in param.get('name', ''):
                value = param.get('formatted_value', 'N/A')
                return f"{value} {unit}" if value != 'N/A' else 'N/A'
        return 'N/A'
    
    def get_system_stats(self):
        """システム統計取得"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # プロセス確認
            python_processes = len([p for p in psutil.process_iter() 
                                  if 'python' in p.name().lower()])
            
            return {
                'cpu_percent': round(cpu_percent, 1),
                'memory_percent': round(memory.percent, 1),
                'disk_percent': round(disk.percent, 1),
                'python_processes': python_processes,
                'uptime': self._get_uptime()
            }
        except Exception as e:
            print(f"システム統計エラー: {e}")
            return {}
    
    def _get_uptime(self):
        """稼働時間取得"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            return f"{days}日 {hours}時間"
        except:
            return "不明"
    
    def get_git_status(self):
        """Git状態取得"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            # 最新コミット
            commit_result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], 
                                         capture_output=True, text=True, cwd=self.base_dir)
            latest_commit = commit_result.stdout.strip() if commit_result.stdout else 'N/A'
            
            return {
                'uncommitted_changes': uncommitted,
                'latest_commit': latest_commit,
                'status': '正常' if uncommitted < 5 else '要確認'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_log_summary(self):
        """ログサマリー取得"""
        try:
            logs_dir = self.base_dir / "logs"
            if not logs_dir.exists():
                return {'error': 'ログディレクトリなし'}
            
            log_files = list(logs_dir.glob("*.log"))
            recent_errors = []
            
            # 最新エラーを検索
            for log_file in log_files[-3:]:  # 最新3ファイルのみ
                try:
                    with open(log_file) as f:
                        lines = f.readlines()[-50:]  # 最新50行
                    
                    for line in lines:
                        if 'ERROR' in line or 'エラー' in line:
                            recent_errors.append({
                                'file': log_file.name,
                                'message': line.strip()[:100] + '...' if len(line) > 100 else line.strip()
                            })
                except:
                    continue
            
            return {
                'total_log_files': len(log_files),
                'recent_errors': recent_errors[-5:],  # 最新5件のエラー
                'status': 'エラーあり' if recent_errors else '正常'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_alerts(self):
        """アラート確認"""
        alerts = []
        
        # システムリソースアラート
        stats = self.get_system_stats()
        if stats.get('cpu_percent', 0) > 80:
            alerts.append({'type': 'warning', 'message': f'CPU使用率が高いです: {stats["cpu_percent"]}%'})
        if stats.get('memory_percent', 0) > 80:
            alerts.append({'type': 'warning', 'message': f'メモリ使用率が高いです: {stats["memory_percent"]}%'})
        if stats.get('disk_percent', 0) > 90:
            alerts.append({'type': 'danger', 'message': f'ディスク使用率が危険です: {stats["disk_percent"]}%'})
        
        # Gitアラート
        git_status = self.get_git_status()
        if git_status.get('uncommitted_changes', 0) > 10:
            alerts.append({'type': 'warning', 'message': f'未コミット変更が多いです: {git_status["uncommitted_changes"]}件'})
        
        # データアラート
        solar_data = self.get_latest_solar_data()
        if solar_data and solar_data.get('battery_soc', 'N/A') != 'N/A':
            try:
                soc_value = float(solar_data['battery_soc'].split()[0])
                if soc_value < 20:
                    alerts.append({'type': 'warning', 'message': f'バッテリーSOCが低いです: {soc_value}%'})
            except:
                pass
        
        return alerts

# Flaskルート定義
dashboard = HANAZONODashboard()

@app.route('/')
def index():
    """メインダッシュボード"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/data')
def api_data():
    """API - 全データ取得"""
    try:
        data = {
            'solar_data': dashboard.get_latest_solar_data(),
            'system_stats': dashboard.get_system_stats(),
            'git_status': dashboard.get_git_status(),
            'log_summary': dashboard.get_log_summary(),
            'alerts': dashboard.check_alerts(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/solar')
def api_solar():
    """API - ソーラーデータのみ"""
    return jsonify(dashboard.get_latest_solar_data())

@app.route('/api/system')
def api_system():
    """API - システム統計のみ"""
    return jsonify(dashboard.get_system_stats())

# HTMLテンプレート
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 HANAZONO リアルタイム監視ダッシュボード</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Arial', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333; 
            min-height: 100vh;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            text-align: center; 
            color: white; 
            margin-bottom: 30px; 
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 20px; 
        }
        .card { 
            background: rgba(255,255,255,0.95); 
            border-radius: 15px; 
            padding: 25px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h3 { 
            color: #4a5568; 
            margin-bottom: 20px; 
            font-size: 1.3em;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }
        .metric { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 15px; 
            padding: 10px;
            background: #f7fafc;
            border-radius: 8px;
        }
        .metric-label { font-weight: bold; color: #2d3748; }
        .metric-value { color: #4299e1; font-weight: bold; }
        .status-good { color: #38a169; }
        .status-warning { color: #d69e2e; }
        .status-danger { color: #e53e3e; }
        .alert { 
            padding: 12px; 
            margin: 8px 0; 
            border-radius: 8px; 
            border-left: 4px solid;
        }
        .alert-warning { 
            background: #fef5e7; 
            border-color: #d69e2e; 
            color: #975a16;
        }
        .alert-danger { 
            background: #fed7d7; 
            border-color: #e53e3e; 
            color: #c53030;
        }
        .timestamp { 
            text-align: center; 
            color: rgba(255,255,255,0.8); 
            margin-top: 20px; 
            font-size: 0.9em;
        }
        .loading { 
            text-align: center; 
            color: #666; 
            font-style: italic;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #38a169, #4299e1);
            transition: width 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 HANAZONO リアルタイム監視ダッシュボード</h1>
            <p>究極の可視化・効率化システム</p>
        </div>
        
        <div class="grid">
            <!-- ソーラーシステム -->
            <div class="card">
                <h3>☀️ ソーラーシステム</h3>
                <div id="solar-data" class="loading">データ読み込み中...</div>
            </div>
            
            <!-- システムリソース -->
            <div class="card">
                <h3>💻 システムリソース</h3>
                <div id="system-stats" class="loading">データ読み込み中...</div>
            </div>
            
            <!-- Git状態 -->
            <div class="card">
                <h3>📊 Git状態</h3>
                <div id="git-status" class="loading">データ読み込み中...</div>
            </div>
            
            <!-- ログ状況 -->
            <div class="card">
                <h3>📝 ログ状況</h3>
                <div id="log-summary" class="loading">データ読み込み中...</div>
            </div>
            
            <!-- アラート -->
            <div class="card">
                <h3>⚠️ アラート</h3>
                <div id="alerts" class="loading">確認中...</div>
            </div>
        </div>
        
        <div class="timestamp" id="last-update">最終更新: 読み込み中...</div>
    </div>

    <script>
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    updateSolarData(data.solar_data);
                    updateSystemStats(data.system_stats);
                    updateGitStatus(data.git_status);
                    updateLogSummary(data.log_summary);
                    updateAlerts(data.alerts);
                    document.getElementById('last-update').textContent = `最終更新: ${data.timestamp}`;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        function updateSolarData(data) {
            const container = document.getElementById('solar-data');
            if (!data) {
                container.innerHTML = '<div class="metric"><span>データなし</span></div>';
                return;
            }
            
            container.innerHTML = `
                <div class="metric">
                    <span class="metric-label">🔋 バッテリーSOC</span>
                    <span class="metric-value">${data.battery_soc}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">⚡ バッテリー電圧</span>
                    <span class="metric-value">${data.battery_voltage}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">🔌 バッテリー電流</span>
                    <span class="metric-value">${data.battery_current}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">⏰ データ時刻</span>
                    <span class="metric-value">${data.timestamp}</span>
                </div>
            `;
        }

        function updateSystemStats(data) {
            const container = document.getElementById('system-stats');
            if (!data || Object.keys(data).length === 0) {
                container.innerHTML = '<div class="metric"><span>データ取得エラー</span></div>';
                return;
            }
            
            const cpuClass = data.cpu_percent > 80 ? 'status-danger' : data.cpu_percent > 60 ? 'status-warning' : 'status-good';
            const memClass = data.memory_percent > 80 ? 'status-danger' : data.memory_percent > 60 ? 'status-warning' : 'status-good';
            
            container.innerHTML = `
                <div class="metric">
                    <span class="metric-label">🖥️ CPU使用率</span>
                    <span class="metric-value ${cpuClass}">${data.cpu_percent}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.cpu_percent}%"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">💾 メモリ使用率</span>
                    <span class="metric-value ${memClass}">${data.memory_percent}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.memory_percent}%"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">🔄 Pythonプロセス</span>
                    <span class="metric-value">${data.python_processes}個</span>
                </div>
                <div class="metric">
                    <span class="metric-label">⏰ 稼働時間</span>
                    <span class="metric-value">${data.uptime}</span>
                </div>
            `;
        }

        function updateGitStatus(data) {
            const container = document.getElementById('git-status');
            if (data.error) {
                container.innerHTML = `<div class="metric"><span>エラー: ${data.error}</span></div>`;
                return;
            }
            
            const statusClass = data.uncommitted_changes === 0 ? 'status-good' : 
                               data.uncommitted_changes < 5 ? 'status-warning' : 'status-danger';
            
            container.innerHTML = `
                <div class="metric">
                    <span class="metric-label">📊 未コミット変更</span>
                    <span class="metric-value ${statusClass}">${data.uncommitted_changes}件</span>
                </div>
                <div class="metric">
                    <span class="metric-label">🔄 状態</span>
                    <span class="metric-value ${statusClass}">${data.status}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">📝 最新コミット</span>
                    <span class="metric-value" style="font-size: 0.9em;">${data.latest_commit}</span>
                </div>
            `;
        }

        function updateLogSummary(data) {
            const container = document.getElementById('log-summary');
            if (data.error) {
                container.innerHTML = `<div class="metric"><span>エラー: ${data.error}</span></div>`;
                return;
            }
            
            const statusClass = data.status === '正常' ? 'status-good' : 'status-warning';
            
            let html = `
                <div class="metric">
                    <span class="metric-label">📁 ログファイル数</span>
                    <span class="metric-value">${data.total_log_files}個</span>
                </div>
                <div class="metric">
                    <span class="metric-label">🔍 状態</span>
                    <span class="metric-value ${statusClass}">${data.status}</span>
                </div>
            `;
            
            if (data.recent_errors && data.recent_errors.length > 0) {
                html += '<h4 style="margin-top: 15px; color: #e53e3e;">最新エラー:</h4>';
                data.recent_errors.forEach(error => {
                    html += `<div style="font-size: 0.8em; margin: 5px 0; padding: 5px; background: #fed7d7; border-radius: 4px;">${error.message}</div>`;
                });
            }
            
            container.innerHTML = html;
        }

        function updateAlerts(alerts) {
            const container = document.getElementById('alerts');
            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<div class="metric status-good"><span>✅ アラートなし - システム正常</span></div>';
                return;
            }
            
            let html = '';
            alerts.forEach(alert => {
                html += `<div class="alert alert-${alert.type}">${alert.message}</div>`;
            });
            
            container.innerHTML = html;
        }

        // 初回読み込みと定期更新
        updateDashboard();
        setInterval(updateDashboard, 10000); // 10秒ごとに更新
    </script>
</body>
</html>
'''

def start_dashboard():
    """ダッシュボード起動"""
    print("🚀 HANAZONOリアルタイム監視ダッシュボード起動中...")
    print("📊 アクセスURL: http://192.168.0.191:8080")
    print("🔄 10秒ごとに自動更新")
    print("⏹️  終了: Ctrl+C")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        print("\n📊 ダッシュボードを終了しました")

if __name__ == "__main__":
    start_dashboard()
