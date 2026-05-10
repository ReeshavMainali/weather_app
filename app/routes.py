from flask import Blueprint, render_template, request
from .weather_services import get_coordinates, get_weather
from .advice import get_advice 

main = Blueprint("__main__", __name__)

WMO = {
    0: ("Clear sky", "☀️"),        1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),           48: ("Rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),   53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌧️"),   61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),   65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),      73: ("Snow", "❄️"),
    75: ("Heavy snow", "❄️"),      77: ("Snow grains", "🌨️"),
    80: ("Rain showers", "🌦️"),    81: ("Heavy showers", "🌧️"),
    82: ("Violent showers", "⛈️"), 95: ("Thunderstorm", "⛈️"),
    96: ("Storm + hail", "⛈️"),    99: ("Storm + hail", "⛈️"),
}

WIND_DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

def parse_weather(raw: dict, location: dict) -> dict:
    cur = raw["current"]
    daily = raw["daily"]
    hourly = raw.get("hourly",{})

    code = cur["weather_code"]
    label, icon = WMO.get(code, ("Unknown", "🌡️"))
    temp = round(cur["temperature_2m"])
    feels = round(cur["apparent_temperature"])
    wind = round(cur["wind_speed_10m"])
    wind_dir = WIND_DIRS[round(cur["wind_direction_10m"] / 45) % 8]
    humidity = round(cur["relative_humidity_2m"])

    uv_list = hourly.get("uv_index") or []
    uv = round(max(uv_list[:24])) if uv_list else 0

    forecast = []
    days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    for i, date_str in enumerate(daily["time"]):
        from datetime import date
        d = date.fromisoformat(date_str)
        wc = daily["weather_code"][i]
        _, d_icon = WMO.get(wc, ("", "🌡️"))
        forecast.append({
            "label": "Today" if i == 0 else days[d.weekday()],
            "icon": d_icon,
            "hi": round(daily["temperature_2m_max"][i]),
            "lo": round(daily["temperature_2m_min"][i]),
            "rain_chance": daily["precipitation_probability_max"][i],
        })
    
    advice = get_advice(code, temp, wind, humidity, uv)

    return {
        "location":f"{location['name']}, {location['country']}",
        "temp": temp, "feels": feels, "label": label, "icon": icon,
        "wind": wind, "wind_dir": wind_dir, "humidity": humidity,"uv": uv,
        "forecast": forecast, "advice": advice,
    }

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/weather", methods=["GET", "POST"])
def weather():
    city = request.form.get("city") or request.args.get("city","Kathmandu")
    error = None
    weather_data = None

    try:
        location = get_coordinates(city)
        if not location:
            error = f"Could not find location for '{city}'. Try a different spelling"
        else:
            raw = get_weather(location["lat"], location["lon"])
            weather_data = parse_weather(raw, location)
    except Exception as e:
        error = f"Error fetching weather data: {str(e)}"

    return render_template("weather.html", weather=weather_data, error=error, city=city)

