import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. Konfiguracja i Szata Graficzna
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .reportview-container, .main .block-container { 
        background: #FFFFFF; 
        color: #1F2937; 
    }
    .main .block-container { padding-top: 1rem; }
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
        width: auto;
    }
    .logo-title-container h1 {
        color: #1E3A8A !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin: 0 !important;
        border: none !important;
        padding: 0 !important;
    }
    h2, h3 { 
        color: #1E3A8A !important;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
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
    div[data-testid="stNotification"] {
        background-color: #EFF6FF !important;
        color: #1E3A8A !important;
        border-left: 5px solid #3B82F6 !important;
        border-radius: 4px;
    }
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
    .stTabs [data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #3B82F6 !important;
        color: #1E3A8A !important;
    }
    .kricon-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 1rem;
        min-width: 400px;
    }
    .kricon-table th {
        background-color: #1E3A8A;
        color: white;
        text-align: left;
        padding: 12px;
        font-weight: 600;
    }
    .kricon-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #E5E7EB;
    }
    .kricon-table tr:hover {
        background-color: #F8FAFC;
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
    "Hiszpania": "es", "Wyspy Zielonego Przylądka": "
