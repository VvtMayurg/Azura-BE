from django.db import models
from django.core.validators import RegexValidator
from azura_be.users.models import User

from azura_be.base.constants import GenderChoices
from azura_be.base.models import BaseModel
from azura_be.provider_groups.models import ProviderGroup


class Patient(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=25, choices=GenderChoices)
    mrn = models.CharField(max_length=50)
    provider_group = models.ForeignKey(ProviderGroup, on_delete=models.PROTECT, related_name="patients")
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
    )
    primary_provider = models.ForeignKey(User, on_delete=models.PROTECT, related_name="patients_primary_provider")
    active = models.BooleanField(default=True)
    address = models.JSONField(null=True, blank=True)
    picture = models.ImageField(upload_to="patients/", null=True, blank=True)
