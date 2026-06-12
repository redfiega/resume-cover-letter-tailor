import pdfplumber
import os
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a Word document."""
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text.strip()


def extract_cv_text(uploaded_file) -> str:
    """Extract text from an uploaded CV file (PDF or Word).
    
    This function receives the uploaded file from Streamlit,
    saves it temporarily, extracts the text, then cleans up.
    """
    # Get the file extension
    file_name = uploaded_file.name
    file_extension = os.path.splitext(file_name)[1].lower()

    # Save the uploaded file temporarily
    temp_path = f"temp_cv{file_extension}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text based on file type
    try:
        if file_extension == ".pdf":
            text = extract_text_from_pdf(temp_path)
        elif file_extension in [".docx", ".doc"]:
            text = extract_text_from_docx(temp_path)
        else:
            text = ""
    finally:
        # Always clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text