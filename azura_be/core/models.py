from django.db import models

from azura_be.base.models import BaseModel

class Frequency(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

class Flag(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

class Tag(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)


class Specialty(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, null=True)
    category = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "Specialty",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_specialties",
    )


class ICDCode(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    icd9 = models.BooleanField(default=False)


class Condition(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    icd_codes = models.ManyToManyField(ICDCode, blank=True)
    ccm = models.BooleanField(default=False)
    pcm = models.BooleanField(default=False)
    rpm = models.BooleanField(default=False)
    bhi = models.BooleanField(default=False)


class CPTCode(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    type = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=255, blank=True)
    subsection = models.CharField(max_length=255, blank=True)
    clinical_descriptor_id = models.CharField(max_length=64, blank=True)
    version = models.CharField(max_length=30, blank=True)
    source = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()


class HCPCSCode(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=50)
    type = models.CharField(max_length=50, blank=True)
    sequence_number = models.CharField(max_length=50, blank=True)
    record_id = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)


class RxCode(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=50)
    ndc = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class LoincCode(BaseModel):
    code = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
