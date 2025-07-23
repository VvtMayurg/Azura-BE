from rest_framework import viewsets

from azura_be.appointments.apis.serializers import AppointmentCreateSerializer
from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.appointments.apis.serializers import AppointmentUpdateSerializer
from azura_be.appointments.models import Appointment


class AppointmentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        if self.action == "partial_update":
            return AppointmentUpdateSerializer
        return super().get_serializer_class()
