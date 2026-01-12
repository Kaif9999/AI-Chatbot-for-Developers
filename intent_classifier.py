"""
Advanced Intent Classification System for Developer Chatbot

This module implements a sophisticated intent classification system using
sentence transformers and cosine similarity to understand developer queries
without relying on external LLM APIs.

Features:
- 15+ intent categories for developer queries
- Semantic similarity matching using sentence embeddings
- Multi-intent detection for complex queries
- Confidence scoring and threshold-based classification
- Extensible intent database
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import json
from typing import List, Dict, Tuple, Optional
import re


class IntentClassifier:
    """
    Advanced intent classifier for developer queries using NLP techniques.

    This classifier uses a combination of:
    1. TF-IDF vectorization for initial feature extraction
    2. Cosine similarity for semantic matching
    3. Pattern-based rules for high-confidence classification
    4. Multi-intent support for complex queries
    """

    # Define comprehensive intent categories for developer queries
    INTENTS = {
        'code_debugging': [
            'why is my code not working',
            'debug this error',
            'fix this bug',
            'getting error message',
            'code throws exception',
            'syntax error in code',
            'runtime error troubleshooting',
            'null pointer exception',
            'index out of bounds',
            'memory leak debugging'
        ],
        'code_explanation': [
            'what does this code do',
            'explain this function',
            'how does this work',
            'what is the purpose of',
            'break down this code',
            'understand this snippet',
            'explain the logic',
            'describe this implementation',
            'what is happening here',
            'interpret this code'
        ],
        'best_practices': [
            'best way to implement',
            'coding standards for',
            'is this good practice',
            'code review suggestions',
            'improve code quality',
            'design patterns for',
            'clean code principles',
            'refactoring recommendations',
            'optimization techniques',
            'professional coding approach'
        ],
        'architecture': [
            'system design for',
            'architecture pattern',
            'microservices design',
            'database schema design',
            'scalability architecture',
            'distributed systems design',
            'api design best practices',
            'component architecture',
            'software architecture patterns',
            'infrastructure design'
        ],
        'performance': [
            'optimize code performance',
            'improve execution speed',
            'reduce memory usage',
            'make code faster',
            'performance bottleneck',
            'algorithm optimization',
            'time complexity improvement',
            'space complexity reduction',
            'profiling and optimization',
            'efficiency improvements'
        ],
        'testing': [
            'how to test this code',
            'unit testing strategies',
            'write test cases',
            'testing framework recommendations',
            'integration testing approach',
            'test coverage improvement',
            'mocking and stubbing',
            'test-driven development',
            'automated testing setup',
            'testing best practices'
        ],
        'concept_explanation': [
            'what is object oriented programming',
            'explain recursion',
            'what are design patterns',
            'what is dependency injection',
            'explain inheritance',
            'what is polymorphism',
            'define encapsulation',
            'what are lambdas',
            'explain closures',
            'what is asynchronous programming'
        ],
        'language_comparison': [
            'difference between python and java',
            'compare javascript and typescript',
            'which language is better for',
            'pros and cons of',
            'language comparison',
            'choose between languages',
            'language features comparison',
            'performance comparison',
            'syntax differences',
            'language selection criteria'
        ],
        'library_framework': [
            'which framework should I use',
            'best library for',
            'framework comparison',
            'how to use this library',
            'library recommendations',
            'framework features',
            'popular frameworks for',
            'library documentation',
            'framework setup guide',
            'choosing right framework'
        ],
        'security': [
            'secure coding practices',
            'prevent sql injection',
            'security vulnerabilities',
            'authentication implementation',
            'authorization best practices',
            'encryption methods',
            'secure api design',
            'xss prevention',
            'csrf protection',
            'security audit recommendations'
        ],
        'deployment': [
            'how to deploy application',
            'deployment strategies',
            'continuous integration setup',
            'docker containerization',
            'kubernetes deployment',
            'cloud deployment guide',
            'production environment setup',
            'deployment automation',
            'release management',
            'infrastructure as code'
        ],
        'database': [
            'database query optimization',
            'sql vs nosql',
            'database design',
            'indexing strategies',
            'query performance tuning',
            'database normalization',
            'orm usage',
            'database migration',
            'transaction management',
            'database scaling'
        ],
        'api_development': [
            'rest api design',
            'graphql implementation',
            'api authentication',
            'api versioning',
            'api documentation',
            'api rate limiting',
            'api error handling',
            'api testing',
            'api security',
            'api best practices'
        ],
        'data_structures': [
            'which data structure to use',
            'array vs linked list',
            'hash table implementation',
            'tree traversal algorithms',
            'graph algorithms',
            'stack and queue usage',
            'data structure selection',
            'efficient data organization',
            'complexity analysis',
            'data structure operations'
        ],
        'algorithms': [
            'sorting algorithm comparison',
            'search algorithm implementation',
            'dynamic programming approach',
            'greedy algorithm usage',
            'recursion vs iteration',
            'algorithm optimization',
            'algorithm complexity',
            'algorithmic problem solving',
            'algorithm design patterns',
            'efficient algorithms'
        ],
        'general_inquiry': [
            'tell me about',
            'what is',
            'how do I',
            'general question about programming',
            'learning resources',
            'getting started with',
            'introduction to',
            'overview of',
            'explain in simple terms',
            'beginner guide to'
        ]
    }

    # Pattern-based rules for high-confidence classification
    PATTERN_RULES = {
        'code_debugging': [
            r'\b(error|bug|exception|crash|fail|broken|not working)\b',
            r'\b(debug|fix|troubleshoot|solve)\b',
            r'\b(traceback|stacktrace)\b'
        ],
        'code_explanation': [
            r'\b(explain|describe|what does|how does|understand)\b.*\b(code|function|method|class)\b',
            r'\b(what is.*doing|what happens)\b'
        ],
        'best_practices': [
            r'\b(best practice|best way|recommended|should I|is it good)\b',
            r'\b(clean code|code quality|standards)\b'
        ],
        'performance': [
            r'\b(optimize|faster|slow|performance|speed up|improve efficiency)\b',
            r'\b(memory|cpu|resource usage)\b'
        ],
        'testing': [
            r'\b(test|testing|unit test|integration test|mock)\b',
            r'\b(pytest|junit|jasmine|mocha)\b'
        ],
        'security': [
            r'\b(security|secure|vulnerability|exploit|injection|xss|csrf)\b',
            r'\b(authentication|authorization|encrypt)\b'
        ],
        'deployment': [
            r'\b(deploy|deployment|ci/cd|docker|kubernetes|production)\b',
            r'\b(containerize|orchestration)\b'
        ]
    }

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the intent classifier.

        Args:
            model_path: Path to saved model file (optional)
        """
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 3),
            stop_words='english',
            lowercase=True
        )

        self.intent_vectors = None
        self.intent_labels = []
        self.training_samples = []

        # Build training data from intent definitions
        self._build_training_data()

        # Train the classifier
        self._train()

        # Load saved model if provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def _build_training_data(self):
        """Build training dataset from intent definitions."""
        for intent, examples in self.INTENTS.items():
            for example in examples:
                self.training_samples.append(example)
                self.intent_labels.append(intent)

    def _train(self):
        """Train the intent classifier."""
        # Fit TF-IDF vectorizer on training samples
        self.intent_vectors = self.vectorizer.fit_transform(self.training_samples)

    def classify(self, query: str, threshold: float = 0.3) -> List[Dict[str, any]]:
        """
        Classify user query into one or more intent categories.

        Args:
            query: User's input query
            threshold: Minimum confidence threshold (0-1)

        Returns:
            List of dicts with 'intent', 'confidence', and 'method' keys
        """
        results = []

        # First, try pattern-based classification (high confidence)
        pattern_results = self._classify_by_patterns(query)
        if pattern_results:
            results.extend(pattern_results)

        # Then, try semantic similarity classification
        semantic_results = self._classify_by_similarity(query, threshold)

        # Merge results, avoiding duplicates
        existing_intents = {r['intent'] for r in results}
        for result in semantic_results:
            if result['intent'] not in existing_intents:
                results.append(result)

        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)

        # If no results, return general inquiry
        if not results:
            results.append({
                'intent': 'general_inquiry',
                'confidence': 0.5,
                'method': 'fallback'
            })

        return results

    def _classify_by_patterns(self, query: str) -> List[Dict[str, any]]:
        """
        Classify using regex pattern matching.

        Args:
            query: User's input query

        Returns:
            List of matching intents with high confidence
        """
        results = []
        query_lower = query.lower()

        for intent, patterns in self.PATTERN_RULES.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    results.append({
                        'intent': intent,
                        'confidence': 0.9,
                        'method': 'pattern'
                    })
                    break  # One match per intent is enough

        return results

    def _classify_by_similarity(self, query: str, threshold: float) -> List[Dict[str, any]]:
        """
        Classify using semantic similarity.

        Args:
            query: User's input query
            threshold: Minimum confidence threshold

        Returns:
            List of matching intents with confidence scores
        """
        # Vectorize query
        query_vector = self.vectorizer.transform([query])

        # Calculate cosine similarity with all training samples
        similarities = cosine_similarity(query_vector, self.intent_vectors)[0]

        # Group by intent and take maximum similarity
        intent_scores = {}
        for idx, similarity in enumerate(similarities):
            intent = self.intent_labels[idx]
            if intent not in intent_scores or similarity > intent_scores[intent]:
                intent_scores[intent] = similarity

        # Filter by threshold and prepare results
        results = []
        for intent, score in intent_scores.items():
            if score >= threshold:
                results.append({
                    'intent': intent,
                    'confidence': float(score),
                    'method': 'similarity'
                })

        return results

    def get_primary_intent(self, query: str) -> str:
        """
        Get the primary (highest confidence) intent for a query.

        Args:
            query: User's input query

        Returns:
            Primary intent category name
        """
        results = self.classify(query)
        return results[0]['intent'] if results else 'general_inquiry'

    def add_training_example(self, intent: str, example: str):
        """
        Add a new training example and retrain.

        Args:
            intent: Intent category
            example: Example query text
        """
        if intent not in self.INTENTS:
            self.INTENTS[intent] = []

        self.INTENTS[intent].append(example)
        self.training_samples.append(example)
        self.intent_labels.append(intent)

        # Retrain
        self._train()

    def save_model(self, path: str):
        """
        Save trained model to disk.

        Args:
            path: File path to save model
        """
        model_data = {
            'vectorizer': self.vectorizer,
            'intent_vectors': self.intent_vectors,
            'intent_labels': self.intent_labels,
            'training_samples': self.training_samples,
            'intents': self.INTENTS
        }

        with open(path, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, path: str):
        """
        Load trained model from disk.

        Args:
            path: File path to load model from
        """
        with open(path, 'rb') as f:
            model_data = pickle.load(f)

        self.vectorizer = model_data['vectorizer']
        self.intent_vectors = model_data['intent_vectors']
        self.intent_labels = model_data['intent_labels']
        self.training_samples = model_data['training_samples']
        self.INTENTS = model_data['intents']

    def get_intent_description(self, intent: str) -> str:
        """
        Get human-readable description of an intent.

        Args:
            intent: Intent category name

        Returns:
            Description string
        """
        descriptions = {
            'code_debugging': 'Debugging code issues and fixing errors',
            'code_explanation': 'Understanding and explaining code functionality',
            'best_practices': 'Coding standards and best practices',
            'architecture': 'Software architecture and system design',
            'performance': 'Performance optimization and efficiency',
            'testing': 'Testing strategies and frameworks',
            'concept_explanation': 'Programming concepts and theory',
            'language_comparison': 'Comparing programming languages',
            'library_framework': 'Libraries and frameworks guidance',
            'security': 'Security best practices and vulnerability prevention',
            'deployment': 'Deployment and DevOps practices',
            'database': 'Database design and optimization',
            'api_development': 'API design and development',
            'data_structures': 'Data structures selection and usage',
            'algorithms': 'Algorithm design and optimization',
            'general_inquiry': 'General programming questions'
        }

        return descriptions.get(intent, 'General inquiry')


def demo():
    """Demonstrate the intent classifier with example queries."""
    print("=" * 70)
    print("Advanced Intent Classification System Demo")
    print("=" * 70)

    classifier = IntentClassifier()

    test_queries = [
        "My Python code is throwing a NullPointerException, how do I fix it?",
        "What's the best way to implement authentication in a REST API?",
        "Explain how recursion works in programming",
        "How can I optimize my database queries for better performance?",
        "What are the differences between Python and Java?",
        "How do I write unit tests for this function?",
        "My application is very slow, how can I make it faster?",
        "What's the difference between a list and a tuple in Python?",
        "How do I deploy my application to AWS using Docker?",
        "What are design patterns and when should I use them?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = classifier.classify(query)

        print(f"Detected Intents:")
        for i, result in enumerate(results[:3], 1):  # Show top 3
            intent = result['intent']
            confidence = result['confidence']
            method = result['method']
            description = classifier.get_intent_description(intent)

            print(f"  {i}. {intent} (confidence: {confidence:.2f}, method: {method})")
            print(f"     Description: {description}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo()
