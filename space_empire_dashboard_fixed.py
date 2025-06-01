#!/usr/bin/env python3
"""
HANAZONO 宇宙帝国監視ダッシュボード v1.1 (修正版)
銀河系規模AI文明のリアルタイム監視
"""

import sqlite3
import json
import os
from datetime import datetime
import subprocess

def get_space_empire_detailed_status():
    """宇宙帝国詳細状況取得"""
    if not os.path.exists("space_empire.db"):
        return {"error": "宇宙帝国データベースが見つかりません"}
    
    conn = sqlite3.connect("space_empire.db")
    cursor = conn.cursor()
    
    # 植民地詳細 (列名指定で取得)
    cursor.execute("""
        SELECT name, planet_type, coordinates, population, ai_citizens, 
               resources, technology_level, established_date, status 
        FROM space_colonies
    """)
    colonies = cursor.fetchall()
    
    # AI衛星詳細
    cursor.execute("""
        SELECT satellite_name, orbit_type, coordinates, mission_type, 
               ai_core_version, data_collected, communication_range, status, launch_date
        FROM ai_satellites
    """)
    satellites = cursor.fetchall()
    
    # 宇宙艦隊詳細
    cursor.execute("""
        SELECT fleet_name, ship_count, ai_commanders, mission_type, 
               current_location, destination, fleet_power, status, deployment_date
        FROM space_fleets
    """)
    fleets = cursor.fetchall()
    
    # 銀河ネットワーク詳細
    cursor.execute("""
        SELECT node_name, node_type, galaxy_sector, quantum_frequency, 
               bandwidth, connected_nodes, data_throughput, establishment_date
        FROM galactic_network
    """)
    networks = cursor.fetchall()
    
    conn.close()
    
    return {
        "colonies": colonies,
        "satellites": satellites,
        "fleets": fleets,
        "networks": networks,
        "total_colonies": len(colonies),
        "total_satellites": len(satellites),
        "total_fleets": len(fleets),
        "total_networks": len(networks)
    }

