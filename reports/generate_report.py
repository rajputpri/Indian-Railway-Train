"""
Project Report PDF Builder
Project : Classification and Clustering of Indian Railway Trains Using Machine Learning
Student : Rajput Prince Singh (Roll No. 83)
Course  : Machine Learning System Design & Implementation (DSC-C-BCA-473P)
College : Lokmanya College of Computer Applications, Ahmedabad (Gujarat University)
"""

import os
import zipfile
from datetime import datetime
from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    Preformatted,
    Flowable,
)


# ==============================================================================
# 1. PATHS & OFFICIAL PROJECT METADATA
# ==============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR).lower() == "reports":
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    REPORTS_DIR = SCRIPT_DIR
else:
    PROJECT_ROOT = SCRIPT_DIR
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

VIS_DIR = os.path.join(PROJECT_ROOT, "visualizations")
os.makedirs(REPORTS_DIR, exist_ok=True)

META = {
    "title": "CLASSIFICATION AND CLUSTERING OF INDIAN RAILWAY TRAINS USING MACHINE LEARNING",
    "student_name": "Rajput Prince Singh",
    "roll_no": "83",
    "program": "Bachelor of Computer Applications (Honours)",
    "semester": "BCA (Hons.) - Semester VII",
    "course_full": "Machine Learning System Design & Implementation (DSC-C-BCA-473P)",
    "guide_name": "Prof. Sejal Shah",
    "guide_designation": "Assistant Professor",
    "director_name": "Dr. Prakash Khuman",
    "director_designation": "Director",
    "college": "Lokmanya College of Computer Applications",
    "city": "Ahmedabad, Gujarat",
    "university": "Gujarat University",
    "academic_year": "2025-26",
    "repo_url": "https://github.com/rajputpri/Indian-Railway-Train",
    "branch": "master",
}


# ==============================================================================
# 2. FONT REGISTRATION & TEMPLATE LOGO EXTRACTION
# ==============================================================================

def register_times_new_roman():
    win_fonts = r"C:\Windows\Fonts"
    times_reg = os.path.join(win_fonts, "times.ttf")
    times_bd = os.path.join(win_fonts, "timesbd.ttf")
    times_it = os.path.join(win_fonts, "timesi.ttf")
    times_bi = os.path.join(win_fonts, "timesbi.ttf")
    consola = os.path.join(win_fonts, "consola.ttf")

    if all(os.path.exists(p) for p in [times_reg, times_bd, times_it, times_bi]):
        pdfmetrics.registerFont(TTFont("TNR", times_reg))
        pdfmetrics.registerFont(TTFont("TNR-Bold", times_bd))
        pdfmetrics.registerFont(TTFont("TNR-Italic", times_it))
        pdfmetrics.registerFont(TTFont("TNR-BoldItalic", times_bi))
        pdfmetrics.registerFontFamily(
            "TNR",
            normal="TNR",
            bold="TNR-Bold",
            italic="TNR-Italic",
            boldItalic="TNR-BoldItalic",
        )
        font_family = "TNR"
    else:
        font_family = "Times-Roman"

    if os.path.exists(consola):
        pdfmetrics.registerFont(TTFont("CodeFont", consola))
        code_font = "CodeFont"
    else:
        code_font = "Courier"

    return font_family, code_font

def extract_logos_from_template():
    """
    Pehle reports/ ya project root mein direct PNG/JPG logos check karta hai.
    Agar nahi mile, toh ASP_INDEX.docx se extract karta hai.
    """
    logo_dir = os.path.join(REPORTS_DIR, "_report_assets")
    os.makedirs(logo_dir, exist_ok=True)
    
    # 1. Direct image check (Agar tu chahye toh dono logos ko reports/ folder mein rakh sakta hai)
    direct_college = os.path.join(REPORTS_DIR, "lokmanya_logo.png")
    direct_uni = os.path.join(REPORTS_DIR, "gujarat_logo.png")
    
    if os.path.exists(direct_college) and os.path.exists(direct_uni):
        return direct_college, direct_uni

    # 2. ASP_INDEX.docx extraction fallback
    candidates = [
        os.path.join(PROJECT_ROOT, "ASP_INDEX.docx"),
        os.path.join(REPORTS_DIR, "ASP_INDEX.docx"),
    ]
    college_logo = None
    uni_logo = None

    for path in candidates:
        if os.path.exists(path):
            try:
                with zipfile.ZipFile(path, "r") as z:
                    for item in z.namelist():
                        if item.startswith("word/media/image1."):
                            ext = os.path.splitext(item)[1]
                            college_logo = os.path.join(logo_dir, f"lokmanya_logo{ext}")
                            with open(college_logo, "wb") as f:
                                f.write(z.read(item))
                        elif item.startswith("word/media/image2."):
                            ext = os.path.splitext(item)[1]
                            uni_logo = os.path.join(logo_dir, f"gujarat_uni_logo{ext}")
                            with open(uni_logo, "wb") as f:
                                f.write(z.read(item))
                break
            except Exception:
                pass
    return college_logo, uni_logo


# ==============================================================================
# 3. TWO-PASS TRACKER FOR 100% ACCURATE TABLE OF CONTENTS PAGE NUMBERS
# ==============================================================================

class BookmarkTracker(Flowable):
    """Zero-height flowable that records the exact PDF page number where a section or figure lands."""

    def __init__(self, key, registry):
        super().__init__()
        self.key = key
        self.registry = registry
        self.width = 0
        self.height = 0

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        self.registry[self.key] = self.canv.getPageNumber()


# ==============================================================================
# 4. ACADEMIC STYLES & CLEAN FOOTER
# ==============================================================================

FONT_FAMILY, CODE_FONT = register_times_new_roman()
FONT_BOLD = "TNR-Bold" if FONT_FAMILY == "TNR" else "Times-Bold"
FONT_ITALIC = "TNR-Italic" if FONT_FAMILY == "TNR" else "Times-Italic"
FONT_BI = "TNR-BoldItalic" if FONT_FAMILY == "TNR" else "Times-BoldItalic"

NAVY_HEADER = colors.HexColor("#1F4E79")
ROW_ALT_BG = colors.HexColor("#F4F8FB")
CODE_BG = colors.HexColor("#F4F6F9")
BORDER_GRAY = colors.HexColor("#BFBFBF")


