"""examples to get emails from repo"""
from github_emails import GithubApi


def main():
    """test the `get emails` ability"""
    github = GithubApi(token='')
    stargazers = github.stargazers('wechaty', 'python-wechaty')
    for stargazer in stargazers:
        github.emails(stargazer)


if __name__ == '__main__':
    main()
