import streamlit as st

# ============================================================
# IMPORT MODULES
# ============================================================

from modules.resume_parser import extract_text_from_pdf
from modules.ats_analyzer import calculate_ats_score
from modules.jd_analyzer import analyze_job_description
from modules.matcher import complete_resume_jd_match

from modules.mock_test import (
    get_questions,
    calculate_score,
    get_feedback
)

from modules.mock_interview import (
    get_interview_questions,
    question_to_speech,
    speech_to_text,
    analyze_answer,
    generate_feedback
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Career Pilot AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "ats_score": None,
    "jd_match_score": None,
    "skill_match_score": None,

    "matching_skills": [],
    "missing_skills": [],

    "matching_keywords": [],
    "missing_keywords": [],

    "mock_score": None,
    "mock_percentage": None,

    "mock_started": False,
    "mock_submitted": False,
    "mock_answers": {},

    "interview_score": None,
    "interview_started": False,
    "interview_question_index": 0,
    "interview_results": []
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# TITLE
# ============================================================

st.title("🚀 Career Pilot AI")

st.write(
    "AI-powered platform for Resume Analysis, "
    "Job Matching, Mock Tests and Mock Interviews."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Resume Analyzer",
        "Job Description Analyzer",
        "Resume + JD Matching",
        "Mock Test",
        "Mock Interview",
        "Dashboard"
    ]
)


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.header("🏠 Welcome to Career Pilot AI")

    st.write(
        """
        Career Pilot AI helps students and job seekers
        prepare for interviews and job applications.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            📄 Resume Analyzer

            Analyze your resume and calculate ATS score.
            """
        )

    with col2:

        st.info(
            """
            🔗 Job Matcher

            Compare your resume with a job description.
            """
        )

    with col3:

        st.info(
            """
            🎙️ Mock Interview

            Practice interview questions using voice.
            """
        )

    st.success(
        "Select a module from the sidebar to begin."
    )


# ============================================================
# RESUME ANALYZER
# ============================================================

elif page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    st.write(
        "Upload your resume in PDF format."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        key="resume_upload"
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🔍 Analyze Resume",
            key="analyze_resume"
        ):

            try:

                resume_text = extract_text_from_pdf(
                    uploaded_file
                )

                if not resume_text:

                    st.error(
                        "Could not extract text from the PDF."
                    )

                else:

                    score, suggestions = calculate_ats_score(
                        resume_text
                    )

                    # Save ATS score
                    st.session_state.ats_score = score

                    st.subheader(
                        "📊 ATS Score"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "ATS Score",
                            f"{score}/100"
                        )

                    with col2:

                        st.progress(
                            min(score / 100, 1.0)
                        )

                    st.subheader(
                        "💡 Resume Suggestions"
                    )

                    if suggestions:

                        for suggestion in suggestions:

                            st.warning(
                                suggestion
                            )

                    else:

                        st.success(
                            "No major suggestions."
                        )

                    with st.expander(
                        "📄 View Resume Text"
                    ):

                        st.text(
                            resume_text
                        )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# ============================================================
# JOB DESCRIPTION ANALYZER
# ============================================================

elif page == "Job Description Analyzer":

    st.header(
        "💼 Job Description Analyzer"
    )

    jd_text = st.text_area(
        "Paste Job Description",
        height=350,
        placeholder="""
Example:

We are looking for an AI/ML Intern.

Requirements:
Python, Machine Learning, Pandas,
NumPy, Scikit-learn and SQL.

Responsibilities:
Develop machine learning models.
Analyze datasets.
Build data pipelines.
""",
        key="jd_analyzer_text"
    )

    if st.button(
        "🔍 Analyze Job Description",
        key="analyze_jd"
    ):

        if not jd_text.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            try:

                result = analyze_job_description(
                    jd_text
                )

                skills = result.get(
                    "skills",
                    []
                )

                keywords = result.get(
                    "keywords",
                    []
                )

                responsibilities = result.get(
                    "responsibilities",
                    []
                )

                required_terms = result.get(
                    "required_terms",
                    []
                )

                preferred_terms = result.get(
                    "preferred_terms",
                    []
                )

                st.subheader(
                    "🛠️ Detected Skills"
                )

                if skills:

                    for skill in skills:

                        st.success(
                            skill
                        )

                else:

                    st.info(
                        "No skills detected."
                    )

                st.subheader(
                    "🔑 Important Keywords"
                )

                if keywords:

                    st.write(
                        " • ".join(keywords)
                    )

                else:

                    st.info(
                        "No keywords detected."
                    )

                st.subheader(
                    "📋 Responsibilities"
                )

                if responsibilities:

                    for item in responsibilities:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.info(
                        "No responsibilities detected."
                    )

                st.subheader(
                    "⭐ Required Terms"
                )

                if required_terms:

                    for item in required_terms:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.info(
                        "No required terms detected."
                    )

                st.subheader(
                    "➕ Preferred Terms"
                )

                if preferred_terms:

                    for item in preferred_terms:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.info(
                        "No preferred terms detected."
                    )

            except Exception as e:

                st.error(
                    f"Error analyzing JD: {e}"
                )


