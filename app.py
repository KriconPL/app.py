import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from datetime import datetime, timedelta

# 1. Konfiguracja aplikacji i Szata Graficzna Dark Navy & Orange
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    /* Wymuszenie ciemnego tła dla całej aplikacji Streamlit */
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0A1128 !important; 
    }
    [data-testid="stSidebar"] {
        background-color: #060B19 !important; 
    }
    [data-testid="stHeader"] {
        background-color: #0A1128 !important;
    }
    
    /* Kolor tekstów globalnych */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #F8FAFC !important;
    }

    /* Kontener loga i tytułu */
    .logo-title-container {
        display: flex;
        align-items: center;
        border-bottom: 3px solid #F97316 !important; 
        padding-bottom: 15px;
        margin-bottom: 25px;
        background-color: #0A1128;
    }
    .logo-container {
        margin-right: 25px;
        background-color: white; 
        padding: 10px 20px;
        border-radius: 8px;
    }
    .logo-image {
        max-height: 80px;
        width: auto;
        object-fit: contain;
    }
    
    .logo-title-container h1 {
        margin: 0 !important;
        border: none !important;
        padding: 0 0 0 15px !important;
        font-size: 2.5rem;
    }
    
    /* Przyciski w kolorystyce KriCon Orange */
    .stButton>button {
        background-color: #F97316 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #EA580C !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(249, 115, 22, 0.4);
    }
    
    /* Inputy numerów (Typy) */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #172554 !important;
        border: 1px solid #1E3A8A !important;
    }
    div[data-baseweb="input"] input {
        color: #F97316 !important;
        font-weight: bold;
    }

    /* Powiadomienia (Toasty / Pop-upy) */
    [data-testid="stToast"], div[data-testid="stNotification"] {
        background-color: #1E3A8A !important;
        color: white !important;
        border-left: 5px solid #F97316 !important;
    }
    
    /* Karty meczów */
    .match-container {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .match-header {
        color: #F97316 !important;
        margin-bottom: 10px;
        font-size: 1.4rem;
        font-weight: 700;
        border-bottom: 1px solid #1E3A8A;
        padding-bottom: 10px;
    }
    .real-score { 
        font-size: 1.3rem; 
        color: #0A1128 !important; 
        font-weight: bold; 
        background-color: #F97316 !important;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 10px;
    }
    
    /* Zakładki (Tabs) */
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #F97316 !important;
        color: #F97316 !important;
    }

    /* Tabele HTML */
    .kricon-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 35px 0;
        font-size: 0.95rem;
        background-color: #172554 !important;
        border-radius: 8px;
        overflow: hidden;
    }
    .kricon-table th {
        background-color: #F97316 !important; 
        color: #0A1128 !important;
        text-align: left;
        padding: 12px;
        font-weight: 800;
    }
    .kricon-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #1E3A8A !important;
        color: #F8FAFC !important;
        vertical-align: middle;
    }
    .kricon-table tr:hover {
        background-color: #1E3A8A !important;
    }
    
    /* Nowe, zaawansowane style wskaźników trendu */
    .badge-trend {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .trend-box-up { background-color: #16A34A; color: white; }
    .trend-box-down { background-color: #DC2626; color: white; }
    .trend-box-stable { background-color: #374151; color: #94A3B8; }
    </style>
""", unsafe_allow_html=True)

# Funkcja odczytująca zdjęcie jako Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

LOCAL_LOGO_PATH = "logo.png"
logo_base64 = get_base64_of_bin_file(LOCAL_LOGO_PATH)

if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Kricon Group Logo" class="logo-image">'
else:
    logo_html = f'<img src="https://kricongroup.com/wp-content/uploads/2021/04/kricon-logotype.png" alt="Kricon Group Logo" class="logo-image">'

st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            {logo_html}
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# Flagi PNG
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
    "TBD": "unknown"
}

def get_flag_html(country_name):
    clean_name = country_name.replace("🏳️", "").strip()
    code = COUNTRY_FLAGS.get(clean_name, "unknown")
    if code == "unknown":
        return f'<span style="font-size:1.2em; margin-right:8px;">🏳️</span> {country_name}'
    flag_url = f"https://flagcdn.com/w40/{code}.png"
    return f'<img src="{flag_url}" width="22" style="vertical-align: middle; margin-right: 8px; border: 1px solid #1E3A8A; border-radius:2px;" alt="flaga"> {country_name}'

# Baza użytkowników
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Marcin": "marcin2026",
    "Kamil": "kamil2026", "Kuba M": "kubam2026", "Tomek": "tomek2026",
    "Kuba K": "kubak2026", "Rafał": "rafal2026", "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

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

# Generator Harmonogramu 104 Meczów
def generate_schedule():
    schedule = {}
    match_id = 1
    months_pl = {6: "Czerwca", 7: "Lipca"}
    
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    group_matches = []
    
    for round_idx in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1, t2 = matchups[round_idx]
            group_matches.append({"stage": group_name, "home": teams[t1], "away": teams[t2]})
            
    start_date = datetime(2026, 6, 11)
    times = [15, 18, 21, 23] 
    
    for i, match in enumerate(group_matches):
        day_offset = i // 4
        time_idx = i % 4
        match_dt = start_date + timedelta(days=day_offset)
        match_dt = match_dt.replace(hour=times[time_idx], minute=0, second=0)
        
        schedule[match_id] = {
            "timestamp": match_dt,
            "date": f"{match_dt.day} {months_pl[match_dt.month]}",
            "time": match_dt.strftime("%H:%00"),
            "stage": match["stage"],
            "home": match["home"], "away": match["away"],
            "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1

    ko_stages = [
        ("1/16 Finału", 16, [(29,6), (30,6), (1,7), (2,7)]), 
        ("1/8 Finału", 8, [(4,7), (5,7), (6,7), (7,7)]),     
        ("Ćwierćfinały", 4, [(9,7), (10,7)]),                
        ("Półfinały", 2, [(14,7), (15,7)]),                  
        ("Mecz o 3. miejsce", 1, [(18,7)]),                  
        ("Finał", 1, [(19,7)])                               
    ]
    
    for stage_name, count, stage_dates in ko_stages:
        date_idx = 0
        matches_per_date = count // len(stage_dates) if len(stage_dates) > 0 else 1
        matches_per_date = max(1, matches_per_date)
        for i in range(count):
            d, m_num = stage_dates[date_idx % len(stage_dates)]
            hour = 18 if i % 2 == 0 else 21
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            
            schedule[match_id] = {
                "timestamp": match_dt,
                "date": f"{d} {months_pl[m_num]}",
                "time": match_dt.strftime("%H:%00"),
                "stage": stage_name,
                "home": "TBD", "away": "TBD",
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            if (i + 1) % matches_per_date == 0:
                date_idx += 1
            
    return schedule

if 'results' not in st.session_state or len(st.session_state.results) != 104:
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state or len(st.session_state.bets) != 104:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

if 'last_positions' not in st.session_state:
    st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(
