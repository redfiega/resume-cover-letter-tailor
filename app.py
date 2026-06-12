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

# Custom CSS
st.markdown("""
    <style>
    textarea {
        border: 2px solid #0065A4 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stTextArea"] textarea {
        border: 2px solid #0065A4 !important;
        border-radius: 6px !important;
        background-color: #f9f9f9 !important;
    }
    /* Path 1 button — solid blue */
    div[data-testid="stColumn"]:first-child button[kind="primary"] {
        background-color: #0065A4 !important;
        border-color: #0065A4 !important;
        color: white !important;
    }
    div[data-testid="stColumn"]:first-child button[kind="primary"]:hover {
        background-color: #004f82 !important;
    }
    /* Path 2 button — outlined blue */
    div[data-testid="stColumn"]:last-child button[kind="secondaryFormSubmit"],
    div[data-testid="stColumn"]:last-child button {
        background-color: #f0f7ff !important;
        border: 2px solid #0065A4 !important;
        color: #0065A4 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stColumn"]:last-child button:hover {
        background-color: #dceeff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Resume & Cover Letter Tailor")
st.write("Upload your CV and a job posting to get started.")

# ─────────────────────────────────────────
# HOMEPAGE — INPUTS
# ─────────────────────────────────────────
if st.session_state.get("path") is None:

    st.header("Step 1 — Upload Your CV and Job Posting")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_cv = st.file_uploader(
            "Upload your CV (PDF or Word)",
            type=["pdf", "docx"],
            help="Upload your full CV in PDF or Word format"
        )

    with col2:
        job_posting = st.text_area(
            "Paste the job posting here:",
            placeholder="Copy and paste the full job description here...",
            height=300
        )

    st.header("Step 2 — Choose Your Path")
    st.write("What would you like to do?")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(
            "✨ Build My Documents\n\nUpload your CV and a job posting. "
            "Answer a few questions. Get a tailored resume and cover letter "
            "ready to download.",
            type="primary",
            use_container_width=True,
            key="path1_button"
        ):
            if not uploaded_cv:
                st.warning("Please upload your CV before continuing.")
            elif not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            else:
                with st.spinner("Reading your CV and analyzing the job "
                                "posting... this may take 20-30 seconds."):
                    try:
                        cv_raw_text = extract_cv_text(uploaded_cv)
                        cv_content = parse_cv(cv_raw_text)
                        job_analysis = analyze_job_posting(job_posting)
                        questions = generate_questions(cv_content, job_analysis)
                        st.session_state["cv_content"] = cv_content
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
            "📊 Evaluate My Documents\n\nAlready have a resume or cover letter? "
            "Upload it and get scored feedback across five dimensions based "
            "on the job posting.",
            use_container_width=True,
            key="path2_button"
        ):
            if not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            else:
                with st.spinner("Analyzing the job posting..."):
                    try:
                        job_analysis = analyze_job_posting(job_posting)
                        st.session_state["job_analysis"] = job_analysis
                        st.session_state["job_posting"] = job_posting
                        st.session_state["path"] = "evaluate"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────
# PATH 1 — GENERATE NEW DOCUMENTS
# ─────────────────────────────────────────
elif st.session_state.get("path") == "generate":

    # ── Style selector ──
    if st.session_state.get("step") == "style":
        st.header("Step 3 — Choose a Document Style")

        selected_style = st.radio(
            "Select a style to see a preview:",
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
                padding: 20px; margin: 10px 0; background-color: #fafafa;">
                <p style="margin: 0 0 8px 0; color: #555;">
                    <strong>Style Preview: {selected_style}</strong></p>
                <div style="background-color: white; border: 1px solid #eee;
                    padding: 16px; font-family: {preview['font']}, serif;">
                    <p style="font-size: 18px; font-weight: bold;
                        color: {preview['name_color']};
                        background-color: {preview['background']};
                        padding: 4px 8px; margin: 0 0 8px 0;">Your Name</p>
                    <p style="font-size: 11px; color: #555; margin: 0 0 12px 0;">
                        your.email@example.com | (555) 123-4567 | City, State</p>
                    <p style="font-size: 11px; font-weight: bold;
                        color: {preview['header_color']};
                        background-color: {preview['background']};
                        padding: 2px 4px; margin: 0 0 6px 0;
                        border-bottom: 1px solid #ccc;">
                        PROFESSIONAL EXPERIENCE</p>
                    <p style="font-size: 10px; color: #333; margin: 0;">
                        • Led curriculum redesign increasing pass rates by 14%<br>
                        • Managed cross-functional team of 6 designers</p>
                </div>
                <p style="margin: 10px 0 0 0; color: #555; font-size: 13px;">
                    {preview['description']}</p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("What would you like to generate?")
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

    # ── Questions ──
    elif st.session_state.get("step") in ["questions", "generating",
                                           "review", "revision"]:
        st.header("Step 4 — Answer a Few Questions")
        st.write("These questions help tailor your documents more precisely.")

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
            st.write(f"Question {min(current_index + 1, total_questions)} "
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
            st.subheader(current_question)

            current_answer = st.text_area(
                "Your answer:",
                placeholder="Type your answer here...",
                height=150,
                key=f"answer_{current_index}"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Next ➡️", type="primary"):
                    if not current_answer.strip():
                        st.warning("Please answer the question before continuing.")
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

            if st.button("✨ Generate Documents", type="primary"):
                st.session_state["user_answers"] = user_answers
                st.session_state["step"] = "generating"

                with st.spinner("Generating your tailored documents... "
                                "this may take 30-60 seconds."):
                    try:
                        cv_content = st.session_state["cv_content"]
                        job_analysis = st.session_state["job_analysis"]

                        if st.session_state.get("generate_resume"):
                            resume_content = write_resume(
                                cv_content, job_analysis, user_answers
                            )
                            st.session_state["resume_content"] = resume_content

                        if st.session_state.get("generate_cover_letter"):
                            resume_for_cl = st.session_state.get(
                                "resume_content", "No resume generated"
                            )
                            cover_letter_content = write_cover_letter(
                                cv_content, job_analysis,
                                user_answers, resume_for_cl
                            )
                            st.session_state["cover_letter_content"] = \
                                cover_letter_content

                        st.session_state["step"] = "review"
                        st.success("Documents generated! Review them below.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    # ── Review and feedback ──
    if st.session_state.get("step") in ["review", "revision"]:
        st.header("Step 5 — Review and Give Feedback")
        st.write("Review your documents below. Provide feedback to request "
                 "changes before downloading.")

        # Resume
        if st.session_state.get("generate_resume") and \
                "resume_content" in st.session_state:
            st.subheader("📋 Your Tailored Resume")
            st.markdown(st.session_state["resume_content"])

            st.markdown("""
                <div style="border: 2px solid #0065A4; border-radius: 8px;
                    padding: 12px; margin: 10px 0;
                    background-color: #f0f7ff;">
                    <strong>💬 Provide Feedback on Your Resume</strong><br>
                    <em>Use the box below to request changes to content
                    or formatting.</em>
                </div>
            """, unsafe_allow_html=True)

            resume_feedback = st.text_area(
                "What would you like to change?",
                placeholder="Example: Make the summary shorter. "
                            "Move education to the top.",
                height=100,
                key="resume_feedback"
            )

            if st.button("🔄 Revise Resume"):
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

        # Cover letter
        if st.session_state.get("generate_cover_letter") and \
                "cover_letter_content" in st.session_state:
            st.subheader("✉️ Your Tailored Cover Letter")
            st.markdown(st.session_state["cover_letter_content"])

            st.markdown("""
                <div style="border: 2px solid #0065A4; border-radius: 8px;
                    padding: 12px; margin: 10px 0;
                    background-color: #f0f7ff;">
                    <strong>💬 Provide Feedback on Your Cover Letter</strong><br>
                    <em>Use the box below to request changes to content
                    or formatting.</em>
                </div>
            """, unsafe_allow_html=True)

            cl_feedback = st.text_area(
                "What would you like to change?",
                placeholder="Example: Make the opening more engaging. "
                            "Shorten the second paragraph.",
                height=100,
                key="cl_feedback"
            )

            if st.button("🔄 Revise Cover Letter"):
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
                            st.session_state["cover_letter_content"] = revised
                            st.session_state["step"] = "revision"
                            st.success("Cover letter revised!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Something went wrong: {e}")

        # Evaluate button
        st.divider()
        st.subheader("📊 Optional — Evaluate Your Documents")
        st.write("Get a scored evaluation report across five dimensions.")

        if st.button("📊 Evaluate My Documents"):
            with st.spinner("Running evaluation... this may take 30-60 seconds."):
                try:
                    results = {}
                    if st.session_state.get("generate_resume") and \
                            "resume_content" in st.session_state:
                        results["Resume"] = review_document(
                            st.session_state["resume_content"],
                            st.session_state["job_analysis"],
                            "Resume"
                        )
                    if st.session_state.get("generate_cover_letter") and \
                            "cover_letter_content" in st.session_state:
                        results["Cover Letter"] = review_document(
                            st.session_state["cover_letter_content"],
                            st.session_state["job_analysis"],
                            "Cover Letter"
                        )
                    st.session_state["evaluation_results"] = results
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if "evaluation_results" in st.session_state:
            for doc_type, report in st.session_state["evaluation_results"].items():
                st.subheader(f"Evaluation Report — {doc_type}")
                st.markdown(report)

        # Download
        st.divider()
        st.header("Step 6 — Download Your Documents")
        st.write("When you are happy with your documents, download them below.")

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.get("generate_resume") and \
                    "resume_content" in st.session_state:
                if st.button("📥 Build Resume for Download"):
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
                                    label="⬇️ Download Resume (.docx)",
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
                if st.button("📥 Build Cover Letter for Download"):
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
                                    label="⬇️ Download Cover Letter (.docx)",
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
        if st.button("🔁 Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ─────────────────────────────────────────
# PATH 2 — EVALUATE EXISTING DOCUMENTS
# ─────────────────────────────────────────
elif st.session_state.get("path") == "evaluate":

    st.header("Evaluate Your Existing Documents")
    st.write("Upload or paste your resume and/or cover letter to get scored "
             "feedback based on the job posting.")

    doc_type = st.selectbox(
        "What are you evaluating?",
        ["Resume", "Cover Letter"]
    )

    input_method = st.radio(
        "How would you like to provide your document?",
        ["Upload a file (PDF or Word)", "Paste as text"],
        horizontal=True
    )

    document_text = ""

    if input_method == "Upload a file (PDF or Word)":
        uploaded_doc = st.file_uploader(
            f"Upload your {doc_type} (PDF or Word)",
            type=["pdf", "docx"]
        )
        if uploaded_doc:
            with st.spinner("Reading your document..."):
                try:
                    document_text = extract_cv_text(uploaded_doc)
                    st.success("Document uploaded successfully!")
                except Exception as e:
                    st.error(f"Could not read the file: {e}")

    else:
        st.warning(
            "⚠️ Note: Visual Structure cannot be evaluated from pasted text. "
            "Upload a Word or PDF file for a complete evaluation including "
            "visual structure scoring."
        )
        document_text = st.text_area(
            f"Paste your {doc_type} here:",
            placeholder=f"Paste the full text of your {doc_type} here...",
            height=400
        )

    if st.button("📊 Evaluate", type="primary"):
        if not document_text.strip():
            st.warning("Please provide your document before evaluating.")
        else:
            with st.spinner("Evaluating your document... "
                            "this may take 30-60 seconds."):
                try:
                    report = review_document(
                        document_text,
                        st.session_state["job_analysis"],
                        doc_type
                    )
                    st.session_state["path2_report"] = report
                    st.session_state["path2_input_method"] = input_method
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if "path2_report" in st.session_state:
        st.subheader(f"📊 Evaluation Report — {doc_type}")

        if st.session_state.get("path2_input_method") == "Paste as text":
            st.info("ℹ️ Visual Structure was not evaluated because text was "
                    "pasted instead of a file being uploaded.")

        st.markdown(st.session_state["path2_report"])

        st.divider()
        st.write("Would you like to generate new tailored documents instead?")
        if st.button("✨ Switch to Generate New Documents"):
            for key in ["path", "path2_report", "path2_input_method"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.divider()
    if st.button("🔁 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()