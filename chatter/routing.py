import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatter.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

application = ProtocolTypeRouter({
    # ✅ ADD THIS LINE (VERY IMPORTANT)
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})