# ============================================================
# RESUME + JD MATCHING
# ============================================================

elif page == "Resume + JD Matching":

    st.header(
        "🔗 Resume + Job Description Matching"
    )

    resume_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"],
        key="matching_resume"
    )

    jd_text = st.text_area(
        "💼 Paste Job Description",
        height=350,
        placeholder="""
Paste the complete job description here.

Example:

We are looking for a Python Developer.

Required:
Python, SQL, Pandas, Machine Learning and Git.

Preferred:
AWS and Docker.
""",
        key="matching_jd"
    )

    if st.button(
        "🚀 Match Resume With Job",
        key="match_resume"
    ):

        if resume_file is None:

            st.warning(
                "Please upload your resume."
            )

        elif not jd_text.strip():

            st.warning(
                "Please paste the job description."
            )

        else:

            try:

                resume_text = extract_text_from_pdf(
                    resume_file
                )

                jd_result = analyze_job_description(
                    jd_text
                )

                jd_skills = jd_result.get(
                    "skills",
                    []
                )

                jd_keywords = jd_result.get(
                    "keywords",
                    []
                )

                result = complete_resume_jd_match(
                    resume_text,
                    jd_skills,
                    jd_keywords
                )

                overall_score = result.get(
                    "overall_percentage",
                    0
                )

                skill_score = result.get(
                    "skill_percentage",
                    0
                )

                keyword_score = result.get(
                    "keyword_percentage",
                    0
                )

                matching_skills = result.get(
                    "matching_skills",
                    []
                )

                missing_skills = result.get(
                    "missing_skills",
                    []
                )

                matching_keywords = result.get(
                    "matching_keywords",
                    []
                )

                missing_keywords = result.get(
                    "missing_keywords",
                    []
                )

                # Save results
                st.session_state.jd_match_score = (
                    overall_score
                )

                st.session_state.skill_match_score = (
                    skill_score
                )

                st.session_state.matching_skills = (
                    matching_skills
                )

                st.session_state.missing_skills = (
                    missing_skills
                )

                st.session_state.matching_keywords = (
                    matching_keywords
                )

                st.session_state.missing_keywords = (
                    missing_keywords
                )

                # Display
                st.subheader(
                    "🎯 Matching Results"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Overall Match",
                        f"{overall_score}%"
                    )

                with col2:

                    st.metric(
                        "Skill Match",
                        f"{skill_score}%"
                    )

                with col3:

                    st.metric(
                        "Keyword Match",
                        f"{keyword_score}%"
                    )

                st.progress(
                    min(
                        overall_score / 100,
                        1.0
                    )
                )

                st.subheader(
                    "✅ Matching Skills"
                )

                if matching_skills:

                    for skill in matching_skills:

                        st.success(
                            f"✓ {skill}"
                        )

                else:

                    st.info(
                        "No matching skills found."
                    )

                st.subheader(
                    "❌ Missing Skills"
                )

                if missing_skills:

                    for skill in missing_skills:

                        st.error(
                            f"✗ {skill}"
                        )

                else:

                    st.success(
                        "No missing skills detected."
                    )

                st.subheader(
                    "🔑 Matching Keywords"
                )

                if matching_keywords:

                    st.write(
                        " • ".join(
                            matching_keywords
                        )
                    )

                else:

                    st.info(
                        "No matching keywords."
                    )

                st.subheader(
                    "⚠️ Missing Keywords"
                )

                if missing_keywords:

                    st.write(
                        " • ".join(
                            missing_keywords
                        )
                    )

                else:

                    st.success(
                        "No missing keywords."
                    )

            except Exception as e:

                st.error(
                    f"Error during matching: {e}"
                )


