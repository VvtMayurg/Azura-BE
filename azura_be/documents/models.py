from django.db import models

from azura_be.base.constants import DocumentCategoryChoices
from azura_be.base.models import BaseModel
from azura_be.patients.models import Patient


class Document(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="documents")
    category = models.CharField(max_length=100, choices=DocumentCategoryChoices)
    file = models.FileField(upload_to="documents/")
