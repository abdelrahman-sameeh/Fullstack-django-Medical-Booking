from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user with email and password"""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser with email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    email = models.EmailField(unique=True, blank=True)
    picture = models.ImageField("pictures", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")], default="M", blank=True)  
    phone_number = models.CharField(max_length=15, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()
