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
    /* Wymuszenie ciemnego tła dla całej aplikacji Streamlit */
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0A1128 !important; 
    }
    [data-testid="stSidebar"] {
        background-color: #060B19 !important; 
    }
    [data-testid="stHeader"] {
        background-color: #0A1128 !important;
    }
    
    /* Kolor tekstów globalnych i formularzy */
    h1, h2, h3, h4, h5, h6, p, span, label, div, [data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
    }

    /* Poprawka widoczności pól formularza logowania i ich etykiet na kolor pomarańczowy */
    div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p {
        color: #F97316 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    div[data-baseweb="select"] *, div[data-baseweb="input"] * {
        color: #F97316 !important; 
        font-weight: bold !important;
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
    
    /* Przyciski w kolorystyce KriCon Orange */
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
    
    /* Inputy numerów (Typy w terminarzu) */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #172554 !important;
        border: 1px solid #1E3A8A !important;
    }

    /* Powiadomienia (Toasty / Pop-upy) */
    [data-testid="stToast"], div[data-testid="stNotification"] {
        background-color: #1E3A8A !important;
        color: white !important;
        border-left: 5px solid #F97316 !important;
    }
    
    /* Karty meczów */
    .match-container {
        background: #172554 !important; 
        border: 1px solid #1E3A8A !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .match-header {
        color: #F97316 !important;
        margin-bottom: 10px;
        font-size: 1.4rem;
        font-weight: 700;
        border-bottom: 1px solid #1E3A8A;
        padding-bottom: 10px;
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
    
    /* Zakładki (Tabs) */
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #F97316 !important;
        color: #F97316 !important;
    }

    /* Tabele HTML */
    .kricon-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 35px 0;
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
        padding: 10px 12px;
        border-bottom: 1px solid #1E3A8A !important;
        color: #F8FAFC !important;
        vertical-align: middle;
    }
    .kricon-table tr:hover {
        background-color: #1E3A8A !important;
    }
    
    /* Style strzałek ligowych */
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
    
    /* Kolorystyka czasu do meczu */
    .time-ok { color: #4ADE80 !important; font-weight: bold; }
    .time-warning { color: #F97316 !important; font-weight: bold; animation: blink 1.5s infinite; }
    .time-normal { color: #CBD5E1 !important; }
    </style>
""", unsafe_allow_html=True)

# Funkcja odczytująca zdjęcie jako Base64
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

# Flagi PNG
COUNTRY_FLAGS = {
    "Meksyk": "mx", "RPA": "za", "Korea Południowa": "kr", "Czechy": "cz",
    "Kanada": "ca", "Bośnia i Hercegowina": "ba", "Katar": "qa", "Szwajcaria": "ch",
    "Brazylia": "br", "Maroko": "ma", "Haiti": "ht", "Szkocja": "gb-sct",
    "USA": "us", "Paragwaj": "py", "Australia": "au", "Turcja": "tr",
    "Niemcy": "de", "Curaçao": "cw", "WKS": "ci", "Ekwador": "ec",
    "Holandia": "nl", "Japonia": "jp", "Szwecja": "se", "Tunezja": "tn",
    "Belgia": "be", "Egipt": "eg", "Iran": "ir", "Nowa Zelandia": "nz",
    "Hiszpania": "es", "Wyspy Zielonego Przylążka": "cv", "Arabia Saudyjska": "sa", "Urugwaj": "uy",
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
    return f'<img src="{flag_url}" width="22" style="vertical-align: middle; margin-right: 8px; border: 1px solid #1E3A8A; border-radius:2px;" alt="flaga"> {country_name}'

# Baza użytkowników
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
    "Grupa H": ["Hiszpania", "Wyspy Zielonego Przylążka", "Arabia Saudyjska", "Urugwaj"],
    "Grupa I": ["Francja", "Senegal", "Irak", "Norwegia"],
    "Grupa J": ["Argentyna", "Algieria", "Austria", "Jordania"],
    "Grupa K": ["Portugalia", "DR Konga", "Uzbekistan", "Kolumbia"],
    "Grupa L": ["Anglia", "Chorwacja", "Ghana", "Panama"]
}

# Generator Harmonogramu 104 Meczów
def generate_schedule():
    schedule = {}
    match_id = 1
    months_pl = {6: "Czerwca", 7: "Lipca"}
    
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    group_matches = []
    
    for round_idx in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1, t2 = matchups[round_idx]
            group_matches.append({"stage": group_name, "home": teams[t1], "away": teams[t2]})
            
    start_date = datetime(2026, 6, 11)
    times = [15, 18, 21, 23] 
    
    for i, match in enumerate(group_matches):
        day_offset = i // 4
        time_idx = i % 4
        match_dt = start_date + timedelta(days=day_offset)
        match_dt = match_dt.replace(hour=times[time_idx], minute=0, second=0)
        
        schedule[match_id] = {
            "timestamp": match_dt,
            "date": f"{match_dt.day} {months_pl[match_dt.month]}",
            "time": match_dt.strftime("%H:%00"),
            "stage": match["stage"],
            "home": match["home"], "away": match["away"],
            "score_h": None, "score_a": None, "status": "Oczekuje"
        }
        match_id += 1

    ko_stages = [
        ("1/16 Finału", 16, [(29,6), (30,6), (1,7), (2,7)]), 
        ("1/8 Finału", 8, [(4,7), (5,7), (6,7), (7,7)]),     
        ("Ćwierćfinały", 4, [(9,7), (10,7)]),                
        ("Półfinały", 2, [(14,7), (15,7)]),                  
        ("Mecz o 3. miejsce", 1, [(18,7)]),                  
        ("Finał", 1, [(19,7)])                               
    ]
    
    for stage_name, count, stage_dates in ko_stages:
        date_idx = 0
        matches_per_date = count // len(stage_dates) if len(stage_dates) > 0 else 1
        matches_per_date = max(1, matches_per_date)
        for i in range(count):
            d, m_num = stage_dates[date_idx % len(stage_dates)]
            hour = 18 if i % 2 == 0 else 21
            match_dt = datetime(2026, m_num, d, hour, 0, 0)
            
            schedule[match_id] = {
                "timestamp": match_dt,
                "date": f"{d} {months_pl[m_num]}",
                "time": match_dt.strftime("%H:%00"),
                "stage": stage_name,
                "home": "TBD", "away": "TBD",
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            if (i + 1) % matches_per_date == 0:
                date_idx += 1
            
    return schedule

if 'results' not in st.session_state or len(st.session_state.results) != 104:
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state or len(st.session_state.bets) != 104:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

if 'last_positions' not in st.session_state:
    st.session_state.last_positions = {player: idx + 1 for idx, player in enumerate(players)}

def calculate_points(pred_h, pred_a, real_h, real_a):
    if real_h is None or real_a is None or pred_h is None or pred_a is None:
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

# Funkcja obliczająca czas do najbliższego nieobstawionego meczu gracza
def get_time_to_next_unbet_match(player_name, now_time):
    # Filtrujemy tylko mecze, które jeszcze się nie zaczęły
    upcoming_matches = sorted(
        [m for m in st.session_state.results.values() if m["status"] == "Oczekuje" and m["timestamp"] > now_time],
        key=lambda x: x["timestamp"]
    )
    
    for match in upcoming_matches:
        match_id = [k for k, v in st.session_state.results.items() if v == match][0]
        player_bet = st.session_state.bets[match_id].get(player_name, (None, None))
        
        # Jeśli gracz nie ma typu dla tego nadchodzącego meczu
        if player_bet == (None, None):
            diff = match["timestamp"] - now_time
            hours = int(diff.total_seconds() // 3600)
            minutes = int((diff.total_seconds() % 3600) // 60)
            
            # Stan alarmowy: Mniej niż godzina do meczu
            if diff <= timedelta(hours=1):
                return f'<span class="time-warning">⏳ Za {hours}h {minutes}m!</span>'
            else:
                return f'<span class="time-normal">Za {hours}h {minutes}m</span>'
                
    return '<span class="time-ok">✔ Wszystko obstawione</span>'

# Funkcja pomocnicza do generowania kodu tabeli klasyfikacji z czasem do meczu
def render_leaderboard_html(now_time, new_positions_dict_dest=None):
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
    
    html_rows = ""
    for idx, row in df_scores.iterrows():
        pos = idx + 1
        player_name = row['Gracz']
        if new_positions_dict_dest is not None:
            new_positions_dict_dest[player_name] = pos
        
        old_pos = st.session_state.last_positions.get(player_name, pos)
        
        if old_pos > pos:
            trend_html = '<div class="badge-trend trend-box-up">▲</div>'  
        elif old_pos < pos:
            trend_html = '<div class="badge-trend trend-box-down">▼</div>'  
        else:
            trend_html = '<div class="badge-trend trend-box-stable">•</div>'  
            
        bg_style = ""
        if pos == 1 and row['Punkty'] > 0:
            bg_style = 'style="background-color: #16A34A; font-weight: bold; color: #FFFFFF;"' 
        elif pos == len(df_scores) and row['Punkty'] > 0:
            bg_style = 'style="background-color: #DC2626; font-weight: bold; color: #FFFFFF;"' 
            
        # Pobieramy czas odliczania dla danego zawodnika
        countdown_html = get_time_to_next_unbet_match(player_name, now_time)
        
        html_rows += f"""
        <tr {bg_style}>
            <td style="text-align:center;"><b>{pos}</b></td>
            <td style="text-align:center;">{trend_html}</td>
            <td>{player_name}</td>
            <td><b>{row['Punkty']} pkt</b></td>
            <td>{countdown_html}</td>
        </tr>
        """
    return f"""
        <table class="kricon-table">
            <tr>
                <th style="width:10%; text-align:center;">Msc.</th>
                <th style="width:10%; text-align:center;">Trend</th>
                <th>Gracz</th>
                <th>Punkty</th>
                <th>Najbliższy mecz</th>
            </tr>
            {html_rows}
        </table>
    """

# System Logowania
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

now = datetime.now()

if st.session_state.logged_in_user is None:
    # PODZIAŁ OKNA LOGOWANIA: Formularz po lewej, klasyfikacja na żywo z odliczaniem po prawej
    col_login, col_board = st.columns([2, 3], gap="large")
    
    with col_login:
        st.subheader("🔒 Logowanie do systemu Kricon Typer")
        username = st.selectbox("Wybierz użytkownika:", [""] + list(USER_CREDENTIALS.keys()))
        password = st.text_input("Wpisz hasło:", type="password")
        
        if st.button("Zaloguj się"):
            if USER_CREDENTIALS.get(username) == password:
                st.session_state.logged_in_user = username
                st.rerun()
            else:
                st.error("Błędne hasło. Spróbuj ponownie.")
                
    with col_board:
        st.subheader("📊 Aktualna Klasyfikacja i Stan Obstawień")
        st.markdown(render_leaderboard_html(now), unsafe_allow_html=True)
else:
    current_user = st.session_state.logged_in_user
    st.sidebar.write(f"👤 Zalogowany jako: **{current_user}**")
    if st.sidebar.button("Wyloguj się"):
        st.session_state.logged_in_user = None
        st.rerun()

    # --- LOGIKA AUTOMATYCZNYCH PRZYPOMNIEŃ POP-UP ---
    for match_id, match in st.session_state.results.items():
        if match["status"] == "Oczekuje":
            try:
                time_to_match = match["timestamp"] - now
                if timedelta(hours=0) < time_to_match <= timedelta(hours=1):
                    for player in players:
                        if player not in st.session_state.bets[match_id] or st.session_state.bets[match_id][player] == (None, None):
                            match_name = f"{match['home']} - {match['away']}"
                            alert_msg = f"Hej {player}, zapomniałeś obstawić mecz {match_name}, który zaraz się zaczyna!"
                            st.toast(alert_msg, icon="⚠️")
                            st.warning(alert_msg)
            except Exception:
                pass 

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Klasyfikacja", "📅 Lista Meczów (Terminarz)", "📈 Tabele Grup", "⚙️ Admin"])

    # ZAKŁADKA 1: KLASYFIKACJA (PO ZALOGOWANIU)
    with tab1:
        st.header("Tabela Wyników Typera")
        new_positions = {}
        st.markdown(render_leaderboard_html(now, new_positions), unsafe_allow_html=True)

    # ZAKŁADKA 2: TERMINARZ
    with tab2:
        if current_user == "admin":
            st.warning("Zaloguj się jako gracz, aby typować.")
        else:
            st.header("Terminarz Mistrzostw Świata 2026")
            
            view_mode = st.radio(
                "Pokaż mecze:", 
                ["Oczekujące (Od najbliższych)", "Wszystkie 104 mecze", "Tylko Zakończone"], 
                horizontal=True,
                key="user_view_mode"
            )
            st.divider()
            
            sorted_matches = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
            
            matches_shown = 0
            for match_id, match in sorted_matches:
                if view_mode == "Oczekujące (Od najbliższych)" and match['status'] == "Zakończony":
                    continue
                if view_mode == "Tylko Zakończone" and match['status'] == "Oczekuje":
                    continue
                
                matches_shown += 1
                is_lock_time = (match['timestamp'] - now).total_seconds() <= 0
                
                st.markdown(f"<div class='match-container'>", unsafe_allow_html=True)
                st.markdown(f"<div class='match-header'>⚽ Mecz #{match_id}</div>", unsafe_allow_html=True)
                st.markdown(f"### {get_flag_html(match['home'])} vs {get_flag_html(match['away'])}", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #94A3B8; margin-bottom:15px;'>Faza: <b>{match['stage']}</b> | Data: {match['date']}, {match['time']}</p>", unsafe_allow_html=True)
                
                if match['status'] == "Zakończony":
                    st.markdown(f"<p class='real-score'>Oficjalny wynik: {match['score_h']} - {match['score_a']}</p>", unsafe_allow_html=True)
                elif is_lock_time:
                    st.markdown("<p style='color: #F87171; font-weight: bold;'>⚠️ Obstawianie tego meczu zostało zablokowane (mecz w toku lub oczekuje na wynik).</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #4ADE80;'>• Rejestracja typów otwarta</p>", unsafe_allow_html=True)
                
                curr_h, curr_a = st.session_state.bets[match_id].get(current_user, (None, None))
                
                c1, c2, c3 = st.columns([1, 1, 2])
                with c1:
                    bet_h = st.number_input(f"Typ: {match['home']}", min_value=0, step=1, key=f"h_{match_id}", value=curr_h if curr_h is not None else 0, disabled=is_lock_time)
                with c2:
                    bet_a = st.number_input(f"Typ: {match['away']}", min_value=0, step=1, key=f"a_{match_id}", value=curr_a if curr_a is not None else 0, disabled=is_lock_time)
                with c3:
                    st.write("")
                    st.write("")
                    if match['status'] == "Zakończony" or is_lock_time:
                        st.button("Zablokowane", disabled=True, key=f"dis_{match_id}")
                    else:
                        if st.button("Zapisz typ", key=f"btn_{match_id}"):
                            st.session_state.bets[match_id][current_user] = (bet_h, bet_a)
                            st.success("Zapisano pomyślnie!")
                
                if is_lock_time or match['status'] == "Zakończony":
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
                            st.write("Nikt z graczy nie obstawił tego meczu.")
                else:
                    st.info("🔒 Typy innych graczy zostaną odsłonięte po rozpoczęciu spotkania.")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            if matches_shown == 0:
                st.info("Brak meczów w wybranej kategorii.")

    # ZAKŁADKA 3: TABELE GRUP
    with tab3:
        st.header("📈 Tabele Fazy Grupowej (Zestawienie Listowe)")
        st.write("Wszystkie grupy zaprezentowane jedna pod drugą w kolejności A-L.")
        st.divider()
        
        for group_name in list(GROUPS_DICT.keys()):
            st.markdown(f"### {group_name}")
            teams_stats = {t: {"Punkty": 0, "BZ": 0, "BS": 0, "RB": 0} for t in GROUPS_DICT[group_name]}
            
            for match in st.session_state.results.values():
                if match["stage"] == group_name and match["status"] == "Zakończony":
                    h_team, a_team = match["home"], match["away"]
                    sh, sa = match["score_h"], match["score_a"]
                    
                    teams_stats[h_team]["BZ"] += sh
                    teams_stats[h_team]["BS"] += sa
                    teams_stats[h_team]["RB"] += (sh - sa)
                    
                    teams_stats[a_team]["BZ"] += sa
                    teams_stats[a_team]["BS"] += sh
                    teams_stats[a_team]["RB"] += (sa - sh)
                    
                    if sh > sa:
                        teams_stats[h_team]["Punkty"] += 3
                    elif sa > sh:
                        teams_stats[a_team]["Punkty"] += 3
                    else:
                        teams_stats[h_team]["Punkty"] += 1
                        teams_stats[a_team]["Punkty"] += 1
                        
            df_group = pd.DataFrame.from_dict(teams_stats, orient='index').reset_index()
            df_group.rename(columns={'index': 'Reprezentacja'}, inplace=True)
            df_group = df_group.sort_values(by=["Punkty", "RB", "BZ"], ascending=[False, False, False]).reset_index(drop=True)
            df_group.index += 1
            
            group_rows = ""
            for idx, row in df_group.iterrows():
                group_rows += f"""
                <tr>
                    <td><b>{idx}</b></td>
                    <td>{get_flag_html(row['Reprezentacja'])}</td>
                    <td><b>{row['Punkty']}</b></td>
                    <td>{row['BZ']}</td>
                    <td>{row['BS']}</td>
                    <td>{row['RB']}</td>
                </tr>
                """
                
            st.markdown(f"""
                <table class="kricon-table">
                    <tr>
                        <th>Poz.</th><th>Reprezentacja</th><th>Pkt</th><th>BZ</th><th>BS</th><th>Bilans</th>
                    </tr>
                    {group_rows}
                </table>
            """, unsafe_allow_html=True)

    # ZAKŁADKA 4: ADMIN
    with tab4:
        if current_user != "admin":
            st.error("Zaloguj się jako 'admin', aby wpisywać wyniki.")
        else:
            st.header("⚙️ Wprowadzanie Wyników (Lista Chronologiczna)")
            search_query = st.text_input("Wyszukaj mecz po fazie, państwie lub dacie:").lower()
            st.divider()
            
            sorted_admin_matches = sorted(st.session_state.results.items(), key=lambda x: (x[1]['timestamp'], x[0]))
            
            for match_id, match in sorted_admin_matches:
                match_text = f"mecz #{match_id} {match['stage']} {match['home']} {match['away']} {match['date']}".lower()
                
                if search_query and search_query not in match_text:
                    continue
                
                st.markdown(f"<div class='match-container' style='padding: 15px;'>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #F97316; font-weight: bold; font-size: 1.2rem;'>Mecz #{match_id}</span> | **{get_flag_html(match['home'])} vs {get_flag_html(match['away'])}** <br><span style='color:#94A3B8; font-size:0.9rem;'>({match['stage']} - {match['date']} {match['time']})</span>", unsafe_allow_html=True)
                
                if "TBD" in match["home"] or "Finał" in match["stage"] or "1/" in match["stage"]:
                    col_h, col_a = st.columns(2)
                    with col_h:
                        new_home = st.text_input(f"Zmień: Drużyna 1 (Mecz #{match_id})", value=match["home"], key=f"edit_h_{match_id}")
                    with col_a:
                        new_away = st.text_input(f"Zmień: Drużyna 2 (Mecz #{match_id})", value=match["away"], key=f"edit_a_{match_id}")
                    st.session_state.results[match_id]["home"] = new_home
                    st.session_state.results[match_id]["away"] = new_away

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
                        
                        temp_positions = {}
                        render_leaderboard_html(now, temp_positions)
                        st.session_state.last_positions = temp_positions
                        
                        st.success("Tabela i punkty przeliczone!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
