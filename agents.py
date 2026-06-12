import anthropic
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
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
    """Review a document using the Reviewer agent (Opus)."""
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

Score each dimension 1-5 and give an overall verdict of APPROVED or NEEDS REVISION.
If NEEDS REVISION, list specific required changes.
"""}
        ]
    )
    return message.content[0].text


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