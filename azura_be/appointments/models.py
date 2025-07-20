from django.db import models
from django.utils import timezone

from azura_be.base.constants import AppointmentStatusChoices, AppointmentTypeChoices, AppointmentVisitTypeChoices, TaskPriorityChoices
from azura_be.base.models import BaseModel
from azura_be.locations.models import Location
from azura_be.patients.models import Patient
from azura_be.users.models import User


class Appointment(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    type = models.CharField(max_length=50, choices=AppointmentTypeChoices)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    location = models.ForeignKey(Location, related_name="appointments", on_delete=models.PROTECT)
    visit_type = models.CharField(max_length=50, choices=AppointmentVisitTypeChoices)
    instructions = models.TextField(blank=True)
    payment = models.CharField(max_length=255, blank=True)
    billing = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100, blank=True)
    referring_provider = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=AppointmentStatusChoices, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == AppointmentStatusChoices.COMPLETED.name and not self.completed_at:
            self.completed_at = timezone.now()
        return super().save(*args, **kwargs)
