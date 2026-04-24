import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

 #── PAGE CONFIG ──
st.set_page_config(
    page_title="Global Health Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/deannalakshman/Desktop/IIT/YEAR 2/SEM 2/DSPLC/Individual technical/Cleaned_datasets/Health_Coverage_Financial_Hardship.csv")
    return df

df = load_data()

# ── PREFILTER TOTAL ROWS ──
df_total = df[
    (df['URBANIZATION_LABEL'] == 'Total') &
    (df['IC_QUINTILE_LABEL'] == 'All') &
    (df['FINANCIAL_HARDSHIP_LABEL'] == 'All')
]

# ── SIDEBAR ──
st.sidebar.image("/Users/deannalakshman/Desktop/IIT/YEAR 2/SEM 2/DSPLC/Individual technical/dashboard/who-logo.png", width=250)
st.sidebar.title("Global Health Dashboard")
st.sidebar.markdown("Exploring Universal Health Coverage and Financial Hardship across 165 countries (2000–2023)")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🌍 Global Overview",
    "📈 Trends Over Time",
    "🔍 Country Deep Dive",
    "📊 Correlation & Breakdown"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** WHO Universal Health Coverage")