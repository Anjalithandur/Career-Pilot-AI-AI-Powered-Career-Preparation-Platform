# ============================================================
# RESUME - JOB DESCRIPTION MATCHER
# ============================================================


def normalize_skill(skill):
    """
    Normalize different names of the same skill.
    """

    skill = skill.lower().strip()

    replacements = {
        "nodejs": "node.js",
        "node js": "node.js",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "ml": "machine learning",
        "genai": "generative ai",
        "restful api": "rest api",
        "amazon web services": "aws",
        "microsoft azure": "azure",
        "google cloud": "gcp"
    }

    return replacements.get(
        skill,
        skill
    )


# ============================================================
# CHECK SKILL IN RESUME
# ============================================================

def skill_exists_in_resume(resume_text, skill):

    if not resume_text:
        return False

    resume_text = resume_text.lower()

    skill = normalize_skill(skill)

    aliases = {

        "python": [
            "python"
        ],

        "java": [
            "java"
        ],

        "javascript": [
            "javascript",
            "java script"
        ],

        "typescript": [
            "typescript"
        ],

        "machine learning": [
            "machine learning",
            "machine-learning"
        ],

        "deep learning": [
            "deep learning",
            "deep-learning"
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "artificial-intelligence"
        ],

        "generative ai": [
            "generative ai",
            "generative-ai",
            "genai"
        ],

        "scikit-learn": [
            "scikit-learn",
            "scikit learn",
            "sklearn"
        ],

        "node.js": [
            "node.js",
            "nodejs",
            "node js"
        ],

        "rest api": [
            "rest api",
            "restful api"
        ],

        "aws": [
            "aws",
            "amazon web services"
        ],

        "azure": [
            "azure",
            "microsoft azure"
        ],

        "gcp": [
            "gcp",
            "google cloud",
            "google cloud platform"
        ],

        "pandas": [
            "pandas"
        ],

        "numpy": [
            "numpy"
        ],

        "sql": [
            "sql",
            "mysql",
            "postgresql"
        ],

        "c++": [
            "c++"
        ],

        "c#": [
            "c#"
        ]
    }

    search_terms = aliases.get(
        skill,
        [skill]
    )

    for term in search_terms:

        if term in resume_text:
            return True

    return False


# ============================================================
# MATCH SKILLS
# ============================================================

def match_resume_with_jd(
    resume_text,
    jd_skills
):

    if not jd_skills:

        return {
            "matching_skills": [],
            "missing_skills": [],
            "match_percentage": 0
        }

    matching_skills = []
    missing_skills = []

    for skill in jd_skills:

        if skill_exists_in_resume(
            resume_text,
            skill
        ):

            matching_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    total_skills = len(jd_skills)

    match_percentage = round(
        (
            len(matching_skills)
            / total_skills
        ) * 100,
        2
    )

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }


# ============================================================
# MATCH KEYWORDS
# ============================================================

def match_keywords(
    resume_text,
    jd_keywords
):

    if not jd_keywords:

        return {
            "matching_keywords": [],
            "missing_keywords": [],
            "keyword_percentage": 0
        }

    resume_text = resume_text.lower()

    matching_keywords = []
    missing_keywords = []

    for keyword in jd_keywords:

        keyword = keyword.lower().strip()

        if keyword in resume_text:

            matching_keywords.append(
                keyword
            )

        else:

            missing_keywords.append(
                keyword
            )

    total_keywords = len(jd_keywords)

    keyword_percentage = round(
        (
            len(matching_keywords)
            / total_keywords
        ) * 100,
        2
    )

    return {
        "matching_keywords": matching_keywords,
        "missing_keywords": missing_keywords,
        "keyword_percentage": keyword_percentage
    }


# ============================================================
# COMPLETE RESUME-JD MATCH
# ============================================================

def complete_resume_jd_match(
    resume_text,
    jd_skills,
    jd_keywords
):

    # Get skill matching result
    skill_result = match_resume_with_jd(
        resume_text,
        jd_skills
    )

    # Get keyword matching result
    keyword_result = match_keywords(
        resume_text,
        jd_keywords
    )

    skill_percentage = skill_result[
        "match_percentage"
    ]

    keyword_percentage = keyword_result[
        "keyword_percentage"
    ]

    # Overall match
    overall_percentage = round(
        (
            skill_percentage * 0.70
        )
        +
        (
            keyword_percentage * 0.30
        ),
        2
    )

    return {

        "matching_skills":
            skill_result[
                "matching_skills"
            ],

        "missing_skills":
            skill_result[
                "missing_skills"
            ],

        "skill_percentage":
            skill_percentage,

        "matching_keywords":
            keyword_result[
                "matching_keywords"
            ],

        "missing_keywords":
            keyword_result[
                "missing_keywords"
            ],

        "keyword_percentage":
            keyword_percentage,

        "overall_percentage":
            overall_percentage
    }