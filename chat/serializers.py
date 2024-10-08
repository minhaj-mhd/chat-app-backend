from rest_framework import serializers
from django.contrib.auth import get_user_model

class GetUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields=['email','first_name','last_name','id']
        extra_kwargs = {'id':{'read_only':True}}
 