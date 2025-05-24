#!/usr/bin/env python3
import time
import threading
from datetime import datetime

class ConnectionManager:
    def __init__(self, min_interval=30):
        self.min_interval = min_interval
        self.last_access = {}
        self.lock = threading.Lock()
    
    def can_access(self, target='inverter'):
        with self.lock:
            now = datetime.now()
            if target in self.last_access:
                elapsed = (now - self.last_access[target]).total_seconds()
                if elapsed < self.min_interval:
                    return False, self.min_interval - elapsed
            self.last_access[target] = now
            return True, 0
    
    def wait_if_needed(self, target='inverter'):
        can_access, wait_time = self.can_access(target)
        if not can_access:
            print(f"接続制御: {wait_time:.1f}秒待機中...")
            time.sleep(wait_time)
            return self.can_access(target)
        return True, 0

connection_manager = ConnectionManager()
