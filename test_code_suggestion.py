"""
Unit tests for Code Suggestion Engine module.
"""

import unittest
from code_suggestion import (
    CodeSuggestionEngine,
    NGramModel,
    CodePatternDatabase,
    CodeSuggestion
)


class TestNGramModel(unittest.TestCase):
    """Test suite for N-gram model."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = NGramModel(n=3)

    def test_tokenize(self):
        """Test code tokenization."""
        code = "def func(x): return x"
        tokens = self.model.tokenize(code)

        self.assertIn('def', tokens)
        self.assertIn('func', tokens)
        self.assertIn('(', tokens)
        self.assertIn('x', tokens)

    def test_train_builds_ngrams(self):
        """Test that training builds n-grams."""
        samples = ["def func ( ) : pass"]
        self.model.train(samples)

        self.assertGreater(len(self.model.ngrams), 0)
        self.assertGreater(len(self.model.vocabulary), 0)

    def test_predict_next(self):
        """Test next token prediction."""
        samples = [
            "if condition : return True",
            "if condition : return False",
        ]
        self.model.train(samples)

        predictions = self.model.predict_next(['if', 'condition'])

        self.assertGreater(len(predictions), 0)
        self.assertIsInstance(predictions[0], tuple)
        self.assertEqual(len(predictions[0]), 2)  # (token, probability)

    def test_probability_sum(self):
        """Test that probabilities are valid."""
        samples = ["a b c", "a b d", "a b e"]
        self.model.train(samples)

        predictions = self.model.predict_next(['a', 'b'])

        for token, prob in predictions:
            self.assertGreaterEqual(prob, 0)
            self.assertLessEqual(prob, 1)


class TestCodePatternDatabase(unittest.TestCase):
    """Test suite for code pattern database."""

    def setUp(self):
        """Set up test fixtures."""
        self.db = CodePatternDatabase()

    def test_database_initialized(self):
        """Test that database is initialized with patterns."""
        self.assertIsInstance(self.db.patterns, dict)
        self.assertGreater(len(self.db.patterns), 0)

    def test_python_patterns_exist(self):
        """Test that Python patterns exist."""
        self.assertIn('python', self.db.patterns)
        python_patterns = self.db.patterns['python']
        self.assertGreater(len(python_patterns), 0)

    def test_javascript_patterns_exist(self):
        """Test that JavaScript patterns exist."""
        self.assertIn('javascript', self.db.patterns)
        js_patterns = self.db.patterns['javascript']
        self.assertGreater(len(js_patterns), 0)

    def test_get_patterns_python_file(self):
        """Test getting patterns for Python file operations."""
        patterns = self.db.get_patterns('python', ['open', 'file'])
        self.assertGreater(len(patterns), 0)

    def test_get_patterns_javascript_async(self):
        """Test getting patterns for JavaScript async operations."""
        patterns = self.db.get_patterns('javascript', ['fetch', 'api'])
        self.assertGreater(len(patterns), 0)

    def test_get_patterns_no_match(self):
        """Test getting patterns with no matches."""
        patterns = self.db.get_patterns('python', ['nonexistent', 'xyz'])
        # May or may not have patterns
        self.assertIsInstance(patterns, list)

    def test_pattern_structure(self):
        """Test that patterns have required fields."""
        patterns = self.db.get_patterns('python', ['open', 'file'])

        if patterns:
            pattern = patterns[0]
            self.assertIn('trigger', pattern)
            self.assertIn('suggestion', pattern)
            self.assertIn('description', pattern)
            self.assertIn('category', pattern)


class TestCodeSuggestionEngine(unittest.TestCase):
    """Test suite for code suggestion engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = CodeSuggestionEngine()

    def test_engine_initialized(self):
        """Test that engine is initialized."""
        self.assertIsInstance(self.engine.ngram_models, dict)
        self.assertIsInstance(self.engine.pattern_db, CodePatternDatabase)

    def test_python_model_trained(self):
        """Test that Python model is trained."""
        self.assertIn('python', self.engine.ngram_models)
        model = self.engine.ngram_models['python']
        self.assertGreater(len(model.ngrams), 0)

    def test_javascript_model_trained(self):
        """Test that JavaScript model is trained."""
        self.assertIn('javascript', self.engine.ngram_models)
        model = self.engine.ngram_models['javascript']
        self.assertGreater(len(model.ngrams), 0)

    def test_suggest_python_file_operations(self):
        """Test suggesting Python file operations."""
        suggestions = self.engine.suggest(
            "I need to open a file",
            language='python'
        )

        self.assertGreater(len(suggestions), 0)
        self.assertIsInstance(suggestions[0], CodeSuggestion)

    def test_suggest_javascript_fetch(self):
        """Test suggesting JavaScript fetch operations."""
        suggestions = self.engine.suggest(
            "fetch data from API",
            language='javascript'
        )

        self.assertGreater(len(suggestions), 0)

    def test_suggestion_has_required_fields(self):
        """Test that suggestions have required fields."""
        suggestions = self.engine.suggest(
            "filter a list",
            language='python'
        )

        if suggestions:
            suggestion = suggestions[0]
            self.assertIsInstance(suggestion.code, str)
            self.assertIsInstance(suggestion.description, str)
            self.assertIsInstance(suggestion.confidence, float)
            self.assertIsInstance(suggestion.category, str)
            self.assertIsInstance(suggestion.language, str)

    def test_confidence_range(self):
        """Test that confidence scores are in valid range."""
        suggestions = self.engine.suggest(
            "filter array",
            language='javascript'
        )

        for suggestion in suggestions:
            self.assertGreaterEqual(suggestion.confidence, 0)
            self.assertLessEqual(suggestion.confidence, 1)

    def test_max_suggestions_limit(self):
        """Test that max_suggestions parameter works."""
        suggestions = self.engine.suggest(
            "list operations",
            language='python',
            max_suggestions=2
        )

        self.assertLessEqual(len(suggestions), 2)

    def test_suggest_completion_python_if(self):
        """Test code completion for Python if statement."""
        completions = self.engine.suggest_completion('if ', 'python')
        self.assertGreater(len(completions), 0)
        self.assertTrue(any('if' in c for c in completions))

    def test_suggest_completion_python_for(self):
        """Test code completion for Python for loop."""
        completions = self.engine.suggest_completion('for ', 'python')
        self.assertGreater(len(completions), 0)
        self.assertTrue(any('for' in c for c in completions))

    def test_suggest_completion_javascript_function(self):
        """Test code completion for JavaScript function."""
        completions = self.engine.suggest_completion('function ', 'javascript')
        self.assertGreater(len(completions), 0)
        self.assertTrue(any('function' in c for c in completions))

    def test_suggestions_sorted_by_confidence(self):
        """Test that suggestions are sorted by confidence."""
        suggestions = self.engine.suggest(
            "handle errors",
            language='python'
        )

        if len(suggestions) > 1:
            for i in range(len(suggestions) - 1):
                self.assertGreaterEqual(
                    suggestions[i].confidence,
                    suggestions[i + 1].confidence
                )

    def test_pattern_suggestions_have_code(self):
        """Test that pattern suggestions include code."""
        suggestions = self.engine.suggest(
            "open file read",
            language='python'
        )

        pattern_suggestions = [s for s in suggestions if s.category != 'completion']
        if pattern_suggestions:
            self.assertGreater(len(pattern_suggestions[0].code), 0)

    def test_multiple_keywords_matching(self):
        """Test suggestions with multiple matching keywords."""
        suggestions = self.engine.suggest(
            "filter and map list",
            language='python'
        )

        # Should get suggestions for both filter and map
        self.assertGreater(len(suggestions), 0)

    def test_unsupported_language(self):
        """Test handling of unsupported language."""
        suggestions = self.engine.suggest(
            "some code",
            language='unsupported'
        )

        # Should return empty or handle gracefully
        self.assertIsInstance(suggestions, list)


class TestCodeSuggestionDataclass(unittest.TestCase):
    """Test CodeSuggestion dataclass."""

    def test_create_suggestion(self):
        """Test creating a CodeSuggestion."""
        suggestion = CodeSuggestion(
            code="test code",
            description="test description",
            confidence=0.9,
            category="test",
            language="python"
        )

        self.assertEqual(suggestion.code, "test code")
        self.assertEqual(suggestion.description, "test description")
        self.assertEqual(suggestion.confidence, 0.9)
        self.assertEqual(suggestion.category, "test")
        self.assertEqual(suggestion.language, "python")


if __name__ == '__main__':
    unittest.main()
