import math


# ----------------------------
# PRECISION @ K
# ----------------------------
def precision_at_k(ranked_docs, relevant_docs, k=10):

    if k == 0:
        return 0

    ranked_docs = ranked_docs[:k]

    retrieved_relevant = 0

    for doc_id, _ in ranked_docs:
        if doc_id in relevant_docs:
            retrieved_relevant += 1

    return retrieved_relevant / k


# ----------------------------
# RECALL
# ----------------------------
def recall(ranked_docs, relevant_docs):

    if len(relevant_docs) == 0:
        return 0

    retrieved_relevant = 0

    for doc_id, _ in ranked_docs:
        if doc_id in relevant_docs:
            retrieved_relevant += 1

    return retrieved_relevant / len(relevant_docs)


# ----------------------------
# AVERAGE PRECISION (AP)
# ----------------------------
def average_precision(ranked_docs, relevant_docs):

    if len(relevant_docs) == 0:
        return 0

    score = 0
    hit_count = 0

    for i, (doc_id, _) in enumerate(ranked_docs, start=1):

        if doc_id in relevant_docs:
            hit_count += 1
            score += hit_count / i

    return score / len(relevant_docs)


# ----------------------------
# MEAN AVERAGE PRECISION (MAP)
# ----------------------------
def mean_average_precision(all_results, qrels):

    ap_values = []

    for qid, ranked_docs in all_results.items():

        relevant_docs = qrels.get(qid, set())

        ap = average_precision(ranked_docs, relevant_docs)
        ap_values.append(ap)

    if len(ap_values) == 0:
        return 0

    return sum(ap_values) / len(ap_values)