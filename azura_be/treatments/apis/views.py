from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from azura_be.patients.models import Patient
from azura_be.treatments.apis.serializers import PatientFormCreateSerializer
from azura_be.treatments.apis.serializers import PatientFormSerializer
from azura_be.treatments.apis.serializers import PatientTreatmentPlanCreateSerializer
from azura_be.treatments.apis.serializers import PatientTreatmentPlanSerializer
from azura_be.treatments.models import PatientForm
from azura_be.treatments.models import PatientTreatmentPlan


class PatientTreatmentPlanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = PatientTreatmentPlan.objects.all()
    serializer_class = PatientTreatmentPlanSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PatientTreatmentPlanCreateSerializer
        return super().get_serializer_class()


class PatientFormViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = PatientForm.objects.all()
    serializer_class = PatientFormSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PatientFormCreateSerializer
        return super().get_serializer_class()
