from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from azura_be.locations.apis.filters import LocationFilter
from azura_be.locations.apis.serializers import LocationPostSerializer
from azura_be.locations.apis.serializers import LocationSerializer
from azura_be.locations.models import Location


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LocationFilter
    ordering_fields = ["name", "status", "type"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return LocationPostSerializer
        return super().get_serializer_class()
