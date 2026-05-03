import math
from collections import defaultdict
from src.preprocess import preprocess


# ----------------------------
# HELPER: IDF
# ----------------------------
def compute_idf(index, total_docs):
    """
    Compute inverse document frequency for all terms
    """

    idf = {}

    for term, postings in index.items():
        df = len(postings)
        idf[term] = math.log((total_docs + 1) / (df + 1)) + 1

    return idf


# ----------------------------
# TF-IDF SCORE
# ----------------------------
def tfidf_score(query, doc_id, index, doc_lengths, idf, use_stemming=True):

    query_terms = preprocess(query, use_stemming=use_stemming)

    score = 0.0

    for term in query_terms:

        if term in index and doc_id in index[term]:

            tf = index[term][doc_id]
            score += tf * idf.get(term, 0)

    return score


# ----------------------------
# BM25 SCORE
# ----------------------------
def bm25_score(query, doc_id, index, doc_lengths, idf,
               k1=1.5, b=0.75, use_stemming=True):

    query_terms = preprocess(query, use_stemming=use_stemming)

    doc_len = doc_lengths.get(doc_id, 0)
    avg_doc_len = sum(doc_lengths.values()) / len(doc_lengths)

    score = 0.0

    for term in query_terms:

        if term not in index:
            continue

        if doc_id not in index[term]:
            continue

        tf = index[term][doc_id]
        term_idf = idf.get(term, 0)

        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))

        score += term_idf * (numerator / denominator)

    return score


# ----------------------------
# RANK DOCUMENTS
# ----------------------------
def rank_documents(query, index, doc_lengths, model="bm25", use_stemming=True, top_k=10):

    docs = list(doc_lengths.keys())
    idf = compute_idf(index, len(docs))

    scores = []

    for doc_id in docs:

        if model == "bm25":
            score = bm25_score(query, doc_id, index, doc_lengths, idf, use_stemming=use_stemming)

        else:
            score = tfidf_score(query, doc_id, index, doc_lengths, idf, use_stemming=use_stemming)

        scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_k]