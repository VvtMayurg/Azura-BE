from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


from azura_be.clinical.apis.serializers import MedicationCreateSerializer
from azura_be.clinical.apis.serializers import MedicationSerializer
from azura_be.clinical.apis.serializers import VitalCreateSerializer
from azura_be.clinical.apis.serializers import VitalSerializer
from azura_be.clinical.apis.serializers import LatestVitalSerializer
from azura_be.clinical.apis.serializers import GraphSerializer
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
    pagination_class = None

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
        self.queryset = self.queryset.filter(patient=patient)
        return super().get_queryset()

    @extend_schema(responses=VitalCreateSerializer(many=True), request=VitalCreateSerializer(many=True))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data = data if isinstance(data, list) else [data]

        for vital in data:
            Vital.objects.create(**vital)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LatestVitalViewSet(viewsets.ModelViewSet):
    queryset = Vital.objects.all()
    serializer_class = LatestVitalSerializer

    @action(detail=False, methods=["get"], url_path="latest")
    def latest_vitals(self, request):
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response(
                {"detail": "patient_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vital_types = ["Heart Rate", "Blood Pressure", "Temperature", "Oxygen Saturation"]

        latest_vitals = [
            Vital.objects.filter(patient_id=patient_id, vital_type=vtype)
            .order_by("-recorded_at")
            .first()
            for vtype in vital_types
        ]

        latest_vitals = [v for v in latest_vitals if v]

        return Response(self.get_serializer(latest_vitals, many=True).data)
    

class GraphViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GraphSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get("patient_id")
        if not patient_id:
            return Vital.objects.none()
        return Vital.objects.filter(patient_id=patient_id, vital_type="Heart Rate").order_by("recorded_at")

    def list(self, request, *args, **kwargs):
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response({"detail": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)
