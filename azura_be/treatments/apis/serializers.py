from rest_framework import serializers

from azura_be.plans.apis.serializers import FormRelatedSerializer
from azura_be.plans.apis.serializers import PlanRelatedSerializer
from azura_be.treatments.models import PatientForm
from azura_be.treatments.models import PatientTreatmentPlan


class PatientTreatmentPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatmentPlan
        fields = ("patient", "plan", "active")


class PatientTreatmentPlanSerializer(serializers.ModelSerializer):
    plan = PlanRelatedSerializer()

    class Meta:
        model = PatientTreatmentPlan
        fields = "__all__"


class PatientFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientForm
        fields = ("patient", "form")


class PatientFormSerializer(serializers.ModelSerializer):
    form = FormRelatedSerializer()

    class Meta:
        model = PatientForm
        fields = "__all__"
