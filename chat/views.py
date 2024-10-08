from django.shortcuts import render
from . import serializers
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserList(request):
    try:
        print("request",request.user)
        print("user_data",User)
        user_obj = User.objects.exclude(id=request.user.id)
        serializer = serializers.GetUsersSerializer(user_obj,many=True)
        print(serializer.data)
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)