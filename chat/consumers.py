import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from channels.db import database_sync_to_async
from .models import Message,OnlineStatusTrack
from accounts.models import User
from datetime import datetime
from django.db.models import Q
class PersonalClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.request_user = self.scope["user"]
        if self.request_user.is_authenticated:
            self.chat_with_user = int(self.scope["url_route"]['kwargs']['id'])
            print("chat with user",self.chat_with_user)
            # try:
            self.chat_user = User.objects.get(id=self.chat_with_user)
            print(self.chat_user)
            # except:
            #     print("error")
            user_ids = [int(self.request_user.id),int(self.chat_with_user)]
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
        message = data["message"]
        reciever = data["reciever"]
        await self.save_message(message,reciever,self.request_user.id)

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':"chat_message",
                "message":message,
                "reciever":reciever
            }
        )
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.checkout()

    @database_sync_to_async   
    def checkout(self):
        obj = OnlineStatusTrack.objects.filter(
            Q(userOne=self.request_user, userTwo = self.chat_User) | Q(userOne=self.chat_user,userTwo =self.request_user)).first()
        print(obj)
        if not obj:
            obj = OnlineStatusTrack(
                userOne=self.request_user,
                userTwo=self.chat_user)
            obj.save()
        
        
    async def chat_message(self,event):
        message = event["message"]
        reciever = event["reciever"]
        await self.send(text_data=json.dumps({"message":message,"reciever":reciever}))

    @database_sync_to_async
    def save_message(self, message,reciever,sender):
        timestamp = datetime.utcnow().isoformat()  # Creating the timestamp here

        message_entry={"message":message,"reciever":reciever,"sender":sender,"timestamp": timestamp}  
        #save message to db
        message = Message.objects.create(sender=sender,reciever=reciever,content=message,timestamp=datetime.now)

        chat_history = cache.get(self.room_group_name, [])

        chat_history.append(message_entry)
        # Store it back to the cache
        cache.set(self.room_group_name, chat_history[-100:], timeout=3600)  # Expires after 1 hour
    
    async def send_cached_messages(self):
        cached_messages = cache.get(self.room_group_name)
        if not cached_messages:
            cached_messages = await self.get_last_messages_from_db()
            cache.set(self.room_group_name,cached_messages,timeout=3600)
        for msg in cached_messages:
            await self.send(text_data=json.dumps({"message": msg["message"],"reciever":msg["reciever"]}))

    @database_sync_to_async
    def get_last_messages_from_db(self):
        messages = Message.objects.filter(
            sender__in=[self.request_user.id,int(self.chat_with_user)],
            reciever__in = [self.request_user.id,int(self.chat_with_user)]
        ).order_by("-timestamp")[:100]
        return [{"sender":message.sender,
                 "reciever":message.reciever,
                 "message":message.content,
                 "timestamp":message.timestamp} for message in messages]
