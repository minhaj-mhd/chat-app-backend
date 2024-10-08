import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone
from channels.db import database_sync_to_async

class JWTauthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None
        
        try:
            User = get_user_model()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # Use a list for algorithms
            self.verify_token(payload=payload)

            user_id = payload["id"]
            user = User.objects.get(id=user_id)
            return (user, token)
        
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid Token")

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("Invalid Token with no expiration")
        
        exp_timestamp = payload["exp"]
        current_timestamp = datetime.now(timezone.utc).timestamp()

        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token Expired")

    def extract_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    @database_sync_to_async
    def authenticate_websocket(self, scope, token):
        try:
            User = get_user_model()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # Consistency in both methods
            self.verify_token(payload=payload)

            user_id = payload['id']
            user = User.objects.get(id=user_id)
            return user
        
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            return None  # Return None if the token is invalid or user does not exist

    @staticmethod
    def generate_token(payload):
        expiration = datetime.now(timezone.utc) + timedelta(hours=24)
        payload["exp"] = expiration
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token
