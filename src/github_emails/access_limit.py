"""access limit decorator"""
import time
from datetime import datetime
from wechaty_puppet import get_logger   # type: ignore

# pylint: disable=invalid-name
logger = get_logger(__name__)


def access_limit(func):
    """decorator of the access limitation"""
    def wrapper():
        """func wrapper"""
        # 1. eval the func
        result = func()

        # 2. check the remaining operations
        if hasattr(result, 'raw_headers'):
            raw_headers: dict = getattr(result, 'raw_headers')
            if hasattr(raw_headers, 'x-ratelimit-remaining') and \
                    int(getattr(raw_headers, 'x-ratelimit-remaining')) == 0:
                reset_time_int = int(getattr(raw_headers, 'x-ratelimit-reset'))
                reset_time = datetime.fromtimestamp(reset_time_int)
                wait_seconds = (datetime.now() - reset_time).seconds + 1
                time.sleep(wait_seconds)
        return result
    return wrapper


def check_for_limit(result):
    """check for the limitation"""
    if hasattr(result, 'raw_headers'):
        raw_headers: dict = getattr(result, 'raw_headers')
        if hasattr(raw_headers, 'x-ratelimit-remaining') and \
                int(getattr(raw_headers, 'x-ratelimit-remaining')) == 0:
            reset_time_int = int(getattr(raw_headers, 'x-ratelimit-reset'))
            reset_time = datetime.fromtimestamp(reset_time_int)
            wait_seconds = (datetime.now() - reset_time).seconds + 1
            time.sleep(wait_seconds)
