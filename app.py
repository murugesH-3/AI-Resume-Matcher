import streamlit as st
import pymupdf
from docx import Document
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from modules.matcher import calculate_similarity
from modules.skill_extractor import compare_skills
from modules.entity_matcher import find_related_entities
from modules.recommender import recommend_skills


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Smart Resume Matcher",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RESUME TEXT EXTRACTION
# =========================================================

def extract_resume_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT resume."""

    file_name = uploaded_file.name.lower()

    # PDF
    if file_name.endswith(".pdf"):

        pdf = pymupdf.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    # DOCX
    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    # TXT
    elif file_name.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    return ""


# =========================================================
# CREATE PDF REPORT
# =========================================================

def create_pdf_report(
    match_percentage,
    matching_skills,
    missing_skills,
    recommended_skills,
    entity_matches
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=letter
    )

    width, height = letter

    # -----------------------------------------------------
    # PAGE 1 - TITLE
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawCentredString(
        width / 2,
        height - 70,
        "AI Smart Resume-Job Matcher"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        width / 2,
        height - 95,
        "AI-Powered Resume Analysis Report"
    )

    # -----------------------------------------------------
    # MATCH SCORE
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        height - 150,
        f"Semantic Match Score: {match_percentage}%"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        50,
        height - 170,
        "This score represents semantic similarity between "
        "the resume and the supplied job description."
    )

    y = height - 220

    # -----------------------------------------------------
    # MATCHING SKILLS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "1. Matching Skills"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        10
    )

    if matching_skills:

        for skill in matching_skills:

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

            y -= 18

    else:

        pdf.drawString(
            70,
            y,
            "No matching skills detected."
        )

        y -= 18

    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    y -= 15

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "2. Missing Skills"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        10
    )

    if missing_skills:

        for skill in missing_skills:

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

            y -= 18

    else:

        pdf.drawString(
            70,
            y,
            "No major missing skills detected."
        )

        y -= 18

    # -----------------------------------------------------
    # RECOMMENDED SKILLS
    # -----------------------------------------------------

    y -= 15

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "3. Recommended Skills"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        10
    )

    if recommended_skills:

        for skill in recommended_skills:

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

            y -= 18

    else:

        pdf.drawString(
            70,
            y,
            "No additional recommendations."
        )

        y -= 18

    # -----------------------------------------------------
    # PAGE 2 - ENTITY MATCHING
    # -----------------------------------------------------

    pdf.showPage()

    y = height - 60

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        y,
        "4. AI Semantic Entity Matching"
    )

    y -= 30

    if entity_matches:

        for index, match in enumerate(
            entity_matches,
            start=1
        ):

            if y < 120:

                pdf.showPage()

                y = height - 60

            pdf.setFont(
                "Helvetica-Bold",
                10
            )

            pdf.drawString(
                50,
                y,
                f"Match {index}"
            )

            y -= 18

            pdf.setFont(
                "Helvetica",
                9
            )

            pdf.drawString(
                60,
                y,
                "Job Requirement:"
            )

            y -= 14

            pdf.drawString(
                70,
                y,
                match["job_requirement"][:100]
            )

            y -= 18

            pdf.drawString(
                60,
                y,
                "Related Resume Content:"
            )

            y -= 14

            pdf.drawString(
                70,
                y,
                match["resume_match"][:100]
            )

            y -= 18

            pdf.drawString(
                60,
                y,
                f"Semantic Similarity: "
                f"{match['similarity']}%"
            )

            y -= 30

    else:

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            60,
            y,
            "No sufficiently related requirements detected."
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Oblique",
        8
    )

    pdf.drawCentredString(
        width / 2,
        30,
        "Generated by AI Smart Resume-Job Matcher"
    )

    pdf.save()

    buffer.seek(0)

    return buffer


# =========================================================
# APPLICATION TITLE
# =========================================================

st.markdown(
    '<div class="main-title">'
    '📄 AI Smart Resume–Job Matcher'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered semantic matching between resumes and job descriptions'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume and paste a job description "
    "to analyze the semantic match between them."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.subheader("1️⃣ Upload Resume")

resume_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx", "txt"]
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.subheader("2️⃣ Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250,
    placeholder="Paste the complete job description..."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("🔍 Analyze Resume"):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if resume_file is None:

        st.warning(
            "Please upload your resume."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter the job description."
        )

    else:

        # -------------------------------------------------
        # EXTRACT RESUME
        # -------------------------------------------------

        resume_text = extract_resume_text(
            resume_file
        )

        if not resume_text.strip():

            st.error(
                "Could not extract text from the resume."
            )

        else:

            st.success(
                "Resume successfully read!"
            )

            # -------------------------------------------------
            # EXTRACTED RESUME TEXT
            # -------------------------------------------------

            st.subheader(
                "📄 Extracted Resume Text"
            )

            st.text_area(
                "Resume content",
                resume_text,
                height=300
            )

            # -------------------------------------------------
            # AI SEMANTIC MATCHING
            # -------------------------------------------------

            st.subheader(
                "🤖 AI Semantic Matching"
            )

            with st.spinner(
                "AI is analyzing your resume and job description..."
            ):

                match_percentage = calculate_similarity(
                    resume_text,
                    job_description
                )

            # -------------------------------------------------
            # AI ANALYSIS DASHBOARD
            # -------------------------------------------------

            st.subheader(
                "📊 AI Analysis Dashboard"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🎯 Semantic Match",
                    f"{match_percentage}%"
                )

            with col2:

                st.metric(
                    "📄 Resume",
                    "Analyzed"
                )

            with col3:

                st.metric(
                    "🤖 AI Analysis",
                    "Completed"
                )

            st.progress(
                min(
                    max(
                        match_percentage / 100,
                        0.0
                    ),
                    1.0
                )
            )

            # -------------------------------------------------
            # MATCH EXPLANATION
            # -------------------------------------------------

            if match_percentage >= 80:

                st.success(
                    "Strong semantic similarity detected."
                )

            elif match_percentage >= 60:

                st.info(
                    "Good semantic similarity detected. "
                    "Some requirements may still be missing."
                )

            elif match_percentage >= 40:

                st.warning(
                    "Moderate semantic similarity detected. "
                    "Consider improving the resume for this job."
                )

            else:

                st.error(
                    "Low semantic similarity detected. "
                    "Several job requirements may be missing."
                )

            # -------------------------------------------------
            # SKILL ANALYSIS
            # -------------------------------------------------

            st.subheader(
                "🛠️ Skill Analysis"
            )

            matching_skills, missing_skills = compare_skills(
                resume_text,
                job_description
            )

            # -------------------------------------------------
            # SKILL STATISTICS
            # -------------------------------------------------

            st.markdown(
                "### 📈 Skill Statistics"
            )

            stat1, stat2 = st.columns(2)

            with stat1:

                st.metric(
                    "✅ Matching Skills",
                    len(matching_skills)
                )

            with stat2:

                st.metric(
                    "❌ Missing Skills",
                    len(missing_skills)
                )

            # -------------------------------------------------
            # MATCHING / MISSING SKILLS
            # -------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    "### ✅ Matching Skills"
                )

                if matching_skills:

                    st.success(
                        f"{len(matching_skills)} "
                        "matching skill(s) detected"
                    )

                    for skill in matching_skills:

                        st.markdown(
                            f"✅ **{skill}**"
                        )

                else:

                    st.info(
                        "No matching skills detected."
                    )

            with col2:

                st.markdown(
                    "### ❌ Missing Skills"
                )

                if missing_skills:

                    st.warning(
                        f"{len(missing_skills)} "
                        "skill(s) may need improvement"
                    )

                    for skill in missing_skills:

                        st.markdown(
                            f"❌ **{skill}**"
                        )

                else:

                    st.success(
                        "No missing skills detected."
                    )

            # -------------------------------------------------
            # AI SKILL RECOMMENDATIONS
            # -------------------------------------------------

            st.subheader(
                "🎯 AI Skill Recommendations"
            )

            recommended_skills = recommend_skills(
                missing_skills
            )

            if recommended_skills:

                st.write(
                    "Based on the missing skills, the AI "
                    "recommends these related technologies "
                    "and learning areas:"
                )

                for skill in recommended_skills:

                    st.markdown(
                        f"📚 **{skill}**"
                    )

            else:

                if missing_skills:

                    st.info(
                        "No additional related skills were found."
                    )

                else:

                    st.success(
                        "No major skill gaps were detected."
                    )

            # -------------------------------------------------
            # RESUME CONTENT ANALYSIS
            # -------------------------------------------------

            st.subheader(
                "📌 Resume Content Analysis"
            )

            st.write(
                "The system checks the resume for education, "
                "project, and experience-related information."
            )

            content_col1, content_col2, content_col3 = st.columns(3)

            resume_lower = resume_text.lower()

            with content_col1:

                st.info(
                    "🎓 Education"
                )

                if (
                    "education" in resume_lower
                    or "computer science" in resume_lower
                    or "bachelor" in resume_lower
                    or "degree" in resume_lower
                ):

                    st.success(
                        "Education information detected"
                    )

                else:

                    st.warning(
                        "Education information not clearly detected"
                    )

            with content_col2:

                st.info(
                    "💻 Projects"
                )

                project_words = [
                    "project",
                    "developed",
                    "built",
                    "implemented",
                    "application",
                    "system"
                ]

                if any(
                    word in resume_lower
                    for word in project_words
                ):

                    st.success(
                        "Project-related content detected"
                    )

                else:

                    st.warning(
                        "Project information not clearly detected"
                    )

            with content_col3:

                st.info(
                    "💼 Experience"
                )

                experience_words = [
                    "intern",
                    "internship",
                    "experience",
                    "developer",
                    "worked",
                    "responsibilities"
                ]

                if any(
                    word in resume_lower
                    for word in experience_words
                ):

                    st.success(
                        "Experience-related content detected"
                    )

                else:

                    st.warning(
                        "Experience information not clearly detected"
                    )

            # -------------------------------------------------
            # RESUME IMPROVEMENT SUGGESTIONS
            # -------------------------------------------------

            st.subheader(
                "💡 Resume Improvement Suggestions"
            )

            if missing_skills:

                st.write(
                    "Based on the job description, consider "
                    "improving your resume in the following areas:"
                )

                for skill in missing_skills:

                    st.markdown(
                        f"📌 **Add or strengthen: {skill}**"
                    )

                st.info(
                    "Tip: Add these skills only if you genuinely "
                    "have knowledge or experience with them."
                )

            else:

                st.success(
                    "Your resume already contains the main "
                    "skills detected from the job description."
                )

            # -------------------------------------------------
            # AI ENTITY MATCHING
            # -------------------------------------------------

            st.subheader(
                "🧠 AI Entity Matching"
            )

            st.write(
                "AI compares job requirements with resume "
                "content to identify semantically related information."
            )

            with st.spinner(
                "Finding related requirements using AI..."
            ):

                entity_matches = find_related_entities(
                    resume_text,
                    job_description
                )

            # -------------------------------------------------
            # AI ENTITY STATISTICS
            # -------------------------------------------------

            st.metric(
                "🧠 AI Related Matches",
                len(entity_matches)
            )

            if entity_matches:

                st.success(
                    f"{len(entity_matches)} related "
                    "requirement(s) identified by AI."
                )

                for index, match in enumerate(
                    entity_matches,
                    start=1
                ):

                    st.markdown(
                        f"### 🔹 Match {index}"
                    )

                    entity_col1, entity_col2 = st.columns(2)

                    with entity_col1:

                        st.markdown(
                            "**📋 Job Requirement**"
                        )

                        st.info(
                            match["job_requirement"]
                        )

                    with entity_col2:

                        st.markdown(
                            "**📄 Related Resume Content**"
                        )

                        st.success(
                            match["resume_match"]
                        )

                    st.metric(
                        "🧠 Semantic Similarity",
                        f"{match['similarity']}%"
                    )

                    st.divider()

            else:

                st.warning(
                    "No sufficiently related requirements were detected."
                )

            # -------------------------------------------------
            # DOWNLOAD PDF REPORT
            # -------------------------------------------------

            st.subheader(
                "📥 Download Analysis Report"
            )

            pdf_report = create_pdf_report(
                match_percentage,
                matching_skills,
                missing_skills,
                recommended_skills,
                entity_matches
            )

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_report,
                file_name="AI_Resume_Job_Analysis_Report.pdf",
                mime="application/pdf"
            )