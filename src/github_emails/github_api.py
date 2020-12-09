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
from typing import Optional, List, Union, Dict
from datetime import datetime
import time
import os
import requests
from wechaty_puppet import get_logger  # type: ignore

from github_emails.config import CACHE_DIR, EMAIL_FILE

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

    def _check_for_limit(self):
        """get the rate limit"""
        res = requests.get(f'{BASE_URL}/rate_limit', headers=self.headers)
        result = res.json()
        if 'resources' in result and 'core' in result['resources']:
            core = result['resources']['core']
            if core['remaining'] == 0:
                wait_time = datetime.fromtimestamp(core['reset']) - datetime.now()
                logger.warning('sleep for the seconds: %s', str(wait_time))
                time.sleep(wait_time.seconds + 1)

    @staticmethod
    def _init_cache_dir() -> str:
        """init the cache data dir"""
        root_dir = os.getcwd()
        cache_dir = os.path.join(root_dir, CACHE_DIR)
        if not os.path.exists(cache_dir):
            logger.info('init cache dir: <%s>', CACHE_DIR)
            os.mkdir(cache_dir)
        email_cache_file = os.path.join(cache_dir, EMAIL_FILE)
        if not os.path.exists(email_cache_file):
            with open(email_cache_file, 'w', encoding='utf-8') as f:
                f.write('')
        return cache_dir

    def stargazers(self, owner: str, repo: str) -> List[str]:
        """get the repo stargazers"""
        logger.info('stargazers(%s, %s)', owner, repo)

        page_index = 1

        # 1. check for the temp dir
        cache_dir = self._init_cache_dir()

        # 2. get info
        repo_file = os.path.join(cache_dir, f'{owner}-{repo}-stargazers.json')
        while True:
            self._check_for_limit()

            res = requests.get(
                f'{BASE_URL}/repos/{owner}/{repo}/stargazers?per_page=100&page={page_index}',
                headers=self.headers
            )
            page_index += 1
            stargazers = res.json()

            logger.info(
                'repo<%s/%s>: stargazers in page<%d>, total<%d>',
                owner, repo, page_index,
                (page_index - 1) * 100 + len(stargazers)
            )

            if 'message' in stargazers:
                break
            if not stargazers or not isinstance(stargazers, list):
                break

            # 2.1 save the stargazers info into local file
            with open(repo_file, 'a+', encoding='utf-8') as f:
                for stargazer in stargazers:
                    f.write(stargazer['login'] + '\n')

        # 3. get user login-name list
        users = []
        if os.path.exists(repo_file):
            with open(repo_file, 'r', encoding='utf-8') as f:
                users = [line.strip('\n') for line in f.readlines()]
        return users

    def emails(self, user: Union[str, List[str]]) -> Union[str, Dict[str, str], None]:
        """get user emails"""
        logger.info('emails(%s)', user)

        if not user:
            raise ValueError('user info is expected')

        if isinstance(user, str):
            users = [user]
        else:
            users = user

        for login_name in users:
            self._get_user_email(login_name)

        # get user from the file
        cache_dir = self._init_cache_dir()
        email_file = os.path.join(cache_dir, EMAIL_FILE)

        user_email = {}
        with open(email_file, 'r', encoding='utf-8') as f:
            lines = [line.strip('\n') for line in f.readlines()]
            for line in lines:
                if line:
                    login_name, email = line.split('\t')
                    user_email[login_name] = email

        if isinstance(user, str):
            if user not in user_email:
                return None
            return user_email[user]
        return user_email

    def _get_user_email(self, login_name: str):
        """get user emails"""
        # 1. check for the temp dir
        cache_dir = self._init_cache_dir()

        # 2. get info
        repo_file = os.path.join(cache_dir, EMAIL_FILE)
        self._check_for_limit()
        page_index = 1

        while True:
            self._check_for_limit()
            res = requests.get(
                f'{BASE_URL}/users/{login_name}/events/public?per_page=100&page={page_index}',
                headers=self.headers
            )
            events = res.json()
            logger.info(
                '%s : public event, page<%d> total<%d>',
                login_name, page_index, (page_index - 1) * 100 + len(events)
            )
            page_index += 1

            if 'message' in events:
                break
            if not isinstance(events, list):
                break

            # 2.1 save the email info into local file
            for event in events:
                if event['type'] == 'PushEvent' and 'payload' in event \
                        and 'commits' in event['payload']:
                    commits = event['payload']['commits']
                    if commits and isinstance(commits, list):
                        commit = commits[0]
                        if 'author' in commit and 'email' in commit['author']:
                            # 2.2 find the user email, and save it to the file
                            email = commit['author']['email']
                            with open(repo_file, 'a+', encoding='utf-8') as f:
                                f.write(f'{login_name}\t{email}\n')
                                logger.info('find user<%s> email<%s>', login_name, email)
                                return
