from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from digimedix_be.base.serializers import AddressSerializer, Base64FileField
from digimedix_be.provider_groups.models import ProviderGroup


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
        fields = "__all__"
