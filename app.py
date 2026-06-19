import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    try:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass

from cv_parser import extract_cv_text
from agents import (
    analyze_job_posting,
    parse_cv,
    generate_questions,
    write_resume,
    write_cover_letter,
    review_document,
    review_document_no_visual,
    smart_evaluate,
    revise_document
)
from document_builder import (
    build_resume_document,
    build_cover_letter_document
)

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Resume & Cover Letter Tailor",
    page_icon="📄",
    layout="wide"
)

# Initialize session counter for widget key resets
if "session_count" not in st.session_state:
    st.session_state["session_count"] = 0

# Custom CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 0rem !important;
        max-width: 900px !important;
    }
    textarea {
        border: 2px solid #0065A4 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stTextArea"] textarea {
        border: 2px solid #0065A4 !important;
        border-radius: 6px !important;
        background-color: #f9f9f9 !important;
    }
    button[kind="primary"] {
        background-color: #0065A4 !important;
        border-color: #0065A4 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover {
        background-color: #004f82 !important;
    }
    button[kind="secondary"] {
        background-color: #f0f7ff !important;
        border: 2px solid #0065A4 !important;
        color: #0065A4 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #dceeff !important;
    }
    h2 {
        color: #0065A4 !important;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-size: 1.05rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.3rem !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }
    div[data-testid="stTabs"] button {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0065A4 0%, #003f6b 100%);
        padding: 32px 40px 28px 40px;
        border-radius: 0 0 12px 12px;
        margin-bottom: 24px;">
        <h1 style="
            color: white;
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 6px 0;">
            Resume &amp; Cover Letter Tailor
        </h1>
        <p style="
            font-size: 1rem;
            color: #cce4f7;
            margin: 0;">
            Upload your CV and a job posting — get a tailored,
            job-ready resume and cover letter in minutes.
        </p>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────
if st.session_state.get("path") is None:

    sc = st.session_state.get("session_count", 0)

    st.markdown("""
        <div style="display: flex; gap: 8px; margin-bottom: 16px;
            align-items: center; flex-wrap: wrap;">
            <span style="background: #0065A4; color: white; padding: 4px 14px;
                border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                1 · Your Documents
            </span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                border-radius: 20px; font-size: 0.85rem;">
                2 · Style
            </span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                border-radius: 20px; font-size: 0.85rem;">
                3 · Questions
            </span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                border-radius: 20px; font-size: 0.85rem;">
                4 · Review
            </span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                border-radius: 20px; font-size: 0.85rem;">
                5 · Download
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="
            background-color: #f0f7ff;
            border-left: 4px solid #0065A4;
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 16px;
            font-size: 0.95rem;
            color: #333;">
            Upload your CV or resume and paste a job posting, then choose
            whether to <strong>generate new documents</strong> or
            <strong>evaluate what you already have</strong>.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Your CV or Resume")
    cv_input_method = st.radio(
        "How would you like to provide your CV or Resume?",
        ["Upload a file (PDF or Word)", "Paste as text", "Skip"],
        horizontal=True,
        key=f"cv_input_method_{sc}"
    )

    cv_text = ""
    cv_file_name = ""

    if cv_input_method == "Upload a file (PDF or Word)":
        uploaded_cv = st.file_uploader(
            "Upload your CV or Resume (PDF or Word)",
            type=["pdf", "docx"],
            key=f"cv_upload_{sc}"
        )
        if uploaded_cv:
            with st.spinner("Reading your document..."):
                try:
                    cv_text = extract_cv_text(uploaded_cv)
                    cv_file_name = uploaded_cv.name
                    st.success(f"Uploaded: {uploaded_cv.name}")
                except Exception as e:
                    st.error(f"Could not read the file: {e}")

    elif cv_input_method == "Paste as text":
        cv_text = st.text_area(
            "Paste your CV or Resume here:",
            placeholder="Paste the full text of your CV or Resume here...",
            height=200,
            key=f"cv_paste_{sc}"
        )

    st.markdown("### Existing Cover Letter *(optional)*")
    cl_input_method = st.radio(
        "How would you like to provide your cover letter?",
        ["Upload a file (PDF or Word)", "Paste as text", "Skip"],
        horizontal=True,
        key=f"cl_input_method_home_{sc}"
    )

    cl_text = ""

    if cl_input_method == "Upload a file (PDF or Word)":
        uploaded_cl = st.file_uploader(
            "Upload your cover letter (PDF or Word)",
            type=["pdf", "docx"],
            key=f"cl_upload_home_{sc}"
        )
        if uploaded_cl:
            with st.spinner("Reading your cover letter..."):
                try:
                    cl_text = extract_cv_text(uploaded_cl)
                    st.success(f"Uploaded: {uploaded_cl.name}")
                except Exception as e:
                    st.error(f"Could not read the file: {e}")

    elif cl_input_method == "Paste as text":
        cl_text = st.text_area(
            "Paste your cover letter here:",
            placeholder="Paste the full text of your cover letter here...",
            height=150,
            key=f"cl_paste_home_{sc}"
        )

    st.markdown("### Job Posting")
    job_posting = st.text_area(
        "Paste the job posting here:",
        placeholder="Copy and paste the full job description here...",
        height=200,
        key=f"job_posting_input_{sc}"
    )

    st.markdown("### Choose Your Path")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(
            "Build My Documents\n\nGenerate a new tailored resume and/or "
            "cover letter based on your CV and the job posting.",
            type="primary",
            use_container_width=True,
            key=f"path1_button_{sc}"
        ):
            if not cv_text.strip():
                st.warning("Please provide your CV or Resume before "
                           "generating new documents.")
            elif not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            else:
                with st.spinner("Reading your documents and analyzing the "
                                "job posting... this may take 20-30 seconds."):
                    try:
                        cv_content = parse_cv(cv_text)
                        job_analysis = analyze_job_posting(job_posting)
                        questions = generate_questions(cv_content, job_analysis)
                        st.session_state["cv_content"] = cv_content
                        st.session_state["cl_content"] = cl_text
                        st.session_state["job_analysis"] = job_analysis
                        st.session_state["job_posting"] = job_posting
                        st.session_state["questions"] = questions
                        st.session_state["path"] = "generate"
                        st.session_state["step"] = "style"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    with col_b:
        if st.button(
            "Evaluate My Documents\n\nGet scored feedback on your existing "
            "resume and/or cover letter based on the job posting.",
            use_container_width=True,
            key=f"path2_button_{sc}"
        ):
            if not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            elif not cv_text.strip() and not cl_text.strip():
                st.warning("Please provide at least one document to evaluate.")
            else:
                with st.spinner("Analyzing the job posting..."):
                    try:
                        job_analysis = analyze_job_posting(job_posting)
                        st.session_state["job_analysis"] = job_analysis
                        st.session_state["job_posting"] = job_posting
                        st.session_state["cv_text_for_eval"] = cv_text
                        st.session_state["cl_text_for_eval"] = cl_text
                        st.session_state["cv_input_method"] = cv_input_method
                        st.session_state["cl_input_method"] = cl_input_method
                        st.session_state["path"] = "evaluate"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────
# PATH 1 — GENERATE NEW DOCUMENTS
# ─────────────────────────────────────────
elif st.session_state.get("path") == "generate":

    if st.session_state.get("step") == "style":
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px;
                align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    1 · Documents
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    2 · Style
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    3 · Questions
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    4 · Review
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    5 · Download
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## Choose a Document Style")

        selected_style = st.radio(
            "Select a style:",
            ["Classic", "Modern", "Bold", "Academic"],
            horizontal=True,
            index=1
        )

        style_previews = {
            "Classic": {
                "description": "Clean black and white formatting with Times New "
                               "Roman font. Traditional and widely accepted.",
                "name_color": "#000000",
                "header_color": "#000000",
                "background": "#ffffff",
                "font": "Times New Roman"
            },
            "Modern": {
                "description": "Blue accents with Calibri font. Clean and "
                               "contemporary, works well for most professional roles.",
                "name_color": "#0065A4",
                "header_color": "#0065A4",
                "background": "#ffffff",
                "font": "Calibri"
            },
            "Bold": {
                "description": "Dark navy header backgrounds with white text. "
                               "High contrast and visually striking.",
                "name_color": "#ffffff",
                "header_color": "#ffffff",
                "background": "#1F497D",
                "font": "Calibri"
            },
            "Academic": {
                "description": "Formal black text with underlined section headers "
                               "and Georgia font. Best for academic roles.",
                "name_color": "#000000",
                "header_color": "#000000",
                "background": "#ffffff",
                "font": "Georgia"
            }
        }

        preview = style_previews[selected_style]
        st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px;
                padding: 16px; margin: 8px 0; background-color: #fafafa;">
                <p style="margin: 0 0 8px 0; color: #555; font-size: 0.85rem;">
                    <strong>Preview — {selected_style}</strong></p>
                <div style="background-color: white; border: 1px solid #eee;
                    padding: 16px; font-family: {preview['font']}, serif;">
                    <p style="font-size: 16px; font-weight: bold;
                        color: {preview['name_color']};
                        background-color: {preview['background']};
                        padding: 4px 8px; margin: 0 0 6px 0;">Your Name</p>
                    <p style="font-size: 10px; color: #555; margin: 0 0 10px 0;">
                        your.email@example.com | (555) 123-4567 | City, State
                    </p>
                    <p style="font-size: 10px; font-weight: bold;
                        color: {preview['header_color']};
                        background-color: {preview['background']};
                        padding: 2px 4px; margin: 0 0 4px 0;
                        border-bottom: 1px solid #ccc;">
                        PROFESSIONAL EXPERIENCE</p>
                    <p style="font-size: 9px; color: #333; margin: 0;">
                        • Led curriculum redesign increasing pass rates by 14%<br>
                        • Managed cross-functional team of 6 designers</p>
                </div>
                <p style="margin: 8px 0 0 0; color: #666; font-size: 0.82rem;">
                    {preview['description']}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### What would you like to generate?")
        generate_resume = st.checkbox("Resume", value=True)
        generate_cover_letter = st.checkbox("Cover Letter", value=True)

        if st.button("Next Step →", type="primary"):
            if not generate_resume and not generate_cover_letter:
                st.warning("Please select at least one document to generate.")
            else:
                st.session_state["selected_style"] = selected_style
                st.session_state["generate_resume"] = generate_resume
                st.session_state["generate_cover_letter"] = generate_cover_letter
                st.session_state["step"] = "questions"
                st.rerun()

    elif st.session_state.get("step") in ["questions", "generating"]:
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px;
                align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    1 · Documents
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    2 · Style
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    3 · Questions
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    4 · Review
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    5 · Download
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## A Few Quick Questions")
        st.caption("These help tailor your documents more precisely.")

        if "question_list" not in st.session_state:
            raw_questions = st.session_state.get("questions", "")
            lines = raw_questions.split("\n")
            question_list = []
            for line in lines:
                line = line.strip()
                if line.startswith("**Question"):
                    question_text = line.replace("**", "").strip()
                    question_list.append(question_text)
            st.session_state["question_list"] = question_list
            st.session_state["current_question_index"] = 0
            st.session_state["question_answers"] = []

        question_list = st.session_state.get("question_list", [])
        current_index = st.session_state.get("current_question_index", 0)
        answers = st.session_state.get("question_answers", [])
        total_questions = len(question_list)

        if total_questions > 0:
            st.progress(current_index / total_questions)
            st.caption(f"Question {min(current_index + 1, total_questions)} "
                       f"of {total_questions}")

        if answers:
            with st.expander("Your answers so far"):
                for i, (q, a) in enumerate(
                    zip(question_list[:len(answers)], answers)
                ):
                    st.write(f"**{q}**")
                    st.write(f"_{a}_")
                    st.divider()

        if current_index < total_questions:
            current_question = question_list[current_index]
            st.markdown(f"### {current_question}")

            current_answer = st.text_area(
                "Your answer:",
                placeholder="Type your answer here...",
                height=120,
                key=f"answer_{current_index}"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Next →", type="primary"):
                    if not current_answer.strip():
                        st.warning(
                            "Please answer the question before continuing."
                        )
                    else:
                        answers.append(current_answer)
                        st.session_state["question_answers"] = answers
                        st.session_state["current_question_index"] = \
                            current_index + 1
                        st.rerun()

        if current_index >= total_questions and total_questions > 0:
            st.success("All questions answered!")
            user_answers = "\n\n".join([
                f"Q: {q}\nA: {a}"
                for q, a in zip(question_list, answers)
            ])

            if st.button("Generate Documents", type="primary"):
                st.session_state["user_answers"] = user_answers
                st.session_state["step"] = "generating"

                with st.spinner("Generating your tailored documents... "
                                "this may take 30-60 seconds."):
                    try:
                        cv_content = st.session_state["cv_content"]
                        job_analysis = st.session_state["job_analysis"]
                        cl_context = st.session_state.get("cl_content", "")

                        if cl_context.strip():
                            user_answers_with_context = (
                                user_answers +
                                f"\n\nExisting cover letter for style/tone "
                                f"reference:\n{cl_context}"
                            )
                        else:
                            user_answers_with_context = user_answers

                        if st.session_state.get("generate_resume"):
                            resume_content = write_resume(
                                cv_content, job_analysis,
                                user_answers_with_context
                            )
                            st.session_state["resume_content"] = resume_content

                        if st.session_state.get("generate_cover_letter"):
                            resume_for_cl = st.session_state.get(
                                "resume_content", "No resume generated"
                            )
                            cover_letter_content = write_cover_letter(
                                cv_content, job_analysis,
                                user_answers_with_context, resume_for_cl
                            )
                            st.session_state["cover_letter_content"] = \
                                cover_letter_content

                        st.session_state["step"] = "review"
                        st.rerun()

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    if st.session_state.get("step") in ["review", "revision"]:
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px;
                align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    1 · Documents
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    2 · Style
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    3 · Questions
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    4 · Review
                </span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px;
                    border-radius: 20px; font-size: 0.85rem;">
                    5 · Download
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="
                background-color: #f0f7ff;
                border-left: 4px solid #0065A4;
                border-radius: 6px;
                padding: 10px 16px;
                margin-bottom: 12px;
                font-size: 0.9rem;
                color: #333;">
                Use the tabs below to switch between reviewing your documents
                and running a Smart Evaluation.
            </div>
        """, unsafe_allow_html=True)

        tab_docs, tab_eval = st.tabs([
            "📋  Your Documents & Download",
            "📊  Smart Evaluation Tool"
        ])

        with tab_docs:
            st.markdown("## Review Your Documents")
            st.caption("Review and request changes before downloading.")

            if st.session_state.get("generate_resume") and \
                    "resume_content" in st.session_state:
                st.markdown("### Your Tailored Resume")
                st.markdown(st.session_state["resume_content"])

                st.markdown("""
                    <div style="border: 2px solid #0065A4; border-radius: 8px;
                        padding: 12px; margin: 10px 0; background-color: #f0f7ff;">
                        <strong>Provide Feedback on Your Resume</strong><br>
                        <span style="font-size: 0.9rem; color: #555;">
                        Request changes to content or formatting below.</span>
                    </div>
                """, unsafe_allow_html=True)

                resume_feedback = st.text_area(
                    "What would you like to change?",
                    placeholder="Example: Make the summary shorter. "
                                "Move education to the top.",
                    height=80,
                    key="resume_feedback"
                )

                if st.button("Revise Resume"):
                    if not resume_feedback.strip():
                        st.warning("Please enter feedback before revising.")
                    else:
                        with st.spinner("Revising your resume..."):
                            try:
                                revised = revise_document(
                                    st.session_state["resume_content"],
                                    resume_feedback,
                                    st.session_state["job_analysis"]
                                )
                                st.session_state["resume_content"] = revised
                                st.session_state["step"] = "revision"
                                st.success("Resume revised!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            if st.session_state.get("generate_cover_letter") and \
                    "cover_letter_content" in st.session_state:
                st.markdown("### Your Tailored Cover Letter")
                st.markdown(st.session_state["cover_letter_content"])

                st.markdown("""
                    <div style="border: 2px solid #0065A4; border-radius: 8px;
                        padding: 12px; margin: 10px 0; background-color: #f0f7ff;">
                        <strong>Provide Feedback on Your Cover Letter</strong><br>
                        <span style="font-size: 0.9rem; color: #555;">
                        Request changes to content or formatting below.</span>
                    </div>
                """, unsafe_allow_html=True)

                cl_feedback = st.text_area(
                    "What would you like to change?",
                    placeholder="Example: Make the opening more engaging. "
                                "Shorten the second paragraph.",
                    height=80,
                    key="cl_feedback"
                )

                if st.button("Revise Cover Letter"):
                    if not cl_feedback.strip():
                        st.warning("Please enter feedback before revising.")
                    else:
                        with st.spinner("Revising your cover letter..."):
                            try:
                                revised = revise_document(
                                    st.session_state["cover_letter_content"],
                                    cl_feedback,
                                    st.session_state["job_analysis"]
                                )
                                st.session_state["cover_letter_content"] = \
                                    revised
                                st.session_state["step"] = "revision"
                                st.success("Cover letter revised!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            st.divider()
            st.markdown("## Download Your Documents")
            st.caption(
                "When you are happy with your documents, download them below."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.session_state.get("generate_resume") and \
                        "resume_content" in st.session_state:
                    if st.button("Build Resume for Download", type="primary"):
                        with st.spinner("Building Word document..."):
                            try:
                                output_path = os.path.join(
                                    "outputs", "resumes", "tailored_resume.docx"
                                )
                                os.makedirs(
                                    os.path.dirname(output_path), exist_ok=True
                                )
                                build_resume_document(
                                    st.session_state["resume_content"],
                                    output_path,
                                    style_name=st.session_state.get(
                                        "selected_style", "Modern"
                                    )
                                )
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        label="Download Resume (.docx)",
                                        data=f,
                                        file_name="tailored_resume.docx",
                                        mime="application/vnd.openxmlformats-"
                                             "officedocument.wordprocessingml"
                                             ".document",
                                        key="download_resume"
                                    )
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            with col2:
                if st.session_state.get("generate_cover_letter") and \
                        "cover_letter_content" in st.session_state:
                    if st.button("Build Cover Letter for Download"):
                        with st.spinner("Building Word document..."):
                            try:
                                output_path = os.path.join(
                                    "outputs", "cover-letters",
                                    "tailored_cover_letter.docx"
                                )
                                os.makedirs(
                                    os.path.dirname(output_path), exist_ok=True
                                )
                                build_cover_letter_document(
                                    st.session_state["cover_letter_content"],
                                    output_path,
                                    style_name=st.session_state.get(
                                        "selected_style", "Modern"
                                    )
                                )
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        label="Download Cover Letter (.docx)",
                                        data=f,
                                        file_name="tailored_cover_letter.docx",
                                        mime="application/vnd.openxmlformats-"
                                             "officedocument.wordprocessingml"
                                             ".document",
                                        key="download_cover_letter"
                                    )
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            st.divider()
            if st.button("Start Over", key="start_over_p1"):
                count = st.session_state.get("session_count", 0) + 1
                st.session_state.clear()
                st.session_state["session_count"] = count
                st.rerun()

        with tab_eval:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem;
                        font-weight: 700;">Smart Evaluation Tool</span>
                    <span style="color: #888; font-size: 0.85rem;
                        font-weight: 400;"> (optional)</span>
                </div>
                <p style="color: #555; font-size: 0.9rem; margin-top: 0;">
                    Claude will analyze your documents and decide how to
                    evaluate them based on what you generated.
                </p>
            """, unsafe_allow_html=True)

            if st.button("Smart Evaluate My Documents", type="primary"):
                with st.spinner("Claude is analyzing your documents... "
                                "this may take 30-60 seconds."):
                    try:
                        resume_content = st.session_state.get(
                            "resume_content", ""
                        ) if st.session_state.get("generate_resume") else ""
                        cover_letter_content = st.session_state.get(
                            "cover_letter_content", ""
                        ) if st.session_state.get(
                            "generate_cover_letter") else ""

                        evaluation = smart_evaluate(
                            resume_content,
                            cover_letter_content,
                            st.session_state["job_analysis"]
                        )
                        st.session_state["smart_evaluation"] = evaluation
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

            if "smart_evaluation" in st.session_state:
                st.markdown("""
                    <div style="
                        border-left: 4px solid #0065A4;
                        border-radius: 6px;
                        padding: 2px 16px;
                        margin: 12px 0;
                        background-color: #f0f7ff;">
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state["smart_evaluation"])

# ─────────────────────────────────────────
# PATH 2 — EVALUATE EXISTING DOCUMENTS
# ─────────────────────────────────────────
elif st.session_state.get("path") == "evaluate":

    st.markdown("## Evaluating Your Documents")
    st.caption("Claude is analyzing your documents against the job posting...")

    cv_text = st.session_state.get("cv_text_for_eval", "")
    cl_text = st.session_state.get("cl_text_for_eval", "")

    if "path2_results" not in st.session_state:
        with st.spinner("Claude is deciding how to evaluate your documents... "
                        "this may take 30-60 seconds."):
            try:
                evaluation = smart_evaluate(
                    cv_text,
                    cl_text,
                    st.session_state["job_analysis"]
                )
                st.session_state["path2_results"] = evaluation
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                import traceback
                st.error(traceback.format_exc())

    if "path2_results" in st.session_state:
        st.markdown("""
            <div style="margin-bottom: 8px; margin-top: 12px;">
                <span style="color: #0065A4; font-size: 1.3rem;
                    font-weight: 700;">Smart Evaluation Report</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state["path2_results"])

        st.divider()
        if st.button("Switch to Generate New Documents", type="primary"):
            count = st.session_state.get("session_count", 0) + 1
            st.session_state.clear()
            st.session_state["session_count"] = count
            st.session_state["path"] = "generate"
            st.session_state["step"] = "style"
            st.rerun()

    st.divider()
    if st.button("Start Over", key="start_over_p2"):
        count = st.session_state.get("session_count", 0) + 1
        st.session_state.clear()
        st.session_state["session_count"] = count
        st.rerun()