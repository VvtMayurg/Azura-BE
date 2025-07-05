from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from digimedix_be.locations.apis.serializers import LocationPostSerializer, LocationSerializer
from digimedix_be.locations.models import Location
from digimedix_be.provider_groups.apis.serializers import DepartmentSerializer, ProviderGroupPostSerializer, ProviderGroupSerializer, DepartmentPostSerializer
from digimedix_be.provider_groups.models import ProviderGroup, Department


class ProviderGroupViewSet(viewsets.ModelViewSet):
    queryset = ProviderGroup.objects.all()
    serializer_class = ProviderGroupSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ProviderGroupPostSerializer
        return super().get_serializer_class()

    @extend_schema(request=DepartmentPostSerializer, responses=DepartmentPostSerializer)
    @action(detail=True, methods=["POST"], url_path="create-department")
    def create_department(self, request, *args, **kwargs):
        provider_group = self.get_object()
        serializer = DepartmentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider_group=provider_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=DepartmentSerializer(many=True))
    @action(detail=True, methods=["GET"], url_path="departments")
    def departments(self, request, *args, **kwargs):
        provider_group = self.get_object()
        departments = Department.objects.filter(provider_group=provider_group)
        page = self.paginate_queryset(departments)
        serializer = DepartmentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(request=LocationPostSerializer, responses=LocationPostSerializer)
    @action(detail=True, methods=["POST"], url_path="create-location")
    def create_location(self, request, *args, **kwargs):
        provider_group = self.get_object()
        serializer = LocationPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider_group=provider_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=LocationSerializer(many=True))
    @action(detail=True, methods=["GET"], url_path="locations")
    def locations(self, request, *args, **kwargs):
        provider_group = self.get_object()
        departments = Location.objects.filter(provider_group=provider_group)
        page = self.paginate_queryset(departments)
        serializer = LocationSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentPostSerializer
    http_method_names = ["patch", "delete"]
