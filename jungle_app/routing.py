from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/plant_updates/$', consumers.PlantGrowthConsumer.as_asgi()),
    re_path(r'ws/weather_updates/$', consumers.WeatherConsumer.as_asgi()),
]