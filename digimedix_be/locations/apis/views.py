from rest_framework import viewsets

from digimedix_be.locations.apis.serializers import LocationPostSerializer
from digimedix_be.locations.models import Location

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationPostSerializer
    http_method_names = ["patch", "delete"]
