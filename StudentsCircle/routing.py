from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import student.routing

# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(student.routing.websocket_urlpatterns)
#         )
#     ),
# })

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            student.routing.websocket_urlpatterns
        )
    ),
})
