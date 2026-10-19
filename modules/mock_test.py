# ============================================================
# MOCK TEST MODULE
# ============================================================

QUESTIONS = [
    {
        "question": "Which Python library is commonly used for data analysis?",
        "options": [
            "Pandas",
            "Django",
            "Flask",
            "Requests"
        ],
        "answer": "Pandas",
        "topic": "Python / Data Analysis"
    },

    {
        "question": "Which algorithm is commonly used for binary classification?",
        "options": [
            "Linear Regression",
            "Logistic Regression",
            "K-Means",
            "PCA"
        ],
        "answer": "Logistic Regression",
        "topic": "Machine Learning"
    },

    {
        "question": "Which library is mainly used for numerical computing in Python?",
        "options": [
            "NumPy",
            "BeautifulSoup",
            "Flask",
            "Django"
        ],
        "answer": "NumPy",
        "topic": "Python / NumPy"
    },

    {
        "question": "What does SQL stand for?",
        "options": [
            "Structured Query Language",
            "Simple Query Language",
            "System Query Logic",
            "Structured Question Language"
        ],
        "answer": "Structured Query Language",
        "topic": "SQL"
    },

    {
        "question": "Which function is used to split data into training and testing sets in Scikit-learn?",
        "options": [
            "train_test_split",
            "split_data",
            "data_split",
            "test_train"
        ],
        "answer": "train_test_split",
        "topic": "Scikit-learn"
    },

    {
        "question": "Which Git command is used to copy a repository?",
        "options": [
            "git push",
            "git commit",
            "git clone",
            "git merge"
        ],
        "answer": "git clone",
        "topic": "Git"
    },

    {
        "question": "Which technique can be used to handle missing numerical values?",
        "options": [
            "Mean imputation",
            "Tokenization",
            "One-hot encoding",
            "Stemming"
        ],
        "answer": "Mean imputation",
        "topic": "Data Preprocessing"
    },

    {
        "question": "Which metric is commonly used to evaluate a classification model?",
        "options": [
            "Accuracy",
            "Mean only",
            "R-squared only",
            "Variance only"
        ],
        "answer": "Accuracy",
        "topic": "Machine Learning"
    },

    {
        "question": "What does API stand for?",
        "options": [
            "Application Programming Interface",
            "Application Process Integration",
            "Advanced Programming Internet",
            "Application Program Internet"
        ],
        "answer": "Application Programming Interface",
        "topic": "API"
    },

    {
        "question": "Which technology is commonly used for containerization?",
        "options": [
            "Docker",
            "Excel",
            "NumPy",
            "Git"
        ],
        "answer": "Docker",
        "topic": "DevOps"
    }
]


# ============================================================
# GET QUESTIONS
# ============================================================

def get_questions():
    return QUESTIONS


# ============================================================
# CALCULATE SCORE
# ============================================================

def calculate_score(user_answers):

    score = 0

    total = len(QUESTIONS)

    for index in range(total):

        user_answer = user_answers.get(index)

        correct_answer = QUESTIONS[index]["answer"]

        if user_answer == correct_answer:
            score += 1

    percentage = round(
        (score / total) * 100,
        2
    )

    return score, total, percentage


# ============================================================
# GET FEEDBACK
# ============================================================

def get_feedback(percentage):

    if percentage >= 80:

        return (
            "Excellent performance! "
            "You have a strong understanding "
            "of the tested concepts."
        )

    elif percentage >= 60:

        return (
            "Good performance. "
            "Review the incorrect topics "
            "and strengthen your fundamentals."
        )

    elif percentage >= 40:

        return (
            "Average performance. "
            "Revise the important technical "
            "concepts before interviews."
        )

    else:

        return (
            "You need more preparation. "
            "Focus on Python, Machine Learning, "
            "SQL and core technical fundamentals."
        )