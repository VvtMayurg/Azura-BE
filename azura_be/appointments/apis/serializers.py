from rest_framework import serializers

from azura_be.appointments.models import Appointment
from azura_be.patients.apis.serializers import PatientRelatedSerializer
from azura_be.users.apis.serializers import UserRelatedSerializer

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("patient", "user", "type", "description", "start_at", "end_at", "location", "visit_type", "instructions", "payment", "billing", "state", "referring_provider")

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("patient", "user", "type", "description", "start_at", "end_at", "location", "visit_type", "instructions", "payment", "billing", "state", "referring_provider", "status", "completed_at")
    
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientRelatedSerializer()
    user = UserRelatedSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
