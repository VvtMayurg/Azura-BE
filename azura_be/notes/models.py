from django.db import models

from azura_be.base.constants import NoteTypeChoices
from azura_be.base.constants import VisitNoteTypeChoices
from azura_be.base.models import BaseModel
from azura_be.patients.models import Patient


class VisitNote(BaseModel):
    patient = models.ForeignKey(Patient, related_name="visit_notes", on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.PROTECT)
    visit_start_at = models.DateTimeField()
    visit_end_at = models.DateTimeField()
    note = models.JSONField()
    note_type = models.CharField(max_length=50, choices=VisitNoteTypeChoices)


class Note(BaseModel):
    patient = models.ForeignKey(Patient, related_name="non_visit_notes", on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.PROTECT)
    note = models.JSONField()
    note_type = models.CharField(max_length=50, choices=NoteTypeChoices)
