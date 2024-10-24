
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register_user,name="register"),
    path('login',views.login_user,name="login"),
    # path("getuser",views.getUser,name="getuser")
]
