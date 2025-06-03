"""
app/api/v1/endpoints/weather.py

API endpoint for retrieving weather forecast from OpenWeather API.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Fetches and returns hourly weather forecast for a specific city and date.
    Uses OpenWeather's geocoding and 5-day forecast APIs.
"""
import requests
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import os

router = APIRouter(
    prefix="/api",
    tags=["Weather"]
)

# Normally this key should come from environment (.env) for security
OPENWEATHER_API_KEY = "93dde574b8b9262f8f1a1590f1bdf790"

@router.get("/weather", operation_id="getWeatherForecast")
def get_weather_forecast(city: str = Query(...), date: str = Query(...)):
    """
    Get hourly weather forecast for a given city and date.

    Args:
        city (str): City name to get weather for.
        date (str): Date in format YYYY-MM-DD.

    Returns:
        dict: Forecast info including time, temperature, description and icon.

    Raises:
        HTTPException: If city not found, forecast fetch fails, or no forecast for date.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    # Step 1: Get city coordinates
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    geo_resp = requests.get(geo_url)
    if geo_resp.status_code != 200 or not geo_resp.json():
        raise HTTPException(status_code=404, detail="Miestas nerastas")

    geo_data = geo_resp.json()[0]
    lat, lon = geo_data["lat"], geo_data["lon"]

    # Step 2: Get weather forecast (3h steps up to 5 days)
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=lt"
    weather_resp = requests.get(forecast_url)
    if weather_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Nepavyko gauti prognozės")

    forecasts = weather_resp.json()["list"]

    # Step 3: Filter forecasts by given date
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    selected = [f for f in forecasts if datetime.fromtimestamp(f["dt"]).date() == target_date]

    if not selected:
        raise HTTPException(status_code=404, detail="Prognozės šiai datai nėra")

    return {
        "city": city,
        "date": date,
        "forecast": [
            {
                "time": datetime.fromtimestamp(f["dt"]).strftime("%H:%M"),
                "temp": f["main"]["temp"],
                "weather": f["weather"][0]["description"],
                "icon": f["weather"][0]["icon"],
            }
            for f in selected
        ]
    }
