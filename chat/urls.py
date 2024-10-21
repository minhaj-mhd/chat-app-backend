
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('users/', views.getUserList,name="users"),
    path('verify/', views.verifyUser,name="verify"),

   
]
