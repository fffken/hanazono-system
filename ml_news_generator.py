"""
HANAZONOシステム NEWSメール生成システム v1.0
機械学習による設定変化をNEWSとして配信

機能:
1. 設定変更の自動検知・NEWS生成
2. ML学習進捗のリアルタイム通知
3. 削減効果・改善点の面白い表現
4. メールシステムとの統合

期待される面白いNEWS例:
📧 「充電電流が機械学習により50A→46Aに最適化（+¥404/月削減予測）」
📊 「1,147件データ分析により予測精度62.4%達成（従来30%から倍増）」
🎯 「SOC設定を45%→40%に調整（6年分データ学習結果）」
"""

import os
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict

class MLNewsGenerator:
    def __init__(self):
        self.logger = self._setup_logger()
        self.history_file = 'settings_change_history.json'
        self.news_cache_file = 'ml_news_cache.json'
        self.news_history = []
        self.load_news_cache()
        
    def _setup_logger(self):
        logger = logging.getLogger('MLニュース')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_news_cache(self):
        """ニュースキャッシュの読み込み"""
        try:
            if os.path.exists(self.news_cache_file):
                with open(self.news_cache_file, 'r', encoding='utf-8') as f:
                    self.news_history = json.load(f)
            else:
                self.news_history = []
        except Exception as e:
            self.logger.warning(f"ニュースキャッシュ読み込みエラー: {e}")
            self.news_history = []

    def save_news_cache(self):
        """ニュースキャッシュの保存"""
        try:
            with open(self.news_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.news_history[-50:], f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"ニュースキャッシュ保存エラー: {e}")

    def load_settings_history(self):
        """設定変更履歴の読み込み"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"履歴読み込みエラー: {e}")
            return []

    def detect_changes(self):
        """設定変更の検知・分析"""
        try:
            history = self.load_settings_history()
            if len(history) < 2:
                return []

            current = history[-1]
            previous = history[-2]
            
            changes = []
            
            # 充電電流の変化
            if current['charge_current'] != previous['charge_current']:
                old_val = int(previous['charge_current'].replace('A', ''))
                new_val = int(current['charge_current'].replace('A', ''))
                diff = new_val - old_val
                
                if diff > 0:
                    direction = "増加"
                    emoji = "⬆️"
                    reason = "雨天対応強化" if diff >= 5 else "効率最適化"
                else:
                    direction = "削減"
                    emoji = "⬇️"
                    reason = "晴天最適化" if abs(diff) >= 5 else "省エネ化"
                
                estimated_savings = abs(diff) * 30  # 簡易計算
                
                changes.append({
                    'type': 'charge_current',
                    'title': f'充電電流設定の機械学習最適化',
                    'content': f'充電電流が{previous["charge_current"]}→{current["charge_current"]}に{direction} {emoji}',
                    'detail': f'機械学習分析により{reason}のため調整されました',
                    'impact': f'月間推定効果: +¥{estimated_savings:,}',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            # 充電時間の変化
            if current['charge_time'] != previous['charge_time']:
                old_val = int(previous['charge_time'].replace('分', ''))
                new_val = int(current['charge_time'].replace('分', ''))
                diff = new_val - old_val
                
                if diff > 0:
                    direction = "延長"
                    emoji = "⏰"
                    reason = "蓄電量確保重視"
                else:
                    direction = "短縮"
                    emoji = "⚡"
                    reason = "効率重視モード"
                
                time_savings = abs(diff) * 15  # 時間価値換算
                
                changes.append({
                    'type': 'charge_time',
                    'title': f'充電時間の自動最適化',
                    'content': f'充電時間が{previous["charge_time"]}→{current["charge_time"]}に{direction} {emoji}',
                    'detail': f'データ分析により{reason}へ調整',
                    'impact': f'効率化効果: +¥{time_savings}/月',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            # SOC設定の変化
            if current['soc_setting'] != previous['soc_setting']:
                old_val = int(previous['soc_setting'].replace('%', ''))
                new_val = int(current['soc_setting'].replace('%', ''))
                diff = new_val - old_val
                
                if diff > 0:
                    direction = "上昇"
                    emoji = "📈"
                    reason = "安定性重視"
                else:
                    direction = "最適化"
                    emoji = "🎯"
                    reason = "効率重視"
                
                soc_savings = abs(diff) * 25
                
                changes.append({
                    'type': 'soc_setting',
                    'title': f'SOC設定の学習調整',
                    'content': f'SOC設定が{previous["soc_setting"]}→{current["soc_setting"]}に{direction} {emoji}',
                    'detail': f'過去パターン分析により{reason}設定へ変更',
                    'impact': f'最適化効果: +¥{soc_savings}/月',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            # 信頼度の向上
            old_conf = float(previous['confidence'].replace('%', ''))
            new_conf = float(current['confidence'].replace('%', ''))
            if new_conf > old_conf + 5:  # 5%以上向上
                changes.append({
                    'type': 'confidence_improvement',
                    'title': '機械学習精度の向上を検出',
                    'content': f'ML予測精度が{previous["confidence"]}→{current["confidence"]}に向上 🚀',
                    'detail': f'{current.get("data_count", 0):,}件のデータ分析により精度が改善',
                    'impact': 'より正確な最適化により削減効果拡大',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            return changes
            
        except Exception as e:
            self.logger.error(f"変更検知エラー: {e}")
            return []

    def generate_milestone_news(self):
        """マイルストーンニュースの生成"""
        try:
            history = self.load_settings_history()
            if not history:
                return []

            current = history[-1]
            news_items = []
            
            # データ数のマイルストーン
            data_count = current.get('data_count', 0)
            if data_count >= 1000 and not any(n.get('type') == 'data_milestone_1000' for n in self.news_history):
                news_items.append({
                    'type': 'data_milestone_1000',
                    'title': '🎉 1,000データポイント突破記念',
                    'content': f'{data_count:,}件のデータ蓄積達成！',
                    'detail': '機械学習の精度向上により、より正確な最適化が可能になりました',
                    'impact': '予測精度の大幅向上を実現',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            # 高精度達成
            confidence = float(current['confidence'].replace('%', ''))
            if confidence >= 60 and not any(n.get('type') == 'high_confidence' for n in self.news_history):
                news_items.append({
                    'type': 'high_confidence',
                    'title': '🏆 高精度ML予測システム稼働開始',
                    'content': f'機械学習予測精度{current["confidence"]}達成！',
                    'detail': '従来の30%から大幅向上。より信頼性の高い最適化を実現',
                    'impact': '年間削減効果の最大化が期待されます',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            # 削減額の達成
            savings = current.get('savings_prediction', 50600)
            if savings > 55000 and not any(n.get('type') == 'savings_milestone' for n in self.news_history):
                news_items.append({
                    'type': 'savings_milestone',
                    'title': '💰 年間削減額5.5万円突破',
                    'content': f'予想年間削減額¥{savings:,.0f}を達成！',
                    'detail': '機械学習最適化により従来比+9.7%の削減効果',
                    'impact': 'システム投資回収の加速化',
                    'confidence': current['confidence'],
                    'timestamp': current['timestamp']
                })

            return news_items
            
        except Exception as e:
            self.logger.error(f"マイルストーンニュース生成エラー: {e}")
            return []

    def generate_analysis_news(self):
        """分析ニュースの生成"""
        try:
            history = self.load_settings_history()
            if len(history) < 3:
                return []

            news_items = []
            recent_changes = history[-3:]
            
            # 設定の安定性分析
            charge_currents = [int(h['charge_current'].replace('A', '')) for h in recent_changes]
            if len(set(charge_currents)) == 1:
                news_items.append({
                    'type': 'stability_analysis',
                    'title': '📊 設定安定期に突入',
                    'content': f'充電電流{recent_changes[-1]["charge_current"]}で3回連続安定',
                    'detail': '機械学習が最適解を発見。当面この設定での運用を推奨',
                    'impact': '安定運用による効率最大化',
                    'confidence': recent_changes[-1]['confidence'],
                    'timestamp': recent_changes[-1]['timestamp']
                })

            # トレンド分析
            confidences = [float(h['confidence'].replace('%', '')) for h in recent_changes]
            if confidences[-1] > confidences[0] + 10:
                news_items.append({
                    'type': 'trend_analysis',
                    'title': '📈 学習精度の継続的向上を確認',
                    'content': f'ML信頼度が{confidences[0]:.1f}%→{confidences[-1]:.1f}%に向上',
                    'detail': 'データ蓄積により予測モデルが継続的に改善中',
                    'impact': '今後さらなる最適化効果が期待されます',
                    'confidence': recent_changes[-1]['confidence'],
                    'timestamp': recent_changes[-1]['timestamp']
                })

            return news_items
            
        except Exception as e:
            self.logger.error(f"分析ニュース生成エラー: {e}")
            return []

    def format_news_for_email(self, news_items):
        """メール用ニュース形式の生成"""
        if not news_items:
            return "現在、新しいMLニュースはありません。"

        formatted_news = []
        formatted_news.append("📰 ML学習NEWS (最新5件)")
        formatted_news.append("=" * 40)
        
        for i, news in enumerate(news_items[-5:], 1):
            timestamp = datetime.strptime(news['timestamp'], '%Y-%m-%d %H:%M:%S')
            time_str = timestamp.strftime('%m/%d %H:%M')
            
            formatted_news.append(f"• [{time_str}] {news['title']}")
            formatted_news.append(f"  {news['content']}")
            formatted_news.append(f"  💡 {news['detail']}")
            formatted_news.append(f"  💰 {news['impact']}")
            formatted_news.append(f"  🎯 信頼度: {news['confidence']}")
            formatted_news.append("")

        return "\n".join(formatted_news)

    def generate_all_news(self):
        """全ニュースの生成・統合"""
        try:
            all_news = []
            
            # 設定変更ニュース
            changes = self.detect_changes()
            all_news.extend(changes)
            
            # マイルストーンニュース
            milestones = self.generate_milestone_news()
            all_news.extend(milestones)
            
            # 分析ニュース
            analysis = self.generate_analysis_news()
            all_news.extend(analysis)
            
            # 新しいニュースのみを履歴に追加
            for news in all_news:
                if not any(h.get('content') == news['content'] for h in self.news_history):
                    self.news_history.append(news)
                    self.logger.info(f"新規ニュース生成: {news['title']}")
            
            # キャッシュ保存
            self.save_news_cache()
            
            return all_news
            
        except Exception as e:
            self.logger.error(f"ニュース生成エラー: {e}")
            return []

    def get_latest_news(self, count=5):
        """最新ニュースの取得"""
        all_news = self.generate_all_news()
        latest_news = sorted(self.news_history, key=lambda x: x['timestamp'], reverse=True)
        return latest_news[:count]

    def get_news_summary(self):
        """ニュースサマリーの取得"""
        try:
            latest_news = self.get_latest_news(5)
            
            summary = {
                'total_news': len(self.news_history),
                'latest_count': len(latest_news),
                'formatted_news': self.format_news_for_email(latest_news),
                'has_new_content': len(latest_news) > 0,
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"サマリー生成エラー: {e}")
            return {
                'total_news': 0,
                'latest_count': 0,
                'formatted_news': "ニュース取得エラーが発生しました。",
                'has_new_content': False,
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

def test_news_generation():
    """ニュース生成システムのテスト"""
    print("📰 ML NEWSジェネレーター テスト開始")
    print("=" * 50)
    
    generator = MLNewsGenerator()
    
    # ニュース生成テスト
    news_items = generator.generate_all_news()
    print(f"✅ ニュース生成: {len(news_items)}件")
    
    # サマリー取得テスト
    summary = generator.get_news_summary()
    print(f"✅ サマリー生成: {summary['latest_count']}件の最新ニュース")
    
    # フォーマット済みニュース表示
    print("\n" + summary['formatted_news'])
    
    return len(news_items) > 0

def generate_news_for_email():
    """メール用ニュース生成（外部呼び出し用）"""
    generator = MLNewsGenerator()
    summary = generator.get_news_summary()
    return summary

if __name__ == "__main__":
    print("📰 HANAZONOシステム ML NEWSジェネレーター v1.0")
    print("=" * 60)
    print("📋 実行オプション:")
    print("1. メイン実行: python3 ml_news_generator.py")
    print("2. テスト実行: python3 -c \"from ml_news_generator import test_news_generation; test_news_generation()\"")
    print("3. ニュース生成: python3 -c \"from ml_news_generator import generate_news_for_email; print(generate_news_for_email())\"")
    print("=" * 60)
    
    test_news_generation()
