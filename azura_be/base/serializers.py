import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    address_line_1 = serializers.CharField(allow_blank=True, required=False)
    address_line_2 = serializers.CharField(allow_blank=True, required=False)
    country = serializers.CharField(allow_blank=True, required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    state = serializers.CharField(allow_blank=True, required=False)
    zip_code = serializers.CharField(allow_blank=True, required=False)


class Base64FileField(serializers.FileField):
    def __init__(self, file_types=None, max_file_size=None, **kwargs):
        self.file_types = file_types
        self.max_file_size = max_file_size
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str):
            if ";base64," not in data:
                raise serializers.ValidationError(
                    detail="Please upload correct base64 string.",
                )
            file_name = str(uuid.uuid4())[:12]
            file_extension, data = self.get_file_extension(data)

            if self.file_types and file_extension not in self.file_types:
                raise serializers.ValidationError(
                    detail="Please upload correct file.",
                )

            try:
                decoded_file = base64.b64decode(data)
            except Exception:
                self.fail("invalid_file")

            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)
            if self.max_file_size and data.size > self.max_file_size * 1025 * 1025:
                msg = "File size should not be more than 60 MB"
                raise serializers.ValidationError(msg)
        return super().to_internal_value(data)

    def get_file_extension(self, encoded_data):
        frmt, data = encoded_data.split(";base64,")
        if (
            frmt
            == "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            frmt = "xlsx"
        if frmt == "data:application/vnd.ms-excel":
            frmt = "xls"
        if frmt == "data:application/vnd.ms-powerpoint":
            frmt = "ppt"
        if (
            frmt
            == "data:application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            frmt = "docx"
        if frmt == "data:application/octet-stream":
            frmt = "txt"
        if frmt == "data:image/svg+xml":
            frmt = "svg"
        ext = frmt.split("/")[-1]
        return ext, data


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    extra = serializers.DictField(required=False)
