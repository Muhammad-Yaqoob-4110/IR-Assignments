import math
import random


class BeliefNetwork:
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
        
        # Network structure with probabilities
        self.network = {
            'variables': {
                'query': {},
                'document_features': {},
                'relevance': {}
            },
            'dependencies': {}
        }
        
        # Initialize network probabilities
        self._initialize_network_probabilities()
    
    def _initialize_network_probabilities(self):
        """
        Initialize probabilities for network variables.
        """
        # Query prior probabilities
        for query in self.queries:
            self.network['variables']['query'][query] = 0.5
        
        # Document feature probabilities
        for doc_idx, doc in enumerate(self.documents):
            # Simple feature extraction (word count)
            word_count = len(doc.split())
            self.network['variables']['document_features'][doc_idx] = {
                'word_count': word_count / max(len(doc.split()) for doc in self.documents)
            }
        
        # Initialize relevance probabilities
        for query in self.queries:
            self.network['variables']['relevance'][query] = {}
            for doc_idx in range(len(self.documents)):
                # Base relevance calculation
                relevance = 1 if (query, doc_idx) in self.relevance_judgments else 0
                self.network['variables']['relevance'][query][doc_idx] = relevance
    
    def compute_bayes_relevance(self, query, document_index):
        """
        Compute document relevance using Bayes' theorem.
        
        Args:
            query (str): Search query
            document_index (int): Document index
        
        Returns:
            float: Probability of document relevance
        """
        # Prior probability of the query
        p_query = self.network['variables']['query'].get(query, 0.5)
        
        # Prior probability of relevance
        p_relevance = self.network['variables']['relevance'][query].get(document_index, 0)
        
        # Compute document features influence
        doc_features = self.network['variables']['document_features'][document_index]
        feature_influence = doc_features['word_count']
        
        # Bayes' theorem computation
        # P(Relevance | Query) = P(Query | Relevance) * P(Relevance) / P(Query)
        
        # Likelihood: P(Query | Relevance)
        # Simplified as a function of feature influence
        p_query_given_relevance = min(feature_influence + p_relevance, 1.0)
        
        # Marginal probability of query (simplified)
        p_query = max(p_query, 0.1)
        
        # Compute final relevance probability
        relevance_probability = (p_query_given_relevance * p_relevance) / p_query
        
        return max(0, min(relevance_probability, 1))
    
    def compute_joint_probability(self, query, document_index):
        """
        Compute joint probability of query and document relevance.
        
        Args:
            query (str): Search query
            document_index (int): Document index
        
        Returns:
            float: Joint probability
        """
        # Relevance probability
        p_relevance = self.compute_bayes_relevance(query, document_index)
        
        # Query probability
        p_query = self.network['variables']['query'].get(query, 0.5)
        
        # Joint probability computation
        joint_prob = p_relevance * p_query
        
        return joint_prob
    
    def evaluate_model(self):
        """
        Evaluate the Belief Network by computing relevance probabilities.
        """
        print("Belief Network Evaluation:")
        for query in self.queries:
            print(f"\nQuery: '{query}'")
            
            # Compute and rank document relevances
            doc_relevances = []
            for doc_idx in range(len(self.documents)):
                # Compute joint probability as relevance metric
                joint_prob = self.compute_joint_probability(query, doc_idx)
                doc_relevances.append((doc_idx, joint_prob))
            
            # Sort and display results
            doc_relevances.sort(key=lambda x: x[1], reverse=True)
            
            for rank, (doc_idx, relevance) in enumerate(doc_relevances, 1):
                print(f"Rank {rank}: Document '{self.documents[doc_idx]}' (Relevance: {relevance:.4f})")

# Main execution
if __name__ == "__main__":
    belief_network = BeliefNetwork()
    belief_network.evaluate_model()