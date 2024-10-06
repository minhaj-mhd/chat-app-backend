from channels.generic.websocket import AsyncWebsocketConsumer

class PersonalClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("testing connection")
        await self.accept()