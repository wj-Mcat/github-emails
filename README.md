# github-emails [![PyPI Version](https://img.shields.io/pypi/v/github-emails?color=blue)](https://pypi.org/project/github-emails/)  ![auto-publish-to-pypi](https://github.com/wj-Mcat/github-emails/workflows/auto-publish-to-pypi/badge.svg)

## Quick start

> the example below: `wechaty` is the owner, `python-wechaty` is the name of repo
> github: https://www.github.com/wechaty/python-wechaty

- Installation

```shell script
pip install github-emails
```

- Simple Code

```python
from github_emails import GithubApi
github = GithubApi(token='')
stargazers = github.stargazers('wechaty', 'python-wechaty')
for stargazer in stargazers:
    github.emails(stargazer)
```

And you will find that your final email info is stored in `.github_info/user-email.txt` file.

- Command

```shell script
github-emails --owner=wechaty --repo=python-wechaty --token=your-token --stargazer-file='.github_info/wechaty-python-wechaty-' --skip-user-emails-file=./user-emails.txt
```

## History

### v0.0.2 (Jun 19, 2020)

- works with token, and everything works well for me

### v0.0.1 (Jun 19, 2020)

- works with username/password & token authentication

## Copyright & License

- Code & Docs © 2020 wj-Mcat <https://github.com/wj-Mcat>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
