from rest_framework import viewsets

from digimedix_be.provider_groups.apis.serializers import ProviderGroupPostSerializer, ProviderGroupSerializer
from digimedix_be.provider_groups.models import ProviderGroup


class ProviderGroupViewSet(viewsets.ModelViewSet):
    queryset = ProviderGroup.objects.all()
    serializer_class = ProviderGroupSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ProviderGroupPostSerializer
        return super().get_serializer_class()
