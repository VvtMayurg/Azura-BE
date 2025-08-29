from django.core.validators import RegexValidator
from django.db import models
from timezone_field.fields import TimeZoneField

from azura_be.base.constants import CommunicationMessageType
from azura_be.base.constants import GenderChoices
from azura_be.base.models import BaseModel
from azura_be.locations.models import Location
from azura_be.provider_groups.models import ProviderGroup
from azura_be.users.models import User


class Patient(BaseModel):
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    admission_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=25, choices=GenderChoices)
    mrn = models.CharField(max_length=50, blank=True)
    health_number = models.CharField(max_length=25, unique=True, null=True)
    guardian_health_number = models.CharField(max_length=25, blank=True)
    provider_group = models.ForeignKey(
        ProviderGroup,
        on_delete=models.PROTECT,
        related_name="patients",
    )
    email = models.EmailField(blank=True)
    phone_type = models.CharField(max_length=50, blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$",
                message="Phone number format must be one of (XXX) XXX-XXXX or XXX-XXX-XXXX",
                code="invalid_phone",
            ),
        ],
        blank=True,
    )
    primary_provider = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="patients_primary_provider",
    )
    referring_provider = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    address = models.JSONField(null=True, blank=True)
    picture = models.ImageField(upload_to="patients/", null=True, blank=True)
    timezone = TimeZoneField(null=True, blank=True)
    preferred_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="patients",
        null=True,
        blank=True,
    )
    contact_preferences = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="patient")


class Insurance(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="insurances",
    )
    front = models.ImageField(upload_to="insurances/", null=True, blank=True)
    back = models.ImageField(upload_to="insurances/", null=True, blank=True)
    relation = models.CharField(max_length=255)
    carrier_name = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=255, blank=True)
    group_id = models.CharField(max_length=100, blank=True)
    copay = models.BooleanField(default=False)
    deductible = models.CharField(max_length=255, blank=True)


class EmailSMS(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="communications")
    type = models.CharField(max_length=10, choices=CommunicationMessageType)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
