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
    /* Globalne wymuszenie wyświetlania głównego suwaka przeglądarki */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0A1128 !important; 
        overflow-y: auto !important;
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

    /* Formularz logowania - poprawki widoczności */
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
    div[data-baseweb="select"] div, div[data-baseweb="input"] input {
        color: #F97316 !important; 
        font-weight: bold !important;
        font-size: 1.1rem !important;
        -webkit-text-fill-color: #F97316 !important;
    }
    div[role="listbox"], ul[role="listbox"] {
        background-color: #060B19 !important;
        border: 1px solid #F97316 !important;
    }
    div[role="option"], li[role="option"], div[role="listbox"] * {
        color: #F97316 !important;
        background-color: #060B19 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    div[role="option"]:hover, li[role="option"]:hover {
        background-color: #F97316 !important;
        color: #0A1128 !important;
    }
    
    /* NEONOWO-POMARAŃCZOWY SUWAK BOCZNY */
    ::-webkit-scrollbar {
        width: 16px !important;
        display: block !important;
    }
    ::-webkit-scrollbar-track {
        background: #060B19 !important;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #FF6B00 !important;
        border-radius: 8px !important;
        border: 2px solid #060B19 !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #FF8833 !important;
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
    
    /* Przyciski KriCon */
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
    
    /* Karty meczów */
    .match-container {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* STYLE DIZAJNU DLA DRABINKI W FORMIE PAJĘCZYNY (SPÓJNE BLOCZKI) */
    .bracket-match-box {
        background: #172554 !important;
        border: 2px solid #1E3A8A !important;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
    }
    .bracket-group-box {
        background: #0D1B3E !important;
        border: 1px dashed #F97316 !important;
        border-radius: 8px;
        padding: 8px;
        margin-bottom: 12px;
        text-align: center;
    }
    .bracket-match-id {
        font-size: 0.75rem !important;
        color: #F97316 !important;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .bracket-team-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        font-size: 0.95rem !important;
    }
    .bracket-winner {
        color: #4ADE80 !important;
        font-weight: 900 !important;
    }
    .bracket-score {
        font-weight: bold;
        background: #0A1128;
        padding: 2px 6px;
        border-radius: 4px;
        color: #F97316;
    }
    
    /* Centralna komórka finałowa o specjalnym wyglądzie */
    .center-final-box {
        background: #23153C !important;
        border: 3px solid #FF6B00 !important;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
    }

    .match-header-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1E3A8A;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .match-header-title {
        color: #F97316 !important;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
    }
    .status-live {
        background-color: #DC2626 !important;
        color: white !important;
        animation: pulse-glow 1.5s infinite;
    }
    .status-ended {
        background-color: #111827 !important;
        color: #94A3B8 !important;
        border: 1px solid #374151;
    }
    .status-waiting {
        background-color: #D97706 !important;
        color: white !important;
    }
    
    @keyframes pulse-glow {
        0% { opacity: 1; box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        50% { opacity: 0.8; box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
        100% { opacity: 1; box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    
    .teams-display {
        font-size: 1.6rem !important;
        font-weight: bold !important;
        color: #F8FAFC !important;
        margin-top: 10px;
        margin-bottom: 5px;
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
        margin: 15px 0 35px 0;
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
        padding: 11px 12px;
        border-bottom: 1px solid #1E3A8A !important;
        color: #F8FAFC !important;
        vertical-align: middle;
    }
    
    .points-legend {
        background-color: #060B19;
        border: 1px solid #1E3A8A;
        border-left: 5px solid #F97316;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 15px;
    }
    .legend-item {
        margin: 4px 0;
        font-size: 0.95rem;
    }
    
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
    .time-ok { color: #4ADE80 !important; font-weight: bold; }
    .time-warning { color: #FF6B00 !important; font-weight: bold; }
    .time-normal { color: #CBD5E1 !important; }
    </style>
""", unsafe_allow_html=True)

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
        return f'<span style="font-size:1.1em; margin-right:4px;">🏳️</span>'
    flag_url = f"https://flagcdn.com/w40/{code}.png"
    return f'<img src="{flag_url}" width="18" style="vertical-align: middle; margin-right: 4px; border: 1px solid #1E3A8A; border-radius:2px;" alt="flaga">'

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

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    raw_fixtures = [
        (2026, 6, 11, 21, 0, "Grupa A", "Meksyk", "RPA"),
        (2026, 6, 12, 4, 0, "Grupa A", "Korea Południowa", "Czechy"),
        (2026, 6, 12, 21, 0, "Grupa B", "Kanada", "Bośnia i Hercegowina"),
        (2026, 6, 13, 3, 0, "Grupa D", "USA", "Paragwaj"),
        (2026, 6, 13, 21, 0, "Grupa B", "Katar", "Szwajcaria"),
        (2026, 6, 14, 0, 0, "Grupa C", "Brazylia", "Maroko"),
        (2026, 6, 14, 3, 0, "Grupa C", "Haiti", "Szkocja"),
        (2026, 6, 14, 6, 0, "Grupa D", "Australia", "Turcja"),
        (2026, 6, 14, 19, 0, "Grupa E", "Niemcy", "Curaçao"),
        (2026, 6, 14, 22, 0, "Grupa F", "Holandia", "Japonia"),
        (2026, 6, 15, 1, 0, "Grupa E", "WKS", "Ekwador"),
        (2026, 6, 15, 4, 0, "Grupa F", "Szwecja", "Tunezja"),
        (2026, 6, 15, 18, 0, "Grupa H", "Hiszpania", "Wyspy Zielonego Przylądka"),
        (2026, 6, 15, 21, 0, "Grupa G", "Belgia", "Egipt"),
        (2026, 6, 16, 0, 0, "Grupa H", "Arabia Saudyjska", "Urugwaj"),
        (2026, 6, 16, 3, 0, "Grupa G", "Iran", "Nowa Zelandia"),
        (2026, 6, 16, 21, 0, "Grupa I", "Francja", "Senegal"),
        (2026, 6, 17, 0, 0, "Grupa I", "Irak", "Norwegia"),
        (2026, 6, 17, 3, 0, "Grupa J", "Argentyna", "Algieria"),
        (2026, 6, 17, 6, 0, "Grupa J", "Austria", "Jordania"),
        (2026, 6, 17, 19, 0, "Grupa K", "Portugalia", "DR Konga"),
        (2026, 6, 17, 22, 0, "Grupa L", "Anglia", "Chorwacja"),
        (2026, 6, 18, 1, 0, "Grupa L", "Ghana", "Panama"),
        (2026, 6, 18, 4, 0, "Grupa K", "Uzbekistan", "Kolumbia"),
        (2026, 6, 18, 18, 0, "Grupa A", "Czechy", "RPA"),
        (2026, 6, 18, 21, 0, "Grupa B", "Szwajcaria", "Bośnia i Hercegowina"),
        (2026, 6, 19, 0, 0, "Grupa B", "Kanada", "Katar"),
        (2026, 6, 19, 3, 0, "Grupa A", "Meksyk", "Korea Południowa"),
        (2026, 6, 19, 21, 0, "Grupa D", "USA", "Australia"),
        (2026, 6, 20, 0, 0, "Grupa C", "Szkocja", "Maroko"),
        (2026, 6, 20, 3, 0, "Grupa C", "Brazylia", "Haiti"),
        (2026, 6, 20, 5, 0, "Grupa D", "Turcja", "Paragwaj"),
        (2026, 6, 20, 19, 0, "Grupa F", "Holandia", "Szwecja"),
        (2026, 6, 20, 22, 0, "Grupa E", "Niemcy", "WKS"),
        (2026, 6, 21, 2, 0, "Grupa E", "Ekwador", "Curaçao"),
        (2026, 6, 21, 6, 0, "Grupa F", "Tunezja", "Japonia"),
        (2026, 6, 21, 18, 0, "Grupa H", "Hiszpania", "Arabia Saudyjska"),
        (2026, 6, 21, 21, 0, "Grupa G", "Belgia", "Iran"),
        (2026, 6, 22, 0, 0, "Grupa H", "Urugwaj", "Wyspy Zielonego Przylądka"),
        (2026, 6, 22, 3, 0, "Grupa G", "Nowa Zelandia", "Egipt")
    ]
    
    match_id = 1
    for yr, mo, dy, hr, mn, stage, home, away in raw_fixtures:
        dt = datetime(yr, mo, dy, hr, mn)
        schedule[match_id] = {
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]}", "time": dt.strftime("%H:00"),
            "stage": stage, "home": home, "away": away, "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1

    sim_day = datetime(2026, 6, 22, 18, 0)
    for g_name, teams in GROUPS_DICT.items():
        schedule[match_id] = {
            "timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"),
            "stage": g_name, "home": teams[0], "away": teams[2], "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1
        schedule[match_id] = {
            "timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"),
            "stage": g_name, "home": teams[1], "away": teams[3], "score_h": None, "score_a": None, "status": "Oczekuje"
        }
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
                "stage": stage_name, "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, "status": "Oczekuje"
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

if 'results' not in st.session_state or len(st.session_state.results) != 104:
    st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 104:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'last_positions' not in st.session_state:
    st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}

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

def render_bracket_match_html(match_id):
    m = st.session_state.results.get(match_id)
    if not m: return ""
    sh = "" if m["score_h"] is None else str(m["score_h"])
    sa = "" if m["score_a"] is None else str(m["score_a"])
    win_h = m["score_h"] is not None and m["score_a"] is not None and m["score_h"] > m["score_a"]
    win_a = m["score_h"] is not None and m["score_a"] is not None and m["score_a"] > m["score_h"]
    return f"""
    <div class="bracket-match-box">
        <div class="bracket-match-id">Mecz #{match_id}</div>
        <div class="bracket-team-line {"bracket-winner" if win_h else ""}">
            <span>{get_flag_html(m['home'])} {m['home']}</span><span class="bracket-score">{sh}</span>
        </div>
        <div class="bracket-team-line {"bracket-winner" if win_a else ""}">
            <span>{get_flag_html(m['away'])} {m['away']}</span><span class="bracket-score">{sa}</span>
        </div>
    </div>
    """

def render_mini_group_html(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = "".join([f"<div style='text-align:left; padding:2px 0;'>{get_flag_html(t)} {t}</div>" for t in teams])
    return f"""
    <div class="bracket-group-box">
        <div style="font-weight:bold; color:#F97316; margin-bottom:4px;">GRUPA {g_code}</div>
        {lines}
    </div>
    """

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
now = datetime.now()
fetch_official_results_from_api(now)

if st.session_state.logged_in_user is None:
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        st.subheader("🔒 Logowanie")
        user = st.selectbox("Użytkownik:", [""] + list(USER_CREDENTIALS.keys()))
        pw = st.text_input("Hasło:", type="password")
        if st.button("Zaloguj się"):
            if USER_CREDENTIALS.get(user) == pw: st.session_state.logged_in_user = user; st.rerun()
            else: st.error("Błąd logowania.")
    with c2:
        st.subheader("📊 Ranking")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    st.sidebar.write(f"👤: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Wyloguj"): st.session_state.logged_in_user = None; st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🕸️ Drabinka i Grupy"])
    
    with tab1: st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        sorted_m = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
        for m_id, m in sorted_m:
            if (mode == "Oczekujące" and m['status'] == "Zakończony") or (mode == "Zakończone" and m['status'] == "Oczekuje"): continue
            status_html = '<span class="status-badge status-live">🔴 LIVE</span>' if m['status'] == "LIVE" else ('<span class="status-badge status-ended">⚫ Zakończony</span>' if m['status'] == "Zakończony" else '<span class="status-badge status-waiting">🟡 Oczekuje</span>')
            st.markdown(f"<div class='match-container'><div class='match-header-wrapper'><h4 class='match-header-title'>⚽ Mecz #{m_id}</h4>{status_html}</div><div class='teams-display'>{get_flag_html(m['home'])} {m['home']} vs {get_flag_html(m['away'])} {m['away']}</div><p style='color: #94A3B8;'>Faza: {m['stage']} | {m['date']}, {m['time']}</p>", unsafe_allow_html=True)
            if m['status'] == "Zakończony": st.markdown(f"<p class='real-score'>Wynik: {m['score_h']} - {m['score_a']}</p>", unsafe_allow_html=True)
            locked = (m['timestamp'] - now).total_seconds() <= 0
            cur_h, cur_a = m_id, m_id # Placeholder key unique setup
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab3:
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
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'}).sort_values(by=["Pkt", "RB", "BZ"], ascending=False).reset_index(drop=True)
            df_g.index+=1
            if len(df_g) >= 3:
                third_team_row = df_g.iloc[2]
                third_places_list.append({"Reprezentacja": third_team_row["Reprezentacja"], "Grupa": g_name, "Pkt": third_team_row["Pkt"], "BZ": third_team_row["BZ"], "BS": third_team_row["BS"], "RB": third_team_row["RB"], "Zwyciestwa": third_team_row["Zwyciestwa"]})
            g_rows = "".join([f"<tr {'style=\"background-color: #16A34A; font-weight: bold; color: #FFFFFF;\"' if idx in [1, 2] else ('style=\"background-color: #EA580C; font-weight: bold; color: #FFFFFF;\"' if idx == 3 else '')}><td><b>{idx}</b></td><td>{get_flag_html(r['Reprezentacja'])} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>" for idx, r in df_g.iterrows()])
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)

    # --- NOWA STRUKTURA ZAKŁADKI 4: PAJĘCZYNA SKRZYDŁOWA (OD BRZEGÓW DO ŚRODKA) ---
    with tab4:
        st.header("🕸️ Skrzydłowa Drabinka i Faza Grupowa (Pajęczyna)")
        st.write("Fazy grupowe rozmieszczone są symetrycznie po bokach ekranu i schodzą się do Wielkiego Finału na samym środku.")
        st.divider()
        
        # Tworzymy symetryczny układ 7 kolumn (Lewe skrzydło -> Centrum -> Prawe skrzydło)
        w_g1, w_g2, w_g3, w_center, w_g4, w_g5, w_g6 = st.columns([1.2, 1.2, 1.2, 1.6, 1.2, 1.2, 1.2])
        
        with w_g1:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Grupy A-D</h4>", unsafe_allow_html=True)
            st.markdown(render_mini_group_html("A"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("B"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("C"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("D"), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/16 (Lewe)</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(73), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(74), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(75), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(76), unsafe_allow_html=True)

        with w_g2:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Grupy E-H</h4>", unsafe_allow_html=True)
            st.markdown(render_mini_group_html("E"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("F"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("G"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("H"), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/16 (Wew.)</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(77), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(78), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(79), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(80), unsafe_allow_html=True)

        with w_g3:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/8 Finału</h4>", unsafe_allow_html=True)
            st.write("")
            st.markdown(render_bracket_match_html(89), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(90), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Ćwierćfinał L</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(97), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(98), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Półfinał Lewy</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(101), unsafe_allow_html=True)

        # --- CENTRUM PAJĘCZYNY: WIELKI FINAŁ ORAZ MECZ O 3. MIEJSCE ---
        with w_center:
            st.markdown("<h3 style='text-align:center; color:#FF6B00;'>👑 CENTRUM TURNIEJU</h3>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            
            st.markdown("<div class='center-final-box'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color:#FFF; font-size:1.8rem; margin-bottom:10px;'>🏆 WIELKI FINAŁ</h2>", unsafe_allow_html=True)
            m_104 = st.session_state.results.get(104)
            sh_104 = "" if m_104["score_h"] is None else str(m_104["score_h"])
            sa_104 = "" if m_104["score_a"] is None else str(m_104["score_a"])
            st.markdown(f"""
                <div style='font-size:1.3rem; font-weight:bold; margin:15px 0;'>
                    {get_flag_html(m_104['home'])} {m_104['home']} <span style='color:#FF6B00; background:#000; padding:4px 10px; border-radius:4px;'>{sh_104} : {sa_104}</span> {get_flag_html(m_104['away'])} {m_104['away']}
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<span style='color:#94A3B8; font-size:0.85rem;'>Mecz #104 • {m_104['date']} {m_104['time']}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            st.write("")
            st.write("")
            
            st.markdown("<div class='bracket-match-box' style='border-color: #38BDF8;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#38BDF8; font-size:1.1rem; margin:0 0 8px 0;'>🥉 MECZ O 3. MIEJSCE</h4>", unsafe_allow_html=True)
            m_103 = st.session_state.results.get(103)
            sh_103 = "" if m_103["score_h"] is None else str(m_103["score_h"])
            sa_103 = "" if m_103["score_a"] is None else str(m_103["score_a"])
            st.markdown(f"""
                <div style='font-size:1.1rem; font-weight:bold;'>
                    {get_flag_html(m_103['home'])} {m_103['home']} <span style='color:#38BDF8;'>{sh_103}:{sa_103}</span> {get_flag_html(m_103['away'])} {m_103['away']}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with w_g4:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Półfinał Prawy</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(102), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Ćwierćfinał P</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(99), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(100), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/8 Finału</h4>", unsafe_allow_html=True)
            st.write("")
            st.markdown(render_bracket_match_html(91), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(92), unsafe_allow_html=True)

        with w_g5:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/16 (Wew.)</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(81), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(82), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(83), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(84), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Grupy I-L</h4>", unsafe_allow_html=True)
            st.markdown(render_mini_group_html("I"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("J"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("K"), unsafe_allow_html=True)
            st.markdown(render_mini_group_html("L"), unsafe_allow_html=True)

        with w_g6:
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>1/16 (Prawe)</h4>", unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(85), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(86), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(87), unsafe_allow_html=True)
            st.markdown(render_bracket_match_html(88), unsafe_allow_html=True)
            st.write("")
            st.markdown("<h4 style='text-align:center; color:#94A3B8;'>Wielkie Marki</h4>", unsafe_allow_html=True)
            st.info("Grupy rozpisane symetrycznie na skrzydłach bocznych.")
