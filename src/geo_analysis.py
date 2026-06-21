import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def perform_kmeans_clustering(df, n_clusters=5, use_opportunity=False):
    """
    Cluster locations based on latitude, longitude and optionally opportunity score.
    Returns df with cluster labels.
    """
    if use_opportunity:
        features = df[['latitude', 'longitude', 'opportunity_score']]
    else:
        features = df[['latitude', 'longitude']]
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['region_cluster'] = kmeans.fit_predict(scaled)
    return df, kmeans

def find_expansion_candidates(df, top_n=10):
    """Identify top expansion spots: high demand, low presence."""
    # "high demand low presence" = high sales, high population, low competitor_count
    # Use opportunity score as proxy
    candidates = df.sort_values('opportunity_score', ascending=False).head(top_n)
    return candidates[['store_id', 'latitude', 'longitude', 'sales', 
                       'competitor_count', 'population', 'opportunity_score', 'expansion_tier']]

def summarize_clusters(df):
    """Aggregate cluster profiles."""
    summary = df.groupby('region_cluster').agg({
        'sales': 'mean',
        'competitor_count': 'mean',
        'population': 'mean',
        'opportunity_score': 'mean',
        'latitude': 'mean',
        'longitude': 'mean'
    }).round(2)
    return summary