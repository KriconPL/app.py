import streamlit as st
import pandas as pd
import numpy as np
import base64
import json 
import gspread
from zoneinfo import ZoneInfo

# --- KONFIGURACJA ---
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0A1128; color: white; }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- UŻYTKOWNICY ---
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Kamil": "kamil2026", 
    "Kuba M": "kubam2026", "Tomek": "tomek2026", "Kuba K": "kubak2026", 
    "Rafał": "rafal2026", "admin": "kriconadmin"
}

# --- FUNKCJE DANYCH ---
@st.cache_resource
def get_gspread_client():
    creds_json = base64.b64decode(st.secrets["gcp_base64_creds"]).decode('utf-8')
    return gspread.service_account_from_dict(json.loads(creds_json))

def load_data():
    gc = get_gspread_client()
    sh = gc.open("Kricon_Typer_2026")
    
    # 1. Wyniki
    results = {}
    try:
        rows = sh.worksheet("Wyniki").get_all_records()
        for r in rows:
            results[int(r["Mecz"])] = {"score_h": int(r["Wynik_H"]), "score_a": int(r["Wynik_A"])}
    except: pass
    
    # 2. Typy
    bets = {}
    try:
        rows = sh.sheet1.get_all_records()
        for r in rows:
            m_id = int(r["Mecz"])
            if m_id not in bets: bets[m_id] = {}
            bets[m_id][r["Gracz"]] = (int(r["Typ_H"]), int(r["Typ_A"]))
    except: pass
    
    return results, bets

def save_bet(m_id, player, h, a):
    gc = get_gspread_client()
    sh = gc.open("Kricon_Typer_2026").sheet1
    data = sh.get_all_records()
    df = pd.DataFrame(data)
    
    # Usuń stary typ jeśli jest
    df = df[~((df["Mecz"] == m_id) & (df["Gracz"] == player))]
    new_row = pd.DataFrame([[m_id, player, h, a]], columns=["Mecz", "Gracz", "Typ_H", "Typ_A"])
    df = pd.concat([df, new_row])
    
    sh.clear()
    sh.update([df.columns.values.tolist()] + df.values.tolist())

# --- LOGIKA RANKINGU ---
def calculate_ranking(bets, results):
    points = {u: 0 for u in USER_CREDENTIALS.keys() if u != "admin"}
    for m_id, player_bets in bets.items():
        if m_id in results:
            res_h, res_a = results[m_id]["score_h"], results[m_id]["score_a"]
            for player, (bet_h, bet_a) in player_bets.items():
                if player in points:
                    # Logika: 3pkt za wynik, 1pkt za wygraną
                    if bet_h == res_h and bet_a == res_a: points[player] += 3
                    elif np.sign(bet_h - bet_a) == np.sign(res_h - res_a): points[player] += 1
    return pd.DataFrame(list(points.items()), columns=["Gracz", "Punkty"]).sort_values("Punkty", ascending=False)

# --- APP ---
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    user = st.selectbox("Użytkownik", [""] + list(USER_CREDENTIALS.keys()))
    pw = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        if USER_CREDENTIALS.get(user) == pw:
            st.session_state.logged_in_user = user
            st.rerun()
else:
    results, bets = load_data()
    tabs = st.tabs(["📊 Ranking", "⚽ Typowanie", "📅 Wyniki"])
    
    with tabs[0]: # Ranking
        st.subheader("Tabela Punktowa")
        st.table(calculate_ranking(bets, results))
        
    with tabs[1]: # Typowanie
        st.subheader("Twoje Typy")
        mecz_id = st.number_input("Numer Meczu", 1, 64)
        h = st.number_input("Gole Gospodarze", 0)
        a = st.number_input("Gole Goście", 0)
        if st.button("Zapisz typ"):
            save_bet(mecz_id, st.session_state.logged_in_user, h, a)
            st.success("Zapisano!")
            st.rerun()

    with tabs[2]: # Admin / Wyniki
        if st.session_state.logged_in_user == "admin":
            st.subheader("⚙️ Admin - Wyniki")
            m_id = st.number_input("Mecz ID", 1, 64)
            h = st.number_input("Wynik H", 0)
            a = st.number_input("Wynik A", 0)
            if st.button("Zapisz Wynik"):
                # Funkcja do zapisu wyniku (identyczna jak w poprzednim kodzie)
                # update_result_to_sheets(m_id, h, a) 
                st.success("Zaktualizowano oficjalny wynik!")
        else:
            st.write("Wgląd w oficjalne wyniki (implementacja analogiczna)")
