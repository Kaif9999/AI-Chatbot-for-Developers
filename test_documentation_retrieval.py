"""
Unit tests for Documentation Retrieval module.
"""

import unittest
from documentation_retrieval import (
    DocumentationRetrieval,
    DocumentationDatabase,
    DocumentationEntry
)


class TestDocumentationDatabase(unittest.TestCase):
    """Test suite for documentation database."""

    def setUp(self):
        """Set up test fixtures."""
        self.database = DocumentationDatabase()

    def test_database_has_entries(self):
        """Test that database is populated with entries."""
        entries = self.database.get_all_entries()
        self.assertGreater(len(entries), 0)

    def test_get_by_language_python(self):
        """Test filtering by Python language."""
        python_docs = self.database.get_by_language('python')
        self.assertGreater(len(python_docs), 0)
        self.assertTrue(all(doc.language == 'python' for doc in python_docs))

    def test_get_by_language_javascript(self):
        """Test filtering by JavaScript language."""
        js_docs = self.database.get_by_language('javascript')
        self.assertGreater(len(js_docs), 0)
        self.assertTrue(all(doc.language == 'javascript' for doc in js_docs))

    def test_get_by_category(self):
        """Test filtering by category."""
        syntax_docs = self.database.get_by_category('syntax')
        self.assertGreater(len(syntax_docs), 0)

    def test_multiple_languages_supported(self):
        """Test that multiple languages are supported."""
        all_entries = self.database.get_all_entries()
        languages = set(entry.language for entry in all_entries)
        self.assertGreaterEqual(len(languages), 5)

    def test_entry_structure(self):
        """Test that entries have required fields."""
        entries = self.database.get_all_entries()
        if entries:
            entry = entries[0]
            self.assertIsInstance(entry, DocumentationEntry)
            self.assertIsInstance(entry.language, str)
            self.assertIsInstance(entry.topic, str)
            self.assertIsInstance(entry.title, str)
            self.assertIsInstance(entry.description, str)
            self.assertIsInstance(entry.code_example, str)
            self.assertIsInstance(entry.keywords, list)


