from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from common.models import AuditableModel
from .manager import UserManager


class User(AuditableModel, AbstractBaseUser, PermissionsMixin):
    """ Custom user for application. """
    
    email = models.EmailField(max_length=125, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)

    # username = models.CharField(blank=True, null=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.full_name} |{ self.email}".strip()
    
    @property
    def full_name(self):
        return f"{self.get_full_name()}"
    

    def change_password(self, password):
        self.set_password(password)
        self.save(update_fields=['password'])

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

