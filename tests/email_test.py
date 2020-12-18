import pytest
import os
from pathlib import Path


@pytest.fixture(scope='function')
def github_api(tmp_path: Path):
    # TODO: make sure this can get temp dir
    if tmp_path.exists():
        tmp_path.rmdir()
    tmp_path.mkdir()
    root_dir = os.path.join(*tmp_path.parts)
    os.environ['ROOT_DIR'] = root_dir
    from github_emails import GithubApi
    return GithubApi()


def test_fetching_data(github_api):
    stargazers = github_api.stargazers('wj-Mcat', 'github-emails')
    assert len(stargazers) > 0


def test_cache_emails(github_api):
    stargazers = github_api.stargazers('wj-Mcat', 'github-emails')
    assert 'wj-Mcat' in stargazers

    emails = github_api.emails(stargazers)
    assert 'wj-Mcat' in emails


def test_cache_skip_emails(github_api):
    stargazers = github_api.stargazers('wj-Mcat', 'github-emails')
    exist_user_emails = {
        "wj-Mcat": '1435130236@qq.com'
    }
    emails = github_api.emails(stargazers, exist_user_emails)
    assert 'wj-Mcat' not in emails
