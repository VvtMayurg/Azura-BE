from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.serializers import AddressSerializer
from azura_be.base.serializers import Base64FileField
from azura_be.communications.apis.serializers import ThreadMessageSerializer
from azura_be.locations.apis.serializers import LocationRelatedSerializer
from azura_be.provider_groups.models import Department
from azura_be.provider_groups.models import ProviderGroup
from azura_be.users.apis.serializers import UserRelatedSerializer


class ProviderGroupRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderGroup
        fields = ("id", "name", "email")


class ProviderGroupPostSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    picture = Base64FileField(
        file_types=["jpg", "jpeg", "png", "svg"],
        max_file_size=5,
        required=False,
        write_only=True,
    )
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)

    class Meta:
        model = ProviderGroup
        fields = (
            "name",
            "group_type",
            "website",
            "email",
            "status",
            "picture",
            "phone",
            "billing_address",
            "physical_address",
            "bio",
            "timezone",
            "code",
        )


class ProviderGroupSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()
    billing_address = AddressSerializer(required=False)
    physical_address = AddressSerializer(required=False)

    class Meta:
        model = ProviderGroup
        fields = (
            "id",
            "created_at",
            "updated_at",
            "name",
            "group_type",
            "website",
            "email",
            "status",
            "picture",
            "phone",
            "billing_address",
            "physical_address",
            "bio",
            "timezone",
            "code",
        )


class DepartmentRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name")


class DepartmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("name", "admin", "phone", "active", "locations", "provider_groups")


class DepartmentSerializer(serializers.ModelSerializer):
    admin = UserRelatedSerializer()
    locations = LocationRelatedSerializer(many=True, required=False)
    provider_groups = ProviderGroupRelatedSerializer(many=True, required=False)

    class Meta:
        model = Department
        fields = (
            "id",
            "created_at",
            "updated_at",
            "name",
            "admin",
            "phone",
            "active",
            "locations",
            "provider_groups",
        )


class AppointmentStatSerializer(serializers.Serializer):
    scheduled = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    not_show = serializers.IntegerField()
    declined = serializers.IntegerField()


class ProviderDashboardSerializer(serializers.Serializer):
    lab_results = serializers.IntegerField()
    tasks = serializers.IntegerField()
    unsigned_encounter = serializers.IntegerField()
    claim_received = serializers.IntegerField()
    claim_in_progress = serializers.IntegerField()
    claim_requiring_action = serializers.IntegerField()

    appointments = AppointmentStatSerializer()
    chat = ThreadMessageSerializer(many=True, required=False)


class OverviewSerializer(serializers.Serializer):
    provider_groups = serializers.IntegerField()
    locations = serializers.IntegerField()
    departments = serializers.IntegerField()
    specialties = serializers.IntegerField()
    users = serializers.IntegerField()
    organization_users = serializers.IntegerField()


class AllModulesSerializer(serializers.Serializer):
    provider_groups = serializers.IntegerField()
    locations = serializers.IntegerField()
    departments = serializers.IntegerField()
    specialties = serializers.IntegerField()
    organization_users = serializers.IntegerField()
    form_builders = serializers.IntegerField()
    custom_forms = serializers.IntegerField()
    form_templates = serializers.IntegerField()
    email_sms_templates = serializers.IntegerField()
    coding_management = serializers.IntegerField()
    audit_logs = serializers.IntegerField()
    billing_payments = serializers.IntegerField()
    subscription_plans = serializers.IntegerField()
    user_profiles = serializers.IntegerField()
    configurations = serializers.IntegerField()


class AgeDistributionSerializer(serializers.Serializer):
    under_18 = serializers.IntegerField()
    above_18_under_25 = serializers.IntegerField()
    above_36_under_55 = serializers.IntegerField()
    above_56 = serializers.IntegerField()


class MonthlyRegistrationsSerializer(serializers.Serializer):
    jan = serializers.IntegerField()
    feb = serializers.IntegerField()
    dec = serializers.IntegerField()


class TopPerformingProviderSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    patients = serializers.IntegerField()


class AnalyticsSerializer(serializers.Serializer):
    age_distribution = AgeDistributionSerializer()
    monthly_registrations = MonthlyRegistrationsSerializer()
    top_performing_providers = TopPerformingProviderSerializer(many=True)
    patient_satisfaction = serializers.IntegerField()
    avg_consultation_time = serializers.CharField()
    follow_up_rate = serializers.IntegerField()


class AdminDashboardSerializer(serializers.Serializer):
    total_patients = serializers.IntegerField()
    healthcare_providers = serializers.IntegerField()
    monthly_revenue = serializers.IntegerField()
    system_uptime = serializers.IntegerField()

    overview = OverviewSerializer()
    all_modules = AllModulesSerializer()
    analytics = AnalyticsSerializer()
