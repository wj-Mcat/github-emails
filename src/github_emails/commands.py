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
from pprint import pprint
from github_emails import GithubApi, GithubOptions


def main():
    """command interface"""
    parser = ArgumentParser()
    parser.add_argument('--owner', type=str, help='the repo of the user', required=True)
    parser.add_argument('--repo', type=str, help='the name of repo', required=True)
    parser.add_argument('--token', type=str, help='personal access token', required=True)
    args = parser.parse_args()
    github = GithubApi(
        options=GithubOptions(token=args.token)
    )
    emails = github.get_repo_star_emails(
        owner=args.owner,
        repo=args.repo
    )
    pprint(emails)


if __name__ == '__main__':
    main()
