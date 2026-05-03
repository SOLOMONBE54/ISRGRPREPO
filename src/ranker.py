import os

from src.models import rank_documents


# ----------------------------
# TREC OUTPUT WRITER
# ----------------------------
def write_results(results, file_path, run_name):
    """
    Writes ranked results in TREC format
    """

    with open(file_path, "w") as f:

        for qid, docs in results.items():

            for rank, (doc_id, score) in enumerate(docs, start=1):

                f.write(f"{qid} Q0 {doc_id} {rank} {score} {run_name}\n")


# ----------------------------
# RUN RANKING OVER ALL QUERIES
# ----------------------------
def run_ranking(
    queries,
    index,
    doc_lengths,
    model="bm25",
    use_stemming=True,
    top_k=100,
    run_name="RUN"
):

    results = {}

    total_queries = len(queries)

    for i, (qid, query_text) in enumerate(queries.items(), start=1):

        print(f"Processing query {i}/{total_queries}")

        ranked_docs = rank_documents(
            query_text,
            index,
            doc_lengths,
            model=model,
            use_stemming=use_stemming,
            top_k=top_k
        )

        results[qid] = ranked_docs

    return results


# ----------------------------
# SAVE FINAL OUTPUT
# ----------------------------
def save_results(results, output_path, run_name):

    with open(output_path, "w") as f:

        for qid, ranked_docs in results.items():

            for rank, (doc_id, score) in enumerate(ranked_docs, start=1):

                f.write(f"{qid} Q0 {doc_id} {rank} {score} {run_name}\n")