from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.appointments.models import Appointment
from azura_be.clinical.apis.serializers import LabResultSerializer
from azura_be.clinical.apis.serializers import MedicationSerializer
from azura_be.clinical.models import LabResult
from azura_be.clinical.models import Medication
from azura_be.documents.apis.serializers import DocumentSerializer
from azura_be.documents.models import Document
from azura_be.patient_portal.apis.serializers import PatientDashboardSerializer
from azura_be.patient_portal.dashboard import patient_dashboard
from azura_be.patients.apis.serializers import PatientGetSerializer


class PatientPortalViewSet(viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = PatientDashboardSerializer

    @action(detail=False, methods=["GET"], url_path="dashboard")
    def dashboard(self, request, *args, **kwargs):
        return Response(patient_dashboard(request.patient))

    @action(detail=False, methods=["GET"], url_path="profile")
    def profile(self, request, *args, **kwargs):
        return Response(PatientGetSerializer(request.patient).data)

    @extend_schema(responses=AppointmentSerializer(many=True))
    @action(detail=False, methods=["GET"], url_path="appointments")
    def get_appointments(self, request, *args, **kwargs):
        appointments = Appointment.objects.filter(patient=request.patient)
        return Response(AppointmentSerializer(appointments, many=True).data)

    @extend_schema(responses=LabResultSerializer(many=True))
    @action(detail=False, methods=["GET"], url_path="labs")
    def get_labs(self, request, *args, **kwargs):
        lab_results = LabResult.objects.filter(patient=request.patient)
        return Response(LabResultSerializer(lab_results, many=True).data)

    @extend_schema(responses=MedicationSerializer(many=True))
    @action(detail=False, methods=["GET"], url_path="medications")
    def get_medications(self, request, *args, **kwargs):
        medications = Medication.objects.filter(patient=request.patient)
        return Response(MedicationSerializer(medications, many=True).data)

    @extend_schema(responses=MedicationSerializer(many=True))
    @action(detail=False, methods=["GET"], url_path="documents")
    def get_documents(self, request, *args, **kwargs):
        documents = Document.objects.filter(patient=request.patient)
        return Response(DocumentSerializer(documents, many=True).data)
