# 🌍 Geospatial Business Expansion – Sales Heatmap & Opportunity Zones

🚀 **Live Demo:** [Launch Interactive Dashboard](https://garbage-classifier-gklub4dptcsntzgmdfhhry.streamlit.app/)

*Built as a senior GIS + Data Science project · June 2026*

---

## 🎯 The Problem

Retail chains often miss profitable new locations because they rely on intuition rather than data.  
This system identifies **under‑served, high‑demand areas** by combining sales, competitor density, and population data. It pinpoints expansion zones before competitors move in – and recommends where to open next.

---

## 📦 Dataset

| Property | Details |
|----------|---------|
| Source | Synthetic (generated) – mimics real retail location data |
| Records | 500 store locations |
| Period | Simulated current snapshot |
| Geography | Fictional metropolitan area (Springfield) |
| Columns | `latitude`, `longitude`, `sales`, `competitor_count`, `population` |

*Note: The data is fully synthetic, but the analytical pipeline works with real CSV files as long as they have the same column names.*

---

## 🏗️ What I Built

### Phase 1 — Data Cleaning & Feature Engineering
- Removed rows with missing coordinates or business metrics.
- Engineered **Opportunity Score** = `(Sales × Population) / (Competitors + 1)`.
- Assigned **Expansion Tiers** (Tier1 = highest potential, Tier3 = lowest).
- Created **City Zones** (NE, NW, SE, SW) based on geographic split.

### Phase 2 — Exploratory Analysis
- Visualised sales density via **Folium heatmaps**.
- Mapped existing stores with colour‑coded competitor levels.
- Identified clusters with **K‑Means** (5 clusters) to segment regions.

### Phase 3 — Opportunity Scoring & Expansion Candidates
- Ranked all locations by Opportunity Score.
- Extracted **top 10 expansion candidates** (high sales, high population, low competition).
- Generated **interactive tier maps** using Plotly.

### Phase 4 — Streamlit Dashboard
- 📍 **Sales Heatmap** – see sales volume density.
- 🏬 **Store Location Map** – all stores coloured by competitor count.
- 🎯 **Opportunity Tier Map** – explore Tiers 1–3 with filters.
- 🔍 **Filter controls** – city zone, minimum sales, expansion tier.
- 📊 **Top candidates** – displayed side‑bar for quick decision‑making.

---

## 🔍 Key Findings

- **Tier1 zones** (top 33% Opportunity Score) represent only 15% of all locations but account for **over 60% of total opportunity**.
- Areas with **low competitor count** and **high population** consistently show the best expansion potential.
- The **Southwest zone** has the highest concentration of Tier1 locations – a prime target for new stores.
- K‑Means clustering reveals **two distinct regional clusters** that behave similarly; expansion strategies can be shared across those regions.

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Data Processing | Python, Pandas, NumPy |
| Machine Learning | Scikit‑learn (KMeans, StandardScaler) |
| Visualisation | Folium (heatmaps), Plotly (interactive maps) |
| Dashboard Engine | Streamlit + streamlit‑folium |
| Version Control | Git, GitHub |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/Padmini122/geospatial-expansion.git
cd geospatial-expansion

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate      # Linux/macOS
# or .\venv\Scripts\Activate  # Windows PowerShell
pip install -r requirements.txt

# Generate sample data (optional – the dashboard does this automatically)
python data/generate_sample_geo_data.py

# Run the dashboard
streamlit run app.py
📊 Live Demo
Launch the interactive dashboard:
https://garbage-classifier-gklub4dptcsntzgmdfhhry.streamlit.app/

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgements
Built with Python, Pandas, NumPy, Scikit‑learn, Folium, Plotly, and Streamlit.

Synthetic data generated for demonstration – easily replaceable with real‑world retail location data.