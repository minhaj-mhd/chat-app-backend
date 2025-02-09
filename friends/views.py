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
    friend = User.objects.get(id=request.data.get("friend"))
    if Friendship.objects.filter(user=request.user, friend=friend).exists() or \
            Friendship.objects.filter(user=friend, friend=request.user).exists():
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
        searched_users = User.objects.filter(email__icontains=query).exclude(id=request.user.id)
        serializer = serializers.GetUsersWithStatusSerializer(searched_users,many=True, context={'request': request})
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_friend_request(request):
    try:

        friend_id = request.data.get("friend")
        friend = User.objects.get(id=friend_id)
        friendship = Friendship.objects.get(user=friend,friend=request.user)
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
        serializer = serializers.GetUsersSerializer(recieved_friends,many=True)
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFriends(request):
    try:
        recieved = request.user.recieved.filter(status="accepted").exclude(user=request.user)
        added = request.user.added.filter(status="accepted").exclude(user=request.user)
        added_data = [Friendship.user for Friendship in added  ]
        recieved_data = [Friendship.user for Friendship in recieved  ]
        friends_data = added_data+recieved_data
        print(friends_data)
        serializer = serializers.GetUsersWithStatusSerializer(friends_data,many=True,context={'request': request})
        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFriendshipRequestsWithStatus(request):
    try:
        recieved = request.user.recieved.filter(status="pending")
        recieved_friends = [Friendship.user for Friendship in recieved  ]
        serializer = serializers.GetUsersSerializer(recieved_friends,many=True)

        return Response(tuple(serializer.data),status=200)
    except Exception as e:
        print ("error")
        return Response("Error getting user list.",status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request):
    try:

        friend_id = request.data.get("friend")
        friend = User.objects.get(id=friend_id)
        friendship = Friendship.objects.get(user=request.user,friend=friend)

        if friendship:
            friendship.delete()
            return Response(status=status.HTTP_202_ACCEPTED)

    except Friendship.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
    
