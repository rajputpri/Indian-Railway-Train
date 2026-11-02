# CLASSIFICATION AND CLUSTERING OF INDIAN RAILWAY TRAINS USING MACHINE LEARNING

**Submitted in partial fulfilment of the requirements for the award of the degree of**  
**Bachelor of Computer Applications (Honours)**  
**Courses:** DSC-C-BCA-471T (Artificial Intelligence), DSC-C-BCA-472T (Machine Learning), and DSC-C-BCA-473P (ML System Design)  
**Academic Year:** 2025-26

---

- **Presented By:** Rajput Prince Singh (Roll No. 83) — BCA (Hons.) — Semester VII
- **Submitted To:** Lokmanya College of Computer Applications, Ahmedabad, Gujarat (Affiliated to Gujarat University)
- **Under the Guidance Of:** Prof. Sejal Shah, Assistant Professor, Lokmanya College of Computer Applications
- **Director:** Dr. Prakash Khuman, Director, Lokmanya College of Computer Applications
- **GitHub Repository:** https://github.com/rajputpri/Indian-Railway-Train (branch: `master`)

---

## TABLE OF CONTENTS

| Section | Title | Page |
|:-------:|:------|:----:|
| 1 | College Certificate | 3 |
| 2 | Acknowledgement | 4 |
| 3 | Project Definition | 5 |
| 4 | Project Exploration (EDA) | 8 |
| 5 | Evaluation Matrix | 14 |
| 6 | Model Building | 18 |
| 7 | Advanced Techniques — Pattern Discovery | 25 |
| 8 | Interpretation of Results & Insights | 29 |
| 9 | Limitations | 32 |
| 10 | Future Enhancements | 33 |
| 11 | Bibliography | 34 |
| 12 | Appendix | 35 |

---

## 1. COLLEGE CERTIFICATE

This is to certify that the project report entitled **"CLASSIFICATION AND CLUSTERING OF INDIAN RAILWAY TRAINS USING MACHINE LEARNING"** is a bonafide record of the work carried out by **Rajput Prince Singh (Roll No. 83)** and submitted to **Gujarat University** in partial fulfilment of the requirements for the award of the degree of **Bachelor of Computer Applications (Honours)** for the courses **DSC-C-BCA-471T (Artificial Intelligence), DSC-C-BCA-472T (Machine Learning), and DSC-C-BCA-473P (ML System Design)** during the academic year **2025-26**.

To the best of our knowledge, this work is original, was carried out at **Lokmanya College of Computer Applications, Ahmedabad, Gujarat**, under the guidance of **Prof. Sejal Shah**, and has not been submitted in part or in full to any other university or institution for the award of any degree or diploma.

- **Project Guide:** Prof. Sejal Shah, Assistant Professor, Lokmanya College of Computer Applications
- **Director:** Dr. Prakash Khuman, Director, Lokmanya College of Computer Applications
- **External Examiner:** Gujarat University

---

## 2. ACKNOWLEDGEMENT

Completing this project has been an invaluable learning experience, and I am grateful to everyone who contributed to it.

First, I thank the management of **Lokmanya College of Computer Applications, Ahmedabad, Gujarat**, for providing excellent laboratory facilities, library resources, and a supportive learning environment throughout my BCA journey.

I express my sincere gratitude to **Dr. Prakash Khuman, Director, Lokmanya College of Computer Applications**, for his constant encouragement and for making all necessary facilities available for this project.

I am deeply thankful to my project guide, **Prof. Sejal Shah, Assistant Professor**, for her valuable guidance at every stage of this work. Her suggestions helped me select the right approach for data exploration, model building, and result interpretation.

I am also grateful to **Gujarat University** for including Machine Learning, Artificial Intelligence, and ML System Design in the BCA (Honours) curriculum under NEP 2020.

Finally, I thank my family and friends for their unwavering support, patience, and motivation throughout this project.

**Rajput Prince Singh** (Roll No. 83)  
BCA (Hons.) — Semester VII — Lokmanya College of Computer Applications

---

## 3. PROJECT DEFINITION

### 3.1 Introduction
Indian Railways is the fourth-largest railway network in the world, spanning over **68,000 route kilometres**, operating more than **13,000 passenger trains daily** across **19+ administrative zones** and **7,300+ stations**. Manual categorisation of trains into service tiers — **Passenger (`Pass`)**, **Express (`Exp`)**, and **Superfast (`SF`)** — is labour-intensive and inconsistent across zones. This project demonstrates that machine learning can automate this multi-class classification with **91.50% accuracy** while discovering latent operational groupings via unsupervised clustering.

### 3.2 Problem Statement
1. Build an accurate **multi-class classifier** predicting a train's service tier (`Pass`, `Exp`, `SF`) from 26 operational metrics.
2. Apply **unsupervised clustering** (K-Means and DBSCAN) to uncover natural operational groupings and isolate schedule anomalies.
3. Diagnose and remediate the corrupted `duration_m` feature via compound duration engineering.

---

## 4. PROJECT EXPLORATION (EDA)

### 4.1 Dataset Overview

| Field | Verified Specification |
|:------|:-----------------------|
| **Name** | Indian Railways Dataset (`sripaadsrinivasan/indian-railways-dataset`) |
| **Original File** | `trains.json` (GeoJSON, 14.08 MB) |
| **Converted File** | `trains.csv` (636 KB) |
| **Raw / Filtered Records** | 5,208 raw records / 4,466 filtered records (3 classes) |
| **Features (after One-Hot)** | 26 |

### 4.2 Target Class Distribution

