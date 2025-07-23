from django.db import models
from django.utils import timezone

from azura_be.base.constants import TaskPriorityChoices
from azura_be.base.models import BaseModel
from azura_be.patients.models import Patient
from azura_be.users.models import User


class Task(BaseModel):
    reason = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    due_at = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=TaskPriorityChoices)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        return super().save(*args, **kwargs)
