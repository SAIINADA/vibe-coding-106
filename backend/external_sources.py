import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Simulated external / internet-like corpus
EXTERNAL_CORPUS = [
    "Machine learning enables systems to learn automatically from data.",
    "Artificial intelligence is widely used in academic research.",
    "Plagiarism detection systems compare documents for similarity.",
    "Deep learning models require large datasets for training.",
    "Natural language processing helps machines understand text."
]

def external_similarity(text):
    if not text or len(text.strip()) < 20:
        return 0.0

    text_emb = model.encode(text)
    corpus_embs = model.encode(EXTERNAL_CORPUS)

    sims = np.dot(corpus_embs, text_emb) / (
        np.linalg.norm(corpus_embs, axis=1) * np.linalg.norm(text_emb)
    )

    return float(round(max(sims) * 100, 2))
