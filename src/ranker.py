import math
from src.preprocess import preprocess


# ----------------------------
# IDF
# ----------------------------
def compute_idf(index, total_docs):
    idf = {}

    for term, postings in index.items():
        df = len(postings)
        idf[term] = math.log((total_docs - df + 0.5) / (df + 0.5)) + 1

    return idf


# ----------------------------
# TF-IDF SCORE
# ----------------------------
def tfidf_score(query_terms, doc_id, index, idf):
    score = 0.0

    for term in query_terms:
        if term in index and doc_id in index[term]:
            tf = index[term][doc_id]
            score += tf * idf.get(term, 0)

    return score


# ----------------------------
# BM25 SCORE
# ----------------------------
def bm25_score(query_terms, doc_id, index, doc_lengths, idf, avg_doc_len,
               k1=1.5, b=0.75):

    score = 0.0
    doc_len = doc_lengths.get(doc_id, 0)

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
def rank_documents(query_terms, index, doc_lengths, idf, model="bm25", top_k=100):

    scores = []

    avg_doc_len = sum(doc_lengths.values()) / len(doc_lengths)

    # 🔥 IMPORTANT: only score candidate docs (faster + better)
    candidate_docs = set()

    for term in query_terms:
        if term in index:
            candidate_docs.update(index[term].keys())

    for doc_id in candidate_docs:

        if model == "bm25":
            score = bm25_score(query_terms, doc_id, index, doc_lengths, idf, avg_doc_len)

        else:
            score = tfidf_score(query_terms, doc_id, index, idf)

        scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_k]


# ----------------------------
# RUN RANKING (ALL QUERIES)
# ----------------------------
def run_ranking(queries, index, doc_lengths, model="bm25", top_k=100, run_name="run"):

    results = {}

    total_docs = len(doc_lengths)
    idf = compute_idf(index, total_docs)

    print()

    for i, (qid, query_text) in enumerate(queries.items(), 1):

        print(f"Processing query {i}/{len(queries)}")

        # determine stemming from experiment name
        use_stemming = "Stem" in run_name

        query_terms = preprocess(query_text, use_stemming=use_stemming)

        ranked_docs = rank_documents(
            query_terms,
            index,
            doc_lengths,
            idf,
            model=model,
            top_k=top_k
        )

        # ✔ store (doc_id, score)
        results[qid] = ranked_docs

    return results


# ----------------------------
# SAVE RESULTS (TREC FORMAT)
# ----------------------------
def save_results(results, output_path, run_name):

    with open(output_path, "w") as f:

        for qid, ranked_docs in results.items():

            for rank, (doc_id, score) in enumerate(ranked_docs, start=1):

                f.write(f"{qid} Q0 {doc_id} {rank} {score:.6f} {run_name}\n")