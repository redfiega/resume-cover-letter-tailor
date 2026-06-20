import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# Model names for each tier
OPUS = "claude-opus-4-5"
SONNET = "claude-sonnet-4-5"
HAIKU = "claude-haiku-4-5-20251001"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompt-library folder."""
    path = os.path.join("prompt-library", filename)
    with open(path, "r") as f:
        return f.read()


def load_domain_primer() -> str:
    """Load the domain primer for context."""
    with open("domain-primer.md", "r") as f:
        return f.read()


def load_evaluation_rubric() -> str:
    """Load the evaluation rubric for scoring guidance."""
    with open("evaluation.md", "r") as f:
        return f.read()


def analyze_job_posting(job_posting: str) -> str:
    """Analyze a job posting using the Job Analyzer agent (Opus)."""
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("analyze-job-posting.txt")

    prompt = prompt_template.replace("{JOB_POSTING}", job_posting)

    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are an expert recruiter and hiring manager. "
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def parse_cv(cv_text: str) -> str:
    """Parse and structure CV content using the CV Parser agent (Haiku)."""
    prompt_template = load_prompt("parse-cv.txt")
    prompt = prompt_template.replace("{CV_TEXT}", cv_text)

    message = client.messages.create(
        model=HAIKU,
        max_tokens=3000,
        system="You are an expert at reading and structuring professional documents. "
               "Extract all content from the CV and organize it into clearly labeled "
               "sections. Preserve everything — nothing should be lost in parsing.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def generate_questions(cv_content: str, job_analysis: str) -> str:
    """Generate clarifying questions using the Question Generator agent (Sonnet)."""
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("generate-questions.txt")

    prompt = prompt_template.replace("{CV_CONTENT}", cv_content)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)

    message = client.messages.create(
        model=SONNET,
        max_tokens=1000,
        system=(f"You are a career coach helping a job seeker prepare their "
                f"application. Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def write_resume(cv_content: str, job_analysis: str,
                 user_answers: str) -> str:
    """Generate a tailored resume using the Resume Writer agent (Sonnet)."""
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
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def write_cover_letter(cv_content: str, job_analysis: str,
                       user_answers: str, resume_content: str) -> str:
    """Generate a tailored cover letter using the Cover Letter Writer (Sonnet)."""
    domain_primer = load_domain_primer()
    prompt_template = load_prompt("write-cover-letter.txt")

    prompt = prompt_template.replace("{CV_CONTENT}", cv_content)
    prompt = prompt.replace("{JOB_ANALYSIS}", job_analysis)
    prompt = prompt.replace("{USER_ANSWERS}", user_answers)
    prompt = prompt.replace("{RESUME_CONTENT}", resume_content)

    message = client.messages.create(
        model=SONNET,
        max_tokens=2000,
        system=(f"You are an expert cover letter writer. "
                f"Here is your domain knowledge:\n\n{domain_primer}"),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def review_document(document_content: str, job_analysis: str,
                    document_type: str) -> str:
    """Review a document using the Reviewer agent (Opus).
    Returns a consistently formatted evaluation report."""
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()

    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are a senior hiring manager reviewing application documents. "
                f"Here is your domain knowledge:\n\n{domain_primer}\n\n"
                f"Here is your scoring rubric:\n\n{rubric}"),
        messages=[
            {"role": "user", "content": f"""
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
"""}
        ]
    )
    return message.content[0].text


def review_document_no_visual(document_content: str, job_analysis: str,
                               document_type: str) -> str:
    """Review a document but skip Visual Structure scoring.
    Used when document is provided as pasted text rather than a file."""
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()

    message = client.messages.create(
        model=OPUS,
        max_tokens=1500,
        system=(f"You are a senior hiring manager reviewing application documents. "
                f"Here is your domain knowledge:\n\n{domain_primer}\n\n"
                f"Here is your scoring rubric:\n\n{rubric}"),
        messages=[
            {"role": "user", "content": f"""
Review this {document_type} against the job analysis below.
IMPORTANT: Do NOT score Visual Structure — the document was provided as
plain text so visual formatting cannot be assessed.

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
| Visual Structure | Not evaluated | Document provided as plain text |
| Completeness | X/5 | [one line] |

