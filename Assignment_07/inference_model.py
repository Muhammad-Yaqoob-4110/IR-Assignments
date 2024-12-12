import math
import random


class InterferenceModel:
    def __init__(self):
        # Sample dataset of documents
        self.documents = [
            "Machine learning is a subset of artificial intelligence",
            "Information retrieval focuses on finding relevant documents",
            "Probabilistic models help in ranking document relevance",
            "Neural networks are powerful for pattern recognition",
            "Data science combines statistics and computer science"
        ]
        
        # Sample queries
        self.queries = [
            "machine learning",
            "information retrieval",
            "data science"
        ]
        
        # Simulated relevance judgments (binary)
        self.relevance_judgments = {
            ("machine learning", 0): 1,  # First doc is relevant
            ("machine learning", 2): 0,  # Third doc is not relevant
            ("information retrieval", 1): 1,
            ("data science", 4): 1
        }
        
        # Probabilities for the interference model
        self.query_probabilities = {}
        self.document_probabilities = {}
        
        # Compute initial probabilities
        self._compute_initial_probabilities()
    
    def _compute_initial_probabilities(self):
        """
        Compute initial probabilities for queries and documents
        based on the dataset and relevance judgments.
        """
        # Compute query probabilities
        for query in self.queries:
            relevant_docs = sum(
                1 for (q, doc_idx) in self.relevance_judgments 
                if q == query and self.relevance_judgments[(q, doc_idx)] == 1
            )
            self.query_probabilities[query] = relevant_docs / len(self.documents)
        
        # Compute document probabilities
        for i, doc in enumerate(self.documents):
            relevant_count = sum(
                1 for (query, doc_idx) in self.relevance_judgments 
                if doc_idx == i and self.relevance_judgments.get((query, doc_idx), 0) == 1
            )
            self.document_probabilities[i] = relevant_count / len(self.queries)
    
    def compute_relevance(self, query, document_index):
        """
        Compute relevance probability using the Interference Model.
        
        Args:
            query (str): The search query
            document_index (int): Index of the document in the document list
        
        Returns:
            float: Probability of relevance
        """
        # Check if we have a direct relevance judgment
        if (query, document_index) in self.relevance_judgments:
            return self.relevance_judgments[(query, document_index)]
        
        # Compute relevance based on query and document probabilities
        query_prob = self.query_probabilities.get(query, 0.1)
        doc_prob = self.document_probabilities.get(document_index, 0.1)
        
        # Interference model relevance calculation
        # Uses a probabilistic interference formula
        relevance_prob = (query_prob * doc_prob) / (query_prob + doc_prob - query_prob * doc_prob)
        
        return relevance_prob
    
    def retrieve_documents(self, query):
        """
        Retrieve and rank documents for a given query based on relevance.
        
        Args:
            query (str): The search query
        
        Returns:
            list: Ranked list of document indices with their relevance scores
        """
        # Compute relevance for all documents
        doc_relevances = [
            (idx, self.compute_relevance(query, idx)) 
            for idx in range(len(self.documents))
        ]
        
        # Sort documents by relevance in descending order
        return sorted(doc_relevances, key=lambda x: x[1], reverse=True)
    
    def evaluate_model(self):
        """
        Evaluate the Interference Model by running queries and displaying results.
        """
        print("Interference Model Evaluation:")
        for query in self.queries:
            print(f"\nQuery: '{query}'")
            ranked_docs = self.retrieve_documents(query)
            
            for rank, (doc_idx, relevance) in enumerate(ranked_docs, 1):
                print(f"Rank {rank}: Document '{self.documents[doc_idx]}' (Relevance: {relevance:.4f})")

# Main execution
if __name__ == "__main__":
    interference_model = InterferenceModel()
    interference_model.evaluate_model()