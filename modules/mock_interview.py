# ============================================================
# MOCK INTERVIEW MODULE
# ============================================================

import os
import re
import tempfile

import speech_recognition as sr
from gtts import gTTS


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

INTERVIEW_QUESTIONS = [
    {
        "question": "Tell me about yourself.",
        "keywords": [
            "education",
            "skills",
            "python",
            "machine learning",
            "project",
            "internship",
            "career"
        ],
        "expected_points": [
            "education",
            "technical skills",
            "projects",
            "internship or experience",
            "career goal"
        ]
    },

    {
        "question": "Explain your machine learning project.",
        "keywords": [
            "dataset",
            "preprocessing",
            "features",
            "model",
            "training",
            "testing",
            "accuracy",
            "prediction"
        ],
        "expected_points": [
            "dataset",
            "data preprocessing",
            "feature selection",
            "machine learning model",
            "training and testing",
            "evaluation metric",
            "result"
        ]
    },

    {
        "question": "What is the difference between supervised and unsupervised learning?",
        "keywords": [
            "supervised",
            "unsupervised",
            "label",
            "labeled",
            "classification",
            "regression",
            "clustering"
        ],
        "expected_points": [
            "supervised learning uses labeled data",
            "unsupervised learning uses unlabeled data",
            "classification or regression",
            "clustering"
        ]
    },

    {
        "question": "What is Python and why do you use it?",
        "keywords": [
            "python",
            "programming",
            "easy",
            "libraries",
            "pandas",
            "numpy",
            "scikit-learn"
        ],
        "expected_points": [
            "Python is a programming language",
            "easy syntax",
            "libraries",
            "data analysis",
            "machine learning"
        ]
    },

    {
        "question": "Why should we hire you?",
        "keywords": [
            "skills",
            "python",
            "machine learning",
            "learning",
            "problem solving",
            "team",
            "project"
        ],
        "expected_points": [
            "technical skills",
            "projects",
            "problem solving",
            "willingness to learn",
            "teamwork"
        ]
    },

    {
        "question": "What are your strengths?",
        "keywords": [
            "problem solving",
            "communication",
            "teamwork",
            "learning",
            "adaptability",
            "hardworking"
        ],
        "expected_points": [
            "specific strengths",
            "examples",
            "problem solving",
            "learning ability"
        ]
    },

    {
        "question": "What is SQL and where have you used it?",
        "keywords": [
            "sql",
            "database",
            "query",
            "select",
            "insert",
            "update",
            "delete",
            "data"
        ],
        "expected_points": [
            "SQL is used to interact with databases",
            "queries",
            "data retrieval",
            "data manipulation"
        ]
    },

    {
        "question": "Explain your most important project.",
        "keywords": [
            "project",
            "problem",
            "technology",
            "implementation",
            "result",
            "team",
            "role"
        ],
        "expected_points": [
            "problem",
            "technology used",
            "your role",
            "implementation",
            "result"
        ]
    },

    {
        "question": "How do you handle a difficult problem?",
        "keywords": [
            "understand",
            "problem",
            "analyze",
            "research",
            "solution",
            "test",
            "debug"
        ],
        "expected_points": [
            "understand the problem",
            "analyze",
            "research",
            "develop solution",
            "test",
            "debug"
        ]
    },

    {
        "question": "Where do you see yourself in the next five years?",
        "keywords": [
            "career",
            "skills",
            "experience",
            "growth",
            "learning",
            "technology",
            "responsibility"
        ],
        "expected_points": [
            "career growth",
            "technical expertise",
            "continuous learning",
            "increased responsibility"
        ]
    }
]


# ============================================================
# GET QUESTIONS
# ============================================================

def get_interview_questions():
    return INTERVIEW_QUESTIONS


# ============================================================
# CONVERT QUESTION TO SPEECH
# ============================================================

def question_to_speech(question):

    try:

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        temp_path = temp_file.name

        temp_file.close()

        tts = gTTS(
            text=question,
            lang="en",
            slow=False
        )

        tts.save(temp_path)

        return temp_path

    except Exception as e:

        return None


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text(audio_file):

    recognizer = sr.Recognizer()

    try:

        # Save Streamlit audio to temporary WAV file

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        temp_file.write(
            audio_file.getvalue()
        )

        temp_file.close()

        audio_path = temp_file.name

        # Read audio

        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

        # Google Speech Recognition

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        # Delete temporary file

        try:
            os.remove(audio_path)
        except:
            pass

        return text

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        return None

    except Exception:

        return None


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DETECT FILLER WORDS
# ============================================================

