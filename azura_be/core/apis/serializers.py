from rest_framework import serializers

from azura_be.core.models import Specialty


class SpecialtyRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name")


class SpecialtyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("name", "description", "active", "parent")


class SpecialtyGetSerializer(serializers.ModelSerializer):
    parent = SpecialtyRelatedSerializer(required=False)

    class Meta:
        model = Specialty
        fields = "__all__"
