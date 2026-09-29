SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "React",
    "SQL",
    "MySQL",
    "MongoDB",
    "HTML",
    "CSS",
    "REST API",
    "FastAPI",
    "Flask",
    "Django",
    "Git",
    "GitHub",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "AWS",
    "Azure",
    "Docker",
]


def extract_skills(text):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matching_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    return matching_skills, missing_skills