from .serializers import UserSerializer,LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.tokenauthentication import JWTauthentication
# Create your views here.
@api_view(["POST"])
def register_user(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status = 400)
@api_view(["POST"])

def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        token = JWTauthentication.generate_token(payload=serializer.data)
        return Response({
            "message": "Login Successful",
            "token":token,
            "user":serializer.data
        })
    return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
