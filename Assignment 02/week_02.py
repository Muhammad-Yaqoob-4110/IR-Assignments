import math
from collections import Counter
import re
import os

document_titles = {}

# Step 1: Define the documents
# Function to add documents from a directory
def add_documents_from_directory(directory_path):
    """Add all text files from a directory to the documents list."""
    documents = []  # List to hold the contents of documents
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # Process only .txt files
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                title = os.path.splitext(os.path.basename(file_path))[0]  # Extract title from file name
                content = file.read()
                doc_id = hash(file_path)  # Use a hash of the file path as a unique ID
                document_titles[doc_id] = title  # Store the title with doc_id
                documents.append(content)
    return documents

# documents list with the documents loaded from a directory
directory_path = "./Documents_02"
documents = add_documents_from_directory(directory_path)

# Step 2: Preprocess the documents
# Stopword list
# stopwords = set(["the", "is", "in", "and", "to", "a", "of", "on", "with", "it", "for", "as", "by", "an", "can", "from"])

def preprocess(text):
     # Remove punctuation using regex
    text = re.sub(r'[^\w\s]', '', text)  # Retain only words and spaces

    # Lowercase, split into words, and remove stopwords
    words = text.lower().split()
    return words
    # return [word for word in words if word not in stopwords]

# Tokenized documents
tokenized_docs = [preprocess(doc) for doc in documents]

# Step 3: Calculate term frequency (TF)
def compute_tf(doc_tokens):
    tf = Counter(doc_tokens)
    for term in tf:
        tf[term] /= len(doc_tokens)
    return tf

# Step 4: Calculate inverse document frequency (IDF)
def compute_idf(tokenized_docs):
    num_docs = len(tokenized_docs)
    idf = {}
    all_terms = set(term for doc in tokenized_docs for term in doc)
    for term in all_terms:
        doc_count = sum(1 for doc in tokenized_docs if term in doc)
        idf[term] = math.log(num_docs / (doc_count)) # remove 1
    return idf

# Step 5: Compute TF-IDF for each document
def compute_tfidf(tf, idf):
    tfidf = {}
    for term, tf_value in tf.items():
        tfidf[term] = tf_value * idf.get(term, 0)
    return tfidf

# Precompute TF and IDF
idfs = compute_idf(tokenized_docs)
tfidf_docs = [compute_tfidf(compute_tf(doc), idfs) for doc in tokenized_docs]

# print(tfidf_docs)

# Step 6: Rank documents based on a user query
def rank_documents(query):
    query_tokens = preprocess(query)
    query_tf = compute_tf(query_tokens)
    query_tfidf = compute_tfidf(query_tf, idfs)

    # Compute cosine similarity for ranking
    rankings = []
    for i, doc_tfidf in enumerate(tfidf_docs):
        dot_product = sum(query_tfidf.get(term, 0) * doc_tfidf.get(term, 0) for term in query_tfidf)
        query_norm = math.sqrt(sum(value ** 2 for value in query_tfidf.values()))
        doc_norm = math.sqrt(sum(value ** 2 for value in doc_tfidf.values()))
        similarity = dot_product / (query_norm * doc_norm) if query_norm and doc_norm else 0
    
        rankings.append((i, similarity))
    
    # Sort by similarity score in descending order
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

# Step 7: Create a simple CLI
def main():
    print("Welcome to the TF-IDF Search Engine!")
    print("Enter your query to find the most relevant documents.")
    
    while True:
        retried = False
        query = input("\nEnter query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting the search engine. Goodbye!")
            break
        
        rankings = rank_documents(query)
        # print("\nDocument Rankings:")
        for rank, (doc_index, score) in enumerate(rankings, start=1):
            if score > 0:
                retried = True
                # Retrieve the document title using the doc_id (using the index in the rankings list)
                doc_id = list(document_titles.keys())[doc_index]
                document_title = document_titles[doc_id]
                print(f"{rank}. {document_title} (Score: {score :.4f}) & (Relevency: {score * 100:.2f}%)")
                # print(f"   {documents[doc_index][:100]}{'...' if len(documents[doc_index]) > 100 else ''}")
        
        if not retried:
            print("\nSorry, no relevant documents found for your query. Please try again with different terms.")
# Run the CLI
if __name__ == "__main__":
    main()
