from django.utils import dateparse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from azura_be.billings.apis.serializers import CalculateValueResponseSerializer
from azura_be.billings.apis.serializers import CalculateValueSerializer
from azura_be.billings.apis.serializers import DiagnosticCodeResponseSerializer
from azura_be.billings.apis.serializers import EligibilityCheckResponseSerializer
from azura_be.billings.apis.serializers import MasterNumberResponseSerializer
from azura_be.billings.apis.serializers import ServiceCodeResponseSerializer
from azura_be.billings.service import GovernmentBillingService


class InvoiceViewSet(GenericViewSet):
    pagination_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.billing_service = GovernmentBillingService()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="String to search service codes by. Search by code or description",
                required=True,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="active_date",
                description="Date that service code is in effect. Default today's date",
                required=False,
                type=OpenApiTypes.DATE,
            ),
        ],
        responses=ServiceCodeResponseSerializer,
    )
    @action(detail=False, methods=["GET"], url_path="service-codes")
    def get_service_codes(self, request):
        active_date = request.query_params.get("active_date")
        search = request.query_params.get("search")
        params = {}
        if active_date:
            active_date = dateparse.parse_date(active_date).strftime("%Y-%m-%d")
            params.update({"active_date": active_date})
        if search:
            params.update({"search_string": search})

        return Response(self.billing_service.execute("GET", "service_code", params))

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="String to search diagnostic codes by. Search by code or description",
                required=True,
                type=OpenApiTypes.STR,
            ),
        ],
        responses=DiagnosticCodeResponseSerializer,
    )
    @action(detail=False, methods=["GET"], url_path="diagnostic-codes")
    def get_diagnostic_codes(self, request):
        search = request.query_params.get("search")
        params = {}
        if search:
            params.update({"search_string": search})

        return Response(self.billing_service.execute("GET", "diagnostic_codes", params))

    @extend_schema(
        parameters=[
            OpenApiParameter(name="master_number", description="Master number to search visit locations by", required=True, type=OpenApiTypes.STR),
        ],
        responses=MasterNumberResponseSerializer,
    )
    @action(detail=False, methods=["GET"], url_path="ontario-master-number")
    def get_ontario_master_number(self, request):
        master_number = request.query_params.get("master_number")
        if not master_number:
            return Response({"master_number": "Master number is required"}, status=400)
        return Response(self.billing_service.execute("GET", "ontario_master_numbers", {}, path_args=(master_number,)))

    @extend_schema(request=CalculateValueSerializer(many=True), responses=CalculateValueResponseSerializer)
    @action(detail=False, methods=["POST"], url_path="calculate-values")
    def calculate_values(self, request):
        serializer = CalculateValueSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(self.billing_service.execute("POST", "calculate_values", {}, serializer.validated_data))

    @extend_schema(
        parameters=[
            OpenApiParameter(name="health_number", description="Patient's health care number", required=True, type=OpenApiTypes.STR),
            OpenApiParameter(name="birth_date", description="Patient's birth date (YYYY-MM-DD)", required=True, type=OpenApiTypes.STR),
            OpenApiParameter(name="service_code", description="Time limited service code to be checked", required=True, type=OpenApiTypes.STR),
            OpenApiParameter(name="ontario_version_code", description="Patient heath care version code", required=False, type=OpenApiTypes.STR),
            OpenApiParameter(
                name="check_status",
                description="Force a check_status to simulate a pending vs completed check",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses=EligibilityCheckResponseSerializer,
    )
    @action(detail=False, methods=["GET"], url_path="check-service-eligibility")
    def check_service_eligibility(self, request):
        health_number = request.query_params.get("health_number")
        birth_date = request.query_params.get("birth_date")
        service_code = request.query_params.get("service_code")
        ontario_version_code = request.query_params.get("ontario_version_code")
        check_status = request.query_params.get("check_status")

        if not health_number:
            return Response({"health_number": "Health number is required"}, status=400)
        if not birth_date:
            return Response({"birth_date": "Birth date is required"}, status=400)
        if not service_code:
            return Response({"service_code": "Service code is required"}, status=400)

        return Response(
            self.billing_service.execute(
                "GET",
                "eligibility_check",
                params={
                    "health_number": health_number,
                    "birth_date": birth_date,
                    "service_code": service_code,
                    "ontario_version_code": ontario_version_code,
                    "check_status": check_status,
                },
            ),
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="health_number", description="Patient's health care number", required=True, type=OpenApiTypes.STR),
            OpenApiParameter(name="ontario_version_code", description="Patient heath care version code", required=False, type=OpenApiTypes.STR),
            OpenApiParameter(
                name="check_status",
                description="Force a check_status to simulate a pending vs completed check",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="is_eligible",
                description="Allows you to simulate both eligible and ineligible patients",
                required=False,
                type=OpenApiTypes.BOOL,
            ),
        ],
        responses=EligibilityCheckResponseSerializer,
    )
    @action(detail=False, methods=["GET"], url_path="check-eligibility")
    def check_eligibility(self, request):
        health_number = request.query_params.get("health_number")
        ontario_version_code = request.query_params.get("ontario_version_code")
        check_status = request.query_params.get("check_status")
        is_eligible = request.query_params.get("is_eligible")

        if not health_number:
            return Response({"health_number": "Health number is required"}, status=400)

        return Response(
            self.billing_service.execute(
                "GET",
                "eligibility",
                params={
                    "health_number": health_number,
                    "ontario_version_code": ontario_version_code,
                    "check_status": check_status,
                    "is_eligible": is_eligible,
                },
            ),
        )

    @extend_schema(
        responses=EligibilityCheckResponseSerializer,
    )
    @action(detail=False, methods=["POST"], url_path="create-invoice")
    def create_invoice(self, request):
        serializer = EligibilityCheckResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(self.billing_service.execute("POST", "create_invoice", {}, serializer.validated_data))
