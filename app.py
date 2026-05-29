Python
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 1. Konfiguracja i Szata Graficzna zgodna z brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    :root {
        --kricon-navy: #0F172A;
        --kricon-navy-light: #1E293B;
        --kricon-navy-background: #F1F5F9;
        --kricon-orange: #F97316;
        --kricon-orange-hover: #EA580C;
        --kricon-orange-background: #FEF3E2;
    }

    .reportview-container, .main .block-container { 
        background: #FFFFFF !important; 
        color: var(--kricon-navy) !important; 
    }
    .main .block-container { padding-top: 1rem; }
    
    [data-testid="stSidebar"] {
        background-color: var(--kricon-navy-background) !important;
    }

    .logo-title-container {
        display: flex;
        align-items: center;
        border-bottom: 3px solid var(--kricon-orange) !important;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .logo-container {
        margin-right: 20px;
    }
    .logo-image {
        max-height: 80px;
        width: auto;
    }
    
    .logo-title-container h1 {
        color: var(--kricon-navy) !important; 
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin: 0 !important;
        border: none !important;
        padding: 0 !important;
    }
    
    h2, h3, h4 { 
        color: var(--kricon-navy) !important;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    .stButton>button {
        background-color: var(--kricon-navy) !important;
        color: white !important;
        border-radius: 6px !important;
        border: 1px solid var(--kricon-navy) !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: var(--kricon-orange) !important;
        border-color: var(--kricon-orange) !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(249, 115, 22, 0.2);
    }
    
    div[data-testid="stNotification"] {
        background-color: var(--kricon-orange-background) !important;
        color: var(--kricon-navy) !important;
        border-left: 5px solid var(--kricon-orange) !important;
        border-radius: 4px;
    }
    
    [data-testid="stToast"] {
        background-color: var(--kricon-navy) !important;
        color: white !important;
    }
    
    .real-score { 
        font-size: 1.3rem; 
        color: var(--kricon-orange) !important; 
        font-weight: bold; 
        background-color: var(--kricon-orange-background) !important;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 5px;
    }

    .match-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--kricon-navy) !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: var(--kricon-orange) !important;
        color: var(--kricon-orange) !important;
    }

    .kricon-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 25px 0;
        font-size: 0.95rem;
        min-width: 100%;
        background-color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kricon-table th {
        background-color: var(--kricon-navy) !important;
        color: white !important;
        text-align: left;
        padding: 10px;
        font-weight: 600;
    }
    .kricon-table td {
        padding: 8px 10px;
        border-bottom: 1px solid #E5E7EB;
    }
    .kricon-table tr:hover {
        background-color: var(--kricon-navy-background) !important;
    }
    </style>
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
    "Hiszpania": "es", "Wyspy Zielonego Przylądka": "cv", "Arabia Saudyjska": "sa", "Urugwaj": "uy",
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
    return f'<img src="{flag_url}" width="22" style="vertical-align: middle; margin-right: 8px; border: 1px solid #ddd; border-radius:2px;" alt="flaga"> {country_name}'

# 2. Wyświetlanie Loga
LOCAL_LOGO_PATH = "./logo.png"

if os.path.exists(LOCAL_LOGO_PATH):
    logo_html = f'<img src="{LOCAL_LOGO_PATH}" alt="Kricon Group Logo" class="logo-image">'
else:
    logo_html = f'<span style="font-size:2em; margin-right:15px; color:#1E3A8A;">KriCon</span>'

st.markdown(f"""
    <div class="logo-title-container">
        <div class="logo-container">
            {logo_html}
        </div>
        <h1>World Cup 2026 Typer</h1>
    </div>
""", unsafe_allow_html=True)

# 3. Baza użytkowników
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

