from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from azura_be.provider_groups.apis.filters import DepartmentFilter
from azura_be.provider_groups.apis.filters import ProviderGroupFilter
from azura_be.provider_groups.apis.serializers import DepartmentPostSerializer
from azura_be.provider_groups.apis.serializers import DepartmentSerializer
from azura_be.provider_groups.apis.serializers import ProviderGroupPostSerializer
from azura_be.provider_groups.apis.serializers import ProviderGroupSerializer
from azura_be.provider_groups.models import Department
from azura_be.provider_groups.models import ProviderGroup


class ProviderGroupViewSet(viewsets.ModelViewSet):
    queryset = ProviderGroup.objects.all()
    serializer_class = ProviderGroupSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProviderGroupFilter
    ordering_fields = ["name", "status"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ProviderGroupPostSerializer
        return super().get_serializer_class()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DepartmentFilter
    ordering_fields = ["name", "active"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return DepartmentPostSerializer
        return super().get_serializer_class()
