import pandas as pd
import numpy as np

def load_data(filepath):
    """Load CSV and basic cleaning."""
    df = pd.read_csv(filepath)
    # drop any rows with missing critical columns
    df = df.dropna(subset=['latitude', 'longitude', 'sales', 'competitor_count', 'population'])
    return df

def assign_zones(df, lat_col='latitude', lon_col='longitude'):
    """Split area into zones based on lat/lon quantiles."""
    lat_median = df[lat_col].median()
    lon_median = df[lon_col].median()
    
    conditions = [
        (df[lat_col] >= lat_median) & (df[lon_col] >= lon_median),
        (df[lat_col] >= lat_median) & (df[lon_col] < lon_median),
        (df[lat_col] < lat_median) & (df[lon_col] >= lon_median),
        (df[lat_col] < lat_median) & (df[lon_col] < lon_median)
    ]
    choices = ['Northeast', 'Northwest', 'Southeast', 'Southwest']
    df['zone'] = np.select(conditions, choices, default='Central')
    return df

def compute_opportunity_score(df, sales_col='sales', pop_col='population', comp_col='competitor_count'):
    """
    Opportunity score = (sales * population) / (competitors + 1)
    Higher = high demand, low competition.
    """
    df['opportunity_score'] = (df[sales_col] * df[pop_col]) / (df[comp_col] + 1)
    return df

def assign_tiers(df, score_col='opportunity_score'):
    """Tier 1 (high), Tier 2 (medium), Tier 3 (low) based on quantiles."""
    q33 = df[score_col].quantile(0.33)
    q66 = df[score_col].quantile(0.66)
    conditions = [
        df[score_col] >= q66,
        (df[score_col] >= q33) & (df[score_col] < q66),
        df[score_col] < q33
    ]
    choices = ['Tier1_High', 'Tier2_Medium', 'Tier3_Low']
    df['expansion_tier'] = np.select(conditions, choices, default='Unknown')
    return df

def prepare_full_data(filepath):
    """Complete pipeline: load → zone → opportunity → tier."""
    df = load_data(filepath)
    df = assign_zones(df)
    df = compute_opportunity_score(df)
    df = assign_tiers(df)
    return df