from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

keyword_weights = {
    'python programming': 2,
    'machine learning projects': 3,
    'data analysis using pandas': 2,
    'deep learning with neural networks': 3
}
keywords = list(keyword_weights.keys())

resumes = [
    "Experienced in Python and machine learning. Worked on data analysis projects.",
    "Skilled in deep learning and NLP. Proficient in Python.",
    "Expert in data analysis and machine learning. Familiar with NLP techniques."
]

resume_embeddings = model.encode(resumes, convert_to_tensor=True)
keyword_embeddings = model.encode(keywords, convert_to_tensor=True)

similarity_matrix = util.cos_sim(resume_embeddings, keyword_embeddings).cpu().numpy()

weights = np.array([keyword_weights[k] for k in keywords])
weighted_scores = similarity_matrix @ weights

ranked_resumes = sorted(zip(resumes, weighted_scores), key=lambda x: x[1], reverse=True)

total_possible_score = sum(keyword_weights.values())

for idx, (resume, score) in enumerate(ranked_resumes, start=1):
    print(f"Rank {idx} - Contextual Score: {score:.2f}/{total_possible_score}\nResume: {resume}\n")
