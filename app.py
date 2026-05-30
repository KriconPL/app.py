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

# ARCHITEKTURA STYLÓW CSS DLA ULTRA-PŁASKIEGO RZĘDU I IDEALNEJ LINII HORIZONTALNEJ
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
        height: 28px !important;
        line-height: 28px !important;
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
        font-weight: bold !important;
        font-size: 0.65rem !important;
    }
    
    .success-bet-banner {
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 28px !important;
        line-height: 28px !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        display: inline-block !important;
        padding: 0 10px !important;
        white-space: nowrap;
    }
    
    .meta-upper-container {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.75rem !important;
        color: #64748B !important;
        margin-top: 6px !important;
        margin-bottom: 2px !important;
        padding-left: 6px;
    }
    .meta-id-text-clean { font-weight: bold; color: #F97316 !important; }
    .meta-badge-clean { color: #94A3B8 !important; background-color: #1E293B; padding: 0px 4px; border-radius: 3px; }
    .meta-venue-clean { color: #38BDF8 !important; background-color: #0B1329; padding: 0px 4px; border-radius: 3px; }
    
    /* ULTRA-PŁASKI BOX MECZOWY */
    .match-card-clean {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important; 
        border-radius: 4px; 
        padding: 4px 12px !important; 
        margin-bottom: 2px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        width: 100%;
    }
    
    .team-text-align-right { font-size: 1.05rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; }
    .team-text-align-left { font-size: 1.05rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; }
    
    .official-score-subtle {
        font-size: 0.8rem !important;
        font-weight: bold !important;
        color: #94A3B8 !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 4px;
        display: inline-block;
        text-align: center;
        white-space: nowrap;
        height: 28px !important;
        line-height: 28px !important;
        padding: 0 8px !important;
    }
    
    /* --- INTEGRALNY MECHANIZM STEPPERÓW W JEDNEJ LINII POZIOMEJ (FLEXBOX DESIGN) --- */
    .stepper-row-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        width: 100%;
        height: 28px;
    }
    .stepper-digit {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: #F8FAFC !important;
        min-width: 16px;
        text-align: center;
    }
    .stepper-separator {
        font-weight: bold;
        color: #F97316 !important;
        padding: 0 4px;
        font-size: 1.1rem;
    }
    
    /* MODYFIKACJA INTERFEJSU PRZYCISKÓW STREAMLIT DLA POZIOMEGO STEPPERA OBOK CYFR */
    div.stButton button, div[data-testid="stBlock"] button {
        background-color: #F97316 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px !important; 
        border: 1px solid #EA580C !important; 
        font-weight: bold !important; 
        height: 28px !important; 
        line-height: 26px !important; 
        padding: 0 12px !important; 
        font-size: 0.85rem !important; 
        width: 100% !important;
        display: inline-block !important;
    }
    div.stButton button:hover { background-color: #EA580C !important; }
    
    /* MINI PRZYCISKI PLUS I MINUS DOPASOWANE DO WYSOKOŚCI TEKSTU */
    .stepper-mini-btn button {
        background-color: #1E293B !important;
        color: #F97316 !important;
        border: 1px solid #334155 !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        height: 26px !important;
        line-height: 24px !important;
        width: 26px !important;
        padding: 0 !important;
    }
    .stepper-mini-btn button:hover { background-color: #334155 !important; color: #FFFFFF !important; }
    
    /* STYLIZACJA WIERSZY PODIUM DLA RANKINGU GRACZY */
    .gold-medal-row { background-color: rgba(254, 240, 138, 0.95) !important; font-weight: bold; }
    .gold-medal-row td, .gold-medal-row b { color: #0A1128 !important; }
    .silver-medal-row { background-color: rgba(226, 232, 240, 0.95) !important; font-weight: bold; }
    .silver-medal-row td, .silver-medal-row b { color: #0A1128 !important; }
    .bronze-medal-row { background-color: rgba(254, 215, 170, 0.95) !important; font-weight: bold; }
    .bronze-medal-row td, .bronze-medal-row b { color: #0A1128 !important; }
    
    .trend-up { color: #16A34A !important; font-weight: bold; }
    .trend-down { color: #DC2626 !important; font-weight: bold; }
    .trend-stable { color: #64748B !important; }
    .gold-medal-row .trend-up, .gold-medal-row .trend-down, .gold-medal-row .trend-stable,
    .silver-medal-row .trend-up, .silver-medal-row .trend-down, .silver-medal-row .trend-stable,
    .bronze-medal-row .trend-up, .bronze-medal-row .trend-down, .bronze-medal-row .trend-stable { color: #0A1128 !important; }
    
    .bracket-match-card { background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 10px; margin: 6px 0; }
    .bracket-match-title { font-size: 0.75rem !important; color: #F97316 !important; font-weight: bold; margin-bottom: 4px; }
    .bracket-row { display: flex; justify-content: space-between; align-items: center; padding: 3px 0; font-size: 0.9rem !important; }
    .bracket-score-cell { background: #0A1128; color: #F97316; font-weight: bold; padding: 2px 6px; border-radius: 4px; min-width: 20px; text-align: center; }
    .bracket-team-winner { color: #4ADE80 !important; font-weight: bold; }
    .bracket-group-box { background: #0D1B3E !important; border: 1px solid #F97316 !important; border-radius: 8px; padding: 8px; }
    .center-final-card { background: #23153C !important; border: 3px solid #FF6B00 !important; border-radius: 10px; padding: 20px; text-align: center; }
    
    .kricon-table { width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }
    .kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; }
    .kricon-table td { padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; }
    .points-legend { background-color: #060B19; border-left: 5px solid #F97316; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    .flag-img { width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; display: inline-block; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# MAPOWANIE KODÓW ISO DLA FLAG SVG
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
    s = re.sub(r'^(MS|MX|ZA|XA|KR|cz|cv|CA|BA|QA|CH|BR|MA|HT|US|PY|AU|TR|DE|WKS|EC|NL|JP|SE|TN|BEL|CE|EM|IR|EGI|IRA|NZ|ESP|SA|URU|FRA|SEN|IRQ|NOR|ARG|ALG|AUT|JOR|POR|DRK|UZB|COL|ANG|CRO|GHA|PAN)\s+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'[^\w\s\-ąęćłńóśźżĄĘĆŁŃÓŚŹŻ]', '', s)
    return s.strip()

def get_cdn_flag_img_html(team_name):
    c_name = clean_and_sanitize_team_string(team_name)
    if c_name == "TBD": return f'🌐'
    code = ISO_FLAGS_MAP.get(c_name, None)
    if code:
        return f'<img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.6/flags/4x3/{code}.svg" class="flag-img" />'
    return f'🌐'

def calculate_points(pred_h, pred_a, real_h, real_a):
    try:
        if real_h is None or real_a is None or pred_h is None or pred_a is None: return 0
        if int(pred_h) == int(real_h) and int(pred_a) == int(real_a): return 3
        if np.sign(int(pred_h) - int(pred_a)) == np.sign(int(real_h) - int(real_a)): return 1
    except (ValueError, TypeError): pass
    return 0

def render_leaderboard_html(now_time, new_positions_dict_dest=None):
    scores = {p: 0 for p in players}
    if 'results' in st.session_state and 'bets' in st.session_state:
        for m_id, res in st.session_state.results.items():
            if res.get('status') == "Zakończony":
                for p in players:
                    if m_id in st.session_state.bets and p in st.session_state.bets[m_id]:
                        scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res.get('score_h'), res.get('score_a'))
                        
    df = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"]).sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    legend_html = """<div class="points-legend"><div style="font-weight: bold; color: #F97316; margin-bottom: 6px; font-size: 1.05rem;">ℹ️ System przyznawania punktów:</div><div>🎯 <b style="color: #4ADE80;">3 Punkty</b> — dokładny wynik</div><div>⚖️ <b style="color: #38BDF8;">1 Punkt</b> — poprawny zwycięzca / remis</div></div>"""
    rows = ""
    for idx, row in df.iterrows():
        pos, p_name = idx + 1, row['Gracz']
        if new_positions_dict_dest is not None: new_positions_dict_dest[p_name] = pos
        
        old_pos = st.session_state.last_positions.get(p_name, pos) if 'last_positions' in st.session_state else pos
        if old_pos > pos:
            trend_html = '<span class="trend-up">▲</span>'
        elif old_pos < pos:
            trend_html = '<span class="trend-down">▼</span>'
        else:
            trend_html = '<span class="trend-stable">•</span>'
            
        if pos == 1:
            bg_class, medal = 'class="gold-medal-row"', "🥇 "
        elif pos == 2:
            bg_class, medal = 'class="silver-medal-row"', "🥈 "
        elif pos == 3:
            bg_class, medal = 'class="bronze-medal-row"', "🥉 "
        else:
            bg_class, medal = "", ""
            
        rows += f"<tr {bg_class}><td style='text-align:center;'><b>{pos}</b></td><td style='text-align:center;'>{trend_html}</td><td>{medal}{p_name}</td><td><b>{row['Punkty']} pkt</b></td></tr>"
    return legend_html + f"<table class='kricon-table'><tr><th>Miejsce</th><th>Trend</th><th>Gracz</th><th>Punkty</th></tr>{rows}</table>"

def render_bracket_match_html_clean(match_id):
    m = st.session_state.results.get(match_id)
    if not m: return ""
    sh, sa = (str(m.get("score_h", "?")), str(m.get("score_a", "?"))) if m.get("status") == "Zakończony" else ("?", "?")
    win_h = m.get("score_h") is not None and m.get("score_a") is not None and m.get("score_h") > m.get("score_a") and m.get("status") == "Zakończony"
    win_a = m.get("score_h") is not None and m.get("score_a") is not None and m.get("score_a") > m.get("score_h") and m.get("status") == "Zakończony"
    
    h_clean = clean_and_sanitize_team_string(m.get('home'))
    a_clean = clean_and_sanitize_team_string(m.get('away'))
    
    st.markdown(f"""
    <div class="bracket-match-card">
        <div class="bracket-match-title">Mecz #{match_id}</div>
        <div class='bracket-row {"bracket-team-winner" if win_h else ""}'>
            <div style="display:flex; align-items:center; gap:8px;">{get_cdn_flag_img_html(h_clean)} <span>{h_clean}</span></div>
            <span class="bracket-score-cell">{sh}</span>
        </div>
        <div class='bracket-row {"bracket-team-winner" if win_a else ""}'>
            <div style="display:flex; align-items:center; gap:8px;">{get_cdn_flag_img_html(a_clean)} <span>{a_clean}</span></div>
            <span class="bracket-score-cell">{sa}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = ""
    for t in teams:
        t_clean = clean_and_sanitize_team_string(t)
        lines += f"<div style='text-align:left; padding:2px 0; font-size:0.9rem; display:flex; align-items:center; gap:8px;'>{get_cdn_flag_img_html(t_clean)} <span>{t_clean}</span></div>"
    return f"""<div class="bracket-group-box"><div style="font-weight:bold; color:#F97316; margin-bottom:4px; font-size:0.85rem;">GRUPA {g_code}</div>{lines}</div>"""

def save_backup_local_and_github():
    try:
        serializable_bets = {str(m_id): bets for m_id in st.session_state.bets.keys() for bets in [st.session_state.bets[m_id]]}
        json_string = json.dumps(serializable_bets, ensure_ascii=False, indent=4)
        with open("typer_backup.json", "w", encoding="utf-8") as f: f.write(json_string)
    except Exception: pass

def load_backup_local():
    if os.path.exists("typer_backup.json"):
        try:
            with open("typer_backup.json", "r", encoding="utf-8") as f: loaded_bets = json.load(f)
            for m_id_str, bets_data in loaded_bets.items():
                m_id = int(m_id_str)
                if m_id not in st.session_state.bets: st.session_state.bets[m_id] = {}
                for player, bet_tuple in bets_data.items(): st.session_state.bets[m_id][player] = tuple(bet_tuple)
            return True
        except Exception: return False
    return False

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    raw_fixtures = [
        (2026, 6, 11, 21, 0, "Grupa A", "Meksyk", "RPA"), (2026, 6, 12, 4, 0, "Grupa A", "Korea Południowa", "Czechy"),
        (2026, 6, 12, 21, 0, "Grupa B", "Kanada", "Bośnia i Hercegowina"), (2026, 6, 13, 3, 0, "Grupa D", "USA", "Paragwaj"),
        (2026, 6, 13, 21, 0, "Grupa B", "Katar", "Szwajcaria"), (2026, 6, 14, 0, 0, "Grupa C", "Brazylia", "Maroko"),
        (2026, 6, 14, 3, 0, "Grupa C", "Szkocja", "Haiti"), (2026, 6, 14, 6, 0, "Grupa D", "Australia", "Turcja"),
        (2026, 6, 14, 19, 0, "Grupa E", "Niemcy", "Curaçao"), (2026, 6, 14, 22, 0, "Grupa F", "Holandia", "Japonia"),
        (2026, 6, 15, 1, 0, "Grupa E", "WKS", "Ekwador"), (2026, 6, 15, 4, 0, "Grupa F", "Szwecja", "Tunezja"),
        (2026, 6, 15, 18, 0, "Grupa H", "Hiszpania", "Wyspy Zielonego Przylądka"), (2026, 6, 15, 21, 0, "Grupa G", "Belgia", "Egipt"),
        (2026, 6, 16, 0, 0, "Grupa H", "Arabia Saudyjska", "Urugwaj"), (2026, 6, 16, 3, 0, "Grupa G", "Iran", "Nowa Zelandia"),
        (2026, 6, 16, 21, 0, "Grupa I", "Francja", "Senegal"), (2026, 6, 16, 21, 0, "Grupa I", "Irak", "Norwegia")
    ]
    match_id = 1
    for yr, mo, dy, hr, mn, stage, home, away in raw_fixtures:
        dt = datetime(yr, mo, dy, hr, mn)
        schedule[match_id] = {
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]} {dt.strftime('%H:%M')}",
            "stage": stage, "home": home, "away": away, "score_h": None, "score_a": None, "status": "Oczekuje",
            "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
        }
        match_id += 1
    return schedule

if 'results' not in st.session_state or len(st.session_state.results) != 18: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 18: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'last_positions' not in st.session_state: st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

load_backup_local()
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
    st.sidebar.write(f"👤 Zalogowany jako: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Wyloguj się"): 
        st.session_state.logged_in_user = None
        st.rerun()
        
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    
    with tab1: 
        current_positions_map = {}
        st.markdown(render_leaderboard_html(now, current_positions_map), unsafe_allow_html=True)
        if current_positions_map: st.session_state.last_positions = current_positions_map
        
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        for m_id, m in sorted(st.session_state.results.items()):
            if (mode == "Oczekujące" and m.get('status') == "Zakończony") or (mode == "Zakończone" and m.get('status') == "Oczekuje"): continue
            
            if m.get('status') == "LIVE":
                status_html = '<span class="status-badge status-live">🔴 LIVE</span>'
            elif m.get('status') == "Zakończony":
                status_html = '<span class="status-badge status-ended">⚫ Zakończony</span>'
            else:
                status_html = '<span class="status-waiting-blink" style="animation: pulseAlertCore 2.0s infinite ease-in-out !important;">🟡 Oczekuje</span>'
                
            oficjalny_wynik_tekst = f"Wynik: {m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}"
            locked = (m['timestamp'] - now).total_seconds() <= 0
            has_existing_bet = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user) is not None
            cur_h, cur_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            home_clean = clean_and_sanitize_team_string(m['home'])
            away_clean = clean_and_sanitize_team_string(m['away'])
            
            st.markdown(f"""
            <div class="meta-upper-container">
                <span class="meta-id-text-clean">⚽ Mecz #{m_id}</span>
                {status_html}
                <span class="meta-badge-clean">📅 {m['date']}</span>
                <span class="meta-venue-clean">📍 {m.get('venue').split(',')[0]}</span>
                <span style="color:#475569;">({m['stage']})</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='match-card-clean'>", unsafe_allow_html=True)
            
            # --- POPRAWIONA STRUKTURA 5 STAŁYCH SEKCJI DLA WYRÓWNANIA PRZYCISKÓW W JEDNEJ LINII ---
            cf1, cf2, cf3, cf4, cf5 = st.columns([2.3, 2.5, 2.3, 1.1, 1.4])
            
            with cf1: 
                st.markdown(f"<div class='team-text-align-right'><span>{home_clean}</span> {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
                
            # --- POZIOMY STEPPER W JEDNYM WIERSZU [ - 0 + : - 0 + ] Z CYFRAMI ---
            with cf2:
                # 1. Tworzymy graficzną strukturę wartości bramkowych z pełnym wyrównaniem inline
                st.markdown(f"""
                <div class="stepper-row-container">
                    <span class="stepper-digit">{cur_h}</span>
                    <span class="stepper-separator">:</span>
                    <span class="stepper-digit">{cur_a}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Przycisk plus i minus ułożone symetrycznie w poziomie bezpośrednio na tej samej wysokości
                cb1, cb2, cb_spacer, cb3, cb4 = st.columns([1, 1, 0.4, 1, 1])
                with cb1:
                    st.markdown("<div class='stepper-mini-btn'>", unsafe_allow_html=True)
                    if st.button("—", key=f"m_h_{m_id}", disabled=locked):
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (max(0, cur_h - 1), cur_a)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with cb2:
                    st.markdown("<div class='stepper-mini-btn'>", unsafe_allow_html=True)
                    if st.button("+", key=f"p_h_{m_id}", disabled=locked):
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (cur_h + 1, cur_a)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with cb3:
                    st.markdown("<div class='stepper-mini-btn'>", unsafe_allow_html=True)
                    if st.button("—", key=f"m_a_{m_id}", disabled=locked):
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (cur_h, max(0, cur_a - 1))
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with cb4:
                    st.markdown("<div class='stepper-mini-btn'>", unsafe_allow_html=True)
                    if st.button("+", key=f"p_a_{m_id}", disabled=locked):
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (cur_h, cur_a + 1)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                        
            with cf3: 
                st.markdown(f"<div class='team-text-align-left'>{get_cdn_flag_img_html(m['away'])} <span>{away_clean}</span></div>", unsafe_allow_html=True)
                
            with cf4: 
                st.markdown(f"<span class='official-score-subtle'>{oficjalny_wynik_tekst}</span>", unsafe_allow_html=True)
                
            with cf5:
                st.markdown("<div class='flex-action-container' style='display:flex; align-items:center; gap:6px; justify-content:flex-end; width:100%; height:32px;'>", unsafe_allow_html=True)
                if locked:
                    st.button("🔒", disabled=True, key=f"lock_{m_id}")
                else:
                    if st.button("Zapisz", key=f"save_{m_id}"):
                        save_backup_local_and_github()
                        st.success("OK!")
                        st.rerun()
                    
                    if has_existing_bet:
                        st.markdown("<div class='success-bet-banner'>✔ OK</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='missing-bet-banner-blink' style='animation: pulseAlertCore 1.2s infinite ease-in-out !important;'>⚠️ BRAK</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.header("Tabele Grup Turniejowych")
        third_places_list = []
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0, "Grupa": g_name} for t in GROUPS_DICT[g_name]}
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'})
            g_rows = ""
            for idx, r in df_g.iterrows():
                rep_clean = clean_and_sanitize_team_string(r['Reprezentacja'])
                g_rows += f"<tr><td><b>{idx+1}</b></td><td>{get_cdn_flag_img_html(r['Reprezentacja'])} {rep_clean}</td><td><b>0</b></td><td>0</td><td>0</td><td>0</td></tr>"
            st.markdown(f"<div class='match-card-clean'><table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table></div>", unsafe_allow_html=True)
            
        st.divider(); st.header("🏆 Ranking Drużyn z 3. Miejsc")
        st.markdown("<div class='match-card-clean'><p style='color:#94A3B8; text-align:center; padding:10px;'>Tabela zaktualizuje się po rozegraniu meczów grupowych.</p></div>", unsafe_allow_html=True)

    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej")
        st.divider()
        c_g1, c_16l, c_mid = st.columns([1.5, 2.0, 2.0])
        with c_g1:
            for g in ["A","B"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
        with c_16l:
            render_bracket_match_html_clean(1)
        with c_mid:
            st.markdown("<div class='center-final-card'><h2>🏆 WIELKI FINAŁ</h2>TBD vs TBD</div>", unsafe_allow_html=True)
