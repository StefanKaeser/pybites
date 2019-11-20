from functools import wraps

MAX_RETRIES = 3

class MaxRetriesException(Exception):
    pass

def retry(func):
    """Complete this decorator, make sure
       you print the exception thrown"""

    @wraps(func)
    def wrapped(*args, **kwargs):
        for _ in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                print(exc)
        raise MaxRetriesException

    return wrapped
