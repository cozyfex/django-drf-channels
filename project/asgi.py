"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import logging
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from redis import Redis, RedisError

import ws.chat.routing
from project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

logger = logging.getLogger(__name__)


async def health_check(scope, receive, send):
    if scope['type'] == 'http' and scope['path'] == '/check/':
        headers = [(b'content-type', b'application/json')]
        body = b'{"status": "ok"}'
        await send({'type': 'http.response.start', 'status': 200, 'headers': headers})
        await send({'type': 'http.response.body', 'body': body})
    else:
        await django_asgi_app(scope, receive, send)


def check_redis_connection():
    try:
        redis_client = Redis(
            host=settings.CHANNELS_REDIS_SERVER,
            port=settings.CHANNELS_REDIS_PORT,
            password=settings.CHANNELS_REDIS_PASSWORD,
            db=settings.CHANNELS_REDIS_DB,
        )
        redis_client.ping()
        logger.info('Redis server is available!')
    except RedisError as e:
        logger.error('Redis server is not available: ' + str(e))


check_redis_connection()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': URLRouter(
            [
                re_path(r'^check/$', health_check),  # Add health check route
                re_path(r'', django_asgi_app),
            ]
        ),
        'websocket': AuthMiddlewareStack(
            URLRouter(ws.chat.routing.websocket_urlpatterns)
        ),
    }
)
