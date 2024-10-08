import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PersonalClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("self.scope",self.scope)
        request_user = self.scope["user"]
        if request_user.is_authenticated:
            print(request_user)
            chat_with_user = self.scope["url_route"]['kwargs']['id']
            user_ids = [int(request_user.id),int(chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print("channel",self.channel_layer)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':"chat_message",
                "message":message
            }
        )
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ) 
    async def chat_message(self,event):
        message = event["message"]
        print("message",message)
        await self.send(text_data=json.dumps({"message":message}))