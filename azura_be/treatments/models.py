from django.db import models

from azura_be.base.models import BaseModel
from azura_be.patients.models import Patient
from azura_be.plans.models import Form
from azura_be.plans.models import Plan


class PatientTreatmentPlan(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatment_plans")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="patient_treatment_plans")
    active = models.BooleanField(default=False)


class PatientTreatmentPlanResponse(BaseModel):
    treatment_plan = models.ForeignKey(PatientTreatmentPlan, on_delete=models.CASCADE, related_name="responses")
    response = models.JSONField()


class PatientForm(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="forms")
    form = models.ForeignKey(Form, on_delete=models.PROTECT, related_name="patient_forms")
    active = models.BooleanField(default=False)


class PatientFormResponse(BaseModel):
    patient_form = models.ForeignKey(PatientForm, on_delete=models.CASCADE, related_name="responses")
    response = models.JSONField()
