# Indian Railway Trains — ML Classification & Clustering

[![Python](https://img.shields.io/badge/Python-3.13.6-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Notebook-VS%20Code-yellow.svg)](https://code.visualstudio.com/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](#license)

**A machine learning project applying supervised classification and unsupervised clustering techniques to Indian Railway trains.**

---

## 📋 Project Overview

This project demonstrates an end-to-end machine learning pipeline applied to the Indian Railways dataset. It classifies trains into three service categories — **Passenger (Pass)**, **Express (Exp)**, and **Superfast (SF)** — and discovers natural operational segments through unsupervised clustering.

The project follows a **four-phase structure** aligned with Gujarat University's BCA Sem-VII curriculum under NEP 2020:

| Phase | Topic | Deliverable |
|-------|-------|-------------|
| Phase 1 | Exploratory Data Analysis & Problem Definition | Distribution analysis, correlation study, class balance |
| Phase 2 | Evaluation Metrics | Confusion matrix, precision/recall, ROC-AUC, macro & micro F1 |
| Phase 3 | Supervised Model Building | KNN, Decision Tree, Naive Bayes, SVM |
| Phase 4 | Unsupervised Clustering | K-Means (k=5), DBSCAN, PCA visualization |

---

## 🎓 Academic Context

- **Course:** Bachelor of Computer Applications (BCA) — Semester VII
- **University:** Gujarat University (NEP 2020)
- **Papers Covered:**
  - DSC-C-BCA-471T — Artificial Intelligence
  - DSC-C-BCA-472T — Machine Learning
  - DSC-C-BCA-473P — Machine Learning System Design
- **Project Type:** Project-Based Learning (100 marks across 4 phases + report + PPT + viva)

---

## 📊 Key Results

### Supervised Classification (Best Models)

| Model | Accuracy | F1 (macro) | F1 (weighted) |
|-------|----------|------------|---------------|
| Baseline (Dummy) | 0.5503 | 0.2367 | 0.3907 |
| KNN (k=5) | 0.8523 | 0.7886 | 0.8484 |
| **Decision Tree (default)** 🏆 | **0.9150** | **0.8896** | **0.9146** |
| Decision Tree (depth=10) | 0.8859 | 0.8459 | 0.8836 |
| Naive Bayes | 0.3702 | 0.3098 | 0.3636 |
| SVM (RBF) | 0.8412 | 0.7651 | 0.8343 |

**Best Model:** Decision Tree (default configuration) — **91.50% accuracy**, **0.8896 macro F1**

**Cross-Validation:** 5-fold CV mean F1 = **0.8743 ± 0.0155** (stable, reproducible)

**ROC-AUC (One-vs-Rest):**
- Decision Tree — 0.9204
- KNN — 0.9355
- SVM — 0.9285

### Unsupervised Clustering

| Algorithm | Clusters | Noise | Silhouette Score |
|-----------|----------|-------|-------------------|
| K-Means (k=5) | 5 | 0.0% | 0.2024 |
| DBSCAN (eps=7.0, min_samples=20) | 4 | 0.4% | 0.2543 |

**K-Means cluster interpretation:**
1. ER-zone regional trains
2. NFR-zone mixed operations
3. Short-distance passenger (58.3% of trains)
4. Long-distance premium AC
5. Unknown-zone short passenger

### Top Predictive Features (Decision Tree)

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | `third_ac` | 0.35 |
| 2 | `distance` | 0.22 |
| 3 | `total_duration` | 0.17 |
| 4 | `chair_car` | 0.12 |

---

## 🔬 Key Finding — Data Quality > Algorithm

A critical data quality issue was identified during extended EDA:

> **Issue:** The `duration_m` column stored only the minute-component of travel time (range 0–58), not total minutes.
>
> **Correction:** Derived a compound feature — `total_duration = (duration_h × 60) + duration_m`

**Impact — All models improved after correction:**

| Model | F1 Before | F1 After | Δ Improvement |
|-------|-----------|----------|---------------|
| KNN | 0.7552 | 0.7886 | +0.0334 |
| DT (default) | 0.8309 | 0.8896 | **+0.0587** |
| DT (depth=10) | 0.7720 | 0.8459 | +0.0739 |
| Naive Bayes | 0.2969 | 0.3098 | +0.0129 |
| SVM | 0.7168 | 0.7651 | +0.0483 |
| Silhouette | 0.1755 | 0.2024 | +0.0269 |

**Takeaway:** Data quality improvements often outweigh algorithm selection — a fundamental principle in applied machine learning.

## 📁 Project Structure

---
```
Indian-Railway-Train/
├── data/
│   ├── trains.json                    # Original dataset (GeoJSON, 14 MB)
│   ├── trains.csv                     # Converted CSV (636 KB, used by notebooks)
│   └── trains_with_clusters.csv       # Output: clustering labels + features
├── notebooks/
│   └── main_notebook.ipynb            # Main notebook — all 4 phases
├── extras/
│   ├── advanced_ml.ipynb              # Model persistence, CV, error analysis
│   └── README.md                      # Extras module documentation
├── models/
│   ├── scaler.joblib                  # Fitted StandardScaler
│   └── dt_classifier.joblib           # Trained Decision Tree model
├── visualizations/                    # 14+ saved plots
│   ├── model_comparison.png
│   ├── confusion_matrix.png
│   ├── roc_curves.png
│   ├── feature_importance.png
│   ├── cross_validation.png
│   ├── elbow_curve.png
│   ├── clusters_k5_pca.png
│   ├── dbscan_vs_kmeans.png
│   ├── error_analysis.png
│   └── ... (more)
├── reports/                           # Final report (pending)
├── requirements.txt                   # Python dependencies
├── .gitignore
├── MASTER_OPERATING_PROMPT.md         # Project continuity prompt
└── README.md
```


