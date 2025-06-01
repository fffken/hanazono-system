#!/usr/bin/env python3
"""
HANAZONO 常時稼働Webダッシュボード v1.0
24時間アクセス可能なWeb監視システム
"""

from flask import Flask, render_template_string, jsonify, request
import os
import json
import subprocess
import psutil
from datetime import datetime
import threading
import time

app = Flask(__name__)

class SystemMonitor:
    def __init__(self):
        self.system_data = {}
        self.update_interval = 10  # 10秒間隔で更新
        self.running = True
        self.start_monitoring()
    
    def get_system_status(self):
        """システム状態取得"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # メモリ使用率
            memory = psutil.virtual_memory()
            
            # ディスク使用率
            disk = psutil.disk_usage('/')
            
            # Pythonプロセス数
            python_processes = len([p for p in psutil.process_iter(['pid', 'name', 'cmdline']) 
                                  if 'python3' in p.info['name'] or 
                                  (p.info['cmdline'] and any('python3' in cmd for cmd in p.info['cmdline']))])
            
            # AI帝国ダッシュボード実行
            empire_status = self.get_empire_status()
            
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": (disk.used / disk.total) * 100,
                "python_processes": python_processes,
                "empire_status": empire_status,
                "uptime": self.get_uptime()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_empire_status(self):
        """AI帝国状態取得"""
        try:
            if os.path.exists("empire_dashboard.sh"):
                result = subprocess.run(['bash', 'empire_dashboard.sh'], 
                                      capture_output=True, text=True, timeout=10)
                return {
                    "status": "running" if result.returncode == 0 else "error",
                    "output": result.stdout[:1000]  # 最初の1000文字のみ
                }
            else:
                return {"status": "not_found", "output": "empire_dashboard.sh が見つかりません"}
        except Exception as e:
            return {"status": "error", "output": str(e)}
    
    def get_uptime(self):
        """システム稼働時間取得"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{days}日 {hours}時間 {minutes}分"
        except:
            return "不明"
    
    def update_system_data(self):
        """システムデータ更新"""
        while self.running:
            try:
                self.system_data = self.get_system_status()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"監視エラー: {e}")
                time.sleep(30)
    
    def start_monitoring(self):
        """監視開始"""
        monitor_thread = threading.Thread(target=self.update_system_data, daemon=True)
        monitor_thread.start()

# グローバル監視インスタンス
monitor = SystemMonitor()

@app.route('/')
def index():
    """メインダッシュボード"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/dashboard')
def dashboard():
    """ダッシュボードページ"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    """システム状態API"""
    return jsonify(monitor.system_data)

@app.route('/api/empire')
def api_empire():
    """AI帝国状態API"""
    empire_data = monitor.system_data.get('empire_status', {})
    return jsonify(empire_data)

@app.route('/manual')
def manual():
    """マニュアルページ"""
    try:
        with open('HANAZONO_SYSTEM_MANUAL_v1.0.md', 'r') as f:
            content = f.read()
        return render_template_string(MANUAL_HTML, manual_content=content)
    except:
        return "マニュアルが見つかりません"

# HTMLテンプレート
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HANAZONO AI EMPIRE ダッシュボード</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .title {
            font-size: 3em;
            color: #00ffff;
            text-shadow: 0 0 20px #00ffff;
            margin-bottom: 10px;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .status-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }
        .card-title {
            color: #ffff00;
            font-size: 1.2em;
            margin-bottom: 15px;
            border-bottom: 1px solid #ffff00;
            padding-bottom: 5px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .metric-value {
            color: #00ff00;
            font-weight: bold;
        }
        .empire-output {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .nav {
            text-align: center;
            margin: 20px 0;
        }
        .nav a {
            color: #00ffff;
            text-decoration: none;
            margin: 0 15px;
            padding: 10px 20px;
            border: 1px solid #00ffff;
            border-radius: 5px;
            transition: all 0.3s;
        }
        .nav a:hover {
            background: #00ffff;
            color: #000;
        }
        .auto-refresh {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 0, 0.2);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #00ff00;
        }
    </style>
    <script>
        // 5秒ごとに自動更新
        setInterval(function() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => console.error('Error:', error));
        }, 5000);
        
        function updateDashboard(data) {
            if (data.error) return;
            
            document.getElementById('timestamp').textContent = data.timestamp;
            document.getElementById('cpu-usage').textContent = data.cpu_usage.toFixed(1) + '%';
            document.getElementById('memory-usage').textContent = data.memory_usage.toFixed(1) + '%';
            document.getElementById('disk-usage').textContent = data.disk_usage.toFixed(1) + '%';
            document.getElementById('python-processes').textContent = data.python_processes;
            document.getElementById('uptime').textContent = data.uptime;
            
            if (data.empire_status && data.empire_status.output) {
                document.getElementById('empire-output').textContent = data.empire_status.output;
            }
        }
        
        // 初回読み込み
        window.onload = function() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => updateDashboard(data));
        };
    </script>
</head>
<body>
    <div class="auto-refresh">
        🔄 自動更新: 5秒
    </div>
    
    <div class="container">
        <div class="header">
            <div class="title">👑 HANAZONO AI EMPIRE</div>
            <div>リアルタイム監視ダッシュボード</div>
            <div id="timestamp">読み込み中...</div>
        </div>
        
        <div class="nav">
            <a href="/dashboard">ダッシュボード</a>
            <a href="/manual">マニュアル</a>
            <a href="/api/status">API状態</a>
            <a href="/api/empire">帝国API</a>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <div class="card-title">🖥️ システム状態</div>
                <div class="metric">
                    <span>CPU使用率:</span>
                    <span class="metric-value" id="cpu-usage">0%</span>
                </div>
                <div class="metric">
                    <span>メモリ使用率:</span>
                    <span class="metric-value" id="memory-usage">0%</span>
                </div>
                <div class="metric">
                    <span>ディスク使用率:</span>
                    <span class="metric-value" id="disk-usage">0%</span>
                </div>
                <div class="metric">
                    <span>稼働時間:</span>
                    <span class="metric-value" id="uptime">不明</span>
                </div>
            </div>
            
            <div class="status-card">
                <div class="card-title">🐍 プロセス状態</div>
                <div class="metric">
                    <span>Pythonプロセス数:</span>
                    <span class="metric-value" id="python-processes">0</span>
                </div>
            </div>
            
            <div class="status-card" style="grid-column: 1 / -1;">
                <div class="card-title">🏛️ AI帝国状態</div>
                <div class="empire-output" id="empire-output">読み込み中...</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

MANUAL_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>HANAZONO マニュアル</title>
    <style>
        body { font-family: monospace; background: #1a1a1a; color: #fff; padding: 20px; }
        pre { background: #2a2a2a; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <pre>{{ manual_content }}</pre>
    <a href="/dashboard" style="color: #00ffff;">← ダッシュボードに戻る</a>
</body>
</html>
"""

if __name__ == '__main__':
    print("🚀 HANAZONO Webダッシュボード起動中...")
    print("📊 アクセス URL: http://solarpi:8080")
    print("🔄 自動更新: 5秒間隔")
    app.run(host='0.0.0.0', port=8080, debug=False)
