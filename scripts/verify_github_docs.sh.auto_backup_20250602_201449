#!/bin/bash
echo "=== GitHub根幹文書確認 ==="

python3 -c "
from github_auto_fetch import GitHubAutoFetch
fetcher = GitHubAutoFetch()

docs = {
    'HANAZONO-SYSTEM-SETTINGS.md': 'docs/HANAZONO-SYSTEM-SETTINGS.md',
    'ROADMAP_COMPLETE.md': 'docs/ROADMAP_COMPLETE.md'
}

all_accessible = True
for name, path in docs.items():
    content = fetcher.get_file_content(path)
    if content:
        print(f'✅ {name}: {len(content)} 文字')
    else:
        print(f'❌ {name}: アクセス失敗')
        all_accessible = False

if all_accessible:
    print('🎯 全ての根幹文書にアクセス可能')
else:
    print('⚠️  GitHub文書アクセスに問題あり')
"
