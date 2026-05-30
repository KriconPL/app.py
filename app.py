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

# ANTY-COPY GUARD ORAZ PEŁNY SYSTEM STYLIZACJI POZIOMEJ KARTY MECZOWEJ
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
    
    /* SYSTEM ANIMACJI OPACITY DLA WSZYSTKICH ALERTÓW BLINK */
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
        height: 34px !important;
        line-height: 34px !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
        padding: 0 14px !important;
        white-space: nowrap !important;
        display: inline-block !important;
    }
    
    .status-waiting-blink {
        animation: pulseAlertCore 2.0s infinite ease-in-out !important;
        background-color: #D97706 !important;
        color: #FFFFFF !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        font-size: 0.7rem !important;
        white-space: nowrap !important;
        display: inline-block !important;
    }
    
    .success-bet-banner {
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 34px !important;
        line-height: 34px !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
        display: inline-block !important;
        padding: 0 14px !important;
        white-space: nowrap;
    }
    
    /* DETALE MECZU WEWNĄTRZ JEDNEGO WIERSZA BOXA */
    .meta-inline-box {
        display: flex;
        flex-direction: column;
        gap: 2px;
        font-size: 0.65rem !important;
        color: #64748B !important;
        white-space: nowrap;
        text-align: left;
        line-height: 1.2;
    }
    .meta-inline-id { font-weight: bold; color: #F97316 !important; font-size: 0.75rem !important; }
    
    /* CIEMNY BOX MECZOWY */
    .match-card-clean {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important; 
        border-radius: 4px; 
        padding: 12px 14px !important; 
        margin-bottom: 5px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    .team-text-align-right { font-size: 1.15rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; }
    .team-text-align-left { font-size: 1.15rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; }
    
    /* SUBTELNY WYNIK OFICJALNY */
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
        height: 34px !important;
        line-height: 34px !important;
        padding: 0 12px !important;
        width: 100%;
    }
    
    /* --- POWIĘKSZONE, BARDZIEJ WIDOCZNE SUWAKI INPUTÓW --- */
    div.stNumberInput { width: 110px !important; margin: 0 !important; padding: 0 !important; display: inline-block !important; }
    div.stNumberInput input { text-align: center !important; background-color: #0A1128 !important; color: #F8FAFC !important; height: 34px !important; font-size: 1.1rem !important; font-weight: bold !important; padding: 0 !important; border: 1px solid #1E3A8A !important; }
    div.stNumberInput button { height: 34px !important; width: 28px !important; background-color: #1E293B !important; color: #F97316 !important; border: 1px solid #334155 !important; }
    div.stNumberInput button:hover { background-color: #334155 !important; color: #FFFFFF !important; }
    
    /* FORMULARZOWY PRZYCISK ZAPISZ DLA KRICON */
    div.stButton button, div[data-testid="stBlock"] button {
        background-color: #F97316 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px !important; 
        border: 1px solid #EA580C !important; 
        font-weight: bold !important; 
        height: 34px !important; 
        line-height: 32px !important; 
        padding: 0 18px !important; 
        font-size: 0.9rem !important; 
        width: 100% !important;
        display: inline-block !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    div.stButton button:hover {
        background-color: #EA580C !important;
        border-color: #C2410C !important;
    }
    
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

def get_time_to_next_unbet_match(player_name, now_time):
    try:
        if 'results' not in st.session_state or 'bets' not in st.session_state: return "..."
        upcoming = sorted([m for m in st.session_state.results.values() if m["timestamp"] > now_time], key=lambda x: x["timestamp"])
        for match in upcoming:
            m_id = [k for k, v in st.session_state.results.items() if v == match][0]
            if st.session_state.bets.get(m_id, {}).get(player_name, (None, None)) == (None, None):
                diff = match["timestamp"] - now_time
                if diff.total_seconds() <= 0: continue
                h, m = int(diff.total_seconds() // 3600), int((diff.total_seconds() % 3600) // 60)
                return f'<span class="time-warning">Za {h}h {m}m</span>'
    except Exception: pass
    return '<span class="time-ok">✔ Wszystko obstawione</span>'

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
        trend = '▲' if old_pos > pos else ('▼' if old_pos < pos else '•')
        bg = 'style="background-color: #16A34A; font-weight: bold;"' if pos == 1 and row['Punkty'] > 0 else ('style="background-color: #DC2626; font-weight: bold;"' if pos == len(df) and row['Punkty'] > 0 else '')
        rows += f"<tr {bg}><td style='text-align:center;'><b>{pos}</b></td><td style='text-align:center;'>{trend}</td><td>{p_name}</td><td><b>{row['Punkty']} pkt</b></td><td>{get_time_to_next_unbet_match(p_name, now_time)}</td></tr>"
    return legend_html + f"<table class='kricon-table'><tr><th>Msc.</th><th>Trend</th><th>Gracz</th><th>Punkty</th><th>Najbliższy mecz</th></tr>{rows}</table>"

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
        lines += f"<div style='text-align:left; padding:3px 0; font-size:0.9rem; display:flex; align-items:center; gap:8px;'>{get_cdn_flag_img_html(t_clean)} <span>{t_clean}</span></div>"
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
        (2026, 6, 13, 21, 0, "Grupa B", "Katar", "Szwajcaria"), (2026, 6, 14, 0, 0, "Grupa C", "Brazylia", "Maroko")
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

if 'results' not in st.session_state: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
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
        
    # --- PRZYWRÓCENIE POPRAWNEGO RENDEROWANIA ZAKŁADEK (TABS FIX) ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    
    with tab1: 
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
        
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        for m_id, m in sorted(st.session_state.results.items()):
            
            status_html = '<span class="status-waiting-blink" style="animation: pulseAlertCore 2.0s infinite ease-in-out !important;">🟡 Oczekuje</span>'
            oficjalny_wynik_tekst = f"Wynik: {m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}"
            locked = (m['timestamp'] - now).total_seconds() <= 0
            has_existing_bet = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user) is not None
            cur_h, cur_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            home_clean = clean_and_sanitize_team_string(m['home'])
            away_clean = clean_and_sanitize_team_string(m['away'])
            
            # PANCERNY BOX MECZOWY: JEDNA IDEALNA LINIA W POZIOMIE
            st.markdown("<div class='match-card-clean'>", unsafe_allow_html=True)
            
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 1.8, 0.7, 0.7, 1.8, 1.1, 1.4])
            
            with c1:
                st.markdown(f"""
                <div class="meta-inline-box">
                    <span class="meta-inline-box meta-inline-id">Mecz #{m_id}</span>
                    <div>{status_html}</div>
                    <span>📅 {m['date']}</span>
                    <span>📍 {m.get('venue').split(',')[0]}</span>
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"<div class='team-text-align-right'><span>{home_clean}</span> {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
            with c3:
                b_h = st.number_input(f"H_{m_id}", 0, 20, int(cur_h), 1, key=f"h_{m_id}", label_visibility="collapsed")
            with c4:
                b_a = st.number_input(f"A_{m_id}", 0, 20, int(cur_a), 1, key=f"a_{m_id}", label_visibility="collapsed")
            with c5:
                st.markdown(f"<div class='team-text-align-left'>{get_cdn_flag_img_html(m['away'])} <span>{away_clean}</span></div>", unsafe_allow_html=True)
            with c6:
                st.markdown(f"<span class='official-score-subtle'>{oficjalny_wynik_tekst}</span>", unsafe_allow_html=True)
            with c7:
                st.markdown("<div class='action-horizontal-row' style='display:flex; flex-direction:column; gap:4px; align-items:center; width:100%;'>", unsafe_allow_html=True)
                if st.button("Zapisz", key=f"save_{m_id}"):
                    st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                    save_backup_local_and_github()
                    st.rerun()
                
                if has_existing_bet:
                    st.markdown("<div class='success-bet-banner'>✔ OK</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='missing-bet-banner-blink' style='animation: pulseAlertCore 1.2s infinite ease-in-out !important;'>⚠️ BRAK</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.header("Tabele Grup Turniejowych")
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0} for t in GROUPS_DICT[g_name]}
            df_g = pd.DataFrame.from_dict(stats, orient='index').reset_index().rename(columns={'index': 'Reprezentacja'})
            g_rows = ""
            for idx, r in df_g.iterrows():
                rep_clean = clean_and_sanitize_team_string(r['Reprezentacja'])
                g_rows += f"<tr><td><b>{idx+1}</b></td><td>{get_cdn_flag_img_html(r['Reprezentacja'])} {rep_clean}</td><td><b>0</b></td><td>0</td><td>0</td><td>0</td></tr>"
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)

    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej")
        c_g1, c_16l, c_mid = st.columns([1.5, 2.0, 2.0])
        with c_g1:
            for g in ["A","B"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
        with c_16l:
            render_bracket_match_html_clean(1)
        with c_mid:
            st.markdown("<div class='center-final-card'><h2>🏆 WIELKI FINAŁ</h2>TBD vs TBD</div>", unsafe_allow_html=True)
