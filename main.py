import argparse
import os
from src.data_loader import prepare_full_data
from src.geo_analysis import perform_kmeans_clustering, find_expansion_candidates, summarize_clusters
from src.visualization import create_sales_heatmap, create_existing_stores_map, create_opportunity_tier_map_plotly

def run_pipeline(generate=False):
    if generate:
        print("Generating sample data...")
        os.system("python data/generate_sample_geo_data.py")
    
    print("Loading and processing data...")
    df = prepare_full_data("data/sample_geo_data.csv")
    
    print("Applying KMeans clustering...")
    df, kmeans = perform_kmeans_clustering(df, n_clusters=5)
    
    print("\n--- Cluster Summary ---")
    print(summarize_clusters(df))
    
    print("\n--- Top 10 Expansion Candidates (High Demand, Low Presence) ---")
    candidates = find_expansion_candidates(df, top_n=10)
    print(candidates.to_string(index=False))
    
    # Output three visual maps as HTML files
    os.makedirs("outputs", exist_ok=True)
    print("\nGenerating visual maps...")
    
    heatmap = create_sales_heatmap(df, save_path="outputs/sales_heatmap.html")
    print("  ✓ sales_heatmap.html")
    
    store_map = create_existing_stores_map(df, save_path="outputs/existing_stores_map.html")
    print("  ✓ existing_stores_map.html")
    
    tier_map = create_opportunity_tier_map_plotly(df, save_path="outputs/opportunity_tiers_map.html")
    print("  ✓ opportunity_tiers_map.html")
    
    print("\n✅ Pipeline finished. Open the HTML files in 'outputs/' or run 'streamlit run app.py' for interactive dashboard.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Geospatial Business Expansion Pipeline")
    parser.add_argument("--generate", action="store_true", help="Generate fresh sample data before analysis")
    args = parser.parse_args()
    run_pipeline(generate=args.generate)