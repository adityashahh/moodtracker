import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# --- LOCAL vs STREAMLIT CLOUD ---
if os.path.exists("keys.json"):
    # Local (your laptop)
    CREDS = ServiceAccountCredentials.from_json_keyfile_name("keys.json", SCOPE)
else:
    # Streamlit Cloud
    import streamlit as st
    CREDS = ServiceAccountCredentials.from_json_keyfile_dict(
        dict(st.secrets["gcp_service_account"]), SCOPE
    )

client = gspread.authorize(CREDS)

sheet = client.open("BUS472")
worksheet = sheet.sheet1