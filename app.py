import streamlit as st
from datetime import datetime
import pandas as pd
from google_auth import worksheet

data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("Class Mood Check-In")

name = st.text_input("Enter your name")
mood = st.selectbox(
    "How are you feeling?",
    ["Happy", "Calm", "Tired", "Stressed", "Sad"]
)

if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name")
    else:
        name_clean = name.strip().title()
        today_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        duplicate = False
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d")
            duplicate = ((df["Name"] == name_clean) & (df["Date"] == today_date)).any()

        if duplicate:
            st.error("You have already submitted today.")
        else:
            worksheet.append_row([name_clean, mood, timestamp])
            st.success("Submitted successfully!")

data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("Live Class Mood Summary")
if not df.empty:
    mood_counts = df["Mood"].value_counts()
    st.bar_chart(mood_counts)
    st.write(f"Total submissions: {len(df)}")

st.subheader("Mood Alerts")
if not df.empty:
    alert_students = []
    for student in df["Name"].unique():
        student_data = df[df["Name"] == student]
        negative_count = student_data[
            student_data["Mood"].isin(["Stressed", "Sad"])
        ].shape[0]

        if negative_count >= 3:
            alert_students.append((student, negative_count))

    if alert_students:
        for s, count in alert_students:
            st.warning(f"{s} has reported stress/sad {count} times")
    else:
        st.success("No alerts")

st.subheader("Full Data")
if not df.empty:
    st.dataframe(df)