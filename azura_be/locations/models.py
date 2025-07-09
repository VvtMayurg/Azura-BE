from django.db import models
from django.core.validators import RegexValidator
from timezone_field.fields import TimeZoneField

from azura_be.base.constants import DayChoices, ProviderGroupLocationStatusChoices
from azura_be.base.models import BaseModel
from azura_be.core.models import Specialty
from azura_be.provider_groups.models import Department, ProviderGroup


class Location(BaseModel):
    name = models.CharField(max_length=255)
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

    class Meta:
        unique_together = (("name", "provider_group"),)


class LocationWorkingHour(BaseModel):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="working_hours"
    )
    day = models.CharField(max_length=10, choices=DayChoices)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        unique_together = (("location", "day"),)
