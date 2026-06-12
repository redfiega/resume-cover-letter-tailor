from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


def set_document_margins(doc: Document, margin_inches: float = 1.0):
    """Set margins for all sections of the document."""
    for section in doc.sections:
        section.top_margin = Inches(margin_inches)
        section.bottom_margin = Inches(margin_inches)
        section.left_margin = Inches(margin_inches)
        section.right_margin = Inches(margin_inches)


def add_header(doc: Document, name: str, contact_info: str):
    """Add the name and contact information header."""
    # Name in large bold font
    name_paragraph = doc.add_paragraph()
    name_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_run = name_paragraph.add_run(name)
    name_run.bold = True
    name_run.font.size = Pt(18)

    # Contact info centered below name
    contact_paragraph = doc.add_paragraph()
    contact_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_run = contact_paragraph.add_run(contact_info)
    contact_run.font.size = Pt(10)


def add_section_header(doc: Document, title: str):
    """Add a bold section header with a line underneath."""
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(title.upper())
    run.bold = True
    run.font.size = Pt(11)

    # Add a horizontal line after the header
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    border.append(bottom)
    paragraph._p.get_or_add_pPr().append(border)


def add_bullet_point(doc: Document, text: str):
    """Add a bullet point."""
    paragraph = doc.add_paragraph(style="List Bullet")
    run = paragraph.add_run(text)
    run.font.size = Pt(10)


def add_body_text(doc: Document, text: str):
    """Add regular body text."""
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    run.font.size = Pt(10)


def build_resume_document(content: str, output_path: str) -> str:
    """Convert resume content text into a formatted Word document.
    
    The content is the raw text from the Resume Writer agent.
    This function parses it and applies Word formatting.
    """
    doc = Document()
    set_document_margins(doc, margin_inches=0.75)

    # Parse the content line by line and apply formatting
    lines = content.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect headers (lines starting with ## or all caps short lines)
        if line.startswith("## "):
            add_section_header(doc, line.replace("## ", ""))
        elif line.startswith("# "):
            # Main title / name
            header_text = line.replace("# ", "")
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run(header_text)
            run.bold = True
            run.font.size = Pt(18)
        elif line.startswith("- ") or line.startswith("* "):
            # Bullet points
            add_bullet_point(doc, line[2:])
        elif line.startswith("**") and line.endswith("**"):
            # Bold text (job titles, company names)
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(line.replace("**", ""))
            run.bold = True
            run.font.size = Pt(10)
        else:
            # Regular body text
            add_body_text(doc, line)

    # Save the document
    doc.save(output_path)
    return output_path


def build_cover_letter_document(content: str, output_path: str) -> str:
    """Convert cover letter content text into a formatted Word document."""
    doc = Document()
    set_document_margins(doc, margin_inches=1.0)

    # Parse the content into paragraphs
    paragraphs = content.split("\n\n")

    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue

        # Remove markdown formatting
        para_text = para_text.replace("**", "")
        para_text = para_text.replace("## ", "")
        para_text = para_text.replace("# ", "")

        paragraph = doc.add_paragraph()
        run = paragraph.add_run(para_text)
        run.font.size = Pt(11)

        # Add spacing between paragraphs
        paragraph.space_after = Pt(12)

    doc.save(output_path)
    return output_path