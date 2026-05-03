# Information Storage and Retrieval (ISR) Project Report

---

## Title Page

**Project Title:** Cranfield Information Retrieval System Using Multiple Ranking Models  
**Course:** Information Storage and Retrieval  
**Dataset:** Cranfield 1400 XML Collection  
**Group Name:** *[Your Group Name]*  
**Instructor:** *[Instructor Name]*  
**Date:** *[Submission Date]*  

---

# 1. Introduction

This project implements an Information Retrieval (IR) system using the Cranfield 1400 dataset.  
The objective is to build a complete retrieval pipeline including parsing, indexing, ranking, and evaluation.

The system is implemented from scratch in Python without using external IR engines such as Elasticsearch, to demonstrate core IR concepts.

---

# 2. Dataset Description

The Cranfield dataset consists of:

- **cran.all.1400.xml** → Document collection (1400 aerospace abstracts)
- **cran.qry.xml** → Query set
- **cranqrel.trec.txt** → Relevance judgments (qrels)

Each document contains:
- Document ID
- Title
- Text body
- Author and bibliographic information

---

# 3. System Architecture

The system is structured into modular components:

## 3.1 Parsing Module
- Extracts documents and queries from XML files

## 3.2 Preprocessing Module
- Tokenization
- Lowercasing
- Stemming (optional)

## 3.3 Indexing Module
- Builds inverted index
- Stores document lengths
- Generates two indexes:
  - Stemmed
  - Non-stemmed

## 3.4 Ranking Module
- BM25
- TF-IDF

## 3.5 Evaluation Module
- MAP (Mean Average Precision)
- Precision@10
- Recall

---

# 4. Indexing Approach

Two separate indexes were built:

## 4.1 No-Stemming Index
- Keeps original word forms
- Higher vocabulary size

## 4.2 Stemming Index
- Uses Porter Stemmer
- Reduces words to root forms

Each index stores:
- Term → Document frequency mapping
- Document lengths

---

# 5. Ranking Models

## 5.1 BM25 Model

BM25 is used as the primary ranking function:

- Term frequency saturation
- Inverse document frequency
- Document length normalization

## 5.2 TF-IDF Model

TF-IDF ranks documents based on:

- Term Frequency (TF)
- Inverse Document Frequency (IDF)

---

# 6. Evaluation Metrics

## 6.1 Mean Average Precision (MAP)
Measures overall ranking effectiveness across queries.

## 6.2 Precision@10
Measures relevance in top 10 retrieved results.

## 6.3 Recall
Measures coverage of relevant documents retrieved.

---

# 7. Experimental Setup

The following configurations were tested:

| Model | Stemming |
|------|----------|
| BM25 | Yes |
| BM25 | No |
| TF-IDF | Yes |
| TF-IDF | No |

All experiments use the same query set and relevance judgments for fairness.

---

# 8. Results

| Model | MAP | Precision@10 | Recall |
|------|-----|--------------|--------|
| BM25 Stem | X.XXX | X.XXX | X.XXX |
| BM25 No Stem | X.XXX | X.XXX | X.XXX |
| TF-IDF Stem | X.XXX | X.XXX | X.XXX |
| TF-IDF No Stem | X.XXX | X.XXX | X.XXX |

---

## 8.1 Discussion

- BM25 is expected to outperform TF-IDF due to better ranking normalization.
- Stemming improves recall by reducing vocabulary sparsity.
- Precision@10 indicates top-result quality.

---

# 9. Challenges Encountered

- XML parsing inconsistencies
- Index-query mismatch due to stemming
- Evaluation errors from qrels formatting
- Debugging ranking logic
- Ensuring consistent preprocessing across pipeline

---

# 10. Conclusion

This project implements a full IR system including indexing, ranking, and evaluation.

The results show the importance of:
- proper preprocessing
- consistent indexing strategy
- robust ranking models

BM25 is expected to provide the strongest performance overall.

---

# 11. Group Members

| Name | Student ID | Role |
|------|-----------|------|
| Member 1 Name | ID | Indexing & Parsing |
| Member 2 Name | ID | Ranking Models |
| Member 3 Name | ID | Evaluation |
| Member 4 Name | ID | Documentation |

---

# 12. Appendix

## Project Structure
