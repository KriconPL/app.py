import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. Konfiguracja i Jaśniejsza Szata Graficzna zgodna z brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# Mapowanie Państw na Kody ISO (dla stabilnych flag PNG z flagcdn.com)
COUNTRY_FLAGS = {
    "Meksyk": "mx", "RPA": "za", "Korea Południowa": "kr", "Czechy": "cz",
    "Kanada": "ca", "Bośnia i Hercegowina": "ba", "Katar": "qa", "Szwajcaria": "ch",
    "Brazylia": "br", "Maroko": "ma", "Haiti": "ht", "Szkocja": "gb-sct",
    "USA": "us", "Paragwaj": "py", "Australia": "au", "Turcja": "tr",
    "Niemcy": "de", "Curaçao": "cw", "WKS": "ci", "Ekwador": "ec",
    "Holandia": "nl", "Japonia": "jp", "Szwecja": "se", "Tunezja": "tn",
    "Belgia": "be", "Egipt": "eg", "Iran": "ir", "Nowa Zelandia": "nz",
    "Hiszpania": "es", "Wyspy Zielonego Przylądka": "cv", "Arabia Saudyjska": "sa", "Urugwaj": "uy",
    "Francja": "fr", "Senegal": "sn", "Irak": "iq", "Norwegia": "no",
    "Argentyna": "ar", "Algieria": "dz", "Austria": "at", "Jordania": "jo",
    "Portugalia": "pt", "DR Konga": "cd", "Uzbekistan": "uz", "Kolumbia": "co",
    "Anglia": "gb-eng", "Chorwacja": "hr", "Ghana": "gh", "Panama": "pa",
    "TBD": "unknown" # flaga dla nieznanych drużyn
}

def get_flag_html(country_name):
    """Generuje kod HTML <img> dla flagi na podstawie nazwy państwa."""
    # Usuwa emotikony, jeśli zostały w nazwie z poprzednich wersji
    clean_name = country_name.replace("🏳️", "").strip()
    code = COUNTRY_FLAGS.get(clean_name, "unknown")
    if code == "unknown":
         return f'<span style="font-size:1.2em; margin-right:8px;">🏳️</span> {country_name}'
    
    flag_url = f"https://flagcdn.com/w40/{code}.png"
    return f'<img src="{flag_url}" width="25" style="vertical-align: middle; margin-right: 10px; border: 1px solid #ddd; border-radius:2px;" alt="flaga {country_name}"> {country_name}'

