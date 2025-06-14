import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_user():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
import streamlit as st
import json
import tempfile

client_info = json.loads(st.secrets["google"]["client_info"])
with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp:
    json.dump(client_info, temp)
    temp.flush()
    flow = Flow.from_client_secrets_file(
        temp.name,
        scopes=SCOPES,
        redirect_uri='https://<deine-app-id>.streamlit.app/'
    )

            scopes=SCOPES,
            redirect_uri='http://localhost:8501/'
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url
    return None

def save_token_from_code(code):
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri='http://localhost:8501/'
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open("token.json", "w") as token:
        token.write(creds.to_json())

def get_calendar_events(max_results=10):
    if not os.path.exists("token.json"):
        return []
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])
