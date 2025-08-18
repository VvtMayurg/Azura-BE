from rest_framework import serializers

from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.clinical.apis.serializers import MedicationSerializer
from azura_be.communications.apis.serializers import ThreadMessageSerializer


class AppointmentStatsSerializer(serializers.Serializer):
    scheduled = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    not_show = serializers.IntegerField()
    declined = serializers.IntegerField()


class PatientDashboardSerializer(serializers.Serializer):
    appointments = AppointmentStatsSerializer()
    upcoming_appointments = AppointmentSerializer(many=True)
    lab_results = serializers.IntegerField()
    medication = MedicationSerializer(many=True)
    chat = ThreadMessageSerializer(many=True)
