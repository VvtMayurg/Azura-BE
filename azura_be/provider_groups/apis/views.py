from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from azura_be.provider_groups.apis.filters import DepartmentFilter
from azura_be.provider_groups.apis.filters import ProviderGroupFilter
from azura_be.provider_groups.apis.serializers import AdminDashboardSerializer
from azura_be.provider_groups.apis.serializers import DepartmentPostSerializer
from azura_be.provider_groups.apis.serializers import DepartmentSerializer
from azura_be.provider_groups.apis.serializers import ProviderDashboardSerializer
from azura_be.provider_groups.apis.serializers import ProviderGroupPostSerializer
from azura_be.provider_groups.apis.serializers import ProviderGroupSerializer
from azura_be.provider_groups.dashboard import admin_dashboard_stats
from azura_be.provider_groups.dashboard import provider_dashboard_stats
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


class DashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ProviderDashboardSerializer

    def get_serializer_class(self):
        if self.action == "admin":
            return AdminDashboardSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["GET"], url_path="provider")
    def provider(self, request, *args, **kwargs):
        user = request.user
        return Response(provider_dashboard_stats(user))

    @action(detail=False, methods=["GET"], url_path="admin")
    def admin(self, request, *args, **kwargs):
        user = request.user
        return Response(admin_dashboard_stats(user))
