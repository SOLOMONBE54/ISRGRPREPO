import pickle

from src.parser import parse_queries, load_qrels
from src.preprocess import preprocess
from src.ranker import run_ranking, save_results
from src.evaluator import precision_at_k, recall, mean_average_precision


# =========================================================
# CONFIG
# =========================================================

DEBUG = True          # True = fast testing, False = full run
USE_STEMMING = True    # switch experiment here
MODEL = "bm25"
RUN_NAME = "BM25_STEM"


# =========================================================
# FILE PATHS
# =========================================================

INDEX_FILE = "results/indexing/index_stem.pkl" if USE_STEMMING else "results/indexing/index_no_stem.pkl"
LENGTH_FILE = "results/indexing/doc_lengths_stem.pkl" if USE_STEMMING else "results/indexing/doc_lengths_no_stem.pkl"
OUTPUT_FILE = f"results/{MODEL}_{'stem' if USE_STEMMING else 'no_stem'}.txt"


# =========================================================
# LOAD INDEX
# =========================================================

print("Loading index...")

with open(INDEX_FILE, "rb") as f:
    index = pickle.load(f)

with open(LENGTH_FILE, "rb") as f:
    doc_lengths = pickle.load(f)

print("Index loaded.")


# =========================================================
# LOAD QUERIES
# =========================================================

print("Loading queries...")

queries = parse_queries("data/cran.qry.xml")

print(f"{len(queries)} queries loaded.")


# =========================================================
# LOAD QRELS
# =========================================================

print("Loading qrels...")

qrels = load_qrels("data/cranqrel.trec.txt")

print(f"{len(qrels)} qrels loaded.")


# =========================================================
# DEBUG MODE (FAST TESTING ONLY)
# =========================================================

if DEBUG:

    print("\n===== DEBUG MODE =====")

    sample_query = next(iter(queries.values()))
    tokens = preprocess(sample_query, use_stemming=USE_STEMMING)

    print("Sample query tokens:", tokens)

    for t in tokens[:5]:
        print(t, "->", t in index)

    print("\nSkipping ranking and evaluation.")
    exit()


# =========================================================
# RUN RANKING
# =========================================================

print("\nRunning ranking...")

results = run_ranking(
    queries=queries,
    index=index,
    doc_lengths=doc_lengths,
    model=MODEL,
    use_stemming=USE_STEMMING,
    top_k=100,
    run_name=RUN_NAME
)

save_results(results, OUTPUT_FILE, run_name=RUN_NAME)

print(f"Ranking complete. Results saved in {OUTPUT_FILE}")


# =========================================================
# EVALUATION
# =========================================================

print("\nRunning evaluation...")

total_p10 = 0
total_recall = 0

num_queries = len(results)

for qid, ranked_docs in results.items():

    relevant_docs = qrels.get(qid, set())

    total_p10 += precision_at_k(ranked_docs, relevant_docs, k=10)
    total_recall += recall(ranked_docs, relevant_docs)

map_score = mean_average_precision(results, qrels)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n===== EVALUATION RESULTS =====")
print(f"MAP: {map_score:.4f}")
print(f"Precision@10: {total_p10 / num_queries:.4f}")
print(f"Recall: {total_recall / num_queries:.4f}")
print("==============================")
print("Sample queries:", list(queries.items())[:3])
print("Sample qrels:", list(qrels.items())[:3])
print("Index size:", len(index))