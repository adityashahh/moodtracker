import streamlit as st
from datetime import datetime
import pandas as pd
from google_auth import worksheet
import base64
import random

# --- Function for autoplay audio ---
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# --- Load data from Google Sheet ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# --- App title ---
st.title("Class Mood Check-In")

# --- Initialize session state ---
if "student_id" not in st.session_state:
    st.session_state.student_id = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "mood" not in st.session_state:
    st.session_state.mood = "Happy 😊"

if "last_quote" not in st.session_state:
    st.session_state.last_quote = None

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

if "last_success" not in st.session_state:
    st.session_state.last_success = False

# --- Student input ---
student_id = st.text_input("Enter your student ID", key="student_id")
name = st.text_input("Enter your name", key="name")

mood = st.selectbox(
    "How are you feeling?",
    ["Happy 😊", "Calm 😌", "Tired 😴", "Stressed 😣", "Sad 😔"],
    key="mood"
)

# --- Audio mapping ---
audio_map = {
    "Happy 😊": "happy.mp3",
    "Calm 😌": "calm.mp3",
    "Tired 😴": "tired.mp3",
    "Stressed 😣": "stressed.mp3",
    "Sad 😔": "sad.mp3"
}

# --- Quote mapping ---
quote_map = {
    "Happy 😊": [
        "Keep shining. Your energy can lift the whole room.",
        "Joy is powerful. Carry it with confidence today.",
        "A good mood can spark great ideas.",
        "Your positivity matters more than you think.",
        "Bring that bright energy into everything you do today.",
        "Happy minds often notice beautiful possibilities.",
        "You are allowed to enjoy this moment fully.",
        "Let your good energy guide your learning today.",
        "A cheerful heart creates space for growth.",
        "Keep smiling. It might help someone else smile too.",
        "Positive energy is contagious. Share it well.",
        "Today is a good day to make progress.",
        "Your happiness is a strength, not a distraction.",
        "Hold onto this feeling and let it support your work.",
        "Enjoy the good mood. You earned it."
    ],
    "Calm 😌": [
        "A calm mind helps you learn with clarity.",
        "Peace creates space for strong thinking.",
        "Stillness can be a quiet kind of strength.",
        "Calm energy helps steady the day ahead.",
        "A peaceful start can shape a productive day.",
        "You do not have to rush to do well.",
        "A centered mind can handle a lot.",
        "Breathe deeply. You are in a good place to begin.",
        "Calmness is not weakness. It is control.",
        "A steady mind makes room for better decisions.",
        "You are grounded, and that is powerful.",
        "Sometimes the strongest energy is calm energy.",
        "Quiet confidence can take you far today.",
        "When your mind is calm, your focus grows stronger.",
        "Let today unfold one clear step at a time."
    ],
    "Tired 😴": [
        "Small steps still count. Keep going gently.",
        "It is okay to feel tired. Progress can still happen.",
        "You do not need to be at 100 percent to do something meaningful.",
        "Take it one task at a time. That is enough.",
        "Rested or not, you are still capable.",
        "Tired does not mean failing. It means you are human.",
        "Give yourself patience as well as effort today.",
        "Even slow progress is progress.",
        "A little focus can still go a long way.",
        "Be kind to yourself while you move through the day.",
        "You can do hard things, even on low energy.",
        "Today may call for gentleness, not perfection.",
        "One good step is enough for now.",
        "Keep showing up. That matters.",
        "Your effort still counts, even when you are tired."
    ],
    "Stressed 😣": [
        "Take one breath, then one task, then the next.",
        "You do not have to solve everything at once.",
        "Pause. Breathe. Begin again.",
        "Stress is real, but it does not define your ability.",
        "Focus on what is in front of you right now.",
        "One calm moment can reset a stressful day.",
        "You are stronger than this moment feels.",
        "Break the day into smaller pieces and keep moving.",
        "You can handle this step by step.",
        "It is okay to slow down and regroup.",
        "Pressure can be managed one breath at a time.",
        "Your worth is not measured by your stress.",
        "Let progress be enough today.",
        "You are not alone in difficult moments.",
        "Take the next small step. That is how things get easier."
    ],
    "Sad 😔": [
        "It is okay to have a heavy day. Be gentle with yourself.",
        "You do not have to hide your hard moments.",
        "Sad days still pass, and better ones can follow.",
        "Give yourself kindness before asking for strength.",
        "You are allowed to feel this without apology.",
        "A difficult feeling does not make you weak.",
        "Take care of yourself in small ways today.",
        "Even on hard days, your presence matters.",
        "You deserve patience, compassion, and support.",
        "There is no shame in feeling low sometimes.",
        "One quiet moment of care can help more than you think.",
        "You are still valuable on your hardest days.",
        "Healing often begins with honesty.",
        "Let today be soft if it needs to be.",
        "Better moments can still come."
    ]
}

# --- Submit logic ---
if st.button("Submit"):
    if student_id.strip() == "" or name.strip() == "":
        st.warning("Please enter both your student ID and your name.")
    else:
        student_id_clean = student_id.strip()
        name_clean = name.strip().title()
        today_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        duplicate = False
        if (
            not df.empty
            and "Timestamp" in df.columns
            and "StudentID" in df.columns
        ):
            df["Date"] = pd.to_datetime(df["Timestamp"], errors="coerce").dt.strftime("%Y-%m-%d")
            duplicate = (
                (df["StudentID"].astype(str).str.strip() == student_id_clean)
                & (df["Date"] == today_date)
            ).any()

        if duplicate:
            st.error("This student ID has already submitted today.")
            st.session_state.last_success = False
        else:
            worksheet.append_row([student_id_clean, name_clean, mood, timestamp])

            st.session_state.last_quote = random.choice(quote_map[mood])
            st.session_state.last_audio = audio_map.get(mood)
            st.session_state.last_success = True

            # Clear inputs
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.session_state.mood = "Happy 😊"

            st.rerun()

# --- Show success / quote / audio after rerun ---
if st.session_state.last_success:
    st.success("Submitted successfully!")

    if st.session_state.last_quote:
        st.info(f"Quote for you: {st.session_state.last_quote}")

    if st.session_state.last_audio:
        autoplay_audio(st.session_state.last_audio)
        with open(st.session_state.last_audio, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

# --- Reload updated data ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# --- Public summary ---
st.subheader("Live Class Mood Summary")

if not df.empty and "Mood" in df.columns:
    mood_counts = df["Mood"].value_counts()
    st.bar_chart(mood_counts)
    st.write(f"Total submissions: {len(df)}")
else:
    st.info("No mood data available yet.")

# --- Support flag logic using StudentID ---
st.subheader("Support Check")

if not df.empty and "StudentID" in df.columns and "Mood" in df.columns:
    flagged = []

    for sid in df["StudentID"].dropna().astype(str).str.strip().unique():
        student_data = df[df["StudentID"].astype(str).str.strip() == sid]

        low_mood_count = student_data[
            student_data["Mood"].isin(["Sad 😔", "Stressed 😣"])
        ].shape[0]

        if low_mood_count >= 3:
            flagged.append(sid)

    if flagged:
        st.warning(
            "Some students may need extra support. "
            "CSUMB PGCC crisis support is available 24/7 at 831-582-3969. "
            "Call or text 988 for the Suicide & Crisis Lifeline. "
            "In an emergency, call 911."
        )
    else:
        st.success("No support flags right now.")
else:
    st.info("Support check will appear once submissions are available.")