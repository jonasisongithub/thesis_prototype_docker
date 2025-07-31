import streamlit as st # type: ignore
import base64
import streamlit.components.v1 as components # type: ignore

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
logo_base64 = get_base64_image("./pages/images/logo_gema.jpg")  # <-- LOGO hier laden

# CSS-Hintergrund anwenden
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
    </style>

    <div class="logo-container">
        <img src="data:image/jpg;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# HTML-Inhalt mit korrektem Styling
components.html(
    f"""
    <div style="
        font-family: 'Segoe UI', sans-serif;
        color: #3f4249;
        font-size: 7vh;
        padding-left: 0vw;
        padding-top: 0vh;
        margin: 0;
        ">
        <h1 style="margin: 0;">GEMA Knowledge Share</h1>
    </div>

    <div style="
        background-color: white;
        width: 100%;
        margin-left: 0vw;
        margin-top: 4vh;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #222;
        ">
        
        <p><strong>Willkommen zum Experteninterview-Tool</strong></p>

        <p>Danke, dass du dir Zeit nimmst und dein Wissen teilst – Dieses ist für uns von unschätzbarem Wert!<br>
        Dieses Tool unterstützt dich dabei, dein Fachwissen einfach und strukturiert weiterzugeben. Ziel ist es, wertvolles Erfahrungswissen von Mitarbeitenden wie dir zu erfassen, zu dokumentieren und für andere Kolleginnen und Kollegen zugänglich zu machen.</p>

        <p>Ob Methoden, Prozesse, Tipps aus der Praxis oder spezielle Fachkenntnisse – dein Beitrag hilft, unser gemeinsames Wissen nachhaltig zu sichern und die Zusammenarbeit zu stärken.</p>

        <p><strong>Los geht’s – dein Wissen zählt!</strong></p>
    </div>
    """,
    height=600,
)
# Abstand zum weißen Kasten
st.markdown("<div style='height: -35vh;'></div>", unsafe_allow_html=True)

# Button CSS & HTML
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: -15vh;
        margin-bottom: 100vh;
    }

    .start-link-button {
        font-family: 'Segoe UI', sans-serif;
        background-color: #cc0000;
        color: white !important;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 20px;
        height: 7vh;
        width: 12vw;
        display: flex;
        justify-content: center;
        align-items: center;
        text-decoration: none !important;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .start-link-button:hover {
        background-color: #a30000;
        transform: scale(1.03);
    }
    </style>

    <div class="button-container">
        <a href="/userinterface_aboutyou" class="start-link-button">Interview starten</a>
    </div>
""", unsafe_allow_html=True)
