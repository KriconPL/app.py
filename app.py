import streamlit as st
import pandas as pd
import numpy as np

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
    .real-score { font-size: 1.2rem; color: #E74C3C; font-weight: bold; }
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

GROUPS_DICT = {
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

# 3. Generator Harmonogramu 104 Meczów z Datami
def generate_schedule():
    schedule = {}
    match_id = 1
    
    # Przykładowe rozbicie dat (Czerwiec - Lipiec)
    dates_group = [f"{d} Czerwca" for d in range(11, 28)]
    
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    date_idx = 0
    
    # Faza Grupowa
    for m_round in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1_idx, t2_idx = matchups[m_round]
            schedule[match_id] = {
                "date": dates_group[date_idx % len(dates_group)],
                "stage": group_name,
                "home": teams[t1_idx], "away": teams[t2_idx],
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            if match_id % 4 == 0: date_idx += 1

    # Faza Pucharowa z datami
    ko_stages = [
        ("1/16 Finału", 16, ["28 Czerwca", "29 Czerwca", "30 Czerwca", "1 Lipca"]), 
        ("1/8 Finału", 8, ["4 Lipca", "5 Lipca", "6 Lipca", "7 Lipca"]), 
        ("Ćwierćfinały", 4, ["9 Lipca", "10 Lipca", "11 Lipca"]), 
        ("Półfinały", 2, ["14 Lipca", "15 Lipca"]), 
        ("Mecz o 3. miejsce", 1, ["18 Lipca"]), 
        ("Finał", 1, ["19 Lipca"])
    ]
    
    for stage_name, count, stage_dates in ko_stages:
        d_idx = 0
        for _ in range(count):
            schedule[match_id] = {
                "date": stage_dates[d_idx % len(stage_dates)],
                "stage": stage_name,
                "home": "TBD (Kwalifikant)", "away": "TBD (Kwalifikant)",
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            d_idx += 1
            
    return schedule

# Inicjalizacja bezpieczna
if 'results' not in st.session_state or "date" not in st.session_state.results.get(1, {}):
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state or len(st.session_state.bets) < 100:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

all_dates = []
for m in st.session_state.results.values():
    if m["date"] not in all_dates:
        all_dates.append(m["date"])

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

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Klasyfikacja", "📅 Terminarz i Typy", "📈 Tabele Grup", "⚙️ Admin"])

    # ZAKŁADKA 1: KLASYFIKACJA
    with tab1:
        st.header("Tabela Wyników Typera")
        scores = {player: 0 for player in players}
        for match_id, result in st.session_state.results.items():
            r_h, r_a = result['score_h'], result['score_a']
            if result['status'] == "Zakończony":
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

    # ZAKŁADKA 2: TERMINARZ I TYPY (Po datach + podgląd innych)
    with tab2:
        if current_user == "admin":
            st.warning("Zaloguj się jako gracz, aby typować.")
        else:
            st.header("Obstawiaj mecze wg dat")
            selected_date = st.selectbox("Wybierz dzień turnieju:", all_dates)
            st.divider()
            
            for match_id, match in st.session_state.results.items():
                if match["date"] == selected_date:
                    st.write(f"### {match['home']} vs {match['away']}")
                    st.caption(f"Faza: {match['stage']} | Mecz #{match_id}")
                    
                    if match['status'] == "Zakończony":
                        st.markdown(f"<p class='real-score'>Oficjalny wynik: {match['score_h']} - {match['score_a']}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='color: gray;'>Mecz oczekuje na rozegranie.</p>", unsafe_allow_html=True)

                    curr_h, curr_a = st.session_state.bets[match_id].get(current_user, (None, None))
                    
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        bet_h = st.number_input(f"Twój typ: {match['home']}", min_value=0, step=1, key=f"h_{match_id}", value=curr_h if curr_h is not None else 0)
                    with c2:
                        bet_a = st.number_input(f"Twój typ: {match['away']}", min_value=0, step=1, key=f"a_{match_id}", value=curr_a if curr_a is not None else 0)
                    with c3:
                        st.write("")
                        st.write("")
                        if match['status'] == "Zakończony":
                            st.button("Zablokowane", disabled=True, key=f"dis_{match_id}")
                        else:
                            if st.button("Zapisz typ", key=f"btn_{match_id}"):
                                st.session_state.bets[match_id][current_user] = (bet_h, bet_a)
                                st.success("Zapisano!")
                    
                    with st.expander("👁️ Zobacz typy innych graczy"):
                        other_bets = []
                        for p in players:
                            if p != current_user:
                                p_bet = st.session_state.bets[match_id].get(p)
                                if p_bet is not None:
                                    other_bets.append({"Gracz": p, "Typ": f"{p_bet[0]} - {p_bet[1]}"})
                                else:
                                    other_bets.append({"Gracz": p, "Typ": "Brak typu"})
                        if other_bets:
                            st.dataframe(pd.DataFrame(other_bets), use_container_width=True)
                        else:
                            st.write("Nikt jeszcze nie obstawił.")
                            
                    st.divider()

    # ZAKŁADKA 3: TABELE GRUP (Automatyczne przeliczanie)
    with tab3:
        st.header("📈 Tabele Fazy Grupowej")
        st.write("Aktualizowane na żywo po wpisaniu oficjalnych wyników.")
        
        group_sel = st.selectbox("Wybierz grupę:", list(GROUPS_DICT.keys()))
        
        # Obliczanie tabeli
        teams_stats = {t: {"Punkty": 0, "BZ": 0, "BS": 0, "RB": 0} for t in GROUPS_DICT[group_sel]}
        
        for match in st.session_state.results.values():
            if match["stage"] == group_sel and match["status"] == "Zakończony":
                h_team, a_team = match["home"], match["away"]
                sh, sa = match["score_h"], match["score_a"]
                
                # Aktualizacja bramek
                teams_stats[h_team]["BZ"] += sh
                teams_stats[h_team]["BS"] += sa
                teams_stats[h_team]["RB"] += (sh - sa)
                
                teams_stats[a_team]["BZ"] += sa
                teams_stats[a_team]["BS"] += sh
                teams_stats[a_team]["RB"] += (sa - sh)
                
                # Aktualizacja punktów
                if sh > sa:
                    teams_stats[h_team]["Punkty"] += 3
                elif sa > sh:
                    teams_stats[a_team]["Punkty"] += 3
                else:
                    teams_stats[h_team]["Punkty"] += 1
                    teams_stats[a_team]["Punkty"] += 1
                    
        df_group = pd.DataFrame.from_dict(teams_stats, orient='index').reset_index()
        df_group.rename(columns={'index': 'Reprezentacja'}, inplace=True)
        # Sortowanie wg zasad (Punkty -> Różnica Bramek -> Bramki Zdobyte)
        df_group = df_group.sort_values(by=["Punkty", "RB", "BZ"], ascending=[False, False, False]).reset_index(drop=True)
        df_group.index += 1
        
        st.dataframe(df_group, use_container_width=True)

    # ZAKŁADKA 4: ADMIN
    with tab4:
        if current_user != "admin":
            st.error("Zaloguj się jako 'admin', aby wpisywać wyniki.")
        else:
            st.header("⚙️ Wprowadzanie Wyników")
            admin_date = st.selectbox("Wybierz dzień:", all_dates, key="admin_date")
            st.divider()
            
            for match_id, match in st.session_state.results.items():
                if match["date"] == admin_date:
                    
                    if "TBD" in match["home"] or "Finał" in match["stage"] or "1/" in match["stage"]:
                        new_home = st.text_input(f"Drużyna 1 (Mecz #{match_id})", value=match["home"], key=f"edit_h_{match_id}")
                        new_away = st.text_input(f"Drużyna 2 (Mecz #{match_id})", value=match["away"], key=f"edit_a_{match_id}")
                        st.session_state.results[match_id]["home"] = new_home
                        st.session_state.results[match_id]["away"] = new_away

                    st.write(f"**{match['home']} vs {match['away']}** ({match['stage']})")
                    
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        res_h = st.number_input(f"Wynik {match['home']}", min_value=0, step=1, key=f"res_h_{match_id}", value=match['score_h'] if match['score_h'] is not None else 0)
                    with c2:
                        res_a = st.number_input(f"Wynik {match['away']}", min_value=0, step=1, key=f"res_a_{match_id}", value=match['score_a'] if match['score_a'] is not None else 0)
                    with c3:
                        st.write("")
                        st.write("")
                        if st.button("Zatwierdź Wynik", key=f"res_btn_{match_id}"):
                            st.session_state.results[match_id]['score_h'] = res_h
                            st.session_state.results[match_id]['score_a'] = res_a
                            st.session_state.results[match_id]['status'] = "Zakończony"
                            st.success("Tabela i punkty przeliczone!")
                    st.markdown("---")
