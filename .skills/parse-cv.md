# Skill: Parse CV

## When to Use
When a user uploads a CV and it needs to be read and structured before tailoring.

## Prerequisites
- CV file uploaded (PDF or Word)
- `pdfplumber` or `python-docx` installed
- `prompt-library/system-prompts.txt` loaded

## Steps
1. Detect file type (PDF or .docx)
2. Extract raw text using pdfplumber (PDF) or python-docx (Word)
3. Send extracted text to CV Parser agent (Haiku)
4. Receive structured CV content organized by section
5. Store structured content in session state for downstream agents

## Expected Output
Structured CV content with clearly labeled sections ready for use by
Job Analyzer, Question Generator, Resume Writer, and Cover Letter Writer.

## Known Failure Modes
- **Scanned PDF:** Text extraction fails on image-based PDFs. Display error
  asking user to upload a text-based PDF or Word document.
- **Unusual formatting:** Heavily formatted CVs may lose structure on extraction.
  Pass raw text to agent and let it do its best.
- **Empty file:** Check for empty content after extraction and display clear error.