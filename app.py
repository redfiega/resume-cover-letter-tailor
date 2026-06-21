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
    revise_document,
    generate_interview_prep
)
from document_builder import (
    build_resume_document,
    build_cover_letter_document
)

st.set_page_config(
    page_title="Resume & Cover Letter Tailor",
    page_icon="📄",
    layout="wide"
)

if "session_count" not in st.session_state:
    st.session_state["session_count"] = 0

if "session_history" not in st.session_state:
    st.session_state["session_history"] = []

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    .block-container {
        padding-top: 0rem !important;
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    textarea { border: 2px solid #0065A4 !important; border-radius: 6px !important; }
    div[data-testid="stTextArea"] textarea {
        border: 2px solid #0065A4 !important;
        border-radius: 6px !important;
        background-color: #f9f9f9 !important;
    }
    div[data-testid="stVerticalBlock"] button[kind="primary"] {
        background-color: #0065A4 !important;
        border-color: #0065A4 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stVerticalBlock"] button[kind="primary"]:hover { background-color: #004f82 !important; }
    div[data-testid="stVerticalBlock"] button[kind="secondary"] {
        background-color: #f0f7ff !important;
        border: 2px solid #0065A4 !important;
        color: #0065A4 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stVerticalBlock"] button[kind="secondary"]:hover { background-color: #dceeff !important; }
    h2 { color: #0065A4 !important; font-size: 1.3rem !important; margin-top: 1.5rem !important; margin-bottom: 0.5rem !important; }
    h3 { font-size: 1.05rem !important; margin-top: 1rem !important; margin-bottom: 0.3rem !important; }
    div[data-testid="stVerticalBlock"] > div { padding-top: 0.2rem !important; padding-bottom: 0.2rem !important; }
    [data-testid="stTabs"] [role="tab"] {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #222 !important;
        padding: 10px 24px !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #0065A4 !important;
    }
    [data-testid="stTabs"] [role="tab"]:hover {
        color: #0065A4 !important;
    }
    .section-header {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #0065A4 !important;
        padding: 10px 16px 6px 16px !important;
        margin: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background: linear-gradient(135deg, #0065A4 0%, #003f6b 100%);
        padding: 32px 40px 28px 40px; border-radius: 0 0 12px 12px; margin-bottom: 24px;">
        <h1 style="color: white; font-size: 2rem; font-weight: 800; margin: 0 0 6px 0;">
            Resume &amp; Cover Letter Tailor</h1>
        <p style="font-size: 1rem; color: #cce4f7; margin: 0;">
            Upload your CV and a job posting — get a tailored,
            job-ready resume and cover letter in minutes.</p>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────
if st.session_state.get("path") is None:

    sc = st.session_state.get("session_count", 0)

    st.markdown("""
        <div style="display: flex; gap: 8px; margin-bottom: 16px; align-items: center; flex-wrap: wrap;">
            <span style="background: #0065A4; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">1 · Your Documents</span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">2 · Style</span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">3 · Questions</span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">4 · Review</span>
            <span style="color: #aaa;">→</span>
            <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">5 · Download</span>
        </div>
    """, unsafe_allow_html=True)

    # ── Collapsible Instructions ──
    st.markdown("""
        <p style="font-size: 1.15rem; font-weight: 700; color: #0065A4;
            margin-bottom: 4px;">Getting Started</p>
    """, unsafe_allow_html=True)
    with st.expander("How to Use This Tool — click to expand", expanded=False):
        st.markdown("""
        ### Welcome to Resume & Cover Letter Tailor

        This tool helps you create tailored, professional application documents
        in minutes. Here's how it works:

        ---

        **Path 1 — Build My Documents**
        Use this when you want to generate a new resume and/or cover letter
        tailored to a specific job posting.

        1. **Upload your CV or Resume** — PDF or Word format, or paste as text
        2. **Upload an existing cover letter** (optional) — used as tone/style reference
        3. **Paste the job posting** — copy the full job description
        4. Click **Build My Documents**
        5. **Choose a style** for your resume (Classic, Modern, Bold, or Academic)
        6. **Choose a tone** for your cover letter (Professional, Conversational,
           Confident, or Mission-Driven)
        7. **Answer a few questions** to help tailor your documents
        8. **Review your documents** — request revisions using the feedback boxes
        9. **Download** your polished Word documents

        ---

        **Path 2 — Evaluate My Documents**
        Use this when you already have a resume and/or cover letter and want
        scored feedback on how well they match a job posting.

        1. **Upload your CV or Resume** and/or **cover letter**
        2. **Paste the job posting**
        3. Click **Evaluate My Documents**
        4. Review your **Smart Evaluation Report** with scores across five dimensions

        ---

        **Tips for Best Results**
        - Paste the complete job description, not just the title
        - Answer the clarifying questions thoughtfully — they significantly
          improve the quality of your documents
        - Use the feedback boxes to request specific changes before downloading
        - Try the **Smart Evaluation Tool** after generating to get scored feedback
        - Use the **Interview Prep** tab to prepare for your interview

        ---

        **Note:** The app may take 20-60 seconds to process requests.
        Documents generated in this session are available in the
        **This Session** tab on the Review page.
        """)

    # ── CV Section Card ──
    st.markdown("""
        <div style="border: 1.5px solid #c8dff5; border-radius: 10px;
            padding: 20px 24px 12px 24px; margin-bottom: 16px;
            background-color: #fafcff;">
            <p style="font-size: 1.05rem; font-weight: 700; color: #0065A4;
                margin: 0 0 12px 0;">Your CV or Resume</p>
        </div>
    """, unsafe_allow_html=True)

    cv_input_method = st.radio(
        "How would you like to provide your CV or Resume?",
        ["Upload a file (PDF or Word)", "Paste as text", "Skip"],
        horizontal=True, key=f"cv_input_method_{sc}"
    )
    cv_text = ""
    if cv_input_method == "Upload a file (PDF or Word)":
        uploaded_cv = st.file_uploader("Upload your CV or Resume (PDF or Word)",
            type=["pdf", "docx"], key=f"cv_upload_{sc}")
        if uploaded_cv:
            with st.spinner("Reading your document..."):
                try:
                    cv_text = extract_cv_text(uploaded_cv)
                    st.success(f"Uploaded: {uploaded_cv.name}")
                except Exception as e:
                    st.error(f"Could not read the file: {e}")
    elif cv_input_method == "Paste as text":
        cv_text = st.text_area("Paste your CV or Resume here:",
            placeholder="Paste the full text of your CV or Resume here...",
            height=200, key=f"cv_paste_{sc}")

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    # ── Cover Letter Section Card ──
    st.markdown("""
        <div style="border: 1.5px solid #c8dff5; border-radius: 10px;
            padding: 20px 24px 12px 24px; margin-bottom: 16px;
            background-color: #fafcff;">
            <p style="font-size: 1.05rem; font-weight: 700; color: #0065A4;
                margin: 0 0 12px 0;">Existing Cover Letter <span style="font-weight: 400; font-size: 0.9rem; color: #888;">(optional)</span></p>
        </div>
    """, unsafe_allow_html=True)

    cl_input_method = st.radio(
        "How would you like to provide your cover letter?",
        ["Upload a file (PDF or Word)", "Paste as text", "Skip"],
        horizontal=True, key=f"cl_input_method_home_{sc}"
    )
    cl_text = ""
    if cl_input_method == "Upload a file (PDF or Word)":
        uploaded_cl = st.file_uploader("Upload your cover letter (PDF or Word)",
            type=["pdf", "docx"], key=f"cl_upload_home_{sc}")
        if uploaded_cl:
            with st.spinner("Reading your cover letter..."):
                try:
                    cl_text = extract_cv_text(uploaded_cl)
                    st.success(f"Uploaded: {uploaded_cl.name}")
                except Exception as e:
                    st.error(f"Could not read the file: {e}")
    elif cl_input_method == "Paste as text":
        cl_text = st.text_area("Paste your cover letter here:",
            placeholder="Paste the full text of your cover letter here...",
            height=150, key=f"cl_paste_home_{sc}")

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    # ── Job Posting Section Card ──
    st.markdown("""
        <div style="border: 1.5px solid #c8dff5; border-radius: 10px;
            padding: 20px 24px 12px 24px; margin-bottom: 16px;
            background-color: #fafcff;">
            <p style="font-size: 1.05rem; font-weight: 700; color: #0065A4;
                margin: 0 0 12px 0;">Job Posting</p>
        </div>
    """, unsafe_allow_html=True)

    job_posting = st.text_area("Paste the job posting here:",
        placeholder="Copy and paste the full job description here...",
        height=200, key=f"job_posting_input_{sc}")

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    # ── Path Selection ──
    st.markdown("### Choose Your Path")
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(
            "Build My Documents\n\nGenerate a new tailored resume and/or "
            "cover letter based on your CV and the job posting.",
            type="primary", use_container_width=True, key=f"path1_button_{sc}"
        ):
            if not cv_text.strip():
                st.warning("Please provide your CV or Resume before generating.")
            elif not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            else:
                with st.spinner("Analyzing... this may take 20-30 seconds."):
                    try:
                        cv_content = parse_cv(cv_text)
                        job_analysis = analyze_job_posting(job_posting)
                        questions = generate_questions(cv_content, job_analysis)
                        st.session_state["cv_content"] = cv_content
                        st.session_state["cl_content"] = cl_text
                        st.session_state["job_analysis"] = job_analysis
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
            use_container_width=True, key=f"path2_button_{sc}"
        ):
            if not job_posting.strip():
                st.warning("Please paste a job posting before continuing.")
            elif not cv_text.strip() and not cl_text.strip():
                st.warning("Please provide at least one document — your CV, "
                           "resume, or cover letter — before evaluating.")
            else:
                with st.spinner("Analyzing the job posting..."):
                    try:
                        job_analysis = analyze_job_posting(job_posting)
                        st.session_state["job_analysis"] = job_analysis
                        st.session_state["cv_text_for_eval"] = cv_text
                        st.session_state["cl_text_for_eval"] = cl_text
                        st.session_state["cv_input_method"] = cv_input_method
                        st.session_state["cl_input_method"] = cl_input_method
                        st.session_state["path"] = "evaluate"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

# ─────────────────────────────────────────
# PATH 1 — GENERATE
# ─────────────────────────────────────────
elif st.session_state.get("path") == "generate":

    if st.session_state.get("step") == "style":
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px; align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">1 · Documents</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">2 · Style</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">3 · Questions</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">4 · Review</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">5 · Download</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## Choose Your Style and Tone")

        st.markdown("### What would you like to generate?")
        generate_resume = st.checkbox("Resume", value=True)
        generate_cover_letter = st.checkbox("Cover Letter", value=True)

        style_previews = {
            "Classic": {"description": "Clean black and white formatting with Times New Roman font. Traditional and widely accepted.", "name_color": "#000000", "header_color": "#000000", "background": "#ffffff", "font": "Times New Roman"},
            "Modern": {"description": "Blue accents with Calibri font. Clean and contemporary, works well for most professional roles.", "name_color": "#0065A4", "header_color": "#0065A4", "background": "#ffffff", "font": "Calibri"},
            "Bold": {"description": "Dark navy header backgrounds with white text. High contrast and visually striking.", "name_color": "#ffffff", "header_color": "#ffffff", "background": "#1F497D", "font": "Calibri"},
            "Academic": {"description": "Formal black text with underlined section headers and Georgia font. Best for academic roles.", "name_color": "#000000", "header_color": "#000000", "background": "#ffffff", "font": "Georgia"}
        }

        selected_style = "Modern"
        if generate_resume:
            st.markdown("### Resume Style")
            selected_style = st.radio("Select a style:",
                ["Classic", "Modern", "Bold", "Academic"], horizontal=True, index=1,
                key="style_radio")
            preview = style_previews[selected_style]
            st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background-color: #fafafa;">
                    <p style="margin: 0 0 8px 0; color: #555; font-size: 0.85rem;"><strong>Resume Preview — {selected_style}</strong></p>
                    <div style="background-color: white; border: 1px solid #eee; padding: 16px; font-family: {preview['font']}, serif;">
                        <p style="font-size: 16px; font-weight: bold; color: {preview['name_color']}; background-color: {preview['background']}; padding: 4px 8px; margin: 0 0 6px 0;">Your Name</p>
                        <p style="font-size: 10px; color: #555; margin: 0 0 10px 0;">your.email@example.com | (555) 123-4567 | City, State</p>
                        <p style="font-size: 10px; font-weight: bold; color: {preview['header_color']}; background-color: {preview['background']}; padding: 2px 4px; margin: 0 0 4px 0; border-bottom: 1px solid #ccc;">PROFESSIONAL EXPERIENCE</p>
                        <p style="font-size: 9px; color: #333; margin: 0;">• Led curriculum redesign increasing pass rates by 14%<br>• Managed cross-functional team of 6 designers</p>
                    </div>
                    <p style="margin: 8px 0 0 0; color: #444; font-size: 0.9rem;">{preview['description']}</p>
                </div>
            """, unsafe_allow_html=True)

        tone_descriptions = {
            "Professional": "Formal, polished, and traditional. Works for most corporate and academic roles.",
            "Conversational": "Warm and approachable. Reads like a confident person speaking directly.",
            "Confident": "Bold and assertive. Emphasizes accomplishments and leadership.",
            "Mission-Driven": "Passionate and values-focused. Ideal for nonprofit, education, and purpose-led organizations."
        }

        selected_tone = "Professional"
        if generate_cover_letter:
            st.markdown("### Cover Letter Tone")
            selected_tone = st.radio("Select a tone:",
                ["Professional", "Conversational", "Confident", "Mission-Driven"],
                horizontal=True, index=0, key="tone_radio")
            st.markdown(
                f'<p style="color: #444; font-size: 0.9rem; margin-top: 4px;">' +
                tone_descriptions[selected_tone] + '</p>',
                unsafe_allow_html=True
            )

        if st.button("Next Step →", type="primary"):
            if not generate_resume and not generate_cover_letter:
                st.warning("Please select at least one document to generate.")
            else:
                st.session_state["selected_style"] = selected_style
                st.session_state["selected_tone"] = selected_tone
                st.session_state["generate_resume"] = generate_resume
                st.session_state["generate_cover_letter"] = generate_cover_letter
                st.session_state["step"] = "questions"
                st.rerun()

        st.divider()
        if st.button("Start Over", key="start_over_style"):
            count = st.session_state.get("session_count", 0) + 1
            history = st.session_state.get("session_history", [])
            st.session_state.clear()
            st.session_state["session_count"] = count
            st.session_state["session_history"] = history
            st.rerun()

    elif st.session_state.get("step") in ["questions", "generating"]:
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px; align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">1 · Documents</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">2 · Style</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">3 · Questions</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">4 · Review</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">5 · Download</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## A Few Quick Questions")
        st.caption("These help tailor your documents more precisely.")

        if "question_list" not in st.session_state:
            raw_questions = st.session_state.get("questions", "")
            question_list = []
            for line in raw_questions.split("\n"):
                line = line.strip()
                if line.startswith("**Question"):
                    question_list.append(line.replace("**", "").strip())
            st.session_state["question_list"] = question_list
            st.session_state["current_question_index"] = 0
            st.session_state["question_answers"] = []

        question_list = st.session_state.get("question_list", [])
        current_index = st.session_state.get("current_question_index", 0)
        answers = list(st.session_state.get("question_answers", []))
        total_questions = len(question_list)

        if total_questions > 0:
            st.progress(current_index / total_questions)
            st.caption(f"Question {min(current_index + 1, total_questions)} of {total_questions}")

        if answers:
            with st.expander("Your answers so far — click Edit to revise"):
                for i, (q, a) in enumerate(zip(question_list[:len(answers)], answers)):
                    col_q, col_btn = st.columns([5, 1])
                    with col_q:
                        st.write(f"**{q}**")
                        st.write(f"_{a}_")
                    with col_btn:
                        if st.button("Edit", key=f"edit_btn_{i}"):
                            ta_key_to_clear = f"ta_q{i}"
                            if ta_key_to_clear in st.session_state:
                                del st.session_state[ta_key_to_clear]
                            st.session_state["current_question_index"] = i
                            st.session_state["editing_answer"] = a
                            st.rerun()
                    st.divider()

        if current_index < total_questions:
            current_question = question_list[current_index]
            st.markdown(f"### {current_question}")

            editing_value = st.session_state.pop("editing_answer", "")
            ta_key = f"ta_q{current_index}"
            if editing_value and ta_key not in st.session_state:
                st.session_state[ta_key] = editing_value

            current_answer = st.text_area(
                "Your answer:",
                placeholder="Type your answer here...",
                height=120,
                key=ta_key
            )

            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if current_index > 0:
                    if st.button("← Back", key=f"back_{current_index}"):
                        prev_index = current_index - 1
                        current_answers = list(st.session_state.get("question_answers", []))
                        prev_answer = current_answers[prev_index] if prev_index < len(current_answers) else ""
                        prev_ta_key = f"ta_q{prev_index}"
                        if prev_ta_key in st.session_state:
                            del st.session_state[prev_ta_key]
                        st.session_state["current_question_index"] = prev_index
                        st.session_state["editing_answer"] = prev_answer
                        st.rerun()

            with col2:
                if st.button("Next →", type="primary", key=f"next_{current_index}"):
                    answer_value = st.session_state.get(ta_key, "").strip()
                    if not answer_value:
                        st.warning("Please answer the question before continuing.")
                    else:
                        new_answers = list(st.session_state.get("question_answers", []))
                        if current_index < len(new_answers):
                            new_answers[current_index] = answer_value
                        else:
                            new_answers.append(answer_value)
                        st.session_state["question_answers"] = new_answers
                        next_index = current_index + 1
                        st.session_state["current_question_index"] = next_index
                        next_ta_key = f"ta_q{next_index}"
                        if next_index < len(new_answers) and next_ta_key not in st.session_state:
                            st.session_state["editing_answer"] = new_answers[next_index]
                        st.rerun()

        if current_index >= total_questions and total_questions > 0:
            final_answers = list(st.session_state.get("question_answers", []))
            st.success("All questions answered!")
            user_answers = "\n\n".join([
                f"Q: {q}\nA: {a}" for q, a in zip(question_list, final_answers)
            ])

            if st.button("Generate Documents", type="primary"):
                st.session_state["user_answers"] = user_answers
                st.session_state["step"] = "generating"

                with st.spinner("Generating your tailored documents... this may take 30-60 seconds."):
                    try:
                        cv_content = st.session_state["cv_content"]
                        job_analysis = st.session_state["job_analysis"]
                        cl_context = st.session_state.get("cl_content", "")
                        selected_tone = st.session_state.get("selected_tone", "Professional")

                        user_answers_with_context = (
                            user_answers + f"\n\nExisting cover letter for style/tone reference:\n{cl_context}"
                            if cl_context.strip() else user_answers
                        )

                        if st.session_state.get("generate_resume"):
                            st.session_state["resume_content"] = write_resume(
                                cv_content, job_analysis, user_answers_with_context)

                        if st.session_state.get("generate_cover_letter"):
                            resume_for_cl = st.session_state.get("resume_content", "No resume generated")
                            st.session_state["cover_letter_content"] = write_cover_letter(
                                cv_content, job_analysis, user_answers_with_context,
                                resume_for_cl, tone=selected_tone)

                        history_entry = {
                            "job_title": job_analysis[:80] + "..." if len(job_analysis) > 80 else job_analysis,
                            "resume": st.session_state.get("resume_content", ""),
                            "cover_letter": st.session_state.get("cover_letter_content", ""),
                            "style": st.session_state.get("selected_style", "Modern"),
                            "tone": selected_tone
                        }
                        st.session_state["session_history"].append(history_entry)

                        st.session_state["step"] = "review"
                        st.rerun()

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

        st.divider()
        if st.button("Start Over", key="start_over_questions"):
            count = st.session_state.get("session_count", 0) + 1
            history = st.session_state.get("session_history", [])
            st.session_state.clear()
            st.session_state["session_count"] = count
            st.session_state["session_history"] = history
            st.rerun()

    if st.session_state.get("step") in ["review", "revision"]:
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 20px; align-items: center; flex-wrap: wrap;">
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">1 · Documents</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">2 · Style</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">3 · Questions</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #0065A4; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">4 · Review</span>
                <span style="color: #aaa;">→</span>
                <span style="background: #e8f0fe; color: #555; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem;">5 · Download</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="background-color: #f0f7ff; border-left: 4px solid #0065A4;
                border-radius: 6px; padding: 10px 16px; margin-bottom: 12px;
                font-size: 0.9rem; color: #333;">
                Use the tabs below to review your documents, run a Smart Evaluation,
                prepare for your interview, or access documents from this session.
            </div>
        """, unsafe_allow_html=True)

        tab_docs, tab_eval, tab_interview, tab_history = st.tabs([
            "Your Documents & Download",
            "Smart Evaluation Tool",
            "Interview Prep",
            "This Session"
        ])

        with tab_docs:
            st.markdown("## Review Your Documents")
            st.caption("Review and request changes before downloading.")

            if st.session_state.get("generate_resume") and "resume_content" in st.session_state:
                with st.expander("Change Resume Style"):
                    new_style = st.radio("Select a new style:",
                        ["Classic", "Modern", "Bold", "Academic"],
                        horizontal=True,
                        index=["Classic", "Modern", "Bold", "Academic"].index(
                            st.session_state.get("selected_style", "Modern")),
                        key="style_change_radio")
                    if st.button("Apply New Style", key="apply_style"):
                        st.session_state["selected_style"] = new_style
                        # Save updated version to session history
                        history = st.session_state.get("session_history", [])
                        history_entry = {
                            "job_title": st.session_state.get("job_analysis", "")[:80],
                            "resume": st.session_state.get("resume_content", ""),
                            "cover_letter": st.session_state.get("cover_letter_content", ""),
                            "style": new_style,
                            "tone": st.session_state.get("selected_tone", "Professional")
                        }
                        history.append(history_entry)
                        st.session_state["session_history"] = history
                        st.success(f"Style updated to {new_style}! Download your resume to see the change.")

            if st.session_state.get("generate_cover_letter") and "cover_letter_content" in st.session_state:
                with st.expander("Change Cover Letter Tone and Regenerate"):
                    new_tone = st.radio("Select a new tone:",
                        ["Professional", "Conversational", "Confident", "Mission-Driven"],
                        horizontal=True,
                        index=["Professional", "Conversational", "Confident", "Mission-Driven"].index(
                            st.session_state.get("selected_tone", "Professional")),
                        key="tone_change_radio")
                    if st.button("Regenerate with New Tone", key="apply_tone"):
                        with st.spinner("Regenerating cover letter with new tone..."):
                            try:
                                new_cl = write_cover_letter(
                                    st.session_state["cv_content"],
                                    st.session_state["job_analysis"],
                                    st.session_state.get("user_answers", ""),
                                    st.session_state.get("resume_content", ""),
                                    tone=new_tone)
                                st.session_state["cover_letter_content"] = new_cl
                                st.session_state["selected_tone"] = new_tone
                                # Save updated version to session history
                                history = st.session_state.get("session_history", [])
                                history_entry = {
                                    "job_title": st.session_state.get("job_analysis", "")[:80],
                                    "resume": st.session_state.get("resume_content", ""),
                                    "cover_letter": new_cl,
                                    "style": st.session_state.get("selected_style", "Modern"),
                                    "tone": new_tone
                                }
                                history.append(history_entry)
                                st.session_state["session_history"] = history
                                st.success(f"Cover letter regenerated with {new_tone} tone!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            if st.session_state.get("generate_resume") and "resume_content" in st.session_state:
                st.markdown("### Your Tailored Resume")
                st.markdown(st.session_state["resume_content"])
                st.markdown("""
                    <div style="border: 2px solid #0065A4; border-radius: 8px;
                        padding: 12px; margin: 10px 0; background-color: #f0f7ff;">
                        <strong>Provide Feedback on Your Resume</strong><br>
                        <span style="font-size: 0.9rem; color: #555;">Request changes to content or formatting below.</span>
                    </div>
                """, unsafe_allow_html=True)
                resume_feedback = st.text_area("What would you like to change?",
                    placeholder="Example: Make the summary shorter. Move education to the top.",
                    height=80, key="resume_feedback")
                if st.button("Revise Resume"):
                    if not resume_feedback.strip():
                        st.warning("Please enter feedback before revising.")
                    else:
                        with st.spinner("Revising your resume..."):
                            try:
                                revised = revise_document(
                                    st.session_state["resume_content"],
                                    resume_feedback,
                                    st.session_state["job_analysis"])
                                st.session_state["resume_content"] = revised
                                st.session_state["step"] = "revision"
                                st.success("Resume revised!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            if st.session_state.get("generate_cover_letter") and "cover_letter_content" in st.session_state:
                st.markdown("### Your Tailored Cover Letter")
                st.markdown(st.session_state["cover_letter_content"])
                st.markdown("""
                    <div style="border: 2px solid #0065A4; border-radius: 8px;
                        padding: 12px; margin: 10px 0; background-color: #f0f7ff;">
                        <strong>Provide Feedback on Your Cover Letter</strong><br>
                        <span style="font-size: 0.9rem; color: #555;">Request changes to content or formatting below.</span>
                    </div>
                """, unsafe_allow_html=True)
                cl_feedback = st.text_area("What would you like to change?",
                    placeholder="Example: Make the opening more engaging. Shorten the second paragraph.",
                    height=80, key="cl_feedback")
                if st.button("Revise Cover Letter"):
                    if not cl_feedback.strip():
                        st.warning("Please enter feedback before revising.")
                    else:
                        with st.spinner("Revising your cover letter..."):
                            try:
                                revised = revise_document(
                                    st.session_state["cover_letter_content"],
                                    cl_feedback,
                                    st.session_state["job_analysis"])
                                st.session_state["cover_letter_content"] = revised
                                st.session_state["step"] = "revision"
                                st.success("Cover letter revised!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            st.divider()
            st.markdown("## Download Your Documents")
            st.caption("When you are happy with your documents, download them below.")
            col1, col2 = st.columns(2)

            with col1:
                if st.session_state.get("generate_resume") and "resume_content" in st.session_state:
                    if st.button("Build Resume for Download", type="primary"):
                        with st.spinner("Building Word document..."):
                            try:
                                output_path = os.path.join("outputs", "resumes", "tailored_resume.docx")
                                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                                build_resume_document(
                                    st.session_state["resume_content"], output_path,
                                    style_name=st.session_state.get("selected_style", "Modern"))
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        label="Download Resume (.docx)", data=f,
                                        file_name="tailored_resume.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="download_resume")
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            with col2:
                if st.session_state.get("generate_cover_letter") and "cover_letter_content" in st.session_state:
                    if st.button("Build Cover Letter for Download"):
                        with st.spinner("Building Word document..."):
                            try:
                                output_path = os.path.join("outputs", "cover-letters", "tailored_cover_letter.docx")
                                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                                build_cover_letter_document(
                                    st.session_state["cover_letter_content"], output_path,
                                    style_name=st.session_state.get("selected_style", "Modern"))
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        label="Download Cover Letter (.docx)", data=f,
                                        file_name="tailored_cover_letter.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="download_cover_letter")
                            except Exception as e:
                                st.error(f"Something went wrong: {e}")

            st.divider()
            if st.button("Start Over", key="start_over_p1"):
                count = st.session_state.get("session_count", 0) + 1
                history = st.session_state.get("session_history", [])
                st.session_state.clear()
                st.session_state["session_count"] = count
                st.session_state["session_history"] = history
                st.rerun()

        with tab_eval:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem; font-weight: 700;">Smart Evaluation Tool</span>
                    <span style="color: #888; font-size: 0.85rem; font-weight: 400;"> (optional)</span>
                </div>
                <p style="color: #555; font-size: 0.9rem; margin-top: 0;">
                    Claude will analyze your documents and decide how to evaluate them,
                    including an ATS compatibility score for your resume.
                </p>
            """, unsafe_allow_html=True)

            if st.button("Smart Evaluate My Documents", type="primary"):
                with st.spinner("Claude is analyzing your documents... this may take 30-60 seconds."):
                    try:
                        resume_content = st.session_state.get("resume_content", "") \
                            if st.session_state.get("generate_resume") else ""
                        cover_letter_content = st.session_state.get("cover_letter_content", "") \
                            if st.session_state.get("generate_cover_letter") else ""
                        evaluation = smart_evaluate(
                            resume_content, cover_letter_content,
                            st.session_state["job_analysis"])
                        st.session_state["smart_evaluation"] = evaluation
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

            if "smart_evaluation" in st.session_state:
                st.markdown("""
                    <div style="border-left: 4px solid #0065A4; border-radius: 6px;
                        padding: 2px 16px; margin: 12px 0; background-color: #f0f7ff;">
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state["smart_evaluation"])

            st.divider()
            if st.button("Start Over", key="start_over_eval"):
                count = st.session_state.get("session_count", 0) + 1
                history = st.session_state.get("session_history", [])
                st.session_state.clear()
                st.session_state["session_count"] = count
                st.session_state["session_history"] = history
                st.rerun()

        with tab_interview:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem; font-weight: 700;">Interview Preparation</span>
                </div>
                <p style="color: #555; font-size: 0.9rem; margin-top: 0;">
                    Get likely interview questions, suggested talking points, and
                    questions to ask the interviewer — tailored to your documents
                    and the job posting.
                </p>
            """, unsafe_allow_html=True)

            if st.button("Generate Interview Prep Guide", type="primary"):
                with st.spinner("Preparing your interview guide... this may take 30-60 seconds."):
                    try:
                        resume_content = st.session_state.get("resume_content", "") \
                            if st.session_state.get("generate_resume") else ""
                        cover_letter_content = st.session_state.get("cover_letter_content", "") \
                            if st.session_state.get("generate_cover_letter") else ""
                        interview_guide = generate_interview_prep(
                            resume_content,
                            st.session_state["job_analysis"],
                            cover_letter_content)
                        st.session_state["interview_prep"] = interview_guide
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

            if "interview_prep" in st.session_state:
                st.markdown("""
                    <div style="border-left: 4px solid #0065A4; border-radius: 6px;
                        padding: 2px 16px; margin: 12px 0; background-color: #f0f7ff;">
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state["interview_prep"])

            st.divider()
            if st.button("Start Over", key="start_over_interview"):
                count = st.session_state.get("session_count", 0) + 1
                history = st.session_state.get("session_history", [])
                st.session_state.clear()
                st.session_state["session_count"] = count
                st.session_state["session_history"] = history
                st.rerun()

        with tab_history:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem; font-weight: 700;">This Session</span>
                </div>
                <p style="color: #555; font-size: 0.9rem; margin-top: 0;">
                    All documents generated during this session are listed below.
                    Download any version before closing the browser.
                </p>
            """, unsafe_allow_html=True)

            history = st.session_state.get("session_history", [])
            if not history:
                st.info("No documents generated yet in this session.")
            else:
                for i, entry in enumerate(reversed(history)):
                    idx = len(history) - 1 - i
                    with st.expander(f"Version {idx + 1} — Style: {entry['style']} | Tone: {entry['tone']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            if entry.get("resume"):
                                if st.button(f"Build Resume v{idx+1}", key=f"hist_resume_{idx}"):
                                    with st.spinner("Building..."):
                                        try:
                                            output_path = os.path.join("outputs", "resumes", f"resume_v{idx+1}.docx")
                                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                                            build_resume_document(entry["resume"], output_path, style_name=entry["style"])
                                            with open(output_path, "rb") as f:
                                                st.download_button(
                                                    label=f"Download Resume v{idx+1}", data=f,
                                                    file_name=f"resume_v{idx+1}.docx",
                                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                    key=f"dl_resume_{idx}")
                                        except Exception as e:
                                            st.error(f"Something went wrong: {e}")
                        with col2:
                            if entry.get("cover_letter"):
                                if st.button(f"Build Cover Letter v{idx+1}", key=f"hist_cl_{idx}"):
                                    with st.spinner("Building..."):
                                        try:
                                            output_path = os.path.join("outputs", "cover-letters", f"cover_letter_v{idx+1}.docx")
                                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                                            build_cover_letter_document(entry["cover_letter"], output_path, style_name=entry["style"])
                                            with open(output_path, "rb") as f:
                                                st.download_button(
                                                    label=f"Download Cover Letter v{idx+1}", data=f,
                                                    file_name=f"cover_letter_v{idx+1}.docx",
                                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                    key=f"dl_cl_{idx}")
                                        except Exception as e:
                                            st.error(f"Something went wrong: {e}")

            st.divider()
            if st.button("Start Over", key="start_over_history"):
                count = st.session_state.get("session_count", 0) + 1
                history = st.session_state.get("session_history", [])
                st.session_state.clear()
                st.session_state["session_count"] = count
                st.session_state["session_history"] = history
                st.rerun()

# ─────────────────────────────────────────
# PATH 2 — EVALUATE
# ─────────────────────────────────────────
elif st.session_state.get("path") == "evaluate":

    st.markdown("## Evaluating Your Documents")
    st.caption("Claude is analyzing your documents against the job posting...")

    cv_text = st.session_state.get("cv_text_for_eval", "")
    cl_text = st.session_state.get("cl_text_for_eval", "")

    if "path2_results" not in st.session_state:
        with st.spinner("Claude is deciding how to evaluate your documents... this may take 30-60 seconds."):
            try:
                evaluation = smart_evaluate(cv_text, cl_text, st.session_state["job_analysis"])
                st.session_state["path2_results"] = evaluation
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                import traceback
                st.error(traceback.format_exc())

    if "path2_results" in st.session_state:

        tab_eval_p2, tab_interview_p2 = st.tabs([
            "Smart Evaluation Report",
            "Interview Prep"
        ])

        with tab_eval_p2:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem; font-weight: 700;">Smart Evaluation Report</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state["path2_results"])

        with tab_interview_p2:
            st.markdown("""
                <div style="margin-bottom: 8px; margin-top: 12px;">
                    <span style="color: #0065A4; font-size: 1.3rem; font-weight: 700;">Interview Preparation</span>
                </div>
                <p style="color: #555; font-size: 0.9rem; margin-top: 0;">
                    Get likely interview questions and talking points based on
                    your documents and the job posting.
                </p>
            """, unsafe_allow_html=True)

            if st.button("Generate Interview Prep Guide", type="primary", key="interview_p2"):
                with st.spinner("Preparing your interview guide... this may take 30-60 seconds."):
                    try:
                        interview_guide = generate_interview_prep(
                            cv_text, st.session_state["job_analysis"], cl_text)
                        st.session_state["interview_prep_p2"] = interview_guide
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

            if "interview_prep_p2" in st.session_state:
                st.markdown(st.session_state["interview_prep_p2"])

        st.divider()
        if st.button("Switch to Generate New Documents", type="primary"):
            count = st.session_state.get("session_count", 0) + 1
            history = st.session_state.get("session_history", [])
            st.session_state.clear()
            st.session_state["session_count"] = count
            st.session_state["session_history"] = history
            st.session_state["path"] = "generate"
            st.session_state["step"] = "style"
            st.rerun()

    st.divider()
    if st.button("Start Over", key="start_over_p2"):
        count = st.session_state.get("session_count", 0) + 1
        history = st.session_state.get("session_history", [])
        st.session_state.clear()
        st.session_state["session_count"] = count
        st.session_state["session_history"] = history
        st.rerun()