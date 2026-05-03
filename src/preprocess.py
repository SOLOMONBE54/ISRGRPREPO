import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# ----------------------------
# INIT
# ----------------------------
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


# ----------------------------
# PREPROCESS FUNCTION
# ----------------------------
def preprocess(text, use_stemming=True, remove_stopwords=True):
    """
    Clean + tokenize + optional stemming + optional stopword removal
    """

    # 1. lowercase
    text = text.lower()

    # 2. remove non-alphabetic noise
    tokens = re.findall(r"[a-z]+", text)

    # 3. remove stopwords (IMPORTANT for MAP improvement)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in stop_words]

    # 4. stemming (optional)
    if use_stemming:
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens