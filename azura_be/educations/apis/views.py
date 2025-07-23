from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from azura_be.educations.apis.serializers import (
    AssignUnassignPatientEducationSerializer,
)
from azura_be.educations.apis.serializers import EducationCreateSerializer
from azura_be.educations.apis.serializers import EducationSerializer
from azura_be.educations.models import Education
from azura_be.patients.apis.serializers import PatientRelatedSerializer
from azura_be.patients.models import Patient


class EducationViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return EducationCreateSerializer
        if self.action == ["assign_unassign"]:
            return AssignUnassignPatientEducationSerializer
        if self.action == "assigned_patients":
            return PatientRelatedSerializer(many=True)
        return super().get_serializer_class()

    @action(detail=True, methods=["PATCH"], url_path="assign-unassign")
    def assign_unassign(self, request, *args, **kwargs):
        education = self.get_object()
        serializer = AssignUnassignPatientEducationSerializer(
            data=request.data, context={"education": education}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @action(
        detail=True,
        methods=["GET"],
        url_path="assigned-patients",
        pagination_class=None,
    )
    def assigned_patients(self, request, *args, **kwargs):
        education = self.get_object()
        patients = Patient.object.filter(educations__education=education)
        return Response(PatientRelatedSerializer(patients).data)
