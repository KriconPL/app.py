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

# MATRYCOWY SYSTEM STYLIZACJI FLEXBOX DLA ULTRA-KOMPAKTOWEGO INTERFEJSU W POZIOMIE
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
    
    /* SYSTEM ANIMACJI OPACITY BLINK DLA WSZYSTKICH ALERTÓW SYSTEMOWYCH */
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
    
    /* DETALE METADANYCH (ZINTEGROWANE I ODCHUDZONE) */
    .meta-inline-box {
        display: flex;
        flex-direction: column;
        gap: 1px;
        font-size: 0.65rem !important;
        color: #64748B !important;
        line-height: 1.2;
        text-align: left;
        white-space: nowrap;
    }
    .meta-inline-id { font-weight: bold; color: #F97316 !important; font-size: 0.75rem !important; }
    
    /* --- ZMINIMALIZOWANY, ULTRA-PŁASKI BOX MECZOWY --- */
    .match-card-clean {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important; 
        border-radius: 4px; 
        padding: 5px 12px !important; /* Odchudzenie wysokości wiersza */
        margin-bottom: 2px !important; /* Maksymalne zagęszczenie linii meczowych */
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
    
    /* --- INTEGRALNE WYRÓWNANIE POL TYPOWANIA OBOK SIEBIE [ X : X ] --- */
    .inputs-horizontal-align-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        width: 100%;
    }
    .score-separator-text { font-weight: bold; color: #F97316 !important; font-size: 1.1rem; }
    
    /* POWIĘKSZONE PRZYCISKI PLUS/MINUS Z DOPASOWANIEM DO JEDNEJ LINII */
    div.stNumberInput { width: 95px !important; margin: 0 !important; padding: 0 !important; display: inline-block !important; }
    div.stNumberInput input { text-align: center !important; background-color: #0A1128 !important; color: #F8FAFC !important; height: 28px !important; font-size: 1rem !important; font-weight: bold !important; padding: 0 !important; border: 1px solid #1E3A8A !important; }
    div.stNumberInput button { height: 28px !important; width: 22px !important; background-color: #1E293B !important; color: #F97316 !important; border: 1px solid #334155 !important; }
    
    /* WYMUSZONY ARCHITEKTONICZNIE POMARAŃCZOWY PRZYCISK ZAPISZ */
    div.stButton button, div[data-testid="stBlock"] button {
        background-color: #F97316 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px !important; 
        border: 1px solid #EA580C !important; 
        font-weight: bold !important; 
        height: 28px !important; 
        line-height: 26px !important; 
        padding: 0 12px !important; 
        font-size: 0.8rem !important; 
        width: 100% !important;
        display: inline-block !important;
    }
    div.stButton button:hover { background-color: #EA580C !important; }
    
    /* STYLIZACJA PODIUM W RANKINGU (ZŁOTO, SREBRO, BRĄZ) */
    .gold-row { background-color: #FEF08A !important; color: #0A1128 !important; font-weight: bold; }
    .gold-row td, .gold-row b { color: #0A1128 !important; }
    .silver-row { background-color: #E2E8F0 !important; color: #0A1128 !important; font-weight: bold; }
    .silver-row td, .silver-row b { color: #0A1128 !important; }
    .bronze-row { background-color: #FED7AA !important; color: #0A1128 !important; font-weight: bold; }
    .bronze-row td, .bronze-row b { color: #0A1128 !important; }
    
    .bracket-match-card { background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 8px; margin: 4px 0; }
    .bracket-match-title { font-size: 0.75rem !important; color: #F97316 !important; font-weight: bold; margin-bottom: 2px; }
    .bracket-row { display: flex; justify-content: space-between; align-items: center; padding: 2px 0; font-size: 0.85rem !important; }
    .bracket-score-cell { background: #0A1128; color: #F97316; font-weight: bold; padding: 1px 5px; border-radius: 4px; min-width: 18px; text-align: center; }
    .bracket-team-winner { color: #4ADE80 !important; font-weight: bold; }
    .bracket-group-box { background: #0D1B3E !important; border: 1px solid #F97316 !important; border-radius: 8px; padding: 6px; margin-bottom: 4px; }
    .center-final-card { background: #23153C !important; border: 3px solid #FF6B00 !important; border-radius: 10px; padding: 16px; text-align: center; }
    
    .kricon-table { width: 100%; border-collapse: collapse; margin: 10px 0 25px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }
    .kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 10px; font-weight: 800; }
    .kricon-table td { padding: 9px 10px; border-bottom: 1px solid #1E3A8A !important; }
    .points-legend { background-color: #060B19; border-left: 5px solid #F97316; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    .flag-img { width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; display: inline-block; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# MAPOWANIE KODÓW ISO DLA SERWERA CDN
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
        
        # DODAWANIE DEKORACYJNYCH IKON MEDALI DLA PIERWSZYCH TRZECH GRACZY
        if pos == 1:
            bg_class, medal_icon = 'class="gold-row"', "🥇 "
        elif pos == 2:
            bg_class, medal_icon = 'class="silver-row"', "🥈 "
        elif pos == 3:
            bg_class, medal_icon = 'class="bronze-row"', "🥉 "
        else:
            bg_class, medal_icon = "", ""
            
        rows += f"<tr {bg_class}><td style='text-align:center;'><b>{pos}</b></td><td>{medal_icon}{p_name}</td><td><b>{row['Punkty']} pkt</b></td></tr>"
    return legend_html + f"<table class='kricon-table'><tr><th>Msc.</th><th>Gracz</th><th>Punkty</th></tr>{rows}</table>"

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
            <div style="display:flex; align-items:center; gap:6px;">{get_cdn_flag_img_html(h_clean)} <span>{h_clean}</span></div>
            <span class="bracket-score-cell">{sh}</span>
        </div>
        <div class='bracket-row {"bracket-team-winner" if win_a else ""}'>
            <div style="display:flex; align-items:center; gap:6px;">{get_cdn_flag_img_html(a_clean)} <span>{a_clean}</span></div>
            <span class="bracket-score-cell">{sa}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = ""
    for t in teams:
        t_clean = clean_and_sanitize_team_string(t)
        lines += f"<div style='text-align:left; padding:1px 0; font-size:0.85rem; display:flex; align-items:center; gap:6px;'>{get_cdn_flag_img_html(t_clean)} <span>{t_clean}</span></div>"
    return f"""<div class="bracket-group-box"><div style="font-weight:bold; color:#F97316; margin-bottom:2px; font-size:0.8rem;">GRUPA {g_code}</div>{lines}</div>"""

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
        (2026, 6, 16, 21, 0, "Grupa I", "Francja", "Senegal"), (2026, 6, 16, 21, 0, "Grupa I", "Irak", "Norwegia"),
        (2026, 6, 17, 3, 0, "Grupa J", "Argentyna", "Algieria"), (2026, 6, 17, 6, 0, "Grupa J", "Austria", "Jordania"),
        (2026, 6, 17, 19, 0, "Grupa K", "Portugalia", "DR Konga"), (2026, 6, 17, 22, 0, "Grupa L", "Anglia", "Chorwacja"),
        (2026, 6, 18, 1, 0, "Grupa L", "Ghana", "Panama"), (2026, 6, 18, 4, 0, "Grupa K", "Uzbekistan", "Kolumbia"),
        (2026, 6, 18, 18, 0, "Grupa A", "Czechy", "RPA"), (2026, 6, 18, 21, 0, "Grupa B", "Szwajcaria", "Bośnia i Hercegowina"),
        (2026, 6, 19, 0, 0, "Grupa B", "Kanada", "Katar"), (2026, 6, 19, 3, 0, "Grupa A", "Meksyk", "Korea Południowa"),
        (2026, 6, 19, 21, 0, "Grupa D", "USA", "Australia"), (2026, 6, 20, 0, 0, "Grupa C", "Szkocja", "Maroko"),
        (2026, 6, 20, 3, 0, "Grupa C", "Brazylia", "Haiti"), (2026, 6, 20, 5, 0, "Grupa D", "Turcja", "Paragwaj"),
        (2026, 6, 20, 19, 0, "Grupa F", "Holandia", "Szwecja"), (2026, 6, 20, 22, 0, "Grupa E", "Niemcy", "WKS"),
        (2026, 6, 21, 2, 0, "Grupa E", "Ekwador", "Curaçao"), (2026, 6, 21, 6, 0, "Grupa F", "Tunezja", "Japonia"),
        (2026, 6, 21, 18, 0, "Grupa H", "Hiszpania", "Arabia Saudyjska"), (2026, 6, 21, 21, 0, "Grupa G", "Belgia", "Iran"),
        (2026, 6, 22, 0, 0, "Grupa H", "Urugwaj", "Wyspy Zielonego Przylądka"), (2026, 6, 22, 3, 0, "Grupa G", "Nowa Zelandia", "Egipt")
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
    sim_day = datetime(2026, 6, 22, 18, 0)
    for g_name, teams in GROUPS_DICT.items():
        for pair in [(teams[0], teams[2]), (teams[1], teams[3])]:
            schedule[match_id] = {"timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]} {sim_day.strftime('%H:%M')}", "stage": g_name, "home": pair[0], "away": pair[1], "score_h": None, "score_a": None, "status": "Oczekuje", "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]}
            match_id += 1
        sim_day += timedelta(hours=4)
    ko_stages = [("1/16 Finału", 16, [(29,6), (30,6), (1,7), (2,7)]), ("1/8 Finału", 8, [(4,7), (5,7), (6,7), (7,7)]), ("Ćwierćfinały", 4, [(9,7), (10,7)]), ("Półfinały", 2, [(14,7), (15,7)]), ("Mecz o 3. miejsce", 1, [(18,7)]), ("Finał", 1, [(19,7)])]
    for stage_name, count, stage_dates in ko_stages:
        date_idx = 0
        matches_per_date = max(1, count // len(stage_dates))
        for i in range(count):
            d, m_num = stage_dates[date_idx % len(stage_dates)]
            hour = 18 if i % 2 == 0 else 22
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            schedule[match_id] = {
                "timestamp": match_dt, "date": f"{d} {months_pl[m_num]} {match_dt.strftime('%H:%M')}",
                "stage": stage_name, "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, "status": "Oczekuje",
                "venue": "MetLife, Nowy Jork" if stage_name == "Finał" else VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
            }
            match_id += 1
            if (i + 1) % matches_per_date == 0: date_idx += 1
    return schedule

if 'results' not in st.session_state or len(st.session_state.results) != 104: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 104: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
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
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
        
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
            
            # LINIA INFORMACYJNA NAD MECZEM (CZCIONKA 0.75REM)
            st.markdown(f"""
            <div class="meta-upper-container">
                <span class="meta-id-text-clean">⚽ Mecz #{m_id}</span>
                {status_html}
                <span class="meta-badge-clean">📅 {m['date']}</span>
                <span class="meta-venue-clean">📍 {m.get('venue').split(',')[0]}</span>
                <span style="color:#475569;">({m['stage']})</span>
            </div>
            """, unsafe_allow_html=True)
            
            # --- START BOXA MECZOWEGO: IDEALNA LINIA POZIOMA Z SUWAKAMI OBOK SIEBIE ---
            st.markdown("<div class='match-card-clean'>", unsafe_allow_html=True)
            
            c_home, c_inputs, c_away, c_score, c_actions = st.columns([2.3, 2.4, 2.3, 1.1, 1.4])
            
            with c_home:
                st.markdown(f"<div class='team-text-align-right'><span>{home_clean}</span> {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
                
            # --- SUWAKI MATRYCOWE Z PRZYCISKAMI +/- UMIESZCZONE OBOK SIEBIE [ X : X ] ---
            with c_inputs:
                st.markdown("<div class='inputs-horizontal-align-container'>", unsafe_allow_html=True)
                b_h = st.number_input(f"H_{m_id}", 0, 20, int(cur_h), 1, key=f"h_{m_id}", label_visibility="collapsed")
                st.markdown("<span class='score-separator-text'>:</span>", unsafe_allow_html=True)
                b_a = st.number_input(f"A_{m_id}", 0, 20, int(cur_a), 1, key=f"a_{m_id}", label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with c_away:
                st.markdown(f"<div class='team-text-align-left'>{get_cdn_flag_img_html(m['away'])} <span>{away_clean}</span></div>", unsafe_allow_html=True)
                
            with c_score:
                st.markdown(f"<span class='official-score-subtle'>{oficjalny_wynik_tekst}</span>", unsafe_allow_html=True)
                
            with c_actions:
                st.markdown("<div style='display:flex; align-items:center; gap:6px; justify-content:flex-end; width:100%; height:32px;'>", unsafe_allow_html=True)
                if locked:
                    st.button("🔒", disabled=True, key=f"lock_{m_id}")
                else:
                    if st.button("Zapisz", key=f"save_{m_id}"):
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                        save_backup_local_and_github()
                        st.rerun()
                    
                    if has_existing_bet:
                        st.markdown("<div class='success-bet-banner'>✔ OK</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='missing-bet-banner-blink' style='animation: pulseAlertCore 1.2s infinite ease-in-out !important;'>⚠️ BRAK</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True) # Zamknięcie .match-card-clean

    with tab3:
        st.header("Tabele Grup Turniejowych")
        third_places_list = []
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0, "Grupa": g_name} for t in GROUPS_DICT[g_name]}
            for m in st.session_state.results.values():
                if m.get("stage") == g_name and m.get("status") == "Zakończony":
                    h = clean_and_sanitize_team_string(m.get("home"))
                    a = clean_and_sanitize_team_string(m.get("away"))
                    sh, sa = m.get("score_h"), m.get("score_a")
                    if h in stats and a in stats:
                        stats[h]["BZ"]+=sh; stats[h]["BS"]+=sa; stats[h]["RB"]+=(sh-sa)
                        stats[a]["BZ"]+=sa; stats[a]["BS"]+=sh; stats[a]["RB"]+=(sa-sh)
                        if sh>sa: stats[h]["Pkt"]+=3; stats[h]["Zwyciestwa"]+=1
                        elif sa>sh: stats[a]["Pkt"]+=3; stats[a]["Zwyciestwa"]+=1
                        else: stats[h]["Pkt"]+=1; stats[a]["Pkt"]+=1
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'}).sort_values(by=["Pkt", "RB", "BZ"], ascending=False).reset_index(drop=True)
            df_g.index+=1
            if len(df_g) >= 3: third_places_list.append(df_g.iloc[2].to_dict())
            
            g_rows = ""
            for idx, r in df_g.iterrows():
                rep_clean = clean_and_sanitize_team_string(r['Reprezentacja'])
                row_style = 'style="background-color:#16A34A;"' if idx in [1, 2] else ('style="background-color:#EA580C;"' if idx == 3 else '')
                g_rows += f"<tr {row_style}><td><b>{idx}</b></td><td>{get_cdn_flag_img_html(r['Reprezentacja'])} {rep_clean}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>"
            st.markdown(f"<div class='match-card-clean'><table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table></div>", unsafe_allow_html=True)
            
        # --- PRZYWRÓCONA W PEŁNI STRUKTURALNA TABELA DRUŻYN Z 3. MIEJSCA ---
        st.divider(); st.header("🏆 Ranking Drużyn z 3. Miejsc")
        if third_places_list:
            df_third = pd.DataFrame(third_places_list).sort_values(by=["Pkt", "RB", "BZ", "Zwyciestwa"], ascending=False).reset_index(drop=True)
            df_third.index += 1; third_rows = ""
            for idx, r in df_third.iterrows(): 
                rep_clean_third = clean_and_sanitize_team_string(r['Reprezentacja'])
                third_rows += f"<tr {'style=\"background-color:#16A34A;\"' if idx <= 8 else ''}><td><b>{idx}</b></td><td><b>{r['Grupa']}</b></td><td>{get_cdn_flag_img_html(r['Reprezentacja'])} {rep_clean_third}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>"
            st.markdown(f"<div class='match-card-clean'><table class='kricon-table'><tr><th>Msc.</th><th>Grupa</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{third_rows}</table></div>", unsafe_allow_html=True)

    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej")
        st.divider()
        c_g1, c_16l, c_8l, c_mid, c_8r, c_r16, c_g2 = st.columns([1.1, 1.3, 1.3, 1.8, 1.3, 1.3, 1.1])
        with c_g1:
            for g in ["A","B","C","D","E","F"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
        with c_16l:
            for i in range(73, 81): render_bracket_match_html_clean(i)
        with c_8l:
            for i in range(89, 93): render_bracket_match_html_clean(i)
        with c_mid:
            st.markdown("<div class='center-final-card'><h2>🏆 WIELKI FINAŁ</h2>TBD vs TBD</div>", unsafe_allow_html=True)
        with c_8r:
            for i in range(93, 97): render_bracket_match_html_clean(i)
        with c_r16:
            for i in range(81, 89): render_bracket_match_html_clean(i)
        with c_g2:
            for g in ["G","H","I","J","K","L"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
