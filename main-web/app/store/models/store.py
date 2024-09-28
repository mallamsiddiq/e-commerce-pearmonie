from django.db import models
from common.models import AuditableModel

class Store(AuditableModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('authapp.User', on_delete=models.CASCADE, related_name='stores')

    def __str__(self):
        return f"{self.name} by {self.owner}"

class Product(AuditableModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='products')
    views_count = models.PositiveIntegerField(default=0, db_index=True) # Field to track total views
    viewers = models.ManyToManyField('authapp.User', related_name='viewed_products', blank=True)

    def __str__(self):
        return self.name

    def increment_views(self, viewer = None):
        self.views_count += 1
        self.save()
        
        if viewer:
            self.viewers.add(viewer)