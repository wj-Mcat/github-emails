"""examples to get emails from repo"""
from pprint import pprint

from github_emails import GithubApi, GithubOptions


def main():
    """test the `get emails` ability"""
    github = GithubApi(token='7685a7a6eb0b3e9c91cf66869a4721b53df2d468')
    emails = github.get_repo_stargazers('wechaty', 'python-wechaty')
    pprint(emails)


if __name__ == '__main__':
    main()
