from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView
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
from azura_be.mobile_devices.service import TwoFactorAuthService
from azura_be.users.apis.serializers import CustomLogoutSerializer
from azura_be.users.apis.serializers import LicenseGetSerializer
from azura_be.users.apis.serializers import LicenseSerializer
from azura_be.users.apis.serializers import SendOTPSerializer
from azura_be.users.apis.serializers import UserCreateSerializer
from azura_be.users.apis.serializers import UserDetailSerializer
from azura_be.users.apis.serializers import UserPreferenceSerializer
from azura_be.users.apis.serializers import ValidateOTPSerializer
from azura_be.users.apis.serializers import WorkScheduleGetSerializer
from azura_be.users.apis.serializers import WorkScheduleSerializer
from azura_be.users.models import License
from azura_be.users.models import User
from azura_be.users.models import UserPreference
from azura_be.users.models import WorkShedule
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from azura_be.users.filters import UserFilter
from azura_be.users.filters import LicenseFilter
from azura_be.users.filters import WorkScheduleFilter






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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilter
    ordering = ["role"]
    ordering_fields = [            
            "email", 
            "first_name", 
            "last_name", 
            "role",
            "is_provider", 
            "email_notification", 
            "sms_notification",
            "auto_form_save", 
            "two_factor_auth",
            "provider_groups", 
            "departments",
            "created_at_before", 
            "created_at_after",
            "updated_at_before", 
            "updated_at_after",
            "business_account",
            ]

    def get_queryset(self, *args, **kwargs):
        if not self.request.user.account_user:
            self.queryset = self.queryset.filter(account_user=False)
        if self.action != "list":
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
        ],
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
            data=request.data,
            many=True,
            context={"user": user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=WorkScheduleGetSerializer(many=True))
    @action(
        detail=True,
        methods=["GET"],
        url_path="work-schedules",
        pagination_class=None,
    )
    def work_schedules(self, request, *args, **kwargs):
        user = self.get_object()
        work_schedules = WorkShedule.objects.filter(user=user)
        serializer = WorkScheduleGetSerializer(work_schedules, many=True)
        return Response(serializer.data)

    @extend_schema(request=LicenseSerializer, responses=LicenseSerializer)
    @action(
        detail=True,
        methods=["POST"],
        url_path="create-license",
        pagination_class=None,
    )
    def create_license(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = LicenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data)

    @extend_schema(responses=LicenseGetSerializer(many=True))
    @action(detail=True, methods=["POST"], url_path="licenses", pagination_class=None)
    def licenses(self, request, *args, **kwargs):
        user = self.get_object()
        licenses = License.objects.filter(user=user)
        serilaizer = LicenseGetSerializer(licenses, many=True)
        return Response(serilaizer.data)

    @extend_schema(responses=UserPreferenceSerializer)
    @action(
        detail=False,
        methods=["GET", "POST"],
        url_path="preferences",
        pagination_class=None,
    )
    def preferences(self, request, *args, **kwargs):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)

        if request.method == "GET":
            return Response(UserPreferenceSerializer(preference).data)

        serializer = UserPreferenceSerializer(data=request.data, instance=preference)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
            data=request.data,
            context={"request": request},
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
            },
        )


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        user = self.serializer.validated_data.get("user")
        if user.two_factor_auth:
            two_factor_auth_service = TwoFactorAuthService()
            response = two_factor_auth_service.get_devices_response(user)
            if response:
                return response

        self.login()
        return self.get_response()


class TwoFactorAuthenticationViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = SendOTPSerializer

    def get_serializer_class(self):
        if self.action == "validate_otp":
            return ValidateOTPSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["POST"], url_path="send-otp")
    def send_otp(self, request, *args, **kwargs):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        two_factor_auth_service = TwoFactorAuthService()
        return two_factor_auth_service.send_otp(
            serializer.validated_data.get("key"),
            serializer.validated_data.get("device_id"),
            serializer.validated_data.get("device_type"),
        )

    @action(detail=False, methods=["POST"], url_path="validate-otp")
    def validate_otp(self, request, *args, **kwargs):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        two_factor_auth_service = TwoFactorAuthService()
        return two_factor_auth_service.validate_otp(
            serializer.validated_data.get("key"),
            serializer.validated_data.get("device_id"),
            serializer.validated_data.get("device_type"),
            serializer.validated_data.get("otp"),
        )

class LicenseViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LicenseFilter
    ordering_fields = [
            "number", 
            "state", 
            "npi", 
            "dea_number",
            "expiry_before", 
            "expiry_after",
            "user_id", 
            "user_email",
            "specialty_id", 
            "specialty_name",
    ]
    ordering = ["User_id"]
    
    
class WorkScheduleViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = WorkShedule.objects.all()
    serializer_class = WorkScheduleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WorkScheduleFilter
    ordering_fields = [
            "day",
            "start_after", 
            "start_before",
            "end_after", 
            "end_before",
            "user_id", 
            "user_email",
    ]
    ordering = ["User_id"]

