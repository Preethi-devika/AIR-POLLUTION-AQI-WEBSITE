import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

# Simple test view (for /weather/)
def weather(request):
    return HttpResponse("wheather area")

# Main AQI view (for home page)
def home(request):
    API_KEY = os.getenv(
        'WEATHER_API_KEY',
        'a27c74e011f0537bce95fc618e1fdd3b'
    )

    context = {}

    if request.method == 'POST':
        city = request.POST.get('city')

        if city:
            geo_url = (
                f"http://api.openweathermap.org/geo/1.0/direct"
                f"?q={city}&limit=1&appid={API_KEY}"
            )
            geo_data = requests.get(geo_url).json()

            if geo_data:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']

                aqi_url = (
                    f"http://api.openweathermap.org/data/2.5/air_pollution"
                    f"?lat={lat}&lon={lon}&appid={API_KEY}"
                )
                aqi_data = requests.get(aqi_url).json()

                aqi = aqi_data['list'][0]['main']['aqi']
                components = aqi_data['list'][0]['components']

                levels = {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor",
                }

                context = {
                    "city": city,
                    "aqi": aqi,
                    "level": levels.get(aqi, "Unknown"),
                    "pm2_5": components.get('pm2_5'),
                    "pm10": components.get('pm10'),
                    "no2": components.get('no2'),
                    "so2": components.get('so2'),
                    "co": components.get('co'),
                    "o3": components.get('o3'),
                }
            else:
                context = {"error": "City not found"}
        else:
            context = {"error": "Please enter a city name"}

    return render(request, "aqi/home.html", context)