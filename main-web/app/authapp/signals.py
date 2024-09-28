from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from store.models import Store

@receiver(post_save, sender=get_user_model())
def create_store_for_user(sender, instance, created, **kwargs):
    """
    Create a store for a user upon signup if the user is not an admin.
    """
    # Check if the user is newly created and is not a superuser (admin)
    if created and not instance.is_superuser:
        # Create a store for the user
        Store.objects.create(owner=instance, name = f"{instance.email.split('@')[0]} Store")

