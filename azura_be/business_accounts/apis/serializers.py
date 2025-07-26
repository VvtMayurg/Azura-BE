from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from djstripe.models import Price
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from azura_be.base.constants import ReminderTypeChoices
from azura_be.business_accounts.models import AccountConfiguration
from azura_be.business_accounts.models import BusinessAccount
from azura_be.business_accounts.models import CommunicationTemplate
from azura_be.business_accounts.models import CommunicationTemplateVersion
from azura_be.business_accounts.models import EmailConfiguration
from azura_be.business_accounts.models import SMSConfiguration
from azura_be.business_accounts.models import VitalAlertConfiguration
from azura_be.users.apis.serializers import UserRelatedSerializer
from azura_be.users.models import User


class CardIntentSerializer(serializers.Serializer):
    client_secret = serializers.CharField()


class PlanSubscriptionSerializer(serializers.Serializer):
    price = serializers.PrimaryKeyRelatedField(queryset=Price.objects.all())
    card_id = serializers.CharField()


class BusinessAccountSignUpSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    validate_only = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = BusinessAccount
        fields = (
            "name",
            "discipline_service",
            "address",
            "contact",
            "email",
            "website",
            "grace_code",
            "web_address",
            "user_email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "validate_only",
        )

    def validate_user_email(self, email):
        email = get_adapter().clean_email(email.lower())
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="User with this email already exists",
            )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.pop("user_email", ""),
            "first_name": self.validated_data.pop("first_name", ""),
            "last_name": self.validated_data.pop("last_name", ""),
            "password1": self.validated_data.pop("password1", ""),
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password1") != attrs.get("password2"):
            raise serializers.ValidationError(
                detail={
                    "password1": "Password and Confirm Password should be same",
                    "password2": "Password and Confirm Password should be same",
                },
            )
        return attrs

    def save_user(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc),
                )
        user.save()
        setup_user_email(request, user, [])
        return user

    def create(self, validated_data):
        self.user = self.save_user(self.context.get("request"))
        validated_data.update({"created_by": self.user.id})
        validated_data.pop("user_email", "")
        validated_data.pop("first_name", "")
        validated_data.pop("last_name", "")
        validated_data.pop("password1", "")
        validated_data.pop("password2", "")
        validated_data.pop("validate_only", False)
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class SignUpResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    account_id = serializers.UUIDField()


class EmailConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfiguration
        fields = (
            "host",
            "port",
            "username",
            "password",
            "from_email",
            "protocol",
            "authentication",
        )
        extra_kwargs = {"password": {"write_only": True}}


class SMSConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSConfiguration
        fields = ("provider", "from_number", "cred_json")
        extra_kwargs = {"cred_json": {"write_only": True}}


class CommunicationTemplateSerializer(serializers.ModelSerializer):
    created_by = UserRelatedSerializer(required=False)
    updated_by = UserRelatedSerializer(required=False)

    class Meta:
        model = CommunicationTemplate
        fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "name",
            "type",
            "user_type",
            "subject",
            "content",
            "active",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

    def update(self, instance, validated_data):
        old_content = instance.content
        old_subject = instance.subject
        instance = super().update(instance, validated_data)
        new_content = instance.content
        new_subject = instance.subject

        if old_content != new_content or old_subject != new_subject:
            CommunicationTemplateVersion.objects.create(
                template=instance,
                old_content=old_content,
                old_subject=old_subject,
                new_content=new_content,
                new_subject=new_subject,
            )


class VitalAlertConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalAlertConfiguration
        fields = (
            "vital_type",
            "min_range",
            "min_value",
            "min_normal_value",
            "max_normal_value",
            "max_value",
            "max_range",
        )


class ReminderConfigurationSerializer(serializers.Serializer):
    reminder_type = serializers.ChoiceField(choices=ReminderTypeChoices)
    duration = serializers.IntegerField()


class AccountConfigurationSerializer(serializers.ModelSerializer):
    reminders = ReminderConfigurationSerializer(many=True, required=False)
    default_timezone = TimeZoneSerializerField(required=False)

    class Meta:
        model = AccountConfiguration
        fields = (
            "reminders",
            "email",
            "sms",
            "push",
            "urgent_alert",
            "default_timezone",
            "session_timeout",
            "date_format",
            "audit_log_retention",
        )
