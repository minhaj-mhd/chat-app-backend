from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status = 400)