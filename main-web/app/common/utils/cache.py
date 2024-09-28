from django.core.cache import cache
from django.conf import settings
import hashlib 
from functools import wraps


def blacklist_access_token(token):
    """
    Stores the given token in cache to blacklist it for the duration of 
    the ACCESS_TOKEN_LIFETIME.
    """
    timeout = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", 3600).total_seconds()  # Get the timeout in seconds
    cache.set(f"blacklisted_token_{token}", True, timeout)
    
    
def is_access_token_blacklisted(token):
    """
    Checks if the given token is blacklisted.
    """
    return bool(cache.get(f"blacklisted_token_{token}"))


def cache_result(timeout=1800 * 3):  # Default timeout of 30 minutes
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique cache key based on the function name and arguments
            cache_key = generate_cache_key(func, *args, **kwargs)
            
            # Try to get the cached result
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call the original function if cache miss
            result = func(*args, **kwargs)
            
            # Cache the result with the specified timeout
            cache.set(cache_key, result, timeout=timeout)
            
            return result
        return wrapper
    return decorator


def generate_cache_key(func, *args, **kwargs):
    """
    Generate a unique cache key using the function name and its arguments.
    Uses a hash to ensure the key is of reasonable length.
    """
    key_base = f"{func.__name__}:{''.join([str(arg) for arg in args])}"
    return hashlib.md5(key_base.encode('utf-8')).hexdigest()

