import uuid
from django.db import models

from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def values(cls):
        return [c.value for c in cls]

    @classmethod
    def choices(cls):
        return [(c.value, c.value) for c in cls]



class AuditableModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def time_stamp(self):
        return self.created_at

    class Meta:
        abstract = True
        ordering = ['-created_at'] 
