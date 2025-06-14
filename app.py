import streamlit as st
import requests
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
import pytz

# Import Google Kalender-Module
from google_calendar import authenticate_user, save_token_from_code, get_calendar_events

# === Wetter-Config ===
API_KEY = "45bf96ebdb4744385db2112b403a9032"
CITY = "Mosbach,de"

weekday_map = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag"
}

# === Wetter-Funktionen ===
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

# === Streamlit App ===
st.set_page_config(page_title="Dein Dashboard", layout="centered")
st.title("📊 Persönliches Dashboard")

# === Wetteranzeige ===
st.header("🌤 Wetter in Mosbach")

weather_data = get_weather(API_KEY, CITY)
if weather_data:
    daily_forecast = format_forecast(weather_data)
    for day, info in list(daily_forecast.items())[:3]:
        st.subheader(f"{day}")
        st.image(f"http://openweathermap.org/img/wn/{info['icon']}@2x.png", width=60)
        st.write(f"{info['desc']}")
        st.write(f"🌡️ {info['min']:.1f}°C – {info['max']:.1f}°C")

# === Google Kalender ===
st.header("🗓️ Nächste Termine (Google Kalender)")

query_params = st.experimental_get_query_params()
if "code" in query_params:
    code = query_params["code"][0]
    save_token_from_code(code)
    st.success("✅ Zugriff erfolgreich erlaubt! Die Termine werden geladen...")
    st.experimental_rerun()

auth_url = authenticate_user()
if auth_url:
    st.info("Bitte erlaube den Zugriff auf deinen Google Kalender.")
    st.markdown(f"[➡️ Hier klicken, um Google-Zugriff zu erlauben]({auth_url})")
else:
    events = get_calendar_events(10)
    if not events:
        st.write("Keine bevorstehenden Termine gefunden.")
    else:
        tz = pytz.timezone("Europe/Berlin")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            dt = datetime.fromisoformat(start).astimezone(tz)
            weekday = dt.strftime("%A")
            date_str = dt.strftime("%d.%m.%Y")
            time_str = dt.strftime("%H:%M")
            st.write(f"📅 **{weekday}, {date_str}** – 🕒 {time_str} – {event['summary']}")
