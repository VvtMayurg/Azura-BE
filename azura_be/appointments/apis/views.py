import asyncio

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from azura_be.appointments.apis.serializers import AppointmentCreateSerializer
from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.appointments.apis.serializers import AppointmentUpdateSerializer
from azura_be.appointments.apis.serializers import VideoCallTokenSerializer
from azura_be.appointments.filters import AppointmentFilter
from azura_be.appointments.models import Appointment
from azura_be.appointments.utils import generate_livekit_token
from azura_be.appointments.utils import start_video_call_recording


class AppointmentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AppointmentFilter
    ordering_fields = ["start_at", "visit_type", "status", "type"]
    ordering = ["start_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        if self.action == "partial_update":
            return AppointmentUpdateSerializer
        if self.action == "get_video_call_token":
            return VideoCallTokenSerializer
        if self.action == "start_recording":
            return None
        return super().get_serializer_class()

    @action(detail=True, methods=["GET"], url_path="video-call-token")
    def get_video_call_token(self, request, *args, **kwargs):
        appointment = self.get_object()
        user = request.user
        return Response({"token": generate_livekit_token(str(user.uid), user.get_full_name(), appointment.room_name(), room_admin=True)})

    @action(detail=True, methods=["PATCH"], url_path="start-recording")
    def start_recording(self, request, *args, **kwargs):
        appointment = self.get_object()
        asyncio.run(start_video_call_recording(str(appointment.id), appointment.room_name()))
        return Response({"detail": "Recording started"})
