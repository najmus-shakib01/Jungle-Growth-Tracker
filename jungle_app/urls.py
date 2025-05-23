from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-plant/', views.add_plant, name='add_plant'),
    path('plant/<int:plant_id>/', views.plant_detail, name='plant_detail'),
    path('plant/<int:plant_id>/upload-image/', views.upload_plant_image, name='upload_plant_image'),
    path('generate-weather/', views.generate_weather, name='generate_weather'),
]