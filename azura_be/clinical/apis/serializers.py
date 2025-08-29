from rest_framework import serializers

from azura_be.clinical.models import LabResult
from azura_be.clinical.models import Medication
from azura_be.clinical.models import Vital


class VitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ("patient", "vital_type", "value", "value1", "unit", "recorded_at", "metadata")


class VitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ("id", "value", "value1", "unit", "recorded_at", "metadata")


class MedicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ("patient", "medicine", "type", "sig", "qty", "unit", "refills", "days")


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ("id", "medicine", "type", "sig", "qty", "unit", "refills", "days")


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        exclude = ("patient",)



class LatestVitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = '__all__'
        

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ['recorded_at', 'value', 'unit']
