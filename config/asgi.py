"""
ASGI config for Azura Backend Application project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""

import django

django.setup()

from azura_be.communications.consumers import NotificationConsumer, ThreadChatConsumer
from azura_be.communications.middleware import middleware_stack

import os
import sys
from pathlib import Path

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

# This allows easy placement of apps within the interior
# azura_be directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "azura_be"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# Import websocket application here, so apps from django_application are loaded first
# from config.websocket import websocket_application


# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         msg = f"Unknown scope type {scope['type']}"
#         raise NotImplementedError(msg)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": middleware_stack(
            URLRouter(
                [
                    path("notification/", NotificationConsumer.as_asgi()),
                    path("threads/<str:thread_id>/", ThreadChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
