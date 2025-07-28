from rest_framework import serializers

from azura_be.base.serializers import Base64FileField
from azura_be.documents.models import Document


class DocumentCreateSerializer(serializers.ModelSerializer):
    file = Base64FileField(
        file_types=[],
        max_file_size=10,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Document
        fields = ("name", "description", "patient", "category", "file")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
