import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Health Dashboard", 
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Cleaned_datasets/Health_Coverage_Financial_Hardship.csv')
    return df

df = load_data()

# sidebar navigation
st.sidebar.title("Global Health Dashboard")
page = st.sidebar.radio("Navigate", [
    "Global Overview",
    "Trends Over Time",
    "Country Analysis",
    "Correlation",
    "Breakdown Analysis"
])

st.sidebar.markdown("---")
st.sidebar.markdown("Data Source: WHO Universal Health Coverage")
