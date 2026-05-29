import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Typer MŚ 2026", page_icon="⚽", layout="wide")

st.title("⚽ Typer Mistrzostw Świata 2026")

# Twoja ekipa
players = ["Adam", "Maciej", "Marcin", "Kamil", "Kuba M", "Tomek", "Kuba K", "Rafał"]

# Inicjalizacja bazy w pamięci (do testów)
if 'bets' not in st.session_state:
    st.session_state.bets = {1: {}, 2: {}} 

if 'results' not in st.session_state:
    st.session_state.results = {
        1: {"home": "🇲🇽 Meksyk", "away": "🇨🇭 Szwajcaria", "score_h": None, "score_a": None},
        2: {"home": "🇵🇱 Polska", "away": "🇺🇸 USA", "score_h": None, "score_a": None}
    }

def calculate_points(pred_h, pred_a, real_h, real_a):
    if pd.isna(real_h) or pd.isna(real_a) or pd.isna(pred_h) or pd.isna(pred_a):
        return 0
    if pred_h == real_h and pred_a == real_a:
        return 3
    if np.sign(pred_h - pred_a) == np.sign(real_h - real_a):
        return 1
    return 0

tab1, tab2, tab3 = st.tabs(["📊 Klasyfikacja", "🎯 Typuj", "⚙️ Wyniki (Admin)"])

with tab1:
    st.header("Klasyfikacja Generalna")
    scores = {player: 0 for player in players}
    for match_id, result in st.session_state.results.items():
        r_h, r_a = result['score_h'], result['score_a']
        for player in players:
            if player in st.session_state.bets[match_id]:
                p_h, p_a = st.session_state.bets[match_id][player]
                scores[player] += calculate_points(p_h, p_a, r_h, r_a)
                
    # Sortowanie tabeli
    df_scores = pd.DataFrame(list(scores.items()), columns=["Gracz", "Punkty"])
    df_scores = df_scores.sort_values(by="Punkty", ascending=False).reset_index(drop=True)
    df_scores.index += 1
    
    # Wyświetlanie stylizowanej tabeli
    def highlight_rows(row):
        if row.name == 1 and row['Punkty'] > 0:
            return ['background-color: #A9DFBF'] * len(row) # Zielony lider
        elif row.name == len(df_scores) and row['Punkty'] > 0:
            return ['background-color: #F5B7B1'] * len(row) # Czerwony ostatni
        return [''] * len(row)

    st.dataframe(df_scores.style.apply(highlight_rows, axis=1), use_container_width=True)

with tab2:
    st.header("Wprowadź swoje typy")
    selected_player = st.selectbox("Wybierz swoje imię:", players)
    
    for match_id, match in st.session_state.results.items():
        st.write(f"**Mecz {match_id}: {match['home']} vs {match['away']}**")
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

with tab3:
    st.header("Panel Administratora")
    st.caption("Tylko dla osoby zarządzającej wynikami.")
    for match_id, match in st.session_state.results.items():
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            res_h = st.number_input(f"Wynik {match['home']}", min_value=0, step=1, key=f"res_h_{match_id}", value=match['score_h'] if match['score_h'] is not None else 0)
        with c2:
            res_a = st.number_input(f"Wynik {match['away']}", min_value=0, step=1, key=f"res_a_{match_id}", value=match['score_a'] if match['score_a'] is not None else 0)
        with c3:
            st.write("")
            st.write("")
            if st.button("Zatwierdź oficjalny wynik", key=f"res_btn_{match_id}"):
                st.session_state.results[match_id]['score_h'] = res_h
                st.session_state.results[match_id]['score_a'] = res_a
                st.success("Zaktualizowano tabelę!")
