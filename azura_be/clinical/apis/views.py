from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from azura_be.clinical.apis.serializers import MedicationCreateSerializer
from azura_be.clinical.apis.serializers import MedicationSerializer
from azura_be.clinical.apis.serializers import VitalCreateSerializer
from azura_be.clinical.apis.serializers import VitalSerializer
from azura_be.clinical.models import Medication
from azura_be.clinical.models import Vital
from azura_be.patients.models import Patient


class MedicationViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return MedicationCreateSerializer
        return super().get_serializer_class()


class VitalViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Vital.objects.all()
    serializer_class = VitalSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return VitalCreateSerializer(many=True)
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data = data if isinstance(data, list) else [data]

        for vital in data:
            Vital.objects.create(**vital)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
