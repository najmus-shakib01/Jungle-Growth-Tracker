import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlantGrowthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "plant_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "plant_updates",
            self.channel_name
        )

    async def plant_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "plant.update",
            "data": event["message"]
        }))

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "weather_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "weather_updates",
            self.channel_name
        )

    async def weather_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "weather.update",
            "data": event["weather_data"] 
        }))