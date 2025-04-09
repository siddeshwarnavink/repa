import re
from sentence_transformers import SentenceTransformer, util
import numpy as np

# ---------------------------------
# Input parameters
# ---------------------------------
keyword_weights = {
    'python programming': 2,
    'machine learning projects': 3,
    'data analysis using pandas': 2,
    'deep learning with neural networks': 3
}
keywords = list(keyword_weights.keys())

resumes = [
    "Experienced in Python and machine learning. Worked on data analysis projects. 3 years of experience in Python.",
    "Skilled in deep learning and NLP. Proficient in Python. Worked with ML since 2020.",
    "Expert in data analysis and machine learning. Familiar with NLP techniques. Over 5 years working with Python."
]

# Mapping from variants to canonical keywords
skill_to_keyword = {
    'python': 'python programming',
    'ml': 'machine learning projects',
    'machine': 'machine learning projects',
    'data': 'data analysis using pandas',
    'deep': 'deep learning with neural networks',
    'dl': 'deep learning with neural networks',
}

# ---------------------------------
# Experience Extraction
# ---------------------------------
def extract_years_experience(text):
    patterns = [
        r'(\d+)\+?\s+years?\s+(?:of\s+)?experience\s+(?:in|with)?\s*(\w+)',
        r'over\s+(\d+)\s+years?\s+(?:working\s+)?(?:with|in)\s*(\w+)',
        r'(\w+).*(since\s+(\d{4}))'
    ]
    experience_map = {}
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                years, skill = match
                years = int(years)
            elif len(match) == 3:
                skill, _, year = match
                current_year = 2025
                years = current_year - int(year)
            else:
                continue
            skill = skill.lower()
            experience_map[skill] = max(experience_map.get(skill, 0), years)
    return experience_map

# ---------------------------------
# Contextual Matching
# ---------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
resume_embeddings = model.encode(resumes, convert_to_tensor=True)
keyword_embeddings = model.encode(keywords, convert_to_tensor=True)

similarity_matrix = util.cos_sim(resume_embeddings, keyword_embeddings).cpu().numpy()
weights = np.array([keyword_weights[k] for k in keywords])
base_scores = similarity_matrix @ weights

# ---------------------------------
# Bonus from Experience + Breakdown
# ---------------------------------
all_resume_data = []
for resume_idx, resume in enumerate(resumes):
    exp_map = extract_years_experience(resume)
    contextual_scores = similarity_matrix[resume_idx]
    experience_bonus = np.zeros(len(keywords))

    for skill, years in exp_map.items():
        for variant, keyword in skill_to_keyword.items():
            if variant in skill:
                idx = keywords.index(keyword)
                if years >= 5:
                    experience_bonus[idx] = 1.5
                elif years >= 3:
                    experience_bonus[idx] = 1.0
                elif years >= 1:
                    experience_bonus[idx] = 0.5

    total_per_skill = (contextual_scores * weights) + experience_bonus
    total_score = sum(total_per_skill)
    skill_breakdown = {
        k: {
            "contextual": round(contextual_scores[i] * weights[i], 2),
            "bonus": round(experience_bonus[i], 2),
            "total": round(total_per_skill[i], 2)
        }
        for i, k in enumerate(keywords)
    }

    all_resume_data.append({
        "resume": resume,
        "total_score": round(total_score, 2),
        "skill_breakdown": skill_breakdown
    })

# ---------------------------------
# Sort and Display
# ---------------------------------
sorted_data = sorted(all_resume_data, key=lambda x: x["total_score"], reverse=True)
max_score = sum(keyword_weights.values()) + 1.5 * len(keywords)

ACCEPT_THRESHOLD = 0.7  # Accept if score >= 70% of max possible
threshold_score = ACCEPT_THRESHOLD * max_score

for idx, data in enumerate(sorted_data, start=1):
    decision = "Accepted" if data['total_score'] >= threshold_score else "Rejected"
    print(f"Rank {idx} - Total Score: {data['total_score']}/{max_score} --> {decision}")
    print(f"Resume: {data['resume']}\n")
    print("Skill Breakdown:")
    for skill, score_info in data["skill_breakdown"].items():
        print(f"  - {skill}: Contextual = {score_info['contextual']}, Bonus = {score_info['bonus']}, Total = {score_info['total']}")
    print("\n" + "-" * 60 + "\n")
