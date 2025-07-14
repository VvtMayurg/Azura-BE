from django.db import models
from django.core.validators import RegexValidator
from django_tenants.models import TenantMixin

from azura_be.base.constants import DisciplineChoices
from azura_be.base.models import BaseModel


class BusinessAccount(BaseModel, TenantMixin):
    name = models.CharField(max_length=255, unique=True)
    discipline_service = models.CharField(max_length=60, choices=DisciplineChoices)
    address = models.JSONField()
    contact = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$",
                message="Contact format must be one of (XXX) XXX-XXXX or XXX-XXX-XXXX",
                code="invalid_phone",
            )
        ],
    )
    email = models.EmailField(unique=True)
    website = models.URLField(unique=True)
    grace_code = models.CharField(max_length=255)
    web_address = models.URLField(unique=True)

    auto_create_schema = True

    def save(self, *args, **kwargs):
        if not self.schema_name:
            self.set_schema_name()
        return super().save(*args, **kwargs)

    def set_schema_name(self):
        self.schema_name = str(self.id).replace("-", "_")
