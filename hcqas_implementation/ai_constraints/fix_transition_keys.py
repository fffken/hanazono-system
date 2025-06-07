import re

# ファイル読み込み
with open('quantified_phase_transition.py', 'r') as f:
    content = f.read()

# PHASE_CRITERIA辞書のキー修正
old_pattern = r"'phase_3a_to_3b'"
new_pattern = r"'phase_3a_to_3b'"
content = content.replace("'phase_3a_to_3b':", "'phase_3a_to_3b':")
content = content.replace("'phase_3b_to_3c':", "'phase_3b_to_3c':")

# criteria_key生成部分の修正
old_line = 'criteria_key = f"{self.current_phase.value}_to_{target_phase.value}"'
new_line = 'criteria_key = f"{self.current_phase.value}_to_{target_phase.value}"'
content = content.replace(old_line, new_line)

# ファイル保存
with open('quantified_phase_transition.py', 'w') as f:
    f.write(content)

print("✅ 移行基準キー修正完了")
