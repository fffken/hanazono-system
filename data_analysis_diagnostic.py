#!/usr/bin/env python3
"""
HANAZONOシステム実データ詳細分析スクリプト
6年間の実際のデータ内容・品質・活用可能性を正確に調査
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

class RealDataAnalyzer:
    """実データ分析器"""
    
    def __init__(self):
        self.data_directory = "data"
        self.analysis_results = {}
        
    def analyze_all_data(self):
        """全データの詳細分析"""
        print("🔍 HANAZONOシステム実データ分析開始")
        print("=" * 60)
        
        # 1. データファイル調査
        self._analyze_data_files()
        
        # 2. データベース調査
        self._analyze_databases()
        
        # 3. 履歴データ詳細分析
        self._analyze_historical_data()
        
        # 4. データ品質評価
        self._evaluate_data_quality()
        
        # 5. ML活用可能性評価
        self._evaluate_ml_feasibility()
        
        return self.analysis_results
    
    def _analyze_data_files(self):
        """データファイル構成分析"""
        print("\n📁 データファイル構成分析:")
        
        if not os.path.exists(self.data_directory):
            print(f"❌ データディレクトリが存在しません: {self.data_directory}")
            return
        
        # JSONファイル調査
        json_files = glob.glob(f"{self.data_directory}/*.json")
        csv_files = glob.glob(f"{self.data_directory}/*.csv")
        db_files = glob.glob(f"{self.data_directory}/*.db")
        
        print(f"📄 JSONファイル: {len(json_files)}件")
        print(f"📊 CSVファイル: {len(csv_files)}件") 
        print(f"🗄️ データベースファイル: {len(db_files)}件")
        
        # 最新・最古ファイル確認
        if json_files:
            json_files.sort()
            print(f"📅 最古JSONファイル: {os.path.basename(json_files[0])}")
            print(f"📅 最新JSONファイル: {os.path.basename(json_files[-1])}")
            
            # ファイルサイズ分析
            total_size = sum(os.path.getsize(f) for f in json_files)
            print(f"💾 総データサイズ: {total_size / 1024 / 1024:.2f} MB")
        
        self.analysis_results['file_analysis'] = {
            'json_files': len(json_files),
            'csv_files': len(csv_files),
            'db_files': len(db_files),
            'total_size_mb': total_size / 1024 / 1024 if json_files else 0
        }
    
    def _analyze_databases(self):
        """データベース内容分析"""
        print("\n🗄️ データベース内容分析:")
        
        db_files = glob.glob(f"{self.data_directory}/*.db")
        
        for db_file in db_files:
            print(f"\n📋 データベース: {os.path.basename(db_file)}")
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # テーブル一覧取得
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"  📊 {table_name}: {count}レコード")
                    
                    # 最古・最新データ確認
                    try:
                        cursor.execute(f"SELECT MIN(timestamp), MAX(timestamp) FROM {table_name}")
                        min_time, max_time = cursor.fetchone()
                        if min_time and max_time:
                            print(f"     期間: {min_time} ～ {max_time}")
                    except:
                        pass
                
                conn.close()
                
            except Exception as e:
                print(f"❌ データベース読み取りエラー: {e}")
    
    def _analyze_historical_data(self):
        """履歴データ詳細分析"""
        print("\n📈 履歴データ詳細分析:")
        
        # JSONファイルベースの分析
        json_files = glob.glob(f"{self.data_directory}/lvyuan_data_*.json")
        
        if not json_files:
            print("❌ lvyuan_data_*.json ファイルが見つかりません")
            return
        
        # 期間別データ分析
        daily_data = []
        monthly_data = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # ファイル名から日付抽出
                filename = os.path.basename(json_file)
                if 'lvyuan_data_' in filename:
                    date_str = filename.replace('lvyuan_data_', '').replace('.json', '')
                    
                    # データ品質確認
                    if isinstance(data, list) and len(data) > 50:  # 1日分想定
                        daily_data.append({
                            'date': date_str,
                            'records': len(data),
                            'file_size': os.path.getsize(json_file)
                        })
                    elif isinstance(data, dict) or len(data) < 50:  # 月次想定
                        monthly_data.append({
                            'date': date_str,
                            'records': len(data) if isinstance(data, list) else 1,
                            'file_size': os.path.getsize(json_file)
                        })
                        
            except Exception as e:
                print(f"❌ ファイル分析エラー {json_file}: {e}")
        
        print(f"📊 日次データファイル: {len(daily_data)}件")
        print(f"📊 月次データファイル: {len(monthly_data)}件")
        
        # 期間分析
        if daily_data:
            daily_data.sort(key=lambda x: x['date'])
            print(f"📅 日次データ期間: {daily_data[0]['date']} ～ {daily_data[-1]['date']}")
            
            # データ密度計算
            total_daily_records = sum(d['records'] for d in daily_data)
            avg_records_per_day = total_daily_records / len(daily_data)
            print(f"📊 平均レコード/日: {avg_records_per_day:.1f}")
        
        if monthly_data:
            monthly_data.sort(key=lambda x: x['date'])
            print(f"📅 月次データ期間: {monthly_data[0]['date']} ～ {monthly_data[-1]['date']}")
        
        self.analysis_results['historical_analysis'] = {
            'daily_files': len(daily_data),
            'monthly_files': len(monthly_data),
            'total_records': sum(d['records'] for d in daily_data + monthly_data)
        }
    
    def _evaluate_data_quality(self):
        """データ品質評価"""
        print("\n🎯 データ品質評価:")
        
        # 実際のデータ期間計算
        json_files = glob.glob(f"{self.data_directory}/lvyuan_data_*.json")
        
        if json_files:
            # ファイル名から期間抽出
            dates = []
            for json_file in json_files:
                filename = os.path.basename(json_file)
                date_str = filename.replace('lvyuan_data_', '').replace('.json', '')
                try:
                    # YYYYMMDD形式想定
                    if len(date_str) == 8:
                        date_obj = datetime.strptime(date_str, '%Y%m%d')
                        dates.append(date_obj)
                except:
                    pass
            
            if dates:
                dates.sort()
                period_start = dates[0]
                period_end = dates[-1]
                total_days = (period_end - period_start).days + 1
                
                print(f"📅 実データ期間: {period_start.strftime('%Y-%m-%d')} ～ {period_end.strftime('%Y-%m-%d')}")
                print(f"📊 総期間: {total_days}日 ({total_days/365.25:.1f}年)")
                print(f"📈 データファイル数: {len(json_files)}件")
                print(f"📉 データ密度: {len(json_files)/total_days*100:.1f}%")
                
                # ML学習可能性評価
                ml_feasible = len(json_files) > 365 and (len(json_files)/total_days) > 0.5
                print(f"🤖 ML学習可能性: {'✅ 可能' if ml_feasible else '⚠️ 限定的'}")
                
                self.analysis_results['quality_evaluation'] = {
                    'period_days': total_days,
                    'period_years': total_days/365.25,
                    'data_density': len(json_files)/total_days,
                    'ml_feasible': ml_feasible
                }
    
    def _evaluate_ml_feasibility(self):
        """ML活用可能性詳細評価"""
        print("\n🤖 ML活用可能性詳細評価:")
        
        quality = self.analysis_results.get('quality_evaluation', {})
        period_years = quality.get('period_years', 0)
        data_density = quality.get('data_density', 0)
        
        print(f"📊 データ期間: {period_years:.1f}年")
        print(f"📈 データ密度: {data_density*100:.1f}%")
        
        # ML可能性ランク判定
        if period_years >= 3 and data_density >= 0.8:
            ml_rank = "A (高精度ML可能)"
            expected_accuracy = "90-95%"
        elif period_years >= 2 and data_density >= 0.5:
            ml_rank = "B (中精度ML可能)"
            expected_accuracy = "80-90%"
        elif period_years >= 1 and data_density >= 0.3:
            ml_rank = "C (基本ML可能)"
            expected_accuracy = "70-80%"
        else:
            ml_rank = "D (ML困難)"
            expected_accuracy = "60-70%"
        
        print(f"🏆 ML可能性ランク: {ml_rank}")
        print(f"🎯 予想精度: {expected_accuracy}")
        
        # 推奨ML機能
        if ml_rank.startswith("A"):
            recommended_features = [
                "完全自動設定変更AI",
                "7日先発電量予測",
                "異常検知システム"
            ]
        elif ml_rank.startswith("B"):
            recommended_features = [
                "3日先発電量予測",
                "季節別最適化",
                "簡易異常検知"
            ]
        else:
            recommended_features = [
                "統計ベース予測",
                "ルールベース最適化"
            ]
        
        print(f"💡 推奨ML機能:")
        for feature in recommended_features:
            print(f"   - {feature}")
        
        self.analysis_results['ml_feasibility'] = {
            'rank': ml_rank,
            'expected_accuracy': expected_accuracy,
            'recommended_features': recommended_features
        }

def main():
    """実データ分析実行"""
    analyzer = RealDataAnalyzer()
    results = analyzer.analyze_all_data()
    
    print("\n" + "=" * 60)
    print("🎯 実データ分析完了サマリー")
    print("=" * 60)
    
    # 総合評価
    quality = results.get('quality_evaluation', {})
    ml_info = results.get('ml_feasibility', {})
    
    if quality:
        print(f"📊 実データ期間: {quality.get('period_years', 0):.1f}年")
        print(f"📈 データ品質: {quality.get('data_density', 0)*100:.1f}%")
    
    if ml_info:
        print(f"🤖 ML可能性: {ml_info.get('rank', 'Unknown')}")
        print(f"🎯 予想精度: {ml_info.get('expected_accuracy', 'Unknown')}")
    
    print("\n✅ 実データ分析完了")
    
    return results

if __name__ == "__main__":
    main()
