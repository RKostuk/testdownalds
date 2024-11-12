from typing import Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email: str) -> str:
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def get_by_natural_key(self, email: str):
        return self.get(**{self.model.USERNAME_FIELD: email})

    def _create_user(
            self, email: str, password: Optional[str], **extra_fields: dict[str, Any]
    ):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        # Використовуємо self.model замість прямого User.objects.create
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email: str, password: Optional[str] = None, **extra_fields: dict[str, Any]
    ):
        """
        Create and save a regular user with the given email, password and extra fields.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(
            self, email: str, password: Optional[str] = None, **extra_fields: dict[str, Any]
    ):
        """
        Create and save a superuser with the given email, password and extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(verbose_name=_("full_name"), max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата реєстрації"))

    is_staff = models.BooleanField(
        verbose_name=_("staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"), default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions_set'
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
