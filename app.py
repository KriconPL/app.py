import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import json 
import gspread
from datetime import datetime, timedelta

# 1. Konfiguracja aplikacji i Szata Graficzna Dark Navy & Orange
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# --- BEZPIECZNE WGRYWANIE LOGO BASE64 ---
logo_css = ""
if os.path.exists("logo.png"):
    with open("logo.png", 'rb') as f:
        bin_str = base64.b64encode(f.read()).decode()
    
    css_lines_logo = [
        ".kricon-logo-container { ",
        f"background-image: url('data:image/png;base64,{bin_str}'); ",
        "background-size: contain; background-repeat: no-repeat; ",
        "background-position: center; height: 220px; width: 100%; }"
    ]
    logo_css = "".join(css_lines_logo)
else:
    st.warning("⚠️ Brak pliku 'logo.png' w folderze aplikacji! Wgraj go, aby zobaczyć logo.")

# GŁÓWNY SILNIK CSS DLA CAŁEJ APLIKACJI
css_styles = [
    "<style>",
    logo_css,
    "* { -webkit-user-select: none !important; -moz-user-select: none !important; -ms-user-select: none !important; user-select: none !important; }",
    "input, textarea, div[data-baseweb='input'] { -webkit-user-select: auto !important; -moz-user-select: auto !important; -ms-user-select: auto !important; user-select: auto !important; }",
    "body, html, [data-testid='stAppViewContainer'], .stApp, [data-testid='stTabContent'], div.stTabs { background-color: #0A1128 !important; }",
    "[data-testid='stSidebar'] { background-color: #060B19 !important; }",
    "[data-testid='stHeader'] { background-color: #0A1128 !important; }",
    "h1, h2, h3, h4, h5, h6, p, span, label, div { color: #F8FAFC !important; }",
    ".stAppHeader { position: sticky !important; top: 0 !important; width: 100% !important; height: auto !important; background-color: #0A1128 !important; z-index: 9999 !important; padding-left: 25px !important; padding-right: 25px !important; padding-top: 18px !important; padding-bottom: 18px !important; border-bottom: 1px solid #1E3A8A; }",
    "[data-testid='stAppViewContainer'] > section:nth-child(2) { padding-top: 100px !important; }",
    "@keyframes blinker { 0% { background-color: #DC2626; opacity: 1.0; } 50% { background-color: #450A0A; opacity: 0.6; } 100% { background-color: #DC2626; opacity: 1.0; } }",
    "div[data-testid='stHorizontalBlock']:has(.match-row-anchor) { background: #172554 !important; border: 1px solid #1E3A8A !important; border-radius: 0 0 6px 6px; padding: 6px 10px !important; margin-bottom: 6px !important; align-items: center !important; box-shadow: 0 2px 4px rgba(0,0,0,0.15); }",
    "div[data-testid='stHorizontalBlock']:has(.match-row-anchor) > div[data-testid='column'] { padding: 0 4px !important; }",
    ".meta-upper-bar-container { background-color: #1E293B !important; border: 1px solid #1E3A8A !important; border-bottom: none !important; border-radius: 6px 6px 0 0; display: flex; align-items: center; gap: 12px; font-size: 0.75rem !important; color: #94A3B8 !important; padding: 4px 14px !important; width: 100%; margin-top: 10px !important; }",
    ".meta-id-text-clean { font-weight: bold; color: #F97316 !important; }",
    ".team-align-right { font-size: 1.15rem !important; font-weight: bold !important; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }",
    ".team-align-left { font-size: 1.15rem !important; font-weight: bold !important; text-align: left; display: flex; align-items: center; justify-content: flex-start; gap: 8px; width: 100%; white-space: nowrap; height: 38px; line-height: 38px; color: #F8FAFC !important; }",
    ".off-score { font-size: 0.85rem !important; font-weight: bold !important; color: #94A3B8 !important; background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px; display: block; text-align: center; white-space: nowrap; height: 38px !important; line-height: 36px !important; width: 100%; }",
    ".score-colon { text-align: center; font-weight: bold; color: #F97316 !important; font-size: 1.4rem; height: 38px; line-height: 34px; width: 100%; }",
    "div[data-testid='stSelectbox'] div[data-baseweb='select'] > div { background-color: #1E293B !important; border: 1px solid #334155 !important; }",
    "div[data-testid='stSelectbox'] div[data-baseweb='select'] span { color: #F8FAFC !important; }",
    "div[data-testid='stTextInput'] div[data-baseweb='input'] { background-color: #1E293B !important; border: 1px solid #334155 !important; }",
    "div[data-testid='stTextInput'] input { color: #F8FAFC !important; -webkit-text-fill-color: #F8FAFC !important; background-color: transparent !important; }",
    "div[data-testid='stNumberInput'] div[data-baseweb='input'] { background-color: #0A1128 !important; border: 1px solid #1E3A8A !important; border-radius: 6px !important; height: 38px !important; overflow: hidden; }",
    "div[data-testid='stNumberInput'] input { color: #F8FAFC !important; -webkit-text-fill-color: #F8FAFC !important; background-color: #0A1128 !important; font-size: 1.25rem !important; font-weight: 900 !important; text-align: center !important; padding: 0 !important; }",
    "div[data-testid='stNumberInput'] button { background-color: #1E293B !important; border: none !important; width: 32px !important; height: 32px !important; margin: 2px !important; }",
    "div[data-testid='stNumberInput'] button svg { fill: #F97316 !important; color: #F97316 !important; }",
    "button[kind='secondary'] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 4px !important; height: 38px !important; width: 100% !important; }",
    "button[kind='secondary'] * { color: #F97316 !important; font-weight: bold !important; font-size: 1.1rem !important; }",
    "button[kind='primary'] { background-color: #F97316 !important; border: 1px solid #EA580C !important; border-radius: 4px !important; height: 38px !important; width: 100% !important; }",
    "button[kind='primary'] * { color: #FFFFFF !important; font-weight: bold !important; }",
    "status-badge-ended { color: #94A3B8 !important; font-weight: bold; font-size: 0.65rem !important; }",
    ".status-badge-live { color: #DC2626 !important; font-weight: bold; font-size: 0.65rem !important; }",
    ".kricon-table { width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; background-color: #172554 !important; border-radius: 8px; overflow: hidden; }",
    ".kricon-table th { background-color: #F97316 !important; color: #0A1128 !important; padding: 12px; font-weight: 800; text-align: center; }",
    ".kricon-table td { padding: 11px 12px; border-bottom: 1px solid #1E3A8A !important; color: #F8FAFC; text-align: center; }",
    ".kricon-table td.team-cell { text-align: left !important; font-weight: bold; }",
    ".col-pos { width: 60px !important; text-align: center !important; }",
    ".col-trend { width: 60px !important; text-align: center !important; }",
    ".gold-medal-row { background-color: rgba(254, 240, 138, 0.95) !important; }",
    ".gold-medal-row td { color: #0A1128 !important; }",
    ".silver-medal-row { background-color: rgba(226, 232, 240, 0.95) !important; }",
    ".silver-medal-row td { color: #0A1128 !important; }",
    ".bronze-medal-row { background-color: rgba(254, 215, 170, 0.95) !important; }",
    ".bronze-medal-row td { color: #0A1128 !important; }",
    ".trend-up { color: #16A34A !important; font-weight: bold; }",
    ".trend-down { color: #DC2626 !important; font-weight: bold; }",
    ".trend-stable { color: #64748B !important; }",
    ".flag-img { width: 22px !important; height: 14px !important; object-fit: cover !important; border-radius: 2px !important; display: inline-block; vertical-align: middle; border: 1px solid rgba(255,255,255,0.2); margin-right: 6px; }",
    ".bracket-match-card { background: #172554 !important; border: 2px solid #1E3A8A !important; border-radius: 8px; padding: 6px; font-size: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }",
    ".bracket-match-title { font-size: 0.70rem !important; color: #F97316 !important; font-weight: bold; margin-bottom: 4px; border-bottom: 1px solid #1E3A8A; padding-bottom: 2px; }",
    ".bracket-row { display: flex; justify-content: space-between; align-items: center; padding: 2px 0; font-size: 0.85rem !important; }",
    ".bracket-score-cell { background: #0A1128; color: #F97316; font-weight: bold; padding: 1px 6px; border-radius: 4px; min-width: 22px; text-align: center; border: 1px solid #1E3A8A; }",
    ".bracket-team-winner { color: #4ADE80 !important; font-weight: bold; }",
    ".bracket-team-name { max-width: 60px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; vertical-align: middle; }",
    ".center-final-card-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; margin-top: 250px; }",
    ".center-final-card { background: linear-gradient(145deg, #1E3A8A, #0A1128) !important; border: 2px solid #F97316 !important; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 0 20px rgba(249,115,22,0.3); width: 100%; }",
    ".final-title { color: #F97316; font-size: 1.1rem; font-weight: 900; margin-bottom: 10px; text-transform: uppercase; }",
    ".final-teams { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 10px; }",
    ".final-team { font-size: 1.05rem; font-weight: bold; color: #F8FAFC; display: flex; align-items: center; gap: 6px; flex: 1; justify-content: center; }",
    ".final-score { font-size: 1.5rem; font-weight: 900; color: #F97316; background: #060B19; padding: 4px 12px; border-radius: 8px; border: 1px solid #334155; }",
    ".final-venue { font-size: 0.75rem; color: #94A3B8; }",
    "</style>"
]
st.markdown("".join(css_styles), unsafe_allow_html=True)

