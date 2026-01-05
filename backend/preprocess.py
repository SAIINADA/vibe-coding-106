import nltk, re
nltk.download("punkt")

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return nltk.sent_tokenize(text)
