from django.contrib.postgres.fields import ArrayField
from django.db import models

from azura_be.base.constants import ProgramChoices
from azura_be.base.models import BaseModel
from azura_be.core.models import Category
from azura_be.core.models import Condition
from azura_be.core.models import Flag
from azura_be.core.models import Frequency
from azura_be.core.models import ICDCode
from azura_be.core.models import Tag


class Form(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, blank=True)
    flag = models.ForeignKey(Flag, null=True, blank=True, on_delete=models.SET_NULL)
    frequency = models.ForeignKey(
        Frequency, null=True, blank=True, on_delete=models.SET_NULL
    )
    conditions = models.ManyToManyField(Condition, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    comment = models.TextField(blank=True)
    nas = models.BooleanField(default=False)
    questions = models.JSONField()


class Plan(BaseModel):
    programs = ArrayField(
        models.CharField(max_length=5, choices=ProgramChoices), null=True, blank=True
    )
    name = models.CharField(max_length=255, unique=True)
    conditions = models.ManyToManyField(Condition)
    icd_codes = models.ManyToManyField(ICDCode)

    goals = models.JSONField(null=True, blank=True)
    barriers = models.JSONField(null=True, blank=True)
    symptoms = models.JSONField(null=True, blank=True)
    interventions = models.JSONField(null=True, blank=True)
    number_to_tracks = models.JSONField(null=True, blank=True)
    expected_outcomes = models.JSONField(null=True, blank=True)

    supports = models.JSONField(null=True, blank=True)
    allergies = models.JSONField(null=True, blank=True)
    medications = models.JSONField(null=True, blank=True)
