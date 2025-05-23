from django.db import models
from django.contrib.auth.models import User

class Plant(models.Model):
    JUNGLE_TYPES = [
        ('RAIN', 'Rainforest'),
        ('DES', 'Desert'),
        ('TROP', 'Tropical'),
        ('TEM', 'Temperate'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    jungle_type = models.CharField(max_length=4, choices=JUNGLE_TYPES)
    date_planted = models.DateField(auto_now_add=True)
    last_watered = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_jungle_type_display()})"

class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='plant_images/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    health_score = models.FloatField(null=True, blank=True)
    growth_percentage = models.FloatField(null=True, blank=True)
    analysis = models.TextField(blank=True)
    
    def __str__(self):
        return f"Image for {self.plant.name} on {self.date_uploaded}"

class WeatherReport(models.Model):
    WEATHER_TYPES = [
        ('SUN', 'Sunny'),
        ('RAIN', 'Rainy'),
        ('CLOUD', 'Cloudy'),
        ('STORM', 'Stormy'),
    ]
    
    weather_type = models.CharField(max_length=5, choices=WEATHER_TYPES)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    forecast = models.TextField()
    animal_activity = models.TextField()
    
    def __str__(self):
        return f"{self.get_weather_type_display()} weather on {self.created_at}"