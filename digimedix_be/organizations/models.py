from django.db import models
from django_tenants.models import TenantMixin

from digimedix_be.base.models import BaseModel


class Organization(BaseModel, TenantMixin):
    name = models.CharField(max_length=100)

    auto_create_schema = True

    def save(self, *args, **kwargs):
        if not self.schema_name:
            self.set_schema_name()
        return super().save(*args, **kwargs)

    def set_schema_name(self):
        self.schema_name = str(self.id)
