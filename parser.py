import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

keyword_weights = {
    'python': 2,
    'machine learning': 3,
    'data analysis': 2,
    'deep learning': 3
}
keywords = list(keyword_weights.keys())

resumes = [
    "Experienced in Python and machine learning. Worked on data analysis projects.",
    "Skilled in deep learning and NLP. Proficient in Python.",
    "Expert in data analysis and machine learning. Familiar with NLP techniques."
]

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

preprocessed_resumes = [preprocess(resume) for resume in resumes]

vectorizer = CountVectorizer(vocabulary=keywords, ngram_range=(1, 2), binary=True)
count_matrix = vectorizer.fit_transform(preprocessed_resumes).toarray()

weights = np.array([keyword_weights[key] for key in keywords])
scores = np.dot(count_matrix, weights)
ranked_resumes = sorted(zip(resumes, scores), key=lambda x: x[1], reverse=True)

total_possible_score = sum(keyword_weights.values())

for idx, (resume, score) in enumerate(ranked_resumes, start=1):
    print(f"Rank {idx} - Score: {score}/{total_possible_score}\nResume: {resume}\n")
