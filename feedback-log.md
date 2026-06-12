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

## Session 2 — UI Improvements

**Date:** 2026-06-11

**User feedback:**
- Questions were displayed all at once requiring a long block of text to answer
  — changed to one question at a time with a progress bar and answer history
- Feedback boxes were hard to see while scrolling — needs a bold outline or
  highlight to make them more visible
- Resume formatting is too plain — would like users to be able to select from
  formatting styles ranging from plain to more colorful/styled

**Changes completed this session:**
- Questions now display one at a time with progress bar and answer history
- Feedback boxes now have blue border labels and visible text area styling
- Resume style selector added with four options: Classic, Modern, Bold, Academic
- Style choice is saved to session state and applied at download time
- document_builder.py updated with full style definitions for all four styles

---