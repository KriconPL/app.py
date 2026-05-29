import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfiguracja i Jaśniejsza Szata Graficzna zgodna z brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# CSS dla jaśniejszej stylizacji brandingowej KriCon, loga i flag
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
    }
    
    /* Nagłówek H1 - Jaśniejszy Granat KriCon wewnątrz kontenera flex */
    .logo-title-container h1 {
        color: #1E3A8A !important; /* Jaśniejszy granat */
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin: 0 !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Pozostałe nagłówki - JAŚNIEJSZE */
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
    
    /* Oficjalny wynik - kolor Emergency z witryny KriCon (Wyróżniający) */
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
        color: #4B5563 !important; /* Szary */
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #3B82F6 !important;
        color: #1E3A8A !important;
    }

    /* Stylizacja flag w tekście */
    .flag-icon {
        font-size: 1.2em;
        margin-right: 8px;
        vertical-align: middle;
    }
    </style>
""", unsafe_allow_html=True)

# Stabilny URL loga Kricon Group (PNG)
KRICON_LOGO_URL_PNG = "https://kricongroup.com/wp-content/uploads/2021/04/kricon-logotype.png"

# Wyświetlanie Loga i Tytułu
st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            <img src="{KRICON_LOGO_URL_PNG}" alt="Kricon Group Logo" class="logo-image">
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# 2. Baza użytkowników
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Marcin": "marcin2026",
    "Kamil": "kamil2026", "Kuba M": "kubam2026", "Tomek": "tomek2026",
    "Kuba K": "kubak2026", "Rafał": "rafal2026", "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

# Oficjalny podział na grupy Mistrzostw Świata 2026 z DODANYMI FLAGAMI
GROUPS_DICT = {
    "Grupa A": ["🇲🇽 Meksyk", "🇿🇦 RPA", "🇰🇷 Korea Południowa", "🇨🇿 Czechy"],
    "Grupa B": ["🇨🇦 Kanada", "🇧🇦 Bośnia i Hercegowina", "🇶🇦 Katar", "🇨🇭 Szwajcaria"],
    "Grupa C": ["🇧🇷 Brazylia", "🇲🇦 Maroko", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Szkocja"],
    "Grupa D": ["🇺🇸 USA", "🇵🇾 Paragwaj", "🇦🇺 Australia", "🇹🇷 Turcja"],
    "Grupa E": ["🇩🇪 Niemcy", "🇨🇼 Curaçao", "🇨🇮 WKS", "🇪🇨 Ekwador"],
    "Grupa F": ["🇳🇱 Holandia", "🇯🇵 Japonia", "🇸🇪 Szwecja", "🇹🇳 Tunezja"],
    "Grupa G": ["🇧🇪 Belgia", "🇪🇬 Egipt", "🇮🇷 Iran", "🇳🇿 Nowa Zelandia"],
    "Grupa H": ["🇪🇸 Hiszpania", "🇨🇻 Wyspy Zielonego Przylądka
