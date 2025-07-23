from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


@database_sync_to_async
def get_user(token):
    validated_token = {}
    for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
        validated_token = AuthToken(token)
    if not validated_token:
        return None
    return User.objects.filter(uid=validated_token["user_uid"]).first()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode("utf8"))
        token = query_params.get("token")[0]

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        if not token:
            return None

        scope["user"] = await get_user(token)
        return await super().__call__(scope, receive, send)


def middleware_stack(inner):
    return JwtAuthMiddleware(inner)
