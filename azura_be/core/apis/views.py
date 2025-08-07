from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter

from azura_be.core.apis.filters import ConditionFilter
from azura_be.core.apis.filters import CPTCodeFilter
from azura_be.core.apis.filters import HCPCSCodeFilter
from azura_be.core.apis.filters import ICDCodeFilter
from azura_be.core.apis.filters import LoincCodeFilter
from azura_be.core.apis.filters import RxCodeFilter
from azura_be.core.apis.filters import SpecialtyFilter
from azura_be.core.apis.serializers import CategorySerializer
from azura_be.core.apis.serializers import ConditionGetSerializer
from azura_be.core.apis.serializers import ConditionSerializer
from azura_be.core.apis.serializers import CPTCodeGetSerializer
from azura_be.core.apis.serializers import CPTCodeSerializer
from azura_be.core.apis.serializers import FlagSerializer
from azura_be.core.apis.serializers import FrequencySerializer
from azura_be.core.apis.serializers import HCPCSCodeGetSerializer
from azura_be.core.apis.serializers import HCPCSCodeSerializer
from azura_be.core.apis.serializers import ICDCodeGetSerializer
from azura_be.core.apis.serializers import ICDCodeSerializer
from azura_be.core.apis.serializers import LoincCodeGetSerializer
from azura_be.core.apis.serializers import LoincCodeSerializer
from azura_be.core.apis.serializers import RxCodeGetSerializer
from azura_be.core.apis.serializers import RxCodeSerializer
from azura_be.core.apis.serializers import SpecialtyGetSerializer
from azura_be.core.apis.serializers import SpecialtyPostSerializer
from azura_be.core.apis.serializers import TagSerializer
from azura_be.core.models import Category
from azura_be.core.models import Condition
from azura_be.core.models import CPTCode
from azura_be.core.models import Flag
from azura_be.core.models import Frequency
from azura_be.core.models import HCPCSCode
from azura_be.core.models import ICDCode
from azura_be.core.models import LoincCode
from azura_be.core.models import RxCode
from azura_be.core.models import Specialty
from azura_be.core.models import Tag


class FrequencyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Frequency.objects.all()
    serializer_class = FrequencySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class FlagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class SpecialtyViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SpecialtyFilter
    ordering_fields = ["name", "active", "category"]
    ordering = ["name"]

    queryset = Specialty.objects.all()
    serializer_class = SpecialtyGetSerializer

    def filter_queryset(self, queryset):
        if self.action != "list":
            return queryset
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get("sub_specialties") != "true" and self.action == "list":
            return queryset.filter(parent=None)
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SpecialtyPostSerializer
        return super().get_serializer_class()

    @extend_schema(
        responses=SpecialtyGetSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search specialty",
                type=OpenApiTypes.STR,
                required=False,
            ),
        ],
    )
    @action(detail=True, methods=["GET"], url_path="sub-specialties")
    def sub_specialties(self, request, *args, **kwargs):
        specialty = self.get_object()
        specialties = specialty.sub_specialties.all()
        search = request.query_params.get("search")
        if search:
            specialties = specialties.filter(
                Q(name__icontains=search) | Q(description__icontains=search),
            )
        page = self.paginate_queryset(specialties)
        serializer = SpecialtyGetSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ICDCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ICDCodeFilter
    ordering_fields = ["title", "code", "icd9"]
    ordering = ["title"]

    queryset = ICDCode.objects.all()
    serializer_class = ICDCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ICDCodeSerializer
        return super().get_serializer_class()


class ConditionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConditionFilter
    ordering_fields = ["name"]
    ordering = ["name"]

    queryset = Condition.objects.all()
    serializer_class = ConditionGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ConditionSerializer
        return super().get_serializer_class()


class CPTCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CPTCodeFilter
    ordering_fields = ["title", "code", "type", "category", "section"]
    ordering = ["title"]

    queryset = CPTCode.objects.all()
    serializer_class = CPTCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return CPTCodeSerializer
        return super().get_serializer_class()


class HCPCSCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HCPCSCodeFilter
    ordering_fields = ["title", "code", "type", "sequence_number"]
    ordering = ["title"]

    queryset = HCPCSCode.objects.all()
    serializer_class = HCPCSCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return HCPCSCodeSerializer
        return super().get_serializer_class()


class RxCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RxCodeFilter
    ordering_fields = ["title", "code", "ndc"]
    ordering = ["title"]

    queryset = RxCode.objects.all()
    serializer_class = RxCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return RxCodeSerializer
        return super().get_serializer_class()


class LoincCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LoincCodeFilter
    ordering_fields = ["code", "category"]
    ordering = ["code"]

    queryset = LoincCode.objects.all()
    serializer_class = LoincCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return LoincCodeSerializer
        return super().get_serializer_class()
