from django.db import models
from django.core.validators import RegexValidator
from timezone_field.fields import TimeZoneField

from azura_be.base.constants import ProviderGroupLocationStatusChoices
from azura_be.base.models import BaseModel
from azura_be.users.models import User


class ProviderGroup(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=15,
        choices=ProviderGroupLocationStatusChoices,
        default=ProviderGroupLocationStatusChoices.PENDING.name,
    )
    picture = models.ImageField(
        upload_to="provider_groups/",
        blank=True,
        null=True,
    )
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
    billing_address = models.JSONField(
        null=True,
        blank=True,
    )
    physical_address = models.JSONField(
        null=True,
        blank=True,
    )
    bio = models.TextField(blank=True)

    timezone = TimeZoneField()

    def __str__(self) -> str:
        return self.group_name


class Department(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, null=True, unique=True)
    description = models.TextField(blank=True)
    admin = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="department_admins"
    )
    provider_groups = models.ManyToManyField(ProviderGroup, related_name="departments")
    locations = models.ManyToManyField("locations.Location", related_name="departments")
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
    active = models.BooleanField(default=True)
