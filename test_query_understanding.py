"""
Unit tests for Query Understanding module.
"""

import unittest
from query_understanding import (
    QueryUnderstandingSystem,
    NamedEntityRecognizer,
    DependencyParser,
    QueryExpander,
    ConversationContext,
    EntityType,
    Entity,
    ParsedQuery
)


class TestNamedEntityRecognizer(unittest.TestCase):
    """Test suite for Named Entity Recognizer."""

    def setUp(self):
        """Set up test fixtures."""
        self.ner = NamedEntityRecognizer()

    def test_extract_language_entities(self):
        """Test extraction of programming languages."""
        text = "I want to learn Python and JavaScript"
        entities = self.ner.extract_entities(text)

        languages = [e for e in entities if e.type == EntityType.LANGUAGE]
        self.assertGreater(len(languages), 0)

    def test_extract_framework_entities(self):
        """Test extraction of frameworks."""
        text = "How do I use React with Django?"
        entities = self.ner.extract_entities(text)

        frameworks = [e for e in entities if e.type == EntityType.FRAMEWORK]
        self.assertGreater(len(frameworks), 0)

    def test_extract_error_entities(self):
        """Test extraction of error types."""
        text = "I'm getting a NullPointerException error"
        entities = self.ner.extract_entities(text)

        errors = [e for e in entities if e.type == EntityType.ERROR]
        self.assertGreater(len(errors), 0)

    def test_extract_concept_entities(self):
        """Test extraction of programming concepts."""
        text = "Explain recursion and inheritance"
        entities = self.ner.extract_entities(text)

        concepts = [e for e in entities if e.type == EntityType.CONCEPT]
        self.assertGreater(len(concepts), 0)

    def test_extract_function_entities(self):
        """Test extraction of function names."""
        text = "Call the calculateSum() function"
        entities = self.ner.extract_entities(text)

        functions = [e for e in entities if e.type == EntityType.FUNCTION]
        self.assertGreater(len(functions), 0)

    def test_extract_class_entities(self):
        """Test extraction of class names."""
        text = "Create a new MyClass instance"
        entities = self.ner.extract_entities(text)

        classes = [e for e in entities if e.type == EntityType.CLASS]
        self.assertGreater(len(classes), 0)

    def test_entity_confidence_scores(self):
        """Test that entities have confidence scores."""
        text = "Python programming"
        entities = self.ner.extract_entities(text)

        for entity in entities:
            self.assertGreaterEqual(entity.confidence, 0)
            self.assertLessEqual(entity.confidence, 1)

    def test_entity_positions(self):
        """Test that entities have correct positions."""
        text = "python java"
        entities = self.ner.extract_entities(text)

        if entities:
            for entity in entities:
                self.assertGreaterEqual(entity.start, 0)
                self.assertLessEqual(entity.end, len(text))
                self.assertLess(entity.start, entity.end)

    def test_duplicate_removal(self):
        """Test that duplicate entities are removed."""
        text = "python python python"
        entities = self.ner.extract_entities(text)

        # Should have only one "python" entity
        python_entities = [e for e in entities if e.text == 'python']
        self.assertLessEqual(len(python_entities), 1)


