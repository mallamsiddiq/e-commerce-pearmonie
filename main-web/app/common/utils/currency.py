import requests,  hashlib, decimal 
from django.conf import settings
from django.core.cache import cache
from functools import wraps

# Base URL for the Free Currency API
BASE_URL = "https://api.freecurrencyapi.com/v1"

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


# @cache_result(timeout=1800 * 3)
def get_latest_rates(base_currency="USD", currencies = None):
    """
    Fetches the latest exchange rates from the Free Currency API.
    
    Parameters:
        api_key (str): Your API key for accessing the API.
        base_currency (str): The base currency (default is 'USD').
        currencies (str): A comma-separated list of currency codes (optional).
        
    Returns:
        dict: The response data from the API containing the exchange rates.
    """
    # Prepare the request parameters
    params = {
        "apikey": settings.CURRENCY_API_KEY,
        "base_currency": base_currency
    }
    
    # Optionally add currencies if provided
    if currencies:
        params["currencies"] = currencies

    try:
        # Make the request to the API
        response = requests.get(f"{BASE_URL}/latest", params=params)
        response.raise_for_status()  # Raise an error for bad responses (4XX, 5XX)
        
        # Parse the response as JSON
        data = response.json()
        return data['data']
     
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return {}
    
    
@cache_result(timeout=60 * 60 * 24)
def validate_currency_from_api(currency_code):
    """
    Validates if a currency code exists by fetching the list of available currencies.
    """
    # Prepare the request parameters
    params = {
        "apikey": settings.CURRENCY_API_KEY,
    }

    try:
        # Make the request to fetch the list of currencies
        response = requests.get(f"{BASE_URL}/currencies", params=params)
        response.raise_for_status()  # Raise an error for bad responses (4XX, 5XX)
        
        # Parse the response as JSON
        currencies_data = response.json()
        
        # Check if the currency code exists in the data
        if currency_code.upper() in currencies_data.get("data", {}):
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error fetching currencies: {e}")
        return False

@cache_result(timeout=60 * 60 * 6)
def get_latest_currency_rate(currency, base_currency="USD",):
    return get_latest_rates(base_currency=base_currency, currencies=currency).get(currency, 1)


@cache_result(timeout=60 * 60 * 6)
def convert_currency(currency, amount, base_currency="USD", date=None):
    rate = get_latest_currency_rate(currency, base_currency = base_currency)
    return decimal.Decimal(rate)*amount