from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

ORGANIZATION_USER_DOES_NOT_EXISTS_MESSAGE = "User is not belongs to this organization"


class DefaultJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        response = super().authenticate(request)
        if response is None:
            return None
        if request.organization and request.organization not in response[0].organizations.all():
            raise AuthenticationFailed(ORGANIZATION_USER_DOES_NOT_EXISTS_MESSAGE, code="user_not_exists")
        return response


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    target_class = DefaultJWTAuthentication
