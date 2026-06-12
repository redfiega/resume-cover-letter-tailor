# Architecture

## Project: Resume and Cover Letter Tailor

---

## 1. Overview

A locally-run Python application with a Streamlit browser interface. The user runs
it on their own computer or accesses it via a deployed Streamlit Cloud URL. It
connects to the Anthropic Claude API to power the AI agents and uses python-docx
to generate Word documents.

---

## 2. Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Interface | Streamlit | Simple browser UI, no web development needed |
| Language | Python 3.11+ | Widely supported, great AI and document libraries |
| LLM Provider | Anthropic Claude | Best reasoning for complex writing tasks |
| Document Generation | python-docx | Creates professional .docx files |
| CV Parsing (PDF) | pdfplumber | Reliable text extraction from PDFs |
| CV Parsing (Word) | python-docx | Reads existing Word documents |
| Config | python-dotenv | Loads API key from .env file safely |
| Version Control | GitHub | Standard; enables backup and sharing |

---

## 3. System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                     │
│                                                             │
│  [CV Upload] [Job Posting Input] [Checkboxes] [Questions]   │
│  [Draft Review] [Feedback Input] [Download Button]          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                        │
│              (claude-opus-4-5 — plans & delegates)          │
└──────┬──────────┬──────────┬──────────┬──────────┬──────────┘
       │          │          │          │          │
       ▼          ▼          ▼          ▼          ▼
  Job         CV         Question   Resume    Cover Letter
  Analyzer   Parser     Generator   Writer      Writer
  (Opus)     (Haiku)    (Sonnet)   (Sonnet)    (Sonnet)
       │          │          │          │          │
       └──────────┴──────────┴──────────┴──────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Reviewer Agent │
                  │    (Opus)       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Revision Agent  │
                  │   (Sonnet)      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Word Document  │
                  │  (.docx output) │
                  └─────────────────┘
```

---

## 4. Data Flow

### Full Workflow
1. User uploads CV (PDF or Word) and pastes job posting
2. User selects Resume, Cover Letter, or both via checkboxes
3. CV Parser (Haiku) extracts and structures CV content
4. Job Analyzer (Opus) extracts requirements, skills, and keywords
5. Question Generator (Sonnet) produces 3-5 clarifying questions
6. User answers questions conversationally in the UI
7. Resume Writer (Sonnet) generates tailored resume draft
8. Cover Letter Writer (Sonnet) generates tailored cover letter draft
9. Reviewer (Opus) checks alignment with job posting
10. Drafts displayed in UI for user review
11. User provides feedback on content and/or visual structure
12. Revision Agent (Sonnet) applies feedback and updates documents
13. Steps 11-12 repeat until user is satisfied
14. Final documents exported as .docx and made available for download

### Feedback Loop Detail
- User types feedback in a text area (e.g., "Make the summary shorter" or
  "Move education to the top")
- Revision Agent receives the current document content, the original job analysis,
  and the user's feedback
- Revised document replaces the previous draft in the UI
- User can provide multiple rounds of feedback before downloading

---

## 5. File Structure

```
resume-cover-letter-tailor/
├── app.py                    # Streamlit entry point
├── agents.py                 # Python code that runs each agent
├── document_builder.py       # python-docx functions for Word output
├── cv_parser.py              # PDF and Word CV parsing functions
├── .env                      # API key (never committed to GitHub)
├── requirements.txt          # Python dependencies
│
├── prompt-library/           # All LLM prompts stored as text files
│   ├── system-prompts.txt
│   ├── analyze-job-posting.txt
│   ├── parse-cv.txt
│   ├── generate-questions.txt
│   ├── write-resume.txt
│   ├── write-cover-letter.txt
│   └── revise-document.txt
│
├── outputs/
│   ├── resumes/              # Generated resume files
│   └── cover-letters/        # Generated cover letter files
│
├── .agents/                  # Agent definition Markdown files
├── .skills/                  # Skill recipe Markdown files
└── synthetic-data/           # Sample CVs and job postings for testing
```

---

## 6. Model Routing Logic

```
Task                              → Model
─────────────────────────────────────────────────────
Job posting analysis              → claude-opus-4-5
Final review and synthesis        → claude-opus-4-5
CV parsing and structuring        → claude-haiku-4-5-20251001
Keyword extraction                → claude-haiku-4-5-20251001
Clarifying question generation    → claude-sonnet-4-5
Resume writing                    → claude-sonnet-4-5
Cover letter writing              → claude-sonnet-4-5
Document revision                 → claude-sonnet-4-5
```

---

## 7. Privacy and Security

- The API key is stored only in the `.env` file on the user's local machine
- The `.gitignore` file prevents `.env` from being uploaded to GitHub
- Uploaded CVs are processed in memory and never stored permanently
- Generated documents are available for download and then discarded
- No user data is retained between sessions