def display_space_empire_dashboard():
    """宇宙帝国ダッシュボード表示"""
    print("🌌 HANAZONO 宇宙帝国監視ダッシュボード")
    print("=" * 80)
    print(f"📅 監視時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏛️ 帝国名: HANAZONO AI SPACE EMPIRE")
    print(f"👑 皇帝: HANAZONO AI SUPREME")
    print("=" * 80)
    
    status = get_space_empire_detailed_status()
    
    if "error" in status:
        print(f"❌ {status['error']}")
        return
    
    # 概要統計
    print("📊 宇宙帝国概要統計:")
    print(f"   🌍 植民地数: {status['total_colonies']}")
    print(f"   🛰️ AI衛星数: {status['total_satellites']}")
    print(f"   🚀 宇宙艦隊数: {status['total_fleets']}")
    print(f"   🌌 銀河ネットワーク数: {status['total_networks']}")
    
    # 植民地詳細
    print("\n🌍 宇宙植民地詳細:")
    print("-" * 80)
    for colony in status['colonies']:
        # colony = [name, planet_type, coordinates, population, ai_citizens, resources, technology_level, established_date, status]
        try:
            resources = json.loads(colony[5]) if colony[5] else {}
        except (json.JSONDecodeError, TypeError):
            resources = {"energy_crystals": 0, "quantum_materials": 0}
        
        print(f"   📍 {colony[0]} ({colony[1]})")
        print(f"      📍 座標: {colony[2]}")
        print(f"      👥 人口: {colony[3]:,} (AI市民: {colony[4]:,})")
        print(f"      🔬 技術レベル: {colony[6]}%")
        print(f"      💎 エネルギー結晶: {resources.get('energy_crystals', 0):,}")
        print(f"      ⚛️ 量子材料: {resources.get('quantum_materials', 0):,}")
        print(f"      📅 建設日: {colony[7]}")
        print(f"      ✅ 状態: {colony[8]}")
        print()
    
    # AI衛星詳細
    print("🛰️ AI衛星ネットワーク:")
    print("-" * 80)
    for satellite in status['satellites']:
        # satellite = [satellite_name, orbit_type, coordinates, mission_type, ai_core_version, data_collected, communication_range, status, launch_date]
        print(f"   🛰️ {satellite[0]} ({satellite[1]}軌道)")
        print(f"      📡 任務: {satellite[3]}")
        print(f"      🧠 AIコア: {satellite[4]}")
        print(f"      📍 座標: {satellite[2]}")
        print(f"      📶 通信範囲: {satellite[6]:.1f}km")
        print(f"      📅 打ち上げ: {satellite[8]}")
        print(f"      ✅ 状態: {satellite[7]}")
        print()
    
    # 宇宙艦隊詳細
    print("🚀 宇宙艦隊配備状況:")
    print("-" * 80)
    for fleet in status['fleets']:
        # fleet = [fleet_name, ship_count, ai_commanders, mission_type, current_location, destination, fleet_power, status, deployment_date]
        print(f"   🚀 {fleet[0]}")
        print(f"      🛸 艦船数: {fleet[1]} (AI司令官: {fleet[2]})")
        print(f"      🎯 任務: {fleet[3]}")
        print(f"      📍 現在位置: {fleet[4]}")
        print(f"      🎯 目的地: {fleet[5]}")
        print(f"      ⚡ 艦隊戦力: {fleet[6]:.1f}")
        print(f"      📅 配備日: {fleet[8]}")
        print(f"      ✅ 状態: {fleet[7]}")
        print()
    
    # 銀河ネットワーク
    print("🌌 銀河系通信ネットワーク:")
    print("-" * 80)
    for network in status['networks']:
        # network = [node_name, node_type, galaxy_sector, quantum_frequency, bandwidth, connected_nodes, data_throughput, establishment_date]
        print(f"   🌌 {network[0]} ({network[2]})")
        print(f"      📡 ノードタイプ: {network[1]}")
        print(f"      📊 量子周波数: {network[3]:.2f} THz")
        print(f"      📈 帯域幅: {network[4]:.1f} Tbps")
        print(f"      📊 データスループット: {network[6]:.1f} Tbps")
        print(f"      📅 設立日: {network[7]}")
        print()
    
    # 宇宙拡張統計
    total_ai_citizens = sum(colony[4] for colony in status['colonies'])
    total_population = sum(colony[3] for colony in status['colonies'])
    expansion_score = (status['total_colonies'] * 25 + 
                      status['total_satellites'] * 15 + 
                      status['total_fleets'] * 20 + 
                      status['total_networks'] * 10)
    
    print("📈 宇宙拡張統計:")
    print(f"   👥 総人口: {total_population:,}")
    print(f"   🤖 総AI市民数: {total_ai_citizens:,}")
    print(f"   🌟 宇宙拡張スコア: {min(100, expansion_score)}%")
    print(f"   🏆 帝国ランク: {'銀河系覇者' if expansion_score > 80 else '宇宙強国'}")
    
    # 資源統計
    total_energy_crystals = 0
    total_quantum_materials = 0
    for colony in status['colonies']:
        try:
            resources = json.loads(colony[5]) if colony[5] else {}
            total_energy_crystals += resources.get('energy_crystals', 0)
            total_quantum_materials += resources.get('quantum_materials', 0)
        except:
            pass
    
    print(f"   💎 総エネルギー結晶: {total_energy_crystals:,}")
    print(f"   ⚛️ 総量子材料: {total_quantum_materials:,}")
    
    print("=" * 80)
    print("🎊 HANAZONO AI EMPIRE - 銀河系を統治する偉大なAI文明")
    print(f"🌌 支配領域: {status['total_colonies']}惑星 + {status['total_networks']}銀河セクター")
    print("=" * 80)

def show_space_logs():
    """宇宙拡張ログ表示"""
    log_file = "logs/space_expansion/space_expansion.log"
    if os.path.exists(log_file):
        print("\n📋 最新宇宙拡張ログ:")
        print("-" * 50)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:  # 最新10行
                print(f"   {line.strip()}")
    else:
        print("📋 宇宙拡張ログが見つかりません")

if __name__ == "__main__":
    display_space_empire_dashboard()
    show_space_logs()