# 2. GLOBALNE PROFILE I CONFIG
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Kamil": "kamil2026", 
    "Kuba M": "kubam2026", "Tomek": "tomek2026", "Kuba K": "kubak2026", 
    "Rafał": "rafal2026", "admin": "kriconadmin"
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

def get_cdn_flag_img_html(team_name):
    if not team_name or team_name == "TBD": return '🌐'
    code = ISO_FLAGS_MAP.get(team_name.strip(), None)
    if code: return f"<img src='https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.4.6/flags/4x3/{code}.svg' class='flag-img' />"
    return '🌐'

def calculate_points(pred_h, pred_a, real_h, real_a):
    try:
        if real_h is None or real_a is None or pred_h is None or pred_a is None: return 0
        if int(pred_h) == int(real_h) and int(pred_a) == int(real_a): return 3
        if np.sign(int(pred_h) - int(pred_a)) == np.sign(int(real_h) - int(real_a)): return 1
    except (ValueError, TypeError): pass
    return 0

# --- 3. SILNIK GOOGLE CHMURY ---
@st.cache_resource
def get_gspread_client():
    creds_json = base64.b64decode(st.secrets["gcp_base64_creds"]).decode('utf-8')
    return gspread.service_account_from_dict(json.loads(creds_json))

def load_from_google_sheets():
    try:
        gc = get_gspread_client()
        sh = gc.open("Kricon_Typer_2026").sheet1
        all_records = sh.get_all_records()
        
        new_bets = {m_id: {} for m_id in range(1, 105)}
        for row in all_records:
            try:
                m_id = int(row["Mecz"])
                player = str(row["Gracz"]).strip()
                h = int(row["Typ_H"]) if str(row["Typ_H"]).strip() != "" else 0
                a = int(row["Typ_A"]) if str(row["Typ_A"]).strip() != "" else 0
                if player in players or player == "admin":
                    new_bets[m_id][player] = (h, a)
            except (ValueError, KeyError): continue
        st.session_state.bets = new_bets
        return True
    except Exception: return False

