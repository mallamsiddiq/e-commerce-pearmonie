from celery import shared_task
from common.utils import log_user_interaction, seed_product_catalogue

@shared_task(name="log_user_interaction_task")
def log_user_interaction_task(user_id, product_id, category):
    """
    Asynchronous task to log user interaction to the recommendation service.
    """
    return log_user_interaction(user_id, product_id, category)


@shared_task(name="seed_product_catalogue_task")
def seed_product_catalogue_task(product_name, product_id, category):
    """
    Asynchronous task to seed new products to recommendation service.
    """
    return seed_product_catalogue(product_name, product_id, category)