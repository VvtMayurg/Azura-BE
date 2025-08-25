import django_filters

from azura_be.appointments.models import Appointment
from azura_be.appointments.models import Vaccine


class AppointmentFilter(django_filters.FilterSet):
    start_at = django_filters.DateTimeFilter(field_name="start_at", lookup_expr="gte")
    end_at = django_filters.DateTimeFilter(field_name="start_at", lookup_expr="lte")
    location = django_filters.CharFilter(field_name="location__name", lookup_expr="istartswith")
    provider_group = django_filters.CharFilter(field_name="provider_group__name", lookup_expr="istartswith")
    email = django_filters.CharFilter(field_name="email", lookup_expr="iexact")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="iexact")

    class Meta:
        model = Appointment
        fields = ["type", "visit_type", "status"]


class VaccineFilter(django_filters.FilterSet):
    class Meta:
        model = Vaccine
        fields = ["completed"]
