from django.shortcuts import render, redirect

from django.contrib import messages
import requests
from datetime import datetime 
import os 

from WeatherA.models import cities

city = cities.objects.all()

# Create your views here.
def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=29e865c8087004bf8971f80c0f4615a1'
    weather_data = []
    cities_list = cities.objects.all()

    if request.method == "POST":
        city_name = request.POST.get('city')
        if city_name:
            add_city = cities.objects.create(city=city_name)
            add_city.save()
            print(city_name)
            return redirect("/")
        else:
            print(city_name)
            city_name = "Jaipur"
    print(cities_list)
    city  = cities_list.last()
    get_weather = requests.get(url.format(city)).json()
    
    if get_weather.get('cod') == 200:  # Check if the response is successful
        temp_f = get_weather['main']['temp']
        temp = "{:.2f}".format((temp_f - 32) * 5/9) 
        weather = {
            'city': city,
            'description': get_weather['weather'][0]['description'],
            'icon': get_weather['weather'][0]['icon'],
            'temp': temp,
            'day': datetime.now().date(),  # Add the current date
        }
       
        weather_data.append(weather)
   
    else:
        # Handle the case when the city is not found
        weather_data.append({
            'city': city,
            'description': 'City not found',
            'icon': 'NA',
            'temp': 0,
            'day': datetime.now().date(),  # Add the current date
        })

    context = {
        'weather_data': weather_data,
        'temp': weather_data[0]['temp'] if weather_data else None,
        'city': weather_data[0]['city'] if weather_data else None,
        'icon': weather_data[0]['icon'] if weather_data else None,
        'description': weather_data[0]['description'] if weather_data else None,
        'day': weather_data[0]['day'] if weather_data else None,
    }

    return render(request, 'WeaterA/index.html', context)