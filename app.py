import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import json 
import re
from datetime import datetime, timedelta

# --- FUNKCJA KODOWANIA OBRAZKA BASE64 (DLA LOGO) ---
# Upewnij się, że plik 'typer_wizu.png' znajduje się w tym samym folderze!
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .kricon-logo-container {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        height: 110px; /* Wysokość unieruchomionego paska loga */
        width: 100%;
        margin-bottom: 20px;
    }}
    </style>
    '''
    return page_bg_img

# Próba wczytania loga z Base64. Jeśli pliku nie ma, aplikacja się nie wywali.
logo_html = ""
if os.path.exists("typer_wizu.png"):
    logo_html = set_png_as_page_bg("typer_wizu.png")
else:
    logo_html = "<div style='color: white; text-align: center; background: rgba(255,255,255,0.1); padding: 10px; margin-bottom: 15px;'>⚠️ Brak pliku typer_wizu.png w folderze! Wgraj go.</div>"

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

# GŁÓWNY SILNIK CSS - ZWIĘKSZONY padding-top DLA UNIERUCHOMIONEGO NAGŁÓWKA
st.markdown(f"""
    {logo_html}
    <style>
    * {{ -webkit-user-select: none !important; -moz-user-select: none !important; -ms-user-select: none !important; user-select: none !important; }}
    input, textarea, div[data-baseweb="input"] {{ -webkit-user-select: auto !important; -moz-user-select: auto !important; -ms-user-select: auto !important; user-select: auto !important; }}

    body, html, [data-testid="stAppViewContainer"] {{ background-color: #0A1128 !important; }}
    [data-testid="stHeader"] {{ background-color: #0A1128 !important; }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{ color: #F8FAFC !important; }}
    
    /* UNIERUCHOMIONY NAGŁÓWEK (STICKY HEADER) - KONTENER NA LOGO */
    div[data-testid="stToolbar"], div.stTabs {{ top: 130px !important; z-index: 99 !important; background-color: #0A1128 !important; }}
    
    .stAppHeader {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 130px; /* Zwiększona wysokość, by zmieścić loga i odstęp */
        background-color: #0A1128 !important;
        z-index: 100 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        padding-top: 10px;
    }}
    
    [data-testid="stAppViewContainer"] > section:nth-child(2) {{
        padding-top: 130px !important; /* Odstęp treści od unieruchomionego nagłówka */
    }}

    @keyframes pulseAlertCore {{ 0% {{ opacity: 1.0; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1.0; }} }}
    
    /* GŁÓWNY BOX MECZU */
    div[data-testid="stHorizontalBlock"]:has(.match-row-anchor) {{
        background: #172554 !important; border: 1px solid #1E3A8A !important; border-radius: 0 0 6px 6px; padding: 6px 10px !important; margin-bottom: 6px !important; align-items: center !important; box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    div[data-testid="stHorizontalBlock"]:has(.match-row-anchor) > div[data-testid="column"] {{ padding: 0 4px !important; }}
    
    .meta-upper-bar-container {{ background-color: #1E293B !important; border: 1px solid #1E3A8A !important; border-bottom: none !important; border-radius: 6px 6px 0 0; display: flex; align-items: center; gap: 12px; font-size: 0.75rem !important; color: #94A3B8 !important; padding: 6px 14px !important; width: 100%; margin-top: 10px !important; }}
    .meta-id-text-clean {{ font-weight: bold; color: #F97316 !important; }}
    
    .team-align-right {{ font-size: 1.15rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }}
    .team-align-left {{ font-size: 1.15rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }}
    
    .off-score {{ font-size: 0.85rem !important; font-weight: bold !important; color: #94A3B8 !important; background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px; display: block; text-align: center; white-space: nowrap; height: 38px !important; line-height: 36px !important; width: 100%; }}
    .score-colon {{ text-align: center; font-weight: bold; color: #F97316 !important; font-size: 1.4rem; height: 38px; line-height: 34px; width: 100%; }}
    
    /* INPUTY I TŁA LOGOWANIA (JASNIEJSZE INPUTY NA STARYM TLE) */
    div[data-testid="stTextInput"] > label {{ color: white !important; font-weight: bold; }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{ background-color: #F8FAFC !important; border: 1px solid #1E3A8A !important; border-radius: 6px !important; height: 42px; }}
    div[data-testid="stTextInput"] input {{ color: #0A1128 !important; -webkit-text-fill-color: #0A1128 !important; font-weight: 600; font-size: 1.1rem; }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{ background-color: #F8FAFC !important; border: 1px solid #1E3A8A !important; border-radius: 6px !important; height: 42px; }}
    div[data-testid="stSelectbox"] span {{ color: #0A1128 !important; font-weight: 600; font-size: 1.1rem; }}
    li[role="option"] {{ color: #0A1128 !important; }}

    /* INPUTY BRAMEK W MECZACH */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {{ background-color: #0A1128 !important; border: 1px solid #1E3A8A !important; border-radius: 6px !important; height: 38px !important; overflow: hidden; }}
    div[data-testid="stNumberInput"] input {{ color: #F8FAFC !important; -webkit-text-fill-color: #F8FAFC !important; background-color: #0A1128 !important; font-size: 1.25rem !important; font-weight: 900 !important; text-align: center !important; padding: 0 !important; }}
    div[data-testid="stNumberInput"] button {{ background-color: #1E293B !important; border-radius: 4px !important; width: 32px !important; height: 32px !important; margin: 2px !important; }}
    
    /* PRZYCISKI */
    button[kind="primary"] {{ background-color: #F97316 !important; border: 1px solid #EA580C !important; border-radius: 4px !important; height: 38px !important; width: 100% !important; }}
    button[kind="primary"] * {{ color: #FFFFFF !important; font-weight: bold !important; font-size: 1rem !important; }}
    button[kind="secondary"] {{ background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px !important; height: 38px !important; width: 100% !important; }}
    button[kind="secondary"] * {{ color: #F97316 !important; font-weight: bold !important; font-size: 1.1rem !important; }}
    
    /* STATUSY I TABELE */
    .bet-ok {{ background: #16A34A; color: white; text-align: center; font-weight: bold; border-radius: 4px; height: 38px; line-height: 38px; }}
    .bet-brak {{ background: #DC2626; color: white; text-align: center; font-weight: bold; border-radius: 4px; height: 38px; line-height: 38px; animation: pulseAlertCore 1.2s infinite; }}
    .kricon-table {{ width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }}
    .kricon-table th {{ background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; }}
    .kricon-table td {{ padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; }}
    .gold-medal-row {{ background-color: rgba(254, 240, 138, 0.95) !important; font-weight: bold; color: #0A1128 !important; }}
    .gold-medal-row * {{ color: #0A1128 !important; }}
    .flag-img {{ width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); }}

    /* DRABINKA (TAB 4) */
    .bracket-match-card {{ background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 10px; margin: 6px 0; }}
    .bracket-match-title {{ font-size: 0.75rem !important; color: #F97316 !important; font-weight: bold; margin-bottom: 4px; border-bottom: 1px solid #1E3A8A; }}
    .bracket-row {{ display: flex; justify-content: space-between; align-items: center; padding: 3px 0; }}
    .bracket-score-cell {{ background: #0A1128; color: #F97316; font-weight: bold; padding: 2px 8px; border-radius: 4px; }}
    .center-final-card {{ background: linear-gradient(145deg, #1E3A8A, #0A1128) !important; border: 2px solid #F97316 !important; border-radius: 12px; padding: 20px; text-align: center; margin-top: 195px; width: 100%; }}
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
    return s

def get_cdn_flag_img_html(team_name):
    c_name = clean_and_sanitize_team_string(team_name)
    if c_name == "TBD": return f'🌐'
    code = ISO_FLAGS_MAP.get(c_name, None)
    if code:
        return f'<img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.6/flags/4x3/{code}.svg" class="flag-img" />'
    return f'🌐'

def calculate_points(pred_h, pred_a, real_h, real_a):
    try:
        if int(pred_h) == int(real_h) and int(pred_a) == int(real_a): return 3
        if np.sign(int(pred_h) - int(pred_a)) == np.sign(int(real_h) - int(real_a)): return 1
    except (ValueError, TypeError): pass
    return 0

# --- INICJALIZACJA STRUKTURY DANYCH TURNIEJU ---
def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    raw_fixtures = [
        (2026, 6, 11, 21, 0, "Grupa A", "Meksyk", "RPA"), (2026, 6, 12, 4, 0, "Grupa A", "Korea Południowa", "Czechy"),
        (2026, 6, 12, 21, 0, "Grupa B", "Kanada", "Bośnia i Hercegowina"), (2026, 6, 13, 3, 0, "Grupa D", "USA", "Paragwaj"),
        (2026, 6, 13, 21, 0, "Grupa B", "Katar", "Szwajcaria"), (2026, 6, 14, 0, 0, "Grupa C", "Brazylia", "Maroko"),
        (2026, 6, 14, 3, 0, "Grupa C", "Szkocja", "Haiti"), (2026, 6, 14, 6, 0, "Grupa D", "Australia", "Turcja")
    ]
    for i, f in enumerate(raw_fixtures):
        match_id = i + 1
        dt = datetime(f[0], f[1], f[2], f[3], f[4])
        schedule[match_id] = {
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]} {dt.strftime('%H:%M')}",
            "stage": f[5], "home": f[6], "away": f[7], "score_h": None, "score_a": None, "status": "Zakończony" if match_id <= 3 else "Oczekuje",
            "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
        }
    # TBD dla Drabinki (Uproszczone ID)
    ko_ranges = {"1/16 Finału": (73, 88), "1/8 Finału": (89, 96), "Ćwierćfinały": (97, 100), "Półfinały": (101, 102), "Mecz o 3. miejsce": (103, 103), "Finał": (104, 104)}
    for stage, r in ko_ranges.items():
        for mid in range(r[0], r[1] + 1):
            schedule[mid] = {"timestamp": datetime(2026, 7, 1), "date": "1 Lipca 21:00", "stage": stage, "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, "status": "Oczekuje", "venue": "MetLife, Nowy Jork" if mid==104 else VENUES_LIST[(mid-1)%len(VENUES_LIST)]}
    return schedule

if 'results' not in st.session_state: st.session_state.results = generate_schedule()
# Wyniki testowe
st.session_state.results[1]["score_h"], st.session_state.results[1]["score_a"] = 3, 1
st.session_state.results[2]["score_h"], st.session_state.results[2]["score_a"] = 1, 1
st.session_state.results[3]["score_h"], st.session_state.results[3]["score_a"] = 0, 2

if 'bets' not in st.session_state: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
# Typy testowe Kuby (Dla trafenia 3pkt, 1pkt, 0pkt w meczach 1-3)
st.session_state.bets[1]["Kuba M"] = (3, 1)
st.session_state.bets[2]["Kuba M"] = (2, 1)
st.session_state.bets[3]["Kuba M"] = (1, 0)
st.session_state.bets[1]["Maciej"] = (1, 1)
st.session_state.bets[1]["Tomek"] = (2, 0)

# --- FUNKCJE RENDERUJĄCE ---
def render_bracket_match_html_clean(match_id):
    m = st.session_state.results.get(match_id, {})
    sh, sa = ("?", "?") if m.get("score_h") is None else (str(m.get("score_h")), str(m.get("score_a")))
    st.markdown(f"""
    <div class="bracket-match-card">
        <div class="bracket-match-title">Mecz #{match_id}</div>
        <div class="bracket-row">
            <div>{get_cdn_flag_img_html(m.get('home'))} {m.get('home')}</div>
            <div class="bracket-score-cell">{sh}</div>
        </div>
        <div class="bracket-row">
            <div>{get_cdn_flag_img_html(m.get('away'))} {m.get('away')}</div>
            <div class="bracket-score-cell">{sa}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- LOGOWANIE I GŁÓWNA STRUKTURA (LOGO WTRĄCONE JAKO FIXED PANE) ---
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    # --- LOGO WTRĄCONE DO STRONY LOGOWANIA ---
    st.markdown("<div class='kricon-logo-container'></div>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("🔒 Logowanie do Typera")
        user = st.selectbox("Wybierz profil", [""] + list(USER_CREDENTIALS.keys()))
        password = st.text_input("Hasło", type="password")
        if st.button("Zaloguj się", type="primary"):
            if user and USER_CREDENTIALS.get(user) == password:
                st.session_state.logged_in_user = user
                st.rerun()
            else: st.error("Błąd logowania")
else:
    # --- LOGO WTRĄCONE NA GÓRĘ GŁÓWNEJ STRONY (UNIERUCHOMIONE PRZEZ CSS) ---
    st.markdown("<div class='stAppHeader'><div class='kricon-logo-container'></div></div>", unsafe_allow_html=True)
    
    st.sidebar.write(f"Zalogowany: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Wyloguj się", type="secondary"):
        st.session_state.logged_in_user = None
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🏆 Drabinka"])
    
    with tab1:
        st.header("Ranking Graczy")
        scores = {p: 0 for p in players}
        for m_id, res in st.session_state.results.items():
            if res.get("status") == "Zakończony":
                for p in players:
                    if m_id in st.session_state.bets and p in st.session_state.bets[m_id]:
                        scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res.get("score_h"), res.get("score_a"))
        df = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"]).sort_values(by="Punkty", ascending=False).reset_index(drop=True)
        
        rows_h = ""
        for idx, row in df.iterrows():
            css = "class='gold-medal-row'" if idx == 0 else ""
            medal = "🥇 " if idx == 0 else "🥈 " if idx == 1 else "🥉 " if idx == 2 else ""
            rows_h += f"<tr {css}><td>{medal}{idx+1}</td><td>{row['Gracz']}</td><td><b>{row['Punkty']} pkt</b></td></tr>"
        st.markdown(f"<table class='kricon-table'><tr><th>Msc.</th><th>Gracz</th><th>Punkty</th></tr>{rows_h}</table>", unsafe_allow_html=True)

    with tab2:
        st.header("Terminarz i Typowanie")
        user = st.session_state.logged_in_user
        now = datetime.now()
        for m_id, m in st.session_state.results.items():
            locked = (m["timestamp"] - now).total_seconds() <= 0
            has_bet = m_id in st.session_state.bets and user in st.session_state.bets[m_id]
            s_h, s_a = st.session_state.bets[m_id].get(user, (0, 0))
            h_key, a_key = f"h_{m_id}", f"a_{m_id}"
            
            st.markdown(f"""
            <div class="meta-upper-bar-container">
                <span class="meta-id-text-clean">Mecz #{m_id}</span>
                <span style="color: {'#DC2626' if locked else '#F97316'}; font-weight: bold;">{m['status']} {'🔒' if locked else ''}</span>
                <span style="color:#94A3B8;">{m['date']}</span>
                <span style="color:#F97316;">📍 {m['venue']}</span>
            </div>
            <div class='match-row-anchor'></div>
            """, unsafe_allow_html=True)
            
            c_hm, c_ih, c_sep, c_ia, c_aw, c_of, c_act, c_st = st.columns([2.5, 1.8, 0.3, 1.8, 2.5, 1.8, 1.2, 1.5])
            with c_hm: st.markdown(f"<div class='team-align-right'>{m['home']} {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
            with c_ih: st.number_input("", 0, 20, key=h_key, label_visibility="collapsed") if not locked else st.markdown(f"<div class='stApp'><b>{s_h}</b></div>", unsafe_allow_html=True)
            with c_sep: st.markdown("<div class='score-colon'>:</div>", unsafe_allow_html=True)
            with c_ia: st.number_input("", 0, 20, key=a_key, label_visibility="collapsed") if not locked else st.markdown(f"<div class='stApp'><b>{s_a}</b></div>", unsafe_allow_html=True)
            with c_aw: st.markdown(f"<div class='team-align-left'>{get_cdn_flag_img_html(m['away'])} {m['away']}</div>", unsafe_allow_html=True)
            with c_of: st.markdown(f"<div class='off-score'>Oficjalny: {m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}</div>", unsafe_allow_html=True)
            with c_act:
                if not locked:
                    if st.button("Zapisz", key=f"s_{m_id}", type="primary"): st.session_state.bets[m_id][user] = (st.session_state[h_key], st.session_state[a_key]); st.rerun()
                else: st.write("🔒")
            with c_st:
                if has_bet: st.markdown("<div class='bet-ok'>✔ OK</div>", unsafe_allow_html=True)
                else: st.markdown("<div class='bet-brak'>⚠ BRAK</div>", unsafe_allow_html=True)
                
    with tab3: st.header("Tabele Grup"); st.info("Uzupełnij logikę liczenia tabel grupowych")
    
    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej")
        st.markdown("<br>", unsafe_allow_html=True)
        # Przykładowe symetryczne ułożenie
        c_16_1, c_16_2, c_8_1, c_4_1, c_2_1, c_fin, c_2_2, c_4_2, c_8_2, c_16_3, c_16_4 = st.columns([1.1]*11)
        
        with c_16_1: render_bracket_match_html_clean(73); render_bracket_match_html_clean(74); render_bracket_match_html_clean(75); render_bracket_match_html_clean(76)
        with c_16_2: render_bracket_match_html_clean(77); render_bracket_match_html_clean(78); render_bracket_match_html_clean(79); render_bracket_match_html_clean(80)
        with c_16_3: render_bracket_match_html_clean(81); render_bracket_match_html_clean(82); render_bracket_match_html_clean(83); render_bracket_match_html_clean(84)
        with c_16_4: render_bracket_match_html_clean(85); render_bracket_match_html_clean(86); render_bracket_match_html_clean(87); render_bracket_match_html_clean(88)
        
        with c_8_1: render_bracket_match_html_clean(89); render_bracket_match_html_clean(90); render_bracket_match_html_clean(91); render_bracket_match_html_clean(92)
        with c_8_2: render_bracket_match_html_clean(93); render_bracket_match_html_clean(94); render_bracket_match_html_clean(95); render_bracket_match_html_clean(96)
        
        with c_4_1: render_bracket_match_html_clean(97); render_bracket_match_html_clean(98)
        with c_4_2: render_bracket_match_html_clean(99); render_bracket_match_html_clean(100)
        
        with c_2_1: render_bracket_match_html_clean(101)
        with c_2_2: render_bracket_match_html_clean(102)
        
        with c_fin:
            st.markdown("<div class='bracket-match-title'>Mecz o 3. miejsce</div>", unsafe_allow_html=True); render_bracket_match_html_clean(103)
            m = st.session_state.results[104]
            sh, sa = ("?", "?") if m.get("score_h") is None else (str(m.get("score_h")), str(m.get("score_a")))
            st.markdown(f"""
            <div class='center-final-card'>
                <div style='color: #F8FAFC !important; font-size: 1.3rem; font-weight: 900; margin-bottom: 15px;'>🏆 WIELKI FINAŁ</div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>{get_cdn_flag_img_html(m['home'])} {m['home']}</div>
                    <div style='font-size: 1.8rem; font-weight: 900; color: #F97316 !important; background: #0A1128; padding: 5px 15px; border-radius: 8px;'>{sh} : {sa}</div>
                    <div>{get_cdn_flag_img_html(m['away'])} {m['away']}</div>
                </div>
                <div style='color: #94A3B8; font-size: 0.8rem; margin-top: 15px;'>MetLife, NY</div>
            </div>
            """, unsafe_allow_html=True)
