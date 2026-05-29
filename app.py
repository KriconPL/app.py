import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfiguracja i Szata Graficzna zgodna z brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# CSS dla jaśniejszej stylizacji brandingowej KriCon, loga i flag
st.markdown("""
    <style>
    /* Tło główne i kontenerów */
    .reportview-container, .main .block-container { 
        background: #FFFFFF; 
        color: #1F2937; 
    }
    .main .block-container { padding-top: 1rem; }
    
    /* Kontener loga i tytułu */
    .logo-title-container {
        display: flex;
        align-items: center;
        border-bottom: 4px solid #3B82F6;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .logo-container {
        margin-right: 20px;
    }
    .logo-image {
        max-height: 80px;
    }
    
    /* Nagłówek H1 */
    .logo-title-container h1 {
        color: #1E3A8A !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin: 0 !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Pozostałe nagłówki */
    h2, h3 { 
        color: #1E3A8A !important;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Przyciski w kolorystyce KriCon */
    .stButton>button {
        background-color: #3B82F6 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
        transform: translateY(-1px);
    }
    
    /* Komunikaty i notyfikacje */
    div[data-testid="stNotification"] {
        background-color: #EFF6FF !important;
        color: #1E3A8A !important;
        border-left: 5px solid #3B82F6 !important;
        border-radius: 4px;
    }
    
    /* Oficjalny wynik */
    .real-score { 
        font-size: 1.3rem; 
        color: #EF4444; 
        font-weight: bold; 
        background-color: #FEF2F2;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* Zakładki (Tabs) */
    .stTabs [data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #3B82F6 !important;
        color: #1E3A8A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Stabilny URL loga Kricon Group (PNG)
KRICON_LOGO_URL_PNG = "https://kricongroup.com/wp-content/uploads/2021/04/kricon-logotype.png"

# Wyświetlanie Loga i Tytułu
st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            <img src="{KRICON_LOGO_URL_PNG}" alt="Kricon Group Logo" class="logo-image">
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# 2. Baza użytkowników - rozbita dla uniku błędów składniowych
USER_CREDENTIALS = {
    "Adam": "adam2026",
    "Maciej": "maciej2026",
    "Marcin": "marcin2026",
    "Kamil": "kamil2026",
    "Kuba M": "kubam2026",
    "Tomek": "tomek2026",
    "Kuba K": "kubak2026",
    "Rafał": "rafal2026",
    "admin": "kriconadmin"
}
players = [k for k in USER_CREDENTIALS.keys() if k != "admin"]

# Oficjalny podział na grupy Mistrzostw Świata 2026 z flagami
GROUPS_DICT = {
    "Grupa A": ["🇲🇽 Meksyk", "🇿🇦 RPA", "🇰🇷 Korea Południowa", "🇨🇿 Czechy"],
    "Grupa B": ["🇨🇦 Kanada", "🇧🇦 Bośnia i Hercegowina", "🇶🇦 Katar", "🇨🇭 Szwajcaria"],
    "Grupa C": ["🇧🇷 Brazylia", "🇲🇦 Maroko", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Szkocja"],
    "Grupa D": ["🇺🇸 USA", "🇵🇾 Paragwaj", "🇦🇺 Australia", "🇹🇷 Turcja"],
    "Grupa E": ["🇩🇪 Niemcy", "🇨🇼 Curaçao", "🇨🇮 WKS", "🇪🇨 Ekwador"],
    "Grupa F": ["🇳🇱 Holandia", "🇯🇵 Japonia", "🇸🇪 Szwecja", "🇹🇳 Tunezja"],
    "Grupa G": ["🇧🇪 Belgia", "🇪🇬 Egipt", "🇮🇷 Iran", "🇳🇿 Nowa Zelandia"],
    "Grupa H": ["🇪🇸 Hiszpania", "🇨🇻 Wyspy Zielonego Przylądka", "🇸🇦 Arabia Saudyjska", "🇺🇾 Urugwaj"],
    "Grupa I": ["🇫🇷 Francja", "🇸🇳 Senegal", "🇮🇶 Irak", "🇳🇴 Norwegia"],
    "Grupa J": ["🇦🇷 Argentyna", "🇩🇿 Algieria", "🇦🇹 Austria", "🇯🇴 Jordania"],
    "Grupa K": ["🇵🇹 Portugalia", "🇨🇩 DR Konga", "🇺🇿 Uzbekistan", "🇨🇴 Kolumbia"],
    "Grupa L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Anglia", "🇭🇷 Chorwacja", "🇬🇭 Ghana", "🇵🇦 Panama"]
}

# 3. Generator Harmonogramu 104 Meczów z Oficjalnymi Ramami Datowymi
def generate_schedule():
    schedule = {}
    match_id = 1
    
    # Faza grupowa: 11 - 27 Czerwca
    dates_group = [f"{d} Czerwca" for d in range(11, 28)]
    
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    date_idx = 0
    
    # Faza Grupowa (72 mecze przy 12 grupach)
    for m_round in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1_idx, t2_idx = matchups[m_round]
            schedule[match_id] = {
                "date": dates_group[date_idx % len(dates_group)],
                "stage": group_name,
                "home": teams[t1_idx], 
                "away": teams[t2_idx],
                "score_h": None, 
                "score_a": None, 
                "status": "Oczekuje"
            }
            match_id += 1
            if match_id % 4 == 0: date_idx += 1

    # Oficjalne ramy czasowe fazy pucharowej MŚ 2026
    ko_stages = [
        ("1/16 Finału", 16, ["28 Czerwca", "29 Czerwca", "30 Czerwca", "1 Lipca", "2 Lipca", "3 Lipca"]), 
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
                "home": "TBD 🏳️", 
                "away": "TBD 🏳️",
                "score_h": None, 
                "score_a": None, 
                "status": "Oczekuje"
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
                return ['background-color: #DBEAFE; color: #1E3A8A; font-weight: bold;'] * len(row)
            elif row.name == len(df_scores) and row['Punkty'] > 0:
                return ['background-color: #FEE2E2; color: #991B1B;'] * len(row)
            return [''] * len(row)

        st.dataframe(df_scores.style.apply(highlight_rows, axis=1), use_container_width=True)

    # ZAKŁADKA 2: TERMINARZ I TYPY
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
                    
                    # SYSTEM ANTY-ŚCIĄGANIA
                    if match['status'] == "Zakończony":
                        with st.expander("👁️ Zobacz typy innych graczy"):
                            other_bets = []
                            for p in players:
                                if p != current_user:
                                    p_bet = st.session_state.bets
