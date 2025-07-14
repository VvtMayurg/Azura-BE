from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from azura_be.base.context import current_context

BUSINESS_ACCOUNT_USER_DOES_NOT_EXISTS_MESSAGE = "User is not belongs to this business account"


class DefaultJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        response = super().authenticate(request)
        if response is None:
            return None
        user = response[0]
        if request.business_account and request.business_account not in user.business_accounts.all():
            raise AuthenticationFailed(BUSINESS_ACCOUNT_USER_DOES_NOT_EXISTS_MESSAGE, code="user_not_exists")
        current_context.user = user
        return response


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    target_class = DefaultJWTAuthentication
