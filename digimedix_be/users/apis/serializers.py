from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from digimedix_be.users.models import User


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
