import streamlit as st
import pandas as pd
import numpy as np
import requests

# 1. Konfiguracja i Szata Graficzna Kricon BV
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #F4F6F9; }
    .main .block-container { padding-top: 2rem; }
    h1 {
        color: #0F2042 !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        border-bottom: 3px solid #3498DB;
        padding-bottom: 10px;
    }
    h2, h3 { color: #1B365D !important; }
    .stButton>button {
        background-color: #0F2042 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3498DB !important;
        transform: scale(1.02);
    }
    div[data-testid="stNotification"] {
        background-color: #EBF5FB !important;
        color: #2C3E50 !important;
        border-left: 5px solid #3498DB !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Kricon BV | World Cup 2026 Typer")

# 2. Baza użytkowników
USER_CREDENTIALS = {
    "Adam": "adam2026", "Maciej": "maciej2026", "Marcin": "marcin2026",
    "Kamil": "kamil2026", "Kuba M": "kubam2026", "Tomek": "tomek2026",
    "Kuba K": "kubak2026", "Rafał": "rafal2026", "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

# 3. Generator Harmonogramu 104 Meczów (MŚ 2026)
def generate_schedule():
    schedule = {}
    match_id = 1
    
    # Podział 48 drużyn na 12 Grup (A-L)
    groups = {
        "Grupa A": ["🇲🇽 Meksyk", "🇨🇭 Szwajcaria", "🇳🇬 Nigeria", "🇳🇿 Nowa Zelandia"],
        "Grupa B": ["🇨🇦 Kanada", "🇩🇰 Dania", "🇨🇲 Kamerun", "🇶🇦 Katar"],
        "Grupa C": ["🇺🇸 USA", "🇵🇱 Polska", "🇿🇦 RPA", "🇺🇿 Uzbekistan"],
        "Grupa D": ["🇦🇷 Argentyna", "🇷🇸 Serbia", "🇩🇿 Algieria", "🇵🇦 Panama"],
        "Grupa E": ["🇫🇷 Francja", "🇨🇴 Kolumbia", "🇮🇶 Irak", "🇯🇲 Jamajka"],
        "Grupa F": ["🇧🇷 Brazylia", "🇦🇹 Austria", "🇬🇭 Ghana", "🇸🇦 Arabia Saudyjska"],
        "Grupa G": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Anglia", "🇪🇨 Ekwador", "🇲🇦 Maroko", "🇨🇷 Kostaryka"],
        "Grupa H": ["🇪🇸 Hiszpania", "🇨🇱 Chile", "🇸🇳 Senegal", "🇦🇺 Australia"],
        "Grupa I": ["🇩🇪 Niemcy", "🇺🇾 Urugwaj", "🇨🇮 WKS", "🇮🇷 Iran"],
        "Grupa J": ["🇵🇹 Portugalia", "🇵🇪 Peru", "🇪🇬 Egipt", "🇯🇵 Japonia"],
        "Grupa K": ["🇮🇹 Włochy", "🇻🇪 Wenezuela", "🇰🇷 Korea Płd.", "🇸🇪 Szwecja"],
        "Grupa L": ["🇳🇱 Holandia", "🇭🇷 Chorwacja", "🇧🇪 Belgia", "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Walia"]
    }
    
    # Faza Grupowa (72 mecze - po 6 w każdej grupie w formacie każdy z każdym)
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    for group_name, teams in groups.items():
        for t1_idx, t2_idx in matchups:
            schedule[match_id] = {
                "stage": group_name,
                "home": teams[t1_idx], "away": teams[t2_idx],
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1

    # Faza Pucharowa (32 mecze)
    ko_stages = [
        ("1/16 Finału", 16), ("1/8 Finału", 8), 
        ("Ćwierćfinały", 4), ("Półfinały", 2), 
        ("Mecz o 3. miejsce", 1), ("Finał", 1)
    ]
    for stage_name, count in ko_stages:
        for _ in range(count):
            schedule[match_id] = {
                "stage": stage_name,
                "home": "TBD (Kwalifikant)", "away": "TBD (Kwalifikant)",
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            
    return schedule

# Inicjalizacja baz danych w pamięci chmury
if 'results' not in st.session_state:
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

# Wyciągnięcie unikalnych etapów (Filtry)
all_stages = []
for m in st.session_state.results.values():
    if m["stage"] not in all_stages:
        all_stages.append(m["stage"])

# Funkcja obliczania punktów
def calculate_points(pred_h, pred_a, real_h, real_a):
    if real_h is None or real_a is None or pred_h is None or pred_a is None:
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

# 4. System Logowania
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    st.subheader("🔒 Logowanie do systemu Kricon Typer")
    username = st.selectbox("Wybierz użytkownika:", [""] + list(USER_CREDENTIALS.keys()))
    password = st.text_input("Wpisz hasło:", type="password")
    
    if st.button("Zaloguj się"):
        if USER_CREDENTIALS.get(username) == password:
            st.session_state.logged_in_user = username
            st.rerun()
        else:
            st.error("Błędne hasło. Spróbuj ponownie.")
else:
    current_user = st.session_state.logged_in_user
    st.sidebar.write(f"👤 Zalogowany jako: **{current_user}**")
    if st.sidebar.button("Wyloguj się"):
        st.session_state.logged_in_user = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📊 Klasyfikacja Generalna", "🎯 Moje Typy", "⚙️ Panel Admina (Wyniki)"])

    # ZAKŁADKA 1: KLASYFIKACJA
    with tab1:
        st.header("Tabela Wyników")
        scores = {player: 0 for player in players}
        for match_id, result in st.session_state.results.items():
            r_h, r_a = result['score_h'], result['score_a']
            for player in players:
                if player in st.session_state.bets[match_id]:
                    p_h, p_a = st.session_state.bets[match_id][player]
                    scores[player] += calculate_points(p_h, p_a, r_h, r_a)
                    
        df_scores = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"])
        df_scores = df_scores.sort_values(by="Punkty", ascending=False).reset_index(drop=True)
        df_scores.index += 1
        
        def highlight_rows(row):
            if row.name == 1 and row['Punkty'] > 0:
                return ['background-color: #A9DFBF; font-weight: bold;'] * len(row) 
            elif row.name == len(df_scores) and row['Punkty'] > 0:
                return ['background-color: #F5B7B1;'] * len(row)
            return [''] * len(row)

        st.dataframe(df_scores.style.apply(highlight_rows, axis=1), use_container_width=True)

    # ZAKŁADKA 2: MOJE TYPY 
    with tab2:
        if current_user == "admin":
            st.warning("Jesteś zalogowany jako admin. Aby typować, zaloguj się na swoje imienne konto.")
        else:
            st.header(f"Twoje Typy - {current_user}")
            # Zastosowanie filtra dla wygody użytkowania
            selected_stage = st.selectbox("Wybierz fazę turnieju do typowania:", all_stages)
            st.divider()
            
            for match_id, match in st.session_state.results.items():
                if match["stage"] == selected_stage:
                    st.write(f"**Mecz #{match_id}: {match['home']} vs {match['away']}** (Status: {match['status']})")
                    
                    curr_h, curr_a = st.session_state.bets[match_id].get(current_user, (None, None))
                    
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        bet_h = st.number_input(f"Bramki {match['home']}", min_value=0, step=1, key=f"h_{match_id}", value=curr_h if curr_h is not None else 0)
                    with c2:
                        bet_a = st.number_input(f"Bramki {match['away']}", min_value=0, step=1, key=f"a_{match_id}", value=curr_a if curr_a is not None else 0)
                    with c3:
                        st.write("")
                        st.write("")
                        if match['status'] == "Zakończony":
                            st.button("Zablokowane", disabled=True, key=f"dis_{match_id}")
                        else:
                            if st.button("Zapisz", key=f"btn_{match_id}"):
                                st.session_state.bets[match_id][current_user] = (bet_h, bet_a)
                                st.success("Zapisano typ!")
                    st.markdown("---")

    # ZAKŁADKA 3: AKTUALIZACJA WYNIKÓW (Panel Administratora)
    with tab3:
        if current_user != "admin":
            st.error("Brak dostępu. Zaloguj się jako 'admin', aby wpisywać oficjalne wyniki meczów.")
        else:
            st.header("⚙️ Zarządzanie Oficjalnymi Wynikami")
            admin_stage = st.selectbox("Wybierz fazę turnieju do edycji:", all_stages, key="admin_stage")
            st.divider()
            
            for match_id, match in st.session_state.results.items():
                if match["stage"] == admin_stage:
                    
                    # Opcja dla fazy pucharowej - edycja nazw drużyn, które awansowały
                    if "TBD" in match["home"] or "Finał" in match["stage"] or "1/" in match["stage"]:
                        new_home = st.text_input(f"Drużyna 1 (Mecz #{match_id})", value=match["home"], key=f"edit_h_{match_id}")
                        new_away = st.text_input(f"Drużyna 2 (Mecz #{match_id})", value=match["away"], key=f"edit_a_{match_id}")
                        st.session_state.results[match_id]["home"] = new_home
                        st.session_state.results[match_id]["away"] = new_away

                    st.write(f"**Mecz #{match_id}: {match['home']} vs {match['away']}**")
                    
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        res_h = st.number_input(f"Wynik {match['home']}", min_value=0, step=1, key=f"res_h_{match_id}", value=match['score_h'] if match['score_h'] is not None else 0)
                    with c2:
                        res_a = st.number_input(f"Wynik {match['away']}", min_value=0, step=1, key=f"res_a_{match_id}", value=match['score_a'] if match['score_a'] is not None else 0)
                    with c3:
                        st.write("")
                        st.write("")
                        if st.button("Zatwierdź Wynik i Zamknij Mecz", key=f"res_btn_{match_id}"):
                            st.session_state.results[match_id]['score_h'] = res_h
                            st.session_state.results[match_id]['score_a'] = res_a
                            st.session_state.results[match_id]['status'] = "Zakończony"
                            st.success("Tabela przeliczona!")
                    st.markdown("---")
