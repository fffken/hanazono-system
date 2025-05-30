"""
システム健全性監視・自動修復システム
今回のようなバッテリー残量乖離問題の再発を防止
"""
import time
import json
import socket
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SystemHealthMonitor:
    """システム健全性を監視し、問題を早期発見・自動修復"""

    def __init__(self, config_path='settings.json'):
        self.config_path = config_path
        self.logger = self._setup_logger()
        self.health_log = []

    def _setup_logger(self):
        logger = logging.getLogger('health_monitor')
        handler = logging.FileHandler('logs/system_health.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def comprehensive_health_check(self) -> Dict:
        """包括的なシステム健全性チェック"""
        health_report = {'timestamp': datetime.now().isoformat(), 'overall_status': 'healthy', 'checks': {}}
        health_report['checks']['data_collection'] = self._check_data_collection()
        health_report['checks']['communication'] = self._check_communication_settings()
        health_report['checks']['data_structure'] = self._check_data_structure()
        health_report['checks']['email_function'] = self._check_email_function()
        health_report['checks']['config_integrity'] = self._check_config_integrity()
        failed_checks = [k for k, v in health_report['checks'].items() if not v['status']]
        if failed_checks:
            health_report['overall_status'] = 'warning' if len(failed_checks) <= 2 else 'critical'
            health_report['failed_checks'] = failed_checks
        self._log_health_report(health_report)
        return health_report

    def _check_data_collection(self) -> Dict:
        """データ収集機能の検証"""
        try:
            from lvyuan_collector import LVYUANCollector
            collector = LVYUANCollector()
            data = collector.collect_data()
            if data and isinstance(data, tuple) and (len(data) > 0):
                actual_data = data[0]
                if 'parameters' in actual_data:
                    soc_data = actual_data['parameters'].get('0x0100', {})
                    if 'value' in soc_data and soc_data['value'] != 'N/A':
                        return {'status': True, 'message': f"SOC正常取得: {soc_data['value']}%", 'soc_value': soc_data['value']}
                    else:
                        return {'status': False, 'message': 'SOC値が取得できません', 'auto_fix': 'communication_check'}
                else:
                    return {'status': False, 'message': 'parametersが見つかりません', 'auto_fix': 'data_structure_fix'}
            else:
                return {'status': False, 'message': 'データ収集が失敗しました', 'auto_fix': 'connection_repair'}
        except Exception as e:
            return {'status': False, 'message': f'データ収集エラー: {e}', 'auto_fix': 'module_repair'}

    def _check_communication_settings(self) -> Dict:
        """通信設定の検証"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            modbus_config = settings.get('modbus', {})
            host = modbus_config.get('host', '192.168.0.202')
            port = modbus_config.get('port', 502)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return {'status': True, 'message': f'通信正常: {host}:{port}', 'host': host, 'port': port}
            else:
                alternative_ports = [8899, 502, 4196]
                for alt_port in alternative_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    alt_result = sock.connect_ex((host, alt_port))
                    sock.close()
                    if alt_result == 0:
                        return {'status': False, 'message': f'設定ポート{port}は不可、ポート{alt_port}が利用可能', 'auto_fix': 'port_correction', 'correct_port': alt_port}
                return {'status': False, 'message': f'通信不可: {host}:{port}', 'auto_fix': 'network_diagnosis'}
        except Exception as e:
            return {'status': False, 'message': f'通信設定エラー: {e}', 'auto_fix': 'config_repair'}

    def _check_data_structure(self) -> Dict:
        """データ構造の検証"""
        try:
            from lvyuan_collector import LVYUANCollector
            collector = LVYUANCollector()
            data = collector.collect_data()
            structure_info = {'data_type': str(type(data)), 'is_tuple': isinstance(data, tuple), 'length': len(data) if data else 0}
            if isinstance(data, tuple) and len(data) > 0:
                actual_data = data[0]
                structure_info['first_element_type'] = str(type(actual_data))
                structure_info['has_parameters'] = 'parameters' in actual_data if isinstance(actual_data, dict) else False
                if isinstance(actual_data, dict) and 'parameters' in actual_data:
                    params = actual_data['parameters']
                    structure_info['parameter_count'] = len(params)
                    structure_info['has_soc'] = '0x0100' in params
                    return {'status': True, 'message': 'データ構造正常', 'structure': structure_info}
                else:
                    return {'status': False, 'message': 'データ構造異常: parametersキーが見つかりません', 'structure': structure_info, 'auto_fix': 'structure_adaptation'}
            else:
                return {'status': False, 'message': 'データ構造異常: 期待される形式ではありません', 'structure': structure_info, 'auto_fix': 'data_format_fix'}
        except Exception as e:
            return {'status': False, 'message': f'データ構造チェックエラー: {e}', 'auto_fix': 'collector_repair'}

    def _check_email_function(self) -> Dict:
        """メール機能の検証"""
        try:
            from email_notifier import EmailNotifier
            from settings_manager import SettingsManager
            from lvyuan_collector import LVYUANCollector
            collector = LVYUANCollector()
            data = collector.collect_data()
            config = SettingsManager()
            notifier = EmailNotifier(config, self.logger)
            battery_info = notifier._extract_battery_info(data)
            if 'エラー' not in battery_info and 'データなし' not in battery_info:
                return {'status': True, 'message': 'メール機能正常', 'sample_output': battery_info[:100] + '...' if len(battery_info) > 100 else battery_info}
            else:
                return {'status': False, 'message': f'メール機能異常: {battery_info}', 'auto_fix': 'email_repair'}
        except Exception as e:
            return {'status': False, 'message': f'メール機能エラー: {e}', 'auto_fix': 'email_module_repair'}

    def _check_config_integrity(self) -> Dict:
        """設定ファイルの整合性確認"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            required_sections = ['modbus', 'notification']
            missing_sections = [section for section in required_sections if section not in settings]
            if missing_sections:
                return {'status': False, 'message': f'設定不備: {missing_sections}が見つかりません', 'auto_fix': 'config_completion'}
            return {'status': True, 'message': '設定ファイル正常', 'sections': list(settings.keys())}
        except Exception as e:
            return {'status': False, 'message': f'設定ファイルエラー: {e}', 'auto_fix': 'config_restoration'}

    def auto_repair(self, health_report: Dict) -> Dict:
        """問題の自動修復"""
        repair_results = {}
        for check_name, check_result in health_report['checks'].items():
            if not check_result['status'] and 'auto_fix' in check_result:
                fix_type = check_result['auto_fix']
                repair_results[check_name] = self._execute_repair(fix_type, check_result)
        return repair_results

    def _execute_repair(self, fix_type: str, check_result: Dict) -> Dict:
        """修復の実行"""
        try:
            if fix_type == 'port_correction':
                return self._fix_port_setting(check_result.get('correct_port'))
            elif fix_type == 'config_completion':
                return self._complete_config()
            elif fix_type == 'structure_adaptation':
                return self._adapt_data_structure()
            else:
                return {'status': False, 'message': f'未対応の修復タイプ: {fix_type}'}
        except Exception as e:
            return {'status': False, 'message': f'修復エラー: {e}'}

    def _fix_port_setting(self, correct_port: int) -> Dict:
        """ポート設定の修正"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            if 'modbus' not in settings:
                settings['modbus'] = {}
            old_port = settings['modbus'].get('port', '未設定')
            settings['modbus']['port'] = correct_port
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            self.logger.info(f'ポート設定を自動修正: {old_port} → {correct_port}')
            return {'status': True, 'message': f'ポート設定を{old_port}から{correct_port}に自動修正'}
        except Exception as e:
            return {'status': False, 'message': f'ポート修正失敗: {e}'}

    def _complete_config(self) -> Dict:
        """設定の補完"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            if 'modbus' not in settings:
                settings['modbus'] = {'host': '192.168.0.202', 'port': 8899, 'timeout': 5}
            if 'notification' not in settings:
                settings['notification'] = {'email': {'enabled': True}}
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return {'status': True, 'message': '設定ファイルを自動補完'}
        except Exception as e:
            return {'status': False, 'message': f'設定補完失敗: {e}'}

    def _adapt_data_structure(self) -> Dict:
        """データ構造への適応（ログ記録のみ）"""
        self.logger.warning('データ構造の変更を検出。email_notifier.pyの確認が必要です。')
        return {'status': True, 'message': 'データ構造変更をログに記録。手動確認が推奨されます。'}

    def _log_health_report(self, health_report: Dict):
        """健全性レポートのログ記録"""
        status = health_report['overall_status']
        self.logger.info(f'システム健全性チェック完了: {status}')
        for check_name, result in health_report['checks'].items():
            level = logging.INFO if result['status'] else logging.WARNING
            self.logger.log(level, f"{check_name}: {result['message']}")

    def generate_health_report(self) -> str:
        """人間が読める形式の健全性レポート生成"""
        health_data = self.comprehensive_health_check()
        report = f"\nHANAZONOシステム 健全性レポート\n生成日時: {health_data['timestamp']}\n総合ステータス: {health_data['overall_status'].upper()}\n\n=== チェック結果詳細 ===\n"
        for check_name, result in health_data['checks'].items():
            status_emoji = '✅' if result['status'] else '❌'
            report += f"{status_emoji} {check_name}: {result['message']}\n"
        if health_data['overall_status'] != 'healthy':
            report += f'\n=== 推奨アクション ===\n'
            for check_name, result in health_data['checks'].items():
                if not result['status'] and 'auto_fix' in result:
                    report += f'- {check_name}: 自動修復可能\n'
        return report

def run_health_check():
    """健全性チェックの実行"""
    monitor = SystemHealthMonitor()
    print('=== システム健全性チェック実行中 ===')
    health_report = monitor.comprehensive_health_check()
    print(monitor.generate_health_report())
    if health_report['overall_status'] != 'healthy':
        print('\n=== 自動修復実行中 ===')
        repair_results = monitor.auto_repair(health_report)
        for check_name, repair_result in repair_results.items():
            status_emoji = '✅' if repair_result['status'] else '❌'
            print(f"{status_emoji} {check_name}: {repair_result['message']}")
    return health_report
if __name__ == '__main__':
    run_health_check()

class HealthConnectionManager:

    def __init__(self, min_interval=60):
        self.min_interval = min_interval
        self.last_check = None

    def should_run_full_check(self):
        """フルチェック実行の判定"""
        now = datetime.now()
        if self.last_check is None:
            self.last_check = now
            return True
        elapsed = (now - self.last_check).total_seconds()
        if elapsed >= self.min_interval:
            self.last_check = now
            return True
        return False

def run_controlled_health_check():
    """制御された健全性チェック"""
    controller = HealthConnectionManager()
    if controller.should_run_full_check():
        print('=== 完全健全性チェック実行 ===')
        return run_health_check()
    else:
        print('=== 軽量チェックのみ実行 ===')
        monitor = SystemHealthMonitor()
        health_report = {'timestamp': datetime.now().isoformat(), 'overall_status': 'healthy', 'checks': {'communication': monitor._check_communication_settings()}}
        return health_report

class HealthConnectionManager:

    def __init__(self, min_interval=60):
        self.min_interval = min_interval
        self.last_check = None

    def should_run_full_check(self):
        """フルチェック実行の判定"""
        now = datetime.now()
        if self.last_check is None:
            self.last_check = now
            return True
        elapsed = (now - self.last_check).total_seconds()
        if elapsed >= self.min_interval:
            self.last_check = now
            return True
        return False

def run_controlled_health_check():
    """制御された健全性チェック"""
    controller = HealthConnectionManager()
    if controller.should_run_full_check():
        print('=== 完全健全性チェック実行 ===')
        return run_health_check()
    else:
        print('=== 軽量チェックのみ実行 ===')
        monitor = SystemHealthMonitor()
        health_report = {'timestamp': datetime.now().isoformat(), 'overall_status': 'healthy', 'checks': {'communication': monitor._check_communication_settings()}}
        return health_report

class HealthConnectionManager:

    def __init__(self, min_interval=60):
        self.min_interval = min_interval
        self.last_check = None

    def should_run_full_check(self):
        """フルチェック実行の判定"""
        now = datetime.now()
        if self.last_check is None:
            self.last_check = now
            return True
        elapsed = (now - self.last_check).total_seconds()
        if elapsed >= self.min_interval:
            self.last_check = now
            return True
        return False

def run_controlled_health_check():
    """制御された健全性チェック"""
    controller = HealthConnectionManager()
    if controller.should_run_full_check():
        print('=== 完全健全性チェック実行 ===')
        return run_health_check()
    else:
        print('=== 軽量チェックのみ実行 ===')
        monitor = SystemHealthMonitor()
        health_report = {'timestamp': datetime.now().isoformat(), 'overall_status': 'healthy', 'checks': {'communication': monitor._check_communication_settings()}}
        return health_report