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
