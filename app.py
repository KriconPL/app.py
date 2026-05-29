import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 1. Konfiguracja i Szata Graficzna zgodna z nowym brandingiem KriCon Group
st.set_page_config(page_title="Kricon BV - Typer MŚ 2026", page_icon="⚽", layout="wide")

# CSS dla nowoczesnej i przejrzystej stylizacji brandingowej KriCon (Navy & Orange)
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
    
    h2, h3 { 
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
        margin: 15px 0;
        font-size: 1rem;
        min-width: 400px;
        background-color: #FFFFFF;
    }
    .kricon-table th {
        background-color: var(--kricon-navy) !important;
        color: white !important;
        text-align: left;
        padding: 12px;
        font-weight: 600;
    }
    .kricon-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #E5E7EB;
    }
    .kricon-table tr:hover {
        background-color: var(--kricon-navy-background) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Mapowanie Państw na Kody ISO
COUNTRY_FLAGS = {
    "Meksyk": "mx", "RPA": "za", "Korea Południowa": "kr", "Czechy": "cz",
    "Kanada": "ca", "Bośnia i Hercegowina": "ba", "Katar": "qa", "Szwajcaria": "ch",
    "Brazylia": "br", "Maroko": "ma", "Haiti": "ht", "Szkocja": "gb-sct",
    "USA": "us", "Paragwaj": "py", "Australia": "au", "Turcja": "tr",
    "Niemcy": "de", "Curaçao": "cw", "WKS": "