# 4. Generator Harmonogramu 104 Meczów z obiektami Datetime
def generate_schedule():
    schedule = {}
    match_id = 1
    
    # Daty fazy grupowej (Dzień, Miesiąc liczbowo, Miesiąc tekstowo)
    dates_group = [(d, 6, "Czerwca") for d in range(11, 28)]
    matchups = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
    date_idx = 0
    
    # 72 mecze grupowe
    for m_round in range(6):
        for group_name, teams in GROUPS_DICT.items():
            t1_idx, t2_idx = matchups[m_round]
            d, m_num, m_str = dates_group[date_idx % len(dates_group)]
            # Różnicowanie godzin dla estetyki (18:00, 20:00, 22:00)
            hour = 18 + (match_id % 3) * 2 
            
            schedule[match_id] = {
                "date": f"{d} {m_str}",
                "time": f"{hour}:00",
                "timestamp": datetime(2026, m_num, d, hour, 0),
                "stage": group_name,
                "home": teams[t1_idx], "away": teams[t2_idx],
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            # Co 4 mecze zmieniamy dzień
            if match_id % 4 == 0: 
                date_idx += 1

    # 32 mecze pucharowe
    ko_stages = [
        ("1/16 Finału", 16, [(28,6,"Czerwca"), (29,6,"Czerwca"), (30,6,"Czerwca"), (1,7,"Lipca"), (2,7,"Lipca"), (3,7,"Lipca")]), 
        ("1/8 Finału", 8, [(4,7,"Lipca"), (5,7,"Lipca"), (6,7,"Lipca"), (7,7,"Lipca")]), 
        ("Ćwierćfinały", 4, [(9,7,"Lipca"), (10,7,"Lipca"), (11,7,"Lipca")]), 
        ("Półfinały", 2, [(14,7,"Lipca"), (15,7,"Lipca")]), 
        ("Mecz o 3. miejsce", 1, [(18,7,"Lipca")]), 
        ("Finał", 1, [(19,7,"Lipca")])
    ]
    
    for stage_name, count, stage_dates in ko_stages:
        d_idx = 0
        for _ in range(count):
            d, m_num, m_str = stage_dates[d_idx % len(stage_dates)]
            schedule[match_id] = {
                "date": f"{d} {m_str}",
                "time": "21:00",
                "timestamp": datetime(2026, m_num, d, 21, 0),
                "stage": stage_name,
                "home": "TBD", "away": "TBD",
                "score_h": None, "score_a": None, "status": "Oczekuje"
            }
            match_id += 1
            d_idx += 1
            
    return schedule

# 5. Inicjalizacja z TWARDYM RESETEM jeśli liczba meczów jest zła (!= 104)
if 'results' not in st.session_state or len(st.session_state.results) != 104:
    st.session_state.results = generate_schedule()

if 'bets' not in st.session_state or len(st.session_state.bets) != 104:
    st.session_state.bets = {m_id: {} for m_id in st.session_state.results.keys()}

def calculate_points(pred_h, pred_a, real_h, real_a):
    if real_h is None or real_a is None or pred_h is None or pred_a is None:
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

# 6. System Logowania
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

    # --- LOGIKA AUTOMATYCZNYCH PRZYPOMNIEŃ POP-UP ---
    now = datetime.now()
    for match_id, match in st.session_state.results.items():
        if match["status"] == "Oczekuje":
            try:
                time_to_match = match["timestamp"] - now
                if timedelta(hours=0) < time_to_match <= timedelta(hours=1):
                    for player in players:
                        if player not in st.session_state.bets[match_id] or st.session_state.bets[match_id][player] == (None, None):
                            match_name = f"{match['home']} - {match['away']}"
                            alert_msg = f"ej typie {player}, zapomniałeś obstawić mecz {match_name}, który zaraz się zaczyna!"
                            st.toast(alert_msg, icon="⚠️")
                            st.warning(alert_msg)
            except Exception:
                pass 

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Klasyfikacja", "📅 Terminarz i Typy", "📈 Tabele Grup", "⚙️ Admin"])

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
        
        html_rows = ""
        for idx, row in df_scores.iterrows():
            bg_style = ""
            if idx == 1 and row['Punkty'] > 0:
                bg_style = 'style="background-color: var(--kricon-orange-background); font-weight: bold; color: var(--kricon-navy);"' 
            elif idx == len(df_scores) and row['Punkty'] > 0:
                bg_style = 'style="background-color: #FEE2E2; color: #991B1B;"' 
            
            html_rows += f"""
            <tr {bg_style}>
                <td><b>{idx}</b></td>
                <td>{row['Gracz']}</td>
                <td><b>{row['Punkty']} pkt</b></td>
            </tr>
            """
        
        st.markdown(f"""
            <table class="kricon-table">
                <tr><th>Miejsce</th><th>Gracz</th><th>Punkty</th></tr>
                {html_rows}
            </table>
        """, unsafe_allow_html=True)

    with tab2:
        if current_user == "admin":
            st.warning("Zaloguj się jako gracz, aby typować.")
        else:
            st.header("Terminarz Mistrzostw Świata 2026")
            
            # Nowy, lepszy system wyboru wyświetlanych meczów
            view_mode = st.radio(
                "Wybierz widok:", 
                ["Oczekujące (Od najbliższych)", "Wszystkie 104 mecze", "Tylko Zakończone"], 
                horizontal=True
            )
            st.divider()
            
            # Sortowanie meczów chronologicznie według prawdziwego czasu
            sorted_matches = sorted(st.session_state.results.items(), key=lambda x: x[1]['timestamp'])
            
            matches_shown = 0
            for match_id, match in sorted_matches:
                if view_mode == "Oczekujące (Od najbliższych)" and match['status'] == "Zakończony":
                    continue
                if view_mode == "Tylko Zakończone" and match['status'] == "Oczekuje":
                    continue
                
                matches_shown += 1
                
                st.markdown(f"<div class='match-container'>", unsafe_allow_html=True)
                st.markdown(f"#### {get_flag_html(match['home'])} vs {get_flag_html(match['away'])}", unsafe_allow_html=True)
                st.caption(f"Faza: **{match['stage']}** | Data: {match['date']}, {match['time']} | Mecz #{match_id}")
                
                if match['status'] == "Zakończony":
                    st.markdown(f"<p class='real-score'>Oficjalny wynik: {match['score_h']} - {match['score_a']}</p>", unsafe_allow_html=True)
                
                curr_h, curr_a = st.session_state.bets[match_id].get(current_user, (None, None))
                
                c1, c2, c3 = st.columns([1, 1, 2])
                with c1:
                    bet_h = st.number_input(f"Typ: {match['home']}", min_value=0, step=1, key=f"h_{match_id}", value=curr_h if curr_h is not None else 0)
                with c2:
                    bet_a = st.number_input(f"Typ: {match['away']}", min_value=0, step=1, key=f"a_{match_id}", value=curr_a if curr_a is not None else 0)
                with c3:
                    st.write("")
                    st.write("")
                    if match['status'] == "Zakończony":
                        st.button("Mecz Zakończony (Zablokowane)", disabled=True, key=f"dis_{match_id}")
                    else:
                        if st.button("Zapisz typ", key=f"btn_{match_id}"):
                            st.session_state.bets[match_id][current_user] = (bet_h, bet_a)
                            st.success("Zapisano pomyślnie!")
                
                if match['status'] == "Zakończony":
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
                    st.info("🔒 Typy innych graczy zostaną odsłonięte po zakończeniu meczu.")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            if matches_shown == 0:
                st.write("Brak meczów w wybranej kategorii.")

    with tab3:
        st.header("📈 Tabele Fazy Grupowej (Wszystkie)")
        st.write("Tabele są generowane automatycznie i aktualizowane po wpisaniu oficjalnych wyników.")
        st.divider()
        
        # Wyświetlanie wszystkich tabel w formie 2 kolumn dla oszczędności miejsca
        group_names = list(GROUPS_DICT.keys())
        col1, col2 = st.columns(2)
        
        for i, group_name in enumerate(group_names):
            target_col = col1 if i % 2 == 0 else col2
            
            with target_col:
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

    with tab4:
        if current_user != "admin":
            st.error("Zaloguj się jako 'admin', aby wpisywać wyniki.")
        else:
            st.header("⚙️ Wprowadzanie Wyników i Edycja")
            
            # Wyszukiwanie meczu po fazie lub nazwie dla wygody
            search_query = st.text_input("Wyszukaj mecz (np. 'Finał', 'Polska', 'Grupa A'):").lower()
            st.divider()
            
            for match_id, match in sorted(st.session_state.results.items(), key=lambda x: x[1]['timestamp']):
                match_text = f"{match['stage']} {match['home']} {match['away']} {match['date']}".lower()
                
                if search_query and search_query not in match_text:
                    continue
                    
                st.markdown(f"**{get_flag_html(match['home'])} vs {get_flag_html(match['away'])}** ({match['stage']} - {match['date']})", unsafe_allow_html=True)
                
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
                        st.success("Tabela i punkty przeliczone!")
                st.markdown("---")
