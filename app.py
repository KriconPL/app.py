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

    /* Formularz logowania */
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
    
    /* --- SYSTEM POŁĄCZEŃ LINIAMI W DRABINCE (PAJĘCZYNA) --- */
    /* Wrapper kolumny wymuszający wyrównanie i relatywne pozycjonowanie linii */
    .bracket-column-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        height: 100%;
        min-height: 1400px; /* Wysokość gwarantująca przestrzeń na linie */
        position: relative;
    }
    
    /* Konstrukcja pojedynczego łącznika / bloczku meczu */
    .bracket-connector-cell {
        position: relative;
        padding: 10px 0;
        width: 100%;
    }
    
    /* Bloczki meczów */
    .bracket-match-box {
        background: #172554 !important;
        border: 2px solid #1E3A8A !important;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        position: relative;
        z-index: 2;
    }
    
    /* Linie poziome wychodzące w prawo (dla lewego skrzydła) */
    .left-wing-branch .bracket-match-box::after {
        content: "";
        position: absolute;
        top: 50%;
        right: -20px;
        width: 20px;
        height: 2px;
        background-color: #F97316;
        z-index: 1;
    }
    
    /* Linie poziome wchodzące z lewej (dla prawego skrzydła) */
    .right-wing-branch .bracket-match-box::before {
        content: "";
        position: absolute;
        top: 50%;
        left: -20px;
        width: 20px;
        height: 2px;
        background-color: #F97316;
        z-index: 1;
    }
    
    /* Pionowe linie scalające dla kolejnych rund (lewa strona) */
    .left-wing-connect::before {
        content: "";
        position: absolute;
        top: 12%;
        bottom: 12%;
        left: -20px;
        width: 2px;
        background-color: #F97316;
        z-index: 1;
    }
    
    /* Pionowe linie scalające dla kolejnych rund (prawa strona) */
    .right-wing-connect::after {
        content: "";
        position: absolute;
        top: 12%;
        bottom: 12%;
        right: -20px;
        width: 2px;
        background-color: #F97316;
        z-index: 1;
    }

    .bracket-group-box {
        background: #0D1B3E !important;
        border: 1px solid #F97316 !important;
        border-radius: 8px;
        padding: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
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
        padding: 2px 0;
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
    
    .center-final-box {
        background: #23153C !important;
        border: 3px solid #FF6B00 !important;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.5);
        margin-bottom: 30px;
    }
    /* ------------------------------------------------------------- */

    .match-container {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .status-live { background-color: #DC2626 !important; color: white !important; animation: pulse 1.5s infinite; }
    .status-ended { background-color: #111827 !important; color: #94A3B8 !important; }
    .status-waiting { background-color: #D97706 !important; color: white !important; }
    
    .teams-display { font-size: 1.6rem !important; font-weight: bold !important; }
    .real-score { font-size: 1.3rem; font-weight: bold; background-color: #F97316 !important; color: #0A1128 !important; padding: 6px 12px; border-radius: 6px; display: inline-block; }
    .kricon-table { width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }
    .kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; }
    .kricon-table td { padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; }
    .points-legend { background-color: #060B19; border-left: 5px solid #F97316; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    </style>
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
    "Anglia": "gb-eng", "Chorwacja": "hr", "Ghana": "gh", "Panama": "pa", "TBD": "unknown"
}

def get_flag_html(country_name):
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
        (2026, 6, 16, 21, 0, "Grupa I", "Francja", "Senegal"), (2026, 6, 17, 0, 0, "Grupa I", "Irak", "Norwegia"),
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
            "stage": stage, "home": home, "away": away, "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1

    sim_day = datetime(2026, 6, 22, 18, 0)
    for g_name, teams in GROUPS_DICT.items():
        schedule[match_id] = {"timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"), "stage": g_name, "home": teams[0], "away": teams[2], "score_h": None, "score_a": None, "status": "Oczekuje"}
        match_id += 1
        schedule[match_id] = {"timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]}", "time": sim_day.strftime("%H:00"), "stage": g_name, "home": teams[1], "away": teams[3], "score_h": None, "score_a": None, "status": "Oczekuje"}
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

if 'results' not in st.session_state or len(st.session_state.results) != 104: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 104: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'last_positions' not in st.session_state: st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}

def get_bracket_match_html_string(match_id):
    m = st.session_state.results.get(match_id)
    if not m: return ""
    sh = "" if m["score_h"] is None else str(m["score_h"])
    sa = "" if m["score_a"] is None else str(m["score_a"])
    win_h = m["score_h"] is not None and m["score_a"] is not None and m["score_h"] > m["score_a"]
    win_a = m["score_h"] is not None and m["score_a"] is not None and m["score_a"] > m["score_h"]
    return f"""
    <div class="bracket-connector-cell">
        <div class="bracket-match-box">
            <div class="bracket-match-id">Mecz #{match_id}</div>
            <div class="bracket-team-line {"bracket-winner" if win_h else ""}">
                <span>{get_flag_html(m['home'])} {m['home']}</span><span class="bracket-score">{sh}</span>
            </div>
            <div class="bracket-team-line {"bracket-winner" if win_a else ""}">
                <span>{get_flag_html(m['away'])} {m['away']}</span><span class="bracket-score">{sa}</span>
            </div>
        </div>
    </div>
    """

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = "".join([f"<div style='text-align:left; padding:2px 0; font-size:0.9rem;'>{get_flag_html(t)} {t}</div>" for t in teams])
    return f"""
    <div class="bracket-group-box">
        <div style="font-weight:bold; color:#F97316; margin-bottom:4px; font-size:0.85rem;">GRUPA {g_code}</div>
        {lines}
    </div>
    """

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🕸️ Drabinka Pajęczyna"])
    
    with tab1: st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        sorted_m = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
        for m_id, m in sorted_m:
            if (mode == "Oczekujące" and m['status'] == "Zakończony") or (mode == "Zakończone" and m['status'] == "Oczekuje"): continue
            status_html = '<span class="status-badge status-live">🔴 LIVE</span>' if m['status'] == "LIVE" else ('<span class="status-badge status-ended">⚫ Zakończony</span>' if m['status'] == "Zakończony" else '<span class="status-badge status-waiting">🟡 Oczekuje</span>')
            st.markdown(f"<div class='match-container'><div class='match-header-wrapper'><h4 class='match-header-title'>⚽ Mecz #{m_id}</h4>{status_html}</div><div class='teams-display'>{get_flag_html(m['home'])} {m['home']} vs {get_flag_html(m['away'])} {m['away']}</div><p style='color: #94A3B8;'>Faza: {m['stage']} | {m['date']}, {m['time']}</p>", unsafe_allow_html=True)
            if m['status'] == "Zakończony": st.markdown(f"<p class='real-score'>Wynik: {m['score_h']} - {m['score_a']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab3:
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0} for t in GROUPS_DICT[g_name]}
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
            g_rows = "".join([f"<tr {'style=\"background-color: #16A34A; font-weight: bold; color: #FFFFFF;\"' if idx in [1, 2] else ('style=\"background-color: #EA580C; font-weight: bold; color: #FFFFFF;\"' if idx == 3 else '')}><td><b>{idx}</b></td><td>{get_flag_html(r['Reprezentacja'])} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>" for idx, r in df_g.iterrows()])
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)

    # --- ZAKŁADKA 4: CZYSZCZENIE I RENDEROWANIE POŁĄCZEŃ LINIAMI ---
    with tab4:
        st.header("🕸️ Oficjalna Drabinka Skrzydłowa z Połączeniami")
        st.write("Wszystkie poziomy są spięte jaskrawymi liniami. Skrzydła schodzą się symetrycznie do środka.")
        st.divider()
        
        col_l_group, col_l_16, col_l_8, col_center, col_r_8, col_r_16, col_r_group = st.columns([1.2, 1.3, 1.3, 1.8, 1.3, 1.3, 1.2])
        
        with col_l_group:
            st.markdown("<div class='bracket-column-wrapper'>", unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("A") + get_mini_group_html_string("B") + get_mini_group_html_string("C") + get_mini_group_html_string("D") + get_mini_group_html_string("E") + get_mini_group_html_string("F"), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_l_16:
            st.markdown("<div class='bracket-column-wrapper left-wing-branch'>", unsafe_allow_html=True)
            html_l_16 = "".join([get_bracket_match_html_string(i) for i in range(73, 81)])
            st.markdown(html_l_16, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_l_8:
            st.markdown("<div class='bracket-column-wrapper left-wing-branch left-wing-connect'>", unsafe_allow_html=True)
            html_l_8 = "".join([get_bracket_match_html_string(i) for i in range(89, 93)])
            html_l_4 = "".join([get_bracket_match_html_string(i) for i in range(97, 99)])
            st.markdown(html_l_8 + "<hr style='border:1px dashed #F97316;'>" + html_l_4 + "<hr style='border:1px dashed #F97316;'>" + get_bracket_match_html_string(101), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_center:
            st.markdown("<div style='text-align: center; padding-top: 180px;'>", unsafe_allow_html=True)
            st.markdown("<div class='center-final-box'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color:#FFF; font-size:1.8rem; margin-bottom:10px;'>🏆 WIELKI FINAŁ</h2>", unsafe_allow_html=True)
            m_104 = st.session_state.results.get(104)
            st.markdown(f"""
                <div style='font-size:1.4rem; font-weight:bold; margin:15px 0;'>
                    {get_flag_html(m_104['home'])} {m_104['home']} 
                    <span style='color:#FF6B00; background:#060B19; padding:6px 14px; border-radius:4px; border:1px solid #F97316;'>
                        {"" if m_104['score_h'] is None else m_104['score_h']} : {"" if m_104['score_a'] is None else m_104['score_a']}
                    </span> 
                    {get_flag_html(m_104['away'])} {m_104['away']}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='bracket-match-box' style='border-color: #38BDF8; margin-top: 100px;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#38BDF8; margin:0 0 6px 0;'>🥉 MECZ O 3. MECZ</h4>", unsafe_allow_html=True)
            m_103 = st.session_state.results.get(103)
            st.markdown(f"<b>{m_103['home']} vs {m_103['away']}</b>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with col_r_8:
            st.markdown("<div class='bracket-column-wrapper right-wing-branch right-wing-connect'>", unsafe_allow_html=True)
            html_r_8 = "".join([get_bracket_match_html_string(i) for i in range(93, 97)])
            html_r_4 = "".join([get_bracket_match_html_string(i) for i in range(99, 101)])
            st.markdown(html_r_8 + "<hr style='border:1px dashed #F97316;'>" + html_r_4 + "<hr style='border:1px dashed #F97316;'>" + get_bracket_match_html_string(102), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_r_16:
            st.markdown("<div class='bracket-column-wrapper right-wing-branch'>", unsafe_allow_html=True)
            html_r_16 = "".join([get_bracket_match_html_string(i) for i in range(81, 89)])
            st.markdown(html_r_16, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_r_group:
            st.markdown("<div class='bracket-column-wrapper'>", unsafe_allow_html=True)
            st.markdown(get_mini_group_html_string("G") + get_mini_group_html_string("H") + get_mini_group_html_string("I") + get_mini_group_html_string("J") + get_mini_group_html_string("K") + get_mini_group_html_string("L"), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
