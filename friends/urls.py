
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('users/', views.getUser,name="users"),
    path('list/', views.getFriends,name="list"),
    path('add/',views.addFriend,name="add"),
    path('friendrequests/',views.getFriendshipRequests,name="friendrequests"),
    path('acceptrequest/',views.confirm_friend_request,name='acceptrequest'),
   
]