"""LVYUAN インバーターのレジスタマップ定義（SRNE互換）"""
SETTINGS_REGISTERS = {57345: {'name': 'PV_Charge_Current', 'unit': 'A', 'factor': 0.1, 'access': 'RW', 'range': (0, 100), 'default': 60}, 57866: {'name': 'Max_Charge_Current', 'unit': 'A', 'factor': 0.1, 'access': 'RW', 'range': (0, 150), 'default': 80}, 57361: {'name': 'Equalizing_Charge_Time', 'unit': 'min', 'factor': 1, 'access': 'RW', 'range': (0, 600), 'default': 120}, 57362: {'name': 'Boost_Charge_Time', 'unit': 'min', 'factor': 1, 'access': 'RW', 'range': (10, 600), 'default': 120}, 57363: {'name': 'Equalizing_Charge_Interval', 'unit': 'day', 'factor': 1, 'access': 'RW', 'range': (0, 255), 'default': 30}, 57379: {'name': 'Equalizing_Charge_Timeout', 'unit': 'min', 'factor': 1, 'access': 'RW', 'range': (5, 900), 'default': 240}, 57359: {'name': 'SOC_Cutoff', 'unit': '%', 'factor': 1, 'access': 'RW', 'range': (0, 100), 'default': 5, 'note': 'High 8bits: Charge cutoff SOC, Low 8bits: Discharge cutoff SOC'}}
MEASUREMENT_REGISTERS = {256: {'name': 'Battery_SOC', 'unit': '%', 'factor': 1}, 257: {'name': 'Battery_Voltage', 'unit': 'V', 'factor': 0.1}, 258: {'name': 'Battery_Current', 'unit': 'A', 'factor': 0.1}}
REGISTER_GROUPS = [{'start': 256, 'count': 20, 'name': 'Battery Measurements'}, {'start': 57344, 'count': 20, 'name': 'Basic Settings'}, {'start': 57856, 'count': 20, 'name': 'Advanced Settings'}]

def encode_soc_cutoff(charge_cutoff, discharge_cutoff):
    """充電カットオフSOCと放電カットオフSOCを1つのレジスタ値に符号化"""
    return (charge_cutoff & 255) << 8 | discharge_cutoff & 255

def decode_soc_cutoff(register_value):
    """レジスタ値から充電カットオフSOCと放電カットオフSOCをデコード"""
    charge_cutoff = register_value >> 8 & 255
    discharge_cutoff = register_value & 255
    return (charge_cutoff, discharge_cutoff)