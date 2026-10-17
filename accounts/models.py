import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Manage users using email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")

        if not extra_fields.get("phone"):
            raise ValueError("A phone number is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault(
            "platform_role", User.PlatformRole.SUPER_ADMIN
        )
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class PlatformRole(models.TextChoices):
        GUEST = "guest", "Guest"
        USER = "user", "User"
        HOST = "host", "Host"
        STAFF = "staff", "Staff"
        SUPER_ADMIN = "super_admin", "Super Admin"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = None
    date_joined = None

    email = models.EmailField(
        max_length=254,
        unique=True,
    )

    bio = models.TextField(
        blank=True,
        default="",
    )

    avatar_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    is_email_verified = models.BooleanField(
        default=False,
    )

    phone = models.CharField(
        max_length=25,
        unique=True,
    )

    is_phone_verified = models.BooleanField(
        default=False,
    )

    platform_role = models.CharField(
        max_length=20,
        choices=PlatformRole.choices,
        default=PlatformRole.GUEST,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email
