import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(a, b):
    e1 = model.encode(a)
    e2 = model.encode(b)
    return np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
