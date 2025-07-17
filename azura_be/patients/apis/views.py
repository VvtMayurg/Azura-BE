from rest_framework import viewsets

from azura_be.patients.models import Patient
from azura_be.patients.apis.serializers import PatientGetSerializer, PatientCreateSerializer


class PatientViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Patient.objects.all()
    serializer_class = PatientGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PatientCreateSerializer
        return super().get_serializer_class()
