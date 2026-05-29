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
    
    /* GŁÓWNY, DUŻY, NEONOWO-POMARAŃCZOWY SUWAK CAŁEJ STRONY INTERNETOWEJ */
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
    
    /* DYNAMICZNE STATUSY WIELO-KOLOROWE */
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

    /* Tabele klasyczne i grupowe */
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
    
    /* Legenda Punktacji */
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
        return f'<span style="font-size:1.2em; margin-right:8px;">🏳️</span> {country_name}'
    flag_url = f"https://flagcdn.com/w40/{code}.png"
    return f'<img src="{flag_url}" width="22" style="vertical-align: middle; margin-right: 8px; border: 1px solid #1E3A8A; border-radius:2px;" alt="flaga">'

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
    all_groups = list(GROUPS_DICT.keys())
    sim_day = datetime(2026, 6, 22, 18, 0)
    while match_id <= 72:
        g_name = all_groups[(match_id % 12)]
        teams = GROUPS_DICT[g_name]
        h, a = (teams[0], teams[3]) if match_id % 2 == 0 else (teams[1], teams[2])
        schedule[match_id] = {
            "timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"),
            "stage": g_name, "home": h, "away": a, "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1
        if match_id % 4 == 0: sim_day += timedelta(days=1)
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
    
    # DODANA LEGENDA ZASAD PUNKTACJI
    legend_html = """
    <div class="points-legend">
        <div style="font-weight: bold; color: #F97316; margin-bottom: 6px; font-size: 1.05rem;">ℹ️ System przyznawania punktów:</div>
        <div class="legend-item">🎯 <b style="color: #4ADE80;">3 Punkty</b> — dokładne wytypowanie wyniku spotkania (np. wynik 2:1, typ 2:1)</div>
        <div class="legend-item">⚖️ <b style="color: #38BDF8;">1 Punkt</b> — poprawne wskazanie zwycięzcy lub remisu (np. wynik 3:1, typ 1:0)</div>
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
    
    table_html = f"<table class='kricon-table'><tr><th>Msc.</th><th>Trend</th><th>Gracz</th><th>Punkty</th><th>Najbliższy mecz</th></tr>{rows}</table>"
    return legend_html + table_html

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
now = datetime.now()

# LOGIKA DYNAMICZNEGO WYKRYWANIA MECZÓW LIVE
for m_id, m in st.session_state.results.items():
    if m['status'] != "Zakończony":
        time_diff = now - m['timestamp']
        if timedelta(minutes=0) <= time_diff <= timedelta(minutes=120):
            st.session_state.results[m_id]['status'] = "LIVE"
        elif time_diff > timedelta(minutes=120) and m['status'] == "LIVE":
            st.session_state.results[m_id]['status'] = "Oczekuje"

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "⚙️ Admin"])
    
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
            
            if m['status'] == "LIVE":
                status_html = '<span class="status-badge status-live">🔴 LIVE</span>'
            elif m['status'] == "Zakończony":
                status_html = '<span class="status-badge status-ended">⚫ Zakończony</span>'
            else:
                status_html = '<span class="status-badge status-waiting">🟡 Oczekuje</span>'
                
            st.markdown(f"""
            <div class='match-container'>
                <div class='match-header-wrapper'>
                    <h4 class='match-header-title'>⚽ Mecz #{m_id}</h4>
                    {status_html}
                </div>
                <div class='teams-display'>{get_flag_html(m['home'])} {m['home']} vs {get_flag_html(m['away'])} {m['away']}</div>
                <p style='color: #94A3B8; font-size: 1.05rem;'>Faza: {m['stage']} | {m['date']}, {m['time']}</p>
            """, unsafe_allow_html=True)
            
            if m['status'] == "Zakończony": 
                st.markdown(f"<p class='real-score'>Wynik końcowy: {m['score_h']} - {m['score_a']}</p>", unsafe_allow_html=True)
            
            locked = (m['timestamp'] - now).total_seconds() <= 0
            cur_h, cur_a = st.session_state.bets[m_id].get(st.session_state.logged_in_user, (0,0))
            
            c1, c2, c3 = st.columns([1,1,2])
            with c1: b_h = st.number_input(f"Wynik {m['home']}", 0, 20, cur_h, 1, key=f"h_{m_id}", disabled=locked)
            with c2: b_a = st.number_input(f"Wynik {m['away']}", 0, 20, cur_a, 1, key=f"a_{m_id}", disabled=locked)
            with c3: 
                st.write(""); st.write("")
                if not locked and st.button("Zapisz Typ", key=f"btn_{m_id}"): 
                    st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                    st.success("Zapisano!")
            
            if locked or m['status'] == "Zakończony":
                with st.expander("👁️ Zobacz typy innych graczy"):
                    other_bets = []
                    for p in players:
                        if p != st.session_state.logged_in_user:
                            p_bet = st.session_state.bets[m_id].get(p)
                            other_bets.append({
                                "Gracz": p, 
                                "Typowany wynik": f"{p_bet[0]} - {p_bet[1]}" if p_bet else "Brak typu"
                            })
                    st.dataframe(pd.DataFrame(other_bets), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
    with tab3:
        st.header("Tabele Grup Turniejowych")
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0} for t in GROUPS_DICT[g_name]}
            for m in st.session_state.results.values():
                if m["stage"] == g_name and m["status"] == "Zakończony":
                    h, a, sh, sa = m["home"], m["away"], m["score_h"], m["score_a"]
                    if h in stats and a in stats:
                        stats[h]["BZ"]+=sh; stats[h]["BS"]+=sa; stats[h]["RB"]+=(sh-sa)
                        stats[a]["BZ"]+=sa; stats[a]["BS"]+=sh; stats[a]["RB"]+=(sa-sh)
                        if sh>sa: stats[h]["Pkt"]+=3
                        elif sa>sh: stats[a]["Pkt"]+=3
                        else: stats[h]["Pkt"]+=1; stats[a]["Pkt"]+=1
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'}).sort_values(by=["Pkt", "RB", "BZ"], ascending=False).reset_index(drop=True)
            df_g.index+=1
            
            g_rows = ""
            for idx, r in df_g.iterrows():
                row_bg = ""
                if idx in [1, 2]:
                    row_bg = 'style="background-color: #16A34A; font-weight: bold; color: #FFFFFF;"'
                elif idx == 3:
                    row_bg = 'style="background-color: #EA580C; font-weight: bold; color: #FFFFFF;"'
                
                g_rows += f"""
                <tr {row_bg}>
                    <td><b>{idx}</b></td>
                    <td>{get_flag_html(r['Reprezentacja'])} {r['Reprezentacja']}</td>
                    <td><b>{r['Pkt']}</b></td>
                    <td>{r['BZ']}</td>
                    <td>{r['BS']}</td>
                    <td>{r['RB']}</td>
                </tr>
                """
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)
        
    with tab4:
        if st.session_state.logged_in_user == "admin":
            st.header("⚙️ Wprowadzanie oficjalnych wyników")
            for m_id, m in sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0])):
                st.markdown(f"<div class='match-container'>Mecz #{m_id} | {m['home']} vs {m['away']}", unsafe_allow_html=True)
                if "TBD" in m["home"] or "/" in m["stage"]:
                    c_h, c_a = st.columns(2)
                    with c_h: m["home"] = st.text_input("D1", m["home"], key=f"ad_h_{m_id}")
                    with c_a: m["away"] = st.text_input("D2", m["away"], key=f"ad_a_{m_id}")
                c1, c2, c3 = st.columns([1,1,2])
                with c1: rh = st.number_input("H", 0, 20, m['score_h'] if m['score_h'] is not None else 0, 1, key=f"rh_{m_id}")
                with c2: ra = st.number_input("A", 0, 20, m['score_a'] if m['score_a'] is not None else 0, 1, key=f"ra_{m_id}")
                with c3:
                    st.write(""); st.write("")
                    if st.button("Zatwierdź Wynik", key=f"rb_{m_id}"):
                        st.session_state.results[m_id]['score_h'] = rh
                        st.session_state.results[m_id]['score_a'] = ra
                        st.session_state.results[m_id]['status'] = "Zakończony"
                        
                        temp_p = {}
                        render_leaderboard_html(now, temp_p)
                        st.session_state.last_positions = temp_p
                        st.success("Zatwierdzono wynik!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
