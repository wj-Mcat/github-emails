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
from typing import Optional, Dict
from wechaty_puppet import get_logger   # type: ignore
from github import Github
from github_emails.access_limit import check_for_limit

# pylint: disable=invalid-name
logger = get_logger(__name__)


@dataclass
class GithubOptions:
    """github options"""
    username: Optional[str] = None
    password: Optional[str] = None

    token: Optional[str] = None


class GithubApi:
    """Github Restful Api"""
    def __init__(self, options: GithubOptions):
        """initialization for github client"""
        if not options.token:
            self.github: Github = Github(login_or_token=options.token)
        elif not options.username and not options.password:
            self.github = Github(
                login_or_token=options.username,
                password=options.password
            )
        else:
            raise ValueError('token or username&password is expected, please use one of them')

    def get_user_email(self, user: str) -> Optional[str]:
        """get github open email by user name"""
        logger.info('get_user_email(%s)', user)

        # 1. get login_user
        login_user = self.github.get_user(user)
        check_for_limit(login_user)

        if not login_user:
            raise ValueError(f'User<{user}> not found')

        # 2. get public events
        events = login_user.get_public_events()
        for event in iter(events):
            check_for_limit(event)
            if event.type == 'PushEvent':
                payload: dict = event.payload
                if 'commits' in payload:
                    commits = payload['commits']
                    if commits and 'author' in commits[0]:
                        author = commits[0]
                        if 'email' in author:
                            return author['email']
        return None

    def get_repo_star_emails(self, owner: str, repo: str) -> Dict[str, str]:
        """get the star email list from the specific repo"""
        logger.info('get_repo_star_emails(%s, %s)', owner, repo)
        repository = self.github.get_repo(f'{owner}/{repo}')
        check_for_limit(repository)

        user_emails: Dict[str, str] = {}
        for stargazer in iter(repository.get_stargazers()):
            email: Optional[str] = stargazer.email
            if not email:
                email = self.get_user_email(stargazer.login)
            if email:
                user_emails[stargazer.login] = email
        return user_emails
