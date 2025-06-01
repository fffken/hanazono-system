import re
import os

# email_notifier.pyを読み込み
with open('email_notifier.py', 'r') as f:
    content = f.read()

# 環境変数展開関数を追加
env_expand_func = '''
import os
import re

def expand_env_vars(config):
    """環境変数を展開"""
    def replace_env_var(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    
    if isinstance(config, dict):
        return {k: expand_env_vars(v) for k, v in config.items()}
    elif isinstance(config, str):
        return re.sub(r'\\$\\{([^}]+)\\}', replace_env_var, config)
    else:
        return config

'''

# __init__メソッドで設定を展開するように修正
new_init_line = "        self.config = expand_env_vars(config)"
content = content.replace("        self.config = config", new_init_line)

# 関数をファイルの先頭（import文の後）に挿入
import_end = content.find('class EnhancedEmailNotifier:')
content = content[:import_end] + env_expand_func + content[import_end:]

# ファイルを保存
with open('email_notifier.py', 'w') as f:
    f.write(content)

print("✅ 環境変数展開機能を追加しました")
