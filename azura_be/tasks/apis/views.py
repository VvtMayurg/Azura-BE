from rest_framework import viewsets

from azura_be.tasks.apis.serializers import TaskCreateSerializer
from azura_be.tasks.apis.serializers import TaskSerializer
from azura_be.tasks.apis.serializers import TaskUpdateSerializer
from azura_be.tasks.models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from azura_be.tasks.filters import TaskFilter



class TaskViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["reason","description","priority","completed","patient_id","user_id","due_after","due_before","completed_after","completed_before"]
    ordering = ["user_id"]

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        if self.action == "partial_update":
            return TaskUpdateSerializer
        return super().get_serializer_class()
