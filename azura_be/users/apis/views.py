from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LogoutView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from azura_be.business_accounts.apis.serializers import BusinessAccountSignUpSerializer
from azura_be.business_accounts.apis.serializers import SignUpResponseSerializer
from azura_be.business_accounts.models import BusinessAccount
from azura_be.users.apis.serializers import CustomLogoutSerializer
from azura_be.users.apis.serializers import LicenseGetSerializer
from azura_be.users.apis.serializers import LicenseSerializer
from azura_be.users.apis.serializers import UserCreateSerializer
from azura_be.users.apis.serializers import UserDetailSerializer
from azura_be.users.apis.serializers import WorkScheduleGetSerializer
from azura_be.users.apis.serializers import WorkScheduleSerializer
from azura_be.users.models import License
from azura_be.users.models import User
from azura_be.users.models import WorkShedule


class UserViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = UserDetailSerializer
    http_method_names = ["get", "post", "patch"]
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        if not self.request.user.account_user:
            self.queryset = self.queryset.filter(account_user=False)
        if not self.action == "list":
            return self.queryset
        account_user = self.request.query_params.get("account_user")
        if account_user == "true":
            self.queryset = self.queryset.filter(account_user=True)
        if account_user == "false":
            self.queryset = self.queryset.filter(account_user=False)
        return self.queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="account_user",
                required=False,
                type=OpenApiTypes.BOOL,
                description="Filter based on account user or provider",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return UserCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if not self.request.user.account_user:
            serializer.validated_data.pop("account_user", None)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if not self.request.user.account_user:
            serializer.validated_data.pop("account_user", None)
        return super().perform_create(serializer)

    @action(detail=False)
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        request=WorkScheduleSerializer(many=True),
        responses=WorkScheduleSerializer(many=True),
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="manage-work-schedules",
        pagination_class=None,
    )
    def manage_work_schedules(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = WorkScheduleSerializer(
            data=request.data, many=True, context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=WorkScheduleGetSerializer(many=True))
    @action(
        detail=True, methods=["GET"], url_path="work-schedules", pagination_class=None
    )
    def work_schedules(self, request, *args, **kwargs):
        user = self.get_object()
        work_schedules = WorkShedule.objects.filter(user=user)
        serializer = WorkScheduleGetSerializer(work_schedules, many=True)
        return Response(serializer.data)

    @extend_schema(request=LicenseSerializer, responses=LicenseSerializer)
    @action(
        detail=True, methods=["POST"], url_path="create-license", pagination_class=None
    )
    def create_license(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = LicenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data)

    @extend_schema(responses=LicenseGetSerializer)
    @action(detail=True, methods=["POST"], url_path="licenses", pagination_class=None)
    def licenses(self, request, *args, **kwargs):
        user = self.get_object()
        licenses = License.objects.filter(user=user)
        serilaizer = LicenseGetSerializer(licenses, many=True)
        return Response(serilaizer.data)


@extend_schema(request=CustomLogoutSerializer, responses=CustomLogoutSerializer)
class CustomLogoutView(LogoutView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]


class BusinessAccountSignUpViewSet(viewsets.GenericViewSet):
    queryset = BusinessAccount.objects.all()
    serializer_class = BusinessAccountSignUpSerializer
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses=SignUpResponseSerializer)
    @action(detail=False, methods=["POST"], url_path="signup")
    def signup(self, request):
        serializer = BusinessAccountSignUpSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data.pop("validate_only", False):
            instance = serializer.save()
            user = serializer.user
            return self.generate_access_token(instance.id, user)
        return Response(serializer.data)

    def generate_access_token(self, account_id, user):
        access, _ = jwt_encode(user)
        return Response(
            {
                "account_id": account_id,
                "access": str(access),
            }
        )
