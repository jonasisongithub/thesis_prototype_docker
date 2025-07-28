import streamlit as st # type: ignore
import base64
import time
import os
from datetime import datetime

# Modul-Pfade für den Zugriff auf Hilfsfunktionen im Stammverzeichnis
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompts import step1_icebreakerquestion, step2_questions, end_conversation, transcript_summary

# --- Sicherheitscheck: Sicherstellen, dass die Vorbereitung abgeschlossen ist ---
if "preparation_done" not in st.session_state or not st.session_state.preparation_done:
    st.warning("Bitte bereite das Interview zuerst auf der 'Über Dich'-Seite vor.")
    st.page_link("app.py", label="Zurück zur Startseite", icon="🏠")
    st.stop()

# Seiteneinstellungen
st.set_page_config(
    page_title="Interview - GEMA Knowledge Share",
    layout="centered", # 'centered' ist oft besser für Chat-Interfaces
    initial_sidebar_state="collapsed",
)

st.markdown("<style> .main .block-container {padding-top: 2rem;} </style>", unsafe_allow_html=True)


# --- Hilfsfunktionen & CSS ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Bilddatei nicht gefunden: {image_path}")
        return ""

bg_base64 = get_base64_image("./assets/background_boxes.jpg")
logo_base64 = get_base64_image("./assets/logo_gema.jpg")

st.markdown(
    f"""
    <style>
    html, body, [class*="stApp"] {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    .logo-container {{ position: fixed; top: 20px; right: 40px; z-index: 1000; }}
    .logo-container img {{ height: 8vh; }}
    /* Weitere CSS-Anpassungen für das Chat-Interface können hier erfolgen */
    </style>
    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)


# --- Initialisierung & Daten aus Session State laden ---
# Laden der Benutzerdaten aus dem Session State
name = st.session_state.get("user_name", "Teilnehmer")
position = st.session_state.get("user_position", "")
task = st.session_state.get("user_task", "")
context = st.session_state.get("expert_context", "")
guideline = st.session_state.get("interview_guideline", "")

# Initialisieren des Chat-Verlaufs und der ersten Frage
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Erste Frage mit den Daten aus dem Session State generieren
    with st.spinner("Moment, die erste Frage wird geladen..."):
        intro_message = step1_icebreakerquestion(name, position, task, context, guideline)
        st.session_state.messages.append({"role": "assistant", "content": intro_message})

# --- Chat-Interface ---
st.title("Interview")
st.markdown("Beantworte die Fragen des Assistenten. Du kannst das Interview jederzeit über den Button oben beenden.")

# Knopf zum Beenden des Interviews
if st.button("Interview beenden"):
    st.session_state.end_session_triggered = True
    st.rerun()

# Anzeigen des Chatverlaufs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Logik für das Beenden der Session
if st.session_state.get("end_session_triggered", False):
    st.chat_input("Das Interview wird beendet...", disabled=True)
    
    with st.spinner("Schließe das Interview ab und erstelle die Zusammenfassung..."):
        # Endnachricht generieren
        final_message = end_conversation(name, position, task, context, guideline, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": final_message})
        
        with st.chat_message("assistant"):
            st.write(final_message)
        
        # Transkript im gemounteten Volumen speichern
        output_path = "/interview_output"
        os.makedirs(output_path, exist_ok=True) 
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_path}/transcript_{timestamp}_{name.replace(' ', '_')}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            for message in st.session_state.messages:
                f.write(f"{message['role'].upper()}: {message['content']}\n\n")

        transcript_summary(filename, context, output_path) 

    st.success("Das Interview wurde erfolgreich beendet und gespeichert. Vielen Dank für deine Teilnahme!")
    st.balloons()
    time.sleep(5)
    
    # Session State aufräumen 
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.page_link("app.py", label="Zurück zur Startseite", icon="🏠")
    st.stop()


# Eingabefeld für Benutzerantworten
if prompt := st.chat_input("Deine Antwort..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Nächste Frage vom Assistenten generieren
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = step2_questions(
                name=name,
                position=position,
                task=task,
                context=context,
                guideline=guideline,
                last_user_response=prompt,
                full_chat_history=st.session_state.messages
            )
            
            # Prüfen, ob das Interview beendet werden soll
            if response == "t435kd90":
                st.session_state.end_session_triggered = True
                st.rerun()
            else:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})