import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Typer MŚ 2026", page_icon="🏆", layout="wide")

st.title("🏆 Typer Mistrzostw Świata 2026")

# Lista graczy
players = ["Adam", "Maciej", "Marcin", "Kamil", "Kuba M", "Tomek", "Kuba K", "Rafał"]

# Baza drużyn i grup
groups = {
    "A": ["🇲🇽 Meksyk", "🇨🇭 Szwajcaria", "🇳🇬 Nigeria", "🇳🇿 Nowa Zelandia"],
    "B": ["🇨🇦 Kanada", "🇩🇰 Dania", "🇨🇲 Kamerun", "🇶🇦 Katar"],
    "C": ["🇺🇸 USA", "🇵🇱 Polska", "🇿🇦 RPA", "🇺🇿 Uzbekistan"],
    "D": ["🇦🇷 Argentyna", "🇷🇸 Serbia", "🇩🇿 Algieria", "🇵🇦 Panama"],
    "E": ["🇫🇷 Francja", "🇨🇴 Kolumbia", "🇮🇶 Irak", "🇯🇲 Jamajka"],
    "F": ["🇧🇷 Brazylia", "🇦🇹 Austria", "🇬🇭 Ghana", "🇸🇦 Arabia Saudyjska"],
    "G": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Anglia", "🇪🇨 Ekwador", "🇲🇦 Maroko", "🇨🇷 Kostaryka"],
    "H": ["🇪🇸 Hiszpania", "🇨🇱 Chile", "🇸🇳 Senegal", "🇦🇺 Australia"],
    "I": ["🇩🇪 Niemcy", "🇺🇾 Urugwaj", "🇨🇮 WKS", "🇮🇷 Iran"],
    "J": ["🇵🇹 Portugalia", "🇵🇪 Peru", "🇪🇬 Egipt", "🇯🇵 Japonia"],
    "K": ["🇮🇹 Włochy", "🇻🇪 Wenezuela", "🇰🇷 Korea Płd.", "🇸🇪 Szwecja"],
    "L": ["🇳🇱 Holandia", "🇭🇷 Chorwacja", "🇧🇪 Belgia", "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Walia"]
}

# Generowanie harmonogramu 72 meczów
match_schedule = []
match_id = 1
for grp_name, teams in groups.items():
    t1, t2, t3, t4 = teams
    matchups = [(t1, t2), (t3, t4), (t1, t3), (t2, t4), (t1, t4), (t2, t3)]
    for h, a in matchups:
        match_schedule.append((match_id, grp_name, h, a))
        match_id += 1

# Inicjalizacja sesji
if 'bets' not in st.session_state:
    st.session_state.bets = {m[0]: {} for m in match_schedule} 

if 'results' not in st.session_state:
    st.session_state.results = {}
    for m_id, grp, h, a in match_schedule:
        st.session_state.results[m_id] = {"group": grp, "home": h, "away": a, "score_h": None, "score_a": None}

def calculate_points(pred_h, pred_a, real_h, real_a):
    if pd.isna(real_h) or pd.isna(real_a) or pd.isna(pred_h) or pd.isna(pred_a):
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

tab1, tab2, tab3 = st.tabs(["📊 Klasyfikacja", "🎯 Typuj", "⚙️ Wyniki (Admin)"])

# ----------------- ZAKŁADKA 1: KLASYFIKACJA -----------------
with tab1:
    st.header("Klasyfikacja Generalna")
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
            return ['background-color: #A9DFBF'] * len(row)
        elif row.name == len(df_scores) and row['Punkty'] > 0:
            return ['background-color: #F5B7B1'] * len(row)
        return [''] * len(row)

    st.dataframe(df_scores.style.apply(highlight_rows, axis=1), use_container_width=True)

# ----------------- ZAKŁADKA 2: TYPOWANIE -----------------
with tab2:
    st.header("Wprowadź swoje typy")
    
    col_player, col_group = st.columns(2)
    with col_player:
        selected_player = st.selectbox("Wybierz swoje imię:", players)
    with col_group:
        group_filter = st.selectbox("Wybierz grupę meczów:", ["Wszystkie"] + list(groups.keys()))
    
    st.divider()
    
    for match_id, match in st.session_state.results.items():
        if group_filter != "Wszystkie" and match["group"] != group_filter:
            continue
            
        st.markdown(f"**Mecz {match_id} (Grupa {match['group']}):**")
        curr_h, curr_a = st.session_state.bets[match_id].get(selected_player, (None, None))
        
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            bet_h = st.number_input(f"{match['home']}", min_value=0, step=1, key=f"h_{match_id}_{selected_player}", value=curr_h if curr_h is not None else 0)
        with c2:
            bet_a = st.number_input(f"{match['away']}", min_value=0, step=1, key=f"a_{match_id}_{selected_player}", value=curr_a if curr_a is not None else 0)
        with c3:
            st.write("")
            st.write("")
            if st.button("Zapisz", key=f"btn_{match_id}_{selected_player}"):
                st.session_state.bets[match_id][selected_player] = (bet_h, bet_a)
                st.success("Zapisano!")
        st.divider()

# ----------------- ZAKŁADKA 3: ADMIN -----------------
with tab3:
    st.header("Panel Administratora")
    st.caption("Tutaj podajesz oficjalne wyniki. Od razu przeliczą klasyfikację.")
    
    admin_group_filter = st.selectbox("Filtruj grupę (Admin):", ["Wszystkie"] + list(groups.keys()))
    st.divider()
    
    for match_id, match in st.session_state.results.items():
        if admin_group_filter != "Wszystkie" and match["group"] != admin_group_filter:
            continue
            
        st.markdown(f"**Mecz {match_id} (Grupa {match['group']}):**")
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            res_h = st.number_input(f"Wynik {match['home']}", min_value=0, step=1, key=f"res_h_{match_id}", value=match['score_h'] if match['score_h'] is not None else 0)
        with c2:
            res_a = st.number_input(f"Wynik {match['away']}", min_value=0, step=1, key=f"res_a_{match_id}", value=match['score_a'] if match['score_a'] is not None else 0)
        with c3:
            st.write("")
            st.write("")
            if st.button("Zatwierdź wynik", key=f"res_btn_{match_id}"):
                st.session_state.results[match_id]['score_h'] = res_h
                st.session_state.results[match_id]['score_a'] = res_a
                st.success("Zaktualizowano tabelę!")
        st.divider()