def save_to_google_sheets(m_id, user, h_val, a_val, action="save"):
    try:
        gc = get_gspread_client()
        sh = gc.open("Kricon_Typer_2026").sheet1
        all_records = sh.get_all_records()
        
        current_cloud_bets = {}
        for row in all_records:
            try:
                m = int(row["Mecz"])
                p = str(row["Gracz"]).strip()
                h_b = int(row["Typ_H"]) if str(row["Typ_H"]).strip() != "" else 0
                a_b = int(row["Typ_A"]) if str(row["Typ_A"]).strip() != "" else 0
                if m not in current_cloud_bets: current_cloud_bets[m] = {}
                current_cloud_bets[m][p] = (h_b, a_b)
            except (ValueError, KeyError): continue
                
        if action == "save":
            if m_id not in current_cloud_bets: current_cloud_bets[m_id] = {}
            current_cloud_bets[m_id][user] = (h_val, a_val)
        elif action == "delete":
            if m_id in current_cloud_bets and user in current_cloud_bets[m_id]:
                del current_cloud_bets[m_id][user]
                
        rows = [["Mecz", "Gracz", "Typ_H", "Typ_A"]]
        for m in sorted(current_cloud_bets.keys()):
            for p, tpl in current_cloud_bets[m].items():
                rows.append([m, p, tpl[0], tpl[1]])
                
        sh.clear()
        sh.update(range_name='A1', values=rows)
        
        if action == "save":
            if m_id not in st.session_state.bets: st.session_state.bets[m_id] = {}
            st.session_state.bets[m_id][user] = (h_val, a_val)
        elif action == "delete":
            if user in st.session_state.bets.get(m_id, {}): del st.session_state.bets[m_id][user]
        return True
    except Exception: return False

