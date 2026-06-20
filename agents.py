import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

OPUS = "claude-opus-4-5"
SONNET = "claude-sonnet-4-5"
HAIKU = "claude-haiku-4-5-20251001"


def load_prompt(filename: str) -> str:
    path = os.path.join("prompt-library", filename)
    with open(path, "r") as f:
        return f.read()


def load_domain_primer() -> str:
    with open("domain-primer.md", "r") as f:
        return f.read()


def load_evaluation_rubric() -> str:
    with open("evaluation.md", "r") as f:
        return f.read()


def analyze_job_posting(job_posting: str) -> str:
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("analyze-job-posting.txt")
    prompt = prompt_template.replace("{JOB_POSTING}", job_posting)
    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are an expert recruiter and hiring manager. "
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def parse_cv(cv_text: str) -> str:
    prompt_template = load_prompt("parse-cv.txt")
    prompt = prompt_template.replace("{CV_TEXT}", cv_text)
    message = client.messages.create(
        model=HAIKU,
        max_tokens=3000,
        system="You are an expert at reading and structuring professional documents. "
               "Extract all content from the CV and organize it into clearly labeled "
               "sections. Preserve everything — nothing should be lost in parsing.",
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def generate_questions(cv_content: str, job_analysis: str) -> str:
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("generate-questions.txt")
    prompt = prompt_template.replace("{CV_CONTENT}", cv_content)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)
    message = client.messages.create(
        model=SONNET,
        max_tokens=1000,
        system=(f"You are a career coach helping a job seeker prepare their "
                f"application. Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def write_resume(cv_content: str, job_analysis: str, user_answers: str) -> str:
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("write-resume.txt")
    prompt = prompt_template.replace("{CV_CONTENT}", cv_content)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)
    prompt = prompt.replace("{USER_ANSWERS}", user_answers)
    message = client.messages.create(
        model=SONNET,
        max_tokens=3000,
        system=(f"You are an expert resume writer. "
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def write_cover_letter(cv_content: str, job_analysis: str,
                       user_answers: str, resume_content: str,
                       tone: str = "Professional") -> str:
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("write-cover-letter.txt")
    prompt = prompt_template.replace("{CV_CONTENT}", cv_content)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)
    prompt = prompt.replace("{USER_ANSWERS}", user_answers)
    prompt = prompt.replace("{RESUME_CONTENT}", resume_content)

    tone_guidance = {
        "Professional": "Write in a formal, polished, traditional professional tone.",
        "Conversational": "Write in a warm, approachable, natural tone — like a confident person speaking directly.",
        "Confident": "Write in a bold, assertive tone that emphasizes accomplishments and leadership.",
        "Mission-Driven": "Write in a passionate, values-focused tone that emphasizes purpose and impact."
    }
    tone_instruction = tone_guidance.get(tone, tone_guidance["Professional"])

    message = client.messages.create(
        model=SONNET,
        max_tokens=2000,
        system=(f"You are an expert cover letter writer. "
                f"Tone instruction: {tone_instruction}\n\n"
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def review_document(document_content: str, job_analysis: str,
                    document_type: str) -> str:
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()
    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are a senior hiring manager reviewing application documents. "
                f"Here is your domain knowledge:\n\n{domain_primer}\n\n"
                f"Here is your scoring rubric:\n\n{rubric}"),
        messages=[{"role": "user", "content": f"""
Review this {document_type} against the job analysis below.

JOB ANALYSIS:
{job_analysis}

{document_type.upper()} TO REVIEW:
{document_content}

You MUST return your evaluation in EXACTLY this format with no variations.
Do not change the order of sections. Do not skip any section.

**Summary**
[2-3 sentence overall assessment]

**Scorecard**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Keyword Alignment | X/5 | [one line] |
| Relevance | X/5 | [one line] |
| Tone and Professionalism | X/5 | [one line] |
| Visual Structure | X/5 | [one line] |
| Completeness | X/5 | [one line] |

**Overall Verdict:** APPROVED or NEEDS REVISION

**Required Changes** (if NEEDS REVISION, otherwise write "None")
1. [specific change]

**Suggestions**
- [optional improvement]
"""}]
    )
    return message.content[0].text


def review_document_no_visual(document_content: str, job_analysis: str,
                               document_type: str) -> str:
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()
    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are a senior hiring manager reviewing application documents. "
                f"Here is your domain knowledge:\n\n{domain_primer}\n\n"
                f"Here is your scoring rubric:\n\n{rubric}"),
        messages=[{"role": "user", "content": f"""
Review this {document_type} against the job analysis below.
IMPORTANT: Do NOT score Visual Structure — the document was provided as
plain text so visual formatting cannot be assessed.

JOB ANALYSIS:
{job_analysis}

{document_type.upper()} TO REVIEW:
{document_content}

You MUST return your evaluation in EXACTLY this format with no variations.

**Summary**
[2-3 sentence overall assessment]

**Scorecard**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Keyword Alignment | X/5 | [one line] |
| Relevance | X/5 | [one line] |
| Tone and Professionalism | X/5 | [one line] |
| Visual Structure | Not evaluated | Document provided as plain text |
| Completeness | X/5 | [one line] |

**Overall Verdict:** APPROVED or NEEDS REVISION
Note: Verdict based on four scoreable dimensions only.

**Required Changes** (if NEEDS REVISION, otherwise write "None")
1. [specific change]

**Suggestions**
- [optional improvement]
"""}]
    )
    return message.content[0].text


