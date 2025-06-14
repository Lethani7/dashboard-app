import streamlit as st
import requests
from datetime import datetime

# === CONFIG ===
API_KEY = "45bf96ebdb4744385db2112b403a9032"
CITY = "Mosbach,de"

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
    daily = {}
    for entry in forecast_list:
        dt = datetime.fromtimestamp(entry["dt"])
        day = dt.strftime("%A")
        if day not in daily:
            daily[day] = entry
    return daily

# === UI ===
st.set_page_config(page_title="Dein Dashboard", layout="centered")
st.title("📊 Persönliches Dashboard")
st.header("🌤 Wetter in Mosbach")

weather_data = get_weather(API_KEY, CITY)
if weather_data:
    daily_forecast = format_forecast(weather_data)
    for day, info in list(daily_forecast.items())[:3]:
        temp = info["main"]["temp"]
        desc = info["weather"][0]["description"].capitalize()
        icon = info["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        st.subheader(f"{day}")
        st.image(icon_url, width=60)
        st.write(f"{desc}, {temp:.1f}°C")
