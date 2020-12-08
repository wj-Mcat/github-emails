"""
*** - https://github.com/wj-Mcat/github-emails

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta
import time
import os
import json
import requests

from github_emails.access_limit import check_for_limit

from wechaty_puppet import get_logger   # type: ignore

# pylint: disable=invalid-name
logger = get_logger(__name__)

BASE_URL = 'https://api.github.com'


@dataclass
class GithubOptions:
    """github options"""

    token: Optional[str] = None


class GithubApi:
    """Github Restful Api"""
    def __init__(self, token: str):
        """initialization for github client"""
        self.headers = {
            'accept': 'application/vnd.github.v3+json',
            'authorization': 'token ' + token
        }

    def check_for_limit(self):
        """get the rate limit"""
        res = requests.get(f'{BASE_URL}/rate_limit', headers=self.headers)
        result = res.json()
        if 'resources' in result and 'core' in result['resources']:
            core = result['resources']['core']
            if core['remaining'] == 0:
                wait_time = datetime.fromtimestamp(core['reset']) - datetime.now()
                logger.warning('sleep for the seconds: %s', str(wait_time))
                time.sleep(wait_time.seconds + 1)

    def get_repo_stargazers(self, owner: str, repo: str):
        """get the repo stargazers"""
        logger.info('get_repo_stargazers(%s, %s)', owner, repo)

        page_index = 0

        # 1. check for the temp dir
        root_dir = os.getcwd()
        info_dir = os.path.join(root_dir, 'github_info')
        if not os.path.exists(info_dir):
            os.mkdir(info_dir)

        # 2. get info
        while True:
            self.check_for_limit()
            logger.info('get_repo_stargazers(%s, %s) get data with page %s', owner, repo, page_index)

            res = requests.get(
                f'{BASE_URL}/repos/{owner}/{repo}/stargazers?per_page=100&page={page_index}',
                headers=self.headers
            )
            page_index += 1

            stargazers = res.json()

            if 'message' in stargazers:
                break
            if not isinstance(stargazers, list):
                break

            # 2.1 save the stargazers info into local file
            repo_file = os.path.join(info_dir, f'{owner}-{repo}.json')
            with open(repo_file, 'w+', encoding='utf-8') as f:
                content = f.read()
                data = {}
                if content:
                    data = json.loads(content)
                if 'stargazers' not in data:
                    data['stargazers'] = []
                data['stargazers'].extend(stargazers)
                json.dump(data, f)