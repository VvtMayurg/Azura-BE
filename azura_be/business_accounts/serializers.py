from allauth.account.adapter import get_adapter
from rest_framework import serializers
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError

from azura_be.business_accounts.models import BusinessAccount
from azura_be.users.models import User


class BusinessAccountSignUpSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    validate_only = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = BusinessAccount
        fields = ("name", "discipline_service", "address", "contact", "email", "website", "grace_code", "web_address", "user_email", "first_name", "last_name", "password1", "password2", "validate_only")

    def validate_user_email(self, email):
        email = get_adapter().clean_email(email.lower())
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="User with this email already exists"
            )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.pop('user_email', ''),
            'first_name': self.validated_data.pop('first_name', ''),
            'last_name': self.validated_data.pop('last_name', ''),
            'password1': self.validated_data.pop('password1', ''),
        }
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password1") != attrs.get("password2"):
            raise serializers.ValidationError(detail={"password1": "Password and Confirm Password should be same", "password2": "Password and Confirm Password should be same"})
        return attrs

    def save_user(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

    def create(self, validated_data):
        user = self.save_user(self.context.get("request"))
        validated_data.update({"created_by": user})
        return super().create(validated_data)