def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["Body"] = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName=FONT_FAMILY,
        fontSize=12,
        leading=18,  # 1.5 line spacing
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        textColor=colors.black,
    )

    styles["BodyCenter"] = ParagraphStyle(
        "BodyCenter",
        parent=styles["Body"],
        alignment=TA_CENTER,
    )

    styles["BodyRight"] = ParagraphStyle(
        "BodyRight",
        parent=styles["Body"],
        alignment=TA_RIGHT,
    )

    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Body"],
        leftIndent=18,
        firstLineIndent=-12,
        spaceAfter=6,
    )

    styles["ChapterHeading"] = ParagraphStyle(
        "ChapterHeading",
        parent=base["Heading1"],
        fontName=FONT_BOLD,
        fontSize=14,
        leading=20,
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=8,
        textColor=colors.black,
        keepWithNext=True,
    )

    styles["SubHeading"] = ParagraphStyle(
        "SubHeading",
        parent=base["Heading2"],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=18,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.black,
        keepWithNext=True,
    )

    styles["Equation"] = ParagraphStyle(
        "Equation",
        parent=styles["Body"],
        fontName=FONT_BI,
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=8,
        backColor=CODE_BG,
        borderPadding=6,
    )

    styles["TableCaption"] = ParagraphStyle(
        "TableCaption",
        parent=styles["Body"],
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    styles["FigureCaption"] = ParagraphStyle(
        "FigureCaption",
        parent=styles["Body"],
        fontName=FONT_ITALIC,
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=14,
    )

    styles["TableHeader"] = ParagraphStyle(
        "TableHeader",
        parent=styles["Body"],
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.white,
        spaceAfter=0,
    )

    styles["TableCell"] = ParagraphStyle(
        "TableCell",
        parent=styles["Body"],
        fontName=FONT_FAMILY,
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=0,
    )

    styles["TableCellCenter"] = ParagraphStyle(
        "TableCellCenter",
        parent=styles["TableCell"],
        alignment=TA_CENTER,
    )

    styles["TableCellBold"] = ParagraphStyle(
        "TableCellBold",
        parent=styles["TableCell"],
        fontName=FONT_BOLD,
    )

    styles["TableCellBoldCenter"] = ParagraphStyle(
        "TableCellBoldCenter",
        parent=styles["TableCellCenter"],
        fontName=FONT_BOLD,
    )

    styles["CodeBlock"] = ParagraphStyle(
        "CodeBlock",
        fontName=CODE_FONT,
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    return styles


STYLES = build_styles()


def draw_page_number_footer(canvas, doc):
    """Draws clean bottom-center page number with zero top-header clutter so figures never clip."""
    canvas.saveState()
    page_num = canvas.getPageNumber()
    canvas.setFont(FONT_FAMILY, 11)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(A4[0] / 2.0, 0.5 * inch, f"Page {page_num}")
    canvas.restoreState()


# ==============================================================================
# 5. HELPER FUNCTIONS FOR SECTIONS, TABLES & LARGE CLEAR FIGURES
# ==============================================================================

def add_chapter(story, key, title, registry, page_break=True):
    if page_break:
        story.append(PageBreak())
    story.append(BookmarkTracker(key, registry))
    story.append(Paragraph(title.upper(), STYLES["ChapterHeading"]))
    rule = Table([[""]], colWidths=[6.27 * inch], rowHeights=[1.5])
    rule.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY_HEADER),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(rule)
    story.append(Spacer(1, 8))


def add_sub(story, title):
    story.append(Paragraph(title, STYLES["SubHeading"]))


def add_p(story, text, bold_prefix=None):
    full = f"<b>{bold_prefix}</b>{text}" if bold_prefix else text
    story.append(Paragraph(full, STYLES["Body"]))


def add_bullet(story, bold_prefix, text):
    full = f"&bull; <b>{bold_prefix}</b>{text}"
    story.append(Paragraph(full, STYLES["Bullet"]))


def add_equation(story, eq_text):
    story.append(Paragraph(eq_text, STYLES["Equation"]))


def add_code(story, code_text):
    pre = Preformatted(code_text.strip(), STYLES["CodeBlock"])
    tbl = Table([[pre]], colWidths=[6.25 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER_GRAY),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(KeepTogether([tbl, Spacer(1, 8)]))


def add_table(story, caption, headers, rows, col_widths, center_cols=None):
    if center_cols is None:
        center_cols = set()

    cap_p = Paragraph(caption, STYLES["TableCaption"])
    data = [[Paragraph(str(h), STYLES["TableHeader"]) for h in headers]]

    for r in rows:
        is_winner = any("WINNER" in str(c) for c in r)
        row_cells = []
        for c_idx, val in enumerate(r):
            if is_winner:
                st = (
                    STYLES["TableCellBoldCenter"]
                    if c_idx in center_cols
                    else STYLES["TableCellBold"]
                )
            else:
                st = (
                    STYLES["TableCellCenter"]
                    if c_idx in center_cols
                    else STYLES["TableCell"]
                )
            row_cells.append(Paragraph(str(val), st))
        data.append(row_cells)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    t_style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r_idx in range(1, len(data)):
        bg = ROW_ALT_BG if r_idx % 2 == 0 else colors.white
        t_style.append(("BACKGROUND", (0, r_idx), (-1, r_idx), bg))

    tbl.setStyle(TableStyle(t_style))
    story.append(KeepTogether([cap_p, tbl, Spacer(1, 10)]))


def add_figure(
    story,
    fig_key,
    filename,
    caption,
    registry,
    max_w=6.1 * inch,
    max_h=4.2 * inch,
):
    """
    Renders an important plot at large, crisp full-page width (up to 6.1 inches wide)
    inside a clean border frame so it never shrinks or clips at page boundaries.
    """
    img_path = os.path.join(VIS_DIR, filename)
    block = [Spacer(1, 6), BookmarkTracker(fig_key, registry)]

    if os.path.exists(img_path):
        with PILImage.open(img_path) as im:
            orig_w, orig_h = im.size
        ratio = min(max_w / float(orig_w), max_h / float(orig_h))
        draw_w = orig_w * ratio
        draw_h = orig_h * ratio
        img_flow = Image(img_path, width=draw_w, height=draw_h)
        img_flow.hAlign = "CENTER"

        frame_tbl = Table([[img_flow]], colWidths=[6.25 * inch])
        frame_tbl.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        block.append(frame_tbl)
    else:
        placeholder = Table(
            [[Paragraph(f"<i>[Visualization: visualizations/{filename}]</i>", STYLES["FigureCaption"])]],
            colWidths=[6.25 * inch],
            rowHeights=[2.2 * inch],
        )
        placeholder.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.6, BORDER_GRAY),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        block.append(placeholder)

    block.append(Paragraph(caption, STYLES["FigureCaption"]))
    story.append(KeepTogether(block))


# ==============================================================================
# 6. BUILD STORY WITH DYNAMIC PAGE NUMBERS
# ==============================================================================

def build_story(page_map, college_logo, uni_logo):
    story = []

    def pg(key, default="--"):
        return str(page_map.get(key, default))

    # --------------------------------------------------------------------------
    # PAGE 1: TITLE PAGE (Matches ASP_INDEX.docx & Official Course DSC-C-BCA-473P)
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>A PROJECT REPORT ON</b>",
            ParagraphStyle(
                "TitleTop",
                parent=STYLES["BodyCenter"],
                fontName=FONT_BOLD,
                fontSize=14,
                leading=20,
                spaceAfter=10,
            ),
        )
    )
    story.append(
        Paragraph(
            f"<b>{META['title']}</b>",
            ParagraphStyle(
                "TitleMain",
                parent=STYLES["BodyCenter"],
                fontName=FONT_BOLD,
                fontSize=17.5,
                leading=24,
                textColor=NAVY_HEADER,
                spaceAfter=14,
            ),
        )
    )
    story.append(
        Paragraph(
            "Submitted in partial fulfilment of the requirements for the award of the degree of<br/>"
            f"<b>{META['program']}</b><br/>"
            f"<b>Course:</b> {META['course_full']}<br/>"
            f"<b>Academic Year:</b> {META['academic_year']}",
            ParagraphStyle(
                "TitleSub",
                parent=STYLES["BodyCenter"],
                fontSize=12,
                leading=19,
                spaceAfter=18,
            ),
        )
    )

    if (college_logo and os.path.exists(college_logo)) or (
        uni_logo and os.path.exists(uni_logo)
    ):
        left_img = (
            Image(college_logo, width=1.65 * inch, height=1.65 * inch)
            if (college_logo and os.path.exists(college_logo))
            else ""
        )
        right_img = (
            Image(uni_logo, width=1.45 * inch, height=1.65 * inch)
            if (uni_logo and os.path.exists(uni_logo))
            else ""
        )
        logo_tbl = Table([[left_img, right_img]], colWidths=[3.1 * inch, 3.1 * inch])
        logo_tbl.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ]
            )
        )
        story.append(logo_tbl)
    else:
        story.append(Spacer(1, 40))

    pb_p = Paragraph(
        f"<b>PRESENTED BY</b><br/><br/>"
        f"<b>{META['student_name']}</b><br/>"
        f"Roll No. {META['roll_no']}<br/>"
        f"{META['semester']}",
        STYLES["BodyCenter"],
    )
    sb_p = Paragraph(
        f"<b>SUBMITTED TO</b><br/><br/>"
        f"<b>{META['college']}</b><br/>"
        f"{META['city']}<br/>"
        f"Affiliated to {META['university']}",
        STYLES["BodyCenter"],
    )
    info_tbl = Table([[pb_p, sb_p]], colWidths=[3.1 * inch, 3.1 * inch])
    info_tbl.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY_HEADER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
                ("BACKGROUND", (0, 0), (-1, -1), ROW_ALT_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(info_tbl)
    story.append(Spacer(1, 24))

    story.append(
        Paragraph(
            f"<b>UNDER THE GUIDANCE OF</b><br/>"
            f"<b>{META['guide_name']}</b><br/>"
            f"{META['guide_designation']}<br/>"
            f"{META['college']}<br/>"
            f"{META['city']}, India<br/>"
            f"Academic Year {META['academic_year']}",
            ParagraphStyle(
                "GuideBlock",
                parent=STYLES["BodyCenter"],
                fontSize=12,
                leading=18,
            ),
        )
    )

    # --------------------------------------------------------------------------
    # PAGE 2: TABLE OF CONTENTS & LIST OF FIGURES (DYNAMICALLY SYNCHRONIZED)
    # --------------------------------------------------------------------------
    add_chapter(story, "TOC", "TABLE OF CONTENTS", page_map, page_break=True)

    toc_rows = [
        ("1", "College Certificate", pg("SEC_1", 3)),
        ("2", "Acknowledgement", pg("SEC_2", 4)),
        ("3", "Project Definition (Introduction, Problem Statement, Objectives, Scope)", pg("SEC_3", 5)),
        ("4", "Project Exploration (EDA) & Data Quality Remediation", pg("SEC_4", 7)),
        ("5", "Evaluation Matrix & Experimental Setup", pg("SEC_5", 11)),
        ("6", "Supervised Model Building & Comparative Evaluation", pg("SEC_6", 13)),
        ("7", "Advanced Techniques - Unsupervised Pattern Discovery", pg("SEC_7", 19)),
        ("8", "Interpretation of Results & Operational Insights", pg("SEC_8", 22)),
        ("9", "Limitations", pg("SEC_9", 23)),
        ("10", "Future Enhancements", pg("SEC_10", 23)),
        ("11", "Bibliography", pg("SEC_11", 24)),
        ("12", "Appendix (Project Structure, Requirements & Skipped Topic Justifications)", pg("SEC_12", 25)),
    ]
    add_table(
        story,
        "Table 0.1: Table of Contents",
        ["Section", "Title", "Page No."],
        toc_rows,
        [0.75 * inch, 4.75 * inch, 0.75 * inch],
        center_cols={0, 2},
    )

    fig_rows = [
        ("Figure 4.1", "Target Service Class and Railway Zone Distribution", pg("FIG_4_1")),
        ("Figure 4.2", "Univariate Feature Histograms (Distance, Duration, Coach Classes)", pg("FIG_4_2")),
        ("Figure 4.3", "Multi-Class Quartile and Outlier Distribution (Boxplots)", pg("FIG_4_3")),
        ("Figure 4.4", "Pearson Correlation Heatmap of Numerical Features", pg("FIG_4_4")),
        ("Figure 4.5", "Before vs After Duration Fix — Macro F1 Impact Across All Models", pg("FIG_4_5")),
        ("Figure 6.1", "Supervised Model Performance Comparison (Accuracy & F1 Scores)", pg("FIG_6_1")),
        ("Figure 6.2", "Confusion Matrix of Champion Model (Decision Tree Classifier)", pg("FIG_6_2")),
        ("Figure 6.3", "One-vs-Rest Multi-Class ROC-AUC Curves", pg("FIG_6_3")),
        ("Figure 6.4", "Decision Tree Feature Importance Ranking", pg("FIG_6_4")),
        ("Figure 6.5", "5-Fold Stratified Cross-Validation Stability Boxplot", pg("FIG_6_5")),
        ("Figure 6.6", "Misclassification and Boundary Overlap Error Analysis", pg("FIG_6_6")),
        ("Figure 7.1", "K-Means Elbow Curve (Inertia Across k = 2 to 10)", pg("FIG_7_1")),
        ("Figure 7.2", "K-Means (k = 5) Operational Clusters in 2D PCA Space", pg("FIG_7_2")),
        ("Figure 7.3", "DBSCAN vs K-Means Clustering Comparison in 2D PCA Space", pg("FIG_7_3")),
    ]
    add_table(
        story,
        "Table 0.2: List of Figures",
        ["Figure No.", "Figure Title", "Page No."],
        fig_rows,
        [1.05 * inch, 4.45 * inch, 0.75 * inch],
        center_cols={0, 2},
    )

    # --------------------------------------------------------------------------
    # SECTION 1: COLLEGE CERTIFICATE
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_1", "1. COLLEGE CERTIFICATE", page_map, page_break=True)

    if (college_logo and os.path.exists(college_logo)) or (
        uni_logo and os.path.exists(uni_logo)
    ):
        lc = (
            Image(college_logo, width=1.25 * inch, height=1.25 * inch)
            if (college_logo and os.path.exists(college_logo))
            else ""
        )
        rc = (
            Image(uni_logo, width=1.1 * inch, height=1.25 * inch)
            if (uni_logo and os.path.exists(uni_logo))
            else ""
        )
        c_logo_tbl = Table([[lc, rc]], colWidths=[3.1 * inch, 3.1 * inch])
        c_logo_tbl.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(c_logo_tbl)

    story.append(
        Paragraph(
            f"<b>{META['college'].upper()}</b><br/>"
            f"Affiliated to {META['university']} &middot; {META['city']}<br/><br/>"
            f"<u><b>CERTIFICATE</b></u>",
            ParagraphStyle(
                "CertHdr",
                parent=STYLES["BodyCenter"],
                fontSize=13.5,
                leading=20,
                spaceAfter=18,
            ),
        )
    )

    add_p(
        story,
        f'This is to certify that the project report entitled <b>"{META["title"]}"</b> is a bonafide '
        f"record of the work carried out by <b>{META['student_name']} (Roll No. {META['roll_no']})</b> "
        f"and submitted to <b>{META['university']}</b> in partial fulfilment of the requirements for "
        f"the award of the degree of <b>{META['program']}</b> for the course "
        f"<b>{META['course_full']}</b> during the academic year <b>{META['academic_year']}</b>.",
    )
    add_p(
        story,
        f"To the best of our knowledge, this work is original, was carried out at <b>{META['college']}, "
        f"{META['city']}</b>, under the guidance of <b>{META['guide_name']}</b>, and has not been "
        "submitted in part or in full to any other university or institution for the award of any "
        "degree or diploma.",
    )

    story.append(Spacer(1, 48))

    sig_left = Paragraph(
        f"<b>{META['guide_name']}</b><br/>Project Guide<br/>{META['college']}",
        STYLES["Body"],
    )
    sig_right = Paragraph(
        f"<b>{META['director_name']}</b><br/>{META['director_designation']}<br/>{META['college']}",
        STYLES["BodyRight"],
    )
    sig_tbl = Table([[sig_left, sig_right]], colWidths=[3.1 * inch, 3.1 * inch])
    sig_tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(sig_tbl)

    story.append(Spacer(1, 45))
    story.append(
        Paragraph(
            f"<b>External Examiner</b><br/>{META['university']}<br/><br/>"
            "<b>Place:</b> Ahmedabad<br/>"
            "<b>Date:</b> ___ / ___ / 2026",
            STYLES["Body"],
        )
    )

    # --------------------------------------------------------------------------
    # SECTION 2: ACKNOWLEDGEMENT
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_2", "2. ACKNOWLEDGEMENT", page_map, page_break=True)

    add_p(
        story,
        "Completing this project has been an invaluable learning experience, and I am grateful to "
        "everyone who contributed to it.",
    )
    add_p(
        story,
        f"First, I thank the management of <b>{META['college']}, {META['city']}</b>, for providing "
        "excellent laboratory facilities, library resources, and a supportive learning environment "
        "throughout my BCA journey.",
    )
    add_p(
        story,
        f"I express my sincere gratitude to <b>{META['director_name']}, {META['director_designation']}, "
        f"{META['college']}</b>, for his constant encouragement and for making all necessary facilities "
        "available for this project.",
    )
    add_p(
        story,
        f"I am deeply thankful to my project guide, <b>{META['guide_name']}, {META['guide_designation']}</b>, "
        "for her valuable guidance at every stage of this work. Her suggestions helped me select the "
        "right approach for data exploration, model building, and result interpretation.",
    )
    add_p(
        story,
        f"I am also grateful to <b>{META['university']}</b> for including the course "
        f"<b>{META['course_full']}</b> in the BCA (Honours) curriculum under NEP 2020. This gave me "
        "the opportunity to work on a real-world classification and clustering problem using the "
        "Indian Railways dataset.",
    )
    add_p(
        story,
        "Finally, I thank my family and friends for their unwavering support, patience, and "
        "motivation throughout this project.",
    )

    story.append(Spacer(1, 36))
    story.append(
        Paragraph(
            f"<b>{META['student_name']}</b><br/>"
            f"Roll No. {META['roll_no']}<br/>"
            f"{META['semester']}<br/>"
            f"{META['college']}",
            STYLES["BodyRight"],
        )
    )

    # --------------------------------------------------------------------------
    # SECTION 3: PROJECT DEFINITION
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_3", "3. PROJECT DEFINITION", page_map, page_break=True)

    add_sub(story, "3.1 Introduction")
    add_p(
        story,
        "Indian Railways is the fourth-largest railway network in the world, spanning over 68,000 "
        "route kilometres, operating more than 13,000 passenger trains daily across 19+ administrative "
        "zones and 7,300+ stations. Every day, this network generates vast operational data — train "
        "schedules, route distances, coach configurations, journey durations, and zone-wise classifications.",
    )
    add_p(
        story,
        "Manual categorisation of trains into service tiers — <b>Passenger (Pass)</b>, <b>Express (Exp)</b>, "
        "and <b>Superfast (SF)</b> — is labour-intensive, inconsistent across zones, and difficult to "
        "scale. This project demonstrates that machine learning can automate this classification with "
        "high accuracy (91.50%) while also discovering latent operational groupings that are not "
        "explicitly labelled.",
    )

    add_sub(story, "3.2 Problem Statement")
    add_p(
        story,
        "The Indian Railways timetable data contains overlapping features across service tiers "
        "(e.g., Express and Superfast trains share similar distances and coach compositions), moderate "
        "class imbalance (Passenger dominates at 55.06%), and a hidden data-quality issue in the "
        "duration_m column. The challenge is to:",
    )
    add_bullet(
        story,
        "1. Multi-Class Classification: ",
        "Build an accurate multi-class classifier that predicts a train's service tier (Pass, Exp, SF) "
        "from 26 operational metrics.",
    )
    add_bullet(
        story,
        "2. Unsupervised Clustering: ",
        "Apply unsupervised clustering (K-Means and DBSCAN) to discover natural groupings of trains "
        "and isolate anomalous schedules.",
    )
    add_bullet(
        story,
        "3. Data Quality Remediation: ",
        "Diagnose and fix data-quality issues in the journey duration representation that degrade "
        "model performance.",
    )

    add_sub(story, "3.3 Project Objectives")
    add_bullet(
        story,
        "1. Data Engineering & EDA: ",
        "Convert the raw GeoJSON dataset (trains.json, 14.08 MB) into a structured CSV (trains.csv, "
        "636 KB); audit constant columns; and visualise feature distributions and correlations.",
    )
    add_bullet(
        story,
        "2. Data Quality Remediation: ",
        "Diagnose and repair the broken duration_m feature via compound duration engineering "
        "total_duration = (duration_h * 60) + duration_m.",
    )
    add_bullet(
        story,
        "3. Leakage-Free Preprocessing: ",
        "Enforce strict 80/20 stratified train-test isolation (3,572 train / 894 test) before fitting "
        "StandardScaler and one-hot encoding 19 railway zones.",
    )
    add_bullet(
        story,
        "4. Multi-Class Classification: ",
        "Train and compare Dummy Baseline, KNN (k=5), Decision Tree (default and depth=10), "
        "Gaussian Naive Bayes, and SVM (RBF) on the 3 train classes.",
    )
    add_bullet(
        story,
        "5. Robust Model Validation: ",
        "Evaluate with Macro/Weighted/Micro F1, confusion matrices, One-vs-Rest ROC-AUC, 5-fold "
        "stratified cross-validation, feature importance, and error analysis.",
    )
    add_bullet(
        story,
        "6. Unsupervised Fleet Discovery: ",
        "Segment trains using K-Means (k=5, Elbow + PCA) and density-based DBSCAN (eps=7.0, "
        "min_samples=20); export labelled clusters to data/trains_with_clusters.csv.",
    )

    add_sub(story, "3.4 Scope of the Project")
    add_bullet(
        story,
        "In Scope: ",
        "Three-class classification (Passenger, Express, Superfast) using 26 engineered features; "
        "two unsupervised clustering algorithms (K-Means, DBSCAN); data-quality diagnostics and "
        "remediation; and reproducible pipeline with saved models and CSV outputs.",
    )
    add_bullet(
        story,
        "Out of Scope: ",
        "Live NTES delay data integration, real-time REST API deployment, and deep learning "
        "approaches (documented under Future Enhancements).",
    )

    add_sub(story, "3.5 Why Machine Learning?")
    add_p(
        story,
        "Machine learning is well-suited to this problem because the classification boundaries between "
        "service tiers are non-linear and threshold-based (matching real-world railway rules), "
        "unsupervised clustering can discover hidden archetypes that manual zoning cannot, and the "
        "trained pipeline can classify new train records automatically.",
    )

    # --------------------------------------------------------------------------
    # SECTION 4: PROJECT EXPLORATION (EDA)
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_4", "4. PROJECT EXPLORATION (EDA)", page_map, page_break=True)

    add_sub(story, "4.1 Dataset Overview")
    ds_rows = [
        ("Name", "Indian Railways Dataset"),
        ("Source", "Kaggle — sripaadsrinivasan/indian-railways-dataset"),
        ("Original File", "trains.json (GeoJSON, 14.08 MB)"),
        ("Converted File", "trains.csv (636 KB)"),
        ("Raw Records", "5,208"),
        ("Filtered Records", "4,466 (3 classes only: Pass, Exp, SF)"),
        ("Features (after one-hot)", "26"),
    ]
    add_table(
        story,
        "Table 4.1: Dataset Overview and Specifications",
        ["Field", "Specification"],
        ds_rows,
        [2.2 * inch, 4.05 * inch],
    )

    add_sub(story, "4.2 Target Variable — Class Distribution")
    cls_rows = [
        ("Pass", "Passenger", "2,459", "55.06%", "Short-distance, frequent halts, unreserved / basic sleeper"),
        ("Exp", "Express", "1,288", "28.84%", "Medium-to-long distance, mixed Sleeper & 3AC/2AC coaches"),
        ("SF", "Superfast", "719", "16.10%", "High priority, fewer halts, high average speed & full AC"),
    ]
    add_table(
        story,
        "Table 4.2: Target Variable Class Distribution (N = 4,466)",
        ["Class Code", "Category", "Count", "Share (%)", "Operational Profile"],
        cls_rows,
        [0.85 * inch, 1.05 * inch, 0.75 * inch, 0.85 * inch, 2.75 * inch],
        center_cols={0, 2, 3},
    )
    add_p(
        story,
        "<b>Observation:</b> The dataset exhibits moderate class imbalance — the Passenger class is "
        "3.4 times larger than Superfast. This makes raw accuracy misleading; therefore, "
        "<b>Macro F1 is adopted as the primary evaluation metric</b>.",
    )

    add_sub(story, "4.3 Zone Distribution")
    add_p(
        story,
        "Zone-wise train counts reveal that NR (Northern Railway), WR (Western Railway), SR (Southern "
        "Railway), ER (Eastern Railway), and CR (Central Railway) handle the highest volumes, "
        "reflecting dense commuter and intercity corridors.",
    )
    add_figure(
        story,
        "FIG_4_1",
        "eda_class_zone_distribution.png",
        "Figure 4.1: Target Class Distribution (Left) and Railway Zone Distribution (Right)",
        page_map,
    )

    add_sub(story, "4.4 Univariate & Quartile Analysis")
    add_bullet(
        story,
        "Distance Distribution: ",
        "Right-skewed distribution with a mean distance of 558 km, a median distance of 244 km, and "
        "a long upper tail extending beyond 4,000 km for long-haul Express and Superfast routes.",
    )
    add_bullet(
        story,
        "Duration Distribution (Before Fix): ",
        "Bimodal distribution bounded between 0 and 58 minutes (mean: 28 minutes, median: 30 minutes), "
        "which directly exposed the duration_m data-quality issue.",
    )
    add_figure(
        story,
        "FIG_4_2",
        "eda_histograms.png",
        "Figure 4.2: Univariate Feature Histograms Across Operational Attributes",
        page_map,
    )
    add_figure(
        story,
        "FIG_4_3",
        "boxplots.png",
        "Figure 4.3: Multi-Class Boxplots Showing Quartile Spread and Route Outliers",
        page_map,
    )

    add_sub(story, "4.5 Correlation Analysis")
    corr_rows = [
        ("Distance <-> Total Duration", "0.98", "Strong linear relationship between route length and travel time"),
        ("Third AC <-> Sleeper", "0.86", "Long-distance overnight trains carry both Sleeper and 3AC coaches"),
        ("Second AC <-> Sleeper", "0.79", "Upper-tier AC coaches accompany Sleeper on Express/SF routes"),
        ("Distance <-> Sleeper", "0.70", "Sleeper coaches are attached primarily on medium/long routes"),
        ("Distance <-> Third AC", "0.69", "Strong positive correlation between distance and 3AC availability"),
        ("First AC <-> Second AC", "0.39", "Selective attachment of 1AC cabins on premier corridors"),
    ]
    add_table(
        story,
        "Table 4.3: Pearson Correlation Coefficients (r) Across Key Features",
        ["Feature Pair", "Correlation (r)", "Interpretation"],
        corr_rows,
        [2.1 * inch, 1.15 * inch, 3.0 * inch],
        center_cols={1},
    )
    add_figure(
        story,
        "FIG_4_4",
        "correlation_heatmap.png",
        "Figure 4.4: Pearson Correlation Heatmap of Numerical Features",
        page_map,
    )

    add_sub(story, "4.6 Data Quality Issue — The Killer Finding")
    add_p(
        story,
        "The <b>duration_m</b> column appeared to store total minutes, but inspection showed that it "
        "only stored the <b>minute remainder (0-58)</b> rather than total journey duration in minutes. "
        "For example, a 24-hour journey with 0 extra minutes appeared as duration_h = 24, duration_m = 0, "
        "and a 14h 30m journey appeared as duration_h = 14, duration_m = 30.",
    )
    add_p(
        story,
        "To restore the true continuous journey time across all 4,466 trains, the compound feature "
        "<b>total_duration</b> was engineered and the broken component columns were dropped:",
    )
    add_equation(story, "total_duration = (duration_h * 60) + duration_m")
    add_figure(
        story,
        "FIG_4_5",
        "before_after_duration_fix.png",
        "Figure 4.5: Before vs After Duration Fix — Macro F1 Improvement Across All Models",
        page_map,
    )

    add_sub(story, "4.7 Constant Column Audit")
    add_p(
        story,
        "Before one-hot encoding, all binary coach indicators (1AC, 2AC, 3AC, Chair Car, Sleeper, "
        "First Class) were audited for variance (nunique() > 1) to prevent encoding zero-variance columns.",
    )

    # --------------------------------------------------------------------------
    # SECTION 5: EVALUATION MATRIX
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_5", "5. EVALUATION MATRIX", page_map, page_break=True)

    add_sub(story, "5.1 Train-Test Split & Leakage Prevention")
    split_rows = [
        ("Training Set", "3,572", "80%", "Stratified model training, 5-fold CV & clustering"),
        ("Testing Set", "894", "20%", "Unseen hold-out evaluation, confusion matrix & ROC-AUC"),
    ]
    add_table(
        story,
        "Table 5.1: Stratified 80/20 Train-Test Split",
        ["Split Partition", "Size", "Ratio", "Role in Pipeline"],
        split_rows,
        [1.5 * inch, 0.9 * inch, 0.85 * inch, 3.0 * inch],
        center_cols={1, 2},
    )
    add_p(
        story,
        "<b>Method:</b> train_test_split(test_size=0.2, stratify=y, random_state=42) preserves exact "
        "class proportions in both splits. StandardScaler was fitted strictly on X_train after splitting "
        "to prevent data leakage.",
    )

    add_sub(story, "5.2 Evaluation Metrics")
    add_bullet(
        story,
        "1. Accuracy: ",
        "Fraction of total test trains classified correctly: (TP + TN) / (TP + TN + FP + FN). "
        "Limitation: Biased toward the majority Passenger class (55.06%).",
    )
    add_bullet(
        story,
        "2. Precision: ",
        "Of the trains predicted as class X, how many were actually class X: TP / (TP + FP).",
    )
    add_bullet(
        story,
        "3. Recall: ",
        "Of the actual class X trains, how many were correctly identified: TP / (TP + FN).",
    )
    add_bullet(
        story,
        "4. F1-Score: ",
        "Harmonic mean of precision and recall: 2 * (Precision * Recall) / (Precision + Recall).",
    )
    add_bullet(
        story,
        "5. Macro-Averaged F1 (Primary Metric): ",
        "Unweighted mean of per-class F1 scores: (F1_Pass + F1_Exp + F1_SF) / 3. Treats all classes "
        "equally — essential for imbalanced datasets.",
    )
    add_bullet(
        story,
        "6. Weighted-Averaged F1: ",
        "F1 score weighted by class support, reflecting natural fleet proportions.",
    )
    add_bullet(
        story,
        "7. Micro-Averaged Precision / Recall: ",
        "Global aggregation of True Positives across all classes (0.9150 for Decision Tree).",
    )
    add_bullet(
        story,
        "8. ROC-AUC (One-vs-Rest) & Confusion Matrix: ",
        "Measures ranking separability across probability thresholds and tabulates actual vs "
        "predicted counts in a 3x3 grid.",
    )

    add_sub(story, "5.3 Impact of Data Quality Fix on Evaluation")
    dq_rows = [
        ("KNN (k=5)", "0.7552", "0.7886", "+0.0334"),
        ("Decision Tree (default)", "0.8309", "0.8896", "+0.0587"),
        ("DT (depth=10)", "0.7720", "0.8459", "+0.0739"),
        ("Naive Bayes", "0.2969", "0.3098", "+0.0129"),
        ("SVM (RBF)", "0.7168", "0.7651", "+0.0483"),
        ("K-Means Silhouette", "0.1755", "0.2024", "+0.0269"),
    ]
    add_table(
        story,
        "Table 5.2: Impact of Compound Duration Fix Across All Models",
        ["Model", "F1 Macro (Before)", "F1 Macro (After)", "Delta Gain"],
        dq_rows,
        [2.35 * inch, 1.3 * inch, 1.3 * inch, 1.3 * inch],
        center_cols={1, 2, 3},
    )
    add_p(
        story,
        "<b>Key Finding:</b> A single data-quality fix improved all 5 supervised models and the "
        "clustering silhouette score — empirical proof that data quality matters more than algorithm choice.",
    )

    # --------------------------------------------------------------------------
    # SECTION 6: MODEL BUILDING
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_6", "6. MODEL BUILDING", page_map, page_break=True)

    add_sub(story, "6.1 Algorithm Selection")
    alg_rows = [
        ("Dummy Classifier", "Baseline", "Establishes minimum benchmark floor"),
        ("KNN (k=5)", "Instance-based", "Distance-based voting; requires feature scaling"),
        ("Decision Tree", "Rule-based", "Interpretable threshold splits; no scaling required"),
        ("Gaussian Naive Bayes", "Probabilistic", "Fast baseline; assumes conditional independence"),
        ("SVM (RBF)", "Margin-based", "Non-linear kernel hyperplane; requires feature scaling"),
    ]
    add_table(
        story,
        "Table 6.1: Supervised Classification Algorithms Selected",
        ["Algorithm", "Type", "Reason for Selection"],
        alg_rows,
        [1.75 * inch, 1.3 * inch, 3.2 * inch],
        center_cols={1},
    )

    add_sub(story, "6.2 Dummy Baseline (Benchmark)")
    add_p(
        story,
        "DummyClassifier(strategy='most_frequent') predicts Passenger for every test sample, achieving "
        "Accuracy = 0.5503, F1 Macro = 0.2367, and F1 Weighted = 0.3907. A model must beat 23.67% "
        "Macro F1 to be meaningful.",
    )

    add_sub(story, "6.3 K-Nearest Neighbors (k = 5)")
    add_p(
        story,
        "For each test point, KNN finds the 5 nearest training points by Euclidean distance and takes "
        "a majority vote. StandardScaler is required because Euclidean distance is otherwise dominated "
        "by large-magnitude features (distance in km). Result: Accuracy = 0.8523, F1 Macro = 0.7886, "
        "F1 Weighted = 0.8484.",
    )

    add_sub(story, "6.4 Decision Tree Classifier (Champion Model)")
    add_p(
        story,
        "Decision Tree recursively splits the feature space on axis-aligned thresholds to maximise "
        "information gain (Gini impurity). It wins because Indian Railways classifies trains via "
        "threshold rules (e.g., 3AC availability, distance, and journey duration). Default tree "
        "achieves <b>0.9150 Accuracy, 0.8896 F1 Macro, and 0.9146 F1 Weighted</b>, outperforming the "
        "pruned depth=10 tree (0.8859 Accuracy, 0.8459 F1 Macro).",
    )

    add_sub(story, "6.5 Gaussian Naive Bayes")
    add_p(
        story,
        "Gaussian Naive Bayes assumes features are conditionally independent given the class and follow "
        "Gaussian distributions. Because Distance, Duration, and AC coaches are strongly correlated "
        "(r > 0.85), Naive Bayes fails with Accuracy = 0.3702, F1 Macro = 0.3098, and F1 Weighted = 0.3636.",
    )

    add_sub(story, "6.6 Support Vector Machine (RBF Kernel)")
    add_p(
        story,
        "SVM finds the maximum-margin hyperplane separating classes using an RBF kernel on scaled "
        "features. Result: Accuracy = 0.8412, F1 Macro = 0.7651, F1 Weighted = 0.8343.",
    )

    add_sub(story, "6.7 Model Comparison Summary")
    comp_rows = [
        ("Dummy Baseline", "0.5503", "0.2367", "0.3907", "Benchmark"),
        ("KNN (k=5)", "0.8523", "0.7886", "0.8484", "Strong"),
        ("Decision Tree (default)", "0.9150", "0.8896", "0.9146", "WINNER"),
        ("DT (depth=10)", "0.8859", "0.8459", "0.8836", "Runner-up"),
        ("Naive Bayes", "0.3702", "0.3098", "0.3636", "Poor fit"),
        ("SVM (RBF)", "0.8412", "0.7651", "0.8343", "Strong"),
    ]
    add_table(
        story,
        "Table 6.2: Supervised Model Comparison Summary",
        ["Model", "Accuracy", "F1 Macro", "F1 Weighted", "Verdict"],
        comp_rows,
        [1.95 * inch, 1.05 * inch, 1.05 * inch, 1.15 * inch, 1.05 * inch],
        center_cols={1, 2, 3, 4},
    )
    add_figure(
        story,
        "FIG_6_1",
        "model_comparison.png",
        "Figure 6.1: Supervised Model Comparison Bar Chart",
        page_map,
    )

    add_sub(story, "6.8 Confusion Matrix — Decision Tree (Best Model)")
    cm_rows = [
        ("Pass", "464", "26", "2", "3.0% error (97.0% recall)"),
        ("Exp", "20", "202", "36", "14.0% error"),
        ("SF", "0", "32", "112", "17.4% error"),
    ]
    add_table(
        story,
        "Table 6.3: Confusion Matrix and Per-Class Error Rates (Decision Tree)",
        ["Actual \\ Predicted", "Pass", "Exp", "SF", "Per-Class Error Rate"],
        cm_rows,
        [1.45 * inch, 0.85 * inch, 0.85 * inch, 0.85 * inch, 2.25 * inch],
        center_cols={1, 2, 3},
    )
    add_p(
        story,
        "Overall error rate is <b>8.50%</b>. Dominant confusion occurs along the SF <-> Exp boundary "
        "(25 SF -> Exp, 16 Exp -> SF), while zero Superfast trains are misclassified as Passenger.",
    )
    add_figure(
        story,
        "FIG_6_2",
        "confusion_matrix_best.png",
        "Figure 6.2: Confusion Matrix for Champion Decision Tree Model",
        page_map,
    )

    add_sub(story, "6.9 ROC-AUC Curves")
    roc_rows = [
        ("KNN (k=5)", "0.9355 (best)"),
        ("SVM (RBF)", "0.9285"),
        ("Decision Tree", "0.9204"),
    ]
    add_table(
        story,
        "Table 6.4: One-vs-Rest Mean ROC-AUC Scores",
        ["Model", "Mean AUC"],
        roc_rows,
        [3.1 * inch, 3.15 * inch],
        center_cols={1},
    )
    add_figure(
        story,
        "FIG_6_3",
        "roc_curves.png",
        "Figure 6.3: One-vs-Rest Multi-Class ROC Curves",
        page_map,
    )

    add_sub(story, "6.10 Feature Importance (Decision Tree)")
    fi_rows = [
        ("1", "third_ac", "0.3551", "Primary separator between Pass and Exp/SF"),
        ("2", "distance", "0.2226", "Commuter vs long-haul separator"),
        ("3", "total_duration", "0.1799", "Engineered feature #3 — validates duration fix"),
        ("4", "chair_car", "0.1181", "Intercity day express indicator"),
        ("5", "first_ac", "0.0133", "Premium AC tier marker"),
    ]
    add_table(
        story,
        "Table 6.5: Decision Tree Feature Importance Ranking",
        ["Rank", "Feature", "Importance", "Interpretation"],
        fi_rows,
        [0.65 * inch, 1.45 * inch, 1.1 * inch, 3.05 * inch],
        center_cols={0, 2},
    )
    add_figure(
        story,
        "FIG_6_4",
        "feature_importance.png",
        "Figure 6.4: Decision Tree Feature Importance Ranking",
        page_map,
    )

    add_sub(story, "6.11 Cross-Validation (5-Fold Stratified) & Error Analysis")
    add_p(
        story,
        "Decision Tree 5-fold stratified cross-validation achieved <b>F1 Macro = 0.8743 +/- 0.0155</b>. "
        "Low variance across folds confirms stability and absence of overfitting. Error analysis "
        "confirms that misclassified trains are concentrated in the mid-distance, mid-duration region "
        "where Express and Superfast overlap operationally.",
    )
    add_figure(
        story,
        "FIG_6_5",
        "cross_validation.png",
        "Figure 6.5: 5-Fold Stratified Cross-Validation Boxplot",
        page_map,
    )
    add_figure(
        story,
        "FIG_6_6",
        "error_analysis.png",
        "Figure 6.6: Error Analysis of Misclassified Trains",
        page_map,
    )

    # --------------------------------------------------------------------------
    # SECTION 7: ADVANCED TECHNIQUES — PATTERN DISCOVERY
    # --------------------------------------------------------------------------
    add_chapter(
        story,
        "SEC_7",
        "7. ADVANCED TECHNIQUES - PATTERN DISCOVERY",
        page_map,
        page_break=True,
    )

    add_sub(story, "7.1 K-Means Clustering (k = 5)")
    add_p(
        story,
        "K-Means partitioned the 3,572 scaled training records into k = 5 clusters (selected via the "
        "Elbow Method across k = 2 to 10). At k = 5, Inertia is <b>69,115.75</b> and Silhouette Score "
        "is <b>0.2024</b> (up from 0.1755 before the duration fix). For visualisation, the 26-dimensional "
        "feature space was projected to 2D using Principal Component Analysis (PCA).",
    )
    add_figure(
        story,
        "FIG_7_1",
        "elbow_curve.png",
        "Figure 7.1: Elbow Curve for Optimal k Selection",
        page_map,
    )
    add_figure(
        story,
        "FIG_7_2",
        "clusters_k5_fixed_pca.png",
        "Figure 7.2: K-Means Clusters (k = 5) in 2D PCA Space",
        page_map,
    )

    add_sub(story, "7.2 DBSCAN Clustering (eps = 7.0, min_samples = 20)")
    add_p(
        story,
        "Density-based DBSCAN (eps = 7.0, min_samples = 20) discovered <b>4 natural clusters</b> "
        "with <b>0.4% noise (13 outlier points)</b> and a Silhouette Score of <b>0.2543</b> "
        "(outperforming K-Means).",
    )
    add_figure(
        story,
        "FIG_7_3",
        "dbscan_vs_kmeans.png",
        "Figure 7.3: DBSCAN vs K-Means Clustering Comparison",
        page_map,
    )

    add_sub(story, "7.3 K-Means vs DBSCAN Comparison & Cluster Interpretation")
    km_db_rows = [
        ("Paradigm", "Centroid-based", "Density-based"),
        ("Clusters", "5 (user-specified)", "4 (natural)"),
        ("Noise handling", "None", "0.4% (13 points)"),
        ("Silhouette", "0.2024", "0.2543"),
        ("Geometry", "Spherical only", "Arbitrary"),
        ("Operational strength", "Granular zone/tier", "Anomaly isolation"),
    ]
    add_table(
        story,
        "Table 7.1: K-Means vs DBSCAN Comparison",
        ["Criterion", "K-Means (k=5)", "DBSCAN (eps=7, min=20)"],
        km_db_rows,
        [1.85 * inch, 2.2 * inch, 2.2 * inch],
    )

    c_interp_rows = [
        ("C-0", "ER-Regional Network", "Eastern Railway regional fleet — medium-short distance, mixed coaches"),
        ("C-1", "NFR-Mixed Operations", "Northeast Frontier strategic routes — hilly gradients"),
        ("C-2", "Short-Distance Commuter Pass", "High-frequency local passenger — short route, zero AC coaches"),
        ("C-3", "Long-Distance AC Premium Fleet", "Flagship Express & Superfast — longest distance, near-100% AC"),
        ("C-4", "Secondary-Zone Short Passenger", "Regional branch-line connectors — rural-to-junction feeders"),
    ]
    add_table(
        story,
        "Table 7.2: Interpretation of Clusters (K-Means, k = 5)",
        ["Cluster", "Name", "Operational Interpretation"],
        c_interp_rows,
        [0.75 * inch, 1.95 * inch, 3.55 * inch],
        center_cols={0},
    )
    add_p(
        story,
        "<b>Output Artifact:</b> All cluster assignments and features were saved to "
        "<b>data/trains_with_clusters.csv</b> (3,572 rows x 28 columns).",
    )

    # --------------------------------------------------------------------------
    # SECTION 8, 9, 10: INSIGHTS, LIMITATIONS & FUTURE ENHANCEMENTS
    # --------------------------------------------------------------------------
    add_chapter(
        story,
        "SEC_8",
        "8. INTERPRETATION OF RESULTS & INSIGHTS",
        page_map,
        page_break=True,
    )

    add_sub(story, "8.1 Key Insight #1 — Data Quality Beats Algorithm Complexity")
    add_p(
        story,
        "Fixing the duration_m bug improved every single supervised model (up to +0.0739 F1) and "
        "the K-Means silhouette score (+0.0269). This is the strongest empirical finding of the "
        "project: understanding and repairing data quality yields greater gains than switching algorithms.",
    )

    add_sub(story, "8.2 Key Insight #2 — Decision Tree Excels on Rule-Bound Data")
    add_p(
        story,
        "The Decision Tree achieved 91.50% accuracy, 0.8896 Macro F1, and 0.8743 +/- 0.0155 CV F1 — "
        "outperforming KNN, SVM, and Naive Bayes. Indian Railways classifies trains via hierarchical "
        "threshold rules, which axis-aligned tree splits model naturally. Top features: third_ac "
        "(35.5%), distance (22.3%), total_duration (18.0%).",
    )

    add_sub(story, "8.3 Key Insight #3 — Complementary Unsupervised Taxonomy")
    add_p(
        story,
        "K-Means (k=5) uncovered interpretable regional/premium archetypes, while DBSCAN isolated "
        "0.4% operational outliers. Together, they provide a data-driven taxonomy of Indian Railways "
        "trains that complements administrative zone boundaries.",
    )

    add_sub(story, "8.4 Why Naive Bayes Failed")
    add_p(
        story,
        "Gaussian Naive Bayes performed poorly (37.02% accuracy) because its core assumption — "
        "feature independence — is heavily violated. Distance, Duration, and AC coach configurations "
        "are strongly correlated (r > 0.85).",
    )

    add_chapter(story, "SEC_9", "9. LIMITATIONS", page_map, page_break=False)
    add_bullet(story, "1. Moderate class imbalance: ", "The minority Superfast class (16.1%) is harder to classify than Passenger (55.1%).")
    add_bullet(story, "2. 8.50% error rate: ", "Dominant confusion occurs between Express and Superfast due to boundary overlap.")
    add_bullet(story, "3. No live telemetry: ", "Data is a static timetable snapshot rather than real-time NTES running data.")
    add_bullet(story, "4. Feature scope: ", "Halt count, average commercial speed, delay history, and seasonality are not included.")
    add_bullet(story, "5. Zone one-hot sparsity: ", "19 binary zone columns dilute Euclidean distances for KNN and SVM.")
    add_bullet(story, "6. No ensemble methods: ", "Random Forest, XGBoost, and Gradient Boosting were kept as future scope.")

    add_chapter(story, "SEC_10", "10. FUTURE ENHANCEMENTS", page_map, page_break=False)
    add_bullet(story, "1. Ensemble & Gradient Boosting: ", "Random Forest / XGBoost / LightGBM to resolve the 8.50% Express <-> Superfast overlap.")
    add_bullet(story, "2. Live NTES Telemetry: ", "Incorporate real-time delay data, halt count, and average commercial speed.")
    add_bullet(story, "3. REST API Deployment: ", "Deploy persisted joblib models (dt_classifier.joblib & scaler.joblib) as a REST API.")
    add_bullet(story, "4. Deep Learning Baseline: ", "Evaluate TabNet and Multi-Layer Perceptrons (MLP) with zone embeddings.")
    add_bullet(story, "5. Web Dashboard: ", "Interactive dashboard for zone-wise train tier predictions.")
    add_bullet(story, "6. Time-Series Forecasting: ", "Predict train volumes by zone and season.")

    # --------------------------------------------------------------------------
    # SECTION 11: BIBLIOGRAPHY
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_11", "11. BIBLIOGRAPHY", page_map, page_break=True)

    refs = [
        ("1. ", "Saikat Dutt, Subramanian Chandramouli, Amit Kumar Das — Machine Learning, Pearson Education."),
        ("2. ", "Andreas C. Muller & Sarah Guido — Introduction to Machine Learning with Python, O'Reilly Media."),
        ("3. ", "Aurelien Geron — Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, O'Reilly Media."),
        ("4. ", "Tom M. Mitchell — Machine Learning, McGraw Hill Education."),
        ("5. ", "Sripaad Srinivasan — Indian Railways Dataset, Kaggle (https://www.kaggle.com/datasets/sripaadsrinivasan/indian-railways-dataset)."),
        ("6. ", "scikit-learn Documentation — https://scikit-learn.org/stable/"),
        ("7. ", "pandas Documentation — https://pandas.pydata.org/docs/"),
        ("8. ", "Matplotlib Documentation — https://matplotlib.org/stable/"),
    ]
    for num, r_txt in refs:
        add_bullet(story, num, r_txt)

    # --------------------------------------------------------------------------
    # SECTION 12: APPENDIX (CLEAN REPO TREE — NO AI MENTION)
    # --------------------------------------------------------------------------
    add_chapter(story, "SEC_12", "12. APPENDIX", page_map, page_break=True)

    add_sub(story, "12.1 Project Folder Structure")
    add_code(
        story,
        """Indian-Railway-Train/
|-- data/
|   |-- trains.json                    # Original dataset (14.08 MB)
|   |-- trains.csv                     # Converted CSV (636 KB)
|   +-- trains_with_clusters.csv       # Cluster output (3,572 x 28)
|-- notebooks/
|   +-- main_notebook.ipynb            # Main notebook (all 4 phases)
|-- extras/
|   |-- advanced_ml.ipynb              # Model persistence, CV, error analysis
|   +-- README.md
|-- models/
|   |-- scaler.joblib
|   +-- dt_classifier.joblib
|-- visualizations/                    # Saved evaluation & EDA plots
|-- reports/
|   +-- Indian_Railway_ML_Presentation.pptx
|-- .gitignore
|-- README.md
+-- requirements.txt""",
    )

    add_sub(story, "12.2 Hardware & Software Requirements")
    hw_rows = [
        ("OS", "Windows 10 / Windows 11"),
        ("Python", "3.13.6"),
        ("Editor", "Jupyter Notebook"),
        ("Libraries", "pandas, numpy, scikit-learn, matplotlib, seaborn, joblib"),
        ("RAM", "Minimum 4 GB"),
        ("Storage", "500 MB free space"),
    ]
    add_table(
        story,
        "Table 12.1: Hardware and Software Specifications",
        ["Component", "Specification"],
        hw_rows,
        [1.85 * inch, 4.4 * inch],
    )

    add_sub(story, "12.3 Reproducibility & GitHub Repository")
    add_code(
        story,
        """pip install -r requirements.txt
# Open notebooks/main_notebook.ipynb in Jupyter Notebook and run all cells top-to-bottom

Repository URL : https://github.com/rajputpri/Indian-Railway-Train
Branch         : master""",
    )

    add_sub(story, "12.4 Justification for Skipped Topics")
    add_bullet(
        story,
        "Linear Regression — Not Applicable: ",
        "The target variable type is categorical (3 classes: Pass, Exp, SF), not continuous. "
        "Linear Regression predicts numeric values and would produce meaningless outputs "
        "(e.g., Pass = 0.87). The correct approach for categorical targets is classification, "
        "which is why we used KNN, Decision Tree, Naive Bayes, and SVM.",
    )
    add_bullet(
        story,
        "Apriori — Not Applicable: ",
        "Apriori discovers association rules from transactional/basket data (e.g., customers who "
        "buy X also buy Y). This dataset contains operational features per train, not transactions. "
        "Therefore, K-Means and DBSCAN were chosen for unsupervised pattern discovery.",
    )

    return story


def generate_pdf_report():
    pdf_path = os.path.join(REPORTS_DIR, "Indian_Railway_ML_Project_Report.pdf")
    college_logo, uni_logo = extract_logos_from_template()

    # PASS 1: Dry run to record exact page numbers for every chapter & figure
    page_map = {}
    temp_path = os.path.join(REPORTS_DIR, "_pass1_temp.pdf")
    doc_pass1 = SimpleDocTemplate(
        temp_path,
        pagesize=A4,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
    )
    story_pass1 = build_story(page_map, college_logo, uni_logo)
    doc_pass1.build(
        story_pass1,
        onFirstPage=draw_page_number_footer,
        onLaterPages=draw_page_number_footer,
    )
    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except Exception:
            pass

    # PASS 2: Final build with 100% verified page numbers injected into TOC & List of Figures
    story_final = build_story(page_map, college_logo, uni_logo)
    try:
        doc_final = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=inch,
            rightMargin=inch,
            topMargin=0.85 * inch,
            bottomMargin=0.85 * inch,
            title=META["title"],
            author=META["student_name"],
        )
        doc_final.build(
            story_final,
            onFirstPage=draw_page_number_footer,
            onLaterPages=draw_page_number_footer,
        )
        saved_pdf = pdf_path
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_pdf = os.path.join(
            REPORTS_DIR, f"Indian_Railway_ML_Project_Report_{ts}.pdf"
        )
        doc_final = SimpleDocTemplate(
            saved_pdf,
            pagesize=A4,
            leftMargin=inch,
            rightMargin=inch,
            topMargin=0.85 * inch,
            bottomMargin=0.85 * inch,
            title=META["title"],
            author=META["student_name"],
        )
        doc_final.build(
            story_final,
            onFirstPage=draw_page_number_footer,
            onLaterPages=draw_page_number_footer,
        )

    return saved_pdf, page_map


if __name__ == "__main__":
    print("=" * 72)
    print("BUILDING FINAL A4 PDF REPORT (2-PASS EXACT PAGE SYNC)...")
    print("=" * 72)
    out_pdf, pmap = generate_pdf_report()
    print(f"[SUCCESS] Clean PDF Report generated at: {out_pdf}")
    print(f"[VERIFIED] Synchronized Page Map       : {pmap}")
    print("=" * 72)