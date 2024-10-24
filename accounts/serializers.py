from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from .tokenauthentication import JWTauthentication
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self,validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password = validated_data["password"],
            first_name=validated_data.get("first_name",""),
            last_name=validated_data.get("last_name","")
        )
        return user
    class Meta:
        model=get_user_model()
        fields=["email","password","first_name","last_name"]
        extra_kwargs={"password":{"write_only:True"}}

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    id = serializers.CharField(max_length=15,read_only=True)
    password=serializers.CharField(max_length=255,write_only=True)
    def validate(self,data):
        email = data.get("email",None)
        password = data.get("password",None)
        if email == None:
            raise serializers.ValidationError("An Email is required for Login")
        if password == None:
            raise serializers.ValidationError("A password id required for Login")
        user = authenticate(username=email,password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        fullName=user.get_full_name()
        return {
            "email":user.email,
            "name":fullName,
            "id":user.id
        }
    class Meta:
        model=get_user_model()
        fields=["email","password","id"]
        extra_kwargs={"password":{"write_only:True"}}