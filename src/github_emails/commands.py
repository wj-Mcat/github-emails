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

from argparse import ArgumentParser
from wechaty_puppet import get_logger   # type: ignore
from github_emails import GithubApi
from github_emails.config import CACHE_DIR, EMAIL_FILE

# pylint: disable=invalid-name
logger = get_logger(__name__)


def main():
    """command interface"""
    parser = ArgumentParser()
    parser.add_argument('--owner', type=str, help='the repo of the user', required=True)
    parser.add_argument('--repo', type=str, help='the name of repo', required=True)
    parser.add_argument('--token', type=str, help='personal access token', required=True)
    parser.add_argument(
        '--stargazers-file',
        type=str, required=False,
        help='find the emails base on stargazers file',
        default='./.github_info/'
    )
    parser.add_argument(
        '--skip-user-emails-file',
        type=str, required=False,
        help='./user-emails.txt'
    )
    args = parser.parse_args()
    github = GithubApi(
        token=args.token
    )
    stargazers = github.stargazers(args.owner, args.repo)
    github.emails(stargazers)
    logger.info('email info has been saved into %s/%s', CACHE_DIR, EMAIL_FILE)


if __name__ == '__main__':
    main()
