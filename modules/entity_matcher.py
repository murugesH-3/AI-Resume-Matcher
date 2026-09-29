from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def find_related_entities(resume_text, job_description):
    """
    Compare sentences from the resume and job description
    using semantic similarity.
    """

    resume_sentences = [
        sentence.strip()
        for sentence in resume_text.split("\n")
        if sentence.strip()
    ]

    job_sentences = [
        sentence.strip()
        for sentence in job_description.split("\n")
        if sentence.strip()
    ]

    if not resume_sentences or not job_sentences:
        return []

    resume_embeddings = model.encode(resume_sentences)
    job_embeddings = model.encode(job_sentences)

    similarity_matrix = cosine_similarity(
        job_embeddings,
        resume_embeddings
    )

    results = []

    for i, job_sentence in enumerate(job_sentences):

        best_match_index = similarity_matrix[i].argmax()
        best_score = similarity_matrix[i][best_match_index]

        if best_score >= 0.55:

            results.append({
                "job_requirement": job_sentence,
                "resume_match": resume_sentences[best_match_index],
                "similarity": round(float(best_score) * 100, 2)
            })

    return results