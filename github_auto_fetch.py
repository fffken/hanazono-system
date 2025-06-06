import os
import base64
import requests
import json

class GitHubAutoFetch:

    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.repo = 'fffken/hanazono-system'
        self.base_url = f'https://api.github.com/repos/{self.repo}'

    def get_file_content(self, file_path):
        """ファイル内容を取得"""
        url = f'{self.base_url}/contents/{file_path}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
        return None

    def get_file_list(self, path=''):
        """ファイル一覧を取得"""
        url = f'{self.base_url}/contents/{path}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
if __name__ == '__main__':
    fetcher = GitHubAutoFetch()
    print('✅ GitHub自動取得ツール準備完了')