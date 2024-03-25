from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    def get_role(self):
        if self.is_admin:
            return 'admin'
        elif self.is_manager:
            return 'manager'
        else:
            return 'user'
