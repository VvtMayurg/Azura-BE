from dj_rest_auth.views import LogoutView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from azura_be.users.apis.serializers import CustomLogoutSerializer
from azura_be.users.apis.serializers import UserDetailSerializer
from azura_be.users.models import User


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(request=CustomLogoutSerializer, responses=CustomLogoutSerializer)
class CustomLogoutView(LogoutView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]
