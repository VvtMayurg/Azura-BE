from rest_framework import serializers

from azura_be.base.serializers import Base64FileField
from azura_be.communications.models import CommunicationMessage
from azura_be.communications.models import Thread
from azura_be.communications.models import ThreadAttachment
from azura_be.communications.models import ThreadMessage
from azura_be.users.apis.serializers import UserRelatedSerializer


class ThreadSerializer(serializers.ModelSerializer):
    created_by = UserRelatedSerializer(required=False)
    picture = Base64FileField(file_types=["jpg", "jpeg", "png", "svg"], max_file_size=5, required=False, write_only=True)

    class Meta:
        model = Thread
        fields = ("id", "created_at", "created_by", "updated_at", "name", "description", "is_group", "picture")
        read_only_fields = ("id", "created_at", "created_by", "updated_at")


class ThreadAttachmentSerializer(serializers.ModelSerializer):
    file = Base64FileField(file_types=[], max_file_size=10, required=False, write_only=True)

    class Meta:
        model = ThreadAttachment
        fields = ("id", "created_at", "file", "ext")


class ThreadMessageSerializer(serializers.ModelSerializer):
    thread_message_attachments = ThreadAttachmentSerializer(many=True, required=False)
    user = UserRelatedSerializer(required=False)

    class Meta:
        model = ThreadMessage
        fields = ("id", "thread_message_attachments", "user", "content", "has_attachment", "read")


class CommunicationMessageSerializer(serializers.ModelSerializer):
    destination_user = UserRelatedSerializer()

    class Meta:
        model = CommunicationMessage
        fields = (
            "id",
            "created_at",
            "subject",
            "content",
            "read",
            "destination_user",
        )
