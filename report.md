# 📄 ISR Project — Cranfield Information Retrieval System

## 📌 Overview

This project implements an **Information Retrieval (IR) system from scratch** using the Cranfield 1400 dataset.  
It includes document parsing, indexing, ranking, and evaluation using standard IR metrics.

The system compares multiple retrieval models:
- BM25
- TF-IDF  
with both:
- Stemming
- No stemming

---

## 📂 Dataset

The system uses the Cranfield dataset:

- `cran.all.1400.xml` → Document collection (1400 aerospace abstracts)
- `cran.qry.xml` → Query set
- `cranqrel.trec.txt` → Relevance judgments (qrels)

Each document contains:
- Document ID
- Title
- Text
- Metadata

---

## 🏗️ System Architecture

### 1. Parsing Module
- Extracts documents and queries from XML files

### 2. Preprocessing Module
- Tokenization
- Lowercasing
- Optional stemming (Porter Stemmer)

### 3. Indexing Module
- Builds inverted index
- Stores document lengths
- Creates:
  - Stemmed index
  - Non-stemmed index

### 4. Ranking Module
- BM25
- TF-IDF

### 5. Evaluation Module
- MAP (Mean Average Precision)
- Precision@10
- Recall

---

## 🔍 Indexing Strategy

### ✔ No-Stemming Index
- Original word forms preserved
- Larger vocabulary

### ✔ Stemming Index
- Uses Porter Stemmer
- Reduces words to root forms

---

## 📊 Ranking Models

### BM25
- Uses term frequency saturation
- Includes document length normalization
- Strong baseline for IR systems

### TF-IDF
- Based on term importance across corpus
- Simpler but less robust than BM25

---

## 📈 Experimental Setup

| Model | Stemming |
|------|----------|
| BM25 | Yes |
| BM25 | No |
| TF-IDF | Yes |
| TF-IDF | No |

All experiments use identical queries and qrels for fair comparison.

---

## 📊 Results

| Model | MAP | Precision@10 | Recall |
|------|-----|--------------|--------|
| BM25 Stem | 0.0051 | 0.0067 | 0.0510 |
| BM25 No Stem | 0.0053 | 0.0084 | 0.0497 |
| TF-IDF Stem | 0.0047 | 0.0071 | 0.0621 |
| TF-IDF No Stem | 0.0045 | 0.0062 | 0.0543 |

---

## 📌 Discussion

- BM25 performs slightly better than TF-IDF overall.
- Stemming has minimal impact on MAP.
- Recall is higher than precision, meaning relevant documents are retrieved but not ranked highly.
- Overall MAP is low, indicating the system requires further tuning.

---

## ⚠️ Challenges

- XML parsing inconsistencies in Cranfield dataset
- Maintaining consistent preprocessing across modules
- Debugging query-index mismatches
- Ensuring correct qrels evaluation format
- Ranking optimization issues

---

## 🎯 Conclusion

This project demonstrates a complete IR pipeline built from scratch, including:

- Document processing
- Index construction
- Ranking models (BM25, TF-IDF)
- Evaluation using standard metrics

### Key findings:
- BM25 outperforms TF-IDF slightly
- Stemming has limited effect without tuning
- System is functional but requires optimization for higher retrieval quality

---

## 🚀 Future Improvements

- Stopword removal tuning
- BM25 parameter optimization (k1, b)
- Query expansion techniques
- Improved preprocessing alignment
- Performance tuning for MAP improvement

---

## 👥 Group Members

| Name | Student ID |
|------|-----------|
| Rahwa Gebretsadkan | UGR/8772/17 |
| Saron Alemu | UGR/7220/17 |
| Solomon Berhanu | UGR/3414/17 |
| Surra Bulto Negera | UGR/0185/17 |
| Tesnim Mohammedamin | UGR/6367/17 |
| Tobias Abnet | UGR/9274/17 |

---

## 📁 Project Structure

```text
src/
data/
results/
main.py