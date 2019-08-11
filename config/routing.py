from django.conf.urls import url
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from color.chat.consumer import MessageConsumer
from color.notification.consumer import NotificationConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/message/<str:username>/", MessageConsumer),
            path("ws/notification/",NotificationConsumer ),
        ])
    ),
})
