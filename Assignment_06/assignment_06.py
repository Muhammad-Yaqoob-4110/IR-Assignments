import math
import random

class VoiceAssistantNN:
    def __init__(self):
        # Semantic knowledge base for synonyms and related terms
        self.semantic_knowledge = {
            'benefits': ['advantages', 'positive effects', 'gains'],
            'exercise': ['workouts', 'physical activity', 'training', 'fitness'],
            'health': ['wellness', 'well-being', 'fitness', 'vitality'],
            'workout': ['exercise', 'training', 'physical activity'],
            'wellness': ['health', 'well-being', 'fitness']
        }

        # Simulated document corpus (in a real-world scenario, this would be a large database)
        self.document_corpus = [
            "Regular exercise provides numerous benefits for physical and mental health",
            "Workouts can improve cardiovascular wellness and overall fitness",
            "Physical activity is crucial for maintaining good health and preventing diseases",
            "Benefits of consistent training include increased energy and reduced stress",
            "Wellness programs emphasize the importance of regular exercise and healthy lifestyle"
        ]

    def preprocess_text(self, query):
        """
        Preprocess the input text by converting to lowercase 
        and splitting into tokens
        """
        return query.lower().split()

    def semantic_understanding(self, tokens):
        """
        Understand the semantic meaning of tokens by expanding 
        with related terms and synonyms
        """
        expanded_tokens = []
        for token in tokens:
            expanded_tokens.append(token)
            # Add synonyms and related terms from semantic knowledge
            if token in self.semantic_knowledge:
                expanded_tokens.extend(self.semantic_knowledge[token])
        
        return list(set(expanded_tokens))  # Remove duplicates

    def calculate_cosine_similarity(self, query_vector, doc_vector):
        """
        Calculate cosine similarity between query and document vectors
        """
        # Dot product
        dot_product = sum(query_vector[token] * doc_vector.get(token, 0) 
                          for token in query_vector)
        
        # Magnitude calculation
        query_magnitude = math.sqrt(sum(val**2 for val in query_vector.values()))
        doc_magnitude = math.sqrt(sum(val**2 for val in doc_vector.values()))
        
        # Prevent division by zero
        if doc_magnitude == 0 or query_magnitude == 0:
            return 0
        
        return dot_product / (query_magnitude * doc_magnitude)

    def tf_idf_vectorization(self, tokens, corpus):
        """
        Create TF-IDF vector representation for tokens
        """
        # Term Frequency (TF)
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        
        # Inverse Document Frequency (IDF)
        idf = {}
        total_docs = len(corpus)
        
        for token in set(tokens):
            doc_count = sum(1 for doc in corpus if token in doc.lower())
            idf[token] = math.log(total_docs / (doc_count + 1)) + 1
        
        # TF-IDF Calculation
        tfidf_vector = {token: tf.get(token, 0) * idf.get(token, 0) for token in set(tokens)}
        return tfidf_vector

    def search_and_retrieve(self, expanded_query):
        """
        Search and retrieve most relevant documents
        """
        query_vector = self.tf_idf_vectorization(expanded_query, self.document_corpus)
        
        # Rank documents by cosine similarity
        document_scores = []
        for doc in self.document_corpus:
            doc_tokens = self.preprocess_text(doc)
            doc_vector = self.tf_idf_vectorization(doc_tokens, self.document_corpus)
            
            similarity = self.calculate_cosine_similarity(query_vector, doc_vector)
            document_scores.append((doc, similarity))
        
        # Sort documents by relevance
        ranked_documents = sorted(document_scores, key=lambda x: x[1], reverse=True)
        return ranked_documents

    def voice_assistant_pipeline(self, user_query):
        """
        Complete pipeline for processing voice query
        """
        print(f"Voice Query: {user_query}")
        
        # 1. Text Preprocessing
        preprocessed_tokens = self.preprocess_text(user_query)
        print(f"Preprocessed Tokens: {preprocessed_tokens}")
        
        # 2. Semantic Understanding & Query Expansion
        expanded_query = self.semantic_understanding(preprocessed_tokens)
        print(f"Expanded Query: {expanded_query}")
        
        # 3. Search and Retrieve
        results = self.search_and_retrieve(expanded_query)
        
        # 4. Return Top Results
        print("\nRetrieved Articles:")
        for doc, score in results[:2]:  # Top 2 results
            print(f"- {doc} (Relevance: {score:.2f})")
        
        return results

# Example Usage
def main():
    voice_assistant = VoiceAssistantNN()
    
    test_queries = [
        "Find me articles about the benefits of exercise for health",
        "Tell me about workouts and wellness",
        "Physical activity and its advantages"
    ]
    
    for query in test_queries:
        print("\n" + "="*50)
        voice_assistant.voice_assistant_pipeline(query)

if __name__ == "__main__":
    main()