| Class Code | Category | Count | Share (%) | Operational Profile |
|:----------:|:---------|------:|----------:|:--------------------|
| `Pass` | Passenger | 2,459 | 55.06% | Short-distance commuter routes, frequent halts, unreserved |
| `Exp` | Express | 1,288 | 28.84% | Medium-to-long distance intercity routes, mixed Sleeper & AC |
| `SF` | Superfast | 719 | 16.10% | High priority, fewer halts, high commercial speed, full AC |

### 4.3 Correlation Analysis
- `distance` ↔ `total_duration`: **0.98**
- `third_ac` ↔ `sleeper`: **0.86**
- `second_ac` ↔ `sleeper`: **0.79**
- `distance` ↔ `sleeper`: **0.70**
- `distance` ↔ `third_ac`: **0.69**
- `first_ac` ↔ `second_ac`: **0.39**

### 4.4 Data Quality Fix — The Killer Finding
The `duration_m` column stored only the minute remainder (`0–58`) rather than total journey duration in minutes. Engineering `total_duration = (duration_h * 60) + duration_m` resolved the corruption and improved every single model:

| Model / Metric | Before Fix | After Fix | Delta Gain |
|:---------------|:----------:|:---------:|:----------:|
| KNN (k=5) F1 Macro | 0.7552 | 0.7886 | +0.0334 |
| Decision Tree (Default) F1 Macro | 0.8309 | 0.8896 | +0.0587 |
| Decision Tree (depth=10) F1 Macro | 0.7720 | 0.8459 | +0.0739 |
| Gaussian Naive Bayes F1 Macro | 0.2969 | 0.3098 | +0.0129 |
| SVM (RBF) F1 Macro | 0.7168 | 0.7651 | +0.0483 |
| K-Means (k=5) Silhouette | 0.1755 | 0.2024 | +0.0269 |

---

## 5. EVALUATION MATRIX

- **Stratified Train-Test Split:** 80% Training (`3,572` records) / 20% Testing (`894` records) with `random_state=42`.
- **Leakage Prevention:** `StandardScaler` fitted strictly on `X_train` (`3,572` rows) before transforming `X_test` (`894` rows).
- **Primary Metric:** Macro-Averaged F1 (treats all 3 classes equally under moderate class imbalance).

---

## 6. MODEL BUILDING & RESULTS

### 6.1 Supervised Classification Benchmark

| Model | Accuracy | F1 (Macro) | F1 (Weighted) | Verdict |
|:------|:--------:|:----------:|:-------------:|:--------|
| Baseline (Dummy) | 0.5503 | 0.2367 | 0.3907 | Benchmark Floor |
| KNN (k=5) | 0.8523 | 0.7886 | 0.8484 | Strong |
| **Decision Tree (default)** | **0.9150** | **0.8896** | **0.9146** | **WINNER** |
| Decision Tree (depth=10) | 0.8859 | 0.8459 | 0.8836 | Runner-Up |
| Gaussian Naive Bayes | 0.3702 | 0.3098 | 0.3636 | Poor Fit |
| SVM (RBF) | 0.8412 | 0.7651 | 0.8343 | Strong |

- **Micro-Averaged Precision / Recall (Decision Tree):** `0.9150`
- **5-Fold Stratified Cross-Validation (Decision Tree):** `0.8743 +/- 0.0155` Macro F1
- **One-vs-Rest Mean ROC-AUC:** KNN `0.9355` (best), SVM `0.9285`, Decision Tree `0.9204`
- **Top 5 Decision Tree Features:** `third_ac` (`0.355124`), `distance` (`0.222583`), `total_duration` (`0.179872`), `chair_car` (`0.118112`), `first_ac` (`0.013265`)
- **Error Analysis:** Overall error rate `8.50%` (Per-class error rates: `Pass` `3.0%`, `Exp` `14.0%`, `SF` `17.4%`; dominant confusion: `25` SF→Exp, `16` Exp→SF).

---

## 7. ADVANCED TECHNIQUES — PATTERN DISCOVERY

- **K-Means (`k = 5`):** Inertia `69,115.75`, Silhouette `0.2024`. Discovered 5 clusters: `C-0` ER-Regional Network, `C-1` NFR-Mixed Operations, `C-2` Short-Distance Commuter Pass, `C-3` Long-Distance AC Premium Fleet, and `C-4` Secondary-Zone Short Passenger.
- **DBSCAN (`eps = 7.0, min_samples = 20`):** Discovered `4` natural clusters with `0.4%` noise (`13` outlier points) and Silhouette `0.2543` (outperforming K-Means).
- **Output Artifact:** Saved to `data/trains_with_clusters.csv` (`3,572` rows × `28` columns).

---

## 8. INTERPRETATION OF RESULTS, LIMITATIONS & FUTURE WORK

1. **Data Quality > Algorithm Choice:** Fixing `total_duration` improved all 5 classifiers and clustering cohesion.
2. **Rule-Based Alignment:** Decision Tree excels because railway classification follows hierarchical coach and distance thresholds.
3. **Future Scope:** Ensemble methods (Random Forest / XGBoost), live NTES halt/speed telemetry, and FastAPI deployment of `models/dt_classifier.joblib`.

---

## 9. BIBLIOGRAPHY

1. Saikat Dutt, Subramanian Chandramouli, Amit Kumar Das — *Machine Learning*, Pearson Education.
2. Andreas C. Muller & Sarah Guido — *Introduction to Machine Learning with Python*, O'Reilly Media.
3. Aurelien Geron — *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*, O'Reilly Media.
4. Tom M. Mitchell — *Machine Learning*, McGraw Hill Education.
5. Sripaad Srinivasan — *Indian Railways Dataset*, Kaggle.
6. scikit-learn Documentation — https://scikit-learn.org/stable/
7. pandas Documentation — https://pandas.pydata.org/docs/
8. Matplotlib Documentation — https://matplotlib.org/stable/
