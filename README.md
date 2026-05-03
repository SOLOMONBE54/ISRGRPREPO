Group members


1.	Rahwa Gebretsadkan 	UGR/8772/17
2.	Saron Alemu 	UGR/7220/17
3.	Solomon Berhanu	UGR/3414/17
4.	Surra Bulto Negera	UGR/0185/17
5.	Tesnim Mohammedamin 	UGR/6367/17
6.	Tobias Abnet	UGR/9274/17

# 📚 Information Storage & Retrieval (ISR) Project

## 🔍 Cranfield Dataset IR System (BM25 + TF-IDF)

This project implements a full **Information Retrieval system from scratch** using the Cranfield dataset. It supports multiple ranking models, stemming experiments, and evaluation metrics.

---

# 📁 Project Structure

```
ISRProject/
│
├── main.py                      # Entry point (runs full system)
├── README.md                    # Setup instructions
├── report.md                    # Project report
│
├── data/                        # Dataset files
│   ├── cran.all.1400.xml
│   ├── cran.qry.xml
│   └── cranqrel.trec.txt
│
├── results/                     # Output files
│   ├── bm25_results.txt
│   ├── bm25_stem_results.txt
│   ├── BM25_No_Stem.txt
│   ├── TF-IDF_Stem.txt
│   ├── TF-IDF_No_Stem.txt
│   └── indexing/
│       ├── index_stem.pkl
│       ├── index_no_stem.pkl
│       ├── doc_lengths_stem.pkl
│       └── doc_lengths_no_stem.pkl
│
└── src/                         # Core system modules
    ├── parser.py               # Query & qrels parsing
    ├── preprocess.py           # Tokenization + stemming
    ├── indexer.py              # Builds inverted index
    ├── ranker.py               # BM25 + TF-IDF ranking
    ├── evaluator.py            # MAP, Precision@10, Recall
    ├── experiment_runner.py    # Runs all experiments
    ├── models.py               # Ranking models (if used)
```

---

# ⚙️ Requirements

Install dependencies:

```bash
pip install nltk
```

Download required NLTK data (first run only):

```python
import nltk
nltk.download('stopwords')
```

---

# 🚀 How to Run the Project

## 1️⃣ Build the Index

```bash
python -m src.indexer
```

This generates inverted indexes and document statistics in:

```
results/indexing/
```

---

## 2️⃣ Run Full System (Single Execution)

```bash
python main.py
```

This will:

* Load index
* Load queries & qrels
* Run BM25 ranking
* Evaluate system
* Print results

---

## 3️⃣ Run Full Experiments

```bash
python -m src.experiment_runner
```

This compares:

| Model  | Stemming |
| ------ | -------- |
| BM25   | Yes      |
| BM25   | No       |
| TF-IDF | Yes      |
| TF-IDF | No       |

---

# 📊 Output Format

Results are stored in `results/` in TREC format:

```
query_id Q0 document_id rank score run_name
```

Example:

```
1 Q0 123 1 15.32 BM25_Stem
```

---

# 📈 Evaluation Metrics

## MAP (Mean Average Precision)

Measures overall ranking quality.

## Precision@10

Measures relevance of top 10 results.

## Recall

Measures coverage of relevant documents.

---

# 🧠 Ranking Models

## BM25 (Primary Model)

* TF saturation
* IDF weighting
* document length normalization

## TF-IDF

* classic term weighting model

---

# 🧹 Preprocessing

* Lowercasing
* Tokenization
* Stopword removal
* Optional stemming


---

# 📌 Example Results

| Model          | MAP    | Precision@10 | Recall |
| -------------- | ------ | ------------ | ------ |
| BM25 Stem      | 0.0054 | 0.0105       | 0.0775 |
| BM25 No Stem   | 0.0059 | 0.0099       | 0.0828 |
| TF-IDF Stem    | 0.0050 | 0.0105       | 0.0942 |
| TF-IDF No Stem | 0.0043 | 0.0092       | 0.0785 |

---

# ⚠️ Limitations

* Low MAP due to basic preprocessing
* No query expansion
* No learning-to-rank

---

# 🚀 Improvements

* Query expansion (PRF)
* Better BM25 tuning (k1, b)
* Embedding-based retrieval
* Hybrid ranking models

---

# 👥 Group Members

| Name                | Student ID  |
| ------------------- | ----------- |
| Rahwa Gebretsadkan  | UGR/8772/17 |
| Saron Alemu         | UGR/7220/17 |
| Solomon Berhanu     | UGR/3414/17 |
| Surra Bulto Negera  | UGR/0185/17 |
| Tesnim Mohammedamin | UGR/6367/17 |
| Tobias Abnet        | UGR/9274/17 |

---

# 🏁 Conclusion

This project demonstrates a full IR pipeline including:

* parsing
* indexing
* ranking
* evaluation
* experimentation

Built entirely from scratch for educational purposes.

