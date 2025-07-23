from rest_framework import serializers

from azura_be.patients.apis.serializers import PatientRelatedSerializer
from azura_be.tasks.models import Task
from azura_be.users.apis.serializers import UserRelatedSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("reason", "patient", "user", "due_at", "priority", "description")


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "reason",
            "patient",
            "user",
            "due_at",
            "priority",
            "description",
            "completed",
            "completed_at",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        due_at = attrs.get("due_at", self.instance.due_at)
        completed_at = attrs.get("completed_at")
        if completed_at and due_at > completed_at:
            raise serializers.ValidationError(
                detail={
                    "completed_at": "Completed date time can not be greater than due date time"
                }
            )
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    patient = PatientRelatedSerializer()
    user = UserRelatedSerializer()

    class Meta:
        model = Task
        fields = "__all__"
