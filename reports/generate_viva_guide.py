"""
Prince's Ultimate Hinglish Viva Master Guide PDF Generator
Project : Classification and Clustering of Indian Railway Trains Using Machine Learning
Student : Rajput Prince Singh (Roll No. 83) | BCA Sem-VII | Gujarat University (NEP 2020)
Courses : DSC-C-BCA-471T (AI), DSC-C-BCA-472T (ML), DSC-C-BCA-473P (ML System Design)
Output  : reports/Prince_Viva_Master_Guide.pdf
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


# ==============================================================================
# 1. PATHS & FONT SETUP
# ==============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR).lower() == "reports":
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    REPORTS_DIR = SCRIPT_DIR
else:
    PROJECT_ROOT = SCRIPT_DIR
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


def register_fonts():
    win_fonts = r"C:\Windows\Fonts"
    arial_reg = os.path.join(win_fonts, "arial.ttf")
    arial_bd = os.path.join(win_fonts, "arialbd.ttf")
    arial_it = os.path.join(win_fonts, "ariali.ttf")
    arial_bi = os.path.join(win_fonts, "arialbi.ttf")

    if all(os.path.exists(p) for p in [arial_reg, arial_bd, arial_it, arial_bi]):
        pdfmetrics.registerFont(TTFont("VivaFont", arial_reg))
        pdfmetrics.registerFont(TTFont("VivaFont-Bold", arial_bd))
        pdfmetrics.registerFont(TTFont("VivaFont-Italic", arial_it))
        pdfmetrics.registerFont(TTFont("VivaFont-BoldItalic", arial_bi))
        pdfmetrics.registerFontFamily(
            "VivaFont",
            normal="VivaFont",
            bold="VivaFont-Bold",
            italic="VivaFont-Italic",
            boldItalic="VivaFont-BoldItalic",
        )
        return "VivaFont", "VivaFont-Bold", "VivaFont-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


F_REG, F_BOLD, F_ITALIC = register_fonts()

# Colors for Designer Callout Boxes
C_NAVY = colors.HexColor("#0F2C59")
C_BLUE_BG = colors.HexColor("#EBF3FA")
C_BLUE_BDR = colors.HexColor("#1F618D")

C_GREEN_BG = colors.HexColor("#E8F8F5")
C_GREEN_BDR = colors.HexColor("#117A65")

C_YELLOW_BG = colors.HexColor("#FEF9E7")
C_YELLOW_BDR = colors.HexColor("#B7950B")

C_RED_BG = colors.HexColor("#FDEDEC")
C_RED_BDR = colors.HexColor("#C0392B")

C_PURPLE_BG = colors.HexColor("#F5EEF8")
C_PURPLE_BDR = colors.HexColor("#7D3C98")

C_GRAY_ALT = colors.HexColor("#F8F9F9")
C_BORDER = colors.HexColor("#D0D3D4")


def get_styles():
    base = getSampleStyleSheet()
    st = {}

    st["TitleMain"] = ParagraphStyle(
        "TitleMain",
        parent=base["Normal"],
        fontName=F_BOLD,
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor= colors.white,
    )
    st["TitleSub"] = ParagraphStyle(
        "TitleSub",
        parent=base["Normal"],
        fontName=F_REG,
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#D6EAF8"),
    )
    st["SectionHdr"] = ParagraphStyle(
        "SectionHdr",
        parent=base["Heading1"],
        fontName=F_BOLD,
        fontSize=14,
        leading=19,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
    st["SubHdr"] = ParagraphStyle(
        "SubHdr",
        parent=base["Heading2"],
        fontName=F_BOLD,
        fontSize=12.5,
        leading=17,
        textColor=C_NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    st["Body"] = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName=F_REG,
        fontSize=10.5,
        leading=15.5,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        textColor=colors.black,
    )
    st["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=st["Body"],
        leftIndent=16,
        firstLineIndent=-10,
        spaceAfter=5,
    )
    st["BoxText"] = ParagraphStyle(
        "BoxText",
        parent=st["Body"],
        fontSize=10.5,
        leading=15.5,
        spaceAfter=4,
    )
    st["TblHdr"] = ParagraphStyle(
        "TblHdr",
        parent=st["Body"],
        fontName=F_BOLD,
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.white,
        spaceAfter=0,
    )
    st["TblCell"] = ParagraphStyle(
        "TblCell",
        parent=st["Body"],
        fontSize=9.8,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    st["TblCellCenter"] = ParagraphStyle(
        "TblCellCenter",
        parent=st["TblCell"],
        alignment=TA_CENTER,
    )
    return st


ST = get_styles()


# ==============================================================================
# 2. DESIGNER COMPONENTS (BANNERS, CALLOUT BOXES, Q&A CARDS, TABLES)
# ==============================================================================

def draw_footer(canvas, doc):
    canvas.saveState()
    page_num = canvas.getPageNumber()
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(0.6 * inch, 0.55 * inch, A4[0] - 0.6 * inch, 0.55 * inch)
    canvas.setFont(F_ITALIC, 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(
        0.6 * inch,
        0.38 * inch,
        "Prince Viva Master Guide (Hinglish Edition) | Roll No. 83 | Indian Railways ML Project",
    )
    canvas.setFont(F_BOLD, 9.5)
    canvas.drawRightString(A4[0] - 0.6 * inch, 0.38 * inch, f"Page {page_num}")
    canvas.restoreState()


def add_section_banner(story, title, page_break=False):
    if page_break:
        story.append(PageBreak())
    story.append(Spacer(1, 6))
    tbl = Table([[Paragraph(title, ST["SectionHdr"])]], colWidths=[7.0 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(KeepTogether([tbl, Spacer(1, 8)]))


def add_callout_box(story, title, paragraphs, bg_color, border_color):
    content = []
    if title:
        content.append(
            Paragraph(
                f"<b>{title}</b>",
                ParagraphStyle(
                    "BxTitle",
                    parent=ST["BoxText"],
                    fontName=F_BOLD,
                    fontSize=11,
                    textColor=border_color,
                    spaceAfter=4,
                ),
            )
        )
    for p_txt in paragraphs:
        content.append(Paragraph(p_txt, ST["BoxText"]))

    tbl = Table([[content]], colWidths=[7.0 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("BOX", (0, 0), (-1, -1), 1.2, border_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(KeepTogether([tbl, Spacer(1, 8)]))


def add_concept_card(story, term_title, baccha_meaning, project_use, viva_line):
    rows = [
        [
            Paragraph(
                f"<b>{term_title}</b>",
                ParagraphStyle(
                    "CT",
                    parent=ST["BoxText"],
                    fontName=F_BOLD,
                    fontSize=11,
                    textColor=C_NAVY,
                ),
            )
        ],
        [
            Paragraph(
                f"<b>Baccha-Level Matlab (Desi Example):</b> {baccha_meaning}",
                ST["BoxText"],
            )
        ],
        [
            Paragraph(
                f"<b>Apne Project Mein Kya Kiya:</b> {project_use}",
                ST["BoxText"],
            )
        ],
        [
            Paragraph(
                f"<b>Examiner Ko Bolne Wali Line:</b> <i>\"{viva_line}\"</i>",
                ParagraphStyle(
                    "VL",
                    parent=ST["BoxText"],
                    textColor=C_GREEN_BDR,
                ),
            )
        ],
    ]
    tbl = Table(rows, colWidths=[7.0 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), C_BLUE_BG),
                ("BACKGROUND", (0, 1), (-1, 2), colors.white),
                ("BACKGROUND", (0, 3), (-1, 3), C_GREEN_BG),
                ("BOX", (0, 0), (-1, -1), 0.9, C_BLUE_BDR),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, C_BLUE_BDR),
                ("LINEABOVE", (0, 3), (-1, 3), 0.6, C_GREEN_BDR),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(KeepTogether([tbl, Spacer(1, 7)]))


def add_qa_card(story, q_num, question, simple_samajh, bolne_wala_answer):
    rows = [
        [
            Paragraph(
                f"<b>Q{q_num}. {question}</b>",
                ParagraphStyle(
                    "QH",
                    parent=ST["BoxText"],
                    fontName=F_BOLD,
                    fontSize=10.8,
                    textColor=colors.white,
                ),
            )
        ],
        [
            Paragraph(
                f"<b>Dimag Mein Samajhne Ke Liye:</b> {simple_samajh}",
                ST["BoxText"],
            )
        ],
        [
            Paragraph(
                f"<b>Sir Ke Saamne Bolna:</b> \"{bolne_wala_answer}\"",
                ParagraphStyle(
                    "QA",
                    parent=ST["BoxText"],
                    textColor=colors.HexColor("#0B5345"),
                ),
            )
        ],
    ]
    tbl = Table(rows, colWidths=[7.0 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), C_YELLOW_BG),
                ("BACKGROUND", (0, 2), (-1, 2), C_GREEN_BG),
                ("BOX", (0, 0), (-1, -1), 0.8, C_NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(KeepTogether([tbl, Spacer(1, 6)]))


def add_data_table(story, headers, rows, col_widths, center_cols=None):
    if center_cols is None:
        center_cols = set()
    data = [[Paragraph(str(h), ST["TblHdr"]) for h in headers]]
    for r in rows:
        row_cells = []
        for idx, val in enumerate(r):
            style = ST["TblCellCenter"] if idx in center_cols else ST["TblCell"]
            row_cells.append(Paragraph(str(val), style))
        data.append(row_cells)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    t_style = [
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r_i in range(1, len(data)):
        bg = C_GRAY_ALT if r_i % 2 == 0 else colors.white
        t_style.append(("BACKGROUND", (0, r_i), (-1, r_i), bg))
    tbl.setStyle(TableStyle(t_style))
    story.append(KeepTogether([tbl, Spacer(1, 8)]))


# ==============================================================================
# 3. BUILD THE COMPLETE HINGLISH VIVA GUIDE PDF
# ==============================================================================

def build_viva_pdf():
    out_path = os.path.join(REPORTS_DIR, "Prince_Viva_Master_Guide.pdf")
    story = []

    # --------------------------------------------------------------------------
    # HEADER BANNER (COVER BLOCK)
    # --------------------------------------------------------------------------
    cover_data = [
        [
            Paragraph(
                "INDIAN RAILWAY TRAINS ML PROJECT — VIVA MASTER GUIDE",
                ST["TitleMain"],
            )
        ],
        [
            Paragraph(
                "Zero-Blank-Out Hinglish Preparation Book | Baccha-Level Concepts + Syllabus Map + 35 Viva Q&A<br/>"
                "<b>Student:</b> Rajput Prince Singh (Roll No. 83) | <b>College:</b> Lokmanya College of Computer Applications<br/>"
                "<b>Courses:</b> DSC-C-BCA-471T (AI) &middot; DSC-C-BCA-472T (ML) &middot; DSC-C-BCA-473P (ML System Design) | <b>Guide:</b> Prof. Sejal Shah",
                ST["TitleSub"],
            )
        ],
    ]
    cover_tbl = Table(cover_data, colWidths=[7.0 * inch])
    cover_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                ("BOX", (0, 0), (-1, -1), 1.5, C_BLUE_BDR),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    story.append(cover_tbl)
    story.append(Spacer(1, 10))

    # --------------------------------------------------------------------------
    # PART 1: ZERO-BLANK-OUT OPENING PITCH (1 PARAGRAPH MAGIC)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 1: JAB EXAMINER POOCHE — 'BATAO BETA, KYA PROJECT BANAYA HAI?'",
    )

    add_callout_box(
        story,
        "TERE DIMAG KE LIYE ASLI MATLAB (Ek Paragraph Mein Poora Project):",
        [
            "Bhai simple samajh: Indian Railways mein roz hazaaron trains chalti hain. Har train ko 3 main category mein baanta jaata hai — "
            "<b>1. Passenger (Pass)</b> (jo choti duri par chalti hai, har chote station par rukti hai aur jisme AC dabbe nahi hote), "
            "<b>2. Express (Exp)</b> (jo medium se lambi duri par chalti hai aur jisme Sleeper + AC dono dabbe hote hain), aur "
            "<b>3. Superfast (SF)</b> (jo sabse fast, VIP priority wali lambi train hoti hai jisme bhar-bhar ke AC dabbe hote hain). "
            "Ab problem yeh thi ki agar hum computer ko sirf train ki <b>Duri (Distance)</b>, <b>Safar ka Time (Duration)</b>, "
            "<b>Kaun-kaun se dabbe lage hain (1AC, 2AC, 3AC, Sleeper, Chair Car)</b>, aur <b>Train ka Zone (WR, NR, ER)</b> dein, "
            "toh kya computer khud pehchan sakta hai ki yeh train Passenger hai, Express hai ya Superfast? "
            "Humne <b>Kaggle</b> se <b>5,208 trains</b> ka data uthaya, usme se <b>4,466 trains</b> filter ki, data ke andar chhupi hui ek "
            "bahut badi galti (<b>duration_m bug</b>) ko pakad kar theek kiya, aur <b>5 Supervised ML Models</b> sikhaye — jisme "
            "<b>Decision Tree</b> ne <b>91.50% Accuracy</b> ke saath top kiya! Iske alawa humne <b>Unsupervised Clustering (K-Means aur DBSCAN)</b> "
            "laga kar bina kisi label ke trains ke <b>5 natural groups</b> aur <b>13 ajeeb (outlier) trains</b> bhi dhoondh nikaali!"
        ],
        C_YELLOW_BG,
        C_YELLOW_BDR,
    )

    add_callout_box(
        story,
        "VIVA MEIN BOLNE WALI 1-MINUTE SPEECH (Isko 3 Baar Bol Kar Practice Kar Le):",
        [
            "<i>\"Good Morning Sir/Ma'am. Mere project ka title hai <b>Classification and Clustering of Indian Railway Trains Using Machine Learning</b>. "
            "Sir, is project mein humne Indian Railways ki <b>4,466 trains</b> ke timetable aur operational data par kaam kiya hai. "
            "Humne do main problems solve ki hain: Pehla, <b>Supervised Classification</b> — jisme hum train ke <b>26 features</b> "
            "(jaise route distance, total journey duration, AC/Sleeper coach indicators, aur 19 railway zones) dekh kar predict karte hain "
            "ki train <b>Passenger (Pass)</b> hai, <b>Express (Exp)</b> hai, ya <b>Superfast (SF)</b> hai. Isme hamara <b>Decision Tree model "
            "91.50% Accuracy aur 0.8896 Macro F1-score</b> ke saath best raha. "
            "Dusra, <b>Unsupervised Clustering</b> — jisme humne <b>K-Means (k=5)</b> aur <b>DBSCAN</b> use karke trains ke hidden operational "
            "groups aur <b>0.4% schedule outliers (13 trains)</b> discover kiye. "
            "Sir, is project ki sabse badi finding yeh thi ki raw data mein <b>duration_m</b> column mein ek bug tha jisko humne "
            "<b>total_duration = (duration_h * 60) + duration_m</b> se fix kiya, aur us ek data quality fix se hamare saare 5 models ki "
            "performance jump kar gayi!\"</i>"
        ],
        C_GREEN_BG,
        C_GREEN_BDR,
    )

    # --------------------------------------------------------------------------
    # PART 2: STEP-BY-STEP STORY (KAISA DATA UTHAYA, KYA PROBLEM THI, KYA KIYA)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 2: PROJECT KI POORI KAHANI — STEP BY STEP (ZERO CONFUSION)",
    )

    story.append(
        Paragraph(
            "Agar examiner pooche ki <b>'Tune shuru se aakhir tak step-by-step kya kiya?'</b>, toh yeh 6 steps dimag mein rakh:",
            ST["Body"],
        )
    )

    steps_rows = [
        (
            "Step 1: Data Kahan Se Aaya? (GeoJSON to CSV)",
            "Kaggle se Sripaad Srinivasan ka 'Indian Railways Dataset' uthaya. Original file trains.json (14.08 MB GeoJSON) thi jisme 5,208 trains thi. JSON file bhaari hoti hai, isliye humne usko clean tabular trains.csv (636 KB) mein convert kiya aur notebook mein CSV-First loading lagayi.",
        ),
        (
            "Step 2: 5,208 Se 4,466 Trains Filter Kyun Ki?",
            "5,208 trains mein kuch ginti ki special trains thi (Rajdhani, Shatabdi, Toy Train). Unke samples bahut kam the. Isliye humne 3 main classes par focus kiya: Passenger (Pass: 2,459 - 55.06%), Express (Exp: 1,288 - 28.84%), aur Superfast (SF: 719 - 16.10%). Total = 4,466 trains.",
        ),
        (
            "Step 3: Sabse Bada Bug Pakda (The Killer Viva Point!)",
            "Dataset mein safar ka time 2 tukdo mein tha: duration_h (ghante) aur duration_m (minute). Par duration_m mein total minutes nahi the! Sirf bache hue 0 se 58 minutes the! Jaise 24 ghante 0 min wali train ka duration_m = 0 tha. Humne formula lagaya: total_duration = (duration_h * 60) + duration_m. Isse 24 ghante wali train 1,440 minutes ban gayi!",
        ),
        (
            "Step 4: Data Cleaning & Leakage-Free Split (80/20)",
            "Train ka Name aur Number hata diya (kyunki naam se math nahi hoti). 19 Railway Zones ko One-Hot Encoding se 0/1 columns banaya (Total 26 features). Phir 80% Training (3,572 trains) aur 20% Testing (894 trains) mein baanta, aur StandardScaler ko SIRF training data par fit kiya taaki paper leak (Data Leakage) na ho!",
        ),
        (
            "Step 5: 5 Supervised Models Ki Race Lagayi",
            "1. Dummy Baseline (55.03%), 2. KNN (85.23%), 3. Decision Tree Default (91.50% - WINNER), 4. Decision Tree Depth=10 (88.59%), 5. Naive Bayes (37.02% - Flop), 6. SVM RBF (84.12%). Decision Tree jeet gaya!",
        ),
        (
            "Step 6: Unsupervised Clustering & Model Saving",
            "Bina label bataye K-Means (k=5, Silhouette 0.2024) se 5 fleet groups banaye aur DBSCAN (Silhouette 0.2543) se 4 natural clusters + 13 ajeeb trains (0.4% noise) pakdi. Aakhir mein data/trains_with_clusters.csv aur models/dt_classifier.joblib save kiya.",
        ),
    ]
    add_data_table(
        story,
        ["Step", "Tune Kya Kiya Aur Kyun Kiya (Simple Hinglish)"],
        steps_rows,
        [1.8 * inch, 5.2 * inch],
    )

    add_callout_box(
        story,
        "KILLER VIVA TABLE: Duration Bug Fix Karne Se Kya Chamatkar Hua?",
        [
            "Examiner ko yeh zaroor batana ki jab humne <b>total_duration = (duration_h * 60) + duration_m</b> banaya, "
            "tab <b>ek bhi model aisa nahi tha jo improve na hua ho!</b> Iska matlab: <b>Data Quality > Algorithm Choice</b>."
        ],
        C_PURPLE_BG,
        C_PURPLE_BDR,
    )

    fix_rows = [
        ("KNN (k=5)", "0.7552", "0.7886", "+0.0334", "Sahi minutes milne se padosi sahi mile"),
        ("Decision Tree (Default)", "0.8309", "0.8896", "+0.0587", "Winner model 83% se seedha ~89% F1 par pahuncha!"),
        ("Decision Tree (Depth=10)", "0.7720", "0.8459", "+0.0739", "Sabse bada jump (+7.39% gain)"),
        ("Naive Bayes", "0.2969", "0.3098", "+0.0129", "Thoda sudhra, par correlation ki wajah se kamzor raha"),
        ("SVM (RBF)", "0.7168", "0.7651", "+0.0483", "Boundary line aur saaf ho gayi"),
        ("K-Means Silhouette", "0.1755", "0.2024", "+0.0269", "Clusters aur tight aur saaf bane"),
    ]
    add_data_table(
        story,
        ["Model / Metric", "Fix Se Pehle (F1)", "Fix Ke Baad (F1)", "Kitna Badha", "Kyun Badha?"],
        fix_rows,
        [1.5 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch, 2.6 * inch],
        center_cols={1, 2, 3},
    )

    # --------------------------------------------------------------------------
    # PART 3: KAUNSI PYTHON LIBRARY KYA KAAM KARTI HAI? (SYLLABUS UNIT 1)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 3: TERE PROJECT KI PYTHON LIBRARIES & TOOLS (BACCHA EXPLANATION)",
        page_break=True,
    )

    story.append(
        Paragraph(
            "Gujarat University ke <b>DSC-C-BCA-472T (Unit 1)</b> aur <b>473P</b> mein sabse pehle poochte hain ki "
            "kaunse tools aur libraries use kiye aur kyun. Isko ghar ke kitchen ki tarah samajh:",
            ST["Body"],
        )
    )

    lib_rows = [
        (
            "Python 3.13.6",
            "Main Programming Language",
            "Machine Learning ki sabse aasan aur powerful bhasha. Jaise kitchen ka gas stove.",
            " data processing aur ML coding ke liye.",
        ),
        (
            "VS Code + Jupyter (.ipynb)",
            "Code Editor / Interactive Notebook",
            "Jahan hum chote-chote boxes (Cells) mein code chala kar turant niche graph aur output dekh sakte hain.",
            "main_notebook.ipynb (40 cells) aur advanced_ml.ipynb (10 cells) banane ke liye.",
        ),
        (
            "pandas",
            "Data Table Manager (Excel on Steroids)",
            "Jaise MS Excel mein rows aur columns ki table (DataFrame) hoti hai, Pandas Python ke andar table load karta hai, filter karta hai aur naye columns jodta hai.",
            "pd.read_csv(), null check, 3 classes filter, aur pd.get_dummies() (One-Hot Encoding) ke liye.",
        ),
        (
            "numpy",
            "Fast Number & Matrix Calculator",
            "Bade-bade numbers ki list (Arrays) aur maths formulas ko bijli ki speed se calculate karne wala calculator.",
            "Log-scale transformation, array manipulation, aur mean/std nikaalne ke liye.",
        ),
        (
            "matplotlib",
            "Basic Artist / Drawing Board",
            "Data ke numbers ko dekh kar sadharan line graph, bar chart aur histogram draw karne wala painter.",
            "Histograms, Bar charts, Line plots, ROC curve aur PNG files save karne ke liye.",
        ),
        (
            "seaborn",
            "HD Designer / Makeup Artist",
            "Matplotlib ke upar bana hua stylish tool jo ek line mein khoobsurat color-coded Heatmaps, Boxplots aur Pairplots banata hai.",
            "Correlation Heatmap, Pairplot, Boxplot aur KDE Density plots banane ke liye.",
        ),
        (
            "scikit-learn (sklearn)",
            "Machine Learning Ka Asli Engine / Dimag",
            "Isi library ke andar saare ready-made ML algorithms (KNN, DT, SVM, Naive Bayes, K-Means, DBSCAN) aur accuracy/F1 naapne ke tarazu rehte hain.",
            "train_test_split, StandardScaler, 5 classifiers, K-Means, DBSCAN, PCA, aur evaluation metrics ke liye.",
        ),
        (
            "joblib",
            "Model Ka Tiffin Box (Save/Load Tool)",
            "Jab model padhai karke taiyaar ho jaaye, toh usko hard disk par file (.joblib) mein pack karke save karne wala dabba taaki baar-baar train na karna pade.",
            "models/scaler.joblib aur models/dt_classifier.joblib ko save karne ke liye.",
        ),
    ]
    add_data_table(
        story,
        ["Library / Tool", "Role", "2 Saal Ke Bacche Jaisa Matlab", "Project Mein Kahan Use Hua?"],
        lib_rows,
        [1.15 * inch, 1.35 * inch, 2.35 * inch, 2.15 * inch],
    )

    # --------------------------------------------------------------------------
    # PART 4: SYLLABUS UNITS 1 TO 4 — HAR EK TERM KI BACCHA-LEVEL DICTIONARY
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 4: SYLLABUS KE SAARE CONCEPTS & TERMS (ZERO UNDEFINED WORDS!)",
    )

    story.append(
        Paragraph("<b>UNIT 1 CONCEPTS: ML BASICS, DATA TYPES & PREPROCESSING</b>", ST["SubHdr"])
    )

    add_concept_card(
        story,
        "1. Machine Learning (ML) vs Traditional Programming",
        "Normal programming mein hum computer ko khud rule likh kar dete hain (if distance > 500 then Express). Par Machine Learning mein hum computer ko <b>purani 3,572 trains ka data aur unka jawab dikhate hain</b>, aur computer khud dekh-dekh kar rules seekh leta hai! Jaise chota baccha 50 kutton aur billiyon ki photo dekh kar khud pehchanna seekh jaata hai.",
        "Humne 3,572 trains dikha kar computer ko sikhaya ki Pass, Exp aur SF trains kaisi dikhti hain.",
        "Sir, Machine Learning enables systems to automatically learn patterns and decision boundaries from historical data without being explicitly programmed.",
    )

    add_concept_card(
        story,
        "2. Supervised Learning vs Unsupervised Learning (Syllabus Unit 1, 3, 4)",
        "<b>Supervised Learning (Teacher ke saath padhai):</b> Jab data ke saath <b>Answer Key (Label)</b> pehle se di ho — jaise har train ke aage likha hai ki woh Pass hai, Exp hai ya SF. <br/><b>Unsupervised Learning (Bina Teacher ke chhantna):</b> Jab koi Answer Key na di ho! Jaise bacche ko 100 alag-alag khilone de diye aur bola ki jo ek jaise dikhte hain unke alag-alag dher (groups/clusters) bana do.",
        "Supervised mein humne 5 models (KNN, DT, NB, SVM, Dummy) se train ka type predict kiya. Unsupervised mein K-Means aur DBSCAN se bina label ke 5 groups (clusters) banaye.",
        "Sir, Supervised learning uses labeled target data (Pass, Exp, SF) for prediction, whereas Unsupervised learning discovers hidden groupings (clusters) without target labels.",
    )

    add_concept_card(
        story,
        "3. Features (X) vs Target Variable (y) & Numerical vs Categorical Data",
        "<b>Features (X) = Sawaal ke Clues:</b> Woh 26 cheezein jinhe dekh kar faisla lena hai (Distance, Total Duration, 3AC, Sleeper, Zone). <br/><b>Target (y) = Aakhiri Jawaab:</b> Train ka type (Pass, Exp, SF). <br/><b>Numerical Data:</b> Number wala data jisko naap sakte hain (Distance = 558 km, Duration = 300 min). <br/><b>Categorical Data:</b> Naam ya group wala data (Zone = WR, NR; Type = Pass, Exp, SF).",
        "Humare paas 26 Features (X) hain aur 1 Categorical Target (y) hai jisme 3 classes hain.",
        "Sir, X represents our 26 independent input features, and y is our dependent categorical target variable containing 3 train classes.",
    )

    add_concept_card(
        story,
        "4. One-Hot Encoding (pd.get_dummies) — 26 Features Kaise Bane?",
        "Computer ko matematik aati hai, ABCD nahi! Agar Zone column mein 'WR', 'NR', 'ER' likha hai, toh computer uska plus-minus nahi kar sakta. Isliye <b>One-Hot Encoding</b> har Zone ke liye ek alag <b>On/Off Switch (0 ya 1 ka column)</b> bana deta hai. Agar train Western Railway (WR) ki hai, toh zone_WR = 1 hoga aur baaki saare 18 zones = 0 honge!",
        "7 numerical/coach features + 19 one-hot encoded zone columns = Total 26 Features bane.",
        "Sir, One-Hot Encoding converts the nominal categorical 'zone' column into 19 binary (0/1) columns so numerical ML models can process them.",
    )

    add_concept_card(
        story,
        "5. Exploratory Data Analysis (EDA) & Correlation (r)",
        "<b>EDA:</b> Model banane se pehle data ki kundali check karna — graphs bana kar dekhna ki kahan kachra hai, kaunsa data tedha (skewed) hai. <br/><b>Correlation (r):</b> Do cheezon ki aapas mein kitni pakki dosti hai (-1 se +1 tak). Agar ek badhne par dusra bhi badhe toh +1 ke paas hota hai.",
        "Distance aur Total Duration ka correlation <b>r = 0.98</b> aaya (kyunki jitni lambi duri hogi, utna hi zyada time lagega!). Third AC aur Sleeper ka <b>r = 0.86</b> aaya.",
        "Sir, EDA helped us discover the duration_m bug and revealed a 0.98 positive Pearson correlation between route distance and total duration.",
    )

    story.append(
        Paragraph("<b>UNIT 2 CONCEPTS: SPLITTING, SCALING, LEAKAGE & EVALUATION METRICS</b>", ST["SubHdr"])
    )

    add_concept_card(
        story,
        "6. Hold-Out Method (80/20 Stratified Train-Test Split)",
        "Soch agar school teacher saal bhar jo 100 sawaal class mein padhaye, bilkul wahi 100 sawaal final exam mein de de, toh pata kaise chalega ki baccha samajh kar aaya hai ya ratta maar ke? Isliye hum <b>4,466 trains mein se 80% (3,572 trains)</b> padhai (Training) ke liye देते hain aur <b>20% (894 trains)</b> chhupa kar rakhte hain Final Exam (Testing) ke liye! <br/><b>Stratified (`stratify=y`) ka matlab:</b> Dono hisson mein Pass (55%), Exp (29%), aur SF (16%) ka barabar अनुपात (ratio) rakhna.",
        "train_test_split(X, y, test_size=0.2, stratify=y, random_state=42) -> 3,572 train aur 894 test.",
        "Sir, we used an 80/20 stratified train-test split so that class proportions remain identical in both training (3,572) and testing (894) sets.",
    )

    add_concept_card(
        story,
        "7. Data Leakage & StandardScaler (Scaling Split Ke Baad Kyun Ki?)",
        "<b>StandardScaler kya hai?</b> Distance column mein 4,000 km tak ke bade numbers hain, jabki 3AC dabbe mein sirf 0 ya 1 hai. KNN aur SVM jaise models bade number (4000) se dar jaate hain aur 0/1 ko ignore kar dete hain. StandardScaler sabhi features ko ek barabar scale (Mean = 0, Std = 1) par le aata hai. <br/><b>Data Leakage kya hai?</b> Agar hum split karne se pehle poore data par scaler laga dein, toh Test set (exam paper) ka average Training mein leak ho jaata hai! Isliye humne pehle split kiya, phir scaler ko sirf X_train par fit kiya.",
        "scaler.fit_transform(X_train) aur scaler.transform(X_test) use kiya.",
        "Sir, fitting StandardScaler before train-test split causes data leakage by exposing test set statistics to the training process. Hence, we fitted it strictly on X_train.",
    )

    add_concept_card(
        story,
        "8. Underfitting vs Overfitting vs 5-Fold Cross-Validation",
        "<b>Underfitting:</b> Baccha bilkul padh kar nahi gaya — class test mein bhi fail, final exam mein bhi fail (Jaise hamara Naive Bayes: 37%). <br/><b>Overfitting:</b> Bacche ne kitaab ke saare sawaal rat liye — ghar par 100% laaya par final exam mein naye sawaal aate hi fail ho gaya! <br/><b>5-Fold Cross-Validation:</b> Yeh check karne ke liye ki hamara Decision Tree ratta (overfit) toh nahi maar raha, humne data ke 5 barabar tukde kiye aur 5 baar alag-alag exam liya.",
        "Decision Tree ka 5-Fold CV Macro F1 <b>0.8743 +/- 0.0155</b> aaya, jo prove karta hai ki model bilkul overfit nahi ho raha!",
        "Sir, our 5-fold stratified cross-validation achieved 0.8743 Macro F1 with a tiny standard deviation of 0.0155, proving our Decision Tree generalizes well without overfitting.",
    )

    add_callout_box(
        story,
        "SABSE ZAROORI: ACCURACY, PRECISION, RECALL AUR F1-SCORE KYA HOTA HAI?",
        [
            "Examiner 100% poochega: <b>'F1-Score kya hota hai aur tune Accuracy ki jagah Macro F1 ko main metric kyun banaya?'</b> Isko aise samajh:",
            "<b>1. Accuracy (91.50%) — Aur Yeh Dhokha Kyun Deti Hai?</b><br/>"
            "Accuracy ka matlab: Total 894 test trains mein se kitni sahi pehchani (818 sahi / 894 = 91.50%). "
            "<b>Par ruk!</b> Humare data mein <b>55.06% trains Passenger</b> hain. Agar ek aalsi baccha (<b>Dummy Baseline</b>) bina soche har train ko 'Passenger' bol de, toh bhi uski Accuracy <b>55.03%</b> aa jayegi, jabki usne ek bhi Express ya Superfast nahi pehchani! Isliye jab classes barabar na hon (Class Imbalance), tab sirf Accuracy nahi dekhte!",
            "<b>2. Precision (Sateekta — 'Fekne par rok'):</b><br/>"
            "Matlab: <i>'Model ne jitni trains ko Superfast BOLA, unme se sach mein kitni Superfast nikli?'</i> Agar model ne 100 trains ko Superfast bola aur unme se 90 sach mein Superfast thi, toh Precision = 90%. Formula: <b>TP / (TP + FP)</b>.",
            "<b>3. Recall (Pakadne ki taqat — 'Chhootne par rok'):</b><br/>"
            "Matlab: <i>'Asliyat mein jitni Superfast trains THI, model ne unme se kitni dhoondh nikaali?'</i> Agar asliyat mein 144 Superfast thi aur model ne 119 pakad li, toh Recall = 82.6%. Formula: <b>TP / (TP + FN)</b>.",
            "<b>4. F1-Score Kya Hota Hai? (Precision aur Recall ka Pakka Balance):</b><br/>"
            "Kabhi-kabhi model Precision badhane ke chakkar mein Recall gira deta hai (ya ulta). <b>F1-Score Precision aur Recall dono ka Harmonic Mean (balance) hota hai: F1 = 2 * (Precision * Recall) / (Precision + Recall).</b> F1-Score tabhi high aayega jab Precision aur Recall DONO high honge!",
            "<b>5. Macro F1 (0.8896) vs Weighted F1 (0.9146) vs Micro F1 (0.9150):</b><br/>"
            "&bull; <b>Macro F1 (Hamara Main Hero Metric = 0.8896):</b> Pehle Pass ka F1 nikaalo, Exp ka F1 nikaalo, SF ka F1 nikaalo, aur teeno ko barabar izzat dete hue 3 se divide kar do: <b>(F1_Pass + F1_Exp + F1_SF) / 3</b>. Kyunki Superfast trains kam (16%) hain, Macro F1 unko bhi barabar importance deta hai!<br/>"
            "&bull; <b>Weighted F1 (0.9146):</b> Jis class ki jitni sankhya hai us hisaab se weight dekar average nikaalna.<br/>"
            "&bull; <b>Micro F1 / Micro Precision / Micro Recall (0.9150):</b> Saari classes ke total sahi predictions ko jod kar nikaalna — multi-class mein yeh humesha Accuracy (0.9150) ke barabar hota hai!"
        ],
        C_BLUE_BG,
        C_BLUE_BDR,
    )

    add_concept_card(
        story,
        "9. Confusion Matrix (3x3 Table) & ROC-AUC Curve",
        "<b>Confusion Matrix:</b> Ek 3x3 ki table jiske ek taraf 'Asliyat (Actual)' aur dusri taraf 'Model ki Bhavishyavani (Predicted)' likhi hoti hai. Isse saaf dikhta hai ki model kahan confuse hua! <br/><b>ROC-AUC Curve:</b> Model apne jawaab par kitna confident hai (0 se 1 ke beech score; 1 ke jitna paas utna shandaar).",
        "Humari overall galti 8.50% hai (Pass mein sirf 3.0% galti, Exp mein 14.0%, SF mein 17.4%). Sabse zyada confusion SF aur Exp ke beech hua (25 SF ko Exp bola, 16 Exp ko SF bola). Ek bhi SF ko Pass nahi bola (0)! ROC-AUC mein KNN (0.9355), SVM (0.9285), aur DT (0.9204) aaye.",
        "Sir, the Confusion Matrix shows an 8.50% overall error rate, mainly along the Express-Superfast boundary, with zero Superfast trains misclassified as Passenger.",
    )

    # --------------------------------------------------------------------------
    # PART 5: SAARE ALGORITHMS KA BACCHA-LEVEL POSTMORTEM (UNITS 3 & 4)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 5: TERE SAARE ALGORITHMS KA '2-SAAL KE BACCHE WALA' EXPLANATION",
        page_break=True,
    )

    story.append(
        Paragraph("<b>SUPERVISED CLASSIFICATION MODELS (UNIT 3)</b>", ST["SubHdr"])
    )

    add_concept_card(
        story,
        "Model 1: K-Nearest Neighbors (KNN, k = 5) -> Accuracy: 85.23% | Macro F1: 0.7886",
        "Kahawat suni hai: <i>'Tumhara dost kaun hai batao, main bataunga tum kaun ho!'</i> KNN bilkul yahi karta hai! Jab koi nayi train aati hai, toh KNN graph par dekhta hai ki is train ke <b>sabse kareeb 5 padosi (k=5 nearest neighbors)</b> kaunse hain (Euclidean distance naap kar). Agar 5 padosiyon mein se 4 Superfast hain aur 1 Express hai, toh Majority Vote se nayi train ko bhi Superfast ghoshit kar deta hai!",
        "Humne k=5 rakha aur StandardScaler lagaya (kyunki bina scaling ke distance naapna galat ho jaata). Accuracy 85.23% aur ROC-AUC sabse best (0.9355) aaya.",
        "Sir, KNN is a distance-based lazy learner that classifies a train by taking a majority vote among its k=5 closest neighbors using Euclidean distance on scaled features.",
    )

    add_concept_card(
        story,
        "Model 2: Decision Tree Classifier (WINNER) -> Accuracy: 91.50% | Macro F1: 0.8896",
        "Bachpan mein 'Yes / No' wala 20-Questions game khela hai? Decision Tree bilkul waisa hi ulta ped (Tree) banata hai! <br/>&bull; <b>Sawaal 1 (Root Node):</b> Kya is train mein 3AC dabba (`third_ac`) laga hai? (Agar Nahi -> Toh 97% chance hai yeh Passenger train hai!). <br/>&bull; <b>Sawaal 2:</b> Agar Haan -> Toh kya iski `distance` aur `total_duration` lambi hai? <br/>Aise hi Gini Impurity check karke yeh Yes/No ke rules banata jaata hai!",
        "<b>Yeh WINNER kyun bana?</b> Kyunki Indian Railways khud asliyat mein aise hi rules se train ka naam rakhti hai! Isko scaling ki bhi zaroorat nahi hoti. Top 5 features: 1. third_ac (35.5%), 2. distance (22.3%), 3. total_duration (18.0%), 4. chair_car (11.8%), 5. first_ac (1.3%).",
        "Sir, Decision Tree won with 91.50% accuracy and 0.8896 Macro F1 because railway service tiers naturally follow hierarchical threshold rules on AC coaches, distance, and duration.",
    )

    add_concept_card(
        story,
        "Model 3: Gaussian Naive Bayes (FLOP MODEL) -> Accuracy: 37.02% | Macro F1: 0.3098",
        "Angrezi mein <b>'Naive' ka matlab hota hai 'Bhola-Bhala / Buddhu'!</b> Is model ko Naive isliye bolte hain kyunki yeh ekdum bhola assumption maanta hai ki saare 26 features ka aapas mein koi rishta (correlation) nahi hai! Yaani yeh maanta hai ki Train ki Distance, Train ka Time (`total_duration`), aur AC/Sleeper dabbo ka aapas mein koi lena-dena hi nahi hai! Jabki humein pata hai ki lambi duri wali train mein hi zyada time lagta hai (`r = 0.98`) aur usi mein Sleeper + 3AC dono hote hain (`r = 0.86`). Is bholepan ki wajah se yeh model buri tarah fail ho gaya!",
        "Accuracy sirf 37.02% aayi (Dummy Baseline 55% se bhi kam!). Yeh prove karta hai ki jab features correlated hon, tab Naive Bayes nahi lagana chahiye.",
        "Sir, Gaussian Naive Bayes failed (37.02% accuracy) because its core conditional independence assumption is heavily violated by strong correlations between distance, duration (r=0.98), and AC coaches.",
    )

    add_concept_card(
        story,
        "Model 4: Support Vector Machine (SVM - RBF Kernel) -> Accuracy: 84.12% | Macro F1: 0.7651",
        "Soch zameen par laal aur neeli gendein (balls) bikhri padi hain. SVM ek aisa Traffic Police hai jo dono rang ki gendon ke beech ek <b>sabse chauda Road / Divider (Maximum-Margin Hyperplane)</b> khinchta hai taaki dono classes ek dusre se zyada se zyada dur rahein! Aur jab gendein aapas mein ghul-mil jaayein (non-linear), tab <b>RBF Kernel</b> chadar ko 3D mein upar utha kar unko kaat deta hai!",
        "Scaled data par RBF kernel ke saath SVM ne 84.12% Accuracy, 0.7651 Macro F1 aur 0.9285 ROC-AUC diya.",
        "Sir, SVM with an RBF kernel maps our scaled 26-dimensional features into a higher-dimensional space to find the maximum-margin hyperplane separating the train classes.",
    )

    story.append(
        Paragraph("<b>UNSUPERVISED CLUSTERING ALGORITHMS (UNIT 4)</b>", ST["SubHdr"])
    )

    add_concept_card(
        story,
        "Clustering 1: K-Means (k = 5) + Elbow Method + Silhouette (0.2024) + PCA",
        "<b>K-Means kaise kaam karta hai?</b> Humne train ke Pass/Exp/SF labels chhupa diye aur computer ko bola: <i>'3,572 trains ke 5 group (k=5) bana ke dikha!'</i> K-Means मैदान mein 5 Chumbak (Centroids) phenkta hai. Har train apne sabse kareebi chumbak se chipak jaati hai, aur 5 group ban jaate hain!<br/>"
        "&bull; <b>Elbow Method kya hai?</b> Humein kaise pata chala ki 5 hi group banane hain? Humne k=2 se k=10 tak graph banaya. Jahan haath ki <b>Kohni (Elbow)</b> jaisa mod aaya (k=5 par, Inertia = 69,115.75), wahi best number hai!<br/>"
        "&bull; <b>PCA (Principal Component Analysis) kya hai?</b> Insaan ki aankh 26 columns (26D) ka graph nahi dekh sakti. PCA 26 columns ko निचोड़ kar 2D photo (X aur Y axis) mein badal deta hai taaki hum 5 rang ke clusters dekh sakein!",
        "5 Clusters mile: C-0 (Eastern Railway Regional), C-1 (Northeast Frontier Hilly Mixed), C-2 (Short-Distance Local Pass), C-3 (Long-Distance AC Premium VIP Fleet), C-4 (Secondary-Zone Branch Pass).",
        "Sir, using the Elbow Method we selected k=5 for K-Means, achieving an Inertia of 69,115.75 and a Silhouette Score of 0.2024, which we visualized in 2D using PCA.",
    )

    add_concept_card(
        story,
        "Clustering 2: DBSCAN (eps=7.0, min_samples=20) -> Silhouette: 0.2543 (Beats K-Means!)",
        "<b>K-Means ki kami kya thi?</b> K-Means zabardasti har ajeeb train ko bhi kisi na kisi group mein ghusa deta hai. <br/><b>DBSCAN kya karta hai?</b> Yeh <b>Bheed (Density)</b> dekhta hai! Yeh kehta hai ki agar 7.0 ke ghere (`eps=7.0`) mein kam se kam 20 trains (`min_samples=20`) ikattha hain, toh unka group banao. Aur jo trains bheed se bilkul alag-thalag akeli khadi hain, unko <b>Noise / Outlier (-1)</b> ghoshit kar do!",
        "DBSCAN ko k batana nahi pada — usne khud <b>4 natural clusters</b> dhoondhe, <b>13 ajeeb trains (0.4% noise)</b> ko alag pakda, aur iska <b>Silhouette Score (0.2543)</b> K-Means (0.2024) se bhi behtar aaya!",
        "Sir, DBSCAN is a density-based algorithm that automatically discovered 4 clusters, isolated 13 anomalous trains (0.4% noise), and achieved a higher Silhouette Score of 0.2543 than K-Means.",
    )

    add_concept_card(
        story,
        "Silhouette Score Kya Hota Hai? (0.2024 vs 0.2543)",
        "Clustering mein koi answer key toh hoti nahi, toh kaise check karein ki groups acche bane hain ya kharab? <b>Silhouette Score (-1 se +1)</b> naapta hai ki ek group ke andar ke log aapas mein kitne kareeb hain (Cohesion) aur dusre group se kitne dur hain (Separation). Plus (+) mein jitna zyada ho, utna accha!",
        "Duration fix ke baad K-Means ka Silhouette 0.1755 se badh kar 0.2024 ho gaya, aur DBSCAN ka 0.2543 aaya.",
        "Sir, Silhouette Score measures intra-cluster cohesion versus inter-cluster separation on a scale of -1 to +1.",
    )

    # --------------------------------------------------------------------------
    # PART 6: 35 ULTIMATE VIVA QUESTIONS & ANSWERS (DIRECT EXAMINER PREP)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 6: 35 LOCKED VIVA QUESTIONS & ANSWERS (EXAMINER JO POOCHEGA)",
        page_break=True,
    )

    qas = [
        (
            1,
            "What is your project title and why did you choose Indian Railways?",
            "Project ka naam aur Indian Railways hi kyun chuna?",
            "Sir, my project is 'Classification and Clustering of Indian Railway Trains Using Machine Learning'. Indian Railways runs over 13,000 trains across 19 zones, generating massive schedule data. Manual categorization is inconsistent, so ML is ideal to automate tier classification and discover hidden fleet patterns.",
        ),
        (
            2,
            "Which dataset did you use? How many rows and columns are there?",
            "Data kahan se liya, kitni rows thi aur kitni bachi?",
            "Sir, we used the Indian Railways Dataset by Sripaad Srinivasan from Kaggle. The raw GeoJSON file (trains.json, 14.08 MB) had 5,208 records. After converting to trains.csv (636 KB) and filtering to the 3 major classes (Pass, Exp, SF), we have 4,466 rows and 26 engineered features.",
        ),
        (
            3,
            "What are the three target classes and their exact percentages?",
            "Teeno classes ka naam aur unka hissa (percentage) kya hai?",
            "Sir, the 3 target classes are: Passenger (Pass) with 2,459 trains (55.06%), Express (Exp) with 1,288 trains (28.84%), and Superfast (SF) with 719 trains (16.10%).",
        ),
        (
            4,
            "Your dataset is imbalanced (55% vs 16%). How did you handle class imbalance?",
            "Passenger 55% hai aur Superfast sirf 16% — is bhedbhav ko kaise sambhala?",
            "Sir, we handled moderate class imbalance in two ways: First, we used stratified train-test splitting (stratify=y) so both train and test sets keep the exact same class ratios. Second, we selected Macro-Averaged F1 as our primary evaluation metric instead of raw Accuracy, because Macro F1 gives equal 1/3 weight to all three classes.",
        ),
        (
            5,
            "What was the biggest data quality bug in your dataset and how did you fix it?",
            "KILLER QUESTION: duration_m wala bug kya tha aur kaise theek kiya?",
            "Sir, the duration_m column stored only the minute remainder (0 to 58 minutes) instead of total journey minutes. For example, a 24-hour 0-minute train had duration_m = 0. We fixed this by engineering total_duration = (duration_h * 60) + duration_m and dropping the raw columns. This single fix improved all 5 supervised models and clustering silhouette score!",
        ),
        (
            6,
            "Why did you drop the 'name' and 'number' columns?",
            "Train ka naam aur train number kyun hata diya?",
            "Sir, train number and train name are unique identifiers with high cardinality. Including them would cause the model to memorize specific train IDs (overfitting) rather than learning general operational rules.",
        ),
        (
            7,
            "What is a Constant Column Audit and why did you perform it?",
            "Constant column audit kya hota hai?",
            "Sir, before encoding, we checked if any feature had zero variance (only 1 unique value across all rows). A constant column carries zero predictive information. Our audit confirmed all coach indicators (1AC, 2AC, 3AC, Sleeper, Chair Car, First Class) had valid variance.",
        ),
        (
            8,
            "What is Data Leakage and how did you prevent it in your notebook?",
            "Paper leak (Data Leakage) kya hota hai aur tune kaise roka?",
            "Sir, data leakage happens when information from the test set leaks into model training — for example, fitting StandardScaler on the full dataset before splitting. We prevented it by splitting the data first (80/20) and calling scaler.fit_transform() strictly on X_train, and only scaler.transform() on X_test.",
        ),
        (
            9,
            "Why is feature scaling (StandardScaler) needed for KNN and SVM, but NOT for Decision Tree?",
            "KNN aur SVM ko scaling kyun chahiye par Decision Tree ko kyun nahi?",
            "Sir, KNN and SVM calculate Euclidean distances between points. Without StandardScaler, a large feature like distance (up to 4,000 km) completely dominates binary coach columns (0 or 1). Decision Tree, however, splits one feature at a time using threshold rules (e.g., distance > 300), so it is scale-invariant.",
        ),
        (
            10,
            "Why did you include a Dummy Classifier in your project?",
            "Dummy baseline model (55.03%) kyun banaya?",
            "Sir, DummyClassifier(strategy='most_frequent') predicts the majority class (Passenger) for every row, giving 55.03% accuracy and 0.2367 Macro F1. It acts as our benchmark floor — any real ML model must beat this baseline to prove it has actually learned patterns.",
        ),
        (
            11,
            "Which model performed the best and WHY did it win?",
            "Sabse best model kaunsa raha aur wahi kyun jeeta?",
            "Sir, the default Decision Tree Classifier won with 91.50% Accuracy, 0.8896 Macro F1, and 0.9146 Weighted F1. It won because Indian Railways classifies trains using hierarchical rule thresholds (such as 3AC coach presence, distance, and duration), which axis-aligned tree splits capture naturally.",
        ),
        (
            12,
            "Why did pruning the Decision Tree to max_depth=10 reduce accuracy from 91.50% to 88.59%?",
            "Jab Decision Tree ki depth 10 par roki toh score kam kyun ho gaya?",
            "Sir, with 26 features including 19 one-hot encoded railway zones, valid zone-specific schedule exceptions sit deeper in the tree. Pruning at max_depth=10 cut off those valid leaf rules, lowering Macro F1 from 0.8896 to 0.8459. And our 5-fold CV (0.8743) proved the default tree wasn't overfitting.",
        ),
        (
            13,
            "Why did Gaussian Naive Bayes fail so badly (37.02% accuracy)?",
            "Naive Bayes itna bura flop (37.02%) kyun hua?",
            "Sir, Gaussian Naive Bayes assumes all features are conditionally independent and normally distributed. In our dataset, distance and total_duration have a 0.98 correlation, and third_ac and sleeper have a 0.86 correlation. Because the independence assumption is heavily violated, Naive Bayes double-counts correlated features and fails.",
        ),
        (
            14,
            "What are the Top 5 most important features in your Decision Tree?",
            "Decision Tree ne kin 5 features ko sabse zyada importance di?",
            "Sir, based on Gini feature importance: 1st is third_ac (35.51%), 2nd is distance (22.26%), 3rd is our engineered total_duration (17.99%), 4th is chair_car (11.81%), and 5th is first_ac (1.33%). Together, the top 4 features account for 87.57% of the decision power.",
        ),
        (
            15,
            "Explain your Confusion Matrix and Error Analysis results.",
            "8.50% galti kahan hui aur kaunsi trains mein confusion hua?",
            "Sir, out of 894 test trains, our overall error rate is 8.50%. Per-class error rates are only 3.0% for Passenger, 14.0% for Express, and 17.4% for Superfast. Zero Superfast trains were misclassified as Passenger. The main confusion is between SF and Exp (25 SF->Exp, 16 Exp->SF) because medium-distance Express and Superfast trains share identical AC/Sleeper coaches.",
        ),
        (
            16,
            "Decision Tree won on F1-score, so why does KNN have a slightly higher ROC-AUC (0.9355 vs 0.9204)?",
            "ROC-AUC mein KNN (0.9355) Decision Tree (0.9204) se thoda aage kyun hai?",
            "Sir, ROC-AUC measures probability ranking across all thresholds. KNN averages over 5 neighbors and SVM (0.9285) uses smooth margin distances, giving smoother probability curves. Decision Tree has pure leaf nodes (0 or 1 probabilities), which gives the sharpest hard classification (91.50% accuracy) even if the ROC curve has fewer stepped thresholds.",
        ),
        (
            17,
            "How did you choose k = 5 in K-Means clustering?",
            "K-Means mein 5 hi clusters kyun banaye?",
            "Sir, we plotted the Within-Cluster Sum of Squares (Inertia) for k = 2 to 10 using the Elbow Method. The curve showed a clear elbow inflection at k = 5 with an Inertia of 69,115.75 and a Silhouette Score of 0.2024.",
        ),
        (
            18,
            "What is the difference between K-Means and DBSCAN in your results?",
            "K-Means aur DBSCAN mein kya farak aaya?",
            "Sir, K-Means is centroid-based, required us to specify k=5, forced all points into spherical clusters, and gave a 0.2024 Silhouette score. DBSCAN (eps=7.0, min_samples=20) is density-based, automatically discovered 4 natural clusters, isolated 13 anomalous trains (0.4% noise), and achieved a better Silhouette score of 0.2543.",
        ),
        (
            19,
            "What do your 5 K-Means clusters represent in real-world Indian Railways?",
            "K-Means ke 5 clusters (C-0 se C-4) ka asli railway mein kya matlab hai?",
            "Sir, C-0 is the Eastern Railway (ER) Regional Network, C-1 is Northeast Frontier (NFR) Mixed Hilly Operations, C-2 is Short-Distance Unreserved Commuter Passenger trains, C-3 is Long-Distance AC Premium Flagship Express/Superfast trains, and C-4 is Secondary-Zone Short Branch-Line Passenger feeders.",
        ),
        (
            20,
            "Why did you use PCA in Phase 4?",
            "PCA (Principal Component Analysis) kyun lagaya?",
            "Sir, our dataset has 26 dimensions, which cannot be plotted directly on a 2D screen. We used PCA to project the 26-dimensional scaled features onto 2 Principal Components (PC1 and PC2) so we could visually inspect the K-Means and DBSCAN clusters.",
        ),
        (
            21,
            "Why did you skip Linear Regression and Apriori from the syllabus?",
            "Syllabus mein Linear Regression aur Apriori bhi hai, woh kyun nahi lagaya?",
            "Sir, Linear Regression predicts continuous numerical values (like house price), whereas our target variable is categorical (Pass, Exp, SF) — so classification is mathematically required. Similarly, Apriori is for transactional market-basket data (like grocery bills), whereas our dataset has fixed operational attributes per train — so K-Means and DBSCAN were used for pattern discovery.",
        ),
        (
            22,
            "Which IDE/Tool did you use? Why not Anaconda? Is your project reproducible?",
            "Kaunsa software use kiya aur dusre computer par kaise chalega?",
            "Sir, I used VS Code with the official Python 3.13.6 and Jupyter extensions. Instead of heavy Anaconda, I used standard Python with pip and requirements.txt for a lighter setup. The .ipynb notebooks and trains.csv are standard formats that run anywhere (VS Code, Jupyter, Colab) top-to-bottom.",
        ),
        (
            23,
            "How does your project connect to Artificial Intelligence (DSC-C-BCA-471T)?",
            "Agar AI subject (471T) ka examiner pooche ki isme AI kahan hai?",
            "Sir, from our AI course (471T), our trained Decision Tree acts as a Rational Knowledge-Based Agent: it perceives the train's environment state (26 operational features) and applies learned logical inference rules (if-then tree paths) to take the optimal classification action.",
        ),
    ]

    for q_num, q_txt, sim_txt, ans_txt in qas:
        add_qa_card(story, q_num, q_txt, sim_txt, ans_txt)

    # --------------------------------------------------------------------------
    # PART 7: 1-PAGE LAST-MINUTE CHEAT SHEET (EXAM HALL REVISION)
    # --------------------------------------------------------------------------
    add_section_banner(
        story,
        "PART 7: 2-MINUTE EXAM HALL CHEAT SHEET (SAARE LOCKED NUMBERS EK JAGAH)",
        page_break=True,
    )

    cheat_rows = [
        ("Raw vs Filtered Dataset", "5,208 raw (trains.json 14.08 MB) -> 4,466 filtered (trains.csv 636 KB)"),
        ("3 Target Classes (y)", "Pass: 2,459 (55.06%) | Exp: 1,288 (28.84%) | SF: 719 (16.10%)"),
        ("Total Features (X)", "26 Features (distance, total_duration, 5 coach binaries + 19 one-hot zones)"),
        ("Train / Test Split (80/20)", "Training: 3,572 trains (80%) | Testing: 894 trains (20%) | random_state=42"),
        ("Killer Data Quality Fix", "total_duration = (duration_h * 60) + duration_m (Improved ALL 5 models!)"),
        ("Top Correlation Pairs", "Distance <-> Duration: r = 0.98 | 3AC <-> Sleeper: r = 0.86 | 2AC <-> Sleeper: r = 0.79"),
        ("Dummy Baseline Score", "Accuracy: 55.03% (0.5503) | Macro F1: 0.2367 | Weighted F1: 0.3907"),
        ("KNN (k=5) Score", "Accuracy: 85.23% (0.8523) | Macro F1: 0.7886 | Mean ROC-AUC: 0.9355 (Best AUC)"),
        ("Decision Tree (WINNER)", "Accuracy: 91.50% (0.9150) | Macro F1: 0.8896 | Weighted F1: 0.9146 | Micro: 0.9150"),
        ("Decision Tree (Depth=10)", "Accuracy: 88.59% (0.8859) | Macro F1: 0.8459 | Weighted F1: 0.8836"),
        ("Gaussian Naive Bayes", "Accuracy: 37.02% (0.3702) | Macro F1: 0.3098 (Failed due to correlated features)"),
        ("SVM (RBF Kernel)", "Accuracy: 84.12% (0.8412) | Macro F1: 0.7651 | Mean ROC-AUC: 0.9285"),
        ("5-Fold Cross Validation", "Decision Tree Mean Macro F1 = 0.8743 +/- 0.0155 (Proves zero overfitting)"),
        ("Top 5 DT Features", "1. third_ac (0.3551) | 2. distance (0.2226) | 3. total_duration (0.1799) | 4. chair_car (0.1181) | 5. first_ac (0.0133)"),
        ("Error Analysis Breakdown", "Overall Error: 8.50% | Pass: 3.0%, Exp: 14.0%, SF: 17.4% | 25 SF->Exp, 16 Exp->SF"),
        ("K-Means Clustering (k=5)", "Inertia: 69,115.75 | Silhouette: 0.2024 (up from 0.1755) | 5 Fleet Archetypes"),
        ("DBSCAN Clustering", "eps=7.0, min_samples=20 | 4 Natural Clusters | 0.4% Noise (13 points) | Silhouette: 0.2543"),
        ("Saved Output Artifacts", "data/trains_with_clusters.csv (3,572 x 28) | models/scaler.joblib & dt_classifier.joblib"),
    ]
    add_data_table(
        story,
        ["Viva Checkpoint", "Exact Verified Number / Formula To Speak"],
        cheat_rows,
        [2.1 * inch, 4.9 * inch],
    )

    add_callout_box(
        story,
        "FINAL CONFIDENCE BOOSTER FOR PRINCE:",
        [
            "Bhai, agar viva mein koi aisa tedha sawaal aa jaaye jiska exact technical word us second yaad na aaye, "
            "toh bilkul chup mat baithna! Seedha apna <b>Brahmastra (Killer Point)</b> chala dena: <br/>"
            "<i>\"Sir, jab humne dataset explore kiya toh dekha ki duration_m column mein sirf 0 se 58 tak minute remainder tha. "
            "Humne total_duration = (duration_h * 60) + duration_m engineer kiya, jisse Decision Tree ka F1-score 0.8309 se "
            "0.8896 aur Accuracy 91.50% pahunch gayi, aur third_ac (35.5%), distance (22.3%), aur total_duration (18.0%) "
            "top predictors nikle!\"</i> <br/>"
            "Yeh line sunte hi examiner samajh jayega ki tune khud data ke andar ghus kar kaam kiya hai!"
        ],
        C_GREEN_BG,
        C_GREEN_BDR,
    )

    # Build PDF with PermissionError fallback
    try:
        doc = SimpleDocTemplate(
            out_path,
            pagesize=A4,
            leftMargin=0.6 * inch,
            rightMargin=0.6 * inch,
            topMargin=0.55 * inch,
            bottomMargin=0.7 * inch,
            title="Prince Viva Master Guide - Indian Railways ML",
            author="Rajput Prince Singh (Roll No. 83)",
        )
        doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
        saved = out_path
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved = os.path.join(REPORTS_DIR, f"Prince_Viva_Master_Guide_{ts}.pdf")
        doc = SimpleDocTemplate(
            saved,
            pagesize=A4,
            leftMargin=0.6 * inch,
            rightMargin=0.6 * inch,
            topMargin=0.55 * inch,
            bottomMargin=0.7 * inch,
            title="Prince Viva Master Guide - Indian Railways ML",
            author="Rajput Prince Singh (Roll No. 83)",
        )
        doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)

    return saved


if __name__ == "__main__":
    print("=" * 72)
    print("GENERATING PRINCE'S HINGLISH VIVA MASTER GUIDE PDF...")
    print("=" * 72)
    pdf_file = build_viva_pdf()
    print(f"[SUCCESS] Viva Guide PDF ready at: {pdf_file}")
    print("=" * 72)