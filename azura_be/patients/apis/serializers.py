from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.serializers import AddressSerializer, Base64FileField
from azura_be.patients.models import Patient
from azura_be.provider_groups.apis.serializers import ProviderGroupRelatedSerializer
from azura_be.users.apis.serializers import UserRelatedSerializer


class PatientRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "first_name", "last_name", "email", "phone")

class PatientCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    picture = Base64FileField(file_types=["jpg", "jpeg", "png", "svg"], max_file_size=5, required=False, write_only=True)

    class Meta:
        model = Patient
        fields = ("first_name", "last_name", "date_of_birth", "gender", "mrn", "provider_group", "email", "phone", "primary_provider", "active", "address", "picture")

class PatientGetSerializer(serializers.ModelSerializer):
    provider_group = ProviderGroupRelatedSerializer()
    primary_provider = UserRelatedSerializer()
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Patient
        fields = "__all__"
