from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.serializers import AddressSerializer, Base64FileField
from azura_be.locations.apis.serializers import LocationRelatedSerializer
from azura_be.provider_groups.models import ProviderGroup, Department
from azura_be.users.apis.serializers import UserRelatedSerializer

class ProviderGroupRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderGroup
        fields = ("id", "name", "email")

class ProviderGroupPostSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    picture = Base64FileField(file_types=["jpg", "jpeg", "png", "svg"], max_file_size=5, required=False, write_only=True)
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)

    class Meta:
        model = ProviderGroup
        fields = (
            "name",
            "website",
            "email",
            "status",
            "picture",
            "phone",
            "billing_address",
            "physical_address",
            "bio",
            "timezone",
        )

class ProviderGroupSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)

    class Meta:
        model = ProviderGroup
        fields = (
            "id",
            "created_at",
            "updated_at",
            "name",
            "website",
            "email",
            "status",
            "picture",
            "phone",
            "billing_address",
            "physical_address",
            "bio",
            "timezone",
        )

class DepartmentRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name",)

class DepartmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("name", "admin", "phone", "active", "locations", "provider_groups")


class DepartmentSerializer(serializers.ModelSerializer):
    admin = UserRelatedSerializer()
    locations = LocationRelatedSerializer(many=True, required=False)
    provider_groups = ProviderGroupRelatedSerializer(many=True, required=False)

    class Meta:
        model = Department
        fields = ("id", "created_at", "updated_at", "name", "admin", "phone", "active", "locations", "provider_groups")
