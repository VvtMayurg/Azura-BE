from django.db import models
from django.core.validators import RegexValidator
from timezone_field.fields import TimeZoneField

from digimedix_be.base.constants import ProviderGroupLocationStatusChoices
from digimedix_be.base.models import BaseModel
from digimedix_be.users.models import User


class ProviderGroup(BaseModel):
    group_name = models.CharField(max_length=255, unique=True)
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
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="department_admins"
    )
    provider_group = models.ForeignKey(ProviderGroup, on_delete=models.PROTECT, related_name="departments")
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
    
    class Meta:
        unique_together = (("name", "provider_group"),)
