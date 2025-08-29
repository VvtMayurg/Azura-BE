from rest_framework import viewsets

from azura_be.plans.apis.serializers import FormCreateSerializer
from azura_be.plans.apis.serializers import FormSerializer
from azura_be.plans.apis.serializers import PlanCreateSerializer
from azura_be.plans.apis.serializers import PlanSerializer
from azura_be.plans.models import Form
from azura_be.plans.models import Plan
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from azura_be.plans.filters import PlanFilter





class FormViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return FormCreateSerializer
        return super().get_serializer_class()


class PlanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PlanFilter
    ordering_fields = ['id','programs','name','conditions','iccd_codes',]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PlanCreateSerializer
        return super().get_serializer_class()
