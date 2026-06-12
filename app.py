import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Handle API key for both local and Streamlit Cloud
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

# Page configuration
st.set_page_config(
    page_title="Resume & Cover Letter Tailor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume & Cover Letter Tailor")
st.write("Upload your CV and a job posting to generate tailored, "
         "professional application documents.")

# ─────────────────────────────────────────
# STEP 1 — INPUTS
# ─────────────────────────────────────────
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

# Document selection checkboxes
st.subheader("What would you like to generate?")
generate_resume = st.checkbox("Resume", value=True)
generate_cover_letter = st.checkbox("Cover Letter", value=True)

# Analyze button
if st.button("🔍 Analyze", type="primary"):
    if not uploaded_cv:
        st.warning("Please upload your CV before continuing.")
    elif not job_posting.strip():
        st.warning("Please paste a job posting before continuing.")
    elif not generate_resume and not generate_cover_letter:
        st.warning("Please select at least one document to generate.")
    else:
        with st.spinner("Reading your CV and analyzing the job posting... "
                        "this may take 20-30 seconds."):
            try:
                # Extract and parse CV
                cv_raw_text = extract_cv_text(uploaded_cv)
                cv_content = parse_cv(cv_raw_text)
                st.session_state["cv_content"] = cv_content

                # Analyze job posting
                job_analysis = analyze_job_posting(job_posting)
                st.session_state["job_analysis"] = job_analysis
                st.session_state["job_posting"] = job_posting
                st.session_state["generate_resume"] = generate_resume
                st.session_state["generate_cover_letter"] = generate_cover_letter

                # Generate clarifying questions
                questions = generate_questions(cv_content, job_analysis)
                st.session_state["questions"] = questions
                st.session_state["step"] = "questions"
                st.success("Analysis complete! Please answer the questions below.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────
# STEP 2 — CLARIFYING QUESTIONS (one at a time)
# ─────────────────────────────────────────
if st.session_state.get("step") in ["questions", "generating",
                                     "review", "revision"]:
    st.header("Step 2 — Answer a Few Questions")
    st.write("These questions help tailor your documents more precisely.")

    # Parse questions into a list if not already done
    if "question_list" not in st.session_state:
        raw_questions = st.session_state.get("questions", "")
        lines = raw_questions.split("\n")
        question_list = []
        for line in lines:
            line = line.strip()
            if line.startswith("**Question"):
                # Extract just the question text
                question_text = line.replace("**", "").strip()
                question_list.append(question_text)
        st.session_state["question_list"] = question_list
        st.session_state["current_question_index"] = 0
        st.session_state["question_answers"] = []

    question_list = st.session_state.get("question_list", [])
    current_index = st.session_state.get("current_question_index", 0)
    answers = st.session_state.get("question_answers", [])

    # Show progress
    total_questions = len(question_list)
    if total_questions > 0:
        st.progress(current_index / total_questions)
        st.write(f"Question {min(current_index + 1, total_questions)} "
                 f"of {total_questions}")

    # Show previous answers
    if answers:
        with st.expander("Your answers so far"):
            for i, (q, a) in enumerate(
                zip(question_list[:len(answers)], answers)
            ):
                st.write(f"**{q}**")
                st.write(f"_{a}_")
                st.divider()

    # Show current question
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
                    st.session_state["current_question_index"] = current_index + 1
                    st.rerun()

    # All questions answered — show generate button
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

                    # Generate resume if selected
                    if st.session_state.get("generate_resume"):
                        resume_content = write_resume(
                            cv_content, job_analysis, user_answers
                        )
                        st.session_state["resume_content"] = resume_content

                    # Generate cover letter if selected
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

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────
# STEP 3 — REVIEW AND FEEDBACK
# ─────────────────────────────────────────
if st.session_state.get("step") in ["review", "revision"]:
    st.header("Step 3 — Review and Give Feedback")
    st.write("Review your documents below. Provide feedback to request changes "
             "before downloading.")

    # Display resume
    if st.session_state.get("generate_resume") and \
            "resume_content" in st.session_state:
        st.subheader("📋 Your Tailored Resume")
        st.markdown(st.session_state["resume_content"])

        resume_feedback = st.text_area(
            "Feedback for resume (optional):",
            placeholder="Example: Make the summary shorter. "
                        "Move education to the top. "
                        "Add more emphasis on leadership experience.",
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

    # Display cover letter
    if st.session_state.get("generate_cover_letter") and \
            "cover_letter_content" in st.session_state:
        st.subheader("✉️ Your Tailored Cover Letter")
        st.markdown(st.session_state["cover_letter_content"])

        cl_feedback = st.text_area(
            "Feedback for cover letter (optional):",
            placeholder="Example: Make the opening more engaging. "
                        "Add a specific mention of their research program. "
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

# ─────────────────────────────────────────
# STEP 4 — DOWNLOAD
# ─────────────────────────────────────────
if st.session_state.get("step") in ["review", "revision"]:
    st.header("Step 4 — Download Your Documents")
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
                            st.session_state["resume_content"], output_path
                        )
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Resume (.docx)",
                                data=f,
                                file_name="tailored_resume.docx",
                                mime="application/vnd.openxmlformats-"
                                     "officedocument.wordprocessingml.document",
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
                            "outputs", "cover-letters", "tailored_cover_letter.docx"
                        )
                        os.makedirs(
                            os.path.dirname(output_path), exist_ok=True
                        )
                        build_cover_letter_document(
                            st.session_state["cover_letter_content"], output_path
                        )
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Cover Letter (.docx)",
                                data=f,
                                file_name="tailored_cover_letter.docx",
                                mime="application/vnd.openxmlformats-"
                                     "officedocument.wordprocessingml.document",
                                key="download_cover_letter"
                            )
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    # Start over button
    st.divider()
    if st.button("🔁 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()