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
    div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p { color: #F97316 !important; font-weight: bold !important; font-size: 1.2rem !important; }
    div[data-baseweb="select"], div[data-baseweb="input"] { background-color: #060B19 !important; border: 2px solid #F97316 !important; border-radius: 6px !important; }
    div[data-baseweb="select"] div { color: #F97316 !important; font-weight: bold; }
    div[role="listbox"], ul[role="listbox"], div[data-baseweb="popover"] { background-color: #060B19 !important; border: 2px solid #F97316 !important; }
    div[role="option"], li[role="option"] { color: #F97316 !important; background-color: #060B19 !important; font-weight: bold; }
    
    .stButton>button { background-color: #F97316 !important; color: #FFFFFF !important; border-radius: 4px !important; border: none !important; font-weight: 700 !important; height: 32px !important; line-height: 32px !important; padding: 0 12px !important; width: 100% !important; font-size: 0.85rem !important; }
    .stButton>button:hover { background-color: #EA580C !important; box-shadow: 0 3px 8px rgba(249, 115, 22, 0.4) !important; }
    
    /* NEONOWA ANIMACJA PULSOWANIA DLA BANERU ALERTÓW */
    @keyframes pulse-red-alert {
        0% { background-color: #DC2626; box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        50% { background-color: #EF4444; box-shadow: 0 0 0 8px rgba(220, 38, 38, 0); }
        100% { background-color: #DC2626; box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    
    .missing-bet-banner {
        animation: pulse-red-alert 1.5s infinite ease-in-out !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 32px !important;
        line-height: 32px !important;
        border-radius: 4px !important;
        font-size: 0.85rem !important;
        display: block !important;
        width: 100% !important;
        white-space: nowrap;
    }
    
    .success-bet-banner {
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 32px !important;
        line-height: 32px !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
        display: block !important;
        width: 100% !important;
        border: 1px solid #22C55E;
        white-space: nowrap;
    }
    
    .match-container { background: #172554 !important; border: 1px solid #1E3A8A !important; border-radius: 4px; padding: 4px 12px !important; margin-bottom: 2px !important; margin-top: 0px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.15); }
    div[data-testid="stVerticalBlock"] { gap: 0px !important; }
    div[data-testid="stVerticalBlock"] > div { padding-bottom: 0px !important; padding-top: 0px !important; margin-bottom: 0px !important; margin-top: 0px !important; }
    .match-top-meta-row { display: flex; align-items: center; gap: 10px; font-size: 0.75rem !important; color: #94A3B8 !important; margin-bottom: 6px; border-bottom: 1px dashed #1E3A8A; padding-bottom: 4px; }
    .match-id-text { font-weight: bold; color: #F97316 !important; }
    .status-badge { padding: 1px 4px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; color: white !important; }
    .status-live { background-color: #DC2626 !important; }
    .status-ended { background-color: #111827 !important; color: #94A3B8 !important; }
    .status-waiting { background-color: #D97706 !important; }
    .match-date-badge { color: #CBD5E1 !important; font-weight: bold; background-color: #0F172A; padding: 1px 4px; border-radius: 4px; }
    .match-venue-badge { color: #38BDF8 !important; font-weight: bold; background-color: #0B1329; padding: 1px 4px; border-radius: 4px; }
    .team-text-align-right { font-size: 1.1rem !important; font-weight: bold !important; text-align: right; display: block; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .team-text-align-left { font-size: 1.1rem !important; font-weight: bold !important; text-align: left; display: block; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .official-score-badge { font-size: 1.1rem !important; font-weight: 800 !important; color: #0A1128 !important; background-color: #F97316 !important; padding: 2px 10px; border-radius: 4px; display: block; text-align: center; width: 100%; height: 32px; line-height: 28px; }
    div[data-testid="stNumberInput"] { height: 32px !important; margin: 0 !important; padding: 0 !important; }
    div[data-testid="stNumberInput"] button { background-color: #1E3A8A !important; color: #F8FAFC !important; height: 32px !important; }
    div[data-testid="stNumberInput"] input { color: #F8FAFC !important; background-color: #0A1128 !important; font-size: 0.9rem !important; height: 32px !important; }
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
    </style>
""", unsafe_allow_html=True)

# --- SYSTEM MAPOWANIA DUAL-KEY (OBSŁUGUJE CZYSTE NAZWY ORAZ STARE ZAPISY Z PREFIKSAMI) ---
def get_flag_emoji(name):
    if not name or name == "TBD": return "🌐"
    s_name = str(name).strip()
    
    flags = {
        "Meksyk": "🇲🇽", "MX Meksyk": "🇲🇽", "RPA": "🇿🇦", "ZA RPA": "🇿🇦", 
        "Korea Południowa": "🇰🇷", "KR Korea Południowa": "🇰🇷", "Czechy": "🇨🇿", "cz Czechy": "🇨🇿",
        "Kanada": "🇨🇦", "CA Kanada": "🇨🇦", "Bośnia i Hercegowina": "🇧🇦", "BA Bośnia i Hercegowina": "🇧🇦", 
        "Katar": "🇶🇦", "QA Katar": "🇶🇦", "Szwajcaria": "🇨🇭", "CH Szwajcaria": "🇨🇭",
        "Brazylia": "🇧🇷", "BR Brazylia": "🇧🇷", "Maroko": "🇲🇦", "MA Maroko": "🇲🇦", 
        "Haiti": "🇭🇹", "HT Haiti": "🇭🇹", "Szkocja": "🏴\u200d☠️", "USA": "🇺🇸", "US USA": "🇺🇸", 
        "Paragwaj": "🇵🇾", "PY Paragwaj": "🇵🇾", "Australia": "🇦🇺", "AU Australia": "🇦🇺", 
        "Turcja": "🇹🇷", "TR Turcja": "🇹🇷", "Niemcy": "🇩🇪", "DE Niemcy": "🇩🇪", 
        "Curaçao": "🇨🇼", "WKS": "🇨🇮", "Ekwador": "🇪🇨", "EC Ekwador": "🇪🇨",
        "Holandia": "🇳🇱", "NL Holandia": "🇳🇱", "Japonia": "🇯🇵", "JP Japonia": "🇯🇵", 
        "Szwecja": "🇸🇪", "SE Szwecja": "🇸🇪", "Tunezja": "🇹🇳", "TN Tunezja": "🇹🇳",
        "Belgia": "🇧🇪", "BEL Belgia": "🇧🇪", "Egipt": "🇪🇬", "EGI Egipt": "🇪🇬", 
        "Iran": "🇮🇷", "IRA Iran": "🇮🇷", "Nowa Zelandia": "🇳🇿", "NZ Nowa Zelandia": "🇳🇿",
        "Hiszpania": "🇪🇸", "ESP Hiszpania": "🇪🇸", "Wyspy Zielonego Przylądka": "🇨🇻", "cv Wyspy Zielonego Przylądka": "🇨🇻", 
        "Arabia Saudyjska": "🇸🇦", "SA Arabia Saudyjska": "🇸🇦", "Urugwaj": "🇺🇾", "URU Urugwaj": "🇺🇾",
        "Francja": "🇫🇷", "FRA Francja": "🇫🇷", "Senegal": "🇸🇳", "SEN Senegal": "🇸🇳", 
        "Irak": "🇮🇶", "IRQ Irak": "🇮🇶", "Norwegia": "🇳🇴", "NOR Norwegia": "🇳🇴",
        "Argentyna": "🇦🇷", "ARG Argentyna": "🇦🇷", "Algieria": "🇩🇿", "ALG Algieria": "🇩🇿", 
        "Austria": "🇦🇹", "AUT Austria": "🇦🇹", "Jordania": "🇯🇴", "JOR Jordania": "🇯🇴",
        "Portugalia": "🇵🇹", "POR Portugalia": "🇵🇹", "DR Konga": "🇨🇩", "DRK DR Konga": "🇨🇩", 
        "Uzbekistan": "🇺🇿", "UZB Uzbekistan": "🇺🇿", "Kolumbia": "🇨🇴", "COL Kolumbia": "🇨🇴",
        "Anglia": "🏴\u200d󠁥󠁮󠁧󠁿", "ANG Anglia": "🏴\u200d󠁥󠁮󠁧󠁿", "Chorwacja": "🇭🇷", "CRO Chorwacja": "🇭🇷", 
        "Ghana": "🇬🇭", "GHA Ghana": "🇬🇭", "Panama": "🇵🇦", "PAN Panama": "🇵🇦"
    }
    return flags.get(s_name, "🌐")

def security_clean_text(val):
    if not isinstance(val, str): return val
    return re.sub(r'<[^>]*?>', '', val).strip()

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
    st.markdown(f"""<div class="bracket-match-card"><div class="bracket-match-title">Mecz #{match_id}</div><div class='bracket-row {"bracket-team-winner" if win_h else ""}'><span>{get_flag_emoji(m.get('home'))} {m.get('home')}</span><span class="bracket-score-cell">{sh}</span></div><div class='bracket-row {"bracket-team-winner" if win_a else ""}'><span>{get_flag_emoji(m.get('away'))} {m.get('away')}</span><span class="bracket-score-cell">{sa}</span></div></div>""", unsafe_allow_html=True)

def get_mini_group_html_string(g_code):
    teams = GROUPS_DICT.get(f"Grupa {g_code}", [])
    lines = "".join([f"<div style='text-align:left; padding:3px 0; font-size:0.9rem;'>{get_flag_emoji(t)} {t}</div>" for t in teams])
    return f"""<div class="bracket-group-box"><div style="font-weight:bold; color:#F97316; margin-bottom:4px; font-size:0.85rem;">GRUPA {g_code}</div>{lines}</div>"""

def save_backup_local_and_github():
    try:
        serializable_bets = {str(m_id): bets for m_id in st.session_state.bets.keys() for bets in [st.session_state.bets[m_id]]}
        json_string = json.dumps(serializable_bets, ensure_ascii=False, indent=4)
        with open("typer_backup.json", "w", encoding="utf-8") as f: f.write(json_string)
        if "github" in st.secrets:
            cfg = st.secrets["github"]
            url = f"https://api.github.com/repos/{cfg['repo']}/contents/typer_backup.json"
            headers = {"Authorization": f"token {cfg['token']}", "Accept": "application/vnd.github.v3+json"}
            res_get = requests.get(url, headers=headers)
            sha = res_get.json().get("sha", None) if res_get.status_code == 200 else None
            content_b64 = base64.b64encode(json_string.encode("utf-8")).decode("utf-8")
            payload = {"message": f"🤖 Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "content": content_b64}
            if sha: payload["sha"] = sha
            requests.put(url, headers=headers, json=payload)
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
            "timestamp": dt, "date": f"{dt.day} {months_pl[dt.month]} o {dt.strftime('%H:%M')}",
            "stage": security_clean_text(stage), "home": security_clean_text(home), "away": security_clean_text(away), "score_h": None, "score_a": None, "status": "Oczekuje",
            "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
        }
        match_id += 1
    sim_day = datetime(2026, 6, 22, 18, 0)
    for g_name, teams in GROUPS_DICT.items():
        for pair in [(teams[0], teams[2]), (teams[1], teams[3])]:
            schedule[match_id] = {"timestamp": sim_day, "date": f"{sim_day.day} {months_pl[sim_day.month]} o {sim_day.strftime('%H:%M')}", "stage": security_clean_text(g_name), "home": security_clean_text(pair[0]), "away": security_clean_text(pair[1]), "score_h": None, "score_a": None, "status": "Oczekuje", "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]}
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
                "timestamp": match_dt, "date": f"{d} {months_pl[m_num]} o {match_dt.strftime('%H:%M')}",
                "stage": security_clean_text(stage_name), "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, "status": "Oczekuje",
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

# --- ZASADNICZY SILNIK INICJALIZACJI SYSTEMU ---
if 'results' not in st.session_state or len(st.session_state.results) != 104: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state or len(st.session_state.bets) != 104: st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}
if 'last_positions' not in st.session_state: st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}

load_backup_local()
now = datetime.now()
fetch_official_results_from_api(now)

for m_id, m in st.session_state.results.items():
    if m.get('status') != "Zakończony":
        time_diff = now - m['timestamp']
        if timedelta(minutes=0) <= time_diff <= timedelta(minutes=120): st.session_state.results[m_id]['status'] = "LIVE"

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

# --- WIDOKI ---
if st.session_state.logged_in_user is None:
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        st.subheader("🔒 Logowanie")
        user = st.selectbox("Wybierz użytkownika:", [""] + list(USER_CREDENTIALS.keys()))
        pw = st.text_input("Wpisz hasło:", type="password")
        if st.button("Zaloguj się"):
            if USER_CREDENTIALS.get(user) == pw: 
                st.session_state.logged_in_user = user
                st.rerun()
            else: st.error("Błąd logowania.")
    with c2:
        st.subheader("📊 Ranking")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    st.sidebar.write(f"👤 Zalogowany jako: **{st.session_state.logged_in_user}**")
    if st.session_state.logged_in_user == "admin":
        st.sidebar.subheader("💾 System Bezpieczeństwa")
        if st.sidebar.button("Wymuś przywrócenie danych (Backup)"):
            if load_backup_local(): st.sidebar.success("Pomyślnie odtworzono typy!"); st.rerun()
            else: st.error("Błąd odczytu bazy.")
    if st.sidebar.button("Wyloguj się"): 
        st.session_state.logged_in_user = None
        st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📅 Terminarz", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    with tab1: st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
    with tab2:
        mode = st.radio("Widok:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        sorted_m = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
        for m_id, m in sorted_m:
            if (mode == "Oczekujące" and m.get('status') == "Zakończony") or (mode == "Zakończone" and m.get('status') == "Oczekuje"): continue
            status_html = '<span class="status-badge status-live">🔴 LIVE</span>' if m.get('status') == "LIVE" else ('<span class="status-badge status-ended">⚫ Zakończony</span>' if m.get('status') == "Zakończony" else '<span class="status-badge status-waiting">🟡 Oczekuje</span>')
            oficjalny_wynik_tekst = f"{m.get('score_h') if m.get('score_h') is not None else '?'} : {m.get('score_a') if m.get('score_a') is not None else '?'}"
            locked = (m['timestamp'] - now).total_seconds() <= 0
            has_existing_bet = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user) is not None
            cur_h, cur_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            flag_h_emoji = get_flag_emoji(m['home'])
            flag_a_emoji = get_flag_emoji(m['away'])
            
            st.markdown(f"<div class='match-container'><div class='match-top-meta-row'><span class='match-id-text'>⚽ Mecz #{m_id}</span>{status_html}<span class='match-date-badge'>📅 {m['date']}</span><span class='match-venue-badge'>📍 {m.get('venue', 'Stadion')}</span><span style='color:#64748B;'>({m['stage']})</span></div>", unsafe_allow_html=True)
            c_home, c_score, c_away, c_in_h, c_in_a, c_btn, c_banner = st.columns([2.2, 1.2, 1.2, 1.3, 1.3, 1.6, 2.5])
            
            with c_home: st.markdown(f"<span class='team-text-align-right'>{flag_h_emoji} {m['home']}</span>", unsafe_allow_html=True)
            with c_score: st.markdown(f"<span class='official-score-badge'>{oficjalny_wynik_tekst}</span>", unsafe_allow_html=True)
            with c_away: st.markdown(f"<span class='team-text-align-left'>{flag_a_emoji} {m['away']}</span>", unsafe_allow_html=True)
            
            with c_in_h: b_h = st.number_input(f"H_{m_id}", 0, 20, int(cur_h), 1, key=f"input_h_{m_id}", disabled=locked, label_visibility="collapsed")
            with c_in_a: b_a = st.number_input(f"A_{m_id}", 0, 20, int(cur_a), 1, key=f"input_a_{m_id}", disabled=locked, label_visibility="collapsed")
            with c_btn:
                if locked: st.button("Zablokowane", disabled=True, key=f"lock_btn_{m_id}")
                else:
                    if st.button("Zapisz", key=f"btn_{m_id}"):
                        if m_id not in st.session_state.bets: st.session_state.bets[m_id] = {}
                        st.session_state.bets[m_id][st.session_state.logged_in_user] = (b_h, b_a)
                        save_backup_local_and_github()
                        st.success("OK!")
                        st.rerun()
            with c_banner:
                if not locked:
                    if has_existing_bet: st.markdown("<div class='success-bet-banner'>✔ ZAPISANY</div>", unsafe_allow_html=True)
                    else: st.markdown("<div class='missing-bet-banner'>⚠️ NIEODDANY TYP</div>", unsafe_allow_html=True)
            if locked or m.get('status') == "Zakończony":
                with st.expander("👁️ Zobacz typy innych graczy"):
                    other_bets = [{"Gracz": p, "Typowany wynik": f"{st.session_state.bets.get(m_id, {}).get(p)[0]} - {st.session_state.bets.get(m_id, {}).get(p)[1]}" if st.session_state.bets.get(m_id, {}).get(p) else "Brak typu"} for p in players if p != st.session_state.logged_in_user]
                    st.dataframe(pd.DataFrame(other_bets), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    with tab3:
        st.header("Tabele Grup Turniejowych")
        third_places_list = []
        for g_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {g_name}")
            stats = {t: {"Pkt": 0, "BZ": 0, "BS": 0, "RB": 0, "Zwyciestwa": 0, "Grupa": g_name} for t in GROUPS_DICT[g_name]}
            for m in st.session_state.results.values():
                if m.get("stage") == g_name and m.get("status") == "Zakończony":
                    h = m.get("home")
                    a = m.get("away")
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
                f_emoji = get_flag_emoji(r['Reprezentacja'])
                row_style = 'style="background-color:#16A34A;"' if idx in [1, 2] else ('style="background-color:#EA580C;"' if idx == 3 else '')
                g_rows += f"<tr {row_style}><td><b>{idx}</b></td><td>{f_emoji} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>"
            st.markdown(f"<table class='kricon-table'><tr><th>Poz.</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{g_rows}</table>", unsafe_allow_html=True)
        st.divider(); st.header("🏆 Ranking Drużyn z 3. Miejsc")
        if third_places_list:
            df_third = pd.DataFrame(third_places_list).sort_values(by=["Pkt", "RB", "BZ", "Zwyciestwa"], ascending=False).reset_index(drop=True)
            df_third.index += 1; third_rows = ""
            for idx, r in df_third.iterrows(): 
                f_emoji = get_flag_emoji(r['Reprezentacja'])
                third_rows += f"<tr {'style=\"background-color:#16A34A;\"' if idx <= 8 else ''}><td><b>{idx}</b></td><td><b>{r['Grupa']}</b></td><td>{f_emoji} {r['Reprezentacja']}</td><td><b>{r['Pkt']}</b></td><td>{r['BZ']}</td><td>{r['BS']}</td><td>{r['RB']}</td></tr>"
            st.markdown(f"<table class='kricon-table'><tr><th>Msc.</th><th>Grupa</th><th>Kraj</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th></tr>{third_rows}</table>", unsafe_allow_html=True)
    with tab4:
        st.header("🏆 Drabinka Fazy Pucharowej"); st.divider()
        c_g1, c_16l, c_8l, c_mid, c_8r, c_r16, c_g2 = st.columns([1.1, 1.3, 1.3, 1.8, 1.3, 1.3, 1.1])
        with c_g1:
            for g in ["A","B","C","D","E","F"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
        with c_16l:
            for i in range(73, 81): render_bracket_match_html_clean(i)
        with c_8l:
            for i in range(89, 93): render_bracket_match_html_clean(i)
            st.write("---")
            for i in range(97, 99): render_bracket_match_html_clean(i)
            st.write("---"); render_bracket_match_html_clean(101)
        with c_mid:
            st.markdown("<div style='padding-top:120px;'><div class='center-final-card'><h2>🏆 WIELKI FINAŁ</h2>", unsafe_allow_html=True)
            m_104 = st.session_state.results.get(104, {})
            f_h_fin = get_flag_emoji(m_104.get('home',''))
            f_a_fin = get_flag_emoji(m_104.get('away',''))
            st.markdown(f"<b>{f_h_fin} {m_104.get('home','TBD')} vs {f_a_fin} {m_104.get('away','TBD')}</b><br><span class='official-score-badge' style='display:inline-block; width:auto;'>{m_104.get('score_h','?')} : {m_104.get('score_a','?')}</span>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
        with c_8r:
            render_bracket_match_html_clean(102); st.write("---")
            for i in range(99, 101): render_bracket_match_html_clean(i)
            st.write("---")
            for i in range(93, 97): render_bracket_match_html_clean(i)
        with c_r16:
            for i in range(81, 89): render_bracket_match_html_clean(i)
        with c_g2:
            for g in ["G","H","I","J","K","L"]: st.markdown(get_mini_group_html_string(g), unsafe_allow_html=True)
