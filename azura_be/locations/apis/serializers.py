from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.serializers import AddressSerializer
from azura_be.base.serializers import Base64FileField
from azura_be.core.apis.serializers import SpecialtyRelatedSerializer
from azura_be.locations.models import Location
from azura_be.locations.models import LocationWorkingHour


class LocationRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "email")


class LocationWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHour
        fields = ("day", "start_at", "end_at")


class LocationPostSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    picture = Base64FileField(
        file_types=["jpg", "jpeg", "png", "svg"],
        max_file_size=5,
        required=False,
        write_only=True,
    )
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)
    working_hours = LocationWorkingHourSerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = (
            "name",
            "email",
            "phone",
            "npi",
            "fax",
            "timezone",
            "note",
            "billing_address",
            "physical_address",
            "status",
            "picture",
            "specialties",
            "working_hours",
            "type",
        )

    def create(self, validated_data):
        working_hours = validated_data.pop("working_hours", [])
        location = super().create(validated_data)
        self.handle_working_locations(location, working_hours)
        return location

    def update(self, instance, validated_data):
        working_hours = validated_data.pop("working_hours", [])
        location = super().update(instance, validated_data)
        self.handle_working_locations(location, working_hours)
        return location

    def handle_working_locations(self, location, working_hours):
        for working_hour in working_hours or []:
            working_hour_obj = LocationWorkingHour.objects.filter(
                location=location,
                day=working_hour.get("day"),
            ).first()
            if working_hour_obj is not None:
                working_hour_obj.start_at = working_hour.get("start_at")
                working_hour_obj.end_at = working_hour.get("end_at")
                working_hour_obj.save()
            else:
                LocationWorkingHour.objects.create(location=location, **working_hour)


class ProviderGroupRelatedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    email = serializers.EmailField()


class LocationSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)
    working_hours = LocationWorkingHourSerializer(many=True, required=False)
    specialties = SpecialtyRelatedSerializer(many=True, required=False)
    provider_group = serializers.SerializerMethodField()

    def get_provider_group(self, instance) -> ProviderGroupRelatedSerializer:
        provider_group = instance.provider_group
        return {
            "id": str(provider_group.id),
            "name": str(provider_group.name),
            "email": str(provider_group.email),
        }

    class Meta:
        model = Location
        fields = (
            "id",
            "provider_group",
            "created_at",
            "updated_at",
            "name",
            "email",
            "phone",
            "npi",
            "fax",
            "timezone",
            "note",
            "billing_address",
            "physical_address",
            "status",
            "picture",
            "specialties",
            "working_hours",
            "type",
        )
