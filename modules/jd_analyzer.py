import re


TECHNICAL_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "r",
    "html",
    "css",
    "react",
    "react.js",
    "node.js",
    "nodejs",
    "angular",
    "vue",
    "django",
    "flask",
    "fastapi",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sqlite",
    "redis",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "data science",
    "data analysis",
    "data engineering",
    "natural language processing",
    "nlp",
    "computer vision",
    "generative ai",
    "genai",
    "large language model",
    "llm",
    "rag",
    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",
    "opencv",
    "matplotlib",
    "seaborn",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "jenkins",
    "git",
    "github",
    "gitlab",
    "api",
    "rest api",
    "graphql",
    "langchain",
    "langgraph",
    "faiss",
    "excel",
    "power bi",
    "tableau",
]


def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(jd_text):

    if not jd_text:
        return []

    text = clean_text(jd_text)

    found_skills = []

    for skill in TECHNICAL_SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def extract_keywords(jd_text):

    if not jd_text:
        return []

    text = clean_text(jd_text)

    keywords = []

    important_keywords = [
        "intern",
        "internship",
        "developer",
        "software developer",
        "software engineer",
        "data analyst",
        "data scientist",
        "data engineer",
        "machine learning engineer",
        "ai engineer",
        "analyst",
        "engineer",
        "development",
        "programming",
        "coding",
        "testing",
        "debugging",
        "deployment",
        "data analysis",
        "data processing",
        "data pipeline",
        "data visualization",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "natural language processing",
        "computer vision",
        "generative ai",
        "api",
        "rest api",
        "integration",
        "communication",
        "teamwork",
        "leadership",
        "problem solving",
        "collaboration",
        "research",
        "documentation",
        "automation",
        "optimization",
        "scalability",
        "performance",
    ]

    for keyword in important_keywords:

        if keyword.lower() in text:
            keywords.append(keyword)

    keywords.extend(extract_skills(jd_text))

    return sorted(list(set(keywords)))


def extract_responsibilities(jd_text):

    if not jd_text:
        return []

    responsibilities = []

    lines = jd_text.split("\n")

    responsibility_words = [
        "responsible",
        "develop",
        "design",
        "build",
        "create",
        "implement",
        "maintain",
        "analyze",
        "test",
        "debug",
        "deploy",
        "manage",
        "support",
        "collaborate",
        "work with",
        "assist",
        "perform",
        "developing",
        "building",
        "creating",
        "implementing",
        "analyzing",
        "testing",
        "working",
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        cleaned_line = re.sub(
            r"^[•●▪◦\-*]+\s*",
            "",
            line
        )

        if any(
            word in line_lower
            for word in responsibility_words
        ):

            if cleaned_line not in responsibilities:
                responsibilities.append(cleaned_line)

    return responsibilities


def extract_required_terms(jd_text):

    if not jd_text:
        return []

    lines = jd_text.split("\n")

    required = []

    required_words = [
        "required",
        "must have",
        "must-have",
        "mandatory",
        "requirements",
        "qualifications",
        "should have",
        "strong knowledge",
        "proficiency",
    ]

    for line in lines:

        if any(
            word in line.lower()
            for word in required_words
        ):

            required.append(line.strip())

    return required


def extract_preferred_terms(jd_text):

    if not jd_text:
        return []

    lines = jd_text.split("\n")

    preferred = []

    preferred_words = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "good to have",
        "plus",
        "bonus",
        "desirable",
        "preferred qualifications",
    ]

    for line in lines:

        if any(
            word in line.lower()
            for word in preferred_words
        ):

            preferred.append(line.strip())

    return preferred


def analyze_job_description(jd_text):

    if not jd_text or not jd_text.strip():

        return {
            "skills": [],
            "keywords": [],
            "responsibilities": [],
            "required_terms": [],
            "preferred_terms": [],
        }

    return {
        "skills": extract_skills(jd_text),
        "keywords": extract_keywords(jd_text),
        "responsibilities": extract_responsibilities(jd_text),
        "required_terms": extract_required_terms(jd_text),
        "preferred_terms": extract_preferred_terms(jd_text),
    }