**Overall Verdict:** APPROVED or NEEDS REVISION
Note: Verdict based on four scoreable dimensions only.

**Required Changes** (if NEEDS REVISION, otherwise write "None")
1. [specific change]

**Suggestions**
- [optional improvement]
"""}
        ]
    )
    return message.content[0].text

def smart_evaluate(resume_content: str, cover_letter_content: str,
                   job_analysis: str) -> str:
    """Smart evaluation using model-callable tools.
    Claude is given tools with JSON schemas and decides to invoke them.
    Results are collected and synthesized into a final report."""
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()

    # Define tools with full JSON schemas
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
                    "resume_text": {
                        "type": "string",
                        "description": "The full text of the resume"
                    },
                    "job_analysis": {
                        "type": "string",
                        "description": "The analyzed job posting requirements"
                    }
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
                    "cover_letter_text": {
                        "type": "string",
                        "description": "The full text of the cover letter"
                    },
                    "job_analysis": {
                        "type": "string",
                        "description": "The analyzed job posting requirements"
                    }
                },
                "required": ["cover_letter_text", "job_analysis"]
            }
        }
    ]

    evaluation_reports = []
    tool_results_for_summary = []

    # Use tool_choice to force each evaluation independently
    if resume_content.strip():
        resume_messages = [
            {
                "role": "user",
                "content": (
                    f"Evaluate this resume against the job analysis.\n\n"
                    f"RESUME:\n{resume_content}\n\n"
                    f"JOB ANALYSIS:\n{job_analysis}"
                )
            }
        ]
        resume_response = client.messages.create(
            model=OPUS,
            max_tokens=500,
            tools=tools,
            tool_choice={"type": "tool", "name": "evaluate_resume_fit"},
            system=f"You are a senior hiring manager. {domain_primer}",
            messages=resume_messages
        )
        # Execute the tool Claude was forced to call
        result = review_document(resume_content, job_analysis, "Resume")
        evaluation_reports.append(f"## Resume Evaluation\n\n{result}")
        tool_results_for_summary.append(f"Resume Evaluation:\n{result}")

    if cover_letter_content.strip():
        cl_messages = [
            {
                "role": "user",
                "content": (
                    f"Evaluate this cover letter against the job analysis.\n\n"
                    f"COVER LETTER:\n{cover_letter_content}\n\n"
                    f"JOB ANALYSIS:\n{job_analysis}"
                )
            }
        ]
        cl_response = client.messages.create(
            model=OPUS,
            max_tokens=500,
            tools=tools,
            tool_choice={"type": "tool", "name": "evaluate_cover_letter_fit"},
            system=f"You are a senior hiring manager. {domain_primer}",
            messages=cl_messages
        )
        # Execute the tool Claude was forced to call
        result = review_document(
            cover_letter_content, job_analysis, "Cover Letter"
        )
        evaluation_reports.append(f"## Cover Letter Evaluation\n\n{result}")
        tool_results_for_summary.append(f"Cover Letter Evaluation:\n{result}")

    if not evaluation_reports:
        return "No documents were available to evaluate."

    # Generate a brief overall summary using Sonnet
    summary_prompt = (
        "Based on these evaluation results, write a brief 2-3 sentence "
        "overall summary and the top 2 action items.\n\n" +
        "\n\n".join(tool_results_for_summary)
    )
    summary_response = client.messages.create(
        model=SONNET,
        max_tokens=500,
        system="You are a career coach providing concise, actionable feedback.",
        messages=[{"role": "user", "content": summary_prompt}]
    )

    summary_text = ""
    for block in summary_response.content:
        if hasattr(block, "text") and block.text:
            summary_text = block.text
            break

    # Build the complete report
    full_report = "\n\n---\n\n".join(evaluation_reports)
    if summary_text:
        full_report = (
            f"**Overall Summary**\n\n{summary_text}\n\n---\n\n{full_report}"
        )

    return full_report

    # If no tools were called, return a message
    return "No documents were available to evaluate. Please make sure you have generated at least one document."

def revise_document(current_content: str, user_feedback: str,
                    job_analysis: str) -> str:
    """Revise a document based on user feedback using the Revision Agent (Sonnet)."""
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
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text