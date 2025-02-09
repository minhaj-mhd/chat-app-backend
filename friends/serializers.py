from .models import Friendship
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()  # Correct usage of get_user_model() to define the user model
class FriendshipSerializer(serializers.ModelSerializer):
    User = get_user_model()  # Correct usage of get_user_model() to define the user model
    user = serializers.StringRelatedField(read_only=True)  # Authenticated user is read-only
    friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Select the friend

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'status', 'created_at']  # Fields to be serialized

    def validate(self, data):
        # Get the authenticated user from the request context
        user = self.context['request'].user
        friend = data.get('friend')

        # Check if the friendship already exists (either way)
        try:
            if Friendship.objects.filter(user=user, friend=friend).exists() or \
            Friendship.objects.filter(user=friend, friend=user).exists():
                    raise serializers.ValidationError("friend request already exists")

        except:
                print("friend request already exists")

                # Ensure users cannot be friends with themselves
        if user == friend:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        
            
     # Ensure the friendship request is in 'pending' state before confirmation
        if self.instance and self.instance.status != 'pending':
            raise serializers.ValidationError("Cannot update a friend request that is not pending.")
        


        return data

    def create(self, validated_data):
        # Get the authenticated user from the request context
        user = self.context['request'].user
        friend = validated_data['friend']

        # Create the friendship request with a status of 'pending'
        return Friendship.objects.create(user=user, friend=friend, status='pending')


class AcceptFriendSerializer(serializers.ModelSerializer):
    User = get_user_model()  # Correct usage of get_user_model() to define the user model
    user = serializers.StringRelatedField(read_only=True)  # Authenticated user is read-only
    friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Select the friend

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'status', 'created_at']  # Fields to be serialized

    def validate(self, data):
        # Get the authenticated user from the request context
        user = self.context['request'].user
        friend = data.get('friend')
         # Ensure the friendship request is in 'pending' state before confirmation
        if self.instance and self.instance.status != 'pending':
            raise serializers.ValidationError("Cannot update a friend request that is not pending.")
        


        return data
    def update(self, instance, validated_data):
        # Update the friendship status (e.g., accepting or declining the request)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

      
        
class GetUsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields=['email','first_name','last_name','id']
        extra_kwargs = {'id':{'read_only':True}}

class GetUsersWithStatusSerializer(serializers.Serializer):

    email=serializers.CharField()
    first_name=serializers.CharField()
    last_name = serializers.CharField()
    id = serializers.CharField()
    friendship_status= serializers.CharField()
    def to_representation(self, instance):
        email=instance.email
        first_name=instance.first_name
        last_name = instance.last_name
        id = instance.id
        print("friend:",id)

        user = self.context['request'].user
        print("friend:",user)

        try:
            friend = User.objects.get(id=id)
            # Check if a friendship exists in either direction
            friendship = (
                Friendship.objects.filter(user=user, friend=friend).first() or
                Friendship.objects.filter(user=friend, friend=user).first()
            )

            # If friendship exists, retrieve the status
            if friendship:
                friendship_status = friendship.status
            else:
                friendship_status="None"

        except User.DoesNotExist:
            pass  # Target user does not exist, keep status as "None"

        return{
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "id":id,
            "friendship_status":friendship_status
        }
