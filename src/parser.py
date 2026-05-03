# src/parser.py

import re


# -----------------------------
# DOCUMENT PARSER
# -----------------------------
def parse_documents(file_path):
    """
    Parses Cranfield document collection (semi-structured XML)
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    docs = {}

    # Extract each full <doc>...</doc> block
    doc_blocks = re.findall(r"<doc>(.*?)</doc>", content, re.DOTALL | re.IGNORECASE)

    for block in doc_blocks:

        # doc id
        docno_match = re.search(r"<docno>\s*(.*?)\s*</docno>", block, re.IGNORECASE)
        if not docno_match:
            continue

        doc_id = docno_match.group(1).strip()

        # title (optional, but useful later)
        title_match = re.search(r"<title>\s*(.*?)\s*</title>", block, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""

        # text (main field)
        text_match = re.search(r"<text>\s*(.*?)\s*</text>", block, re.IGNORECASE | re.DOTALL)
        text = text_match.group(1).strip() if text_match else ""

        # combine title + text (VERY IMPORTANT for IR quality)
        full_text = (title + " " + text).strip()

        docs[doc_id] = full_text

    return docs


# -----------------------------
# QUERY PARSER
# -----------------------------
def parse_queries(file_path):
    """
    Parses Cranfield queries (cran.qry.xml)
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    queries = {}

    # each query is inside <top> ... </top>
    query_blocks = re.findall(r"<top>(.*?)</top>", content, re.DOTALL | re.IGNORECASE)

    for block in query_blocks:

        # query id
        id_match = re.search(r"<num>.*?(\d+)\s*</num>", block, re.IGNORECASE)
        if not id_match:
            continue

        qid = id_match.group(1).strip()

        # query text (title field)
        title_match = re.search(r"<title>\s*(.*?)\s*</title>", block, re.IGNORECASE | re.DOTALL)
        if not title_match:
            continue

        text = title_match.group(1).strip()

        queries[qid] = text

    return queries


# -----------------------------
# QRELS PARSER
# -----------------------------
def load_qrels(file_path):
    """
    Parses TREC qrels format (cranqrel.trec.txt)
    """

    qrels = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 4:
                continue

            qid, _, doc_id, relevance = parts

            if relevance == "1":
                if qid not in qrels:
                    qrels[qid] = set()

                qrels[qid].add(doc_id)

    return qrels