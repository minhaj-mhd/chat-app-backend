from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from accounts.tokenauthentication import JWTauthentication
from django.db import close_old_connections
import logging

logger = logging.getLogger(__name__)

class JWTWebsocketMiddleware(BaseMiddleware):
    async def resolve_scope(self, scope):
        """
        Resolves and modifies the scope for WebSocket connections by adding the authenticated user.
        """
        close_old_connections()

        # Parse the query string to extract the token
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(qp.split("=") for qp in query_string.split("&") if "=" in qp)
        token = query_parameters.get("token", None)

        if not token:
            logger.error("Token missing in WebSocket connection")
            raise AuthenticationFailed("No token provided")

        authentication = JWTauthentication()

        try:
            # Authenticate the user using the JWT token
            user = await authentication.authenticate_websocket(scope, token)
            if user:
                logger.info(f"User {user} authenticated successfully")
                scope["user"] = user  # Attach user to the scope for further use
            else:
                logger.error("User authentication failed")
                raise AuthenticationFailed("Invalid token")
        except AuthenticationFailed as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise
