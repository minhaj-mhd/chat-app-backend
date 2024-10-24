from django.shortcuts import get_object_or_404, redirect
from .models import Friendship
from django.shortcuts import render
from . import serializers
from rest_framework import status

from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
# Create your views here.

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addFriend(request):
    print(request.data)
    print(request.user)
    friends=Friendship.objects.filter(friend=request.data.get("friend"),user=request.user)
    if friends:
        return Response(status.HTTP_208_ALREADY_REPORTED)
    
    try:
        serializer = serializers.FriendshipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Save the friend request
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUser(request):
    try:
        query = request.GET.get("q")
        print(query)
        searched_users = User.objects.filter(email__icontains=query).exclude(id=request.user.id)
        print(searched_users)
        serializer = serializers.GetUsersSerializer(searched_users,many=True)
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_friend_request(request):
    try:
        print(request)

        friend_id = request.data.get("friend")
        print(friend_id)
        friend = User.objects.get(id=friend_id)
        print(friend)
        friendship = Friendship.objects.get(user=friend,friend=request.user)
        print(friendship)
    except Friendship.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.AcceptFriendSerializer(friendship, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFriendshipRequests(request):
    try:
        recieved = request.user.recieved.filter(status="pending")
        recieved_friends = [Friendship.user for Friendship in recieved  ]
        print(recieved_friends)
        serializer = serializers.GetUsersSerializer(recieved_friends,many=True)
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFriends(request):
    try:
        recieved = request.user.recieved.filter(status="accepted")
        added = request.user.added.filter(status="accepted")
        added_data = [Friendship.user for Friendship in added  ]
        recieved_data = [Friendship.user for Friendship in recieved  ]
        friends_data = added_data+recieved_data
        print(friends_data)
        serializer = serializers.GetUsersSerializer(friends_data,many=True)
        print(serializer.data)
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)
