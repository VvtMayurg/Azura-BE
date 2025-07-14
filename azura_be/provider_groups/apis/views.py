from rest_framework import viewsets

from azura_be.provider_groups.apis.serializers import DepartmentSerializer, ProviderGroupPostSerializer, ProviderGroupSerializer, DepartmentPostSerializer
from azura_be.provider_groups.models import ProviderGroup, Department


class ProviderGroupViewSet(viewsets.ModelViewSet):
    queryset = ProviderGroup.objects.all()
    serializer_class = ProviderGroupSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ProviderGroupPostSerializer
        return super().get_serializer_class()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return DepartmentPostSerializer
        return super().get_serializer_class()
