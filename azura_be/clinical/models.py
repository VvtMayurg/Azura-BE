from django.db import models

from azura_be.base.models import BaseModel
from azura_be.patients.models import Patient


class Vital(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals")
    vital_type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    value1 = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)
    recorded_at = models.DateTimeField()
    metadata = models.JSONField(null=True, blank=True)


class Medication(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medications")
    medicine = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    sig = models.CharField(max_length=255)
    qty = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    refills = models.CharField(max_length=255)
    days = models.IntegerField(default=0)