# ============================================================
# MOCK TEST
# ============================================================

elif page == "Mock Test":

    st.header(
        "🎤 Mock Test"
    )

    questions = get_questions()

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    if not st.session_state.mock_started:

        st.subheader(
            "📋 Test Instructions"
        )

        st.info(
            f"""
            Total Questions: {len(questions)}

            Each question carries 1 mark.

            Select the correct answer and submit
            the test at the end.
            """
        )

        if st.button(
            "🚀 Start Mock Test",
            key="start_mock"
        ):

            st.session_state.mock_started = True

            st.session_state.mock_submitted = False

            st.session_state.mock_answers = {}

            st.rerun()

    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    elif not st.session_state.mock_submitted:

        st.subheader(
            "📝 Answer the Questions"
        )

        for index, question in enumerate(
            questions
        ):

            st.markdown(
                f"### Question {index + 1}"
            )

            st.write(
                question["question"]
            )

            answer = st.radio(
                "Select answer:",
                question["options"],
                key=f"mock_q_{index}"
            )

            st.session_state.mock_answers[
                index
            ] = answer

            st.divider()

        if st.button(
            "📤 Submit Mock Test",
            key="submit_mock"
        ):

            st.session_state.mock_submitted = True

            st.rerun()

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    else:

        score, total, percentage = calculate_score(
            st.session_state.mock_answers
        )

        st.session_state.mock_score = score

        st.session_state.mock_percentage = percentage

        st.subheader(
            "🏆 Mock Test Result"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Score",
                f"{score}/{total}"
            )

        with col2:

            st.metric(
                "Percentage",
                f"{percentage}%"
            )

        with col3:

            if percentage >= 80:

                performance = "Excellent"

            elif percentage >= 60:

                performance = "Good"

            elif percentage >= 40:

                performance = "Average"

            else:

                performance = "Needs Improvement"

            st.metric(
                "Performance",
                performance
            )

        st.progress(
            min(
                percentage / 100,
                1.0
            )
        )

        feedback = get_feedback(
            percentage
        )

        st.info(
            feedback
        )

        st.subheader(
            "📚 Answer Review"
        )

        for index, question in enumerate(
            questions
        ):

            user_answer = (
                st.session_state.mock_answers.get(
                    index
                )
            )

            correct_answer = question[
                "answer"
            ]

            st.write(
                f"### Question {index + 1}"
            )

            st.write(
                question["question"]
            )

            if user_answer == correct_answer:

                st.success(
                    f"Your Answer: {user_answer} ✅"
                )

            else:

                st.error(
                    f"Your Answer: {user_answer} ❌"
                )

                st.success(
                    f"Correct Answer: {correct_answer}"
                )

            st.divider()

        if st.button(
            "🔄 Restart Mock Test",
            key="restart_mock"
        ):

            st.session_state.mock_started = False

            st.session_state.mock_submitted = False

            st.session_state.mock_answers = {}

            st.session_state.mock_score = None

            st.session_state.mock_percentage = None

            st.rerun()


# ============================================================
# MOCK INTERVIEW
# ============================================================

