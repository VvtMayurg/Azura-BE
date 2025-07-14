import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from azura_be.users.managers import UserManager


class User(AbstractUser):
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    first_name = models.CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated_by",
    )
    business_accounts = models.ManyToManyField("business_accounts.BusinessAccount", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
