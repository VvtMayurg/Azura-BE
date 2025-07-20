from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from azura_be.base.filterset_classes import SpecialtyFilter
from azura_be.core.apis.serializers import CategorySerializer, FlagSerializer, FrequencySerializer, SpecialtyGetSerializer, SpecialtyPostSerializer, ICDCodeGetSerializer, ICDCodeSerializer, ConditionGetSerializer, ConditionSerializer, CPTCodeGetSerializer, CPTCodeSerializer, HCPCSCodeGetSerializer, HCPCSCodeSerializer, RxCodeGetSerializer, RxCodeSerializer, LoincCodeGetSerializer, LoincCodeSerializer, TagSerializer
from azura_be.core.models import Specialty, ICDCode, Condition, CPTCode, HCPCSCode, RxCode, LoincCode, Frequency, Category, Tag, Flag


class FrequencyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Frequency.objects.all()
    serializer_class = FrequencySerializer

class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class FlagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer



class SpecialtyViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    # Filtering, Searching and Ordering
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SpecialtyFilter
    ordering_fields = ["name", "active", "emergency_available", "created_at"]
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
            OpenApiParameter(name="search", description="Search specialty", type=OpenApiTypes.STR, required=False),
        ],
    )
    @action(detail=True, methods=["GET"], url_path="sub-specialties")
    def sub_specialties(self, request, *args, **kwargs):
        specialty = self.get_object()
        specialties = specialty.sub_specialties.all()
        search = request.query_params.get("search")
        if search:
            specialties = specialties.filter(Q(name__icontains=search) | Q(description__icontains=search))
        page = self.paginate_queryset(specialties)
        serializer = SpecialtyGetSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ICDCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = ICDCode.objects.all()
    serializer_class = ICDCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ICDCodeSerializer
        return super().get_serializer_class()


class ConditionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = Condition.objects.all()
    serializer_class = ConditionGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return ConditionSerializer
        return super().get_serializer_class()

class CPTCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = CPTCode.objects.all()
    serializer_class = CPTCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return CPTCodeSerializer
        return super().get_serializer_class()


class HCPCSCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = HCPCSCode.objects.all()
    serializer_class = HCPCSCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return HCPCSCodeSerializer
        return super().get_serializer_class()

class RxCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = RxCode.objects.all()
    serializer_class = RxCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return RxCodeSerializer
        return super().get_serializer_class()

class LoincCodeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = LoincCode.objects.all()
    serializer_class = LoincCodeGetSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return LoincCodeSerializer
        return super().get_serializer_class()
