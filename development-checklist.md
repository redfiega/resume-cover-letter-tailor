# Development Checklist

## Project: Resume and Cover Letter Tailor

---

## Phase 0 — Project Setup

- [ ] Repository created on GitHub
- [ ] All Markdown documentation files created
- [ ] `.gitignore` file created
- [ ] `requirements.txt` created
- [ ] `claude.md` created
- [ ] Pushed to GitHub

---

## Phase 1 — Environment Setup

- [ ] Python virtual environment created
- [ ] All packages installed successfully
- [ ] `.env` file created with `ANTHROPIC_API_KEY`
- [ ] API connection tested

---

## Phase 2 — Agent and Skill Files

- [ ] `.agents/orchestrator.md` created
- [ ] `.agents/job-analyzer.md` created
- [ ] `.agents/cv-parser.md` created
- [ ] `.agents/question-generator.md` created
- [ ] `.agents/resume-writer.md` created
- [ ] `.agents/cover-letter-writer.md` created
- [ ] `.agents/reviewer.md` created
- [ ] `.agents/revision-agent.md` created
- [ ] `.skills/parse-cv.md` created
- [ ] `.skills/analyze-job-posting.md` created
- [ ] `.skills/generate-questions.md` created
- [ ] `.skills/write-resume.md` created
- [ ] `.skills/write-cover-letter.md` created
- [ ] `.skills/revise-document.md` created

---

## Phase 3 — Prompt Library

- [ ] `prompt-library/system-prompts.txt` created
- [ ] `prompt-library/analyze-job-posting.txt` created
- [ ] `prompt-library/parse-cv.txt` created
- [ ] `prompt-library/generate-questions.txt` created
- [ ] `prompt-library/write-resume.txt` created
- [ ] `prompt-library/write-cover-letter.txt` created
- [ ] `prompt-library/revise-document.txt` created

---

## Phase 4 — Core Python Modules

- [ ] `cv_parser.py` — PDF and Word CV parsing functions
- [ ] `document_builder.py` — python-docx Word document generation
- [ ] `agents.py` — All agent functions with correct model routing
- [ ] API calls use environment variable for key
- [ ] CV parsing tested with sample PDF and Word files

---

## Phase 5 — Streamlit UI

- [ ] `app.py` created with full workflow
- [ ] CV upload widget (PDF and Word)
- [ ] Job posting text area
- [ ] Resume/Cover Letter checkboxes
- [ ] Conversational question display
- [ ] Draft document preview
- [ ] Feedback text area and Revise button
- [ ] Download buttons for Word documents
- [ ] App runs without errors

---

## Phase 6 — Synthetic Data and Testing

- [ ] Sample academic CV created in `synthetic-data/`
- [ ] Sample university job posting created
- [ ] Sample industry job posting created
- [ ] Full workflow tested end to end
- [ ] Feedback loop tested with at least two revision rounds
- [ ] Results documented in `evaluation.md`

---

## Phase 7 — Deployment

- [ ] App deployed to Streamlit Community Cloud
- [ ] API key added to Streamlit secrets
- [ ] Live URL added to `README.md`
- [ ] Final push to GitHub
- [ ] End-to-end test on deployed version