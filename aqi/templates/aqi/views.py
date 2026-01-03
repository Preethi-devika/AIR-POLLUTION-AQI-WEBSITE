import os
import requests
from django.shortcuts import render

# Using the key you provided directly
API_KEY = "a27c74e011f0537bce95fc618e1fdd3b"

def home(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get("city")

        # 1. Convert City Name to Coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url).json()

        if geo_data:
            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

            # 2. Fetch Air Quality Index (AQI)
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            aqi_data = requests.get(aqi_url).json()

            aqi = aqi_data['list'][0]['main']['aqi']
            comp = aqi_data['list'][0]['components']
            levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

            context = {
                "city": city,
                "aqi": aqi,
                "level": levels.get(aqi, "Unknown"),
                "pm2_5": comp.get('pm2_5'),
                "no2": comp.get('no2'),
            }
        else:
            context = {"error": "City not found. Please check the spelling."}

    return render(request, "home.html", context)

def weather(request):
    return render(request, "aqi/weather.html")
