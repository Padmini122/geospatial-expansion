import streamlit as st
import pandas as pd
from src.data_loader import prepare_full_data
from src.geo_analysis import perform_kmeans_clustering, find_expansion_candidates
from src.visualization import create_sales_heatmap, create_existing_stores_map, create_opportunity_tier_map_plotly
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Geo Expansion Dashboard")

@st.cache_data
def load_and_prepare():
    df = prepare_full_data("data/sample_geo_data.csv")
    df, _ = perform_kmeans_clustering(df, n_clusters=5)
    return df

st.title("📍 Geospatial Business Expansion")
st.markdown("Find high‑demand / low‑presence areas using opportunity scoring + clustering")

# Load data
df = load_and_prepare()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_zones = st.sidebar.multiselect("City Zone", options=df['zone'].unique(), default=df['zone'].unique())
min_sales = st.sidebar.slider("Minimum Sales ($)", min_value=float(df['sales'].min()), max_value=float(df['sales'].max()), value=float(df['sales'].min()))
selected_tiers = st.sidebar.multiselect("Expansion Tier", options=df['expansion_tier'].unique(), default=df['expansion_tier'].unique())

filtered_df = df[
    (df['zone'].isin(selected_zones)) &
    (df['sales'] >= min_sales) &
    (df['expansion_tier'].isin(selected_tiers))
]

st.subheader(f"📊 Data Overview ({len(filtered_df)} locations)")

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your filters.")
    st.dataframe(pd.DataFrame())
else:
    st.dataframe(filtered_df[['store_id', 'latitude', 'longitude', 'sales', 'competitor_count', 'population', 'opportunity_score', 'expansion_tier', 'zone']].head(100))

    # Three key visuals in tabs
    tab1, tab2, tab3 = st.tabs(["🔥 Sales Heatmap", "🏬 Existing Stores", "🎯 Opportunity Zones (Tier Map)"])

    with tab1:
        st.markdown("**Sales‑weighted heatmap** – hotter = higher sales volume")
        heatmap = create_sales_heatmap(filtered_df, sample_size=2000)
        st_folium(heatmap, width=800, height=500)

    with tab2:
        st.markdown("**All store locations** – color: green (few competitors) → red (many competitors)")
        stores_map = create_existing_stores_map(filtered_df)
        st_folium(stores_map, width=800, height=500)

    with tab3:
        st.markdown("**Tier 1 (red) = highest expansion potential** – sales × population / (competitors+1)")
        fig = create_opportunity_tier_map_plotly(filtered_df)
        # Fix deprecation: replace use_container_width with width='stretch'
        st.plotly_chart(fig, width='stretch')

# Top expansion candidates (show only if filter not empty)
st.sidebar.subheader("🔍 Top Expansion Candidates (from current filter)")
if not filtered_df.empty:
    top_candidates = find_expansion_candidates(filtered_df, top_n=10)
    st.sidebar.dataframe(top_candidates[['store_id', 'sales', 'competitor_count', 'population', 'opportunity_score', 'expansion_tier']])
else:
    st.sidebar.info("No candidates with current filters.")

st.sidebar.info("Opportunity Score = (Sales × Population) / (Competitors+1)")