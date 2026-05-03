from src.parser import parse_documents, parse_queries, load_qrels
import nltk
nltk.download('stopwords')
docs = parse_documents("data/cran.all.1400.xml")
queries = parse_queries("data/cran.qry.xml")
qrels = load_qrels("data/cranqrel.trec.txt")

print("Docs:", len(docs))
print("Queries:", len(queries))
print("Qrels:", len(qrels))

# sanity check samples
print("\nSample Doc:", list(docs.items())[0])
print("\nSample Query:", list(queries.items())[0])

from src.preprocess import preprocess

sample = "Experimental investigation of the aerodynamics of a wing in a slipstream."

print(preprocess(sample))