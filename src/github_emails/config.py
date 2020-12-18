"""configuration for github emails tools"""
import os

ROOT_DIR = os.environ.get('ROOT_DIR') or os.getcwd()
CACHE_DIR = os.environ.get('GITHUB_CACHE') or '.github_cache'
EMAIL_FILE = os.environ.get('EMAIL_FILE') or 'user-emails.txt'
SKIP_EMAIL_FILE = os.environ.get('SKIP_EMAIL_FILE') or \
    os.path.join(ROOT_DIR, CACHE_DIR, 'skip-user-emails.txt')

__all__ = [
    'CACHE_DIR',
    'EMAIL_FILE'
]
