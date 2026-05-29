import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. Konfiguracja i Szata Graficzna zgodna z brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# CSS dla jaśniejszej stylizacji brandingowej KriCon i elementów interfejsu
st.markdown("""
    <style>
    /* Tło główne i kontenerów */
    .reportview-container, .main .block-container { 
        background: #FFFFFF; 
        color: #1F2937; 
    }
    .main .block-container { padding-top: 1rem; }
    
    /* Kontener loga i tytułu */
    .logo-title-container {
        display: flex;
        align-items: center;
        border-bottom: 4px solid #3B82F6;
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
        color: #1E3A8A !important;
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
    
    /* Przyciski w kolorystyce KriCon */
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
        color: #EF4444; 
        font-weight: bold; 
        background-color: #FEF2F2;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* Zakładki (Tabs) */
    .stTabs [data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #3B82F6 !important;
        color: #1E3A8A !important;
    }

    /* Stylizacja tabel HTML */
    .kricon-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 1rem;
        min-width: 400px;
    }
    .kricon-table th {
        background-color: #1E3A8A;
        color: white;
        text-align: left;
        padding: 12px;
        font-weight: 600;
    }
    .kricon-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #E5E7EB;
    }
    .kricon-table tr:hover {
        background-color: #F8FAFC;
    }
    </style>
""", unsafe_allow_html=True)

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
    "TBD": "unknown"
}

def get_flag_html(country_name):
    """Generuje kod HTML dla flagi na podstawie nazwy państwa."""
    clean_name = country_name.replace("🏳️", "").strip()
    code = COUNTRY_FLAGS.get(clean_name, "unknown")
    if code == "unknown":
        return f'<span style="font-size:1.2em; margin-right:8px;">🏳️</span> {country_name}'
    flag_url = f"https://flagcdn.com/w40/{code}.png"
    return f'<img src="{flag_url}" width="25" style="vertical-align: middle; margin-right: 10px; border: 1px solid #ddd; border-radius:2px;" alt="flaga"> {country_name}'

# 2. Wyświetlanie Loga i Tytułu
LOCAL_LOGO_PATH = "./logo.png"
if os.path.exists(LOCAL_LOGO_PATH):
    logo_html = f'<img src="{LOCAL_LOGO_PATH}" alt="Kricon Group Logo" class="logo-image">'
else:
    logo_html = '<span style="font-size:2em; margin-right:15px;">🌐</span>'

st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            {logo_html}
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# Baza użytkowników
USER_CREDENTIALS = {
    "Adam": "adam2026",
    "Maciej": "maciej2026",
    "Marcin": "marcin2026",
    "Kamil": "kamil2026",
    "Kuba M": "kubam2026",
    "Tomek": "tomek2026",
    "Kuba K": "kubak2026",
    "Rafał": "rafal2026",
    "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

# Oficjalny podział na grupy
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

# 3. Generator Harmonogramu
def generate_schedule():
    schedule = {}
    match_id =
