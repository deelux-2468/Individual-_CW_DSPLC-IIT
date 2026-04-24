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
        /* ── FONT: loads Lexend Deca from Google Fonts ── */
        @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;500;600;700&display=swap');
        
        /* ── FONT: applies to the entire page body ── */
        html, body, [class*="css"] {
            font-family: 'Lexend Deca', sans-serif;
            font-weight: 200;
        }
        
        /* ── FONT: makes headings bold ── */
        h1, h2, h3 {
            font-family: 'Lexend Deca', sans-serif;
            font-weight: 600;
        }
        
        /* ── FONT: forces all text elements to use the same font ── */
        p, span, div, label, li {
            font-family: 'Lexend Deca', sans-serif !important;
        }
        
        /* ── SIDEBAR: background colour ── */
        [data-testid="stSidebar"] {
            background-color: white;
        }
        
        /* ── SIDEBAR: text colour for everything inside it ── */
        [data-testid="stSidebar"] * {
            color: #0c5369 !important;
        }

        /* ── SIDEBAR: radio button dot colour ── */
        [data-testid="stRadio"] label span {
            background-color: black !important;
            border-color: black !important;
        }
        [data-testid="stRadio"] label:first-child span {
            background-color: black !important;
        }
        
        /* ── KPI CARDS: font size and weight of the big number ── */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
        }
        
        /* ── SLIDER: the year label above the thumb ── */
        [data-testid="stSlider"] * {
            color: white !important;
        }
        
        /* ── SLIDER: the circular thumb you drag ── */
        [data-baseweb="slider"] [role="slider"] {
            background-color: white !important;
            border-color: white !important;
        }
        
        /* ── SLIDER: the filled portion of the track (left of thumb) ── */
        [data-baseweb="slider"] div[class*="TrackHighlight"] {
            background-color: #4a9cba !important;
        }
        
        /* ── SLIDER: the unfilled portion of the track (right of thumb) ── */
        [data-baseweb="slider"] div[class*="Track"] {
            background-color: #cccccc !important;
        }
        /* ── DIVIDER: custom horizontal rule - thick and white ── */
    hr {
        border: none;
        border-top: 3px solid white;
        margin: 20px 0;
        }
        /* ── MULTISELECT: tag background colour ── */
        [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background-color: #0c5369 !important;}
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
st.sidebar.image(logo_path, width=250)
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

if page == "🌍 Global Overview":
    st.title("Global Overview")
    st.markdown("Exploring financial hardship from out-of-pocket health spending across 162 countries.")

    selected_year = st.slider(
        "Select Year", min_value=2000, max_value=2023,
        value=2019, step=1
    )
    yr = str(selected_year)

    map_df = df_total[['REF_AREA_LABEL', yr]].dropna(subset=[yr]).copy()
    map_df.columns = ['Country', 'Value']

    c1, div1, c2, div2, c3, div3, c4 = st.columns([10, 0.5, 10, 0.5, 10, 0.5, 10])

    with c1:
        st.metric("Countries with data", len(map_df))
    with div1:
        st.markdown("<div style='border-left: 2px solid white; height: 60px; margin-top: 10px;'></div>", unsafe_allow_html=True)
    with c2:
        st.metric("Global Average (%)", f"{map_df['Value'].mean():.1f}")
    with div2:
        st.markdown("<div style='border-left: 2px solid white; height: 60px; margin-top: 10px;'></div>", unsafe_allow_html=True)
    with c3:
        st.metric("Highest Rate (%)", f"{map_df['Value'].max():.1f}")
    with div3:
        st.markdown("<div style='border-left: 2px solid white; height: 60px; margin-top: 10px;'></div>", unsafe_allow_html=True)
    with c4:
        top_country = map_df.loc[map_df['Value'].idxmax(), 'Country']
        st.metric("Most Affected", top_country)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader(f"Financial Hardship by Country — {selected_year}")

    fig_map = px.choropleth(
        map_df,
        locations="Country",
        locationmode="country names",
        color="Value",
        hover_name="Country",
        color_continuous_scale=["#d0eaf3", "#4a9cba", "#0c5369", "#07303d"],
        labels={"Value": "% Population"},
        title=f"Population (%) facing financial hardship from OOP health spending ({selected_year})"
    )
    fig_map.update_layout(
        font=dict(family='Lexend Deca, sans-serif'),
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        coloraxis_colorbar=dict(title="% Population"),
        margin=dict(l=0, r=0, t=40, b=0),
        height=480
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    top10    = map_df.nlargest(10, 'Value').sort_values('Value')
    bottom10 = map_df.nsmallest(10, 'Value').sort_values('Value', ascending=False)

    with col_left:
        st.subheader(f"Top 10 Most Affected — {selected_year}")
        fig_top = px.bar(
            top10, x='Value', y='Country', orientation='h',
            color='Value',
            color_continuous_scale=["#4a9cba", "#0c5369"],
            labels={'Value': '% Population', 'Country': ''}
        )
        fig_top.update_layout(
            font=dict(family="Lexend Deca, sans-serif"),
            coloraxis_showscale=False,
            xaxis_title="% Population",
            height=380,
            margin=dict(l=0, r=20, t=40, b=0)
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_right:
        st.subheader(f"Top 10 Least Affected — {selected_year}")
        fig_bot = px.bar(
            bottom10, x='Value', y='Country', orientation='h',
            color='Value',
            color_continuous_scale=["#d0eaf3", "#4a9cba"],
            labels={'Value': '% Population', 'Country': ''}
        )
        fig_bot.update_layout(
            font=dict(family="Lexend Deca, sans-serif"),
            coloraxis_showscale=False,
            xaxis_title="% Population",
            height=380,
            margin=dict(l=0, r=20, t=40, b=0)
        )
        st.plotly_chart(fig_bot, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"Distribution of Hardship Rates — {selected_year}")

    # Build histogram data manually so we can colour each bar by its x value
    import numpy as np
    counts, bin_edges = np.histogram(map_df['Value'].dropna(), bins=30)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    fig_hist = go.Figure(go.Bar(
        x=bin_centers,
        y=counts,
        marker=dict(
            color=bin_centers,
            colorscale=["#d0eaf3", "#4a9cba", "#0c5369"],
            showscale=False
        )
    ))
    fig_hist.update_layout(
        font=dict(family="Lexend Deca, sans-serif"),
        xaxis_title="% Population facing financial hardship",
        yaxis_title="Number of Countries",
        height=320,
        margin=dict(l=0, r=0, t=40, b=0),
        bargap=0.05
    )
    st.plotly_chart(fig_hist, use_container_width=True)

elif page == "📈 Trends Over Time":
    st.title("Trends Over Time")
    st.markdown("Track how financial hardship has evolved across countries from 2000 to 2023.")

    all_countries = sorted(df['REF_AREA_LABEL'].unique().tolist())
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        selected_countries = st.multiselect(
            "Select Countries",
            options=all_countries,
            default=["India", "Brazil", "Nigeria", "Germany"]
        )
    with col_f2:
        selected_hardship = st.selectbox(
            "Select Hardship Type",
            options=["All", "Large OOP", "Impoverishing", "Pushed into poverty", "Further impoverished"]
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Hardship Rate Over Time")

    YEARS = [str(y) for y in range(2000, 2024)]

    df_lines = df[
        (df['REF_AREA_LABEL'].isin(selected_countries)) &
        (df['URBANIZATION_LABEL'] == 'Total') &
        (df['IC_QUINTILE_LABEL'] == 'All') &
        (df['FINANCIAL_HARDSHIP_LABEL'] == selected_hardship)
    ].copy()

    df_melted = df_lines.melt(
        id_vars=['REF_AREA_LABEL'],
        value_vars=YEARS,
        var_name='Year',
        value_name='Value'
    )
    df_melted['Year'] = df_melted['Year'].astype(int)
    df_melted = df_melted.dropna(subset=['Value'])

    fig_line = px.line(
        df_melted,
        x='Year', y='Value',
        color='REF_AREA_LABEL',
        markers=True,
        labels={'Value': '% Population', 'REF_AREA_LABEL': 'Country', 'Year': 'Year'}
    )
    fig_line.update_layout(
        font=dict(family="Lexend Deca, sans-serif"),
        xaxis_title="Year",
        yaxis_title="% Population facing financial hardship",
        height=450,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(title="Country")
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Global Average Trend Over Time")

    df_avg = df_total[YEARS].mean().reset_index()
    df_avg.columns = ['Year', 'Value']
    df_avg['Year'] = df_avg['Year'].astype(int)

    fig_area = px.area(
        df_avg,
        x='Year', y='Value',
        color_discrete_sequence=["#4a9cba"],
        labels={'Value': '% Population', 'Year': 'Year'}
    )
    fig_area.update_layout(
        font=dict(family="Lexend Deca, sans-serif"),
        xaxis_title="Year",
        yaxis_title="Global Average % facing financial hardship",
        height=350,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig_area.update_traces(line_color="#0c5369", fillcolor="rgba(74, 156, 186, 0.3)")
    st.plotly_chart(fig_area, use_container_width=True)