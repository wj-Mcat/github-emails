"""examples to get emails from repo"""
from pprint import pprint

from github_emails import GithubApi, GithubOptions


def main():
    """test the `get emails` ability"""
    github = GithubApi(options=GithubOptions(token='931fb50e71ef0b5508b6e8f8032132c0c2debafc'))
    emails = github.get_repo_star_emails('wechaty', 'python-wechaty')
    pprint(emails)


if __name__ == '__main__':
    main()
