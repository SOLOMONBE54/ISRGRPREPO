# src/parser.py

import xml.etree.ElementTree as ET


# -----------------------------
# 1. DOCUMENTS PARSER
# -----------------------------
def parse_documents(file_path):
    """
    Parses Cranfield document collection (cran.all.1400.xml)

    Returns:
        dict: {doc_id: document_text}
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    docs = {}

    for doc in root.findall("doc"):
        doc_id_elem = doc.find("docno")
        text_elem = doc.find("text")

        if doc_id_elem is None or text_elem is None:
            continue

        doc_id = doc_id_elem.text.strip()
        text = text_elem.text.strip() if text_elem.text else ""

        docs[doc_id] = text

    return docs


# -----------------------------
# 2. QUERY PARSER
# -----------------------------
def parse_queries(file_path):
    """
    Parses Cranfield queries (cran.qry.xml)

    Returns:
        dict: {query_id: query_text}
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    queries = {}

    # Cranfield queries usually use <top> blocks
    for top in root.findall("top"):
        qid_elem = top.find("num")
        text_elem = top.find("title")

        if qid_elem is None or text_elem is None:
            continue

        # Extract query id (clean numbers)
        qid = qid_elem.text.strip().split()[-1]
        text = text_elem.text.strip()

        queries[qid] = text

    return queries


# -----------------------------
# 3. RELEVANCE JUDGMENTS (QRELS)
# -----------------------------
def load_qrels(file_path):
    qrels = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:
            parts = line.strip().split()

            if len(parts) < 4:
                continue

            qid = str(parts[0]).strip()

            # ❗ IMPORTANT: skip the middle "0" column
            doc_id = str(parts[2]).strip()
            relevance = int(parts[3])

            if relevance > 0:
                if qid not in qrels:
                    qrels[qid] = set()
                qrels[qid].add(doc_id)

    return qrels