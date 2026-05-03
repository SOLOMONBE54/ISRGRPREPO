import os
import pickle
from collections import defaultdict, Counter

from src.preprocess import preprocess


# ----------------------------
# PATH SETUP
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "results", "indexing")

os.makedirs(RESULTS_DIR, exist_ok=True)


# ----------------------------
# DOCUMENT PARSER (Cranfield format)
# ----------------------------
def parse_documents(file_path):
    docs = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:

        doc = None
        capture_text = False
        capture_title = False

        for line in f:
            line = line.strip()

            if line == "<doc>":
                doc = {"docno": None, "title": [], "text": []}
                continue

            if line == "</doc>":
                if doc and doc["docno"]:
                    docs.append(doc)
                doc = None
                continue

            if doc is not None:

                if "<docno>" in line:
                    doc["docno"] = line.replace("<docno>", "").replace("</docno>", "").strip()

                elif "<title>" in line:
                    capture_title = True

                elif "</title>" in line:
                    capture_title = False

                elif "<text>" in line:
                    capture_text = True

                elif "</text>" in line:
                    capture_text = False

                else:
                    clean = line

                    if capture_title:
                        doc["title"].append(clean)
                    elif capture_text:
                        doc["text"].append(clean)

    return docs


# ----------------------------
# INDEX BUILDER
# ----------------------------
def build_index(docs, use_stemming=True):
    """
    Builds inverted index + document lengths
    """

    inverted_index = defaultdict(dict)
    doc_lengths = {}

    for doc in docs:

        docno = doc["docno"]

        full_text = " ".join(doc["title"] + doc["text"])

        # ALL preprocessing handled externally
        tokens = preprocess(full_text, use_stemming=use_stemming)

        doc_lengths[docno] = len(tokens)

        term_freq = Counter(tokens)

        for term, freq in term_freq.items():
            inverted_index[term][docno] = freq

    return inverted_index, doc_lengths


# ----------------------------
# SAVE HELPER
# ----------------------------
def save(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


# ----------------------------
# MAIN PIPELINE
# ----------------------------
if __name__ == "__main__":

    all_docs = []

    # load all files in data folder
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)

        if os.path.isfile(file_path):
            all_docs.extend(parse_documents(file_path))

    print(f"Loaded {len(all_docs)} documents")


    # ----------------------------
    # NO STEM INDEX
    # ----------------------------
    print("Building NO-STEM index...")

    index_no_stem, len_no_stem = build_index(all_docs, use_stemming=False)

    save(index_no_stem, os.path.join(RESULTS_DIR, "index_no_stem.pkl"))
    save(len_no_stem, os.path.join(RESULTS_DIR, "doc_lengths_no_stem.pkl"))


    # ----------------------------
    # STEM INDEX
    # ----------------------------
    print("Building STEM index...")

    index_stem, len_stem = build_index(all_docs, use_stemming=True)

    save(index_stem, os.path.join(RESULTS_DIR, "index_stem.pkl"))
    save(len_stem, os.path.join(RESULTS_DIR, "doc_lengths_stem.pkl"))


    print("Indexing complete. Files saved in results/indexing/")