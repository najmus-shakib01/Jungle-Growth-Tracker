from django.contrib import admin
from .models import Plant, PlantImage, WeatherReport

class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'jungle_type', 'date_planted')
    list_filter = ('jungle_type', 'date_planted')
    search_fields = ('name', 'user__username')

class PlantImageAdmin(admin.ModelAdmin):
    list_display = ('plant', 'date_uploaded', 'health_score', 'growth_percentage')
    list_filter = ('date_uploaded', 'health_score')
    search_fields = ('plant__name', 'analysis')

class WeatherReportAdmin(admin.ModelAdmin):
    list_display = ('weather_type', 'temperature', 'humidity', 'created_at')
    list_filter = ('weather_type', 'created_at')

admin.site.register(Plant,PlantAdmin)
admin.site.register(PlantImage,PlantImageAdmin)
admin.site.register(WeatherReport,WeatherReportAdmin)