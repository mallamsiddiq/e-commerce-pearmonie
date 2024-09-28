# signals.py

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Product
from store.task import seed_product_catalogue_task, log_user_interaction_task

@receiver(post_save, sender=Product)
def seed_ai_product_table(sender, instance, created, **kwargs):
    """
    Signal that triggers when a new product is created.
    Seeds the AI product table.
    """
    if created:
        # Create an entry in the AIProduct table based on the created Product instance
        seed_product_catalogue_task.delay(instance.name, str(instance.id), instance.category)
        
      

@receiver(m2m_changed, sender=Product.viewers.through)
def create_product_view(sender, instance, action, reverse, model, **kwargs):
    if action == 'post_add':
        # Get the list of user IDs being added
        viewers = kwargs.get('pk_set', [])
        for viewer_id in viewers:
            # Call the Celery task asynchronously
            log_user_interaction_task.delay(str(viewer_id), str(instance.id), instance.category)
