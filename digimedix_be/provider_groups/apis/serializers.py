from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from digimedix_be.base.serializers import AddressSerializer, Base64FileField
from digimedix_be.provider_groups.models import ProviderGroup, Department
from digimedix_be.users.apis.serializers import UserRelativeSerializer


class ProviderGroupPostSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    picture = Base64FileField(file_types=["jpg", "jpeg", "png", "svg"], max_file_size=5, required=False, write_only=True)
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)

    class Meta:
        model = ProviderGroup
        fields = (
            "group_name",
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
            "group_name",
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


class DepartmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("name", "admin", "phone", "active")


class DepartmentSerializer(serializers.ModelSerializer):
    admin = UserRelativeSerializer()

    class Meta:
        model = Department
        fields = ("id", "created_at", "updated_at", "name", "admin", "phone", "active")
