import streamlit as st
import json
from logic.regeln import lade_regeln, pruefe_filter, berechne_score

def lade_produkte():
    with open("data/produkte.json", "r") as f:
        return json.load(f)

# Modernes App-Style CSS + HDI-Label-Farben
st.markdown("""
<style>

body, .stApp {
    background-color: #F7F9FA !important;
    font-family: "Inter", sans-serif;
    color: #1A1A1A;
}

h1, h2, h3, h4 {
    font-weight: 700;
    color: #0A5C36;
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #0A5C36 !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
}

.stButton>button {
    background: linear-gradient(135deg, #0A8F4A, #0A6F3A);
    color: white !important;
    border-radius: 12px;
    padding: 0.8em 1.4em;
    font-size: 1.1rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: 0.2s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #0A6F3A, #0A5C36);
    transform: translateY(-2px);
}

.produkt-card {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #E5E8EB;
}

.score-badge {
    background-color: #0A8F4A;
    color: white;
    padding: 0.35rem 0.7rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    margin-left: 0.5rem;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 1.2rem;
    margin-bottom: 0.4rem;
    color: #0A6F3A;
    display: flex;
    align-items: center;
    gap: 6px;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 20px;
    margin-bottom: 0.5rem;
}

.info-item {
    font-size: 0.95rem;
    padding: 4px 0;
}

.info-label {
    font-weight: 600;
    color: #333;
}

</style>
""", unsafe_allow_html=True)

# HDI Logo
st.image("logo.png", width=180)
st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

st.title("Versicherungsempfehler – Prototyp")
st.header("Profil eingeben")

beruf = st.text_input("Beruf")
alter = st.number_input("Alter", min_value=18, max_value=70, step=1)
rente = st.number_input("Gewünschte BU-Rente", min_value=500, max_value=5000, step=100)

schicht = st.selectbox("Schicht", ["egal", "1", "2", "3"])
typ = st.selectbox("Produkt-Typ", ["egal", "SBU", "BUZ-B", "BUZ-BR"])


def render_produktkarte(p, score):
    info = p.get("info", {})

    def row(label, value):
        if value in [None, "", "null"]:
            return ""
        return f'<div class="info-item"><span class="info-label">{label}:</span> {value}</div>'

    # Keys mit Bindestrich vorher extrahieren
    hv_airbag = info.get("hv-airbag")
    freie_phase = info.get("freie_phase")
    gebundene_phase = info.get("gebundene_phase")
    karriereplus = info.get("karriereplus")

    html = f'''
<div class="produkt-card">
<h3>{p['name']} <span class="score-badge">{score}</span></h3>

<div class="section-title"><span>📦</span><span>Leistungsumfang</span></div>
<div class="info-grid">
{row("Leistung", info.get("leistungsumfang"))}
{row("Max. Rente", info.get("max_rente_display") or p["matching"].get("max_rente"))}
</div>

<div class="section-title"><span>⚙️</span><span>Konditionen</span></div>
<div class="info-grid">
{row("Abkommensnummer", info.get("abkommensnummer"))}
{row("Wartezeit", info.get("wartezeit"))}
{row("Gesundheitserklärung", info.get("gesundheitserklärung"))}
{row("Beitragsdynamik", info.get("beitragsdynamik"))}
</div>

<div class="section-title"><span>✨</span><span>Besondere Merkmale</span></div>
<div class="info-grid">
{row("HV-Airbag", hv_airbag)}
{row("Freie Phase", freie_phase)}
{row("Gebundene Phase", gebundene_phase)}
{row("KarrierePlus", karriereplus)}
</div>

</div>
'''

    st.markdown(html, unsafe_allow_html=True)


if st.button("Empfehlung anzeigen"):
    profil = {
        "beruf": beruf,
        "alter": alter,
        "wuensche_rente": rente,
        "schicht": schicht,
        "typ": typ
    }

    produkte = lade_produkte()
    regeln = lade_regeln()

    ergebnisse = []

    for produkt in produkte:
        if all(pruefe_filter(regel, produkt, profil) for regel in regeln["filter"]):
            score = sum(berechne_score(regel, produkt, profil) for regel in regeln["scoring"])
            ergebnisse.append({"produkt": produkt, "score": score})

    ergebnisse.sort(key=lambda x: x["score"], reverse=True)

    st.header("Empfohlene Produkte")

    if not ergebnisse:
        st.warning("Keine passenden Produkte gefunden.")
    else:
        for eintrag in ergebnisse:
            render_produktkarte(eintrag["produkt"], eintrag["score"])
