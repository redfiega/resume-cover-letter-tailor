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

## Session 3 — Style Selector UI Improvement

**Date:** 2026-06-11

**User feedback:**
- The four style preview boxes looked like clickable buttons but were not
- The dropdown menu below them was hard to notice
- Users tried clicking the preview boxes expecting them to select the style

**Fix applied:**
- Removed the four non-interactive preview boxes
- Replaced dropdown with a radio button selector (horizontal layout)
- Added a dynamic preview panel that updates based on the selected style
- Preview panel shows a sample name, contact line, section header, and
  bullet points styled to match the chosen format
- Each style includes a written description below the preview

---

## Session 4 — App Restructure and UI Improvements

**Date:** 2026-06-11

**User feedback:**
- App needed a homepage with two clear paths:
  1. Generate New Documents (existing workflow)
  2. Evaluate Existing Documents (new workflow)
- Style preview boxes looked like buttons but were not clickable — confusing
- Path selection boxes looked like buttons but were not clickable — confusing
- Button colors were jarring (red primary button stood out too much)
- Evaluation log needed a built-in way to generate scores automatically

**Changes applied:**
- Rebuilt app.py with a homepage that routes users to Path 1 or Path 2
- Path 1: Generate New Documents (existing workflow, now with evaluation
  button at the end)
- Path 2: Evaluate Existing Documents (new workflow — upload or paste
  existing resume/cover letter, get scored feedback across five dimensions)
- Path 2 includes warning when text is pasted instead of file uploaded,
  noting that Visual Structure cannot be evaluated from text
- Path 2 includes option to switch to Path 1 after evaluation
- Style selector preview boxes replaced with radio buttons and dynamic
  preview panel
- Path selection redesigned as two large clickable buttons with descriptions
  built into the button text
- Primary button color changed from red to blue (#0065A4) to match app theme
- Evaluate My Documents button added at end of Path 1 review section

**Changes still in progress:**
- Full end-to-end testing of both paths
- Deployment to Streamlit Cloud

---