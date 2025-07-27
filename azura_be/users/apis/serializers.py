from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.constants import DayChoices
from azura_be.base.constants import NotificationCategoryChoices
from azura_be.base.serializers import Base64FileField
from azura_be.core.apis.serializers import SpecialtyRelatedSerializer
from azura_be.users.models import License
from azura_be.users.models import User
from azura_be.users.models import UserPreference
from azura_be.users.models import WorkShedule


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class UserDetailSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "picture",
            "timezone",
            "role",
            "two_factor_auth",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField(required=False)
    picture = Base64FileField(
        file_types=["jpg", "jpeg", "png", "svg"],
        max_file_size=5,
        required=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "picture",
            "timezone",
            "email_noftification",
            "sms_notification",
            "auto_form_save",
            "provider_groups",
            "departments",
            "primary_location",
            "phone",
            "role",
            "account_user",
            "two_factor_auth",
        )


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = (
            "user",
            "number",
            "state",
            "exiry_date",
            "npi",
            "dea_number",
            "specialties",
        )


class LicenseGetSerializer(serializers.ModelSerializer):
    specialties = SpecialtyRelatedSerializer(many=True, required=False)

    class Meta:
        model = License
        fields = "__all__"


class WorkScheduleSerializer(serializers.Serializer):
    day = serializers.ChoiceField(choices=DayChoices)
    start = serializers.TimeField()
    end = serializers.TimeField()

    def save(self):
        validated_data = self.validated_data
        user = self.context.get("user")

        for obj in validated_data:
            instance = WorkShedule.objects.filter(user=user, day=obj.get("day")).first()
            if instance:
                instance.start = obj.get("start")
                instance.end = obj.get("end")
                instance.save()
            else:
                instance = WorkShedule.objects.create(user=user, **obj)


class WorkScheduleGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShedule
        fields = ("id", "created_at", "updated_at", "day", "start", "end")


class NotificationSettingSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=NotificationCategoryChoices)
    email = serializers.BooleanField(default=False)
    sms = serializers.BooleanField(default=False)
    push = serializers.BooleanField(default=False)


class UserPreferenceSerializer(serializers.ModelSerializer):
    notification_settings = NotificationSettingSerializer(required=False)

    class Meta:
        model = UserPreference
        fields = ("notification_settings", "navbar_preferences")


class SendOTPSerializer(serializers.Serializer):
    key = serializers.CharField()
    device_type = serializers.CharField()
    device_id = serializers.IntegerField()


class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    key = serializers.CharField()
    device_type = serializers.CharField()
    device_id = serializers.IntegerField()
