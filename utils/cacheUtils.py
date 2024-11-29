import functools
from datetime import datetime, timedelta

def timed_cache(minutes: int):
    """
    Caches the result of a function for a given amount of time.
    
    Args:
        minutes (int): The time in minutes the result should be cached.
    """
    cache: dict[any, tuple[any, datetime]] = {}  # type: ignore

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now()

            # check if the result is already in the cache
            if args in cache:
                result, timestamp = cache[args]

                # check if the result is still valid and return it if it is valid
                if now - timestamp < timedelta(minutes=minutes):
                    return result

            # if the result is not in the cache or not valid anymore, get the result
            result = func(*args, **kwargs)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator
