import random
from .serializers import UserSerializer,LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.tokenauthentication import JWTauthentication
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import User
from django.core.cache import cache
from backend_ca import settings
from django.core.mail import send_mail

# Create your views here.
@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    sendOtp(request.data["email"])
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status = 400)
    
@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
   
    if serializer.is_valid():
        user = User.objects.get(id=serializer.data["id"])
        token = JWTauthentication.generate_token(payload=serializer.data)
        return Response({
            "message": "Login Successful",
            "token":token,
            "user":serializer.data,
            "name":user.get_full_name()
            
        })
    return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def check_health(request):
    return JsonResponse({"status":"ok"})


def sendOtp(email):
    otp = str(random.randint(100000, 999999))
    Subject = "Verify Your Chat-App Account"
    message = f'Your One-Time Password is :{otp}' 
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list =[email]
    print(recipient_list)
    try:
        send_mail(Subject,message,from_email,recipient_list)
        store_otp(email,otp)
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")

def store_otp(email,otp):
    cache.set(f"otp:{email}", otp, timeout=300)

def verify_otp(email,check_otp):
    otp=cache.get(f"otp:{email}")
    if otp ==   check_otp:
        return Response(status=201)



