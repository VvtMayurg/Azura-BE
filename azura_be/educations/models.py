from django.db import models

from azura_be.base.constants import EducationFormTypeChoices
from azura_be.base.models import BaseModel
from azura_be.core.models import Condition, Specialty
from azura_be.patients.models import Patient


class Education(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    specialties = models.ManyToManyField(Specialty, blank=True)
    information = models.TextField(blank=True)
    conditions = models.ManyToManyField(Condition, blank=True)
    form_type = models.CharField(max_length=50, choices=EducationFormTypeChoices)
    file = models.FileField(upload_to="educations/")

class PatientEducation(BaseModel):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name="patients")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="educations")

    class Meta:
        unique_together = (("education", "patient"),)
