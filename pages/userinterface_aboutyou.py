import streamlit as st # type: ignore
import base64
import sys
import os
import time
import json


# Modul-Pfad erweitern für Zugriff auf rag.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag import get_context
from interview_guideline import generate_interview_guideline

# Seiteneinstellungen
st.set_page_config(
    page_title="GEMA Knowledge Share",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Hintergrundbild laden und kodieren
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

bg_base64 = get_base64_image("./pages/images/background_boxes.jpg")
logo_base64 = get_base64_image("./pages/images/logo_gema.jpg")

# CSS: Hintergrund + Logo + Headline-Styles + Button
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

    .logo-container {{
        position: fixed;
        top: 60px;
        right: 80px;
        z-index: 1000;
    }}

    .logo-container img {{
        height: 10vh;
    }}

    h1.gema-headline {{
        font-family: 'Segoe UI', sans-serif;
        font-size: 11vh;
        color: #3f4249;
        margin: 0 0 2vh 0;
        padding: 0;
    }}

    h2.gema-subheadline {{
        font-family: 'Segoe UI', sans-serif;
        font-size: 4vh;
        color: #3f4249;
        margin: 0 0 1vh 0;
        padding: 0;
    }}

    p.gema-intro {{
        font-size: 20px;
        color: #3f4249;
        margin-bottom: 2vh;
    }}

    .centered-button {{
        display: flex;
        justify-content: center;
        margin-top: 4vh;
    }}

    .red-button button {{
        background-color: #cc0000;
        color: white !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        padding: 0.5em 2em !important;
        width: 12vw;
        height: 7vh;
        font-weight: bold;
    }}

    .red-button button:hover {{
        background-color: #a30000;
        transform: scale(1.03);
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Überschrift + Introtext
st.markdown("""
<h1 class="gema-headline">GEMA Knowledge Share</h1>
<h2 class="gema-subheadline">Über dich</h2>
<br>
<p class="gema-intro">
Damit wir dir im Nachgang passende Fragen stellen können, hilft es uns sehr, wenn du uns kurz ein paar Dinge über dich verrätst.
</p>
""", unsafe_allow_html=True)

# Eingabefelder
st.markdown("<div style='margin-top: 5px; font-size: 20px; font-weight: bold; color: #3f4249; margin-bottom: -50px;'>Wer bist du?</div>", unsafe_allow_html=True)
name = st.text_input("", placeholder="z.B. Max Mustermann")


st.markdown("<div style='margin-top: 2vh;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 5px; font-size: 20px; font-weight: bold; color: #3f4249; margin-bottom: -50px;'>Wie lautet deine Stellenbezeichnung bei der GEMA?</div>", unsafe_allow_html=True)
position = st.text_input("", placeholder="z.B. Service Managerin im Second Level Support, Direktion MKS, im Kundenservice")

st.markdown("<div style='margin-top: 2vh;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 5px; font-size: 20px; font-weight: bold; color: #3f4249; margin-bottom: -50px;'>Zu welchen Themen wirst du besonders häufig von deinen Kolleginnen und Kollegen um Rat gefragt? Was sind Aufgaben, Prozesse oder Projekte bei der GEMA über die wir heute sprechen wollen? Gib uns hier gern möglichst viele Einblicke und Schlagwörter, um das Interview bestmöglich vorbereiten zu können.</div>", unsafe_allow_html=True)
task = st.text_input("", placeholder="z.B. Mitgliederservice im Second Level Support, Fragen zu Detailaufstellungen, Reklamationen Live-U")


# Init Session States
if "weiter_geklickt" not in st.session_state:
    st.session_state["weiter_geklickt"] = False
    st.session_state["ladephase_abgeschlossen"] = False


# Weiter-Button-Verarbeitung
def handle_continue_click():
    st.session_state["weiter_geklickt"] = True
    with st.spinner("⏳"):
        st.markdown('<p style="color:#3f4249;">Wir bereiten das Interview für dich vor. Dies kann bis zu einer Minute dauern. Bitte habe ein wenig Geduld. Wir freuen uns auf das Interview mit dir!</p>', unsafe_allow_html=True)

        context = None
        guideline = None

        try:
            context = get_context(task)
            print("Retrieval successful", context)
            st.session_state["expert_context"] = context
        except Exception as e:
            st.error(f"Fehler beim Laden des Kontexts: {e}")
            st.session_state["expert_context"] = None

        try:
            if context is not None:
                guideline = generate_interview_guideline(position, task, context)
                print("Guideline generation successful", guideline)
                st.session_state["interview_guideline"] = guideline
            else:
                st.warning("Kontext konnte nicht geladen werden, Interviewleitfaden wird möglicherweise nicht optimal generiert.")
                st.session_state["interview_guideline"] = None
        except Exception as e:
            st.error(f"Fehler bei der Generierung des Interviewleitfadens: {e}")
            st.session_state["interview_guideline"] = None

        time.sleep(0.5)
        st.session_state["ladephase_abgeschlossen"] = True

        st.session_state.name = name
        st.session_state.position = position
        st.session_state.task = task
        st.session_state.context = context
        st.session_state.guideline = guideline


# Flexible Darstellung des Weiter-Buttons
st.markdown('<div class="centered-button red-button">', unsafe_allow_html=True)
if not st.session_state["weiter_geklickt"]:
    if st.button("Weiter"):
        if name.strip() and position.strip() and task.strip():
            handle_continue_click()
            st.rerun() # Wichtig, damit die Seite neu geladen und der untere Teil angezeigt wird
        else:
            st.markdown("""
            <div style="
                background-color: #fff8e1;
                border: 1px solid #d6b600;
                color: #3f4249;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                margin-top: 20px;
                text-align: center;
            ">
            Bitte fülle <strong>alle Felder</strong> aus, bevor du fortfährst.
            </div>
            """, unsafe_allow_html=True)
else:
    st.button("Weiter", disabled=True)

st.markdown('</div>', unsafe_allow_html=True)

# Display Datenschutz after generation of context and guideline
if st.session_state["ladephase_abgeschlossen"]:
    st.markdown("""
    <div style="
        background-color: white;
        border-radius: 12px;
        width: 100%;
        padding: 20px;
        margin-top: 40px;
    ">
        <h2 class="gema-subheadline">Datenschutz</h2>
        <p style="font-size: 18px; color: #3f4249;">
            Danke für diese Informationen. Wir nutzen diese Angaben, um die Fragen möglichst gut an dein Expertenthema anzupassen. Bevor wir starten können, benötigen wir deine Erlaubnis, dieses Interview zu transkribieren und die Inhalte weiterzuverwenden, um Wissensartikel daraus erstellen zu können. Wenn du damit einverstanden bist, klicke bitte auf "Zustimmen". Vielen Dank für deine Unterstützung!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="centered-button red-button" style="margin-top: -100vh; margin-bottom: 100vh;">', unsafe_allow_html=True)
    if st.button("Zustimmen"):
        st.switch_page("pages/userinterface_interview.py")
    st.markdown('</div>', unsafe_allow_html=True)