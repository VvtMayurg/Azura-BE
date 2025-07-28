from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from azura_be.documents.apis.serializers import DocumentCreateSerializer
from azura_be.documents.apis.serializers import DocumentSerializer
from azura_be.documents.models import Document
from azura_be.patients.models import Patient


class DocumentViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return DocumentCreateSerializer
        return super().get_serializer_class()
