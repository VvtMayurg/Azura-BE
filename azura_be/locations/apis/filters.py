import django_filters
from django.db.models import Q

from azura_be.locations.models import Location


class LocationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="istartswith")
    code = django_filters.CharFilter(field_name="code", lookup_expr="iexact")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="iexact")
    email = django_filters.CharFilter(field_name="email", lookup_expr="iexact")
    provider_group = django_filters.CharFilter(field_name="provider_group__name", lookup_expr="istartswith")
    search = django_filters.CharFilter(method="search_query")

    def search_query(self, queryset, name, value):
        if value:
            return queryset.filter(Q(name__icontains=value) | Q(note__icontains=value))
        return queryset

    class Meta:
        model = Location
        fields = ["type", "status"]
