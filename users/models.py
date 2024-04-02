from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, fullname, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(fullname=fullname, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, fullname ,email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 3)
        return self._create_user(fullname, email, username, password, **extra_fields)

    def create_superuser(self,fullname, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 1)
        return self._create_user(fullname, email, username, password, **extra_fields)

    def create_manager_user(self, fullname, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 2)
        return self._create_user(fullname, email, username, password, **extra_fields)


class User(AbstractUser):
    SUPER_ADMIN = 1
    MANAGER = 2
    USER = 3

    ROLES_CHOICES = (
        (SUPER_ADMIN, "super_admin"),
        (MANAGER, "manager"),
        (USER, "user"),
    )
    fullname=models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.PositiveIntegerField(choices=ROLES_CHOICES,default=1)
    objects = UserManager()
    REQUIRED_FIELDS = ["email", "password"]

    def get_role(self):
        return self.get_role_display()
    



class Profile(models.Model):
    fullname=models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=150)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    address= models.CharField(max_length=150, blank=True, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )