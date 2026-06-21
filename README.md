# Resume and Cover Letter Tailor

🔗 **Live App:** [Resume and Cover Letter Tailor](https://resume-cover-letter-tailor.streamlit.app/)

An AI-powered tool that helps job seekers tailor a resume and cover letter to a
specific job posting. Upload your CV, paste a job description, answer a few targeted
questions, and download polished, job-ready Word documents.

---

## What This Tool Does

- **Analyzes** a job posting to extract key requirements, skills, and keywords
- **Parses** your uploaded CV to understand your experience and qualifications
- **Asks** targeted clarifying questions to capture context the CV alone cannot provide
- **Generates** a tailored resume and/or cover letter as downloadable Word documents
- **Offers four resume styles** — Classic, Modern, Bold, and Academic
- **Offers four cover letter tones** — Professional, Conversational, Confident, and Mission-Driven
- **Accepts feedback** and revises documents based on specific user requests
- **Allows style and tone changes** after generation without restarting the workflow
- **Evaluates** documents using a Smart Evaluation Tool powered by model-driven
  tool calling — Claude autonomously decides which evaluation tools to invoke
- **Scores ATS compatibility** — estimates how well a resume would perform
  against Applicant Tracking Systems used by employers
- **Generates interview preparation guides** — likely questions, talking points,
  and suggested questions to ask the interviewer
- **Tracks session history** — all documents generated in a session are
  accessible for download without losing previous versions
- **Supports back navigation** on the questions page with answer preservation

## Agentic Tool Use

The Smart Evaluation Tool demonstrates genuine agentic behavior using the
Anthropic tool use API. Three tools are defined with full JSON schemas and passed
to Claude Opus via the `tools=` parameter:

- **`evaluate_resume_fit`** — evaluates how well a resume matches a job posting
  across five dimensions
- **`evaluate_cover_letter_fit`** — evaluates how well a cover letter matches
  a job posting across five dimensions
- **`calculate_ats_score`** — calculates an ATS compatibility score by checking
  keyword density, formatting, and section completeness

Claude autonomously selects which tools to invoke using `tool_choice="auto"` —
the model examines the available documents and decides independently which
evaluation tools are needed, without Python hardcoding the sequence. Python
then executes the tools Claude selected and synthesizes a final report. This
satisfies the model-driven tool selection requirement — the model, not Python,
is making the decisions.

---

## How to Use

### Path 1 — Build My Documents

**Step 1 — Upload and Input**
1. Upload your CV or resume (PDF or Word) or paste as text
2. Optionally upload an existing cover letter for tone and style reference
3. Paste the full job posting into the text box
4. Click **Build My Documents**

**Step 2 — Choose Style and Tone**
1. Select what you want to generate — Resume, Cover Letter, or both
2. Choose a resume style: Classic, Modern, Bold, or Academic
3. Choose a cover letter tone: Professional, Conversational, Confident, or Mission-Driven
4. Click **Next Step →**

**Step 3 — Answer Clarifying Questions**
1. Answer each question to help tailor your documents
2. Use **← Back** to revisit and edit previous answers at any time
3. Click **Generate Documents** when all questions are answered

**Step 4 — Review and Revise**
1. Review your documents in the **Your Documents & Download** tab
2. Use the feedback boxes to request specific changes and click **Revise**
3. Change your resume style or cover letter tone at any time using the expanders
4. Use the **Smart Evaluation Tool** tab for scored feedback and ATS compatibility
5. Use the **Interview Prep** tab to generate interview questions and talking points
6. Access all documents generated this session in the **This Session** tab

**Step 5 — Download**
1. Click **Build Resume for Download** or **Build Cover Letter for Download**
2. Click the download button to save your Word document
3. Open in Microsoft Word or Google Docs for any final edits

---

### Path 2 — Evaluate My Documents

**Step 1 — Upload and Input**
1. Upload your existing resume and/or cover letter (PDF or Word) or paste as text
2. Paste the full job posting into the text box
3. Click **Evaluate My Documents**

**Step 2 — Review Your Results**
1. Review your **Smart Evaluation Report** with scores across five dimensions
   and an ATS compatibility score
2. Use the **Interview Prep** tab to generate interview preparation materials
3. Click **Switch to Generate New Documents** to create improved versions
---

## Setup Instructions

> **Note for new coders:** Follow these steps exactly, one at a time.

### Step 1 — Make sure Python is installed
```bash
python --version
```
You should see `Python 3.11.x` or higher.

### Step 2 — Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/resume-cover-letter-tailor.git
cd resume-cover-letter-tailor
```

### Step 3 — Create a virtual environment
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 4 — Install required packages
```bash
pip install -r requirements.txt
```

### Step 5 — Add your Anthropic API key
Create a file called `.env` in the root folder and add:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### Step 6 — Run the app
```bash
streamlit run app.py
```

---

## Evaluation Criteria

Documents generated by this tool are scored on five dimensions:

| Dimension | Passing Score | What It Measures |
|-----------|--------------|------------------|
| Keyword Alignment | 4 or higher | Resume/cover letter uses language from the job posting |
| Relevance | 4 or higher | Most pertinent experience is highlighted, irrelevant content removed |
| Tone and Professionalism | 4 or higher | Writing is polished and appropriate for the industry |
| Visual Structure | 3 or higher | Document is clean, scannable, and professionally formatted |
| Completeness | 4 or higher | All required sections are present and well-developed |

---

## Known Limitations

- The tool works best when the job posting is detailed and specific
- Very long CVs (10+ pages) may require more targeted clarifying questions
- Visual formatting in Word documents may need minor adjustments depending on
  the version of Word or Google Docs used to open them
- The tool is currently optimized for professional and academic job postings
- Saved documents do not persist on the deployed version; download before closing

---

## Build Log

### Project Design Decisions

**Why conversational clarifying questions?**
A CV alone cannot capture everything relevant to a specific job posting. The question
phase allows the AI to gather context that is not in the CV — such as which
accomplishments to emphasize, preferred tone, or specific projects most relevant to
the role.

**Why a feedback loop?**
Generated documents are a starting point, not a final product. The feedback loop
allows users to request specific changes to content and visual structure before
downloading, ensuring the final document truly represents them.

**Why Word documents?**
Word documents are the standard format for job applications. They are editable,
widely accepted by applicant tracking systems, and easy to open on any device.

**Why three different AI models?**
- **Claude Opus** is used for job analysis, document review, smart evaluation,
  and interview preparation because these tasks require the deepest reasoning
- **Claude Sonnet** is used for writing, revision, ATS scoring, and evaluation
  summaries because these tasks require creativity and content quality
- **Claude Haiku** is used for CV parsing because this is a structured task
  that does not require deep reasoning

### Known Weaknesses
- Visual formatting options are limited to what python-docx supports
- The tool cannot access URLs directly; job postings must be pasted as text
- Saved documents do not persist on the deployed version