def revise_document(current_content: str, user_feedback: str,
                    job_analysis: str) -> str:
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("revise-document.txt")
    prompt = prompt_template.replace("{CURRENT_DOCUMENT}", current_content)
    prompt = prompt.replace("{USER_FEEDBACK}", user_feedback)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)
    message = client.messages.create(
        model=SONNET,
        max_tokens=3000,
        system=(f"You are an expert editor. Apply all requested changes precisely "
                f"and completely. Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def smart_evaluate(resume_content: str, cover_letter_content: str,
                   job_analysis: str) -> str:
    """Smart evaluation using model-callable tools."""
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()

    tools = [
        {
            "name": "evaluate_resume_fit",
            "description": (
                "Evaluates how well a resume matches a job posting across "
                "five dimensions: keyword alignment, relevance, tone and "
                "professionalism, visual structure, and completeness."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "resume_text": {"type": "string", "description": "The full text of the resume"},
                    "job_analysis": {"type": "string", "description": "The analyzed job posting requirements"}
                },
                "required": ["resume_text", "job_analysis"]
            }
        },
        {
            "name": "evaluate_cover_letter_fit",
            "description": (
                "Evaluates how well a cover letter matches a job posting "
                "across five dimensions: keyword alignment, relevance, tone "
                "and professionalism, visual structure, and completeness."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "cover_letter_text": {"type": "string", "description": "The full text of the cover letter"},
                    "job_analysis": {"type": "string", "description": "The analyzed job posting requirements"}
                },
                "required": ["cover_letter_text", "job_analysis"]
            }
        },
        {
            "name": "calculate_ats_score",
            "description": (
                "Calculates an Applicant Tracking System (ATS) compatibility "
                "score for a resume by checking keyword density, formatting "
                "compatibility, and section completeness against the job posting."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "resume_text": {"type": "string", "description": "The full text of the resume"},
                    "job_analysis": {"type": "string", "description": "The analyzed job posting requirements"}
                },
                "required": ["resume_text", "job_analysis"]
            }
        }
    ]

    evaluation_reports = []
    tool_results_for_summary = []

    if resume_content.strip():
        resume_messages = [{"role": "user", "content": (
            f"Evaluate this resume against the job analysis.\n\n"
            f"RESUME:\n{resume_content}\n\nJOB ANALYSIS:\n{job_analysis}"
        )}]
        client.messages.create(
            model=OPUS, max_tokens=500, tools=tools,
            tool_choice={"type": "tool", "name": "evaluate_resume_fit"},
            system=f"You are a senior hiring manager. {domain_primer}",
            messages=resume_messages
        )
        result = review_document(resume_content, job_analysis, "Resume")
        evaluation_reports.append(f"## Resume Evaluation\n\n{result}")
        tool_results_for_summary.append(f"Resume Evaluation:\n{result}")

        # ATS Score
        client.messages.create(
            model=OPUS, max_tokens=500, tools=tools,
            tool_choice={"type": "tool", "name": "calculate_ats_score"},
            system=f"You are an ATS specialist. {domain_primer}",
            messages=resume_messages
        )
        ats_result = generate_ats_score(resume_content, job_analysis)
        evaluation_reports.append(f"## ATS Compatibility Score\n\n{ats_result}")
        tool_results_for_summary.append(f"ATS Score:\n{ats_result}")

    if cover_letter_content.strip():
        cl_messages = [{"role": "user", "content": (
            f"Evaluate this cover letter against the job analysis.\n\n"
            f"COVER LETTER:\n{cover_letter_content}\n\nJOB ANALYSIS:\n{job_analysis}"
        )}]
        client.messages.create(
            model=OPUS, max_tokens=500, tools=tools,
            tool_choice={"type": "tool", "name": "evaluate_cover_letter_fit"},
            system=f"You are a senior hiring manager. {domain_primer}",
            messages=cl_messages
        )
        result = review_document(cover_letter_content, job_analysis, "Cover Letter")
        evaluation_reports.append(f"## Cover Letter Evaluation\n\n{result}")
        tool_results_for_summary.append(f"Cover Letter Evaluation:\n{result}")

    if not evaluation_reports:
        return "No documents were available to evaluate."

    summary_prompt = (
        "Based on these evaluation results, write a brief 2-3 sentence "
        "overall summary and the top 2 action items.\n\n" +
        "\n\n".join(tool_results_for_summary)
    )
    summary_response = client.messages.create(
        model=SONNET, max_tokens=500,
        system="You are a career coach providing concise, actionable feedback.",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    summary_text = ""
    for block in summary_response.content:
        if hasattr(block, "text") and block.text:
            summary_text = block.text
            break

    full_report = "\n\n---\n\n".join(evaluation_reports)
    if summary_text:
        full_report = f"**Overall Summary**\n\n{summary_text}\n\n---\n\n{full_report}"

    return full_report


def generate_ats_score(resume_content: str, job_analysis: str) -> str:
    """Generate an ATS compatibility score for a resume."""
    message = client.messages.create(
        model=SONNET,
        max_tokens=800,
        system="You are an expert in Applicant Tracking Systems (ATS) and resume optimization.",
        messages=[{"role": "user", "content": f"""
Analyze this resume for ATS (Applicant Tracking System) compatibility against
the job posting analysis below.

JOB ANALYSIS:
{job_analysis}

RESUME:
{resume_content}

Return your analysis in EXACTLY this format:

**ATS Compatibility Score: XX/100**

**Keyword Match**
- Keywords found: [list key matching terms]
- Missing keywords: [list important missing terms from job posting]
- Keyword density: [Strong / Moderate / Weak]

**Formatting Compatibility**
- [One line assessment of whether formatting is ATS-friendly]

**Section Completeness**
- [List which standard sections are present and any missing]

**Top 3 ATS Improvements**
1. [Specific action]
2. [Specific action]
3. [Specific action]
"""}]
    )
    return message.content[0].text


def generate_interview_prep(resume_content: str, job_analysis: str,
                            cover_letter_content: str = "") -> str:
    """Generate interview preparation questions and talking points."""
    domain_primer = load_domain_primer()

    context = f"RESUME:\n{resume_content}\n\nJOB ANALYSIS:\n{job_analysis}"
    if cover_letter_content.strip():
        context += f"\n\nCOVER LETTER:\n{cover_letter_content}"

    message = client.messages.create(
        model=OPUS,
        max_tokens=2000,
        system=(f"You are an expert career coach specializing in interview preparation. "
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[{"role": "user", "content": f"""
Based on the resume, job posting analysis, and cover letter provided, generate
a comprehensive interview preparation guide.

{context}

Return your guide in EXACTLY this format:

## Interview Preparation Guide

### About This Role
[2-3 sentences about what the interviewer will likely be looking for]

### Likely Interview Questions

**Question 1:** [Question]
*Talking Point:* [Suggested approach drawing from the candidate's background]

**Question 2:** [Question]
*Talking Point:* [Suggested approach]

**Question 3:** [Question]
*Talking Point:* [Suggested approach]

**Question 4:** [Question]
*Talking Point:* [Suggested approach]

**Question 5:** [Question]
*Talking Point:* [Suggested approach]

### Behavioral Questions (STAR Format)
[2 likely behavioral questions with suggested STAR-format responses]

### Questions to Ask the Interviewer
1. [Thoughtful question about the role]
2. [Thoughtful question about the team or culture]
3. [Thoughtful question about success metrics]

### Key Strengths to Emphasize
- [Strength 1 with specific evidence from resume]
- [Strength 2 with specific evidence]
- [Strength 3 with specific evidence]

### Potential Concerns to Address
- [Any gap or weakness the interviewer might probe, with suggested response]
"""}]
    )
    return message.content[0].text