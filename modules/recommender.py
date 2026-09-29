# -----------------------------
# AI Skill Recommendation Engine
# -----------------------------

RELATED_SKILLS = {
    "Python": [
        "FastAPI",
        "Flask",
        "Django",
        "Pandas",
        "NumPy"
    ],

    "SQL": [
        "MySQL",
        "PostgreSQL",
        "Database Design"
    ],

    "JavaScript": [
        "React",
        "Node.js",
        "TypeScript"
    ],

    "Machine Learning": [
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Data Science"
    ],

    "Git": [
        "GitHub",
        "GitLab",
        "Version Control"
    ],

    "REST API": [
        "FastAPI",
        "Flask",
        "API Testing"
    ],

    "React": [
        "JavaScript",
        "TypeScript",
        "Node.js"
    ]
}


def recommend_skills(missing_skills):

    recommendations = []

    for skill in missing_skills:

        related = RELATED_SKILLS.get(skill, [])

        for related_skill in related:

            if related_skill not in recommendations:
                recommendations.append(related_skill)

    return recommendations