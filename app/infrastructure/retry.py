import time
from functools import wraps

from app.config import MAX_RETRIES


def retry_with_backoff(max_retries=MAX_RETRIES):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            delay = 0.5

            for attempt in range(max_retries):

                try:
                    return function(*args, **kwargs)

                except Exception:

                    if attempt == max_retries - 1:
                        raise

                    time.sleep(delay)

                    delay *= 2

        return wrapper

    return decorator
