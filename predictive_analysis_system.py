"""
HANAZONOシステム 予測分析システム v1.0
将来の問題予測・最適化提案・パフォーマンス予測
"""
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any
import logging
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalysisSystem:

    def __init__(self):
        self.setup_logging()
        self.data_dir = 'prediction_data'
        self.models_dir = 'prediction_models'
        self.reports_dir = 'prediction_reports'
        self.metrics_history = {}
        self.performance_history = {}
        self.error_patterns = {}
        self.models = {'resource_usage': None, 'error_frequency': None, 'performance_trend': None, 'maintenance_schedule': None}
        self.initialize_directories()

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('predictive_analysis.log'), logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)

    def initialize_directories(self):
        """ディレクトリ初期化"""
        for directory in [self.data_dir, self.models_dir, self.reports_dir]:
            os.makedirs(directory, exist_ok=True)

    def collect_historical_data(self) -> Dict:
        """履歴データ収集"""
        historical_data = {'system_metrics': self.collect_system_metrics(), 'error_logs': self.collect_error_logs(), 'performance_data': self.collect_performance_data(), 'usage_patterns': self.collect_usage_patterns(), 'maintenance_history': self.collect_maintenance_history()}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(self.data_dir, f'historical_data_{timestamp}.json')
        with open(data_file, 'w') as f:
            json.dump(historical_data, f, indent=2, default=str)
        self.logger.info(f'履歴データ収集完了: {data_file}')
        return historical_data

    def collect_system_metrics(self) -> List[Dict]:
        """システムメトリクス収集"""
        metrics = []
        try:
            log_files = ['monitoring_logs/system_monitor.log']
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        for line in f:
                            if 'CPU:' in line and 'MEM:' in line:
                                parts = line.strip().split(',')
                                if len(parts) >= 4:
                                    timestamp = parts[0]
                                    cpu = int(parts[1].split(':')[1].replace('%', ''))
                                    memory = int(parts[2].split(':')[1].replace('%', ''))
                                    disk = int(parts[3].split(':')[1].replace('%', ''))
                                    metrics.append({'timestamp': timestamp, 'cpu_usage': cpu, 'memory_usage': memory, 'disk_usage': disk})
        except Exception as e:
            self.logger.error(f'システムメトリクス収集エラー: {e}')
        return metrics

    def collect_error_logs(self) -> List[Dict]:
        """エラーログ収集"""
        errors = []
        try:
            log_files = ['monitoring_logs/alerts.log', 'ai_auto_fix.log', 'predictive_analysis.log']
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        for line_num, line in enumerate(f, 1):
                            if any((keyword in line.lower() for keyword in ['error', 'exception', 'fail', 'warning'])):
                                errors.append({'file': log_file, 'line': line_num, 'timestamp': datetime.now().isoformat(), 'message': line.strip(), 'severity': self.classify_error_severity(line)})
        except Exception as e:
            self.logger.error(f'エラーログ収集エラー: {e}')
        return errors

    def collect_performance_data(self) -> List[Dict]:
        """パフォーマンスデータ収集"""
        performance = []
        try:
            import subprocess
            import time
            tests = [('git_status', 'git status --porcelain'), ('python_import', 'python3 -c "import main"'), ('file_read', 'cat settings.json')]
            for test_name, command in tests:
                start_time = time.time()
                try:
                    subprocess.run(command.split(), capture_output=True, timeout=10)
                    execution_time = time.time() - start_time
                    performance.append({'test_name': test_name, 'execution_time': execution_time, 'timestamp': datetime.now().isoformat(), 'status': 'success'})
                except Exception as e:
                    execution_time = time.time() - start_time
                    performance.append({'test_name': test_name, 'execution_time': execution_time, 'timestamp': datetime.now().isoformat(), 'status': 'failed', 'error': str(e)})
        except Exception as e:
            self.logger.error(f'パフォーマンスデータ収集エラー: {e}')
        return performance

    def collect_usage_patterns(self) -> Dict:
        """使用パターン収集"""
        patterns = {'file_access_frequency': {}, 'command_usage': {}, 'time_patterns': {}, 'seasonal_usage': {}}
        try:
            important_files = ['main.py', 'email_notifier.py', 'settings.json']
            for file_path in important_files:
                if os.path.exists(file_path):
                    stat = os.stat(file_path)
                    patterns['file_access_frequency'][file_path] = {'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(), 'last_accessed': datetime.fromtimestamp(stat.st_atime).isoformat(), 'size': stat.st_size}
            try:
                import subprocess
                git_log = subprocess.run(['git', 'log', '--oneline', '-n', '50'], capture_output=True, text=True)
                commits_by_hour = {}
                for line in git_log.stdout.split('\n'):
                    if line:
                        hour = datetime.now().hour
                        commits_by_hour[hour] = commits_by_hour.get(hour, 0) + 1
                patterns['time_patterns']['commits_by_hour'] = commits_by_hour
            except Exception as e:
                self.logger.warning(f'Git履歴分析エラー: {e}')
        except Exception as e:
            self.logger.error(f'使用パターン収集エラー: {e}')
        return patterns

    def collect_maintenance_history(self) -> List[Dict]:
        """メンテナンス履歴収集"""
        maintenance = []
        try:
            backup_dirs = ['ai_auto_fix_backups', 'system_backups', 'temp_excluded']
            for backup_dir in backup_dirs:
                if os.path.exists(backup_dir):
                    for file_name in os.listdir(backup_dir):
                        file_path = os.path.join(backup_dir, file_name)
                        if os.path.isfile(file_path):
                            stat = os.stat(file_path)
                            maintenance.append({'type': 'backup', 'file': file_name, 'timestamp': datetime.fromtimestamp(stat.st_ctime).isoformat(), 'size': stat.st_size})
        except Exception as e:
            self.logger.error(f'メンテナンス履歴収集エラー: {e}')
        return maintenance

    def classify_error_severity(self, error_message: str) -> str:
        """エラー重要度分類"""
        error_lower = error_message.lower()
        if any((keyword in error_lower for keyword in ['critical', 'fatal', 'emergency'])):
            return 'critical'
        elif any((keyword in error_lower for keyword in ['error', 'exception', 'fail'])):
            return 'high'
        elif any((keyword in error_lower for keyword in ['warning', 'warn'])):
            return 'medium'
        else:
            return 'low'

    def build_prediction_models(self, historical_data: Dict) -> Dict:
        """予測モデル構築"""
        models_built = {}
        try:
            if historical_data['system_metrics']:
                resource_model = self.build_resource_usage_model(historical_data['system_metrics'])
                models_built['resource_usage'] = resource_model
            if historical_data['error_logs']:
                error_model = self.build_error_frequency_model(historical_data['error_logs'])
                models_built['error_frequency'] = error_model
            if historical_data['performance_data']:
                performance_model = self.build_performance_trend_model(historical_data['performance_data'])
                models_built['performance_trend'] = performance_model
            if historical_data['maintenance_history']:
                maintenance_model = self.build_maintenance_schedule_model(historical_data['maintenance_history'])
                models_built['maintenance_schedule'] = maintenance_model
        except Exception as e:
            self.logger.error(f'予測モデル構築エラー: {e}')
        return models_built

    def build_resource_usage_model(self, metrics_data: List[Dict]) -> Dict:
        """リソース使用量予測モデル構築"""
        try:
            if len(metrics_data) < 5:
                return {'status': 'insufficient_data', 'min_required': 5}
            df = pd.DataFrame(metrics_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['minute_of_day'] = df['timestamp'].dt.hour * 60 + df['timestamp'].dt.minute
            df['cpu_ma'] = df['cpu_usage'].rolling(window=3, min_periods=1).mean()
            df['memory_ma'] = df['memory_usage'].rolling(window=3, min_periods=1).mean()
            features = ['hour', 'day_of_week', 'minute_of_day', 'cpu_ma', 'memory_ma']
            X = df[features].fillna(0)
            models = {}
            y_cpu = df['cpu_usage']
            cpu_model = RandomForestRegressor(n_estimators=50, random_state=42)
            cpu_model.fit(X, y_cpu)
            models['cpu'] = cpu_model
            y_memory = df['memory_usage']
            memory_model = RandomForestRegressor(n_estimators=50, random_state=42)
            memory_model.fit(X, y_memory)
            models['memory'] = memory_model
            model_file = os.path.join(self.models_dir, 'resource_usage_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump({'models': models, 'features': features, 'data_stats': df.describe().to_dict()}, f)
            return {'status': 'success', 'models_created': list(models.keys()), 'features': features, 'data_points': len(df), 'model_file': model_file}
        except Exception as e:
            self.logger.error(f'リソース予測モデル構築エラー: {e}')
            return {'status': 'error', 'message': str(e)}

    def build_error_frequency_model(self, error_data: List[Dict]) -> Dict:
        """エラー頻度予測モデル構築"""
        try:
            if len(error_data) < 3:
                return {'status': 'insufficient_data', 'min_required': 3}
            df = pd.DataFrame(error_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            severity_counts = df['severity'].value_counts().to_dict()
            hourly_errors = df.groupby('hour').size()
            daily_errors = df.groupby('day_of_week').size()
            error_prediction = {'hourly_average': hourly_errors.mean(), 'peak_hours': hourly_errors.idxmax() if len(hourly_errors) > 0 else None, 'severity_distribution': severity_counts, 'total_errors': len(error_data), 'prediction_next_24h': hourly_errors.mean() * 24}
            model_file = os.path.join(self.models_dir, 'error_frequency_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(error_prediction, f)
            return {'status': 'success', 'prediction': error_prediction, 'model_file': model_file}
        except Exception as e:
            self.logger.error(f'エラー頻度モデル構築エラー: {e}')
            return {'status': 'error', 'message': str(e)}

    def build_performance_trend_model(self, performance_data: List[Dict]) -> Dict:
        """パフォーマンス傾向予測モデル構築"""
        try:
            if len(performance_data) < 3:
                return {'status': 'insufficient_data', 'min_required': 3}
            df = pd.DataFrame(performance_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            success_rate = (df['status'] == 'success').mean()
            successful_tests = df[df['status'] == 'success']
            avg_execution_times = successful_tests.groupby('test_name')['execution_time'].agg(['mean', 'std', 'min', 'max']).to_dict()
            trends = {}
            for test_name in df['test_name'].unique():
                test_data = df[df['test_name'] == test_name]
                if len(test_data) >= 2:
                    X = np.array(range(len(test_data))).reshape(-1, 1)
                    y = test_data['execution_time'].values
                    model = LinearRegression()
                    model.fit(X, y)
                    trends[test_name] = {'slope': model.coef_[0], 'intercept': model.intercept_, 'trend': 'improving' if model.coef_[0] < 0 else 'degrading'}
            performance_model = {'success_rate': success_rate, 'avg_execution_times': avg_execution_times, 'trends': trends, 'total_tests': len(performance_data)}
            model_file = os.path.join(self.models_dir, 'performance_trend_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(performance_model, f)
            return {'status': 'success', 'model': performance_model, 'model_file': model_file}
        except Exception as e:
            self.logger.error(f'パフォーマンス傾向モデル構築エラー: {e}')
            return {'status': 'error', 'message': str(e)}

    def build_maintenance_schedule_model(self, maintenance_data: List[Dict]) -> Dict:
        """メンテナンススケジュール予測モデル構築"""
        try:
            if len(maintenance_data) < 2:
                return {'status': 'insufficient_data', 'min_required': 2}
            df = pd.DataFrame(maintenance_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            intervals = []
            for i in range(1, len(df)):
                interval = (df.iloc[i]['timestamp'] - df.iloc[i - 1]['timestamp']).total_seconds() / 3600
                intervals.append(interval)
            if intervals:
                avg_interval = np.mean(intervals)
                next_maintenance = df['timestamp'].max() + timedelta(hours=avg_interval)
                maintenance_model = {'average_interval_hours': avg_interval, 'next_predicted_maintenance': next_maintenance.isoformat(), 'maintenance_types': df['type'].value_counts().to_dict(), 'total_maintenances': len(maintenance_data)}
            else:
                maintenance_model = {'average_interval_hours': 168, 'next_predicted_maintenance': (datetime.now() + timedelta(days=7)).isoformat(), 'maintenance_types': df['type'].value_counts().to_dict(), 'total_maintenances': len(maintenance_data)}
            model_file = os.path.join(self.models_dir, 'maintenance_schedule_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(maintenance_model, f)
            return {'status': 'success', 'model': maintenance_model, 'model_file': model_file}
        except Exception as e:
            self.logger.error(f'メンテナンススケジュールモデル構築エラー: {e}')
            return {'status': 'error', 'message': str(e)}

    def generate_predictions(self, prediction_horizon_days: int=7) -> Dict:
        """予測生成"""
        predictions = {'prediction_date': datetime.now().isoformat(), 'horizon_days': prediction_horizon_days, 'resource_usage': {}, 'error_frequency': {}, 'performance_trends': {}, 'maintenance_schedule': {}, 'recommendations': []}
        try:
            resource_file = os.path.join(self.models_dir, 'resource_usage_model.pkl')
            if os.path.exists(resource_file):
                predictions['resource_usage'] = self.predict_resource_usage(resource_file, prediction_horizon_days)
            error_file = os.path.join(self.models_dir, 'error_frequency_model.pkl')
            if os.path.exists(error_file):
                predictions['error_frequency'] = self.predict_error_frequency(error_file, prediction_horizon_days)
            performance_file = os.path.join(self.models_dir, 'performance_trend_model.pkl')
            if os.path.exists(performance_file):
                predictions['performance_trends'] = self.predict_performance_trends(performance_file, prediction_horizon_days)
            maintenance_file = os.path.join(self.models_dir, 'maintenance_schedule_model.pkl')
            if os.path.exists(maintenance_file):
                predictions['maintenance_schedule'] = self.predict_maintenance_schedule(maintenance_file, prediction_horizon_days)
            predictions['recommendations'] = self.generate_recommendations(predictions)
        except Exception as e:
            self.logger.error(f'予測生成エラー: {e}')
            predictions['error'] = str(e)
        return predictions

    def predict_resource_usage(self, model_file: str, days: int) -> Dict:
        """リソース使用量予測"""
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            models = model_data['models']
            features = model_data['features']
            future_predictions = {}
            for hour in range(0, 24, 4):
                for day_of_week in range(7):
                    minute_of_day = hour * 60
                    feature_values = [hour, day_of_week, minute_of_day, 50, 60]
                    if len(feature_values) == len(features):
                        X_pred = np.array(feature_values).reshape(1, -1)
                        cpu_pred = models['cpu'].predict(X_pred)[0]
                        memory_pred = models['memory'].predict(X_pred)[0]
                        time_key = f'day_{day_of_week}_hour_{hour}'
                        future_predictions[time_key] = {'cpu_usage': max(0, min(100, cpu_pred)), 'memory_usage': max(0, min(100, memory_pred))}
            high_usage_periods = []
            for time_key, pred in future_predictions.items():
                if pred['cpu_usage'] > 80 or pred['memory_usage'] > 85:
                    high_usage_periods.append({'time': time_key, 'cpu': pred['cpu_usage'], 'memory': pred['memory_usage']})
            return {'status': 'success', 'predictions': future_predictions, 'high_usage_periods': high_usage_periods, 'summary': {'avg_cpu': np.mean([p['cpu_usage'] for p in future_predictions.values()]), 'avg_memory': np.mean([p['memory_usage'] for p in future_predictions.values()]), 'peak_cpu': max([p['cpu_usage'] for p in future_predictions.values()]), 'peak_memory': max([p['memory_usage'] for p in future_predictions.values()])}}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def predict_error_frequency(self, model_file: str, days: int) -> Dict:
        """エラー頻度予測"""
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            predicted_errors = model_data['prediction_next_24h'] * days
            severity_dist = model_data['severity_distribution']
            return {'status': 'success', 'predicted_total_errors': predicted_errors, 'predicted_by_severity': {severity: count / sum(severity_dist.values()) * predicted_errors for severity, count in severity_dist.items()}, 'peak_error_hours': model_data.get('peak_hours', []), 'recommendation': 'critical' if predicted_errors > 10 else 'normal'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def predict_performance_trends(self, model_file: str, days: int) -> Dict:
        """パフォーマンス傾向予測"""
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            trends = model_data['trends']
            future_performance = {}
            for test_name, trend_data in trends.items():
                slope = trend_data['slope']
                intercept = trend_data['intercept']
                future_value = intercept + slope * days
                future_performance[test_name] = {'predicted_execution_time': max(0, future_value), 'trend': trend_data['trend'], 'change_from_current': slope * days}
            return {'status': 'success', 'future_performance': future_performance, 'overall_trend': 'improving' if sum((t['slope'] for t in trends.values())) < 0 else 'degrading'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def predict_maintenance_schedule(self, model_file: str, days: int) -> Dict:
        """メンテナンススケジュール予測"""
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            next_maintenance = datetime.fromisoformat(model_data['next_predicted_maintenance'])
            days_until_maintenance = (next_maintenance - datetime.now()).days
            return {'status': 'success', 'next_maintenance_date': next_maintenance.isoformat(), 'days_until_maintenance': days_until_maintenance, 'urgency': 'high' if days_until_maintenance < 3 else 'normal', 'maintenance_types': model_data['maintenance_types']}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def generate_recommendations(self, predictions: Dict) -> List[str]:
        """推奨事項生成"""
        recommendations = []
        try:
            if predictions['resource_usage'].get('status') == 'success':
                resource_data = predictions['resource_usage']
                if resource_data['summary']['peak_cpu'] > 90:
                    recommendations.append('🔥 CPU使用率が90%を超える予測。処理の分散化を検討してください')
                if resource_data['summary']['peak_memory'] > 95:
                    recommendations.append('💾 メモリ使用率が95%を超える予測。メモリ最適化が必要です')
                if len(resource_data['high_usage_periods']) > 5:
                    recommendations.append('⚡ 高負荷期間が多数予測されます。システム拡張を検討してください')
            if predictions['error_frequency'].get('status') == 'success':
                error_data = predictions['error_frequency']
                if error_data['predicted_total_errors'] > 20:
                    recommendations.append('🚨 高頻度のエラーが予測されます。ログ監視を強化してください')
                if error_data.get('recommendation') == 'critical':
                    recommendations.append('⚠️ クリティカルエラーの増加が予測されます。予防的メンテナンスを実施してください')
            if predictions['performance_trends'].get('status') == 'success':
                perf_data = predictions['performance_trends']
                if perf_data['overall_trend'] == 'degrading':
                    recommendations.append('📉 システムパフォーマンスの低下傾向。最適化作業が推奨されます')
            if predictions['maintenance_schedule'].get('status') == 'success':
                maint_data = predictions['maintenance_schedule']
                if maint_data['urgency'] == 'high':
                    recommendations.append(f"🔧 {maint_data['days_until_maintenance']}日以内にメンテナンスが必要です")
            current_month = datetime.now().month
            if 6 <= current_month <= 8:
                recommendations.append('🌡️ 夏季期間：システム温度監視を強化し、冷却に注意してください')
            elif 12 <= current_month <= 2:
                recommendations.append('❄️ 冬季期間：電力消費が増加する傾向があります。充電設定を確認してください')
            if not recommendations:
                recommendations.append('✅ 現在の予測では重大な問題は検出されていません。定期的な監視を継続してください')
        except Exception as e:
            recommendations.append(f'⚠️ 推奨事項生成中にエラーが発生: {str(e)}')
        return recommendations

    def generate_comprehensive_report(self, predictions: Dict) -> str:
        """包括的レポート生成"""
        report = f"\n🔮 HANAZONOシステム 予測分析レポート v1.0\n生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n予測期間: {predictions['horizon_days']}日間\n\n📊 予測サマリー:\n"
        if predictions['resource_usage'].get('status') == 'success':
            resource = predictions['resource_usage']['summary']
            report += f"\n🖥️ リソース使用量予測:\n  - 平均CPU使用率: {resource['avg_cpu']:.1f}%\n  - 平均メモリ使用率: {resource['avg_memory']:.1f}%\n  - 最大CPU使用率: {resource['peak_cpu']:.1f}%\n  - 最大メモリ使用率: {resource['peak_memory']:.1f}%\n  - 高負荷期間: {len(predictions['resource_usage']['high_usage_periods'])}回\n"
        if predictions['error_frequency'].get('status') == 'success':
            error = predictions['error_frequency']
            report += f"\n🚨 エラー頻度予測:\n  - 予測総エラー数: {error['predicted_total_errors']:.1f}件\n  - 重要度分布: {error['predicted_by_severity']}\n  - 推奨レベル: {error['recommendation']}\n"
        if predictions['performance_trends'].get('status') == 'success':
            perf = predictions['performance_trends']
            report += f"\n⚡ パフォーマンス傾向:\n  - 全体的傾向: {perf['overall_trend']}\n  - 詳細予測:\n"
            for test_name, pred in perf['future_performance'].items():
                report += f"    - {test_name}: {pred['predicted_execution_time']:.3f}秒 ({pred['trend']})\n"
        if predictions['maintenance_schedule'].get('status') == 'success':
            maint = predictions['maintenance_schedule']
            next_date = datetime.fromisoformat(maint['next_maintenance_date']).strftime('%Y-%m-%d')
            report += f"\n🔧 メンテナンススケジュール:\n  - 次回メンテナンス予定: {next_date}\n  - 残り日数: {maint['days_until_maintenance']}日\n  - 緊急度: {maint['urgency']}\n"
        report += '\n💡 推奨事項:\n'
        for i, recommendation in enumerate(predictions['recommendations'], 1):
            report += f'  {i}. {recommendation}\n'
        report += f"\n⚠️ 注意事項:\n- 予測は過去のデータに基づいており、実際の結果と異なる場合があります\n- 定期的なモデル更新により精度向上を図っています\n- 予測精度は継続的な監視により改善されます\n\n📈 次回予測更新予定: {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}\n"
        return report

def main():
    """メイン実行"""
    print('🔮 HANAZONOシステム 予測分析システム v1.0')
    print('=' * 60)
    predictor = PredictiveAnalysisSystem()
    try:
        print('📊 履歴データ収集中...')
        historical_data = predictor.collect_historical_data()
        print('🧠 予測モデル構築中...')
        models_built = predictor.build_prediction_models(historical_data)
        print('構築されたモデル:')
        for model_name, result in models_built.items():
            status = result.get('status', 'unknown')
            print(f'  - {model_name}: {status}')
        print('\n🔮 予測生成中...')
        predictions = predictor.generate_predictions(prediction_horizon_days=7)
        print('📄 レポート生成中...')
        report = predictor.generate_comprehensive_report(predictions)
        print('\n' + report)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = os.path.join(predictor.reports_dir, f'prediction_report_{timestamp}.txt')
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f'\n📁 詳細レポート保存: {report_filename}')
        prediction_filename = os.path.join(predictor.reports_dir, f'predictions_{timestamp}.json')
        with open(prediction_filename, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2, default=str)
        print(f'📊 予測データ保存: {prediction_filename}')
        print('\n🎉 予測分析システム実行完了!')
    except Exception as e:
        predictor.logger.error(f'メイン実行エラー: {e}')
        print(f'❌ エラーが発生しました: {e}')
if __name__ == '__main__':
    main()