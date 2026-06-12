from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os


# ─────────────────────────────────────────
# STYLE DEFINITIONS
# ─────────────────────────────────────────

STYLES = {
    "Classic": {
        "name_size": 18,
        "header_size": 11,
        "body_size": 12,
        "name_color": RGBColor(0, 0, 0),
        "header_color": RGBColor(0, 0, 0),
        "header_bold": True,
        "header_underline": False,
        "accent_color": RGBColor(0, 0, 0),
        "background": False,
        "margin": 1.0,
        "font": "Times New Roman"
    },
    "Modern": {
        "name_size": 20,
        "header_size": 11,
        "body_size": 12,
        "name_color": RGBColor(0, 101, 164),
        "header_color": RGBColor(0, 101, 164),
        "header_bold": True,
        "header_underline": False,
        "accent_color": RGBColor(0, 101, 164),
        "background": False,
        "margin": 0.75,
        "font": "Calibri"
    },
    "Bold": {
        "name_size": 22,
        "header_size": 12,
        "body_size": 12,
        "name_color": RGBColor(255, 255, 255),
        "header_color": RGBColor(255, 255, 255),
        "background": True,
        "background_hex": "1F497D",
        "margin": 0.75,
        "font": "Calibri"
    },
    "Academic": {
        "name_size": 16,
        "header_size": 11,
        "body_size": 12,
        "name_color": RGBColor(0, 0, 0),
        "header_color": RGBColor(0, 0, 0),
        "header_bold": True,
        "header_underline": True,
        "accent_color": RGBColor(0, 0, 0),
        "background": False,
        "margin": 1.0,
        "font": "Georgia"
    }
}


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def set_document_margins(doc: Document, margin_inches: float = 1.0):
    """Set margins for all sections of the document."""
    for section in doc.sections:
        section.top_margin = Inches(margin_inches)
        section.bottom_margin = Inches(margin_inches)
        section.left_margin = Inches(margin_inches)
        section.right_margin = Inches(margin_inches)


def add_horizontal_line(paragraph):
    """Add a horizontal line below a paragraph."""
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    border.append(bottom)
    paragraph._p.get_or_add_pPr().append(border)


def add_shading(paragraph, hex_color: str):
    """Add background color shading to a paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    clean_color = hex_color.replace("#", "")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), clean_color)
    pPr.append(shd)


# ─────────────────────────────────────────
# RESUME BUILDER
# ─────────────────────────────────────────

def build_resume_document(content: str, output_path: str,
                          style_name: str = "Modern") -> str:
    """Convert resume content text into a formatted Word document."""
    style = STYLES.get(style_name, STYLES["Modern"])

    doc = Document()
    set_document_margins(doc, margin_inches=style["margin"])

    lines = content.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("# "):
            # Name / main title
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if style["background"]:
                if style["background"]:
                    add_shading(paragraph, style.get("background_hex", "1F497D"))
            run.bold = True
            run.font.size = Pt(style["name_size"])
            run.font.color.rgb = style["name_color"]
            run.font.name = style["font"]

        elif line.startswith("## "):
            # Section header
            paragraph = doc.add_paragraph()
            if style["background"]:
                add_shading(paragraph, style.get("background_hex", "1F497D"))
            run = paragraph.add_run(line.replace("## ", "").upper())
            run.bold = style["header_bold"]
            run.underline = style["header_underline"]
            run.font.size = Pt(style["header_size"])
            run.font.color.rgb = style["header_color"]
            run.font.name = style["font"]
            if not style["background"]:
                add_horizontal_line(paragraph)

        elif line.startswith("- ") or line.startswith("* "):
            # Bullet point
            paragraph = doc.add_paragraph(style="List Bullet")
            run = paragraph.add_run(line[2:])
            run.font.size = Pt(style["body_size"])
            run.font.name = style["font"]

        elif line.startswith("**") and line.endswith("**"):
            # Bold text (job titles, company names)
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(line.replace("**", ""))
            run.bold = True
            run.font.size = Pt(style["body_size"])
            run.font.name = style["font"]

        else:
            # Regular body text — handle inline bold (**text**)
            paragraph = doc.add_paragraph()
            parts = line.split("**")
            is_bold = False
            for part in parts:
                if part:
                    run = paragraph.add_run(part)
                    run.bold = is_bold
                    run.font.size = Pt(style["body_size"])
                    run.font.name = style["font"]
                is_bold = not is_bold

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path


# ─────────────────────────────────────────
# COVER LETTER BUILDER
# ─────────────────────────────────────────

def build_cover_letter_document(content: str, output_path: str,
                                style_name: str = "Modern") -> str:
    """Convert cover letter content text into a formatted Word document."""
    style = STYLES.get(style_name, STYLES["Modern"])

    doc = Document()
    set_document_margins(doc, margin_inches=1.0)

    paragraphs = content.split("\n\n")

    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue

        para_text = para_text.replace("**", "")
        para_text = para_text.replace("## ", "")
        para_text = para_text.replace("# ", "")

        paragraph = doc.add_paragraph()
        run = paragraph.add_run(para_text)
        run.font.size = Pt(12)
        run.font.name = style["font"]
        paragraph.space_after = Pt(12)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path