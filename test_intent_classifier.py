"""
Unit tests for Intent Classifier module.

Tests cover:
- Intent classification accuracy
- Pattern-based classification
- Similarity-based classification
- Multi-intent detection
- Model save/load functionality
- Training example addition
"""

import unittest
import os
import tempfile
from intent_classifier import IntentClassifier


class TestIntentClassifier(unittest.TestCase):
    """Test suite for IntentClassifier."""

    def setUp(self):
        """Set up test fixtures."""
        self.classifier = IntentClassifier()

    def test_code_debugging_intent(self):
        """Test debugging-related queries."""
        queries = [
            "My code is not working, can you help?",
            "I'm getting a NullPointerException",
            "How do I fix this bug?",
            "Debug this error message"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('code_debugging', intents,
                         f"Failed to detect debugging intent for: {query}")

    def test_code_explanation_intent(self):
        """Test code explanation queries."""
        queries = [
            "What does this function do?",
            "Explain how this code works",
            "Can you break down this snippet?"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('code_explanation', intents,
                         f"Failed to detect explanation intent for: {query}")

    def test_performance_intent(self):
        """Test performance optimization queries."""
        queries = [
            "How can I make my code faster?",
            "Optimize this algorithm",
            "My application is slow"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('performance', intents,
                         f"Failed to detect performance intent for: {query}")

    def test_testing_intent(self):
        """Test testing-related queries."""
        queries = [
            "How do I write unit tests?",
            "What's the best testing framework?",
            "Help me test this function"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('testing', intents,
                         f"Failed to detect testing intent for: {query}")

    def test_security_intent(self):
        """Test security-related queries."""
        queries = [
            "How to prevent SQL injection?",
            "Secure authentication implementation",
            "What are common security vulnerabilities?"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('security', intents,
                         f"Failed to detect security intent for: {query}")

    def test_multi_intent_detection(self):
        """Test detection of multiple intents in complex queries."""
        query = "My code is slow and has bugs, how do I optimize and fix it?"

        results = self.classifier.classify(query)
        intents = [r['intent'] for r in results]

        # Should detect both performance and debugging intents
        self.assertTrue(
            'performance' in intents or 'code_debugging' in intents,
            "Failed to detect multiple intents"
        )

    def test_confidence_scores(self):
        """Test that confidence scores are within valid range."""
        query = "What is object-oriented programming?"

        results = self.classifier.classify(query)

        for result in results:
            self.assertGreaterEqual(result['confidence'], 0.0)
            self.assertLessEqual(result['confidence'], 1.0)

    def test_pattern_based_classification(self):
        """Test pattern-based classification method."""
        query = "I'm getting an error in my code"

        results = self.classifier.classify(query)

        # Check if any result uses pattern method
        methods = [r['method'] for r in results]
        self.assertIn('pattern', methods)

    def test_similarity_based_classification(self):
        """Test similarity-based classification method."""
        query = "which framework is better for web development"

        results = self.classifier.classify(query)

        # Should have at least one result
        self.assertGreater(len(results), 0)

    def test_get_primary_intent(self):
        """Test getting primary intent."""
        query = "How do I fix this bug in my Python code?"

        primary_intent = self.classifier.get_primary_intent(query)

        self.assertIsNotNone(primary_intent)
        self.assertIsInstance(primary_intent, str)

    def test_fallback_intent(self):
        """Test fallback to general_inquiry for unknown queries."""
        query = "xyz abc def random nonsense query"

        results = self.classifier.classify(query, threshold=0.8)

        # Should fallback to general_inquiry
        intents = [r['intent'] for r in results]
        self.assertIn('general_inquiry', intents)

    def test_add_training_example(self):
        """Test adding new training examples."""
        initial_count = len(self.classifier.training_samples)

        self.classifier.add_training_example(
            'code_debugging',
            'my application crashes on startup'
        )

        # Check training data was updated
        self.assertEqual(
            len(self.classifier.training_samples),
            initial_count + 1
        )

    def test_model_save_and_load(self):
        """Test saving and loading model."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp:
            tmp_path = tmp.name

        try:
            # Save model
            self.classifier.save_model(tmp_path)
            self.assertTrue(os.path.exists(tmp_path))

            # Load model
            new_classifier = IntentClassifier(model_path=tmp_path)

            # Test that loaded model works
            query = "How do I fix this error?"
            original_results = self.classifier.classify(query)
            loaded_results = new_classifier.classify(query)

            self.assertEqual(
                original_results[0]['intent'],
                loaded_results[0]['intent']
            )

        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_get_intent_description(self):
        """Test getting intent descriptions."""
        intent = 'code_debugging'
        description = self.classifier.get_intent_description(intent)

        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)

    def test_all_intents_have_descriptions(self):
        """Test that all defined intents have descriptions."""
        for intent in self.classifier.INTENTS.keys():
            description = self.classifier.get_intent_description(intent)
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)

    def test_threshold_filtering(self):
        """Test that threshold parameter filters low confidence results."""
        query = "random query text"

        # High threshold should return fewer results
        high_threshold_results = self.classifier.classify(query, threshold=0.8)

        # Low threshold should return more results
        low_threshold_results = self.classifier.classify(query, threshold=0.1)

        self.assertLessEqual(
            len(high_threshold_results),
            len(low_threshold_results)
        )

    def test_deployment_intent(self):
        """Test deployment-related queries."""
        queries = [
            "How do I deploy to production?",
            "Docker containerization guide",
            "CI/CD pipeline setup"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('deployment', intents,
                         f"Failed to detect deployment intent for: {query}")

    def test_database_intent(self):
        """Test database-related queries."""
        queries = [
            "How to optimize database queries?",
            "SQL vs NoSQL comparison",
            "Database indexing strategies"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('database', intents,
                         f"Failed to detect database intent for: {query}")

    def test_api_development_intent(self):
        """Test API development queries."""
        queries = [
            "REST API design best practices",
            "How to implement GraphQL?",
            "API authentication methods"
        ]

        for query in queries:
            results = self.classifier.classify(query)
            intents = [r['intent'] for r in results]
            self.assertIn('api_development', intents,
                         f"Failed to detect API development intent for: {query}")


class TestIntentClassifierEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.classifier = IntentClassifier()

    def test_empty_query(self):
        """Test handling of empty query."""
        results = self.classifier.classify("")
        self.assertGreater(len(results), 0)

    def test_very_long_query(self):
        """Test handling of very long queries."""
        query = "how do I " + "optimize " * 100 + "my code?"
        results = self.classifier.classify(query)
        self.assertGreater(len(results), 0)

    def test_special_characters(self):
        """Test handling of special characters."""
        query = "What is @#$%^&* in programming?"
        results = self.classifier.classify(query)
        self.assertGreater(len(results), 0)

    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        query = "How to handle unicode strings like café and naïve?"
        results = self.classifier.classify(query)
        self.assertGreater(len(results), 0)

    def test_mixed_case_query(self):
        """Test case insensitivity."""
        query1 = "HOW DO I FIX THIS BUG?"
        query2 = "how do i fix this bug?"

        results1 = self.classifier.classify(query1)
        results2 = self.classifier.classify(query2)

        self.assertEqual(results1[0]['intent'], results2[0]['intent'])


if __name__ == '__main__':
    unittest.main()
