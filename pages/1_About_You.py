import streamlit as st # type: ignore
import base64
import sys
import os
import time


from rag import get_context
from interview_guideline import generate_interview_guideline

# Seiteneinstellungen
st.set_page_config(
    page_title="Über Dich - GEMA Knowledge Share",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("<style> .main .block-container {padding-top: 2rem;} </style>", unsafe_allow_html=True)


# --- Hilfsfunktionen und CSS ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Bilddatei nicht gefunden: {image_path}")
        return ""

# Pfade zum neuen assets-Ordner im Stammverzeichnis
bg_base64 = get_base64_image("./assets/background_boxes.jpg")
logo_base64 = get_base64_image("./assets/logo_gema.jpg")

# CSS: Hintergrund, Logo und Stile
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
    .logo-container {{ position: fixed; top: 60px; right: 80px; z-index: 1000; }}
    .logo-container img {{ height: 10vh; }}
    h1.gema-headline, h2.gema-subheadline, p.gema-intro {{ font-family: 'Segoe UI', sans-serif; color: #3f4249; }}
    h1.gema-headline {{ font-size: 8vh; margin: 0 0 1vh 0; }}
    h2.gema-subheadline {{ font-size: 4vh; margin: 0 0 1vh 0; }}
    p.gema-intro {{ font-size: 20px; margin-bottom: 2vh; }}
    </style>

    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# --- Seiteninhalt ---

st.markdown("""
<h1 class="gema-headline">GEMA Knowledge Share</h1>
<h2 class="gema-subheadline">Über dich</h2>
<p class="gema-intro">
Damit wir dir im Nachgang passende Fragen stellen können, hilft es uns sehr, wenn du uns kurz ein paar Dinge über dich verrätst.
</p>
""", unsafe_allow_html=True)

# Formular zur Erfassung der Benutzerdaten
with st.form("user_info_form"):
    name = st.text_input("**Wer bist du?**", placeholder="z.B. Max Mustermann")
    position = st.text_input("**Wie lautet deine Stellenbezeichnung?**", placeholder="z.B. Service Managerin im Second Level Support")
    task = st.text_area("**Zu welchen Themen und Aufgaben bei der GEMA möchtest du heute sprechen?**", placeholder="Gib uns hier gern möglichst viele Einblicke und Schlagwörter, z.B. Mitgliederservice, Detailaufstellungen, Reklamationen Live-U, ...", height=150)
    
    submitted = st.form_submit_button("Weiter")

if submitted:
    if name.strip() and position.strip() and task.strip():
        with st.spinner("Wir bereiten dein persönliches Interview vor. Dies kann bis zu einer Minute dauern..."):
            try:
                # 1. Kontext aus RAG abrufen
                context = get_context(task)
                st.session_state["expert_context"] = context
                print("Retrieval successful")

                # 2. Interview-Leitfaden generieren
                guideline = generate_interview_guideline(position, task, context)
                st.session_state["interview_guideline"] = guideline
                print("Guideline generation successful")
                
                # 3. Alle Daten im Session State speichern
                st.session_state["user_name"] = name
                st.session_state["user_position"] = position
                st.session_state["user_task"] = task
                
                # Markieren, dass die Vorbereitung abgeschlossen ist
                st.session_state["preparation_done"] = True

            except Exception as e:
                st.error(f"Ein Fehler ist bei der Vorbereitung aufgetreten: {e}")
                st.session_state["preparation_done"] = False
    else:
        st.warning("Bitte fülle alle Felder aus, um fortzufahren.", icon="⚠️")

# Logik nach der erfolgreichen Vorbereitung
if st.session_state.get("preparation_done", False):
    st.success("Vorbereitung abgeschlossen! Fast geschafft.", icon="✅")
    
    st.markdown("""
    <div style="background-color: white; border-radius: 12px; width: 100%; padding: 20px; margin-top: 20px;">
        <h2 class="gema-subheadline">Datenschutz</h2>
        <p style="font-size: 18px; color: #3f4249;">
            Danke für diese Informationen. Bevor wir starten, benötigen wir deine Erlaubnis, dieses Interview zu transkribieren und die Inhalte zur Erstellung von Wissensartikeln weiterzuverwenden. Wenn du damit einverstanden bist, klicke bitte auf "Zustimmen & Interview starten".
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Zustimmen & Interview starten", type="primary"):
        st.switch_page("pages/2_Interview.py")