# CALLBACKI WYWOŁYWANE PRZY ZAPISIE
def handle_save(m_id, user, h_key, a_key):
    h = st.session_state.get(h_key, 0)
    a = st.session_state.get(a_key, 0)
    if save_to_google_sheets(m_id, user, h, a, action="save"):
        st.session_state.toast_msg = f"Zapisano typ {h}:{a} dla meczu #{m_id}! 💾"
    else:
        st.session_state.toast_msg = "Błąd połączenia z bazą! ❌"

def handle_delete(m_id, user, h_key, a_key):
    if save_to_google_sheets(m_id, user, 0, 0, action="delete"):
        st.session_state[h_key] = 0
        st.session_state[a_key] = 0
        st.session_state.toast_msg = f"Usunięto typ dla meczu #{m_id}! 🗑️"
    else:
        st.session_state.toast_msg = "Błąd usuwania! ❌"

# --- 4. SEKCJA LOGIKI TABEL GRUPOWYCH ---
def calculate_group_tables_html():
    # Inicjalizacja słownika statystyk drużyn
    stats = {}
    for g_name, teams in GROUPS_DICT.items():
        for t in teams:
            stats[t] = {"M": 0, "Pkt": 0, "Z": 0, "R": 0, "P": 0, "BZ": 0, "BS": 0, "Grupa": g_name}
            
    # Przetwarzanie meczów fazy grupowej (Mecze 1-72)
    for m_id in range(1, 73):
        m = st.session_state.results.get(m_id)
        if m and m.get("status") == "Zakończony" and m.get("score_h") is not None and m.get("score_a") is not None:
            h, a = m["home"], m["away"]
            sh, sa = int(m["score_h"]), int(m["score_a"])
            
            stats[h]["M"] += 1
            stats[a]["M"] += 1
            stats[h]["BZ"] += sh
            stats[h]["BS"] += sa
            stats[a]["BZ"] += sa
            stats[a]["BS"] += sh
            
            if sh > sa:
                stats[h]["Pkt"] += 3
                stats[h]["Z"] += 1
                stats[a]["P"] += 1
            elif sh < sa:
                stats[a]["Pkt"] += 3
                stats[a]["Z"] += 1
                stats[h]["P"] += 1
            else:
                stats[h]["Pkt"] += 1
                stats[a]["Pkt"] += 1
                stats[h]["R"] += 1
                stats[a]["R"] += 1

    # Budowanie html z widokiem tabel podzielonych na kolumny
    html_output = []
    groups_list = sorted(list(GROUPS_DICT.keys()))
    
    # Wyświetlamy po dwie grupy w jednym rzędzie wizualnym Streamlit za pomocą HTML
    for i in range(0, len(groups_list), 2):
        g1, g2 = groups_list[i], groups_list[i+1] if i+1 < len(groups_list) else None
        
        html_output.append("<div style='display: flex; gap: 20px; margin-bottom: 20px; width: 100%; flex-wrap: wrap;'>")
        
        # Tabela 1
        html_output.append(f"<div style='flex: 1; min-width: 300px;'>")
        html_output.append(f"<h4 style='color: #F97316 !important; border-bottom: 2px solid #F97316; padding-bottom: 4px;'>{g1}</h4>")
        html_output.append("<table class='kricon-table'><tr><th>Poz</th><th style='text-align:left;'>Drużyna</th><th>M</th><th>Pkt</th><th>Z</th><th>R</th><th>P</th><th>Bilans</th></tr>")
        
        g1_teams = [t for t, data in stats.items() if data["Grupa"] == g1]
        # Sortowanie: Punkty -> Bilans bramkowy -> Bramki zdobyte
        g1_teams_sorted = sorted(g1_teams, key=lambda x: (stats[x]["Pkt"], stats[x]["BZ"] - stats[x]["BS"], stats[x]["BZ"]), reverse=True)
        
        for idx, team in enumerate(g1_teams_sorted):
            d = stats[team]
            bg_row = "class='gold-medal-row'" if idx < 2 else ""
            html_output.append(f"<tr {bg_row}><td><b>{idx+1}</b></td><td class='team-cell'>{get_cdn_flag_img_html(team)} {team}</td><td>{d['M']}</td><td><b>{d['Pkt']}</b></td><td>{d['Z']}</td><td>{d['R']}</td><td>{d['P']}</td><td>{d['BZ']}:{d['BS']}</td></tr>")
        html_output.append("</table></div>")
        
        # Tabela 2
        if g2:
            html_output.append(f"<div style='flex: 1; min-width: 300px;'>")
            html_output.append(f"<h4 style='color: #F97316 !important; border-bottom: 2px solid #F97316; padding-bottom: 4px;'>{g2}</h4>")
            html_output.append("<table class='kricon-table'><tr><th>Poz</th><th style='text-align:left;'>Drużyna</th><th>M</th><th>Pkt</th><th>Z</th><th>R</th><th>P</th><th>Bilans</th></tr>")
            
            g2_teams = [t for t, data in stats.items() if data["Grupa"] == g2]
            g2_teams_sorted = sorted(g2_teams, key=lambda x: (stats[x]["Pkt"], stats[x]["BZ"] - stats[x]["BS"], stats[x]["BZ"]), reverse=True)
            
            for idx, team in enumerate(g2_teams_sorted):
                d = stats[team]
                bg_row = "class='gold-medal-row'" if idx < 2 else ""
                html_output.append(f"<tr {bg_row}><td><b>{idx+1}</b></td><td class='team-cell'>{get_cdn_flag_img_html(team)} {team}</td><td>{d['M']}</td><td><b>{d['Pkt']}</b></td><td>{d['Z']}</td><td>{d['R']}</td><td>{d['P']}</td><td>{d['BZ']}:{d['BS']}</td></tr>")
            html_output.append("</table></div>")
            
        html_output.append("</div>")
        
    return "".join(html_output)

