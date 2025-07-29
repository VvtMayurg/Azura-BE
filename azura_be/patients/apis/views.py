from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from azura_be.patients.apis.serializers import EmailSMSCreateSerializer
from azura_be.patients.apis.serializers import EmailSMSSerializer
from azura_be.patients.apis.serializers import PatientCreateSerializer
from azura_be.patients.apis.serializers import PatientGetSerializer
from azura_be.patients.models import EmailSMS
from azura_be.patients.models import Patient


class PatientViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Patient.objects.all()
    serializer_class = PatientGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PatientCreateSerializer
        return super().get_serializer_class()


class EmailSMSViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = EmailSMS.objects.all()
    serializer_class = EmailSMSSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type"]

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return EmailSMSCreateSerializer
        return super().get_serializer_class()
