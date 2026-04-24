import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Global Health Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ── CUSTOM STYLING ──
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
        }
        [data-testid="stSidebar"] {
            background-color: white;
        }
        [data-testid="stSidebar"] * {
            color: #0c5369 !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, '..', 'Cleaned_Datasets', 'Financial_Hardships_Cleaned.csv')
    return pd.read_csv(path)

df = load_data()

# ── PREFILTER TOTAL ROWS ──
df_total = df[
    (df['URBANIZATION_LABEL'] == 'Total') &
    (df['IC_QUINTILE_LABEL'] == 'All') &
    (df['FINANCIAL_HARDSHIP_LABEL'] == 'All')
]

# ── SIDEBAR ──
base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, 'WHO_logo.png')
st.sidebar.image(logo_path, width=200)
st.sidebar.title("Global Health Dashboard")
st.sidebar.markdown("Exploring Financial Hardship due to out-of-pocket health expenditure across 162 countries (2000–2023)")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🌍 Global Overview",
    "📈 Trends Over Time",
    "🔍 Country Deep Dive",
    "📊 Breakdown Analysis"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** WHO Universal Health Coverage")