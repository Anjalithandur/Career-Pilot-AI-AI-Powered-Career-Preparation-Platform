def calculate_ats_score(text):
    """
    Calculate a basic ATS-style resume compatibility score.
    Returns:
        score
        section_details
    """

    score = 0

    text = text.lower()

    section_details = {}

    # ---------------------------------------------
    # EDUCATION
    # ---------------------------------------------

    if (
        "education" in text
        or "b.tech" in text
        or "btech" in text
        or "degree" in text
        or "university" in text
        or "college" in text
    ):
        score += 15
        section_details["Education"] = True

    else:
        section_details["Education"] = False


    # ---------------------------------------------
    # SKILLS
    # ---------------------------------------------

    if (
        "skills" in text
        or "technical skills" in text
        or "technologies" in text
    ):
        score += 15
        section_details["Skills"] = True

    else:
        section_details["Skills"] = False


    # ---------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------

    if (
        "experience" in text
        or "internship" in text
        or "work experience" in text
    ):
        score += 15
        section_details["Experience"] = True

    else:
        section_details["Experience"] = False


    # ---------------------------------------------
    # PROJECTS
    # ---------------------------------------------

    if (
        "projects" in text
        or "project" in text
    ):
        score += 15
        section_details["Projects"] = True

    else:
        section_details["Projects"] = False


    # ---------------------------------------------
    # EMAIL / CONTACT
    # ---------------------------------------------

    if (
        "email" in text
        or "@" in text
    ):
        score += 10
        section_details["Email"] = True

    else:
        section_details["Email"] = False


    # ---------------------------------------------
    # PHONE
    # ---------------------------------------------

    if (
        "phone" in text
        or "mobile" in text
        or "contact" in text
    ):
        score += 10
        section_details["Phone"] = True

    else:
        section_details["Phone"] = False


    # ---------------------------------------------
    # SUMMARY / OBJECTIVE
    # ---------------------------------------------

    if (
        "summary" in text
        or "objective" in text
        or "profile" in text
    ):
        score += 10
        section_details["Summary"] = True

    else:
        section_details["Summary"] = False


    # ---------------------------------------------
    # CERTIFICATIONS
    # ---------------------------------------------

    if (
        "certification" in text
        or "certifications" in text
        or "certificate" in text
    ):
        score += 10
        section_details["Certifications"] = True

    else:
        section_details["Certifications"] = False


    # ---------------------------------------------
    # RETURN BOTH VALUES
    # ---------------------------------------------

    return score, section_details