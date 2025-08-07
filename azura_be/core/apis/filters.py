import django_filters
from django.db.models import Q

from azura_be.core.models import Condition
from azura_be.core.models import CPTCode
from azura_be.core.models import HCPCSCode
from azura_be.core.models import ICDCode
from azura_be.core.models import LoincCode
from azura_be.core.models import RxCode
from azura_be.core.models import Specialty


class SpecialtyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
        return queryset

    class Meta:
        model = Specialty
        fields = ["active"]


class ICDCodeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(code__icontains=value))
        return queryset

    class Meta:
        model = ICDCode
        fields = ["icd9"]


class ConditionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="istartswith")
    programs = django_filters.CharFilter(method="search_programs")
    search = django_filters.CharFilter(method="search_query")

    def search_programs(self, queryset, name, value):
        programs_list = [program for program in value.split(",") if program in ["ccm", "pcm", "bhi"]]
        fltr = Q
        for program in programs_list:
            fltr |= Q(**{program: True})
        return queryset.filter(programs_list)

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
        return queryset

    class Meta:
        model = Condition
        fields = []


class CPTCodeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(code__icontains=value))
        return queryset

    class Meta:
        model = CPTCode
        fields = ["type", "category", "section", "subsection"]


class HCPCSCodeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(code__icontains=value))
        return queryset

    class Meta:
        model = HCPCSCode
        fields = ["type", "sequence_number", "record_id"]


class RxCodeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(code__icontains=value))
        return queryset

    class Meta:
        model = RxCode
        fields = ["ndc"]


class LoincCodeFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(field_name="code", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(description__icontains=value) | Q(code__icontains=value))
        return queryset

    class Meta:
        model = LoincCode
        fields = ["category"]
