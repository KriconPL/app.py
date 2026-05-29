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
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0A1128 !important; 
    }
    [data-testid="stSidebar"] {
        background-color: #060B19 !important; 
    }
    [data-testid="stHeader"] {
        background-color: #0A1128 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #F8FAFC !important;
    }
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
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #172554 !important;
        border: 1px solid #1E3A8A !important;
    }
    div[data-baseweb="input"] input {
        color: #F97316 !important;
        font-weight: bold;
    }
    [data-testid="stToast"], div[data-testid="stNotification"] {
        background-color: #1E3A8A !important;
        color: white !important;
        border-left: 5px solid #F97316 !important;
    }
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
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #F97316 !important;
        color: #F97316 !important;
    }
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
    }
    .kricon-table tr:hover {
        background-color: #1E3A8A !important;
    }
    .trend-up { color: #4ADE80 !important; font-weight: bold; }
    .trend-down { color: #F87171 !important; font-weight: bold; }
    .trend-stable { color: #94A3B8 !important; font-weight: bold; }
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
