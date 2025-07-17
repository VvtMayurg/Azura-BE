import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from azura_be.base.constants import DayChoices
from timezone_field.fields import TimeZoneField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from azura_be.base.models import BaseModel
from azura_be.core.models import Specialty
from azura_be.users.managers import UserManager


class User(AbstractUser):
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    first_name = models.CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(null=True, blank=True)
    timezone = TimeZoneField(null=True, blank=True)
    email_noftification = models.BooleanField(default=True)
    sms_notification = models.BooleanField(default=True)
    auto_form_save = models.BooleanField(default=False)

    provider_groups = ArrayField(models.UUIDField(), null=True, blank=True)
    departments = ArrayField(models.UUIDField(), null=True, blank=True)
    primary_location = models.UUIDField(null=True, blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$",
                message="Phone number format must be one of (XXX) XXX-XXXX or XXX-XXX-XXXX",
                code="invalid_phone",
            )
        ],
        blank=True,
    )
    role = models.CharField(max_length=255, blank=True)

    account_user = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)

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


class License(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="licenses")
    number = models.CharField(max_length=25)
    state = models.CharField(max_length=150)
    exiry_date = models.DateField()
    npi = models.CharField(max_length=10)
    dea_number = models.CharField(max_length=50, blank=True)
    specialties = models.ManyToManyField(Specialty, blank=True)

    class Meta:
        unique_together = (("user", "number"),)


class WorkShedule(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(max_length=10, choices=DayChoices)
    start = models.TimeField()
    end = models.TimeField()