# CSS dla jaśniejszej stylizacji brandingowej KriCon i loga
st.markdown("""
    <style>
    /* Tło główne i kontenerów - JAŚNIEJSZE */
    .reportview-container, .main .block-container { background: #FFFFFF; color: #1F2937; }
    .main .block-container { padding-top: 1rem; }
    
    /* Kontener loga i tytułu */
    .logo-title-container {
        display: flex;
        align-items: center;
        border-bottom: 4px solid #3B82F6; /* Jaśniejszy niebieski akcent */
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .logo-container {
        margin-right: 20px;
    }
    .logo-image {
        max-height: 80px;
        width: auto;
    }
    
    /* Nagłówek H1 */
    .logo-title-container h1 {
        color: #1E3A8A !important; /* Jaśniejszy granat */
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin: 0 !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Pozostałe nagłówki */
    h2, h3 { 
        color: #1E3A8A !important;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Przyciski w kolorystyce KriCon (Jaśniejszy Niebieski) */
    .stButton>button {
        background-color: #3B82F6 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
        transform: translateY(-1px);
    }
    
    /* Komunikaty i notyfikacje */
    div[data-testid="stNotification"] {
        background-color: #EFF6FF !important;
        color: #1E3A8A !important;
        border-left: 5px solid #3B82F6 !important;
        border-radius: 4px;
    }
    
    /* Oficjalny wynik */
    .real-score { 
        font-size: 1.3rem; 
        color: #EF4444; /* Emergency Red */
        font-weight: bold; 
        background-color: #FEF2F2;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* Zakładki (Tabs) dopasowane do stylu */
    .stTabs [data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #3B82F6 !important;
        color: #1E3A8A !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Wyświetlanie Loga i Tytułu (Ładowanie lokalne dla stabilności)
# ⚠️ UWAGA: Umieść plik 'logo.png' w tym samym folderze co app.py
LOCAL_LOGO_PATH = "./logo.png"

logo_html = ""
if os.path.exists(LOCAL_LOGO_PATH):
    # Streamlit potrafi interpretować lokalne ścieżki w st.image, ale w HTML musimy użyć triku base64
    # Dla uproszczenia wewnątrz markdown, załadujemy je standardowo, jeśli Streamlit je obsłuży,
    # lub wyświetlimy sam tytuł, jeśli pliku brak.
    logo_html = f'<img src="{LOCAL_LOGO_PATH}" alt="Kricon Group Logo" class="logo-image">'
else:
    # Ostrzeżenie dla administratora (widoczne tylko w logach lub jeśli dodasz st.warning)
    print(f"OSTRZEŻENIE: Nie znaleziono pliku loga pod ścieżką: {LOCAL_LOGO_PATH}")
    logo_html = '<span style="font-size:2em; margin-right:15px;">🌐</span>' # Placeholder

st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            {logo_html}
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# 3. Baza użytkowników
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Marcin": "marcin2026",
    "Kamil": "kamil2026", "Kuba M": "kubam2026", "Tomek": "tomek2026",
    "Kuba K": "kubak2026", "Rafał": "rafal2026", "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

# Oficjalny podział na grupy Mistrzostw Świata 2026 (Czyste nazwy, flagi PNG dodawane dynamicznie)
GROUPS_DICT = {
    "Grupa A": ["Meksyk", "RPA", "Korea Południowa", "Czechy"],
    "Grupa B": ["Kanada", "Bośnia i Hercegowina", "Katar", "Szwajcaria"],
    "Grupa C": ["Brazylia", "Maroko", "Haiti", "Szkocja"],
    "Grupa D": ["USA", "Paragwaj", "Australia", "Turcja"],
    "Grupa E": ["Niemcy", "Curaçao", "WKS", "Ekwador"],
    "Grupa F": ["Holandia", "Japonia", "Szwecja", "Tunezja"],
    "Grupa G": ["Belgia", "Egipt", "Iran", "Nowa Zelandia"],
    "Grupa H": ["Hiszpania", "Wyspy Zielonego Przylądka", "Arabia Saudyjska", "Urugwaj"],
    "Grupa I": ["Francja", "Senegal", "Irak", "Norwegia"],
    "Grupa J": ["Argentyna", "Algieria", "Austria", "Jordania"],
    "Grupa K": ["Portugalia", "DR Konga", "Uzbekistan", "Kolumbia"],
    "Grupa L": ["Anglia", "Chorwacja", "Ghana", "Panama"]
}

# 4. Generator Harmonogramu 104 Meczów z Oficjalnymi Ramami Datowymi
def generate_schedule():
    schedule = {}
    match_id = 1
    
    # Faza grupowa: 11 - 27 Czerwca
    dates_group = [f"{d} Czerwca" for d in range(11, 28)]
    
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    date_idx = 0
    
    # Faza Grupowa (72 mecze przy 12 grupach)
    for m_round in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1_idx, t2_idx = matchups[m_round]
            schedule[match_id] = {
                "date": dates_group[date_idx % len(dates_group)],
                "stage": group_name,
                "home": teams[t1_idx], "away": teams[t2_idx],
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            if match_id % 4 == 0: date_idx += 1

    # Oficjalne ramy czasowe fazy pucharowej MŚ 2026
    ko_stages = [
        ("1/16 Finału", 16, ["28 Czerwca", "29 Czerwca", "30 Czerwca", "1 Lipca", "2 Lipca", "3 Lipca"]), 
        ("1/8 Finału", 8, ["4 Lipca", "5 Lipca", "6 Lipca", "7 Lipca"]), 
        ("Ćwierćfinały", 4, ["9 Lipca", "10 Lipca", "11 Lipca"]), 
        ("Półfinały", 2, ["14 Lipca", "15 Lipca"]), 
        ("Mecz o 3. miejsce", 1, ["18 Lipca"]), 
        ("Finał", 1, ["19 Lipca"])
    ]
    
    for stage_name, count, stage_dates in ko_stages:
        d_idx = 0
        for _ in range(count):
            schedule[match_id] = {
                "date": stage_dates[d_idx % len(stage_dates)],
                "stage": stage_name,
                "home": "TBD", "away": "TBD", # dynamiczne flagi obsłużą brak kodu
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            d_idx += 1
            
    return schedule

# Inicjalizacja bezpieczna
if 'results' not in st.session_state or "date" not in st.session_state.results.get(1, {}):
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state or len(st.session_state.bets) < 100:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

all_dates = []
for m in st.session_state.results.values():
    if m["date"] not in all_dates:
        all_dates.append(m["date"])

def calculate_points(pred_h, pred_a, real_h, real_a):
    if real_h is None or real_a is None or pred_h is None or pred_a is None:
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

# 5. System Logowania
if 'logged_in_user' not in st.session_state:
