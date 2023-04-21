from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields) -> "CustomUserModel":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError(_("The given email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if user.is_superuser:
            user.user_type = user.UserTypes.ADMIN  # SETTING SUPERUSER STATUS AS ADMIN
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields) -> "CustomUserModel":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUserModel(AbstractUser):
    class UserTypes(models.TextChoices):
        STANDARD = _("Standard")
        STUFF_ACCELERATION = _("Stuff-Acceleration")
        STUFF_DIRECTION = _("Stuff-Direction")
        ADMIN = _("Admin")

    username = None  # THIS FIELD IS NOT REQUIRED
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(_("email address"), unique=True)

    user_type = models.CharField(
        max_length=150,
        choices=UserTypes.choices,
        default=UserTypes.STANDARD,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
