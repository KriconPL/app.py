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

# GŁÓWNY SILNIK CSS
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
    * { -webkit-user-select: none !important; -moz-user-select: none !important; -ms-user-select: none !important; user-select: none !important; }
    input, textarea, div[data-baseweb="input"] { -webkit-user-select: auto !important; -moz-user-select: auto !important; -ms-user-select: auto !important; user-select: auto !important; }

    body, html, [data-testid="stAppViewContainer"], .stApp, [data-testid="stTabContent"], div.stTabs { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] { background-color: #060B19 !important; }
    [data-testid="stHeader"] { background-color: #0A1128 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #F8FAFC !important; }
    
    @keyframes pulseAlertCore { 0% { opacity: 1.0; } 50% { opacity: 0.3; } 100% { opacity: 1.0; } }
    
    /* GŁÓWNY BOX MECZU */
    div[data-testid="stHorizontalBlock"]:has(.match-row-anchor) {
        background: #172554 !important; border: 1px solid #1E3A8A !important; border-radius: 0 0 6px 6px; padding: 6px 10px !important; margin-bottom: 6px !important; align-items: center !important; box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    div[data-testid="stHorizontalBlock"]:has(.match-row-anchor) > div[data-testid="column"] { padding: 0 4px !important; }
    
    .meta-upper-bar-container { background-color: #1E293B !important; border: 1px solid #1E3A8A !important; border-bottom: none !important; border-radius: 6px 6px 0 0; display: flex; align-items: center; gap: 12px; font-size: 0.75rem !important; color: #94A3B8 !important; padding: 4px 14px !important; width: 100%; margin-top: 10px !important; }
    .meta-id-text-clean { font-weight: bold; color: #F97316 !important; }
    
    .team-align-right { font-size: 1.15rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }
    .team-align-left { font-size: 1.15rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }
    
    .off-score { font-size: 0.85rem !important; font-weight: bold !important; color: #94A3B8 !important; background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px; display: block; text-align: center; white-space: nowrap; height: 38px !important; line-height: 36px !important; width: 100%; }
    .score-colon { text-align: center; font-weight: bold; color: #F97316 !important; font-size: 1.4rem; height: 38px; line-height: 34px; width: 100%; }
    
    /* WYNIKI I PODŚWIETLANIA ZAKOŃCZONYCH MECZÓW */
    .result-box { display: flex; align-items: center; justify-content: center; height: 38px; width: 100%; border-radius: 6px; font-weight: 900; font-size: 1.3rem; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3); }
    .bet-locked { background: #0F172A; color: #64748B; border: 1px solid #1E293B; }
    .bet-exact { background: #16A34A; color: #FFFFFF; border: 2px solid #4ADE80; box-shadow: 0 0 10px rgba(74, 222, 128, 0.4); } 
    .bet-winner { background: #064E3B; color: #4ADE80; border: 1px dashed #16A34A; } 
    .bet-wrong { background: #450A0A; color: #FCA5A5; border: 1px dashed #DC2626; } 
    
    /* INPUTY I TŁA LOGOWANIA */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div { background-color: #1E293B !important; border: 1px solid #334155 !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span { color: #F8FAFC !important; }
    ul[role="listbox"] { background-color: #1E293B !important; }
    li[role="option"] { background-color: #1E293B !important; color: #F8FAFC !important; }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #334155 !important; color: #F97316 !important; }
    div[data-testid="stTextInput"] div[data-baseweb="input"] { background-color: #1E293B !important; border: 1px solid #334155 !important; }
    div[data-testid="stTextInput"] input { color: #F8FAFC !important; -webkit-text-fill-color: #F8FAFC !important; background-color: transparent !important; }

    /* INPUTY BRAMEK W MECZACH */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] { background-color: #0A1128 !important; border: 1px solid #1E3A8A !important; border-radius: 6px !important; height: 38px !important; transition: none !important; overflow: hidden; }
    div[data-testid="stNumberInput"] input { color: #F8FAFC !important; -webkit-text-fill-color: #F8FAFC !important; background-color: #0A1128 !important; font-size: 1.25rem !important; font-weight: 900 !important; text-align: center !important; padding: 0 !important; }
    div[data-testid="stNumberInput"] button { background-color: #1E293B !important; border: none !important; border-radius: 4px !important; width: 32px !important; height: 32px !important; margin: 2px !important; transition: transform 0.1s ease !important; }
    div[data-testid="stNumberInput"] button svg { fill: #F97316 !important; color: #F97316 !important; }
    div[data-testid="stNumberInput"] button:active, div[data-testid="stNumberInput"] button:focus { opacity: 1.0 !important; background-color: #0F172A !important; transform: scale(0.90) !important; outline: none !important; box-shadow: none !important; }
    div[data-testid="stNumberInput"] button:hover { background-color: #334155 !important; }
    div[data-testid="stNumberInput"] button:hover svg { fill: #FFFFFF !important; }
    
    /* GŁÓWNE PRZYCISKI AKCJI (STREAMLIT KINDS) */
    button[kind="secondary"] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px !important; height: 38px !important; min-height: 38px !important; padding: 0 !important; width: 100% !important; display: block !important; }
    button[kind="secondary"] * { color: #F97316 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    button[kind="secondary"]:hover { background-color: #334155 !important; }
    button[kind="secondary"]:hover * { color: #FFFFFF !important; }
    
    button[kind="primary"] { background-color: #F97316 !important; border: 1px solid #EA580C !important; border-radius: 4px !important; height: 38px !important; min-height: 38px !important; padding: 0 !important; width: 100% !important; display: block !important; box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important; }
    button[kind="primary"] * { color: #FFFFFF !important; font-size: 0.9rem !important; font-weight: bold !important; }
    button[kind="primary"]:hover { background-color: #EA580C !important; border-color: #C2410C !important; }
    
    /* STATUSY TYPOWANIA NA SAMYM KOŃCU */
    .bet-ok { background: #16A34A; color: white; text-align: center; font-weight: bold; border-radius: 4px; height: 38px; line-height: 38px; font-size: 0.8rem; width: 100%; white-space: nowrap; display:block; }
    .bet-brak { background: #DC2626; color: white; text-align: center; font-weight: bold; border-radius: 4px; height: 38px; line-height: 38px; font-size: 0.7rem; width: 100%; animation: pulseAlertCore 1.2s infinite ease-in-out; white-space: nowrap; display:block; }
    .missing-bet-banner-blink { animation: pulseAlertCore 1.2s infinite ease-in-out !important; background-color: #DC2626 !important; color: #FFFFFF !important; font-weight: bold !important; text-align: center !important; height: 38px !important; line-height: 38px !important; border-radius: 4px !important; font-size: 0.7rem !important; display: block !important; width: 100% !important; margin: 0 !important; white-space: nowrap !important; }
    .status-waiting-blink { animation: pulseAlertCore 2.0s infinite ease-in-out !important; color: #D97706 !important; font-weight: bold !important; font-size: 0.65rem !important; }
    .status-badge-ended { color: #94A3B8 !important; font-weight: bold; font-size: 0.65rem !important; }
    .status-badge-live { color: #DC2626 !important; font-weight: bold; font-size: 0.65rem !important; }
    
    /* TABELE */
    .kricon-table { width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }
    .kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; }
    .kricon-table td { padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; }
    .col-pos { width: 60px !important; text-align: center !important; }
    .col-trend { width: 60px !important; text-align: center !important; }
    .col-missing { width: 100px !important; text-align: center !important; font-weight: bold !important; }
    
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
    
    .points-legend { background-color: #060B19; border-left: 5px solid #F97316; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    .flag-img { width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; display: inline-block; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); }
    
    /* DRABINKA I TABELE */
    .bracket-match-card { background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 8px; margin: 5px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .bracket-match-title { font-size: 0.70rem !important; color: #F97316 !important; font-weight: bold; margin-bottom: 3px; border-bottom: 1px solid #1E3A8A; padding-bottom: 2px; }
    .bracket-row { display: flex; justify-content: space-between; align-items: center; padding: 2px 0; font-size: 0.85rem !important; }
    .bracket-score-cell { background: #0A1128; color: #F97316; font-weight: bold; padding: 1px 6px; border-radius: 4px; min-width: 22px; text-align: center; border: 1px solid #1E3A8A; }
    .bracket-team-winner { color: #4ADE80 !important; font-weight: bold; }
    .bracket-team-name { max-width: 60px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; vertical-align: middle; }
    
    .bracket-group-box { background: #0D1B3E !important; border: 1px solid #F97316 !important; border-radius: 8px; padding: 8px; margin-bottom: 8px; }
    
    .center-final-card-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; margin-top: 250px; }
    .center-final-card { background: linear-gradient(145deg, #1E3A8A, #0A1128) !important; border: 2px solid #F97316 !important; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 0 20px rgba(249,115,22,0.3); width: 100%; }
    .final-title { color: #F97316; font-size: 1.1rem; font-weight: 900; margin-bottom: 10px; letter-spacing: 1px; text-transform: uppercase; }
    .final-teams { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 10px; }
    .final-team { font-size: 1.05rem; font-weight: bold; color: #F8FAFC; display: flex; align-items: center; gap: 6px; flex: 1; justify-content: center; overflow: hidden; }
    .final-score { font-size: 1.5rem; font-weight: 900; color: #F97316; background: #060B19; padding: 4px 12px; border-radius: 8px; border: 1px solid #334155; }
    .final-venue { font-size: 0.75rem; color: #94A3B8; }
    </style>
""", unsafe_allow_html=True)

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

def save_backup_local_and_github():
    try:
        if os.path.exists("typer_backup.json"):
            with open("typer_backup.json", "r", encoding="utf-8") as f:
                loaded_bets = json.load(f)
            for m_id_str, bets_data in loaded_bets.items():
                m_id = int(m_id_str)
                if m_id not in st.session_state.bets: st.session_state.bets[m_id] = {}
                for player, bet_tuple in bets_data.items():
                    if player != st.session_state.logged_in_user:
                        st.session_state.bets[m_id][player] = tuple(bet_tuple)
        
        serializable_bets = {str(m_id): bets for m_id, bets in st.session_state.bets.items()}
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

def btn_save_action(m_id, user, h_key, a_key):
    st.session_state.bets[m_id][user] = (st.session_state[h_key], st.session_state[a_key])
    save_backup_local_and_github()

def btn_delete_action(m_id, user, h_key, a_key):
    if user in st.session_state.bets.get(m_id, {}):
        del st.session_state.bets[m_id][user]
    st.session_state[h_key] = 0
    st.session_state[a_key] = 0
    save_backup_local_and_github()

@st.dialog("👁️ Typy graczy dla tego meczu")
def show_other_bets(m_id, current_user):
    st.markdown(f"<h4 style='text-align: center; color: #F97316 !important;'>Mecz #{m_id}</h4>", unsafe_allow_html=True)
    other_bets = []
    for p in players:
        if p != current_user:
            bet = st.session_state.bets.get(m_id, {}).get(p)
            if bet:
                other_bets.append({"Gracz": p, "Typ": f"{bet[0]} : {bet[1]}"})
            else:
                other_bets.append({"Gracz": p, "Typ": "Brak typu"})
    df = pd.DataFrame(other_bets)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_leaderboard_html(now_time, new_positions_dict_dest=None):
    scores = {p: 0 for p in players}
    missing_bets = {p: 0 for p in players}
    
    if 'results' in st.session_state and 'bets' in st.session_state:
        for m_id, res in st.session_state.results.items():
            is_past = (res['timestamp'] - now_time).total_seconds() <= 0
            for p in players:
                has_bet = m_id in st.session_state.bets and p in st.session_state.bets[m_id]
                if is_past and not has_bet:
                    missing_bets[p] += 1
            
            if res.get('status') == "Zakończony":
                for p in players:
                    if m_id in st.session_state.bets and p in st.session_state.bets[m_id]:
                        scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res.get('score_h'), res.get('score_a'))
                        
    df_scores = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"])
    df_missing = pd.DataFrame(list(missing_bets.items()), columns=["Gracz", "Brak typu"])
    df = pd.merge(df_scores, df_missing, on="Gracz").sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    
    legend_html = """<div class="points-legend"><div style="font-weight: bold; color: #F97316; margin-bottom: 6px; font-size: 1.05rem;">ℹ️ System przyznawania punktów:</div><div>🎯 <b style="color: #4ADE80;">3 Punkty</b> — dokładny wynik</div><div>⚖️ <b style="color: #38BDF8;">1 Punkt</b> — poprawny zwycięzca / remis</div></div>"""
    rows = ""
    for idx, row in df.iterrows():
        pos, p_name = idx + 1, row['Gracz']
        if new_positions_dict_dest is not None: new_positions_dict_dest[p_name] = pos
        
        old_pos = st.session_state.last_positions.get(p_name, pos) if 'last_positions' in st.session_state else pos
        if old_pos > pos: trend_html = '<span class="trend-up">▲</span>'
        elif old_pos < pos: trend_html = '<span class="trend-down">▼</span>'
        else: trend_html = '<span class="trend-stable">•</span>'
            
        if pos == 1: bg_class, medal = 'class="gold-medal-row"', "🥇 "
        elif pos == 2: bg_class, medal = 'class="silver-medal-row"', "🥈 "
        elif pos == 3: bg_class, medal = 'class="bronze-medal-row"', "🥉 "
        else: bg_class, medal = "", ""
        
        miss_val = row['Brak typu']
        miss_html = f"<span style='color: #DC2626;'>{miss_val}</span>" if miss_val > 0 else f"<span style='color: #64748B;'>0</span>"
            
        rows += f"<tr {bg_class}><td class='col-pos'><b>{pos}</b></td><td class='col-trend'>{trend_html}</td><td>{medal}{p_name}</td><td><b>{row['Punkty']} pkt</b></td><td class='col-missing'>{miss_html}</td></tr>"
    return legend_html + f"<table class='kricon-table'><tr><th class='col-pos'>Miejsce</th><th class='col-trend'>Trend</th><th>Gracz</th><th>Punkty</th><th class='col-missing'>Brak typu</th></tr>{rows}</table>"

def render_bracket_match_html_clean(match_id, mt="0px", mb="6px"):
    m = st.session_state.results.get(match_id)
    if not m: return ""
    
    status = m.get("status")
    if status in ["Zakończony", "LIVE"] and m.get("score_h") is not None and m.get("score_a") is not None:
        sh, sa = str(m.get("score_h")), str(m.get("score_a"))
        win_h = m.get("score_h") > m.get("score_a") and status == "Zakończony"
        win_a = m.get("score_a") > m.get("score_h") and status == "Zakończony"
    else:
        sh, sa = "?", "?"
        win_h, win_a = False, False
    
    h_clean = clean_and_sanitize_team_string(m.get('home'))
    a_clean = clean_and_sanitize_team_string(m.get('away'))
    
    st.markdown(f"""
    <div class="bracket-match-card" style="margin-top: {mt}; margin-bottom: {mb};">
        <div class="bracket-match-title">Mecz #{match_id}</div>
        <div class='bracket-row {"bracket-team-winner" if win_h else ""}'>
            <div style="display:flex; align-items:center; gap:6px; overflow: hidden;">
                {get_cdn_flag_img_html(h_clean)}
                <span class="bracket-team-name" title="{h_clean}">{h_clean}</span>
            </div>
            <span class="bracket-score-cell">{sh}</span>
        </div>
        <div class='bracket-row {"bracket-team-winner" if win_a else ""}'>
            <div style="display:flex; align-items:center; gap:6px; overflow: hidden;">
                {get_cdn_flag_img_html(a_clean)}
                <span class="bracket-team-name" title="{a_clean}">{a_clean}</span>
            </div>
            <span class="bracket-score-cell">{sa}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = ""
    for t in teams:
        t_clean = clean_and_sanitize_team_string(t)
        lines += f"<div style='text-align:left; padding:2px 0; font-size:0.85rem; display:flex; align-items:center; gap:6px;'>{get_cdn_flag_img_html(t_clean)} <span style='max-width: 75px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{t_clean}</span></div>"
    return f"""<div class="bracket-group-box"><div style="font-weight:bold; color:#F97316; margin-bottom:4px; font-size:0.85rem;">GRUPA {g_code}</div>{lines}</div>"""

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    match_id = 1
    start_dt = datetime(2026, 6, 11, 21, 0)
    
    # Precyzyjne 72 mecze grupowe (12 grup * 6 meczów)
    for matchday in range(3):
        for g_name, teams in GROUPS_DICT.items():
            if matchday == 0: pairs = [(teams[0], teams[1]), (teams[2], teams[3])]
            elif matchday == 1: pairs = [(teams[0], teams[2]), (teams[3], teams[1])]
            else: pairs = [(teams[0], teams[3]), (teams[1], teams[2])]
                
            for t_home, t_away in pairs:
                dt = start_dt + timedelta(days=(match_id-1)//4, hours=((match_id-1)%4)*3)
                schedule[match_id] = {
                    "timestamp": dt, "date": f"{dt.day} {months_pl.get(dt.month, 'Czerwca')} {dt.strftime('%H:%M')}",
                    "stage": g_name, "home": t_home, "away": t_away, "score_h": None, "score_a": None, "status": "Oczekuje",
                    "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
                }
                match_id += 1
                
    ko_stages = [("1/16 Finału", 16, [(29,6), (30,6), (1,7), (2,7)]), ("1/8 Finału", 8, [(4,7), (5,7), (6,7), (7,7)]), ("Ćwierćfinały", 4, [(9,7), (10,7)]), ("Półfinały", 2, [(14,7), (15,7)]), ("Mecz o 3. miejsce", 1, [(18,7)]), ("Finał", 1, [(19,7)])]
    for stage_name, count, stage_dates in ko_stages:
        date_idx = 0
        matches_per_date = max(1, count // len(stage_dates))
        for i in range(count):
            d, m_num = stage_dates[date_idx % len(stage_dates)]
            hour = 18 if i % 2 == 0 else 22
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            schedule[match_id] = {
                "timestamp": match_dt, "date": f"{d} {months_pl.get(m_num, 'Lipca')} {match_dt.strftime('%H:%M')}",
                "stage": stage_name, "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, "status": "Oczekuje",
                "venue": "MetLife, Nowy Jork" if stage_name == "Finał" else VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
            }
            match_id += 1
            if (i + 1) % matches_per_date == 0: date_idx += 1
            
    return schedule

def fetch_official_results_from_api(now_time):
    for m_id, m in st.session_state.results.items():
        if m['timestamp'] <= now_time and m['status'] != "Zakończony":
            np.random.seed(m_id)
            m['score_h'] = int(np.random.choice([0, 1, 2, 3]))
            m['score_a'] = int(np.random.choice([0, 1, 2]))
            m['status'] = "Zakończony"
            if m_id >= 73:
                if m['home'] == "TBD": m['home'] = "Meksyk"
                if m['away'] == "TBD": m['away'] = "RPA"

if 'results' not in st.session_state or len(st.session_state.results) != 104: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 104: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'last_positions' not in st.session_state: st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

load_backup_local()
now = datetime.now()
fetch_official_results_from_api(now)

for m_id, m in st.session_state.results.items():
    if m.get('status') != "Zakończony":
        time_diff = now - m['timestamp']
        if timedelta(minutes=0) <= time_diff <= timedelta(minutes=120): st.session_state.results[m_id]['status'] = "LIVE"

# LOGOWANIE
if st.session_state.logged_in_user is None:
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        st.subheader("🔒 Logowanie")
        user = st.selectbox("Wybierz użytkownika:", [""] + list(USER_CREDENTIALS.keys()))
        pw = st.text_input("Wpisz hasło:", type="password")
        if st.button("Zaloguj się", type="primary"):
            if USER_CREDENTIALS.get(user) == pw: 
                st.session_state.logged_in_user = user
                st.rerun()
            else: st.error("Błąd logowania.")
    with c2:
        st.subheader("📊 Ranking")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    st.sidebar.write(f"👤 Zalogowany jako: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Wyloguj się", type="primary"): 
        st.session_state.logged_in_user = None
        st.rerun()
        
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ranking", "📅 Terminarz", "🕵️ Typy graczy", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    
    with tab1: 
        current_positions_map = {}
        st.markdown(render_leaderboard_html(now, current_positions_map), unsafe_allow_html=True)
        if current_positions_map: st.session_state.last_positions = current_positions_map
        
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        for m_id, m in sorted(st.session_state.results.items()):
            if (mode == "Oczekujące" and m.get('status') == "Zakończony") or (mode == "Zakończone" and m.get('status') == "Oczekuje"): continue
            
            if m.get('status') == "LIVE":
                status_html = '<span class="status-badge-live">🔴 LIVE</span>'
            elif m.get('status') == "Zakończony":
                status_html = '<span class="status-badge-ended">⚫ Zakończony</span>'
            else:
                status_html = '<span class="status-waiting-blink">🟡 Oczekuje</span>'
                
            oficjalny_wynik_tekst = f"Wynik: {m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}"
            
            # BLOKADA CZASOWA
            locked = (m['timestamp'] - now).total_seconds() <= 0
            
            has_existing_bet = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user) is not None
            saved_h, saved_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            h_key, a_key = f"h_{m_id}", f"a_{m_id}"
            if h_key not in st.session_state: st.session_state[h_key] = int(saved_h)
            if a_key not in st.session_state: st.session_state[a_key] = int(saved_a)
            
            home_clean = clean_and_sanitize_team_string(m['home'])
            away_clean = clean_and_sanitize_team_string(m['away'])
            
            st.markdown(f"""
            <div class="meta-upper-bar-container">
                <span class="meta-id-text-clean">⚽ Mecz #{m_id}</span>
                {status_html}
                <span style="color:#94A3B8;">📅 {m['date']}</span>
                <span style="color:#38BDF8; font-weight:bold;">📍 {m.get('venue').split(',')[0]}</span>
                <span style="color:#64748B;">({m['stage']})</span>
            </div>
            <div class='match-row-anchor'></div>
            """, unsafe_allow_html=True)
            
            c_home, c_inph, c_sep, c_inpa, c_away, c_score, c_save, c_del, c_status = st.columns([2.5, 1.8, 0.2, 1.8, 2.5, 1.5, 1.2, 0.6, 1.2])
            
            with c_home:
                st.markdown(f"<div class='team-align-right'><span>{home_clean}</span> {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
                
            box_class_h = "bet-locked"
            box_class_a = "bet-locked"
            
            if locked and m.get('status') == "Zakończony" and has_existing_bet:
                pts = calculate_points(saved_h, saved_a, m.get('score_h'), m.get('score_a'))
                if pts == 3: box_class_h = box_class_a = "bet-exact"
                elif pts == 1: box_class_h = box_class_a = "bet-winner"
                else: box_class_h = box_class_a = "bet-wrong"
            
            with c_inph:
                if locked:
                    val_h = saved_h if has_existing_bet else "-"
                    st.markdown(f"<div class='result-box {box_class_h}'>{val_h}</div>", unsafe_allow_html=True)
                else:
                    st.number_input("H", min_value=0, max_value=20, key=h_key, label_visibility="collapsed")
                    
            with c_sep:
                st.markdown("<div class='score-colon'>:</div>", unsafe_allow_html=True)
                
            with c_inpa:
                if locked:
                    val_a = saved_a if has_existing_bet else "-"
                    st.markdown(f"<div class='result-box {box_class_a}'>{val_a}</div>", unsafe_allow_html=True)
                else:
                    st.number_input("A", min_value=0, max_value=20, key=a_key, label_visibility="collapsed")
                    
            with c_away:
                st.markdown(f"<div class='team-align-left'>{get_cdn_flag_img_html(m['away'])} <span>{away_clean}</span></div>", unsafe_allow_html=True)
                
            with c_score:
                st.markdown(f"<div class='off-score'>{oficjalny_wynik_tekst}</div>", unsafe_allow_html=True)
                
            with c_save:
                if locked:
                    st.button("👥 Typy", key=f"typy_{m_id}", type="secondary", on_click=show_other_bets, args=(m_id, st.session_state.logged_in_user))
                else:
                    st.button("Zapisz", key=f"save_{m_id}", type="primary", on_click=btn_save_action, args=(m_id, st.session_state.logged_in_user, h_key, a_key))
            
            with c_del:
                if not locked and has_existing_bet:
                    st.button("✖", key=f"del_{m_id}", type="secondary", on_click=btn_delete_action, args=(m_id, st.session_state.logged_in_user, h_key, a_key))
                else:
                    st.empty()
                        
            with c_status:
                if has_existing_bet:
                    st.markdown("<div class='success-bet-banner'>✔ OK</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='missing-bet-banner-blink'>⚠️ BRAK TYPU</div>", unsafe_allow_html=True)

    with tab3:
        st.header("🕵️ Podgląd wszystkich typów")
        st.markdown("Tutaj możesz śledzić, jak rywale obstawili spotkania. Tabela odblokowuje się wraz z pierwszym gwizdkiem w danym meczu.")
        
        locked_matches = [m_id for m_id, m in st.session_state.results.items() if (m['timestamp'] - now).total_seconds() <= 0]
        
        if not locked_matches:
            st.info("Żaden mecz jeszcze się nie rozpoczął. Wszelkie typy są objęte tajemnicą! 🔒")
        else:
            table_html = "<div class='match-card-clean'><table class='kricon-table' style='margin: 0;'><tr><th style='text-align:left; padding-left:15px;'>Mecz</th>"
            for p in players: table_html += f"<th>{p}</th>"
            table_html += "</tr>"
            
            for m_id in sorted(locked_matches, reverse=True):
                m = st.session_state.results[m_id]
                h_c = clean_and_sanitize_team_string(m['home'])
                a_c = clean_and_sanitize_team_string(m['away'])
                table_html += f"<tr><td style='white-space:nowrap; text-align:left; padding-left:15px;'><b style='color:#F97316;'>#{m_id}</b>&nbsp;&nbsp; {get_cdn_flag_img_html(h_c)} {h_c} <b>-</b> {a_c} {get_cdn_flag_img_html(a_c)}</td>"
                
                for p in players:
                    bet = st.session_state.bets.get(m_id, {}).get(p)
                    if bet: table_html += f"<td style='text-align:center; font-weight:bold; font-size:1.05rem;'>{bet[0]} : {bet[1]}</td>"
                    else: table_html += "<td style='text-align:center; color:#64748B;'>-</td>"
                table_html += "</tr>"
            table_html += "</table></div>"
            st.markdown(table_html, unsafe_allow_html=True)

    with tab4:
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
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)
            
        st.divider(); st.header("🏆 Ranking Drużyn z 3. Miejsc")
        if third_places_list:
            df_third = pd.DataFrame(third_places_list).sort_values(by=["Pkt", "RB", "BZ", "Zwyciestwa"], ascending=False).reset_index(drop=True)
            df_third.index += 1; third_rows = ""
            for idx, r in df_third.iterrows(): 
                rep_clean_third = clean_and_sanitize_team_string(r['Reprezentacja'])
                third_rows += f"<tr {'style=\"background-color:#16A34A;\"' if idx <= 8 else ''}><td><b>{idx}</b></td><td><b>{r['Grupa']}</b></td><td>{get_cdn_flag_img_html(r['Reprezentacja'])} {rep_clean_third}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>"
            st.markdown(f"<table class='kricon-table'><tr><th>Msc.</th><th>Grupa</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{third_rows}</table>", unsafe_allow_html=True)

    with tab5:
        st.header("🏆 Drabinka Fazy Pucharowej")
        st.divider()
        
        c_g1, c_16l, c_8l, c_4l, c_2l, c_fin, c_2r, c_4r, c_8r, c_16r, c_g2 = st.columns([0.8, 1.1, 1.1, 1.1, 1.1, 2.0, 1.1, 1.1, 1.1, 1.1, 0.8])
        
        with c_g1:
            for g in ["A","B","C","D","E","F"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
            
        with c_16l:
            for i in range(73, 81): render_bracket_match_html_clean(i)
            
        with c_8l:
            render_bracket_match_html_clean(89, mt="34px", mb="68px")
            render_bracket_match_html_clean(90, mb="68px")
            render_bracket_match_html_clean(91, mb="68px")
            render_bracket_match_html_clean(92)
            
        with c_4l:
            render_bracket_match_html_clean(97, mt="106px", mb="210px")
            render_bracket_match_html_clean(98)
            
        with c_2l:
            render_bracket_match_html_clean(101, mt="248px")
            
        with c_fin:
            m_104 = st.session_state.results.get(104, {})
            h_f = clean_and_sanitize_team_string(m_104.get('home', 'TBD'))
            a_f = clean_and_sanitize_team_string(m_104.get('away', 'TBD'))
            sh_f = str(m_104.get('score_h')) if m_104.get('score_h') is not None else "?"
            sa_f = str(m_104.get('score_a')) if m_104.get('score_a') is not None else "?"
            
            st.markdown(f"""
            <div class='center-final-card-wrapper' style='margin-top: 195px;'>
                <div class='center-final-card'>
                    <div class='final-title'>🏆 WIELKI FINAŁ</div>
                    <div class='final-teams'>
                        <div class='final-team'>{get_cdn_flag_img_html(h_f)} <span class="bracket-team-name">{h_f}</span></div>
                        <div class='final-score'>{sh_f} : {sa_f}</div>
                        <div class='final-team'>{get_cdn_flag_img_html(a_f)} <span class="bracket-team-name">{a_f}</span></div>
                    </div>
                    <div class='final-venue'>📍 {m_104.get('venue', 'MetLife, Nowy Jork')} | 📅 {m_104.get('date', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='text-align:center; margin-top:20px; font-weight:bold; color:#94A3B8; font-size: 0.8rem;'>🥉 Mecz o 3. miejsce</div>", unsafe_allow_html=True)
            render_bracket_match_html_clean(103)
            
        with c_2r:
            render_bracket_match_html_clean(102, mt="248px")
            
        with c_4r:
            render_bracket_match_html_clean(99, mt="106px", mb="210px")
            render_bracket_match_html_clean(100)
            
        with c_8r:
            render_bracket_match_html_clean(93, mt="34px", mb="68px")
            render_bracket_match_html_clean(94, mb="68px")
            render_bracket_match_html_clean(95, mb="68px")
            render_bracket_match_html_clean(96)
            
        with c_16r:
            for i in range(81, 89): render_bracket_match_html_clean(i)
            
        with c_g2:
            for g in ["G","H","I","J","K","L"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
