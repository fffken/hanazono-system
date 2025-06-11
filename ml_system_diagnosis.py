#!/usr/bin/env python3
"""
機械学習システム詳細調査診断スクリプト
現在の実装状況・稼働状態・データ状況を包括的に調査
"""

import os
import json
import importlib
import sys
from datetime import datetime
from pathlib import Path

def print_section(title):
    """セクション表示"""
    print(f"\n{'='*70}")
    print(f"🔍 {title}")
    print('='*70)

def check_ml_files():
    """機械学習関連ファイル確認"""
    print_section("機械学習関連ファイル確認")
    
    ml_files = [
        "ml_enhancement_phase1.py",
        "ml_enhancement_phase1_v2.py", 
        "ml_enhancement_phase1_v3.py",
        "ml_enhancement_phase1_v4.py",
        "ml_news_generator.py",
        "ml_news_cache.json",
        "dynamic_settings_manager.py",
        "predictive_analysis_system.py"
    ]
    
    existing_files = []
    
    for file in ml_files:
        if os.path.exists(file):
            stat = os.stat(file)
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            print(f"✅ {file}: {size:,}バイト (更新: {mtime})")
            existing_files.append(file)
        else:
            print(f"❌ {file}: 未存在")
    
    return existing_files

def check_ml_data():
    """機械学習データ確認"""
    print_section("機械学習データ確認")
    
    data_locations = [
        "data/",
        "prediction_data/",
        "prediction_models/",
        "prediction_reports/"
    ]
    
    total_data_size = 0
    data_file_count = 0
    
    for location in data_locations:
        if os.path.exists(location):
            print(f"\n📁 {location}:")
            for root, dirs, files in os.walk(location):
                for file in files:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    total_data_size += size
                    data_file_count += 1
                    
                    if file.endswith(('.json', '.csv', '.pkl', '.model')):
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
                        print(f"  📄 {file}: {size:,}バイト ({mtime})")
        else:
            print(f"❌ {location}: ディレクトリ未存在")
    
    print(f"\n📊 データサマリー:")
    print(f"  総ファイル数: {data_file_count}個")
    print(f"  総データサイズ: {total_data_size:,}バイト ({total_data_size/1024/1024:.2f}MB)")
    
    return total_data_size, data_file_count

def test_ml_imports():
    """機械学習モジュールインポートテスト"""
    print_section("機械学習モジュールインポートテスト")
    
    ml_modules = [
        "ml_enhancement_phase1",
        "ml_news_generator", 
        "dynamic_settings_manager",
        "predictive_analysis_system"
    ]
    
    working_modules = []
    
    for module_name in ml_modules:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name}: インポート成功")
            
            # 主要関数・クラスの確認
            if hasattr(module, '__doc__') and module.__doc__:
                doc = module.__doc__.strip().split('\n')[0]
                print(f"   📝 {doc}")
            
            working_modules.append(module_name)
            
        except Exception as e:
            print(f"❌ {module_name}: インポートエラー - {e}")
    
    return working_modules

def check_ml_config():
    """機械学習設定確認"""
    print_section("機械学習設定確認")
    
    config_files = [
        "ml_news_cache.json",
        "settings.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                print(f"✅ {config_file}:")
                
                if 'ml' in config:
                    print(f"   🤖 ML設定セクション存在")
                    ml_config = config['ml']
                    for key, value in ml_config.items():
                        print(f"     {key}: {value}")
                
                if config_file == "ml_news_cache.json":
                    print(f"   📊 キャッシュエントリ数: {len(config)}個")
                    
            except Exception as e:
                print(f"❌ {config_file}: 読み込みエラー - {e}")
        else:
            print(f"❌ {config_file}: 未存在")

def test_ml_functionality():
    """機械学習機能テスト"""
    print_section("機械学習機能テスト")
    
    # dynamic_settings_manager テスト
    try:
        import dynamic_settings_manager as dsm
        print("✅ dynamic_settings_manager: 利用可能")
        
        if hasattr(dsm, 'get_recommended_settings'):
            print("   📊 get_recommended_settings 関数: 存在")
        if hasattr(dsm, 'MLSettingsOptimizer'):
            print("   🤖 MLSettingsOptimizer クラス: 存在")
            
    except Exception as e:
        print(f"❌ dynamic_settings_manager: テストエラー - {e}")
    
    # ml_enhancement_phase1 テスト
    try:
        import ml_enhancement_phase1 as ml1
        print("✅ ml_enhancement_phase1: 利用可能")
        
        if hasattr(ml1, 'train_model'):
            print("   🎓 train_model 関数: 存在")
        if hasattr(ml1, 'predict'):
            print("   🔮 predict 関数: 存在")
            
    except Exception as e:
        print(f"❌ ml_enhancement_phase1: テストエラー - {e}")

def check_cron_ml_integration():
    """cron機械学習統合確認"""
    print_section("cron機械学習統合確認")
    
    try:
        import subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode == 0:
            cron_content = result.stdout
            
            ml_related = []
            for line in cron_content.split('\n'):
                if any(keyword in line for keyword in ['ml_', 'machine', 'predict', 'dynamic_settings']):
                    ml_related.append(line.strip())
            
            if ml_related:
                print("✅ cronに機械学習関連ジョブ発見:")
                for job in ml_related:
                    print(f"   📅 {job}")
            else:
                print("⚠️ cronに機械学習関連ジョブなし")
        else:
            print("❌ crontab確認失敗")
            
    except Exception as e:
        print(f"❌ cron確認エラー: {e}")

def main():
    print("🤖 機械学習システム詳細調査開始")
    print(f"📅 調査実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 各種調査実行
    existing_files = check_ml_files()
    data_size, data_count = check_ml_data()
    working_modules = test_ml_imports()
    check_ml_config()
    test_ml_functionality()
    check_cron_ml_integration()
    
    # 総合サマリー
    print_section("総合調査サマリー")
    
    print(f"📊 機械学習システム現状:")
    print(f"  存在ファイル数: {len(existing_files)}個")
    print(f"  動作可能モジュール: {len(working_modules)}個")
    print(f"  データファイル数: {data_count}個")
    print(f"  総データサイズ: {data_size/1024/1024:.2f}MB")
    
    # 推定実装レベル
    if len(working_modules) >= 3 and data_size > 1024*1024:  # 1MB以上
        print("🚀 実装レベル: Phase 2以上（高度実装）")
    elif len(working_modules) >= 2:
        print("🔧 実装レベル: Phase 1（基本実装）")
    elif len(working_modules) >= 1:
        print("🌱 実装レベル: 初期段階")
    else:
        print("❌ 実装レベル: 未実装または問題あり")

if __name__ == "__main__":
    main()
