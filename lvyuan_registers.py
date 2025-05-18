"""LVYUAN インバーターのレジスタマップ定義（SRNE互換）"""

# 設定関連レジスタ
SETTINGS_REGISTERS = {
    # 充電電流関連
    0xE001: {"name": "PV_Charge_Current", "unit": "A", "factor": 0.1, "access": "RW", "range": (0, 100), "default": 60},
    0xE20A: {"name": "Max_Charge_Current", "unit": "A", "factor": 0.1, "access": "RW", "range": (0, 150), "default": 80},
    
    # 充電時間関連
    0xE011: {"name": "Equalizing_Charge_Time", "unit": "min", "factor": 1, "access": "RW", "range": (0, 600), "default": 120},
    0xE012: {"name": "Boost_Charge_Time", "unit": "min", "factor": 1, "access": "RW", "range": (10, 600), "default": 120},
    0xE013: {"name": "Equalizing_Charge_Interval", "unit": "day", "factor": 1, "access": "RW", "range": (0, 255), "default": 30},
    0xE023: {"name": "Equalizing_Charge_Timeout", "unit": "min", "factor": 1, "access": "RW", "range": (5, 900), "default": 240},
    
    # SOC設定関連
    0xE00F: {"name": "SOC_Cutoff", "unit": "%", "factor": 1, "access": "RW", "range": (0, 100), "default": 5, 
             "note": "High 8bits: Charge cutoff SOC, Low 8bits: Discharge cutoff SOC"}
}

# 計測値レジスタ (テストで確認済み)
MEASUREMENT_REGISTERS = {
    0x0100: {"name": "Battery_SOC", "unit": "%", "factor": 1},
    0x0101: {"name": "Battery_Voltage", "unit": "V", "factor": 0.1},
    0x0102: {"name": "Battery_Current", "unit": "A", "factor": 0.1}
}

# レジスタグループ定義 (探索用)
REGISTER_GROUPS = [
    {"start": 0x0100, "count": 20, "name": "Battery Measurements"},
    {"start": 0xE000, "count": 20, "name": "Basic Settings"},
    {"start": 0xE200, "count": 20, "name": "Advanced Settings"}
]

# SOC設定値の操作ヘルパー関数
def encode_soc_cutoff(charge_cutoff, discharge_cutoff):
    """充電カットオフSOCと放電カットオフSOCを1つのレジスタ値に符号化"""
    return ((charge_cutoff & 0xFF) << 8) | (discharge_cutoff & 0xFF)

def decode_soc_cutoff(register_value):
    """レジスタ値から充電カットオフSOCと放電カットオフSOCをデコード"""
    charge_cutoff = (register_value >> 8) & 0xFF
    discharge_cutoff = register_value & 0xFF
    return charge_cutoff, discharge_cutoff
