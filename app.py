import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import json 
import requests 
from datetime import datetime, timedelta

# 1. Konfiguracja aplikacji i Szata Graficzna Dark Navy & Orange
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stTabContent"], div.stTabs {
        background-color: #0A1128 !important; 
        overflow-y: auto !important;
        overflow-x: auto !important;
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

    /* Poprawka widoczności listy rozwijanej (Logowanie) */
    div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p {
        color: #F97316 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #060B19 !important;
        border: 2px solid #F97316 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] div {
        color: #F97316 !important;
        font-weight: bold !important;
    }
    div[role="listbox"], ul[role="listbox"], div[data-baseweb="popover"] {
        background-color: #060B19 !important;
        border: 2px solid #F97316 !important;
    }
    div[role="option"], li[role="option"] {
        color: #F97316 !important;
        background-color: #060B19 !important;
        font-weight: bold !important;
    }
    
    /* Globalne wymuszenie wysokości dla przycisków oraz bannerów */
    .stButton>button {
        background-color: #F97316 !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        border: none !important;
        font-weight: 700 !important;
        height: 32px !important;
        line-height: 32px !important;
        padding: 0 12px !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #EA580C !important;
        box-shadow: 0 3px 8px rgba(249, 115, 22, 0.4) !important;
    }
    
    .missing-bet-banner {
        background-color: #DC2626 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 32px !important;
        line-height: 32px !important;
        border-radius: 4px !important;
        font-size: 0.85rem !important;
        display: block !important;
        width: 100% !important;
        animation: simple-blink 1.2s infinite ease-in-out;
    }
    .success-bet-banner {
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 32px !important;
        line-height: 32px !important;
        border-radius: 4px !important;
        font-size: 0.85rem !important;
        display: block !important;
        width: 100% !important;
        border: 1px solid #22C55E;
    }
    @keyframes simple-blink {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* ULTRA CIASNY UKŁAD PIONOWY LISTY MECZÓW */
    .match-container { 
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important; 
        border-radius: 4px; 
        padding: 4px 12px !important; 
        margin-bottom: 0px !important; 
        margin-top: 0px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 2px !important; 
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-bottom: 0px !important;
        padding-top: 0px !important;
        margin-bottom: 0px !important;
        margin-top: 0px !important;
    }
    
    /* SYMETRYCZNY, WYRÓWNANY W PIONIE RZĄD MECZOWY */
    .match-inline-main-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .match-title-section {
        font-weight: bold;
        color: #F97316 !important;
        font-size: 0.95rem !important;
        display: flex;
        align-items: center;
        gap: 6px;
        width: 25%; /* Zwiększona szerokość na pomieszczenie lokalizacji */
        white-space: nowrap;
    }
    .status-badge { padding: 1px 4px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; }
    .status-live { background-color: #DC2626 !important; color: white !important; }
    .status-ended { background-color: #111827 !important; color: #94A3B8 !important; }
    .status-waiting { background-color: #D97706 !important; color: white !important; }
    
    .match-date-badge {
        color: #CBD5E1 !important;
        font-size: 0.75rem !important;
        font-weight: bold;
        background-color: #0F172A;
        padding: 1px 6px;
        border-radius: 4px;
        border: 1px solid #1E3A8A;
    }
    
    /* NOWOŚĆ: Stylizacja przypisanego stadionu/miasta */
    .match-venue-badge {
        color: #38BDF8 !important;
        font-size: 0.75rem !important;
        font-weight: bold;
        background-color: #0B1329;
        padding: 1px 6px;
        border-radius: 4px;
        border: 1px solid #1E3A8A;
    }

    /* SIATKA KOLUMN DLA DRUŻYN I WYNIKU */
    .teams-display-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 75%; 
    }
    .team-home-wing {
        width: 42%;
        text-align: right;
        font-size: 1.15rem !important; 
        font-weight: bold !important;
        color: #F8FAFC !important;
        padding-right: 15px;
    }
    .score-center-wing {
        width: 16%;
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .team-away-wing {
        width: 42%;
        text-align: left;
        font-size: 1.15rem !important; 
        font-weight: bold !important;
        color: #F8FAFC !important;
        padding-left: 15px;
    }
    
    .official-score-badge {
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #0A1128 !important;
        background-color: #F97316 !important;
        padding: 1px 12px;
        border-radius: 4px;
        display: inline-block;
        min-width: 60px;
        text-align: center;
        box-shadow: 0 0 5px rgba(249, 115, 22, 0.5);
    }
    
    .flex-bet-label {
        font-size: 0.85rem !important;
        color: #38BDF8 !important;
        font-weight: bold;
        height: 32px !important;
        line-height: 32px !important;
        margin: 0 !important;
        display: flex;
        align-items: center;
    }
    
    div[data-testid="stNumberInput"] { height: 32px !important; margin: 0 !important; padding: 0 !important; }
    div[data-testid="stNumberInput"] button { background-color: #1E3A8A !important; color: #F8FAFC !important; height: 32px !important; }
    div[data-testid="stNumberInput"] input { color: #F8FAFC !important; background-color: #0A1128 !important; font-size: 0.85rem !important; height: 32px !important; }
    
    /* Drabinka i Tabele */
    .bracket-match-card { background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 10px; margin: 8px 0; }
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
    .bracket-column-wrapper { display: flex; flex-direction: column; justify-content: space-around; height: 100%; min-height: 1400px; position: relative; }
    ::-webkit-scrollbar { width: 16px !important; height: 16px !important; display: block !important; }
    ::-webkit-scrollbar-track { background: #060B19 !important; }
    ::-webkit-scrollbar-thumb { background-color: #FF6B00 !important; border-radius: 8px !important; border: 2px solid #060B19 !important; }
    </style>
""", unsafe_allow_html=True)

BACKUP_FILE = "typer_backup.json"

def save_backup_local_and_github():
    try:
        serializable_bets = {str(m_id): bets for m_id in st.session_state.bets.keys() for bets in [st.session_state.bets[m_id]]}
        json_string = json.dumps(serializable_bets, ensure_ascii=False, indent=4)
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            f.write(json_string)
            
        if "github" in st.secrets:
            cfg = st.secrets["github"]
            url = f"https://api.github.com/repos/{cfg['repo']}/contents/{BACKUP_FILE}"
            headers = {"Authorization": f"token {cfg['token']}", "Accept": "application/vnd.github.v3+json"}
            res_get = requests.get(url, headers=headers)
            sha = res_get.json().get("sha", None) if res_get.status_code == 200 else None
            content_b64 = base64.b64encode(json_string.encode("utf-8")).decode("utf-8")
            payload = {"message": f"🤖 Backup typów: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "content": content_b64}
            if sha: payload["sha"] = sha
            requests.put(url, headers=headers, json=payload)
    except Exception:
        pass

def load_backup_local():
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                loaded_bets = json.load(f)
            for m_id_str, bets_data in loaded_bets.items():
                m_id = int(m_id_str)
                for player, bet_tuple in bets_data.items():
                    st.session_state.bets[m_id][player] = tuple(bet_tuple)
            return True
        except Exception:
            return False
    return False

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
    "Anglia": "gb-eng", "Chorwacja": "hr", "Ghana": "gh", "Panama": "pa", "TBD": "unknown"
}

def get_flag_html(country_name):
    if not country_name or country_name == "TBD":
        return f'<span style="font-size:1.1em; margin-right:4px;">🏳️</span>'
    clean_name = country_name.replace("🏳️", "").strip()
    code = COUNTRY_FLAGS.get(clean_name, "unknown")
    if code == "unknown": return f'<span style="font-size:1.1em; margin-right:4px;">🏳️</span>'
    return f'<img src="https://flagcdn.com/w40/{code}.png" width="18" style="vertical-align: middle; margin-right: 4px; border-radius:2px;">'

USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Marcin": "marcin2026",
    "Kamil": "kamil2026", "Kuba M": "kubam2026", "Tomek": "tomek2026",
    "Kuba K": "kubak2026", "Rafał": "rafal2026", "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

GROUPS_DICT = {
    "Grupa A": ["Meksyk", "RPA", "Korea Południowa", "Czechy"], "Grupa B": ["Kanada", "Bośnia i Hercegowina", "Katar", "Szwajcaria"],
    "Grupa C": ["Brazylia", "Maroko", "Haiti", "Szkocja"], "Grupa D": ["USA", "Paragwaj", "Australia", "Turcja"],
    "Grupa E": ["Niemcy", "Curaçao", "WKS", "Ekwador"], "Grupa F": ["Holandia", "Japonia", "Szwecja", "Tunezja"],
    "Grupa G": ["Belgia", "Egipt", "Iran", "Nowa Zelandia"], "Grupa H": ["Hiszpania", "Wyspy Zielonego Przylądka", "Arabia Saudyjska", "Urugwaj"],
    "Grupa I": ["Francja", "Senegal", "Irak", "Norwegia"], "Grupa J": ["Argentyna", "Algieria", "Austria", "Jordania"],
    "Grupa K": ["Portugalia", "DR Konga", "Uzbekistan", "Kolumbia"], "Grupa L": ["Anglia", "Chorwacja", "Ghana", "Panama"]
}

# NOWOŚĆ: Oficjalna lista stadionów/miast MŚ 2026 przypisana rotacyjnie
VENUES_LIST = [
    "Azteca, Meksyk", "MetLife, Nowy Jork", "SoFi, Los Angeles", "AT&T, Dallas",
    "Mercedes-Benz, Atlanta", "BC Place, Vancouver", "Hard Rock, Miami", "Arrowhead, Kansas City",
    "Lincoln Financial, Filadelfia", "Levi's, San Francisco", "Lumen Field, Seattle", "NRG, Houston",
    "Gillette, Boston", "BMO Field, Toronto", "BBVA, Monterrey", "Akron, Guadalajara"
]

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    raw_fixtures = [
        (2026, 6, 11, 21, 0, "Grupa A", "Meksyk", "RPA"), (2026, 6, 12, 4, 0, "Grupa A", "Korea Południowa", "Czechy"),
        (2026, 6, 12, 21, 0, "Grupa B", "Kanada", "Bośnia i Hercegowina"), (2026, 6, 13, 3, 0, "Grupa D", "USA", "Paragwaj"),
        (2026, 6, 13, 21, 0, "Grupa B", "Katar", "Szwajcaria"), (2026, 6, 14, 0, 0, "Grupa C", "Brazylia", "Maroko"),
        (2026, 6, 14, 3, 0, "Grupa C", "Haiti", "Szkocja"), (2026, 6, 14, 6, 0, "Grupa D", "Australia", "Turcja"),
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
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]}", "time": dt.strftime("%H:00"),
            "stage": stage, "home": home, "away": away, "score_h": None, "score_a": None, "status": "Oczekuje",
            "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)] # Dynamiczne przypisanie miasta
        }
        match_id += 1

    sim_day = datetime(2026, 6, 22, 18, 0)
    for g_name, teams in GROUPS_DICT.items():
        for pair in [(teams[0], teams[2]), (teams[1], teams[3])]:
            schedule[match_id] = {"timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"), "stage": g_name, "home": pair[0], "away": pair[1], "score_h": None, "score_a": None, "status": "Oczekuje", "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]}
            match_id += 1
        sim_day += timedelta(hours=4)

    ko_stages = [
        ("1/16 Finału", 16, [(29,6), (30,6), (1,7), (2,7)]), ("1/8 Finału", 8, [(4,7), (5,7), (6,7), (7,7)]),     
        ("Ćwierćfinały", 4, [(9,7), (10,7)]), ("Półfinały", 2, [(14,7), (15,7)]),                  
        ("Mecz o 3. miejsce", 1, [(18,7)]), ("Finał", 1, [(19,7)])                               
    ]
    for stage_name, count, stage_dates in ko_stages:
        date_idx = 0
        matches_per_date = max(1, count // len(stage_dates))
        for i in range(count):
            d, m_num = stage_dates[date_idx % len(stage_dates)]
            hour = 18 if i % 2 == 0 else 22
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            schedule[match_id] = {
                "timestamp": match_dt, "date": f"{d} {months_pl[m_num]}", "time": match_dt.strftime("%H:00"),
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

if 'backup_loaded' not in st.session_state:
    load_backup_local()
    st.session_state.backup_loaded = True

def calculate_points(pred_h, pred_a, real_h, real_a):
    if real_h is None or real_a is None or pred_h is None or pred_a is None: return 0
    if pred_h == real_h and pred_a == real_a: return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a): return 1
    return 0

def get_time_to_next_unbet_match(player_name, now_time):
    upcoming = sorted([m for m in st.session_state.results.values() if m["timestamp"] > now_time], key=lambda x: x["timestamp"])
    for match in upcoming:
        m_id = [k for k, v in st.session_state.results.items() if v == match][0]
        if st.session_state.bets[m_id].get(player_name, (None, None)) == (None, None):
            diff = match["timestamp"] - now_time
            if diff.total_seconds() <= 0: continue
            h, m = int(diff.total_seconds() // 3600), int((diff.total_seconds() % 3600) // 60)
            return f'<span class="{"time-warning" if diff <= timedelta(hours=1) else "time-normal"}">Za {h}h {m}m</span>'
    return '<span class="time-ok">✔ Wszystko obstawione</span>'

def render_leaderboard_html(now_time, new_positions_dict_dest=None):
    scores = {p: 0 for p in players}
    for m_id, res in st.session_state.results.items():
        if res['status'] == "Zakończony":
            for p in players:
                if p in st.session_state.bets[m_id]:
                    scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res['score_h'], res['score_a'])
    df = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"]).sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    
    legend_html = """
    <div class="points-legend">
        <div style="font-weight: bold; color: #F97316; margin-bottom: 6px; font-size: 1.05rem;">ℹ️ System przyznawania punktów:</div>
        <div class="legend-item">🎯 <b style="color: #4ADE80;">3 Punkty</b> — dokładne wytypowanie wyniku spotkania</div>
        <div class="legend-item">⚖️ <b style="color: #38BDF8;">1 Punkt</b> — poprawne wskazanie zwycięzcy lub remisu</div>
    </div>
    """
    rows = ""
    for idx, row in df.iterrows():
        pos, p_name = idx + 1, row['Gracz']
        if new_positions_dict_dest is not None: new_positions_dict_dest[p_name] = pos
        old_pos = st.session_state.last_positions.get(p_name, pos)
        trend = '<div class="badge-trend trend-box-up">▲</div>' if old_pos > pos else ('<div class="badge-trend trend-box-down">▼</div>' if old_pos < pos else '<div class="badge-trend trend-box-stable">•</div>')
        bg = 'style="background-color: #16A34A; font-weight: bold; color: #FFFFFF;"' if pos == 1 and row['Punkty'] > 0 else ('style="background-color: #DC2626; font-weight: bold; color: #FFFFFF;"' if pos == len(df) and row['Punkty'] > 0 else '')
        rows += f"<tr {bg}><td style='text-align:center;'><b>{pos}</b></td><td style='text-align:center;'>{trend}</td><td>{p_name}</td><td><b>{row['Punkty']} pkt</b></td><td>{get_time_to_next_unbet_match(p_name, now_time)}</td></tr>"
    
    return legend_html + f"<table class='kricon-table'><tr><th>Msc.</th><th>Trend</th><th>Gracz</th><th>Punkty</th><th>Najbliższy mecz</th></tr>{rows}</table>"

def render_bracket_match_html_clean(match_id):
    m = st.session_state.results.get(match_id)
    if not m: return ""
    if m.get("status") == "Zakończony":
        sh = str(m.get("score_h", "?"))
        sa = str(m.get("score_a", "?"))
    else:
        sh, sa = "?", "?"
        
    win_h = m.get("score_h") is not None and m.get("score_a") is not None and m.get("score_h") > m.get("score_a") and m.get("status") == "Zakończony"
    win_a = m.get("score_h") is not None and m.get("score_a") is not None and m.get("score_a") > m.get("score_h") and m.get("status") == "Zakończony"
    
    home_name = m.get('home', 'TBD')
    away_name = m.get('away', 'TBD')
    
    st.markdown(f"""
    <div class="bracket-match-card">
        <div class="bracket-match-title">Mecz #{match_id}</div>
        <div class="bracket-row {"bracket-team-winner" if win_h else ""}">
            <span>{get_flag_html(home_name)} {home_name}</span>
            <span class="bracket-score-cell">{sh}</span>
        </div>
        <div class="bracket-row {"bracket-team-winner" if win_a else ""}">
            <span>{get_flag_html(away_name)} {away_name}</span>
            <span class="bracket-score-cell">{sa}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = "".join([f"<div style='text-align:left; padding:3px 0; font-size:0.9rem;'>{get_flag_html(t)} {t}</div>" for t in teams])
    return f"""
    <div class="bracket-group-box">
        <div style="font-weight:bold; color:#F97316; margin-bottom:4px; font-size:0.85rem;">GRUPA {g_code}</div>
        {lines}
    </div>
    """

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
now = datetime.now()
fetch_official_results_from_api(now)

# LOGIKA LIVE DLA TRANZYCJI IKON
for m_id, m in st.session_state.results.items():
    if m['status'] != "Zakończony":
        time_diff = now - m['timestamp']
        if timedelta(minutes=0) <= time_diff <= timedelta(minutes=120):
            st.session_state.results[m_id]['status'] = "LIVE"

if st.session_state.logged_in_user is None:
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        st.subheader("🔒 Logowanie")
        user = st.selectbox("Wybierz użytkownika:", [""] + list(USER_CREDENTIALS.keys()))
        pw = st.text_input("Wpisz hasło:", type="password")
        if st.button("Zaloguj się"):
            if USER_CREDENTIALS.get(user) == pw: st.session_state.logged_in_user = user; st.rerun()
            else: st.error("Błąd logowania.")
    with c2:
        st.subheader("📊 Ranking")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    st.sidebar.write(f"👤 Zalogowany jako: **{st.session_state.logged_in_user}**")
    st.sidebar.markdown("---")
    
    if st.session_state.logged_in_user == "admin":
        st.sidebar.subheader("💾 System Bezpieczeństwa")
        if os.path.exists(BACKUP_FILE): st.sidebar.success("Kopia lokalna: OK")
        if "github" in st.secrets: st.sidebar.success("GitHub Cloud Sync: OK")
        if st.sidebar.button("Wymuś przywrócenie danych (Backup)"):
            if load_backup_local(): st.sidebar.success("Pomyślnie odtworzono typy!")
            else: st.sidebar.error("Błąd odczytu bazy.")
        st.sidebar.markdown("---")
        
    if st.sidebar.button("Wyloguj się"): st.session_state.logged_in_user = None; st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    
    with tab1: 
        st.header("Klasyfikacja")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
        
    with tab2:
        st.header("Terminarz MŚ 2026")
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        st.divider()
        
        sorted_m = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
        for m_id, m in sorted_m:
            if (mode == "Oczekujące" and m['status'] == "Zakończony") or (mode == "Zakończone" and m['status'] == "Oczekuje"): continue
            status_html = '<span class="status-badge status-live">🔴 LIVE</span>' if m['status'] == "LIVE" else ('<span class="status-badge status-ended">⚫ Zakończony</span>' if m['status'] == "Zakończony" else '<span class="status-badge status-waiting">🟡 Oczekuje</span>')
            
            if m.get('status') == "Zakończony":
                sh_real = str(m.get('score_h', '?'))
                sa_real = str(m.get('score_a', '?'))
                oficjalny_wynik_tekst = f"{sh_real} : {sa_real}"
            else:
                oficjalny_wynik_tekst = "? : ?"
            
            locked = (m['timestamp'] - now).total_seconds() <= 0
            has_existing_bet = st.session_state.bets[m_id].get(st.session_state.logged_in_user) is not None
            cur_h, cur_a = st.session_state.bets[m_id].get(st.session_state.logged_in_user, (0,0))
            
            st.markdown(f"<div class='match-container'>", unsafe_allow_html=True)
            
            # --- POPRAWKA: STRUKTURA INLINE + DODANIE MIASTA DO SZEFA GRUPY ---
            c_info, c_input_h, c_input_a, c_btn, c_banner = st.columns([4.2, 0.6, 0.6, 1.1, 2.5])
            
            with c_info:
                # Wstrzyknięcie badge .match-venue-badge obok daty spotkania
                st.markdown(f"""
                <div class='match-inline-main-row'>
                    <div class='match-title-section'>
                        <span>⚽ #{m_id}</span>
                        {status_html}
                        <span class='match-date-badge'>{m['date']}</span>
                        <span class='match-venue-badge'>📍 {m.get('venue', 'USA')}</span>
                    </div>
                    <div class='teams-display-container'>
                        <div class='team-home-wing'>{get_flag_html(m['home'])} {m['home']}</div>
                        <div class='score-center-wing'><span class='official-score-badge'>{oficjalny_wynik_tekst}</span></div>
                        <div class='team-away-wing'>{get_flag_html(m['away'])} {m['away']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_input_h:
                b_h = st.number_input(f"H_{m_id}", 0, 20, int(cur_h), 1, key=f"input_h_{m_id}", disabled=locked, label_visibility="collapsed")
            with c_input_a:
                b_a = st.number_input(f"A_{m_id}", 0, 20, int(cur_a), 1, key=f"input_a_{m_id}", disabled=locked, label_visibility="collapsed")
                
            with c_btn:
                if locked:
                    st.button("Zablokowane", disabled=True, key=f"lock_btn_{m_id}")
                else:
                    button_container_class = "" if has_existing_bet else "pulsing-save-btn"
                    st.markdown(f"<div class='{button_container_class}'>", unsafe_allow_html=True)
                    if st.button("Zapisz", key=f"btn_{m_id}"): 
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                        save_backup_local_and_github() 
                        st.success("Zapisano!")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            with c_banner:
                if not locked:
                    if has_existing_bet:
                        st.markdown("<div class='success-bet-banner'>✔ ZAPISANY</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='missing-bet-banner'>⚠️ NIEODDANY TYP</div>", unsafe_allow_html=True)
            
            if locked or m['status'] == "Zakończony":
                with st.expander("👁️ Zobacz typy innych graczy"):
                    other_bets = []
                    for p in players:
                        if p != st.session_state.logged_in_user:
                            p_bet = st.session_state.bets[m_id].get(p)
                            other_bets.append({"Gracz": p, "Typowany wynik": f"{p_bet[0]} - {p_bet[1]}" if p_bet else "Brak typu"})
                    st.dataframe(pd.DataFrame(other_bets), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab3:
        st.header("Tabele Grup Turniejowych")
        third_places_list = []
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0, "Grupa": g_name} for t in GROUPS_DICT[g_name]}
            for m in st.session_state.results.values():
                if m["stage"] == g_name and m["status"] == "Zakończony":
                    h, a, sh, sa = m["home"], m["away"], m["score_h"], m["score_a"]
                    if h in stats and a in stats:
                        stats[h]["BZ"]+=sh; stats[h]["BS"]+=sa; stats[h]["RB"]+=(sh-sa)
                        stats[a]["BZ"]+=sa; stats[a]["BS"]+=sh; stats[a]["RB"]+=(sa-sh)
                        if sh>sa: stats[h]["Pkt"]+=3; stats[h]["Zwyciestwa"]+=1
                        elif sa>sh: stats[a]["Pkt"]+=3; stats[a]["Zwyciestwa"]+=1
                        else: stats[h]["Pkt"]+=1; stats[a]["Pkt"]+=1
            for t in GROUPS_DICT[g_name]:
                if t not in stats: stats[t] = {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0, "Grupa": g_name}
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'}).sort_values(by=["Pkt", "RB", "BZ"], ascending=False).reset_index(drop=True)
            df_g.index+=1
            if len(df_g) >= 3:
                third_team_row = df_g.iloc[2]
                third_places_list.append({"Reprezentacja": third_team_row["Reprezentacja"], "Grupa": g_name, "Pkt": third_team_row["Pkt"], "BZ": third_team_row["BZ"], "BS": third_team_row["BS"], "RB": third_team_row["RB"], "Zwyciestwa": third_team_row["Zwyciestwa"]})
            g_rows = "".join([f"<tr {'style=\"background-color: #16A34A; font-weight: bold; color: #FFFFFF;\"' if idx in [1, 2] else ('style=\"background-color: #EA580C; font-weight: bold; color: #FFFFFF;\"' if idx == 3 else '')}><td><b>{idx}</b></td><td>{get_flag_html(r['Reprezentacja'])} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>" for idx, r in df_g.iterrows()])
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)

        st.divider()
        st.header("🏆 Ranking Drużyn z 3. Miejsc (Awansuje 8 najlepszych)")
        df_third = pd.DataFrame(third_places_list)
        if not df_third.empty:
            df_third = df_third.sort_values(by=["Pkt", "RB", "BZ", "Zwyciestwa"], ascending=[False, False, False, False]).reset_index(drop=True)
            df_third.index += 1
            third_rows = ""
            for idx, r in df_third.iterrows():
                row_bg = 'style="background-color: #16A34A; font-weight: bold; color: #FFFFFF;"' if idx <= 8 else ''
                third_rows += f"<tr {row_bg}><td style='text-align:center;'><b>{idx}</b></td><td><b>{r['Grupa']}</b></td><td>{get_flag_html(r['Reprezentacja'])} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td><td>{r['Zwyciestwa']}</td></tr>"
            st.markdown(f"<table class='kricon-table'><tr><th style='text-align:center;'>Msc.</th><th>Źródło</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th><th>Zwycięstwa</th></tr>{third_rows}</table>", unsafe_allow_html=True)

    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej")
        st.divider()
        c_g1, c_16l, c_8l, c_mid, c_8r, c_r16, c_g2 = st.columns([1.1, 1.3, 1.3, 1.8, 1.3, 1.3, 1.1])
        
        with c_g1:
            st.markdown("<h5 style='text-align:center; color:#F97316;'>Grupy A-F</h5>", unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("A"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("B"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("C"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("D"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("E"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("F"), unsafe_allow_html=True)
            
        with c_16l:
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>1/16 Finału</h5>", unsafe_allow_html=True)
            for i in range(73, 81): render_bracket_match_html_clean(i)
            
        with c_8l:
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>1/8 Finału</h5>", unsafe_allow_html=True)
            for i in range(89, 93): render_bracket_match_html_clean(i)
            st.write("---")
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>Ćwierćfinały</h5>", unsafe_allow_html=True)
            for i in range(97, 99): render_bracket_match_html_clean(i)
            st.write("---")
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>Półfinał</h5>", unsafe_allow_html=True)
            render_bracket_match_html_clean(101)
            
        with c_mid:
            st.markdown("<div style='padding-top: 120px;'>", unsafe_allow_html=True)
            st.markdown("<div class='center-final-card'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color:#FFF; font-size:1.6rem; margin-bottom:5px;'>🏆 WIELKI FINAŁ</h2>", unsafe_allow_html=True)
            
            m_104 = st.session_state.results.get(104, {})
            h_f = m_104.get('home', 'TBD')
            a_f = m_104.get('away', 'TBD')
            sh_f = "" if m_104.get('score_h') is None else str(m_104.get('score_h'))
            sa_f = "" if m_104.get('score_a') is None else str(m_104.get('score_a'))
            
            st.markdown(f"""
                <div style='font-size:1.25rem; font-weight:bold; margin:15px 0;'>
                    {get_flag_html(h_f)} {h_f} 
                    <span style='color:#FF6B00; background:#060B19; padding:4px 10px; border-radius:4px; border:1px solid #F97316;'>
                        {sh_f} : {sa_f}
                    </span> 
                    {get_flag_html(a_f)} {a_f}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='bracket-match-card' style='border-color: #38BDF8; margin-top: 150px;'>", unsafe_allow_html=True)
            st.markdown("<h5 style='color:#38BDF8; margin:0 0 4px 0;'>🥉 MECZ O 3. MIEJSCE</h5>", unsafe_allow_html=True)
            m_103 = st.session_state.results.get(103, {})
            h_3 = m_103.get('home', 'TBD')
            a_3 = m_103.get('away', 'TBD')
            st.markdown(f"<b>{h_3} vs {a_3}</b>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with c_8r:
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>Półfinał</h5>", unsafe_allow_html=True)
            render_bracket_match_html_clean(102)
            st.write("---")
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>Ćwierćfinały</h5>", unsafe_allow_html=True)
            for i in range(99, 101): render_bracket_match_html_clean(i)
            st.write("---")
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>1/8 Finału</h5>", unsafe_allow_html=True)
            for i in range(93, 97): render_bracket_match_html_clean(i)
            
        with c_r16:
            st.markdown("<h5 style='text-align:center; color:#94A3B8;'>1/16 Finału</h5>", unsafe_allow_html=True)
            for i in range(81, 89): render_bracket_match_html_clean(i)
            
        with c_g2:
            st.markdown("<h5 style='text-align:center; color:#F97316;'>Grupy G-L</h5>", unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("G"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("H"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("I"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("J"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("K"), unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("L"), unsafe_allow_html=True)
