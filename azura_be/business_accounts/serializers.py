from rest_framework import serializers

from azura_be.business_accounts.models import BusinessAccount
from azura_be.users.models import User


class BusinessAccountSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = BusinessAccount
        fields = "__all__"

    def validate_user_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                detail="User with this email already exists"
            )
        return value
