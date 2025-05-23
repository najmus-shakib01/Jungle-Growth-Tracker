from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plant, PlantImage, WeatherReport
from .forms import PlantForm, PlantImageForm
import cv2
import numpy as np
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def dashboard(request):
    plants = Plant.objects.filter(user=request.user)
    latest_weather = WeatherReport.objects.last()
    return render(request, 'jungle_app/dashboard.html', {
        'plants': plants,
        'weather': latest_weather
    })

@login_required
def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'plant_updates',
                {
                    'type': 'plant_update',
                    'message': {  
                        'event': 'new_plant',
                        'plant_name': plant.name,
                        'jungle_type': plant.get_jungle_type_display(),
                        'message': f'New plant added: {plant.name}',
                        'time': datetime.now().strftime("%H:%M:%S")
                    }
                }
            )
            return redirect('dashboard')
    else:
        form = PlantForm()
    return render(request, 'jungle_app/add_plant.html', {'form': form})

@login_required
def upload_plant_image(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id, user=request.user)
    
    if request.method == 'POST':
        form = PlantImageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if not request.FILES['image'].content_type.startswith('image/'):
                    raise ValueError("Uploaded file is not an image")

                plant_image = form.save(commit=False)
                plant_image.plant = plant

                img_bytes = np.fromstring(request.FILES['image'].read(), np.uint8)
                img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
                
                if img is None:
                    raise ValueError("Could not decode the image file")

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_green = np.array([35, 50, 50])
                upper_green = np.array([85, 255, 255])
                mask = cv2.inRange(hsv, lower_green, upper_green)
                green_pixels = cv2.countNonZero(mask)
                total_pixels = img.shape[0] * img.shape[1]
                
                if total_pixels == 0:
                    raise ValueError("Image has no pixels")

                health_score = (green_pixels / total_pixels) * 100
                plant_image.health_score = round(health_score, 2)

                previous_images = PlantImage.objects.filter(plant=plant).order_by('-date_uploaded')
                if previous_images.exists():
                    prev_img = previous_images.first()
                    growth = health_score - prev_img.health_score
                    plant_image.growth_percentage = round(growth, 2)
                    
                    if growth > 0:
                        plant_image.analysis = f"Health improved by {growth:.2f}% since last check."
                    elif growth < 0:
                        plant_image.analysis = f"Health decreased by {abs(growth):.2f}% since last check."
                    else:
                        plant_image.analysis = "Health remains the same since last check."
                else:
                    plant_image.growth_percentage = 0
                    plant_image.analysis = "First health check. Base score established."
                
                plant_image.save()

                try:
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        'plant_updates',
                        {
                            'type': 'plant_update',
                            'message': {
                                'event': 'new_image',
                                'plant_name': plant.name,
                                'health_score': health_score,
                                'growth': plant_image.growth_percentage,
                                'message': f'New image for {plant.name}',
                                'time': datetime.now().strftime("%H:%M:%S")
                            }
                        }
                    )
                except Exception as e:
                    print(f"WebSocket error: {str(e)}")

                return redirect('plant_detail', plant_id=plant.id)

            except Exception as e:
                form.add_error('image', str(e))
    else:
        form = PlantImageForm()
    
    return render(request, 'jungle_app/upload_image.html', {
        'form': form,
        'plant': plant
    })


@login_required
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id, user=request.user)
    images = plant.images.all().order_by('-date_uploaded')
    return render(request, 'jungle_app/plant_detail.html', {
        'plant': plant,
        'images': images
    })

@csrf_exempt
def generate_weather(request):
    if request.method == 'POST':
        
        import random
        weather_types = ['SUN', 'RAIN', 'CLOUD', 'STORM']
        weather_type = random.choice(weather_types)
        
        if weather_type == 'SUN':
            temp = random.randint(25, 35)
            humidity = random.randint(40, 60)
            forecast = "Bright sunshine today! Perfect for photosynthesis."
            activity = "Monkeys are sunbathing on the treetops. Parrots are showing off their colorful feathers."
        elif weather_type == 'RAIN':
            temp = random.randint(20, 28)
            humidity = random.randint(70, 95)
            forecast = "Heavy rainfall expected. The jungle is getting a good drink today!"
            activity = "Frogs are having a concert. Tigers are taking shelter under large leaves."
        elif weather_type == 'CLOUD':
            temp = random.randint(22, 30)
            humidity = random.randint(60, 80)
            forecast = "Partly cloudy with a chance of monkey business."
            activity = "Sloths are moving slightly faster than usual. Birds are building nests."
        else:  
            temp = random.randint(18, 25)
            humidity = random.randint(80, 100)
            forecast = "Thunderstorm warning! Trees may sway dramatically."
            activity = "All animals are taking cover. Only the bravest jungle explorers are out today."
        
        weather = WeatherReport.objects.create(
            weather_type=weather_type,
            temperature=temp,
            humidity=humidity,
            forecast=forecast,
            animal_activity=activity
        )
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'weather_updates',
            {
                'type': 'weather_update',
                'weather_data': {
                    'weather': weather.get_weather_type_display(),
                    'temp': weather.temperature,
                    'humidity': weather.humidity,
                    'forecast': weather.forecast,
                    'activity': weather.animal_activity,
                    'time': datetime.now().strftime("%H:%M")
                }
            }
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)