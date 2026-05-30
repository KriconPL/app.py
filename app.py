import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import json 
import requests 
import re
from datetime import datetime, timedelta

# 1. Konfiguracja aplikacji i Szata Graficzna Dark Navy & Orange
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# GLOBALNE PROFILE I CONFIG
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

VENUES_LIST = [
    "Azteca, Meksyk", "MetLife, Nowy Jork", "SoFi, Los Angeles", "AT&T, Dallas",
    "Mercedes-Benz, Atlanta", "BC Place, Vancouver", "Hard Rock, Miami", "Arrowhead, Kansas City",
    "Lincoln Financial, Filadelfia", "Levi's, San Francisco", "Lumen Field, Seattle", "NRG, Houston",
    "Gillette, Boston", "BMO Field, Toronto", "BBVA, Monterrey", "Akron, Guadalajara"
]

# SYSTEM CAŁKOWITEGO WYRÓWNANIA POZIOMEGO CSS
st.markdown("""
    <script>
    document.addEventListener('contextmenu', function(e) { e.preventDefault(); });
    document.addEventListener('keydown', function(e) {
        if (e.keyCode == 123 || (e.ctrlKey && e.shiftKey && e.keyCode == 73) || (e.ctrlKey && e.keyCode == 85) || (e.ctrlKey && e.keyCode == 83) || (e.ctrlKey && e.keyCode == 67)) {
            e.preventDefault();
            return false;
        }
    });
    </script>
    <style>
    body, html, [data-testid="stAppViewContainer"], .stApp {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
    }
    html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stTabContent"], div.stTabs {
        background-color: #0A1128 !important; 
        overflow-y: auto !important;
        overflow-x: auto !important;
    }
    [data-testid="stSidebar"] { background-color: #060B19 !important; }
    [data-testid="stHeader"] { background-color: #0A1128 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #F8FAFC !important; }
    
    @keyframes pulseAlertCore {
        0% { opacity: 1.0; }
        50% { opacity: 0.2; }
        100% { opacity: 1.0; }
    }
    
    .missing-bet-banner-blink {
        animation: pulseAlertCore 1.2s infinite ease-in-out !important;
        background-color: #DC2626 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 30px !important;
        line-height: 30px !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        padding: 0 10px !important;
        white-space: nowrap !important;
        display: inline-block !important;
    }
    
    .status-waiting-blink {
        animation: pulseAlertCore 2.0s infinite ease-in-out !important;
        background-color: #D97706 !important;
        color: #FFFFFF !important;
        padding: 1px 5px !important;
        border-radius: 4px !important;
    }
    
    .success-bet-banner {
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 30px !important;
        line-height: 30px !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        display: inline-block !important;
        padding: 0 12px !important;
        white-space: nowrap;
    }
    
    .meta-upper-container {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.75rem !important;
        color: #64748B !important;
        margin-top: 8px !important;
        margin-bottom: 2px !important;
        padding-left: 6px;
    }
    .meta-id-text-clean { font-weight: bold; color: #F97316 !important; }
    .meta-badge-clean { color: #94A3B8 !important; background-color: #1E293B; padding: 0px 4px; border-radius: 3px; }
    .meta-venue-clean { color: #38BDF8 !important; background-color: #0B1329; padding: 0px 4px; border-radius: 3px; }
    
    .match-card-clean {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important; 
        border-radius: 4px; 
        padding: 8px 12px !important; 
        margin-bottom: 4px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    .team-text-align-right { font-size: 1.1rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; height: 30px; line-height: 30px; }
    .team-text-align-left { font-size: 1.1rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; height: 30px; line-height: 30px; }
    
    .official-score-subtle {
        font-size: 0.85rem !important;
        font-weight: bold !important;
        color: #94A3B8 !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 4px;
        display: inline-block;
        text-align: center;
        white-space: nowrap;
        height: 30px !important;
        line-height: 30px !important;
        padding: 0 10px !important;
        width: 100%;
    }
    
    div.stNumberInput { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    div.stNumberInput input { text-align: center !important; background-color: #0A1128 !important; color: #F8FAFC !important; height: 30px !important; font-size: 0.95rem !important; font-weight: bold !important; border: 1px solid #1E3A8A !important; }
    div.stNumberInput button { height: 30px !important; width: 22px !important; background-color: #1E293B !important; color: #F97316 !important; }
    
    /* --- AGRESYWNY FIX KOLORU POMARAŃCZOWEGO DLA PRZYCISKU ZAPISZ --- */
    div.stButton button, div[data-testid="stBlock"] button {
        background-color: #F97316 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px !important; 
        border: 1px solid #EA580C !important; 
        font-weight: bold !important; 
        height: 30px !important; 
        line-height: 28px !important; 
        padding: 0 14px !important; 
        font-size: 0.85rem !important; 
        width: 100% !important;
        display: inline-block !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    div.stButton button:hover {
        background-color: #EA580C !important;
        border-color: #C2410C !important;
    }
    
    .kricon-table { width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }
    .kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; }
    .kricon-table td { padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; }
    .flag-img { width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; display: inline-block; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# MAPOWANIE KODÓW ISO
ISO_FLAGS_MAP = {
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
    "Anglia": "gb-eng", "Chorwacja": "hr", "Ghana": "gh", "Panama": "pa"
}

def clean_and_sanitize_team_string(raw_name):
    if not raw_name or raw_name == "TBD": return "TBD"
    s = str(raw_name).strip()
    s = re.sub(r'[^\w\s\-ąęćłńóśźżĄĘĆŁŃÓŚŹŻ]', '', s)
    return s.strip()

def get_cdn_flag_img_html(team_name):
    c_name = clean_and_sanitize_team_string(team_name)
    code = ISO_FLAGS_MAP.get(c_name, None)
    if code:
        return f'<img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.6/flags/4x3/{code}.svg" class="flag-img" />'
    return f'<span style="font-size:1rem; margin-right:4px;">🌐</span>'

def calculate_points(pred_h, pred_a, real_h, real_a):
    try:
        if real_h is None or real_a is None or pred_h is None or pred_a is None: return 0
        if int(pred_h) == int(real_h) and int(pred_a) == int(real_a): return 3
        if np.sign(int(pred_h) - int(pred_a)) == np.sign(int(real_h) - int(real_a)): return 1
    except (ValueError, TypeError): pass
    return 0

def render_leaderboard_html(now_time):
    scores = {p: 0 for p in players}
    if 'results' in st.session_state and 'bets' in st.session_state:
        for m_id, res in st.session_state.results.items():
            if res.get('status') == "Zakończony":
                for p in players:
                    if m_id in st.session_state.bets and p in st.session_state.bets[m_id]:
                        scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res.get('score_h'), res.get('score_a'))
    df = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"]).sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    rows = ""
    for idx, row in df.iterrows():
        rows += f"<tr><td><b>{idx+1}</b></td><td>{row['Gracz']}</td><td><b>{row['Punkty']} pkt</b></td></tr>"
    return f"<table class='kricon-table'><tr><th>Msc.</th><th>Gracz</th><th>Punkty</th></tr>{rows}</table>"

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    raw_fixtures = [
        (2026, 6, 11, 21, 0, "Grupa A", "Meksyk", "RPA"), (2026, 6, 12, 4, 0, "Grupa A", "Korea Południowa", "Czechy"),
        (2026, 6, 12, 21, 0, "Grupa B", "Kanada", "Bośnia i Hercegowina"), (2026, 6, 13, 3, 0, "Grupa D", "USA", "Paragwaj")
    ]
    match_id = 1
    for yr, mo, dy, hr, mn, stage, home, away in raw_fixtures:
        dt = datetime(yr, mo, dy, hr, mn)
        schedule[match_id] = {
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]} o {dt.strftime('%H:%M')}",
            "stage": stage, "home": home, "away": away, "score_h": None, "score_a": None, "status": "Oczekuje",
            "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
        }
        match_id += 1
    return schedule

if 'results' not in st.session_state: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

now = datetime.now()

# LOGOWANIE
if st.session_state.logged_in_user is None:
    user = st.selectbox("Wybierz użytkownika:", list(USER_CREDENTIALS.keys()))
    pw = st.text_input("Wpisz hasło:", type="password")
    if st.button("Zaloguj się"):
        if USER_CREDENTIALS.get(user) == pw: 
            st.session_state.logged_in_user = user
            st.rerun()
else:
    tab1, tab2 = st.tabs(["📊 Ranking", "📅 Terminarz"])
    with tab1: st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
    with tab2:
        for m_id, m in sorted(st.session_state.results.items()):
            status_html = '<span class="status-waiting-blink">🟡 Oczekuje</span>'
            oficjalny_wynik_tekst = f"Wynik: {m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}"
            
            has_existing_bet = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user) is not None
            cur_h, cur_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            # Pasek górny informacyjny
            st.markdown(f"""
            <div class="meta-upper-container">
                <span class="meta-id-text-clean">⚽ Mecz #{m_id}</span>
                {status_html}
                <span class="meta-badge-clean">📅 {m['date']}</span>
                <span class="meta-venue-clean">📍 {m.get('venue')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # KARTA MECZOWA - IDEALNY UKŁAD 6 POZIOMYCH KOLUMN
            st.markdown("<div class='match-card-clean'>", unsafe_allow_html=True)
            c1, c2, c3, c4, c5, c6 = st.columns([2.0, 0.5, 0.5, 2.0, 1.2, 1.0])
            
            with c1:
                st.markdown(f"<div class='team-text-align-right'><span>{m['home']}</span> {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
            with c2:
                b_h = st.number_input(f"H_{m_id}", 0, 20, int(cur_h), 1, key=f"h_{m_id}", label_visibility="collapsed")
            with c3:
                b_a = st.number_input(f"A_{m_id}", 0, 20, int(cur_a), 1, key=f"a_{m_id}", label_visibility="collapsed")
            with c4:
                st.markdown(f"<div class='team-text-align-left'>{get_cdn_flag_img_html(m['away'])} <span>{m['away']}</span></div>", unsafe_allow_html=True)
            with c5:
                st.markdown(f"<span class='official-score-subtle'>{oficjalny_wynik_tekst}</span>", unsafe_allow_html=True)
            with c6:
                if st.button("Zapisz", key=f"save_{m_id}"):
                    st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                    st.rerun()
                
                if has_existing_bet:
                    st.markdown("<div class='success-bet-banner'>✔ OK</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='missing-bet-banner-blink'>⚠️ BRAK</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
