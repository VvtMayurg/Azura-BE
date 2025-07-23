from rest_framework import viewsets

from azura_be.locations.apis.serializers import LocationPostSerializer
from azura_be.locations.apis.serializers import LocationSerializer
from azura_be.locations.models import Location


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return LocationPostSerializer
        return super().get_serializer_class()
