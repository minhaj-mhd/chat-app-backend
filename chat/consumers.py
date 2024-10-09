import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from channels.db import DatabaseSyncToAsync
class PersonalClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope["user"]
        if request_user.is_authenticated:
            chat_with_user = self.scope["url_route"]['kwargs']['id']
            user_ids = [int(request_user.id),int(chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send_cached_messages()


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print("data",data)
        message = data["message"]
        receiver = data["receiver"]
        self.store_message_in_cache(message,receiver)

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':"chat_message",
                "message":message,
                "receiver":receiver
            }
        )
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ) 
    async def chat_message(self,event):
        print("event",event)
        message = event["message"]
        receiver = event["receiver"]
        print("message",message)
        print("receiver",receiver)
        await self.send(text_data=json.dumps({"message":message,"receiver":receiver}))
    @DatabaseSyncToAsync
    def store_message_in_cache(self, message,receiver):
        # Here we use a simple list to store messages, you can customize the storage
        message_entry={"message":message,"receiver":receiver}
        
        chat_history = cache.get(self.room_group_name, [])
        print("chat_history",chat_history)
        print(message,receiver)
        chat_history.append(message_entry)

        # Store it back to the cache
        cache.set(self.room_group_name, chat_history, timeout=3600)  # Expires after 1 hour
    async def send_cached_messages(self):
        print("sending cached messages")
        cached_messages = cache.get(self.room_group_name, [])
        print("sending cached messages",cached_messages)
        for msg in cached_messages:
            await self.send(text_data=json.dumps({"message": msg["message"],"receiver":msg["receiver"]}))