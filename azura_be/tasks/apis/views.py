from rest_framework import viewsets

from azura_be.tasks.models import Task
from azura_be.tasks.apis.serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        if self.action == "partial_update":
            return TaskUpdateSerializer
        return super().get_serializer_class()

