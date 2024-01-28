"""
ASGI config for channelsConsumer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channelsConsumer.settings')
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

import app.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    
    'websocket': AuthMiddlewareStack (URLRouter(
        app.routing.websocket_urlpatterns
    ))
    
})
