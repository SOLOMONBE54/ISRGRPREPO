import pickle

from src.parser import parse_queries, load_qrels
from src.ranker import run_ranking, save_results
from src.evaluator import precision_at_k, recall, mean_average_precision


# =========================================================
# EXPERIMENT CONFIGURATION
# =========================================================

EXPERIMENTS = [
    {"model": "bm25", "stem": True,  "name": "BM25 Stem"},
    {"model": "bm25", "stem": False, "name": "BM25 No Stem"},
    {"model": "tfidf", "stem": True,  "name": "TF-IDF Stem"},
    {"model": "tfidf", "stem": False, "name": "TF-IDF No Stem"},
]


# =========================================================
# LOAD DATA ONCE
# =========================================================

print("Loading queries...")
queries = parse_queries("data/cran.qry.xml")

print("Loading qrels...")
qrels = load_qrels("data/cranqrel.trec.txt")


# =========================================================
# RESULTS STORAGE
# =========================================================

results_table = []


# =========================================================
# RUN EXPERIMENTS
# =========================================================

for exp in EXPERIMENTS:

    print("\n===================================")
    print(f"Running: {exp['name']}")
    print("===================================")

    stem = exp["stem"]

    # ----------------------------
    # LOAD INDEX
    # ----------------------------
    index_path = f"results/indexing/index_{'stem' if stem else 'no_stem'}.pkl"
    length_path = f"results/indexing/doc_lengths_{'stem' if stem else 'no_stem'}.pkl"

    with open(index_path, "rb") as f:
        index = pickle.load(f)

    with open(length_path, "rb") as f:
        doc_lengths = pickle.load(f)


    # ----------------------------
    # RUN RANKING
    # ----------------------------
    results = run_ranking(
        queries=queries,
        index=index,
        doc_lengths=doc_lengths,
        model=exp["model"],
        use_stemming=stem,
        top_k=100,
        run_name=exp["name"]
    )

    # save results file
    output_file = f"results/{exp['name'].replace(' ', '_')}.txt"
    save_results(results, output_file, run_name=exp["name"])


    # ----------------------------
    # EVALUATION
    # ----------------------------
    total_p10 = 0
    total_recall = 0

    num_queries = len(results)

    for qid, ranked_docs in results.items():
        relevant_docs = qrels.get(qid, set())

        total_p10 += precision_at_k(ranked_docs, relevant_docs, k=10)
        total_recall += recall(ranked_docs, relevant_docs)

    map_score = mean_average_precision(results, qrels)


    # store results
    results_table.append([
        exp["name"],
        map_score,
        total_p10 / num_queries,
        total_recall / num_queries
    ])


# =========================================================
# FINAL MARKDOWN TABLE OUTPUT
# =========================================================

print("\n\n# ===== FINAL RESULTS =====\n")

print("| Model | MAP | Precision@10 | Recall |")
print("|------|-----|--------------|--------|")

for row in results_table:
    model, map_score, p10, rec = row

    print(
        f"| {model} | {map_score:.4f} | {p10:.4f} | {rec:.4f} |"
    )