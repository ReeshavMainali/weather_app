import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORCAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city:str) -> dict | None:
    resp = requests.get(GEO_URL,params={"name": city, "count": 1, "language": "en", "format": "json"},timeout=5)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        return None
    r = results[0]
    return {
        "name": r["name"],
        "country": r.get("country",""),
        "lat": r["latitude"],
        "lon": r["longitude"],
    }

def get_weather(lat: float , lon: float) -> dict:
    resp = requests.get(FORCAST_URL,params={
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m", "precipitation", 
            "weather_code", "wind_speed_10m", "wind_direction_10m"
        ],
        "daily": [
            "weather_code", "temperature_2m_max",
            "temperature_2m_min", "precipitation_probability_max",
        ],
        "hourly": "uv_index",
        "forecast_days": 7,
        "timezone": "auto",
    }, timeout=5)
    resp.raise_for_status()
    return resp.json()