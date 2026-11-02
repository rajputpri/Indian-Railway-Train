# 🚂 Indian Railway Trains — ML Classification & Clustering (RailDrishti)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13.6-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-VS_Code-F37626?style=for-the-badge&logo=Jupyter&logoColor=white)](https://code.visualstudio.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](https://opensource.org/licenses/MIT)

**An end-to-end, production-grade Machine Learning pipeline and premium interactive web application to classify and cluster Indian Railway trains.**

</div>

---

## 🌟 Why This Project Stands Out

This is not just a standard academic project. It is a **complete, deployable product** that demonstrates the entire data science lifecycle — from raw data wrangling and bug forensics to model deployment with a cinematic UI.

*   🏆 **91.50% Accuracy** achieved using a tuned Decision Tree Classifier.
*   🕵️‍♂️ **Data Forensics:** Discovered a critical bug in the raw dataset (`duration_m`) and mathematically proved that **Data Quality > Algorithm Choice**.
*   🚀 **RailDrishti Web App:** A premium, interactive Streamlit dashboard with parallax animations, live e-ticket generation, and intelligent advisory business logic.

---

## 🎥 The RailDrishti Web Application

The project features a fully functional **Streamlit** web app (`app.py`) that brings the ML model to life for real-world users.

*   **Interactive UI:** IRCTC-inspired dark theme with custom CSS, sliders, and manual input forms.
*   **Cinematic Animations:** Real-time parallax train animations based on the predicted train type.
*   **Smart Advisory Engine:** Doesn't just predict; it recommends. (e.g., *"This Express train has premium features and should be upgraded to Superfast."*)
*   **Live E-Ticket Generation:** Generates a simulated Indian Railways ticket with PNR, Barcode, and QR code using the model's prediction.

---

## 🧠 Machine Learning Pipeline

The project follows a rigorous four-phase data science lifecycle:

### 1. Exploratory Data Analysis (EDA)
*   Analyzed **5,208** raw GeoJSON records, filtered down to **4,466** valid samples (Pass, Exp, SF).
*   Conducted univariate and bivariate analysis across 10+ visualization types (Histograms, KDE, Pairplots, Correlation Heatmaps).
*   Handled moderate class imbalance (55.06% Passenger, 16.10% Superfast) by adopting **Macro F1-Score** as the primary metric.

### 2. 🔥 The "Killer" Data Quality Fix
During EDA, a critical schema bug was discovered: the `duration_m` column only stored the minute remainder (0-58), not the total duration.
*   **The Fix:** Engineered a new feature: `total_duration = (duration_h * 60) + duration_m`.
*   **The Impact:** This single data quality fix improved **every single supervised model** by up to **+7.39%** in Macro F1 Score.

### 3. Supervised Classification
Benchmarked 4 algorithms against a Dummy Baseline:

| Model | Accuracy | F1 (Macro) | F1 (Weighted) |
| :--- | :--- | :--- | :--- |
| Baseline (Dummy) | 0.5503 | 0.2367 | 0.3907 |
| KNN (k=5) | 0.8523 | 0.7886 | 0.8484 |
| **Decision Tree (Champion)** 🏆 | **0.9150** | **0.8896** | **0.9146** |
| SVM (RBF) | 0.8412 | 0.7651 | 0.8343 |
| Naive Bayes | 0.3702 | 0.3098 | 0.3636 |

*   **Best Model:** Decision Tree (Default) — Stable under 5-fold CV (F1: `0.8743 ± 0.0155`).
*   **Top Features:** `third_ac` (35.5%), `distance` (22.3%), `total_duration` (18.0%).

### 4. Unsupervised Clustering
Discovered latent operational archetypes without using labels:
*   **K-Means (k=5):** Silhouette Score `0.2024`. Revealed 5 distinct fleets (e.g., ER-Regional, Long-Distance AC Premium).
*   **DBSCAN:** Silhouette Score `0.2543`. Isolated 0.4% noise (anomalies) and found 4 natural density-based clusters.

---

## 🛠️ Tech Stack & Architecture

| Domain | Tools & Technologies |
| :--- | :--- |
| **Languages** | Python 3.13.6, HTML/CSS (for Streamlit UI) |
| **Data Manipulation** | Pandas, NumPy |
| **Machine Learning** | Scikit-Learn, Joblib (Model Persistence) |
| **Data Visualization** | Matplotlib, Seaborn, Plotly (Web App) |
| **Web Framework** | Streamlit, Streamlit Components |
| **Tools** | VS Code, Jupyter Notebooks, Git, GitHub |

---

## 📁 Repository Structure

```text
Indian-Railway-Train/
├── app.py                             # 🚀 Premium Streamlit Web Application
├── data/
│   ├── trains.json                    # Original raw dataset (GeoJSON)
│   ├── trains.csv                     # Cleaned & processed dataset
│   └── trains_with_clusters.csv       # K-Means/DBSCAN output data
├── notebooks/
│   └── main_notebook.ipynb            # Core ML pipeline (EDA, Training, Clustering)
├── extras/
│   └── advanced_ml.ipynb              # Cross-validation & model persistence
├── models/
│   ├── scaler.joblib                  # Fitted StandardScaler
│   └── dt_classifier.joblib           # Trained Decision Tree (Champion Model)
├── visualizations/                    # 15+ generated plots (ROC, Heatmaps, etc.)
├── reports/                           # Project assets, images, and prompt templates
├── requirements.txt                   # Project dependencies
├── LICENSE                            # MIT License
└── README.md                          # You are here