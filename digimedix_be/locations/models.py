from django.db import models
from django.core.validators import RegexValidator
from timezone_field.fields import TimeZoneField

from digimedix_be.base.constants import DayChoices, ProviderGroupLocationStatusChoices
from digimedix_be.base.models import BaseModel
from digimedix_be.core.models import Specialty
from digimedix_be.provider_groups.models import ProviderGroup
from digimedix_be.users.models import User


class Department(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="department_admins"
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
    active = models.BooleanField(default=True)


class Location(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    provider_group = models.ForeignKey(ProviderGroup, on_delete=models.PROTECT, related_name="locations")
    email = models.EmailField()
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
        unique=True,
    )
    npi = models.CharField(max_length=10, unique=True)
    fax = models.CharField(max_length=15, unique=True)
    timezone = TimeZoneField()
    note = models.TextField(blank=True)
    billing_address = models.JSONField(
        null=True,
        blank=True,
    )
    physical_address = models.JSONField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=15,
        choices=ProviderGroupLocationStatusChoices,
        default=ProviderGroupLocationStatusChoices.PENDING.name,
    )
    picture = models.ImageField(upload_to="locations/", null=True, blank=True)
    departments = models.ManyToManyField(Department, blank=True)
    specialties = models.ManyToManyField(Specialty, blank=True)


class LocationWorkingHour(BaseModel):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="working_hours"
    )
    day = models.CharField(max_length=10, choices=DayChoices)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        unique_together = (("location", "day"),)
