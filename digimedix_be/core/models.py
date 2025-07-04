from django.db import models

from digimedix_be.base.models import BaseModel


class Specialty(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey("Specialty", null=True, blank=True, on_delete=models.CASCADE, related_name="sub_specialties")
