# ============================================================
# generate_viva_bank.py  (FIXED for fpdf2 2.8.x)
# Hinglish Viva Question Bank - Indian Railway Trains ML Project
# Run: python reports\generate_viva_bank.py
# ============================================================

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUT_FILE = Path(__file__).parent / "Viva_Question_Bank.pdf"

# ------------------------- COLORS ----------------------------
NAVY    = (10, 31, 68)
DARK    = (30, 30, 30)
GREY    = (95, 95, 95)
LIGHT   = (240, 244, 250)
RED     = (200, 30, 30)
ORANGE  = (210, 105, 0)
BLUE    = (30, 90, 180)
GREEN   = (25, 135, 60)
PURPLE  = (130, 60, 170)
SOFT    = (70, 100, 130)

DIFF_COLORS = {
    "MOST IMP":  RED,
    "IMPORTANT": ORANGE,
    "MEDIUM":    BLUE,
    "EASY":      GREEN,
    "HARD":      PURPLE,
}


def clean(t: str) -> str:
    """ASCII-safe fallback for default Helvetica."""
    repl = {
        "\u2192": "->", "\u2190": "<-", "\u2194": "<->",
        "\u2265": ">=", "\u2264": "<=", "\u2013": "-", "\u2014": "-",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00d7": "x", "\u00b1": "+/-", "\u00b7": ".",
        "\u2022": "-",
    }
    for k, v in repl.items():
        t = t.replace(k, v)
    return t


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GREY)
        self.set_x(self.l_margin)
        self.cell(0, 6, "Viva Question Bank  |  Indian Railway Trains ML Project",
                  align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 6, f"Page {self.page_no()}", align="R",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

    def footer(self):
        pass


# ---------- low-level text helpers (all reset X safely) ----------

def _set_font(pdf, size=11, bold=False, italic=False, color=DARK):
    style = ""
    if bold:
        style += "B"
    if italic:
        style += "I"
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(*color)


def MC(pdf, txt, size=11, bold=False, italic=False, color=DARK,
       align="L", h=6, fill=False, indent=0):
    _set_font(pdf, size, bold, italic, color)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(0, h, clean(txt), align=align, fill=fill,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def H1(pdf, t):
    pdf.ln(3)
    MC(pdf, t, size=20, bold=True, color=NAVY, h=10)
    pdf.ln(1)


def H2(pdf, t):
    pdf.ln(2)
    MC(pdf, t, size=14, bold=True, color=NAVY, h=8)


def H3(pdf, t):
    pdf.ln(1)
    MC(pdf, t, size=12, bold=True, color=(60, 60, 60), h=7)


def P(pdf, t, size=11):
    MC(pdf, t, size=size, h=6)


def B(pdf, t, size=11):
    MC(pdf, "- " + t, size=size, h=6, indent=4)


def MONO(pdf, t):
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.set_fill_color(*LIGHT)
    for line in t.split("\n"):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5, clean(line), fill=True,
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def Q(pdf, num, diff, question):
    color = DIFF_COLORS.get(diff, GREY)
    pdf.ln(3)
    MC(pdf, f"Q{num}. {question}", size=12, bold=True, color=NAVY, h=7)
    MC(pdf, f"[{diff}]", size=9, bold=True, color=color, h=5)


def A(pdf, text):
    MC(pdf, "Ans: " + text, size=10.5, h=6)


def EX(pdf, text):
    MC(pdf, "Example (hamare project se): " + text, size=10, italic=True,
       color=SOFT, h=6)


def KEY(pdf, text):
    MC(pdf, "Keywords: " + text, size=9.5, italic=True, color=GREY, h=5)


# ============================================================
#  SECTION A - PROJECT DEEP DIVE
# ============================================================

def build_section_a(pdf):
    pdf.add_page()
    H1(pdf, "SECTION A - PROJECT DEEP DIVE")
    P(pdf, "Viva se pehle poora project ek baar sar se paanv tak samajh le. "
           "Ye section sabse pehle padh - iske baad Q&A apne aap fit baithega. "
           "Hinglish mein likha hai, examples project se hi diye hain.")

    H2(pdf, "A1. Project ek line mein")
    P(pdf, "Indian Railways ke trains ka data le kar Machine Learning se do kaam kiye: "
           "(1) classify - naye train ko 3 classes (Pass / Exp / SF) mein daalna, "
           "(2) cluster - bina label ke trains ko similar groups mein baantna.")

    H2(pdf, "A2. Project kya solve karta hai?")
    B(pdf, "Railway board ko naye train ka type decide karna hota hai. Hum predict kar sakte hain "
           "ki naya train Pass hoga, Exp hoga ya SF.")
    B(pdf, "Operations team similar trains ko group kar sakti hai - schedule optimize karne ke liye.")
    B(pdf, "Passengers ko rough idea milta hai ki kaunse route pe kaisi service hai.")

    H2(pdf, "A3. Data ki kahani")
    B(pdf, "Source: Kaggle - sripaadsrinivasan/indian-railways-dataset")
    B(pdf, "Original: trains.json (GeoJSON, 14 MB)")
    B(pdf, "Converted: trains.csv (636 KB) - notebook CSV-first padhta hai")
    B(pdf, "Raw records: 5,208 -> Filtered: 4,466 (sirf 3 classes)")
    B(pdf, "One-hot ke baad 26 features")
    B(pdf, "Train/Test: 80/20 stratified -> 3,572 train / 894 test")

    H2(pdf, "A4. Folder structure - kaha kya rakha hai")
    MONO(pdf, """
Indian-Railway-Train/
|-- data/
|   |-- trains.json                 <- original raw
|   |-- trains.csv                  <- converted (notebook isko padhta hai)
|   `-- trains_with_clusters.csv    <- clustering output (labels + features)
|
|-- notebooks/
|   `-- main_notebook.ipynb         <- MAIN file, 4 phases isi mein
|
|-- extras/
|   |-- advanced_ml.ipynb           <- CV, feature importance, error analysis
|   `-- README.md
|
|-- models/
|   |-- scaler.joblib               <- fitted StandardScaler
|   `-- dt_classifier.joblib        <- trained Decision Tree
|
|-- visualizations/                 <- 20+ PNG plots
|
|-- reports/
|   |-- images/                     <- AI-generated hero images
|   |-- generate_ppt.py
|   |-- generate_viva_bank.py       <- ye script
|   |-- Viva_Question_Bank.pdf      <- OUTPUT
|   `-- final_report.md
|
|-- .gitignore
|-- MASTER_OPERATING_PROMPT.md
|-- requirements.txt
`-- README.md
    """.strip("\n"))

    H2(pdf, "A5. Notebook - kaunsa cell kya karta hai")

    H3(pdf, "Phase 1 - EDA (Exploratory Data Analysis)")
    B(pdf, "Cell 1-3: Imports + CSV-first load. Agar CSV nahi mila toh JSON fallback.")
    B(pdf, "Cell 4-6: head, shape, dtypes, nulls, describe - basic sanity check.")
    B(pdf, "Cell 7-9: class count plot, zone distribution bar, histograms.")
    B(pdf, "Cell 10-12: bivariate scatter, boxplots, correlation heatmap, pairplot.")
    B(pdf, "Constant-column audit: har row mein same value wale columns drop.")

    H3(pdf, "Phase 2 - Preprocessing + Evaluation")
    B(pdf, "Duration fix cell: total_duration = duration_h * 60 + duration_m  (killer fix).")
    B(pdf, "One-hot encoding: train_type, zones, etc. 0/1 columns mein.")
    B(pdf, "name aur number drop - identifier hain, ML mein kaam ke nahi.")
    B(pdf, "train_test_split(stratify=y) - pehle split, phir scale (leakage nahi).")
    B(pdf, "Metrics: accuracy, precision, recall, F1 (macro + weighted + micro), CM, ROC-AUC.")

    H3(pdf, "Phase 3 - Supervised models")
    B(pdf, "Cell 30-FIX: Decision Tree - acc 0.9150, macro F1 0.8896  <- WINNER")
    B(pdf, "KNN (k=5), SVM (RBF), Naive Bayes - comparison ke liye.")
    B(pdf, "DummyClassifier baseline - 0.5503 accuracy (sirf 'Pass' bolke).")
    B(pdf, "Model comparison leaderboard + feature importance plot.")

    H3(pdf, "Phase 4 - Clustering")
    B(pdf, "Cell 31-FIX: K-Means k=5 - inertia 69,115.75, silhouette 0.2024.")
    B(pdf, "Elbow curve se k=5 chuna.")
    B(pdf, "PCA 2D - 26 features ko 2D mein project kiya.")
    B(pdf, "DBSCAN (eps=7, min_samples=20) - 4 clusters, silhouette 0.2543, 0.4% noise.")
    B(pdf, "trains_with_clusters.csv - 3,572 rows, 28 columns.")

    H3(pdf, "Extras notebook (advanced_ml.ipynb)")
    B(pdf, "Mini rebuild cell - poora pipeline chhote version mein.")
    B(pdf, "5-fold CV F1 macro 0.8743 +/- 0.0155.")
    B(pdf, "Feature importance - third_ac top pe (0.355).")
    B(pdf, "Error analysis chart.")
    B(pdf, "Models persisted - scaler.joblib, dt_classifier.joblib.")

    H2(pdf, "A6. Visualizations folder - har PNG kya dikhati hai")
    B(pdf, "eda_histograms.png        - distance, duration ka distribution.")
    B(pdf, "eda_class_zone_distribution.png - kaunsa zone mein kitne trains, kaunsi class.")
    B(pdf, "bivariate_scatter.png     - distance vs duration scatter.")
    B(pdf, "boxplots.png              - har class ke feature ka spread (outliers).")
    B(pdf, "correlation_heatmap.png   - features ke beech correlation.")
    B(pdf, "pairplot.png              - har pair ka scatter, class colours.")
    B(pdf, "line_plot_trends.png      - duration vs distance trend.")
    B(pdf, "density_plots.png         - KDE curves.")
    B(pdf, "histograms_logscale.png   - skew features ka log-scale view.")
    B(pdf, "before_after_duration_fix.png - killer slide, fix se pehle vs baad.")
    B(pdf, "confusion_matrix_best.png - DT ka confusion matrix.")
    B(pdf, "roc_curves.png            - 3 classes ke ROC + AUC.")
    B(pdf, "model_comparison.png      - 5 models ka bar chart.")
    B(pdf, "feature_importance.png    - DT ki top features.")
    B(pdf, "cross_validation.png      - 5 folds ka F1.")
    B(pdf, "error_analysis.png        - kaha model galat hua.")
    B(pdf, "elbow_curve.png           - k vs inertia, k=5 pe kink.")
    B(pdf, "clusters_pca.png          - K-Means ka 2D PCA.")
    B(pdf, "clusters_k5_fixed_pca.png - duration fix ke baad K-Means PCA.")
    B(pdf, "dbscan_vs_kmeans.png      - dono ka side-by-side.")

    H2(pdf, "A7. Models folder - kya saved hai")
    B(pdf, "scaler.joblib - fitted StandardScaler. Naye data pe same scaling apply karne ke liye.")
    B(pdf, "dt_classifier.joblib - trained Decision Tree. Load karo, predict karo.")

    H2(pdf, "A8. Poora pipeline ek line mein")
    P(pdf, "Raw JSON -> CSV -> 3 classes filter -> EDA -> duration fix -> one-hot -> "
           "80/20 split -> scale -> 5 models -> DT jeeta (91.5%) -> K-Means + DBSCAN -> "
           "clusters CSV save -> models persist.")


# ============================================================
#  SECTION B - VIVA Q&A
# ============================================================

QNA = [

    # ---------- PROJECT & DATA ----------
    dict(d="MOST IMP",
         q="Project ka title kya hai aur ye kya karta hai?",
         a="Title hai 'Classification and Clustering of Indian Railway Trains Using "
           "Machine Learning'. Isme Indian Railways ke trains ko do tarike se study "
           "karte hain: (1) Supervised Classification - naye train ko 3 classes mein "
           "daalna (Pass, Exp, SF), (2) Unsupervised Clustering - bina label ke "
           "similar trains ko groups mein baantna.",
         ex="Jaise school mein 3 sections A, B, C hote hain - waise hi humara model "
            "naye train ko dekh kar bata deta hai ki wo Pass hai, Exp hai ya SF.",
         k="Classification, Clustering, Supervised, Unsupervised, Pass/Exp/SF"),

    dict(d="IMPORTANT",
         q="Ye project kyu chuna? Real-world relevance kya hai?",
         a="Indian Railways duniya ka 4th largest network hai, data bahut rich hai. "
           "Railway board naye train ka type decide karta hai, operations team schedule "
           "optimize karti hai. Ye real, non-toy dataset hai - textbook wala iris flower "
           "nahi.",
         ex="Agar naya train Mumbai-Delhi chalana hai, uski speed, distance, stops dekh "
            "kar predict kar sakte hain ki Pass hoga, Exp hoga ya SF.",
         k="Real-world, non-toy dataset, operations, scheduling"),

    dict(d="MOST IMP",
         q="Dataset kaha se liya? Kitne rows? Kaunse columns?",
         a="Kaggle se - 'sripaadsrinivasan/indian-railways-dataset'. Original file "
           "trains.json (GeoJSON, 14 MB) thi. CSV mein convert ki - 5,208 raw records, "
           "3 classes pe filter kiya - 4,466 trains. One-hot ke baad 26 features. "
           "Important columns: train_type, distance, duration_h, duration_m, zones, "
           "third_ac, chair_car, first_ac, sleeper.",
         ex="Humne har zone ke trains cover kiye - ER, NFR, WR, SR etc.",
         k="Kaggle, GeoJSON, 5,208 raw, 4,466 filtered, 26 features"),

    dict(d="IMPORTANT",
         q="Teen classes kya hain? Distribution kya thi?",
         a="Pass (Passenger), Exp (Express), SF (Superfast). Distribution: Pass 2,459 "
           "(55.06%), Exp 1,288 (28.84%), SF 719 (16.10%). Moderate imbalance hai - "
           "Pass bahut zyada, SF kam.",
         ex="Kyunki Pass sabse zyada tha, humne macro F1 ko primary metric banaya, "
            "accuracy ko nahi - warna model sirf Pass predict karke 55% le aata.",
         k="Class distribution, imbalance, 55/29/16"),

    dict(d="IMPORTANT",
         q="Class imbalance tha? Handle kaise kiya?",
         a="Haan, moderate (55/29/16). Humne: (1) accuracy ki jagah macro F1 primary "
           "metric banaya - minority class (SF) bhi respect kare, (2) stratified split "
           "- train aur test dono mein same ratio, (3) confusion matrix se per-class "
           "error dekha.",
         ex="Baseline DummyClassifier ne 0.5503 accuracy di - sirf 'Pass' bolke. Lekin "
            "macro F1 sirf 0.2367. Isse pata chala accuracy dhoka de sakti hai.",
         k="Macro F1, stratified split, confusion matrix, minority class"),

    # ---------- PREPROCESSING ----------
    dict(d="MOST IMP",
         q="Data leakage kya hai? Aapne kaise roka?",
         a="Data leakage tab hota hai jab test data ki info training mein chali jaye. "
           "Model ratta maar leta hai aur real world mein fail. Humne roka: pehle "
           "train_test_split, phir StandardScaler ko sirf train pe FIT kiya, test pe "
           "sirf TRANSFORM. Agar pehle scale karte phir split, to test ke mean/std "
           "training mein leak ho jaate.",
         ex="Rule yaad rakho: 'fit' sirf train pe, 'transform' train aur test dono pe.",
         k="Data leakage, fit, transform, train_test_split order"),

    dict(d="IMPORTANT",
         q="name aur number columns drop kyu kiye?",
         a="Ye identifier hain - har train ka naam aur number unique hai. Model ke liye "
           "useless kyunki pattern nahi sikhate, sirf yaad karte hain. Zyada columns se "
           "overfitting bhi badhta hai.",
         ex="Jaise roll number se kisi student ki personality nahi pata chalti - waise "
            "hi train number se type predict nahi hota.",
         k="Identifier, overfitting, feature selection"),

    dict(d="MOST IMP",
         q="duration_m ka kya problem tha? Fix kaise kiya?",
         a="duration_m column sirf minute-component tha (0-58 range), total minutes "
           "nahi. Matlab agar train 5 ghante 30 min chalti hai, to duration_m mein 30 "
           "aata, 330 nahi. Isse model confuse ho raha tha. Fix: "
           "total_duration = duration_h * 60 + duration_m.",
         ex="Fix se pehle DT ka F1 0.8309 tha, fix ke baad 0.8896 - 0.0587 ka jump!",
         k="duration_m, total_duration, feature engineering, data quality"),

    dict(d="MOST IMP",
         q="Fix ka impact kya padha? (before vs after)",
         a="Sab 5 supervised models ka F1 badha, aur silhouette bhi. Ye project ka "
           "sabse bada finding hai: Data quality > Algorithm choice. KNN +0.0334, "
           "DT +0.0587, DT(depth=10) +0.0739, Naive Bayes +0.0129, SVM +0.0483, "
           "Silhouette +0.0269.",
         ex="Koi bhi algorithm badalne se itna consistent jump nahi aata. Data fix "
            "karna hi asli kaam tha.",
         k="Data quality > Algorithm choice, consistent improvement"),

    dict(d="IMPORTANT",
         q="Scaling split ke baad kyu kiya, pehle nahi?",
         a="Kyunki leakage rokna tha. Agar pehle scale karte, test set ke mean/std bhi "
           "training data ke saath mix ho jaate. Isliye pehle train_test_split, phir "
           "StandardScaler.fit(X_train), phir scaler.transform(X_train aur X_test).",
         ex="Agar test data pehle se dekha, to evaluation fake ho jayega - real world "
            "mein aisa nahi hota.",
         k="Leakage prevention, scaling order"),

    dict(d="EASY",
         q="StandardScaler kaam kya karta hai?",
         a="Har feature ko is formula se transform karta hai: z = (x - mean) / std. "
           "Result: mean 0, std 1. Isse sab features same scale pe aa jaate hain.",
         ex="distance hazaar mein hai, duration_h 10 mein - bina scale, distance "
            "dominate kar deta KNN/SVM mein. Scale ke baad dono barabar.",
         k="StandardScaler, z-score, mean 0 std 1"),

    dict(d="MEDIUM",
         q="One-hot encoding kya hai? Kyu use kiya?",
         a="Categorical column ko 0/1 columns mein todna. Example: zone column mein "
           "'ER', 'WR' hai - one-hot se 'zone_ER' aur 'zone_WR' do columns ban jate "
           "hain, jisme 0/1 aata hai. ML model sirf numbers samajhta hai, strings nahi.",
         ex="Humne train_type, zones etc. ko one-hot kiya. Isse 26 features ban gaye.",
         k="One-hot encoding, categorical to numeric, dummy variables"),

    # ---------- SUPERVISED ----------
    dict(d="IMPORTANT",
         q="KNN aur SVM ke liye scaling kyu chahiye, DT ke liye nahi?",
         a="KNN distance calculate karta hai - bade scale wala feature dominate kar "
           "deta. SVM margin bhi distance pe based hai. Isliye scaling zaroori. "
           "Decision Tree splits pe kaam karta hai - 'x > 500?' - threshold se farak "
           "nahi padta ki value 500 hai ya 500000. Isliye DT scale-free hai.",
         ex="Humne DT ko unscaled aur scaled dono pe chalaya - same result. Lekin "
            "KNN/SVM ka result scale ke bina bahut kharab tha.",
         k="Distance-based, tree-based, scale-invariant, threshold"),

    dict(d="MEDIUM",
         q="Naive Bayes ka independence assumption kya hai?",
         a="NB maan leta hai ki saare features ek doosre se independent hain - matlab "
           "'distance' aur 'duration' ka koi relation nahi. Ye assumption real mein "
           "galat hoti hai (duration distance pe depend karta hai), isliye NB weak "
           "perform karta hai.",
         ex="Hamare project mein NB ka F1 sirf 0.3098 nikla - sabse kam. Kyunki "
            "features correlated the.",
         k="Conditional independence, Bayes theorem, correlated features"),

    dict(d="IMPORTANT",
         q="Confusion matrix kya dikhata hai? Apna result batao.",
         a="4 cheezein: True Positive, True Negative, False Positive, False Negative. "
           "Multi-class mein har class ke liye. Diagonal = correct predictions.",
         ex="Hamare DT ka overall error 8.50%. Dominant confusion: SF <-> Exp (25 SF "
            "ko Exp bola, 16 Exp ko SF bola). Pass sirf 3% galat, Exp 14%, SF 17.4%. "
            "Kyunki SF aur Exp features overlap karte hain.",
         k="TP, TN, FP, FN, diagonal, per-class error"),

    dict(d="MOST IMP",
         q="Accuracy vs F1 - kab kaunsa use karein?",
         a="Accuracy tab jab classes balanced ho. F1 tab jab imbalance ho, kyunki F1 "
           "precision aur recall ka harmonic mean hai - minority class ko bhi respect "
           "karta hai. Hamare project mein imbalance tha, isliye macro F1 primary "
           "metric tha.",
         ex="Hamara baseline 0.55 accuracy le raha tha sirf 'Pass' bolke, par macro F1 "
            "0.2367 thi. Accuracy dhoka de rahi thi, F1 ne sach bataya.",
         k="Accuracy, precision, recall, F1, harmonic mean, macro"),

    dict(d="MOST IMP",
         q="Best model kaunsa nikla? Kyu jeeta?",
         a="Decision Tree (default parameters) jeeta. Accuracy 91.50%, macro F1 0.8896, "
           "weighted F1 0.9146. Kyu: (1) DT ko scaling ki zaroorat nahi, (2) non-linear "
           "splits handle karta hai, (3) rule-based - interpretable, (4) one-hot "
           "features pe natural fit hai.",
         ex="KNN 0.8523, SVM 0.8412 - dono DT se kam. Naive Bayes 0.3702 - independence "
            "assumption ne maara.",
         k="Decision Tree, 91.50%, 0.8896 macro F1, interpretable, non-linear"),

    dict(d="IMPORTANT",
         q="Top feature importance kaunse nikle?",
         a="Decision Tree ki importance: (1) third_ac - 0.355, (2) distance - 0.223, "
           "(3) total_duration - 0.180, (4) chair_car - 0.118, (5) first_ac - 0.013.",
         ex="third_ac top pe hai kyunki SF aur Exp trains mein 3AC coaches zyada hote "
            "hain, Pass mein kam. Matlab coach composition hi class ka signal hai.",
         k="Feature importance, third_ac, distance, total_duration"),

    dict(d="IMPORTANT",
         q="ROC-AUC kya measure karta hai?",
         a="ROC curve - True Positive Rate vs False Positive Rate, har threshold pe. "
           "AUC = area under curve. 0.5 = random, 1.0 = perfect. Ye batata hai ki "
           "model threshold se independent kitna achha separate karta hai.",
         ex="Hamare results: KNN 0.9355 (best), SVM 0.9285, DT 0.9204. Sab 0.9 ke upar "
            "- matlab classes kaafi separable hain.",
         k="ROC, AUC, TPR, FPR, threshold-independent"),

    dict(d="MEDIUM",
         q="Stratified split kya hai? Kyu use kiya?",
         a="train_test_split mein 'stratify=y' - train aur test dono mein class ratio "
           "same rahega. Hamare 55/29/16 ka ratio dono sets mein preserve hua.",
         ex="Agar random split karte, to test set mein SF 5% hi reh jaata - model ka "
            "SF performance judge nahi kar pate.",
         k="Stratified split, class ratio preservation"),

    dict(d="IMPORTANT",
         q="5-fold Cross Validation kya hai? Result batao.",
         a="Data ko 5 equal parts mein baanto. Har baar 1 part test, baaki 4 train. "
           "5 different results aate hain. Average lo - pata chalta hai ki model "
           "stable hai ya nahi. Hamara DT ka 5-fold CV F1 macro 0.8743 +/- 0.0155.",
         ex="Agar single split pe 0.8896 aaya aur CV pe 0.8743 - matlab model "
            "overfit nahi hai, stable hai.",
         k="K-fold, cross validation, stability, variance"),

    # ---------- CLUSTERING ----------
    dict(d="IMPORTANT",
         q="Classification aur clustering mein kya difference?",
         a="Classification supervised hai - labeled data, model sikh ke naye data pe "
           "label deta hai. Clustering unsupervised hai - labels nahi hote, algorithm "
           "khud se similar cheezein group karta hai.",
         ex="Humne dono kiye - pehle 3 classes pe classify kiya, phir bina label ke "
            "K-Means/DBSCAN se 5 clusters nikale.",
         k="Supervised vs unsupervised, labeled vs unlabeled"),

    dict(d="IMPORTANT",
         q="Elbow method kya hai? k=5 kaise chuna?",
         a="Elbow method: different k values pe K-Means chala ke inertia (within-cluster "
           "sum of squares) plot karte hain. Jaha graph ka 'kone' (elbow) banta hai, "
           "wahi best k hota hai. Us point ke baad inertia slow hoti hai.",
         ex="Hamare elbow curve mein k=5 pe kink aayi - isliye k=5 chuna. "
            "Inertia 69,115.75.",
         k="Elbow method, inertia, WCSS, k selection"),

    dict(d="IMPORTANT",
         q="K-Means se pehle scaling kyu karte hain?",
         a="K-Means Euclidean distance pe based hai. Agar ek feature 1000s mein aur "
           "doosra 10s mein ho, to bada feature dominate kar deta. Scaling se sab "
           "features barabar weight pe aate hain.",
         ex="Bina scaling, distance wala feature cluster decide kar raha hota, "
            "duration_h ka role nahi rehta.",
         k="Euclidean distance, scaling, K-Means"),

    dict(d="IMPORTANT",
         q="Silhouette score kya batata hai?",
         a="Ye -1 se +1 ke beech hota hai. Batata hai ki point apne cluster mein kitna "
           "fit hai vs doosre cluster se kitna alag. +1 perfect, 0 boundary, -1 galat "
           "cluster.",
         ex="Hamara K-Means silhouette 0.2024 (fix ke baad). DBSCAN 0.2543 - thoda "
            "behtar. Low-medium hai kyunki clusters overlap karte hain real data mein.",
         k="Silhouette, cohesion, separation, -1 to +1"),

    dict(d="IMPORTANT",
         q="K-Means vs DBSCAN - kab kaunsa?",
         a="K-Means: k pehle dena padta, spherical clusters, outlier-sensitive. "
           "DBSCAN: k nahi batana, density-based, arbitrary shape, noise alag kar "
           "deta. DBSCAN better jab clusters irregular ho aur outliers ho.",
         ex="K-Means (k=5) silhouette 0.2024, DBSCAN (eps=7, min_samples=20) 4 "
            "clusters + 0.4% noise, silhouette 0.2543 - DBSCAN thoda behtar.",
         k="K-Means, DBSCAN, density-based, noise, eps, min_samples"),

    dict(d="MEDIUM",
         q="PCA kya hai? Plot ke liye kyu use kiya?",
         a="PCA (Principal Component Analysis) dimensionality reduction technique hai. "
           "26 features ko 2 principal components mein compress karta hai jo maximum "
           "variance capture karte hain. Isse 2D plot bana sakte hain.",
         ex="Hum 26 features ko direct plot nahi kar sakte. PCA ne 2D mein laaya taaki "
            "clusters visually dikh sakein - clusters_pca.png mein dikhaya.",
         k="PCA, dimensionality reduction, variance, principal components"),

    dict(d="IMPORTANT",
         q="5 clusters ko kaise interpret kiya?",
         a="Har cluster ka mean nikaal ke dekha. 5 clusters: (1) ER-regional, "
           "(2) NFR-mixed, (3) Short-distance Pass, (4) Long-distance AC Premium, "
           "(5) Unknown-zone Short Pass. Zone, distance, duration, coach types se "
           "interpret kiya.",
         ex="Cluster 3 (Short Pass) mein distance kam, sleeper coaches zyada. "
            "Cluster 4 (Long AC) mein distance zyada, 3AC/2AC zyada.",
         k="Cluster profiling, mean features, interpretation"),

    # ---------- DATA QUALITY STORY ----------
    dict(d="MOST IMP",
         q="Data quality fix ki poori story sunao (viva ke liye ready rakho).",
         a="EDA karte waqt notice kiya ki duration_m column ka range sirf 0-58 tha, "
           "jabki duration_h alag tha. Matlab duration_m total minutes nahi, sirf "
           "minute-component tha. Fix kiya: total_duration = duration_h*60 + "
           "duration_m. Phir saare models dobara train kiye - sab ka F1 sudhar gaya. "
           "Ye project ka central finding hai: data quality > algorithm choice.",
         ex="Pehle DT 0.8309, baad 0.8896. Naive Bayes bhi 0.2969 -> 0.3098. Sab "
            "consistent improvement.",
         k="Data quality fix, duration_m, total_duration, before/after"),

    dict(d="MOST IMP",
         q="Isse kya seekha? Biggest takeaway?",
         a="Biggest takeaway: Data quality > Algorithm choice. Log samajhte hain naya "
           "algorithm laane se accuracy badhegi. Lekin humne dekha ek simple fix ne 5 "
           "models ka performance badha diya. Viva mein zaroor bolna.",
         ex="Agar hum data fix na karte, DT 0.83 pe atka rehta. Kitne bhi models try "
            "karte, data hi galat tha.",
         k="Data quality > Algorithm choice, takeaway"),

    dict(d="MOST IMP",
         q="Har model ka fix se pehle/baad F1 batao.",
         a="KNN 0.7552 -> 0.7886 (+0.0334). DT 0.8309 -> 0.8896 (+0.0587). "
           "DT(depth=10) 0.7720 -> 0.8459 (+0.0739). Naive Bayes 0.2969 -> 0.3098 "
           "(+0.0129). SVM 0.7168 -> 0.7651 (+0.0483). Silhouette 0.1755 -> 0.2024 "
           "(+0.0269). Sab up!",
         ex="Ye table before_after_duration_fix.png mein bhi saved hai.",
         k="Before/after table, consistent improvement"),

    # ---------- LIMITATIONS ----------
    dict(d="IMPORTANT",
         q="Project ki limitations kya hain?",
         a="(1) Data 2020-21 ka snapshot hai, real-time nahi. (2) Sirf 3 classes cover "
           "kiye - real IR mein aur types hain. (3) SF aur Exp ka overlap hai - "
           "confusion matrix mein dikha. (4) Zone info mein kuch 'Unknown' values thi. "
           "(5) Model deployment not tested - notebook-level hai.",
         ex="SF ka error 17.4% - sabse zyada, kyunki SF aur Exp ke features overlap "
            "karte hain.",
         k="Snapshot data, 3 classes only, SF-Exp overlap, deployment"),

    dict(d="MEDIUM",
         q="Future mein kya improve kar sakte ho?",
         a="(1) Real-time data integrate - API se. (2) Deep learning try - Neural "
           "Network. (3) SMOTE se minority class (SF) balance. (4) Hyperparameter "
           "tuning - GridSearchCV. (5) Streamlit dashboard. (6) Zyada classes add - "
           "Rajdhani, Shatabdi, Vande Bharat.",
         ex="SMOTE se SF ke 719 samples ko 1,288 tak la sakte hain.",
         k="SMOTE, GridSearchCV, Streamlit, Neural Network, real-time"),

    # ---------- TOOLING ----------
    dict(d="EASY",
         q="Tool kaunsa use kiya?",
         a="VS Code with Python 3.13.6 aur Jupyter extension. Notebook .ipynb format "
           "mein. Terminal PowerShell.",
         ex="Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, joblib. "
            "Sab pip se install - requirements.txt mein hai.",
         k="VS Code, Python 3.13.6, Jupyter extension, .ipynb"),

    dict(d="EASY",
         q="Anaconda kyu nahi?",
         a="Anaconda ek bundled distribution hai - 3-4 GB ka. Humne Python aur "
           "libraries manually pip se install kiye. Same result, lighter setup, "
           "cleaner environment.",
         ex="pip install -r requirements.txt - bas.",
         k="pip vs conda, lightweight setup"),

    dict(d="IMPORTANT",
         q="Ye project reproducible hai? Kaise?",
         a="Bilkul. (1) requirements.txt hai - pip install -r se saare libraries. "
           "(2) Data CSV repo mein hai. (3) Notebook top-to-bottom chalao. "
           "(4) Random seed fixed - same results repeat honge. (5) Models bhi saved - "
           "load karke use kar sakte ho.",
         ex="Kisi bhi laptop pe git clone, pip install, notebook run - same results.",
         k="Reproducibility, requirements.txt, random seed, saved models"),

    dict(d="MEDIUM",
         q="Confusion matrix ko 3 classes ke liye kaise padhte hain?",
         a="3x3 grid hoti hai. Row = actual class, column = predicted. Diagonal pe "
           "correct predictions (Pass-Pass, Exp-Exp, SF-SF). Off-diagonal pe "
           "confusions - humne dekha SF 25 baar Exp bola gaya, Exp 16 baar SF.",
         ex="SF ka error 17.4% highest kyunki SF aur Exp features kaafi similar hain.",
         k="3x3 confusion matrix, diagonal, off-diagonal"),

    dict(d="MEDIUM",
         q="Micro vs macro vs weighted averaging mein difference?",
         a="Macro = har class ka score ka simple average (minority ko equal weight). "
           "Weighted = class size se weight (majority dominate). Micro = total TP/FP/FN "
           "ka aggregate. Imbalance wale data mein macro best.",
         ex="Hamare DT: macro 0.8896, weighted 0.9146, micro 0.9150. Macro lowest "
            "hai kyunki SF minority hai - wahi sach batata hai.",
         k="Macro, micro, weighted, averaging strategies"),

    dict(d="HARD",
         q="Kya model overfit hai? Kaise pata chala?",
         a="Nahi overfit nahi hai. Kaise pata chala: train accuracy ~ test accuracy. "
           "Aur 5-fold CV F1 0.8743 +/- 0.0155 - low variance. Agar overfit hota, "
           "train 99% test 70% hota aur CV mein bahut fluctuation aata.",
         ex="DT default parameters pe 0.9150 test accuracy diya. Depth 10 pe kam "
            "aaya (0.8859) - matlab simple model better hai.",
         k="Overfitting, train vs test, variance, CV"),

    dict(d="HARD",
         q="Agar koi feature missing ho jaye production mein toh?",
         a="Options: (1) Imputation - mean/median se bharo. (2) Model-based impute - "
           "KNN imputer. (3) Us feature ko drop karke retrain. (4) Agar missing rate "
           "bahut zyada - feature hatao. Production mein imputation pipeline "
           "preprocessing ke saath attach karni chahiye.",
         ex="Hamare data mein nulls nahi the, lekin real production mein ye common "
            "problem hai - pipeline mein imputer zaroor rakho.",
         k="Imputation, KNN imputer, preprocessing pipeline, production"),
]


def build_section_b(pdf):
    pdf.add_page()
    H1(pdf, "SECTION B - VIVA Q&A")
    P(pdf, "Har question ke saath difficulty tag hai: [MOST IMP] zaroor padhna, "
           "[IMPORTANT] achha hai, [MEDIUM]/[EASY] baad mein, [HARD] agar guide "
           "deep pooch le. Answer Hinglish mein hai, saath mein project ka example "
           "aur keywords diye hain. Keywords match hone chahiye - wording nahi.")

    for i, item in enumerate(QNA, start=1):
        Q(pdf, i, item["d"], item["q"])
        A(pdf, item["a"])
        if item.get("ex"):
            EX(pdf, item["ex"])
        if item.get("k"):
            KEY(pdf, item["k"])


# ============================================================
#  MAIN
# ============================================================

def main():
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(18, 15, 18)

    # ---------- COVER ----------
    pdf.add_page()
    pdf.ln(35)
    MC(pdf, "Viva Question Bank", size=28, bold=True, color=NAVY, align="C", h=12)
    pdf.ln(2)
    MC(pdf, "Indian Railway Trains ML Project", size=16, color=GREY, align="C", h=9)

    pdf.ln(12)
    MC(pdf, "Classification and Clustering of Indian Railway Trains "
            "Using Machine Learning",
       size=12, bold=True, color=DARK, align="C", h=7)

    pdf.ln(18)
    MC(pdf, "Prepared for: Rajput Prince Singh (Roll No. 83)",
       size=11, color=GREY, align="C", h=7)
    MC(pdf, "BCA Semester VII - Lokmanya College of Computer Application",
       size=11, color=GREY, align="C", h=7)
    MC(pdf, "Gujarat University - NEP 2020 - Academic Year 2025-26",
       size=11, color=GREY, align="C", h=7)

    pdf.ln(20)
    MC(pdf, "Contents:", size=11, bold=True, color=NAVY, h=7)
    MC(pdf, "Section A - Project Deep Dive (kya, kaise, kaha, kaunsa cell)",
       size=10.5, h=6)
    MC(pdf, f"Section B - {len(QNA)} Viva Questions with difficulty tags, "
            "examples, aur keywords", size=10.5, h=6)

    pdf.ln(6)
    MC(pdf, "Difficulty key: [MOST IMP] = zaroor, [IMPORTANT] = hona chahiye, "
            "[MEDIUM] = achha, [EASY] = basic, [HARD] = agar deep pooche.",
       size=9.5, italic=True, color=GREY, h=5)

    # ---------- SECTIONS ----------
    build_section_a(pdf)
    build_section_b(pdf)

    pdf.output(str(OUT_FILE))
    print(f"[OK] PDF generated: {OUT_FILE}")
    print(f"[OK] Total pages: {pdf.page_no()}")
    print(f"[OK] Total questions: {len(QNA)}")


if __name__ == "__main__":
    main()