def detect_filler_words(text):

    filler_words = [
        "um",
        "umm",
        "uh",
        "uhh",
        "like",
        "actually",
        "basically",
        "you know",
        "sort of",
        "kind of",
        "maybe"
    ]

    text_lower = text.lower()

    found = []

    for word in filler_words:

        pattern = r"\b" + re.escape(word) + r"\b"

        matches = re.findall(
            pattern,
            text_lower
        )

        if matches:

            found.append(
                {
                    "word": word,
                    "count": len(matches)
                }
            )

    return found


# ============================================================
# CHECK KEYWORDS
# ============================================================

def check_keywords(answer, keywords):

    cleaned_answer = clean_text(answer)

    matched = []
    missing = []

    for keyword in keywords:

        keyword_clean = clean_text(
            keyword
        )

        if keyword_clean in cleaned_answer:

            matched.append(keyword)

        else:

            missing.append(keyword)

    return matched, missing


# ============================================================
# DETECT ANSWER QUALITY
# ============================================================

def analyze_answer(
    question_data,
    answer
):

    if not answer:

        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": question_data["keywords"],
            "filler_words": [],
            "word_count": 0,
            "mistakes": [
                "No answer was detected."
            ],
            "improvements": [
                "Speak clearly into the microphone.",
                "Give a complete answer.",
                "Include examples from your projects."
            ]
        }

    # --------------------------------------------------------
    # CLEAN ANSWER
    # --------------------------------------------------------

    cleaned_answer = clean_text(
        answer
    )

    words = cleaned_answer.split()

    word_count = len(words)

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    matched, missing = check_keywords(
        answer,
        question_data["keywords"]
    )

    # --------------------------------------------------------
    # FILLER WORDS
    # --------------------------------------------------------

    filler_words = detect_filler_words(
        answer
    )

    filler_count = sum(
        item["count"]
        for item in filler_words
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    keyword_score = 0

    if question_data["keywords"]:

        keyword_score = (
            len(matched)
            / len(question_data["keywords"])
        ) * 60

    # Answer length score

    if word_count >= 80:

        length_score = 20

    elif word_count >= 50:

        length_score = 15

    elif word_count >= 25:

        length_score = 10

    elif word_count >= 10:

        length_score = 5

    else:

        length_score = 0

    # Filler score

    if filler_count == 0:

        filler_score = 20

    elif filler_count <= 2:

        filler_score = 15

    elif filler_count <= 5:

        filler_score = 10

    else:

        filler_score = 5

    total_score = round(
        keyword_score
        + length_score
        + filler_score
    )

    total_score = min(
        total_score,
        100
    )

    # --------------------------------------------------------
    # MISTAKES
    # --------------------------------------------------------

    mistakes = []

    if word_count < 10:

        mistakes.append(
            "Your answer is too short."
        )

    if len(matched) < 2:

        mistakes.append(
            "Your answer does not cover enough important points."
        )

    if filler_count >= 3:

        mistakes.append(
            "You used too many filler words."
        )

    if not mistakes:

        mistakes.append(
            "No major problems detected."
        )

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    improvements = []

    if missing:

        improvements.append(
            "Include these important concepts: "
            + ", ".join(missing[:5])
        )

    if word_count < 30:

        improvements.append(
            "Give a more detailed answer with a specific example."
        )

    if filler_count >= 3:

        improvements.append(
            "Reduce filler words such as um, like and basically."
        )

    if word_count >= 30 and word_count < 50:

        improvements.append(
            "Add more detail to make your answer stronger."
        )

    improvements.append(
        "Use a clear structure: situation, action and result."
    )

    return {
        "score": total_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "filler_words": filler_words,
        "word_count": word_count,
        "mistakes": mistakes,
        "improvements": improvements
    }


# ============================================================
# GENERATE FEEDBACK
# ============================================================

def generate_feedback(
    score,
    analysis
):

    if score >= 80:

        feedback = (
            "Excellent answer. "
            "Your answer covers the important concepts "
            "and has good detail. "
            "Continue speaking clearly and confidently."
        )

    elif score >= 60:

        feedback = (
            "Good answer, but there is room for improvement. "
            "Add more relevant technical points and examples."
        )

    elif score >= 40:

        feedback = (
            "Your answer is partially correct. "
            "Try to provide more technical details, "
            "examples and a clearer structure."
        )

    else:

        feedback = (
            "Your answer needs significant improvement. "
            "Try to understand the question first and "
            "provide a structured answer with examples."
        )

    return feedback