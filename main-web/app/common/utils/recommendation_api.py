import requests
from django.conf import settings

headers = {
        'Client-Header-Secret': 'PEARMONIEAPI',  # Replace with the correct client secret
        'Content-Type': 'application/json'  # Set content type
    }

def log_user_interaction(user_id, product_id, category):
    """
    Sends a user-product interaction to the recommendation service.

    Args:
        user_id (int): ID of the user who viewed the product.
        product_id (int): ID of the product viewed.
        category (str): Category of the product.

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    interaction_data = {
        'user_id': user_id,
        'product_id': product_id,
        'category': category
    }

    try:
        response = requests.post(
            f'{settings.RECOMMENDATION_BASE_URL}/ai/interactions',
            json=interaction_data, headers=headers
        )
        response.raise_for_status()  # Raise an exception if the request failed
        return True
    except Exception as e:
        # fial silently
        print(f"Failed to log interaction: {e}")
        return False


def seed_product_catalogue(product_name, product_id, category):
    """
    Sends a user-product interaction to the recommendation service.

    Args:
        product_name (int): ID of the user who viewed the product.
        product_id (int): ID of the product viewed.
        category (str): Category of the product.

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    interaction_data = {
        'product_name': product_name,
        'product_id': product_id,
        'category': category
    }
    
    
    try:
        response = requests.post(
            f'{settings.RECOMMENDATION_BASE_URL}/ai/products',
            json=interaction_data, headers=headers
        )
        response.raise_for_status()  # Raise an exception if the request failed
        return True
    except Exception as e:
        # fial silently
        print(f"Failed to log interaction: {e}")
        return False