elif page == "Mock Interview":

    st.header(
        "🎙️ AI Mock Interview"
    )

    st.write(
        """
        Practice a real interview using your microphone.

        The interviewer asks questions using voice.
        You answer using your microphone.
        Your answer is converted to text and analyzed.
        """
    )

    questions = get_interview_questions()

    # ========================================================
    # START INTERVIEW
    # ========================================================

    if not st.session_state.interview_started:

        st.subheader(
            "📋 Interview Instructions"
        )

        st.info(
            """
            🎧 Listen to the question.

            🎙️ Record your answer.

            📝 Your speech will be converted into text.

            🔍 Your answer will be analyzed.

            💡 You will receive improvement suggestions.

            🔊 Feedback will also be provided as audio.
            """
        )

        st.write(
            f"Total Questions: {len(questions)}"
        )
        if st.button(
            "🚀 Start Mock Interview",
            key="start_interview"
        ):

            st.session_state.interview_started = True

            st.session_state.interview_question_index = 0

            st.session_state.interview_results = []

            st.session_state.interview_score = None

            st.rerun()

    else:

        current_index = (
            st.session_state.interview_question_index
        )

        # ====================================================
        # INTERVIEW COMPLETE
        # ====================================================

        if current_index >= len(questions):

            st.subheader(
                "🏆 Interview Completed"
            )

            results = (
                st.session_state.interview_results
            )

            if results:

                total_score = sum(
                    result["analysis"]["score"]
                    for result in results
                )

                average_score = round(
                    total_score / len(results)
                )

            else:

                average_score = 0

            st.session_state.interview_score = (
                average_score
            )

            st.metric(
                "🎙️ Mock Interview Score",
                f"{average_score}/100"
            )

            st.progress(
                min(
                    average_score / 100,
                    1.0
                )
            )

            if average_score >= 80:

                st.success(
                    "Excellent interview performance! 🌟"
                )

            elif average_score >= 60:

                st.info(
                    "Good performance. Keep practicing."
                )

            elif average_score >= 40:

                st.warning(
                    "More interview practice is recommended."
                )

            else:

                st.error(
                    "Work on your technical fundamentals and communication."
                )

            st.subheader(
                "📊 Interview Review"
            )

            for index, result in enumerate(
                results
            ):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(
                    result["question"]
                )

                st.metric(
                    "Score",
                    f"{result['analysis']['score']}/100"
                )

                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    result["answer"]
                )

                st.divider()

            if st.button(
                "🔄 Start New Interview",
                key="new_interview"
            ):

                st.session_state.interview_started = False

                st.session_state.interview_question_index = 0

                st.session_state.interview_results = []

                st.session_state.interview_score = None

                st.rerun()

        # ====================================================
        # CURRENT QUESTION
        # ====================================================

        else:

            question_data = questions[
                current_index
            ]

            question = question_data[
                "question"
            ]

            st.subheader(
                f"Question {current_index + 1} "
                f"of {len(questions)}"
            )

            st.markdown(
                f"## 🎤 {question}"
            )

            # ------------------------------------------------
            # QUESTION AUDIO
            # ------------------------------------------------

            audio_path = question_to_speech(
                question
            )

            if audio_path:

                st.audio(
                    audio_path,
                    format="audio/mp3"
                )

            else:

                st.warning(
                    "Could not generate question audio."
                )

            st.divider()

            # ------------------------------------------------
            # USER AUDIO
            # ------------------------------------------------

            st.subheader(
                "🎙️ Record Your Answer"
            )

            st.write(
                "Click the microphone button and speak clearly."
            )

            audio_input = st.audio_input(
                "Record your answer",
                key=f"interview_audio_{current_index}"
            )

            if audio_input:

                st.success(
                    "Answer recorded successfully."
                )

                st.audio(
                    audio_input,
                    format="audio/wav"
                )

                if st.button(
                    "🔍 Analyze My Answer",
                    key=f"analyze_interview_{current_index}"
                ):

                    with st.spinner(
                        "Converting speech to text..."
                    ):

                        answer_text = speech_to_text(
                            audio_input
                        )

                    # ----------------------------------------
                    # SPEECH ERROR
                    # ----------------------------------------

                    if answer_text is None:

                        st.error(
                            """
                            Speech recognition failed.
                            Please check your internet connection
                            and try again.
                            """
                        )

                    elif not answer_text:

                        st.error(
                            """
                            I could not understand your answer.
                            Please record it again.
                            """
                        )

                    else:

                        st.subheader(
                            "📝 Your Answer"
                        )

                        st.write(
                            answer_text
                        )

                        # ------------------------------------
                        # ANALYZE
                        # ------------------------------------

                        analysis = analyze_answer(
                            question_data,
                            answer_text
                        )

                        score = analysis[
                            "score"
                        ]

                        # ------------------------------------
                        # SAVE RESULT
                        # ------------------------------------

                        already_saved = False

                        for result in (
                            st.session_state.interview_results
                        ):

                            if result["question"] == question:

                                already_saved = True

                        if not already_saved:

                            st.session_state.interview_results.append(
                                {
                                    "question": question,
                                    "answer": answer_text,
                                    "analysis": analysis
                                }
                            )

                        # ------------------------------------
                        # SCORE
                        # ------------------------------------

                        st.subheader(
                            "📊 Answer Analysis"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.metric(
                                "Answer Score",
                                f"{score}/100"
                            )

                        with col2:

                            st.metric(
                                "Word Count",
                                analysis["word_count"]
                            )

                        with col3:

                            st.metric(
                                "Points Matched",
                                len(
                                    analysis[
                                        "matched_keywords"
                                    ]
                                )
                            )

                        st.progress(
                            min(
                                score / 100,
                                1.0
                            )
                        )

                        # ------------------------------------
                        # MATCHED
                        # ------------------------------------

                        st.subheader(
                            "✅ Detected Points"
                        )

                        if analysis[
                            "matched_keywords"
                        ]:

                            for keyword in analysis[
                                "matched_keywords"
                            ]:

                                st.success(
                                    keyword
                                )

                        else:

                            st.warning(
                                "No important points detected."
                            )

                        # ------------------------------------
                        # MISSING
                        # ------------------------------------

                        st.subheader(
                            "❌ Missing Points"
                        )

                        if analysis[
                            "missing_keywords"
                        ]:

                            for keyword in analysis[
                                "missing_keywords"
                            ]:

                                st.error(
                                    keyword
                                )

                        else:

                            st.success(
                                "Good coverage of important points."
                            )

                        # ------------------------------------
                        # FILLER WORDS
                        # ------------------------------------

                        st.subheader(
                            "🗣️ Filler Words"
                        )

                        if analysis[
                            "filler_words"
                        ]:

                            for item in analysis[
                                "filler_words"
                            ]:

                                st.warning(
                                    f"{item['word']} "
                                    f"→ {item['count']} time(s)"
                                )

                        else:

                            st.success(
                                "No major filler words detected."
                            )

                        # ------------------------------------
                        # MISTAKES
                        # ------------------------------------

                        st.subheader(
                            "⚠️ Mistakes / Weak Areas"
                        )

                        for mistake in analysis[
                            "mistakes"
                        ]:

                            st.warning(
                                mistake
                            )

                        # ------------------------------------
                        # IMPROVEMENTS
                        # ------------------------------------

                        st.subheader(
                            "💡 How to Improve"
                        )

                        for improvement in analysis[
                            "improvements"
                        ]:

                            st.info(
                                improvement
                            )

                        # ------------------------------------
                        # VOICE FEEDBACK
                        # ------------------------------------

                        feedback = generate_feedback(
                            score,
                            analysis
                        )

                        st.subheader(
                            "🔊 AI Feedback"
                        )

                        feedback_audio = question_to_speech(
                            feedback
                        )

                        if feedback_audio:

                            st.audio(
                                feedback_audio,
                                format="audio/mp3"
                            )

                        st.write(
                            feedback
                        )

                        st.divider()

                        # ------------------------------------
                        # NEXT QUESTION
                        # ------------------------------------

                        if st.button(
                            "➡️ Next Question",
                            key=f"next_interview_{current_index}"
                        ):

                            st.session_state.interview_question_index += 1

                            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.header(
        "📊 Career Dashboard"
    )

    st.write(
        "Your complete Career Pilot AI performance."
    )

    # ========================================================
    # SCORE CARDS
    # ========================================================

    st.subheader(
        "📌 Performance Overview"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        if st.session_state.ats_score is not None:

            st.metric(
                "📄 ATS",
                f"{st.session_state.ats_score}/100"
            )

        else:

            st.metric(
                "📄 ATS",
                "N/A"
            )

    with col2:

        if st.session_state.jd_match_score is not None:

            st.metric(
                "🎯 JD Match",
                f"{st.session_state.jd_match_score}%"
            )

        else:

            st.metric(
                "🎯 JD Match",
                "N/A"
            )

    with col3:

        if st.session_state.skill_match_score is not None:

            st.metric(
                "🛠️ Skills",
                f"{st.session_state.skill_match_score}%"
            )

        else:

            st.metric(
                "🛠️ Skills",
                "N/A"
            )

    with col4:

        if st.session_state.mock_percentage is not None:

            st.metric(
                "🎤 Mock Test",
                f"{st.session_state.mock_percentage}%"
            )

        else:

            st.metric(
                "🎤 Mock Test",
                "N/A"
            )

    with col5:

        if st.session_state.interview_score is not None:

            st.metric(
                "🎙️ Interview",
                f"{st.session_state.interview_score}/100"
            )

        else:

            st.metric(
                "🎙️ Interview",
                "N/A"
            )

    # ========================================================
    # OVERALL SCORE
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Overall Career Preparation"
    )

    scores = []

    if st.session_state.ats_score is not None:

        scores.append(
            st.session_state.ats_score
        )

    if st.session_state.jd_match_score is not None:

        scores.append(
            st.session_state.jd_match_score
        )

    if st.session_state.mock_percentage is not None:

        scores.append(
            st.session_state.mock_percentage
        )

    if st.session_state.interview_score is not None:

        scores.append(
            st.session_state.interview_score
        )

    if scores:

        overall_score = round(
            sum(scores) / len(scores)
        )

        st.metric(
            "Overall Preparation",
            f"{overall_score}%"
        )

        st.progress(
            min(
                overall_score / 100,
                1.0
            )
        )

    else:

        overall_score = 0

        st.info(
            """
            Complete the modules to generate
            your overall preparation score.
            """
        )

    # ========================================================
    # SKILL GAP
    # ========================================================

    st.divider()

    st.subheader(
        "🧩 Skill Gap"
    )

    if st.session_state.missing_skills:

        for skill in st.session_state.missing_skills:

            st.warning(
                f"❌ {skill}"
            )

    else:

        st.info(
            "Complete Resume + JD Matching first."
        )

    # ========================================================
    # MATCHING SKILLS
    # ========================================================

    st.subheader(
        "✅ Matching Skills"
    )

    if st.session_state.matching_skills:

        for skill in st.session_state.matching_skills:

            st.success(
                f"✓ {skill}"
            )

    else:

        st.info(
            "No matching skill data yet."
        )

    # ========================================================
    # KEYWORDS
    # ========================================================

    st.subheader(
        "🔑 Keyword Analysis"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Matching Keywords**"
        )

        if st.session_state.matching_keywords:

            for keyword in (
                st.session_state.matching_keywords
            ):

                st.write(
                    f"✅ {keyword}"
                )

        else:

            st.write(
                "No data."
            )

    with col2:

        st.write(
            "**Missing Keywords**"
        )

        if st.session_state.missing_keywords:

            for keyword in (
                st.session_state.missing_keywords
            ):

                st.write(
                    f"⚠️ {keyword}"
                )

        else:

            st.write(
                "No data."
            )

    # ========================================================
    # INTERVIEW SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "🎙️ Mock Interview"
    )

    if st.session_state.interview_score is not None:

        st.metric(
            "Interview Score",
            f"{st.session_state.interview_score}/100"
        )

        st.progress(
            min(
                st.session_state.interview_score / 100,
                1.0
            )
        )

    else:

        st.info(
            "Complete the Mock Interview to see your score."
        )

    # ========================================================
    # FINAL FEEDBACK
    # ========================================================

    st.divider()

    st.subheader(
        "💡 Career Feedback"
    )

    if not scores:

        st.info(
            "Complete the modules first."
        )

    elif overall_score >= 80:

        st.success(
            """
            Your current preparation metrics are strong.
            Continue practicing interviews and improving
            your resume.
            """
        )

    elif overall_score >= 60:

        st.warning(
            """
            Your preparation is developing well.
            Focus on your missing skills and interview
            performance.
            """
        )

    else:

        st.warning(
            """
            More preparation is recommended.
            Focus on ATS optimization, job matching,
            technical knowledge and interview practice.
            """
        )

    # ========================================================
    # MODULE STATUS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Module Status"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        if st.session_state.ats_score is not None:

            st.success("✅ ATS")

        else:

            st.warning("⏳ ATS")

    with col2:

        if st.session_state.jd_match_score is not None:

            st.success("✅ Job Match")

        else:

            st.warning("⏳ Job Match")

    with col3:

        if st.session_state.mock_percentage is not None:

            st.success("✅ Mock Test")

        else:

            st.warning("⏳ Mock Test")

    with col4:

        if st.session_state.interview_score is not None:

            st.success("✅ Interview")

        else:

            st.warning("⏳ Interview")

    with col5:

        if scores:

            st.success("✅ Dashboard")

        else:

            st.warning("⏳ Dashboard")


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "🚀 Career Pilot AI"
)

st.sidebar.caption(
    "Resume • ATS • JD Match • Mock Test • Mock Interview"
)