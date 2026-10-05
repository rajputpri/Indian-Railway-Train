# Indian Railway Trains — ML Classification & Clustering

**Course:** Gujarat University BCA Sem-VII (NEP 2020)
**Papers:** DSC-C-BCA-471T, 472T, 473P
**Project:** Classification and Clustering of Indian Railway Trains Using Machine Learning

---

## Project Overview

Ye project Indian Railways ke 5,208 trains ke data pe ML classification aur clustering karta hai. Hum trains ko 3 categories mein classify karte hain (Passenger / Express / Superfast) aur K-Means se route-based segments discover karte hain.

## Dataset

- **Source:** Kaggle — [Indian Railways Dataset](https://www.kaggle.com/datasets/sripaadsrinivasan/indian-railways-dataset)
- **File:** `trains.json` (GeoJSON FeatureCollection)
- **Size:** 5,208 trains, 21 raw properties
- **After cleaning:** 4,466 trains, 3 classes

## Quick Start

```bash
# Clone or download this project
cd Indian-Railway-Train

# Install dependencies
pip install -r requirements.txt

# Open notebook
code notebooks/main_notebook.ipynb