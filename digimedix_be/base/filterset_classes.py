from django_filters.filterset import FilterSet
from django.db.models import Q
from django_filters.filters import CharFilter, BooleanFilter

from digimedix_be.core.models import Specialty

class SpecialtyFilter(FilterSet):
    search = CharFilter(method="filter_by_search")
    name = CharFilter(field_name="name", lookup_expr="istartswith")
    description = CharFilter(field_name="description", lookup_expr="istartswith")
    sub_specialties = BooleanFilter(method="filter_sub_specialties")

    def filter_by_search(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value),
        )

    def filter_sub_specialties(self, queryset, name, value):
        if value:
            return queryset.exclude(parent=None)
        return queryset

    class Meta:
        model = Specialty
        fields = ["search", "name", "description", "active"]