class TestDependencyParser(unittest.TestCase):
    """Test suite for Dependency Parser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = DependencyParser()

    def test_parse_action_object(self):
        """Test parsing action-object relations."""
        text = "fix bug"
        dependencies = self.parser.parse(text, [])

        self.assertGreater(len(dependencies), 0)

    def test_parse_with_entities(self):
        """Test parsing with entity information."""
        text = "optimize code performance"
        entities = []
        dependencies = self.parser.parse(text, entities)

        self.assertIsInstance(dependencies, list)

    def test_verb_recognition(self):
        """Test that verbs are recognized."""
        self.assertIn('fix', self.parser.verb_patterns)
        self.assertIn('implement', self.parser.verb_patterns)
        self.assertIn('optimize', self.parser.verb_patterns)

    def test_dependency_structure(self):
        """Test dependency relation structure."""
        text = "create function"
        dependencies = self.parser.parse(text, [])

        if dependencies:
            dep = dependencies[0]
            self.assertIsInstance(dep.head, str)
            self.assertIsInstance(dep.relation, str)
            self.assertIsInstance(dep.dependent, str)


class TestQueryExpander(unittest.TestCase):
    """Test suite for Query Expander."""

    def setUp(self):
        """Set up test fixtures."""
        self.expander = QueryExpander()

    def test_expand_with_synonyms(self):
        """Test query expansion with synonyms."""
        query = "fix bug"
        expanded = self.expander.expand(query)

        # Should contain original words and synonyms
        self.assertIn('fix', expanded.lower())

    def test_synonyms_exist(self):
        """Test that synonym dictionary is populated."""
        self.assertGreater(len(self.expander.synonyms), 0)

    def test_expansion_contains_originals(self):
        """Test that expansion includes original terms."""
        query = "optimize code"
        expanded = self.expander.expand(query)

        for word in query.split():
            self.assertIn(word, expanded.lower())


class TestConversationContext(unittest.TestCase):
    """Test suite for Conversation Context."""

    def setUp(self):
        """Set up test fixtures."""
        self.context = ConversationContext(max_history=3)

    def test_add_query(self):
        """Test adding queries to context."""
        parsed_query = ParsedQuery(
            original_query="test query",
            tokens=["test", "query"],
            entities=[],
            dependencies=[],
            intent="test",
            expanded_query="test query",
            key_concepts=[]
        )

        self.context.add_query(parsed_query)
        self.assertEqual(len(self.context.history), 1)

    def test_history_limit(self):
        """Test that history is limited."""
        for i in range(5):
            parsed_query = ParsedQuery(
                original_query=f"query {i}",
                tokens=[],
                entities=[],
                dependencies=[],
                intent="test",
                expanded_query="",
                key_concepts=[]
            )
            self.context.add_query(parsed_query)

        # Should keep only max_history queries
        self.assertLessEqual(len(self.context.history), self.context.max_history)

    def test_track_entities(self):
        """Test tracking mentioned entities."""
        entity = Entity(
            text="python",
            type=EntityType.LANGUAGE,
            start=0,
            end=6,
            confidence=0.9
        )

        parsed_query = ParsedQuery(
            original_query="test",
            tokens=[],
            entities=[entity],
            dependencies=[],
            intent="test",
            expanded_query="",
            key_concepts=[]
        )

        self.context.add_query(parsed_query)

        # Should track the entity
        self.assertIn('python', self.context.entities_mentioned[EntityType.LANGUAGE])

    def test_resolve_references(self):
        """Test pronoun reference resolution."""
        # Add a query with entity
        entity = Entity(
            text="python",
            type=EntityType.LANGUAGE,
            start=0,
            end=6,
            confidence=0.9
        )

        parsed_query = ParsedQuery(
            original_query="What is Python?",
            tokens=[],
            entities=[entity],
            dependencies=[],
            intent="test",
            expanded_query="",
            key_concepts=[]
        )

        self.context.add_query(parsed_query)

        # Resolve reference in next query
        resolved = self.context.resolve_references("How do I use it?")

        # "it" should be replaced
        self.assertNotEqual(resolved, "How do I use it?")


class TestQueryUnderstandingSystem(unittest.TestCase):
    """Test suite for complete Query Understanding System."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = QueryUnderstandingSystem()

    def test_understand_basic_query(self):
        """Test understanding a basic query."""
        query = "How do I use Python?"
        parsed = self.system.understand(query, use_context=False)

        self.assertIsInstance(parsed, ParsedQuery)
        self.assertEqual(parsed.original_query, query)

    def test_entity_extraction(self):
        """Test that entities are extracted."""
        query = "Fix NullPointerException in Java"
        parsed = self.system.understand(query, use_context=False)

        self.assertGreater(len(parsed.entities), 0)

    def test_intent_inference_debug(self):
        """Test intent inference for debugging queries."""
        query = "How do I fix this error?"
        parsed = self.system.understand(query, use_context=False)

        # Should infer some intent
        self.assertIsNotNone(parsed.intent)

    def test_intent_inference_explanation(self):
        """Test intent inference for explanation queries."""
        query = "What is recursion?"
        parsed = self.system.understand(query, use_context=False)

        self.assertEqual(parsed.intent, 'explanation')

    def test_intent_inference_implementation(self):
        """Test intent inference for implementation queries."""
        query = "How do I implement authentication?"
        parsed = self.system.understand(query, use_context=False)

        self.assertEqual(parsed.intent, 'implementation')

    def test_intent_inference_optimization(self):
        """Test intent inference for optimization queries."""
        query = "How can I make my code faster?"
        parsed = self.system.understand(query, use_context=False)

        self.assertEqual(parsed.intent, 'optimization')

    def test_intent_inference_comparison(self):
        """Test intent inference for comparison queries."""
        query = "What's the difference between list and tuple?"
        parsed = self.system.understand(query, use_context=False)

        self.assertEqual(parsed.intent, 'comparison')

    def test_query_expansion(self):
        """Test that queries are expanded."""
        query = "fix bug"
        parsed = self.system.understand(query, use_context=False)

        # Expanded query should be different
        self.assertNotEqual(parsed.expanded_query, query)

    def test_key_concept_extraction(self):
        """Test key concept extraction."""
        query = "Implement recursion algorithm"
        parsed = self.system.understand(query, use_context=False)

        # Should extract some concepts
        self.assertIsInstance(parsed.key_concepts, list)

    def test_format_analysis(self):
        """Test formatting of analysis."""
        query = "How do I use Python?"
        parsed = self.system.understand(query, use_context=False)

        formatted = self.system.format_analysis(parsed)

        self.assertIn(query, formatted)
        self.assertIn("QUERY ANALYSIS", formatted)

    def test_context_usage(self):
        """Test using conversation context."""
        # First query
        parsed1 = self.system.understand("What is Python?", use_context=True)

        # Second query (should use context)
        parsed2 = self.system.understand("How do I use it?", use_context=True)

        # Context should have both queries
        self.assertEqual(len(self.system.context.history), 2)

    def test_multiple_entities_extraction(self):
        """Test extraction of multiple entities."""
        query = "Use Python with Django and React"
        parsed = self.system.understand(query, use_context=False)

        # Should extract multiple entities
        self.assertGreater(len(parsed.entities), 2)

    def test_empty_query(self):
        """Test handling of empty query."""
        parsed = self.system.understand("", use_context=False)

        self.assertIsInstance(parsed, ParsedQuery)

    def test_complex_query(self):
        """Test handling of complex multi-part query."""
        query = "How do I fix a NullPointerException in my Java Spring application when using React frontend?"
        parsed = self.system.understand(query, use_context=False)

        # Should extract multiple entities and understand intent
        self.assertGreater(len(parsed.entities), 2)
        self.assertIsNotNone(parsed.intent)


if __name__ == '__main__':
    unittest.main()
