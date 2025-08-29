
import django_filters
from azura_be.users.models import User,License,WorkShedule

class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name="email", 
        lookup_expr="icontains",
        required=False,
        )
    first_name = django_filters.CharFilter(
        field_name="first_name", 
        lookup_expr="icontains",
        required=False,
        )
    last_name = django_filters.CharFilter(
        field_name="last_name", 
        lookup_expr="icontains",
        require=False,
        )
    role = django_filters.CharFilter(
        field_name="role", 
        lookup_expr="icontains",
        require=False,
        )
    is_provider = django_filters.BooleanFilter(
        field_name="is_provider",
        require=False,
        )
    email_notification = django_filters.BooleanFilter(
        field_name="email_notification",
        require=False,
        )
    sms_notification = django_filters.BooleanFilter(
        field_name="sms_notification",
        require=False,
        )
    auto_form_save = django_filters.BooleanFilter(
        field_name="auto_form_save",
        require=False,
        )
    two_factor_auth = django_filters.BooleanFilter(
        field_name="two_factor_auth",
        require=False,
        )
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", 
        lookup_expr="lte",
        require=False,
        )
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", 
        lookup_expr="gte",
        require=False,
        )
    updated_at_before = django_filters.DateTimeFilter(
        field_name="updated_at", 
        lookup_expr="lte",
        require=False,
        )
    updated_at_after = django_filters.DateTimeFilter(
        field_name="updated_at", 
        lookup_expr="gte",
        require=False,
        )
    provider_groups = django_filters.CharFilter(
        method="filter_array_contains",
        require=False,
        )
    departments = django_filters.CharFilter(
        method="filter_array_contains",
        require=False,
        )
    business_account = django_filters.UUIDFilter(
        method="filter_business_account",
        require=False,
        )

    class Meta:
        model = User
        fields = [
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

    def filter_array_contains(self, queryset, name, value):
        """Filter ArrayFields by checking if a UUID is inside the array"""
        return queryset.filter(**{f"{name}__contains": [value]})

    def filter_business_account(self, queryset, name, value):
        """Filter users by linked business account"""
        return queryset.filter(business_accounts__id=value)

class LicenseFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(
        field_name="number", 
        lookup_expr="icontains"
        )
    state = django_filters.CharFilter(
        field_name="state", 
        lookup_expr="icontains"
        )
    npi = django_filters.CharFilter(
        field_name="npi", 
        lookup_expr="icontains",
        required=False,
        )
    dea_number = django_filters.CharFilter(
        field_name="dea_number", 
        lookup_expr="icontains",
        required=False,
        )
    expiry_before = django_filters.DateFilter(
        field_name="exiry_date", 
        lookup_expr="lte",
        required=False,
        )
    expiry_after = django_filters.DateFilter(
        field_name="exiry_date", 
        lookup_expr="gte",
        required=False,
        )
    user_id = django_filters.UUIDFilter(
        field_name="user__uid",
        required=False,
        )
    user_email = django_filters.CharFilter(
        field_name="user__email", 
        lookup_expr="icontains",
        required=False,
        )
    specialty_id = django_filters.NumberFilter(
        field_name="specialties__id",
        required=False,
        )
    specialty_name = django_filters.CharFilter(
        field_name="specialties__name", 
        lookup_expr="icontains",
        required=False,
        )
    class Meta:
        model = License
        fields = [
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

class WorkSheduleFilter(django_filters.FilterSet):
    day = django_filters.CharFilter(
        field_name="day", 
        lookup_expr="iexact",
        required=False,
        )

    start_after = django_filters.TimeFilter(
        field_name="start", 
        lookup_expr="gte",
        required=False,
        )
    start_before = django_filters.TimeFilter(
        field_name="start", 
        lookup_expr="lte",
        required=False,
        )
    end_after = django_filters.TimeFilter(
        field_name="end", 
        lookup_expr="gte",
        required=False,
        )
    end_before = django_filters.TimeFilter(
        field_name="end", 
        lookup_expr="lte",
        required=False,
        )

    user_id = django_filters.UUIDFilter(
        field_name="user__uid",
        required=False,
        )
    user_email = django_filters.CharFilter(
        field_name="user__email", 
        lookup_expr="icontains",
        required=False,
        )

    class Meta:
        model = WorkShedule
        fields = [
            "day",
            "start_after", 
            "start_before",
            "end_after", 
            "end_before",
            "user_id", 
            "user_email",
        ]
