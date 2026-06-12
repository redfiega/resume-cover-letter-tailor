# Product Requirements Document (PRD)

## Project: Resume and Cover Letter Tailor

---

## 1. Problem Statement

Job seekers with long, exhaustive CVs face several pain points when applying for
specific positions:

- **Structural uncertainty:** It is hard to know how to organize a tailored resume
  from a long CV. Which sections come first? What should be cut?
- **Wording difficulty:** Academic or professional CV language does not always match
  the tone and keywords expected in a job application resume.
- **Content selection:** Deciding what to keep and what to remove for a specific
  posting requires careful reading of both the CV and the job description — a
  time-consuming and cognitively demanding task.
- **Cover letter paralysis:** Writing a compelling, tailored cover letter from scratch
  for every application is exhausting and often results in generic output.
- **No feedback mechanism:** Most AI writing tools generate a draft with no way to
  refine it without starting over.

---

## 2. Users

**Primary user:** A university professional with a long academic CV applying for
positions that require a focused resume and tailored cover letter.

**Secondary users:** Students and general job seekers who want to tailor their
existing resume or CV to a specific job posting.

---

## 3. In Scope (Prototype)

- Upload a CV in PDF or Word format
- Paste a job posting as text
- Select resume, cover letter, or both
- Conversational clarifying questions (3-5 per session)
- Generate tailored resume as a downloadable Word document
- Generate tailored cover letter as a downloadable Word document
- Feedback loop for content and visual structure revisions
- Repeat revision cycle until user is satisfied

---

## 4. Out of Scope (Prototype)

- Direct URL parsing of job postings
- LinkedIn or ATS integration
- Multiple CV uploads in one session
- Saving documents to a persistent cloud database
- Interview preparation features
- Salary negotiation guidance

---

## 5. Requirements

### REQ-01: CV Upload and Parsing
**Pain point:** Users have a long CV that needs to be understood before tailoring  
**Specification:** Accept PDF and Word CV uploads; extract and structure all content
including work experience, education, skills, publications, and awards  
**Value:** Eliminates manual copy-pasting; enables intelligent content selection

### REQ-02: Job Posting Analysis
**Pain point:** Users need to know what the employer is looking for  
**Specification:** Extract key requirements, preferred skills, keywords, tone, and
industry context from the pasted job posting  
**Value:** Ensures the tailored documents speak the employer's language

### REQ-03: Clarifying Questions
**Pain point:** CV alone cannot capture all relevant context  
**Specification:** Generate 3-5 targeted questions based on the gap between the CV
and the job posting; present them conversationally one at a time  
**Value:** Captures accomplishments, preferences, and context that improve output quality

### REQ-04: Document Generation
**Pain point:** Structuring, wording, and selecting content is time-consuming  
**Specification:** Generate a tailored resume and/or cover letter as Word documents
based on CV content, job analysis, and clarifying question answers  
**Value:** Produces a professional draft in minutes instead of hours

### REQ-05: Feedback Loop
**Pain point:** First drafts are never perfect; users need to refine  
**Specification:** Allow users to provide written feedback on content and visual
structure; revise documents accordingly; repeat until satisfied  
**Value:** Ensures the final document truly represents the user

### REQ-06: Word Document Download
**Pain point:** Users need a standard, editable format for submission  
**Specification:** Output documents in .docx format downloadable directly from the app  
**Value:** Documents are immediately usable with no format conversion needed

---

## 6. Success Criteria

- Generated resume requires no more than 10 minutes of editing before submission
- Cover letter sounds personal and specific, not generic
- All key terms from the job posting appear naturally in the documents
- Feedback is applied accurately within one revision cycle
- Word documents open correctly in Microsoft Word and Google Docs

---

## 7. Out of Scope Decisions Log

| Decision | Reason |
|----------|--------|
| No URL parsing | Requires web scraping; adds complexity beyond prototype scope |
| No ATS integration | Out of scope for prototype |
| No persistent storage | Privacy consideration; users download and keep their own documents |