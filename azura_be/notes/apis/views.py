from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from azura_be.notes.apis.serializers import NoteCreateSerializer
from azura_be.notes.apis.serializers import NoteSerializer
from azura_be.notes.apis.serializers import VisitNoteCreateSerializer
from azura_be.notes.apis.serializers import VisitNoteSerializer
from azura_be.notes.models import Note
from azura_be.notes.models import VisitNote
from azura_be.patients.models import Patient


class VisitNoteViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = VisitNote.objects.all()
    serializer_class = VisitNoteSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return VisitNoteCreateSerializer
        return super().get_serializer_class()


class NoteViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return NoteCreateSerializer
        return super().get_serializer_class()
