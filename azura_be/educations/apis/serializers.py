from rest_framework import serializers

from azura_be.base.serializers import Base64FileField
from azura_be.core.apis.serializers import ConditionRelatedSerializer
from azura_be.core.apis.serializers import SpecialtyRelatedSerializer
from azura_be.educations.models import Education
from azura_be.educations.models import PatientEducation
from azura_be.patients.models import Patient


class EducationCreateSerializer(serializers.ModelSerializer):
    file = Base64FileField(
        file_types=[], max_file_size=5, required=False, write_only=True
    )

    class Meta:
        model = Education
        fields = (
            "title",
            "specialties",
            "information",
            "conditions",
            "form_type",
            "file",
        )


class EducationSerializer(serializers.ModelSerializer):
    specialties = SpecialtyRelatedSerializer(many=True, required=False)
    conditions = ConditionRelatedSerializer(many=True, required=False)

    class Meta:
        model = Education
        fields = "__all__"


class AssignUnassignPatientEducationSerializer(serializers.ModelSerializer):
    patients = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    )
    assign = serializers.BooleanField(default=False)

    def save(self):
        data = self.validated_data
        eduction = self.context.get("education")
        assign = data.get("assign")

        if assign:
            for patient in data.get("patients"):
                if not PatientEducation.objects.filter(
                    eduction=eduction, patient=patient
                ).exists():
                    PatientEducation.objects.create(education=eduction, patient=patient)
        else:
            for patient in data.get("patients"):
                PatientEducation.objects.filter(
                    eduction=eduction, patient=patient
                ).delete()
