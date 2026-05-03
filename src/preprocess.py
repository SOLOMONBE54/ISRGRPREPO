# src/preprocess.py

import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# -----------------------------
# TOKENIZATION
# -----------------------------
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return text.split()


# -----------------------------
# CORE PREPROCESS FUNCTION
# -----------------------------
def preprocess(text, use_stemming=True):
    """
    Preprocess text with optional stemming
    """

    tokens = tokenize(text)

    processed = []

    for token in tokens:
        if token in stop_words:
            continue
        if len(token) < 2:
            continue

        if use_stemming:
            token = stemmer.stem(token)

        processed.append(token)

    return processed