import streamlit as st
import requests
from datetime import datetime
from collections import defaultdict

# === CONFIG ===
API_KEY = "45bf96ebdb4744385db2112b403a9032"
CITY = "Mosbach,de"

# === Wochentage auf Deutsch ===
weekday_map = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag"
}

# === FUNKTIONEN ===
def get_weather(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=de"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler beim Abrufen der Wetterdaten.")
        return None

def format_forecast(data):
    forecast_list = data["list"]
    daily = defaultdict(list)

    for entry in forecast_list:
        dt = datetime.fromtimestamp(entry["dt"])
        weekday_en = dt.strftime("%A")
        weekday_de = weekday_map.get(weekday_en, weekday_en)
        day_key = f"{weekday_de}, {dt.strftime('%d.%m.')}"
        daily[day_key].append(entry)

    summary = {}
    for day, entries in daily.items():
        temps = [e["main"]["temp"] for e in entries]
        temp_min = min([e["main"]["temp_min"] for e in entries])
        temp_max = max([e["main"]["temp_max"] for e in entries])
        icon = entries[0]["weather"][0]["icon"]
        desc = entries[0]["weather"][0]["description"].capitalize()
        summary[day] = {
            "min": temp_min,
            "max": temp_max,
            "icon": icon,
            "desc": desc
        }
    return summary

# === UI ===
st.set_page_config(page_title="Dein Dashboard", layout="centered")
st.title("📊 Persönliches Dashboard")
st.header("🌤 Wetter in Mosbach")

weather_data = get_weather(API_KEY, CITY)
if weather_data:
    daily_forecast = format_forecast(weather_data)
    for day, info in list(daily_forecast.items())[:3]:
        st.subheader(f"{day}")
        st.image(f"http://openweathermap.org/img/wn/{info['icon']}@2x.png", width=60)
        st.write(f"{info['desc']}")
        st.write(f"🌡️ {info['min']:.1f}°C – {info['max']:.1f}°C")
