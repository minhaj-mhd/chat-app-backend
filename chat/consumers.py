import json
import logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from channels.db import database_sync_to_async
from .models import Message, OnlineStatusTrack
from accounts.models import User
from django.db.models import Q

logger = logging.getLogger(__name__)

#chat_user_obj is User model obj
#chat_with_user is the userid of the 2nd user

class PersonalClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connencting")
        self.request_user = self.scope["user"]
        print("user",self.request_user)
        if self.request_user.is_authenticated:
            self.chat_with_user = self.scope["url_route"]['kwargs']['id']
            user_ids = sorted([self.request_user.id, self.chat_with_user])
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send_cached_messages()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        reciever = data["reciever"]
        await self.save_message(message, reciever, self.request_user.id)

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': "chat_message",
                "message": message,
                "reciever": reciever
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.checkout()

    @database_sync_to_async
    def checkout(self):
        self.chat_user_obj = User.objects.get(id=self.chat_with_user)

        obj = OnlineStatusTrack.objects.filter(
            Q(userOne=self.request_user, userTwo=self.chat_user_obj) | 
            Q(userOne=self.chat_user_obj, userTwo=self.request_user)
        ).first()
        if not obj:
            OnlineStatusTrack.objects.create(
                userOne=self.request_user,
                userTwo=self.chat_user_obj
            )

    async def chat_message(self, event):
        message = event["message"]
        reciever = event["reciever"]
        await self.send(text_data=json.dumps({"message": message, "reciever": reciever}))

    @database_sync_to_async
    def save_message(self, message, reciever, sender):
        timestamp = datetime.now()  # Creating the timestamp here
        message_entry = {
            "message": message,
            "reciever": reciever,
            "sender": sender,
            "timestamp": timestamp
        }
        # Save message to DB
        Message.objects.create(
            sender=sender,
            reciever=reciever,
            content=message,
            timestamp=datetime.now()
        )
        chat_history = cache.get(self.room_group_name, [])
        chat_history.insert(0, message_entry)
        cache.set(self.room_group_name, chat_history[-100:], timeout=3600)  # Cache expires after 1 hour

    async def send_cached_messages(self):
        cached_messages = cache.get(self.room_group_name)
        print("cached",cached_messages)
        if not cached_messages:
            cached_messages = await self.get_last_messages_from_db()
            cache.set(self.room_group_name, cached_messages, timeout=3600)
        for msg in reversed(cached_messages):
            await self.send(text_data=json.dumps({
                "message": msg["message"],
                "reciever": msg["reciever"]
            }))

    @database_sync_to_async
    def get_last_messages_from_db(self):
        self.chat_user_obj = User.objects.get(id=self.chat_with_user)
        messages = Message.objects.filter(
            sender__in=[self.request_user.id, self.chat_user_obj.id],
            reciever__in=[self.request_user.id, self.chat_user_obj.id]
        ).order_by("-timestamp")[:100]
        return [{
            "sender": message.sender,
            "reciever": message.reciever,
            "message": message.content,
            "timestamp": message.timestamp
        } for message in messages]