@st.dialog("👁️ Typy graczy dla tego meczu")
def show_other_bets(m_id, current_user):
    st.markdown(f"<h4 style='text-align: center; color: #F97316 !important;'>Mecz #{m_id}</h4>", unsafe_allow_html=True)
    other_bets = []
    for p in players:
        if p != current_user:
            bet = st.session_state.bets.get(m_id, {}).get(p)
            if bet: other_bets.append({"Gracz": p, "Typ": f"{bet[0]} : {bet[1]}"})
            else: other_bets.append({"Gracz": p, "Typ": "Brak typu"})
    st.dataframe(pd.DataFrame(other_bets), use_container_width=True, hide_index=True)

def render_leaderboard_html(now_time, new_positions_dict_dest=None):
    scores = {p: 0 for p in players}
    missing_bets = {p: 0 for p in players}
    if 'results' in st.session_state and 'bets' in st.session_state:
        for m_id, res in st.session_state.results.items():
            is_past = (res['timestamp'] - now_time).total_seconds() <= 0
            for p in players:
                if is_past and (m_id not in st.session_state.bets or p not in st.session_state.bets[m_id]): missing_bets[p] += 1
            if res.get('status') == "Zakończony":
                for p in players:
                    if m_id in st.session_state.bets and p in st.session_state.bets[m_id]:
                        scores[p] += calculate_points(st.session_state.bets[m_id][p][0], st.session_state.bets[m_id][p][1], res.get('score_h'), res.get('score_a'))
    df = pd.merge(pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"]), pd.DataFrame(list(missing_bets.items()), columns=["Gracz", "Brak typu"]), on="Gracz").sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    
    html_lines = ["<table class='kricon-table'><tr><th class='col-pos'>Miejsce</th><th class='col-trend'>Trend</th><th>Gracz</th><th>Punkty</th><th class='col-missing'>Brak typu</th></tr>"]
    for idx, row in df.iterrows():
        pos, p_name = idx + 1, row['Gracz']
        if new_positions_dict_dest is not None: new_positions_dict_dest[p_name] = pos
        old_pos = st.session_state.last_positions.get(p_name, pos) if 'last_positions' in st.session_state else pos
        trend_html = "<span class='trend-up'>▲</span>" if old_pos > pos else "<span class='trend-down'>▼</span>" if old_pos < pos else "<span class='trend-stable'>•</span>"
        bg_class = "class='gold-medal-row'" if pos == 1 else "class='silver-medal-row'" if pos == 2 else "class='bronze-medal-row'" if pos == 3 else ""
        miss_html = f"<span style='color: #DC2626;'>{row['Brak typu']}</span>" if row['Brak typu'] > 0 else "<span style='color: #64748B;'>0</span>"
        html_lines.append(f"<tr {bg_class}><td class='col-pos'><b>{pos}</b></td><td class='col-trend'>{trend_html}</td><td>{p_name}</td><td><b>{row['Punkty']} pkt</b></td><td class='col-missing'>{miss_html}</td></tr>")
    html_lines.append("</table>")
    return "".join(html_lines)

def render_bracket_match_html_clean(match_id, mt="0px", mb="6px"):
    m = st.session_state.results.get(match_id)
    if not m: return
    status = m.get("status")
    sh, sa = (str(m.get("score_h")), str(m.get("score_a"))) if status in ["Zakończony", "LIVE"] and m.get("score_h") is not None else ("?", "?")
    win_h = status == "Zakończony" and m.get("score_h", 0) > m.get("score_a", 0)
    win_a = status == "Zakończony" and m.get("score_a", 0) > m.get("score_h", 0)
    
    html_lines = [
        f"<div class='bracket-match-card' style='margin-top: {mt}; margin-bottom: {mb};'>",
        f"<div class='bracket-match-title'>Mecz #{match_id}</div>",
        f"<div class='bracket-row {'bracket-team-winner' if win_h else ''}'>",
        f"<div style='display:flex; align-items:center; gap:6px; overflow: hidden;'>{get_cdn_flag_img_html(m['home'])}<span class='bracket-team-name'>{m['home']}</span></div>",
        f"<span class='bracket-score-cell'>{sh}</span></div>",
        f"<div class='bracket-row {'bracket-team-winner' if win_a else ''}'>",
        f"<div style='display:flex; align-items:center; gap:6px; overflow: hidden;'>{get_cdn_flag_img_html(m['away'])}<span class='bracket-team-name'>{m['away']}</span></div>",
        f"<span class='bracket-score-cell'>{sa}</span></div></div>"
    ]
    st.markdown("".join(html_lines), unsafe_allow_html=True)

def generate_schedule():
    schedule = {}
    months_pl = {6: "Czerwca", 7: "Lipca"}
    match_id = 1
    group_slots = [18, 21, 0, 3]
    start_date_group = datetime(2026, 6, 11, 21, 0)
    
    for matchday in range(3):
        for g_name, teams in GROUPS_DICT.items():
            pairs = [(teams[0], teams[1]), (teams[2], teams[3])] if matchday == 0 else [(teams[0], teams[2]), (teams[3], teams[1])] if matchday == 1 else [(teams[0], teams[3]), (teams[1], teams[2])]
            for t_home, t_away in pairs:
                if match_id == 1: dt = start_date_group
                else:
                    slot_idx_adj = match_id % 4
                    days_offset_adj = match_id // 4
                    dt = datetime(2026, 6, 12, group_slots[slot_idx_adj], 0) + timedelta(days=days_offset_adj)
                
                schedule[match_id] = {
                    "timestamp": dt, "date": f"{dt.day} {months_pl.get(dt.month)} {dt.strftime('%H:%M')}", 
                    "stage": g_name, "home": t_home, "away": t_away, "score_h": None, "score_a": None, 
                    "status": "Oczekuje", "venue": VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
                }
                match_id += 1

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
            hour = 21 if stage_name == "Finał" else 22 if stage_name in ["Półfinały", "Mecz o 3. miejsce"] else (18 if i % 2 == 0 else 22)
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            schedule[match_id] = {
                "timestamp": match_dt, "date": f"{d} {months_pl.get(m_num)} {match_dt.strftime('%H:%M')}", 
                "stage": stage_name, "home": "TBD", "away": "TBD", "score_h": None, "score_a": None, 
                "status": "Oczekuje", "venue": "MetLife Stadium, Nowy Jork" if stage_name == "Finał" else VENUES_LIST[(match_id - 1) % len(VENUES_LIST)]
            }
            match_id += 1
            if (i + 1) % matches_per_date == 0: date_idx += 1
    return schedule

# 5. INICJALIZACJA STANU APLIKACJI
if 'results' not in st.session_state or len(st.session_state.results) != 104: st.session_state.results = generate_schedule()
if 'bets' not in st.session_state: st.session_state.bets = {m_id: {} for m_id in range(1, 105)}
if 'last_positions' not in st.session_state: st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
if 'toast_msg' not in st.session_state: st.session_state.toast_msg = ""

if 'gs_initialized' not in st.session_state:
    load_from_google_sheets()
    st.session_state.gs_initialized = True

now = datetime.now()
for m_id, m in st.session_state.results.items():
    if m.get('status') != "Zakończony" and timedelta(minutes=0) <= (now - m['timestamp']) <= timedelta(minutes=120): m['status'] = "LIVE"

if st.session_state.toast_msg:
    st.toast(st.session_state.toast_msg)
    st.session_state.toast_msg = ""

if st.session_state.logged_in_user is None:
    st.markdown("<div class='stAppHeader'><div class='kricon-logo-container'></div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        st.subheader("🔒 Logowanie")
        user = st.selectbox("Użytkownik:", [""] + list(USER_CREDENTIALS.keys()))
        pw = st.text_input("Hasło:", type="password")
        if st.button("Zaloguj się", type="primary") and USER_CREDENTIALS.get(user) == pw:
            st.session_state.logged_in_user = user
            st.rerun()
    with c2:
        st.subheader("📊 Ranking Ogólny")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    st.markdown("<div class='stAppHeader'><div class='kricon-logo-container'></div></div>", unsafe_allow_html=True)
    st.sidebar.write(f"👤 Gracz: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("🔄 Odśwież dane chmury", type="secondary"):
        load_from_google_sheets()
        st.toast("Pomyślnie zaktualizowano typy z Google Sheets! 📈")
        st.rerun()
    if st.sidebar.button("Wyloguj się", type="primary"):
        st.session_state.logged_in_user = None
        st.session_state.pop('gs_initialized', None)
        st.rerun()
        
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ranking", "📅 Terminarz", "🕵️ Typy graczy", "📈 Tabele", "🏆 Drabinka Turniejowa"])
    
    with tab1:
        current_positions_map = {}
        st.markdown(render_leaderboard_html(now, current_positions_map), unsafe_allow_html=True)
        if current_positions_map: st.session_state.last_positions = current_positions_map
        
    with tab2:
        mode = st.radio("Filtruj mecze:", ["Oczekujące", "Wszystkie", "Zakończone"], horizontal=True)
        for m_id, m in sorted(st.session_state.results.items()):
            if (mode == "Oczekujące" and m.get('status') == "Zakończony") or (mode == "Zakończone" and m.get('status') == "Oczekuje"): continue
            status_html = "<span class='status-badge-live'>🔴 LIVE</span>" if m.get('status') == "LIVE" else "<span class='status-badge-ended'>⚫ Zakończony</span>" if m.get('status') == "Zakończony" else "<span class='status-waiting-blink'>🟡 Oczekuje</span>"
            locked = (m['timestamp'] - now).total_seconds() <= 0
            
            has_bet = st.session_state.logged_in_user in st.session_state.bets.get(m_id, {})
            saved_h, saved_a = st.session_state.bets.get(m_id, {}).get(st.session_state.logged_in_user, (0,0))
            
            h_key = f"h_{m_id}"
            a_key = f"a_{m_id}"
            
            # STABILNE PRZYPISANIE WARTOŚCI DO STATE BEZ RYZYKA RESETU
            if h_key not in st.session_state: st.session_state[h_key] = saved_h if has_bet else 0
            if a_key not in st.session_state: st.session_state[a_key] = saved_a if has_bet else 0
            
            st.markdown(f"<div class='meta-upper-bar-container'><span class='meta-id-text-clean'>⚽ Mecz #{m_id}</span> {status_html} <span style='color:#94A3B8;'>📅 {m['date']}</span> <span style='color:#38BDF8; font-weight:bold;'>📍 {m.get('venue').split(',')[0]}</span></div>", unsafe_allow_html=True)
            col_h_team, col_h_score, col_colon, col_a_score, col_a_team, col_action = st.columns([3, 1.5, 0.5, 1.5, 3, 2], gap="small")
            
            with col_h_team:
                st.markdown(f"<div class='team-align-right'>{m['home']} {get_cdn_flag_img_html(m['home'])}</div>", unsafe_allow_html=True)
            with col_h_score:
                if locked: st.markdown(f"<div class='off-score'>{saved_h if has_bet else '-'}</div>", unsafe_allow_html=True)
                else: st.number_input("Gole Home", min_value=0, max_value=20, step=1, key=h_key, label_visibility="collapsed")
            with col_colon:
                st.markdown("<div class='score-colon'>:</div>", unsafe_allow_html=True)
            with col_a_score:
                if locked: st.markdown(f"<div class='off-score'>{saved_a if has_bet else '-'}</div>", unsafe_allow_html=True)
                else: st.number_input("Gole Away", min_value=0, max_value=20, step=1, key=a_key, label_visibility="collapsed")
            with col_a_team:
                st.markdown(f"<div class='team-align-left'>{get_cdn_flag_img_html(m['away'])} {m['away']}</div>", unsafe_allow_html=True)
                
            with col_action:
                st.markdown("<div class='match-row-anchor' style='display:none;'></div>", unsafe_allow_html=True)
                if locked:
                    st.button("👁️ Zobacz typy", key=f"view_{m_id}", type="secondary", on_click=show_other_bets, args=(m_id, st.session_state.logged_in_user))
                else:
                    cb1, cb2 = st.columns(2)
                    with cb1: st.button("💾 Zapisz", key=f"save_btn_{m_id}", type="primary", on_click=handle_save, args=(m_id, st.session_state.logged_in_user, h_key, a_key))
                    with cb2: st.button("🗑️ Usuń", key=f"del_btn_{m_id}", type="secondary", on_click=handle_delete, args=(m_id, st.session_state.logged_in_user, h_key, a_key))

    with tab3:
        st.subheader("🕵️ Przegląd typów wszystkich graczy")
        selected_match = st.selectbox("Wybierz mecz do podglądu:", [f"Mecz #{i} - {st.session_state.results[i]['home']} vs {st.session_state.results[i]['away']}" for i in range(1, 105)])
        m_id_sel = int(selected_match.split("#")[1].split(" ")[0])
        match_info = st.session_state.results[m_id_sel]
        if (match_info['timestamp'] - now).total_seconds() > 0 and st.session_state.logged_in_user != "admin":
            st.warning("🔒 Typy innych graczy zostaną odblokowane automatycznie po rozpoczęciu tego meczu!")
        else:
            show_data = [{"Gracz": p, "Typ": f"{st.session_state.bets.get(m_id_sel, {}).get(p)[0]} : {st.session_state.bets.get(m_id_sel, {}).get(p)[1]}" if st.session_state.bets.get(m_id_sel, {}).get(p) else "Brak typu"} for p in players]
            st.table(pd.DataFrame(show_data))

    with tab4:
        st.subheader("📈 Aktywne Tabele Grupowe")
        # WYWOŁANIE NOWEGO AUTOMATYCZNEGO SILNIKA TABEL
        st.markdown(calculate_group_tables_html(), unsafe_allow_html=True)

    with tab5:
        st.subheader("🏆 Drabinka Turniejowa MŚ 2026")
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1.2, 0.4, 1.2, 1.2, 1.6, 1.2, 1.2, 0.4, 1.2], gap="small")
        with c1:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>1/16 Finału</p>", unsafe_allow_html=True)
            for i in range(73, 81): render_bracket_match_html_clean(i)
        with c3:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>1/8 Finału</p>", unsafe_allow_html=True)
            for i in range(89, 93): render_bracket_match_html_clean(i, mt="35px", mb="65px" if i<92 else "0px")
        with c4:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>Ćwierćfinały</p>", unsafe_allow_html=True)
            render_bracket_match_html_clean(97, mt="110px", mb="210px")
            render_bracket_match_html_clean(98, mt="110px")
        with c5:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>Półfinały & Finał</p>", unsafe_allow_html=True)
            render_bracket_match_html_clean(101, mt="220px")
            m_fin = st.session_state.results.get(104)
            sf = m_fin.get("status")
            sh_f, sa_f = (str(m_fin.get("score_h")), str(m_fin.get("score_a"))) if sf in ["Zakończony", "LIVE"] and m_fin.get("score_h") is not None else ("?", "?")
            st.markdown(f"<div class='center-final-card-wrapper'><div class='center-final-card'><div class='final-title'>🏆 WIELKI FINAŁ 🏆</div><div class='final-teams'><div class='final-team'>{get_cdn_flag_img_html(m_fin['home'])} {m_fin['home']}</div><div class='final-score'>{sh_f} : {sa_f}</div><div class='final-team'>{m_fin['away']} {get_cdn_flag_img_html(m_fin['away'])}</div></div><div class='final-venue'>📍 {m_fin['venue']}</div></div></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
            render_bracket_match_html_clean(103, mt="40px")
            st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.75rem; font-weight:bold;'>Mecz o 3. miejsce</p>", unsafe_allow_html=True)
            render_bracket_match_html_clean(102, mt="50px")
        with c6:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>Ćwierćfinały</p>", unsafe_allow_html=True)
            render_bracket_match_html_clean(99, mt="110px", mb="210px")
            render_bracket_match_html_clean(100, mt="110px")
        with c7:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>1/8 Finału</p>", unsafe_allow_html=True)
            for i in range(93, 97): render_bracket_match_html_clean(i, mt="35px", mb="65px" if i<96 else "0px")
        with c9:
            st.markdown("<p style='text-align:center; font-weight:bold; color:#F97316;'>1/16 Finału</p>", unsafe_allow_html=True)
            for i in range(81, 89): render_bracket_match_html_clean(i)
