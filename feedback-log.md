# Feedback Log

## Project: Resume and Cover Letter Tailor

> Every user-provided prompt, correction, or decision is logged here in order.
> This log is the project's memory. Read it before starting any new round of work.

---

## Session 1 — Project Discovery

**Date:** 2026-06-11

**User input (paraphrased from conversation):**
- User is a university mathematics instructor with a long academic CV
- Wants a workflow to tailor a resume and cover letter to specific job postings
- Primary user is themselves; secondary users are students and wider audiences
- Biggest pain point: deciding what to keep/remove, how to structure, how to word
  documents for a specific posting
- Wants to upload CV and paste job posting; system asks clarifying questions
- Output should be polished, downloadable Word documents
- Checkboxes to select resume, cover letter, or both
- Wants a feedback loop for content AND visual structure revisions
- Feedback loop repeats until user is satisfied

**Decisions made:**
- Tech stack: Python + Streamlit + python-docx + Anthropic Claude API
- CV parsing: pdfplumber for PDF, python-docx for Word
- Model routing: Opus for analysis/review, Sonnet for writing/revision,
  Haiku for parsing/classification
- Sub-agents: Orchestrator, Job Analyzer, CV Parser, Question Generator,
  Resume Writer, Cover Letter Writer, Reviewer, Revision Agent
- Full repository structure created and pushed to GitHub

---

*Append new entries below as the project develops.*