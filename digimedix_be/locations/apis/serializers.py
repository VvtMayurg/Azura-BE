from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from digimedix_be.base.serializers import AddressSerializer, Base64FileField
from digimedix_be.core.apis.serializers import SpecialtyRelatedSerializer
from digimedix_be.locations.models import Location, LocationWorkingHour
from digimedix_be.provider_groups.apis.serializers import DepartmentRelatedSerializer

class LocationWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHour
        fields = ("day", "start_at", "end_at")


class LocationPostSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    picture = Base64FileField(file_types=["jpg", "jpeg", "png", "svg"], max_file_size=5, required=False, write_only=True)
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)
    working_hours = LocationWorkingHourSerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = ("name", "email", "phone", "npi", "fax", "timezone", "note", "billing_address", "physical_address", "status", "picture", "departments", "specialties", "working_hours")

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
            working_hour_obj = LocationWorkingHour.objects.filter(location=location, day=working_hour.get("day")).first()
            if working_hour_obj is not None:
                working_hour_obj.start_at = working_hour.get("start_at")
                working_hour_obj.end_at = working_hour.get("end_at")
                working_hour_obj.save()
            else:
                LocationWorkingHour.objects.create(location=location, **working_hour)


class LocationSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)
    working_hours = LocationWorkingHourSerializer(many=True, required=False)
    specialties = SpecialtyRelatedSerializer(many=True, required=False)
    departments = DepartmentRelatedSerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = ("id", "created_at", "updated_at","name", "email", "phone", "npi", "fax", "timezone", "note", "billing_address", "physical_address", "status", "picture", "departments", "specialties", "working_hours")

