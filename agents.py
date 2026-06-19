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
    Claude decides which tools to call based on available content."""
    domain_primer = load_domain_primer()
    rubric = load_evaluation_rubric()

    # Define the tools Claude can call
    tools = [
        {
            "name": "evaluate_resume_fit",
            "description": (
                "Evaluates how well a resume matches a job posting across "
                "five dimensions: keyword alignment, relevance, tone and "
                "professionalism, visual structure, and completeness. "
                "Use this tool when a resume is available to evaluate."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "resume_text": {
                        "type": "string",
                        "description": "The full text of the resume to evaluate"
                    },
                    "job_analysis": {
                        "type": "string",
                        "description": "The analyzed job posting requirements"
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional specific areas to focus on"
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
                "and professionalism, visual structure, and completeness. "
                "Use this tool when a cover letter is available to evaluate."
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
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional specific areas to focus on"
                    }
                },
                "required": ["cover_letter_text", "job_analysis"]
            }
        }
    ]

    # Build the user message based on what content is available
    available_docs = []
    if resume_content.strip():
        available_docs.append("a resume")
    if cover_letter_content.strip():
        available_docs.append("a cover letter")
    docs_description = " and ".join(available_docs)

    # First call — Claude decides which tools to use
    messages = [
        {
            "role": "user",
            "content": (
                f"I have {docs_description} that need to be evaluated "
                f"against a job posting. Please use the available tools "
                f"to evaluate the documents and tell me how well they fit "
                f"the role.\n\n"
                f"RESUME:\n{resume_content}\n\n"
                f"COVER LETTER:\n{cover_letter_content}\n\n"
                f"JOB ANALYSIS:\n{job_analysis}"
            )
        }
    ]

    response = client.messages.create(
        model=OPUS,
        max_tokens=2000,
        tools=tools,
        tool_choice={"type": "auto"},
        system=(
            f"You are a senior hiring manager and career coach. "
            f"You have access to evaluation tools. Use them to assess "
            f"the provided documents against the job posting. "
            f"Use evaluate_resume_fit if a resume is provided. "
            f"Use evaluate_cover_letter_fit if a cover letter is provided. "
            f"After calling the tools, provide a clear conversational "
            f"summary of your findings.\n\n"
            f"Domain knowledge:\n{domain_primer}\n\n"
            f"Scoring rubric:\n{rubric}"
        ),
        messages=messages
    )

    # Process tool calls Claude decided to make
    tool_results = []
    final_text = []

    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input

            # Execute the tool Claude called
            if tool_name == "evaluate_resume_fit":
                result = review_document(
                    resume_content,
                    job_analysis,
                    "Resume"
                )
            elif tool_name == "evaluate_cover_letter_fit":
                result = review_document(
                    cover_letter_content,
                    job_analysis,
                    "Cover Letter"
                )
            else:
                result = "Tool not recognized."

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

        elif block.type == "text" and block.text:
            final_text.append(block.text)

    # If Claude called tools, send results back for final summary
    if tool_results:
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        messages.append({
            "role": "user",
            "content": tool_results
        })

        final_response = client.messages.create(
            model=OPUS,
            max_tokens=2000,
            tools=tools,
            system=(
                f"You are a senior hiring manager and career coach. "
                f"Based on the tool results, provide a clear, well-formatted "
                f"evaluation report. Include the scorecard tables from the "
                f"tool results and add a brief overall summary and "
                f"actionable recommendations.\n\n"
                f"Domain knowledge:\n{domain_primer}"
            ),
            messages=messages
        )

        return "\n\n".join([
            block.text for block in final_response.content
            if hasattr(block, "text") and block.text
        ])

    # If no tools were called, return any text Claude produced
    return "\n\n".join(final_text) if final_text else "Evaluation could not be completed."

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