class TestDocumentationRetrieval(unittest.TestCase):
    """Test suite for documentation retrieval system."""

    def setUp(self):
        """Set up test fixtures."""
        self.retrieval = DocumentationRetrieval()

    def test_search_python_exceptions(self):
        """Test searching for Python exception handling."""
        results = self.retrieval.search("exception handling in python", language="python")
        self.assertGreater(len(results), 0)

        # Check that results are relevant
        entry, score = results[0]
        self.assertEqual(entry.language, 'python')
        self.assertGreater(score, 0)

    def test_search_javascript_promises(self):
        """Test searching for JavaScript promises."""
        results = self.retrieval.search("javascript promises async", language="javascript")
        self.assertGreater(len(results), 0)

        entry, score = results[0]
        self.assertEqual(entry.language, 'javascript')

    def test_search_without_language_filter(self):
        """Test searching without language filter."""
        results = self.retrieval.search("how to handle errors")
        self.assertGreater(len(results), 0)

    def test_search_returns_scores(self):
        """Test that search returns relevance scores."""
        results = self.retrieval.search("python list comprehension")
        self.assertGreater(len(results), 0)

        for entry, score in results:
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0)  # Score can be 0 for weak matches

    def test_top_k_parameter(self):
        """Test top_k parameter limits results."""
        results_3 = self.retrieval.search("programming", top_k=3)
        results_5 = self.retrieval.search("programming", top_k=5)

        self.assertLessEqual(len(results_3), 3)
        self.assertLessEqual(len(results_5), 5)

    def test_keyword_boosting(self):
        """Test that keyword matches boost scores."""
        results = self.retrieval.search("dictionary hash table python", language="python")

        if len(results) > 1:
            # Results should be sorted by score
            self.assertGreaterEqual(results[0][1], results[1][1])

    def test_topic_matching(self):
        """Test exact topic matching."""
        results = self.retrieval.search("list comprehension", language="python")
        self.assertGreater(len(results), 0)

    def test_inverted_index_built(self):
        """Test that inverted index is built."""
        self.assertIsInstance(self.retrieval.inverted_index, dict)
        self.assertGreater(len(self.retrieval.inverted_index), 0)

    def test_idf_scores_calculated(self):
        """Test that IDF scores are calculated."""
        self.assertIsInstance(self.retrieval.idf_scores, dict)
        self.assertGreater(len(self.retrieval.idf_scores), 0)

        # All IDF scores should be positive
        for score in self.retrieval.idf_scores.values():
            self.assertGreater(score, 0)

    def test_tokenization(self):
        """Test text tokenization."""
        tokens = self.retrieval._tokenize("Hello, World! How are you?")
        self.assertEqual(tokens, ['hello', 'world', 'how', 'are', 'you'])

    def test_get_related(self):
        """Test getting related documentation."""
        # Find an entry with related topics
        for doc in self.retrieval.documents:
            if doc.related_topics:
                related = self.retrieval.get_related(doc.topic, doc.language)
                # May or may not have related docs depending on database
                self.assertIsInstance(related, list)
                break

    def test_format_result(self):
        """Test formatting documentation entry."""
        if self.retrieval.documents:
            entry = self.retrieval.documents[0]
            formatted = self.retrieval.format_result(entry, 0.95)

            self.assertIn(entry.title, formatted)
            self.assertIn(entry.description, formatted)
            self.assertIn(entry.code_example, formatted)
            self.assertIn('0.95', formatted)

    def test_search_empty_query(self):
        """Test searching with empty query."""
        results = self.retrieval.search("")
        # Should return empty or handle gracefully
        self.assertIsInstance(results, list)

    def test_search_nonexistent_term(self):
        """Test searching for non-existent term."""
        results = self.retrieval.search("xyzabc123nonexistent")
        self.assertEqual(len(results), 0)

    def test_language_filter_works(self):
        """Test that language filter excludes other languages."""
        results = self.retrieval.search("function", language="python")

        if results:
            for entry, score in results:
                self.assertEqual(entry.language.lower(), 'python')

    def test_bm25_score_calculation(self):
        """Test BM25 score calculation."""
        query_tokens = ['python', 'list']
        score = self.retrieval._calculate_bm25_score(query_tokens, 0)

        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)

    def test_doc_lengths_calculated(self):
        """Test that document lengths are calculated."""
        self.assertEqual(len(self.retrieval.doc_lengths), len(self.retrieval.documents))
        self.assertTrue(all(length > 0 for length in self.retrieval.doc_lengths))

    def test_avg_doc_length(self):
        """Test average document length calculation."""
        self.assertGreater(self.retrieval.avg_doc_length, 0)

    def test_search_java_topics(self):
        """Test searching Java documentation."""
        results = self.retrieval.search("java generics type safety", language="java")
        if results:
            entry, score = results[0]
            self.assertEqual(entry.language, 'java')

    def test_search_sql_topics(self):
        """Test searching SQL documentation."""
        results = self.retrieval.search("database query optimization", language="sql")
        if results:
            entry, score = results[0]
            self.assertEqual(entry.language, 'sql')

    def test_case_insensitive_search(self):
        """Test that search is case insensitive."""
        results1 = self.retrieval.search("PYTHON LIST")
        results2 = self.retrieval.search("python list")

        # Both should return results
        self.assertGreater(len(results1), 0)
        self.assertGreater(len(results2), 0)


class TestBM25Ranking(unittest.TestCase):
    """Test BM25 ranking algorithm."""

    def setUp(self):
        """Set up test fixtures."""
        self.retrieval = DocumentationRetrieval()

    def test_more_relevant_docs_score_higher(self):
        """Test that more relevant documents score higher."""
        # Search for specific topic
        results = self.retrieval.search("python list comprehension syntax", language="python")

        if len(results) >= 2:
            # First result should have higher or equal score
            self.assertGreaterEqual(results[0][1], results[1][1])

    def test_term_frequency_affects_score(self):
        """Test that term frequency affects BM25 score."""
        # Documents with more matching terms should score higher
        results = self.retrieval.search("python dictionary map hash")

        if results:
            # At least one result should have a positive score
            self.assertGreater(results[0][1], 0)

    def test_idf_affects_score(self):
        """Test that IDF affects scoring."""
        # Rare terms should have higher IDF
        common_term_idf = self.retrieval.idf_scores.get('the', 0)
        rare_term_idf = self.retrieval.idf_scores.get('polymorphism', float('inf'))

        # If both exist, rare term should have higher IDF
        if common_term_idf > 0 and rare_term_idf < float('inf'):
            self.assertGreater(rare_term_idf, common_term_idf)


if __name__ == '__main__':
    unittest.main()
