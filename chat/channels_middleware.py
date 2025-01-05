from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from accounts.tokenauthentication import JWTauthentication
from django.db import close_old_connections


class JWTWebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        # Parse the query string to get the token
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(qp.split("=") for qp in query_string.split("&") if "=" in qp)
        token = query_parameters.get("token", None)

        if token is None:
            # No token provided, close the WebSocket connection
            await send({
                "type": "websocket.close",  # Fixed typo
                "code": 4000
            })
            return  # Stop further execution

        authentication = JWTauthentication()  # Assuming you have this class

        try:
            # Authenticate the user using JWT token
            user = await authentication.authenticate_websocket(scope, token)
            if user is not None:
                scope['user'] = user  # Attach user to the scope for further use
            else:
                # Authentication failed, close the WebSocket connection
                await send({
                    "type": "websocket.close",
                    "code": 4000
                })
                return  # Stop further execution

            # Call the next middleware/consumer
            return await super().__call__(scope, receive, send)

        except AuthenticationFailed:
            # JWT token invalid, close the WebSocket connection
            await send({
                "type": "websocket.close",
                "code": 4000
            })
