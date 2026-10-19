import re
import PyPDF2


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF."""

    text = ""

    try:
        reader = PyPDF2.PdfReader(pdf_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"PDF extraction error: {e}")

    return text


def extract_email(text):
    """Extract email address from resume text."""

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not Found"


def extract_phone(text):
    """Extract phone number from resume text."""

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not Found"


def extract_name(text):
    """Try to extract candidate name from the first few lines."""

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if lines:
        return lines[0]

    return "Not Found"


def extract_skills(text):
    """Extract common technical skills from resume."""

    skills_list = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "SQL",
        "MySQL",
        "MongoDB",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "OpenCV",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Generative AI",
        "Artificial Intelligence",
        "Streamlit",
        "Git",
        "GitHub",
        "AWS",
        "Docker",
        "RAG",
        "LangChain",
        "LangGraph"
    ]

    found_skills = []

    text_lower = text.lower()

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills