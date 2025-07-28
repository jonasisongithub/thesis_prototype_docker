import streamlit as st # type: ignore
import base64
import streamlit.components.v1 as components # type: ignore
import time
import json
from datetime import datetime
import os
from streamlit.navigation import switch_page # type: ignore

# WICHTIG: Prüfung, ob die Session-Variablen existieren.
# Wenn nicht, wird der Nutzer zur Startseite zurückgeleitet.
if "name" not in st.session_state or st.session_state.name == "":
    # Je nachdem, wie deine Startseite heißt. app.py ist der Standard.
    switch_page("app.py")


# Import all necessary functions
from prompts import step1_icebreakerquestion, step2_questions, end_conversation, transcript_summary


# Load variables from session state
name = st.session_state.get("name")
position = st.session_state.get("position")
task = st.session_state.get("task")
context = st.session_state.get("context")
guideline = st.session_state.get("guideline")

# Seiteneinstellungen
st.set_page_config(
    page_title="GEMA Knowledge Share",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# --- Initialize messages and intro question at the very beginning ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    intro_message = step1_icebreakerquestion()
    st.session_state.messages.append({"role": "assistant", "content": intro_message})

if "intro_displayed_once" not in st.session_state:
    st.session_state.intro_displayed_once = False
# --- End initialization ---


# background image and logo loading
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

bg_base64 = get_base64_image("./pages/images/background_boxes.jpg")
logo_base64 = get_base64_image("./pages/images/logo_gema.jpg")

# --- Injecting Global CSS ---
st.markdown(
    """
    <style>
    html, body, [class*="stApp"] {
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }

    .logo-container {
        position: fixed;
        top: 60px;
        right: 80px;
        z-index: 1000;
    }

    .logo-container img {
        height: 10vh;
    }

    .exit-button-container {
        position: fixed;
        top: 20px; /* Adjust as needed */
        right: 80px; /* Align with logo or adjust */
        z-index: 1001; /* Ensure it's above other elements */
    }

    .explanation-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #3f4249;
        margin-bottom: 20px;
        margin-top: -5vh;
    }
    .explanation-box p {
        margin-bottom: 0.5em;
    }

    div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
        background-color: rgba(51, 51, 51, 0.7) !important;
        border-radius: 0.5rem;
        padding: 0.8rem;
        color: #FFFFFF !important;
    }

    div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"]::before {
        border-right-color: rgba(51, 51, 51, 0.7) !important;
        border-left-color: rgba(51, 51, 51, 0.7) !important;
    }

    .stChatMessage {
        background-color: transparent !important;
        margin-bottom: 0.5rem;
    }

    .scroll-marker {
        height: 10px; /* Small height to make it scrollable */
        width: 100%;
        margin-top: 50px; /* Space before marker */
        /* background-color: transparent; /* Make it invisible */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- End Injecting Global CSS ---

# --- Direct Background Image Injection ---
st.markdown(
    f"""
    <style>
    html, body, [class*="stApp"] {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- End Direct Background Image Injection ---

# --- Logo ---
st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)
# --- End Logo ---

# Header
components.html(
    f"""
    <div style="
        font-family: 'Segoe UI', sans-serif;
        color: #3f4249;
        font-size: 30vh;
        padding-left: 0vw;
        padding-top: 0vh;
        margin: 0;
        ">
        <h1 style="margin: 0;">GEMA Knowledge Share</h1>
    </div>
    """,
    height=150,
)

# Explanation Box
st.markdown(
    """
    <div class="explanation-box">
        <p>Willkommen zu diesem Interview!</p>
        <p>Dir werden gleich Fragen gestellt, die du einfach über die <b>Eingabezeile</b> beantworten kannst. Es gibt dabei kein Richtig oder Falsch, sondern es geht vor allem um deine Erfahrungen, deine Sichtweisen und dein Wissen!</p>
        <p>Du kannst das Interview jederzeit pausieren oder beenden. Zum Beenden drücke entweder den "Beenden"-Button oben links verwenden oder gib im Gespräch den Hinweis, dass du das Interview gern beenden möchtest.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Stream Function
def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.02)

# Exit Button
exit_button_placeholder = st.empty()


# Display historic messages
for i, message in enumerate(st.session_state.messages):
    # Special handling for the very first message to ensure it streams after UI loads
    if i == 0 and not st.session_state.intro_displayed_once:
        # Sleep to wait for full rendering
        if "initial_ui_load_delay" not in st.session_state:
            time.sleep(0.5)
            st.session_state.initial_ui_load_delay = True

        with st.chat_message("assistant"):
            st.write_stream(stream_text(message["content"]))
        st.session_state.intro_displayed_once = True
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

scroll_marker_placeholder = st.empty()

def trigger_end_session():
    """Triggers the entire session end sequence."""
    st.session_state.end_session_triggered = True
    st.rerun()

# Input Field
# Only show input if the session is active and not pending termination
if "end_session_triggered" not in st.session_state or not st.session_state.end_session_triggered:
    if prompt := st.chat_input("Deine Antwort"):
        # display input & add to history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        last_user_response = prompt
        full_chat_history = st.session_state.messages

        response_text = step2_questions(last_user_response, full_chat_history)

        # Always check for temrination code
        if response_text == "t435kd90":
            trigger_end_session() # Automatically trigger end sequence
        else:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.write_stream(stream_text(response_text))
            if 'awaiting_stream' in st.session_state:
                del st.session_state['awaiting_stream']
else:
    st.chat_input("Das Interview wird beendet...", disabled=True)


# Logic for Exit Button
with exit_button_placeholder:
    if st.button("Beenden"):
        trigger_end_session()

if "end_session_triggered" in st.session_state and st.session_state.end_session_triggered:
    # Scroll to the end message before displaying it
    with scroll_marker_placeholder.container():
        st.markdown('<div id="scroll_to_me" class="scroll-marker"></div>', unsafe_allow_html=True)
        components.html(
            """
            <script>
                var element = document.getElementById('scroll_to_me');
                if (element) {
                    element.scrollIntoView({behavior: "smooth", block: "end"});
                }
            </script>
            """,
            height=0, width=0,
        )

    time.sleep(1)

    # Ending message
    final_display_message = end_conversation(full_chat_history=st.session_state.messages)

    if not st.session_state.messages or st.session_state.messages[-1]["content"] != final_display_message:
         st.session_state.messages.append({"role": "assistant", "content": final_display_message})

    with st.chat_message("assistant"):
        st.write_stream(stream_text(final_display_message))

    time.sleep(1)

    # store the transcript
    if not os.path.exists("./output/transcripts"):
        os.makedirs("./output/transcripts", exist_ok=True)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_name = st.session_state.get("name", "user")
    filename = f"./output/transcripts/transcript_{current_time}_{transcript_name}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for message in st.session_state.messages:
            f.write(f"{message['role'].upper()}: {message['content']}\n\n")

    transcript_summary(filename)

    time.sleep(2)

    #Success message
    st.session_state.clear()
    st.success(f"Das Interview wurde beendet. Vielen Dank für deine Teilnahme!")
    st.stop()