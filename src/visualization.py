import folium
from folium.plugins import HeatMap, MarkerCluster
import plotly.express as px
import pandas as pd
import numpy as np

def create_sales_heatmap(df, sample_size=None, save_path=None):
    """Folium heatmap weighted by sales. Handles empty/NaN data."""
    # If input df is empty or has no valid lat/lon
    if df.empty or df['latitude'].isna().all() or df['longitude'].isna().all():
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium.Marker([0, 0], popup="No valid location data to display").add_to(m)
        if save_path:
            m.save(save_path)
        return m

    # Drop rows with NaN in lat/lon
    df_clean = df.dropna(subset=['latitude', 'longitude']).copy()
    if df_clean.empty:
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium.Marker([0, 0], popup="No valid location data after cleaning").add_to(m)
        if save_path:
            m.save(save_path)
        return m

    if sample_size and len(df_clean) > sample_size:
        heat_df = df_clean.sample(sample_size)
    else:
        heat_df = df_clean

    center_lat = heat_df['latitude'].median()
    center_lon = heat_df['longitude'].median()
    if np.isnan(center_lat) or np.isnan(center_lon):
        center_lat, center_lon = 0, 0

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')
    heat_data = [[row['latitude'], row['longitude'], row['sales']] for _, row in heat_df.iterrows()]
    HeatMap(heat_data, radius=12, blur=10, max_zoom=1).add_to(m)

    if save_path:
        m.save(save_path)
    return m

def create_existing_stores_map(df, sample_size=None, save_path=None):
    """Marker map showing all stores, color by competitor count. Handles empty/NaN."""
    if df.empty or df['latitude'].isna().all() or df['longitude'].isna().all():
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium.Marker([0, 0], popup="No valid store data to display").add_to(m)
        if save_path:
            m.save(save_path)
        return m

    df_clean = df.dropna(subset=['latitude', 'longitude']).copy()
    if df_clean.empty:
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium.Marker([0, 0], popup="No valid location data after cleaning").add_to(m)
        if save_path:
            m.save(save_path)
        return m

    if sample_size and len(df_clean) > sample_size:
        map_df = df_clean.sample(sample_size)
    else:
        map_df = df_clean

    center_lat = map_df['latitude'].median()
    center_lon = map_df['longitude'].median()
    if np.isnan(center_lat) or np.isnan(center_lon):
        center_lat, center_lon = 0, 0

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in map_df.iterrows():
        popup_text = f"""
        <b>Store:</b> {row['store_id']}<br>
        <b>Sales:</b> ${row['sales']:,.0f}<br>
        <b>Competitors:</b> {row['competitor_count']}<br>
        <b>Population:</b> {row['population']:,}<br>
        <b>Opportunity:</b> {row['opportunity_score']:.0f}<br>
        <b>Tier:</b> {row['expansion_tier']}
        """
        color = 'green' if row['competitor_count'] <= 1 else 'orange' if row['competitor_count'] <= 3 else 'red'
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=color, icon='store', prefix='fa')
        ).add_to(marker_cluster)

    if save_path:
        m.save(save_path)
    return m

def create_opportunity_tier_map_plotly(df, save_path=None):
    """Plotly scatter_geo with fallback for empty data."""
    if df.empty or df['latitude'].isna().all() or df['longitude'].isna().all():
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="No valid location data to display", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(title="Expansion Opportunity Zones (No Data)")
        return fig

    df_clean = df.dropna(subset=['latitude', 'longitude']).copy()
    if df_clean.empty:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="No valid location data after cleaning", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(title="Expansion Opportunity Zones (No Data)")
        return fig

    fig = px.scatter_geo(
        df_clean,
        lat='latitude',
        lon='longitude',
        color='expansion_tier',
        size='opportunity_score',
        hover_name='store_id',
        hover_data={
            'sales': ':.0f',
            'competitor_count': True,
            'population': ':,.0f',
            'opportunity_score': ':,.0f'
        },
        title="Expansion Opportunity Zones (Tier 1 = Highest Potential)",
        projection="natural earth",
        color_discrete_map={
            'Tier1_High': 'red',
            'Tier2_Medium': 'orange',
            'Tier3_Low': 'green'
        }
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        resolution=50,
        showcoastlines=True,
        coastlinecolor="LightGray",
        showland=True,
        landcolor="rgb(240, 240, 240)"
    )
    fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})

    if save_path:
        fig.write_html(save_path)
    return fig