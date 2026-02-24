"""ASGI config for djust-admin tests.

This is needed for running tests with Daphne which supports WebSockets.
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

# Initialize Django ASGI application early to populate the app registry
django_asgi_app = get_asgi_application()

# Import after django setup (must be after get_asgi_application)
from djust.websocket import LiveViewConsumer  # noqa: E402

# WebSocket URL patterns - the djust client connects to /ws/live/
websocket_urlpatterns = [
    path("ws/live/", LiveViewConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": SessionMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
