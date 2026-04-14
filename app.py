import streamlit as st
from datetime import datetime
import pandas as pd
from google_auth import worksheet

# --- Load data from Google Sheet ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# --- App title ---
st.title("Class Mood Check-In")

# --- Student input ---
name = st.text_input("Enter your name")

mood = st.selectbox(
    "How are you feeling?",
    ["Happy", "Calm", "Tired", "Stressed", "Sad"]
)

# --- Submit logic ---
if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name")
    else:
        name_clean = name.strip().title()
        today_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        duplicate = False
        if not df.empty and "Timestamp" in df.columns and "Name" in df.columns:
            df["Date"] = pd.to_datetime(df["Timestamp"], errors="coerce").dt.strftime("%Y-%m-%d")
            duplicate = ((df["Name"] == name_clean) & (df["Date"] == today_date)).any()

        if duplicate:
            st.error("You have already submitted today.")
        else:
            worksheet.append_row([name_clean, mood, timestamp])
            st.success("Submitted successfully!")

# --- Reload updated data ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# --- Public summary only ---
st.subheader("Live Class Mood Summary")

if not df.empty and "Mood" in df.columns:
    mood_counts = df["Mood"].value_counts()
    st.bar_chart(mood_counts)
    st.write(f"Total submissions: {len(df)}")
else:
    st.info("No mood data available yet.")