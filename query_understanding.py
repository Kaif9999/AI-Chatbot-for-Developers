"""
Advanced Query Understanding System with NER and Dependency Parsing

This module provides sophisticated query understanding capabilities using
Named Entity Recognition (NER), dependency parsing, and semantic analysis
to comprehend complex technical questions without external APIs.

Features:
- Named Entity Recognition for programming entities
- Dependency parsing for syntactic structure
- Multi-turn conversation context
- Query expansion and reformulation
- Entity extraction (functions, classes, variables, languages)
- Intent refinement based on entities
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
from enum import Enum


class EntityType(Enum):
    """Types of programming entities."""
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    DATATYPE = "datatype"
    CONCEPT = "concept"
    ERROR = "error"
    TOOL = "tool"


@dataclass
class Entity:
    """Represents an extracted entity."""
    text: str
    type: EntityType
    start: int
    end: int
    confidence: float


@dataclass
class DependencyRelation:
    """Represents a dependency relation between tokens."""
    head: str
    relation: str
    dependent: str


@dataclass
class ParsedQuery:
    """Represents a fully parsed query."""
    original_query: str
    tokens: List[str]
    entities: List[Entity]
    dependencies: List[DependencyRelation]
    intent: Optional[str]
    expanded_query: str
    key_concepts: List[str]


class NamedEntityRecognizer:
    """
    Custom NER system for programming domain.

    Recognizes programming languages, frameworks, concepts, and entities.
    """

    def __init__(self):
        """Initialize NER system."""
        self.entity_patterns = self._build_entity_patterns()

    def _build_entity_patterns(self) -> Dict[EntityType, List[Tuple[str, float]]]:
        """
        Build patterns for entity recognition.

        Returns:
            Dictionary mapping entity types to (pattern, confidence) tuples
        """
        patterns = {
            EntityType.LANGUAGE: [
                (r'\b(python|java|javascript|typescript|c\+\+|cpp|c#|csharp|ruby|go|golang|rust|swift|kotlin|php|scala|r|matlab|perl|lua|dart|elixir|haskell|julia)\b', 0.95),
                (r'\b(js|ts|py)\b', 0.80),
            ],
            EntityType.FRAMEWORK: [
                (r'\b(react|angular|vue|django|flask|spring|express|fastapi|rails|laravel|nextjs|gatsby|svelte|ember|backbone|meteor|nest|nuxt)\b', 0.90),
                (r'\b(tensorflow|pytorch|keras|scikit-learn|pandas|numpy|matplotlib)\b', 0.90),
                (r'\b(jquery|bootstrap|tailwind|material-ui|ant-design)\b', 0.85),
            ],
            EntityType.DATATYPE: [
                (r'\b(string|integer|int|float|double|boolean|bool|array|list|dict|dictionary|map|set|tuple|object|class|struct|enum|interface)\b', 0.85),
            ],
            EntityType.CONCEPT: [
                (r'\b(recursion|iteration|loop|inheritance|polymorphism|encapsulation|abstraction|interface|async|synchronous|callback|promise|closure|decorator|generator|coroutine)\b', 0.85),
                (r'\b(oop|object[- ]oriented|functional programming|procedural|declarative|imperative)\b', 0.85),
                (r'\b(algorithm|data structure|design pattern|architecture|api|rest|graphql|websocket)\b', 0.85),
            ],
            EntityType.ERROR: [
                (r'\b(nullpointerexception|nullreferenceexception|indexoutofbounds|stackoverflow|syntaxerror|typeerror|nameerror|valueerror|keyerror|attributeerror|importerror)\b', 0.90),
                (r'\b(exception|error|bug|issue|crash|failure)\b', 0.70),
            ],
            EntityType.TOOL: [
                (r'\b(git|docker|kubernetes|jenkins|travis|circleci|gitlab|github|bitbucket|npm|pip|maven|gradle|webpack|babel|eslint|prettier)\b', 0.90),
            ],
        }

        return patterns

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from text.

        Args:
            text: Input text

        Returns:
            List of Entity objects
        """
        entities = []
        text_lower = text.lower()

        for entity_type, patterns in self.entity_patterns.items():
            for pattern, confidence in patterns:
                for match in re.finditer(pattern, text_lower):
                    entity = Entity(
                        text=match.group(),
                        type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=confidence
                    )
                    entities.append(entity)

        # Extract function-like patterns (camelCase, snake_case with parentheses)
        function_pattern = r'\b([a-z_][a-z0-9_]*|[a-z][a-zA-Z0-9]*)\s*\('
        for match in re.finditer(function_pattern, text):
            func_name = match.group(1)
            entity = Entity(
                text=func_name,
                type=EntityType.FUNCTION,
                start=match.start(),
                end=match.start() + len(func_name),
                confidence=0.80
            )
            entities.append(entity)

        # Extract class-like patterns (PascalCase)
        class_pattern = r'\b([A-Z][a-zA-Z0-9]*)\b'
        for match in re.finditer(class_pattern, text):
            class_name = match.group()
            # Filter out common words
            if class_name not in ['I', 'A', 'The', 'This', 'That', 'What', 'How', 'Why', 'When']:
                entity = Entity(
                    text=class_name,
                    type=EntityType.CLASS,
                    start=match.start(),
                    end=match.end(),
                    confidence=0.70
                )
                entities.append(entity)

        # Remove duplicates (keep highest confidence)
        unique_entities = {}
        for entity in entities:
            key = (entity.text, entity.type)
            if key not in unique_entities or entity.confidence > unique_entities[key].confidence:
                unique_entities[key] = entity

        return list(unique_entities.values())


class DependencyParser:
    """
    Simple rule-based dependency parser for technical queries.

    Identifies key relationships like:
    - Action-Object (e.g., "fix bug")
    - Modifier-Noun (e.g., "memory leak")
    - Subject-Verb-Object
    """

    def __init__(self):
        """Initialize dependency parser."""
        self.verb_patterns = self._build_verb_patterns()

    def _build_verb_patterns(self) -> Set[str]:
        """Build set of common verbs in technical queries."""
        return {
            'fix', 'debug', 'solve', 'resolve', 'implement', 'create', 'build',
            'write', 'code', 'develop', 'optimize', 'improve', 'refactor',
            'test', 'deploy', 'install', 'configure', 'setup', 'use', 'handle',
            'manage', 'process', 'parse', 'validate', 'sanitize', 'convert',
            'transform', 'map', 'filter', 'reduce', 'sort', 'search', 'find',
            'get', 'set', 'update', 'delete', 'remove', 'add', 'insert'
        }

    def parse(self, text: str, entities: List[Entity]) -> List[DependencyRelation]:
        """
        Parse dependencies in text.

        Args:
            text: Input text
            entities: Extracted entities

        Returns:
            List of DependencyRelation objects
        """
        dependencies = []
        words = text.lower().split()

        # Find verb-object relationships
        for i, word in enumerate(words):
            if word in self.verb_patterns:
                # Look for objects after verb
                if i + 1 < len(words):
                    dependencies.append(DependencyRelation(
                        head=word,
                        relation='action-object',
                        dependent=words[i + 1]
                    ))

                # Look for subjects before verb
                if i > 0:
                    dependencies.append(DependencyRelation(
                        head=words[i - 1],
                        relation='subject-action',
                        dependent=word
                    ))

        # Find modifier-noun relationships (adjective + noun)
        modifiers = {'memory', 'syntax', 'type', 'null', 'index', 'key', 'value', 'stack', 'heap'}
        for i, word in enumerate(words):
            if word in modifiers and i + 1 < len(words):
                dependencies.append(DependencyRelation(
                    head=word,
                    relation='modifier-noun',
                    dependent=words[i + 1]
                ))

        return dependencies


class QueryExpander:
    """
    Expands queries with synonyms and related terms for better matching.
    """

    def __init__(self):
        """Initialize query expander."""
        self.synonyms = self._build_synonyms()

    def _build_synonyms(self) -> Dict[str, List[str]]:
        """
        Build synonym dictionary.

        Returns:
            Dictionary mapping terms to synonyms
        """
        return {
            'fix': ['debug', 'resolve', 'solve', 'repair'],
            'bug': ['error', 'issue', 'problem', 'defect'],
            'function': ['method', 'procedure', 'routine'],
            'variable': ['var', 'identifier', 'name'],
            'optimize': ['improve', 'enhance', 'speed up', 'make faster'],
            'slow': ['sluggish', 'inefficient', 'poor performance'],
            'crash': ['fail', 'break', 'hang', 'freeze'],
            'install': ['setup', 'configure', 'deploy'],
            'use': ['utilize', 'employ', 'apply'],
            'create': ['make', 'build', 'generate', 'construct'],
            'delete': ['remove', 'erase', 'drop'],
            'update': ['modify', 'change', 'alter', 'edit'],
        }

    def expand(self, query: str) -> str:
        """
        Expand query with synonyms.

        Args:
            query: Original query

        Returns:
            Expanded query with synonyms
        """
        words = query.lower().split()
        expanded_terms = set(words)

        for word in words:
            if word in self.synonyms:
                expanded_terms.update(self.synonyms[word])

        return ' '.join(expanded_terms)


class ConversationContext:
    """
    Manages multi-turn conversation context.
    """

    def __init__(self, max_history: int = 5):
        """
        Initialize conversation context.

        Args:
            max_history: Maximum number of turns to remember
        """
        self.max_history = max_history
        self.history: List[ParsedQuery] = []
        self.entities_mentioned: Dict[EntityType, Set[str]] = defaultdict(set)

    def add_query(self, parsed_query: ParsedQuery):
        """
        Add a parsed query to context.

        Args:
            parsed_query: Parsed query object
        """
        self.history.append(parsed_query)

        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Track mentioned entities
        for entity in parsed_query.entities:
            self.entities_mentioned[entity.type].add(entity.text)

    def get_context_entities(self) -> List[Entity]:
        """
        Get all entities mentioned in conversation context.

        Returns:
            List of entities from context
        """
        entities = []
        for entity_type, entity_texts in self.entities_mentioned.items():
            for text in entity_texts:
                entities.append(Entity(
                    text=text,
                    type=entity_type,
                    start=0,
                    end=len(text),
                    confidence=0.8
                ))
        return entities

    def resolve_references(self, query: str) -> str:
        """
        Resolve pronoun references using context.

        Args:
            query: Current query

        Returns:
            Query with resolved references
        """
        # Simple pronoun resolution
        pronouns = ['it', 'this', 'that', 'these', 'those']

        for pronoun in pronouns:
            if pronoun in query.lower():
                # Get most recent entity
                if self.history:
                    last_entities = self.history[-1].entities
                    if last_entities:
                        # Replace pronoun with most recent entity
                        query = re.sub(
                            r'\b' + pronoun + r'\b',
                            last_entities[0].text,
                            query,
                            flags=re.IGNORECASE
                        )

        return query


class QueryUnderstandingSystem:
    """
    Complete query understanding system integrating all components.
    """

    def __init__(self):
        """Initialize query understanding system."""
        self.ner = NamedEntityRecognizer()
        self.parser = DependencyParser()
        self.expander = QueryExpander()
        self.context = ConversationContext()

    def understand(self, query: str, use_context: bool = True) -> ParsedQuery:
        """
        Fully understand and parse a query.

        Args:
            query: User query
            use_context: Whether to use conversation context

        Returns:
            ParsedQuery object with all analysis
        """
        # Resolve references using context
        if use_context:
            query = self.context.resolve_references(query)

        # Extract entities
        entities = self.ner.extract_entities(query)

        # Parse dependencies
        dependencies = self.parser.parse(query, entities)

        # Expand query
        expanded_query = self.expander.expand(query)

        # Extract key concepts
        key_concepts = self._extract_key_concepts(query, entities)

        # Infer intent based on entities and dependencies
        intent = self._infer_intent(query, entities, dependencies)

        # Create parsed query object
        parsed_query = ParsedQuery(
            original_query=query,
            tokens=query.lower().split(),
            entities=entities,
            dependencies=dependencies,
            intent=intent,
            expanded_query=expanded_query,
            key_concepts=key_concepts
        )

        # Add to context
        if use_context:
            self.context.add_query(parsed_query)

        return parsed_query

    def _extract_key_concepts(self, query: str, entities: List[Entity]) -> List[str]:
        """
        Extract key concepts from query.

        Args:
            query: Query text
            entities: Extracted entities

        Returns:
            List of key concepts
        """
        concepts = []

        # Add all concept-type entities
        for entity in entities:
            if entity.type == EntityType.CONCEPT:
                concepts.append(entity.text)

        # Add important verbs
        important_verbs = {'implement', 'optimize', 'debug', 'refactor', 'test'}
        words = query.lower().split()

        for word in words:
            if word in important_verbs:
                concepts.append(word)

        return list(set(concepts))

    def _infer_intent(self, query: str, entities: List[Entity], dependencies: List[DependencyRelation]) -> str:
        """
        Infer user intent from query components.

        Args:
            query: Query text
            entities: Extracted entities
            dependencies: Dependency relations

        Returns:
            Inferred intent
        """
        query_lower = query.lower()

        # Check for error-related intent
        if any(entity.type == EntityType.ERROR for entity in entities):
            return 'debug_error'

        # Check for comparison intent (before explanation)
        if any(word in query_lower for word in ['difference', 'compare', 'vs', 'versus', 'better than']):
            return 'comparison'

        # Check for optimization intent (before implementation)
        if any(word in query_lower for word in ['optimize', 'improve', 'faster', 'performance', 'slow']):
            if not any(word in query_lower for word in ['implement', 'create', 'build']):
                return 'optimization'

        # Check for implementation intent
        if any(word in query_lower for word in ['implement', 'create', 'build', 'write', 'code']):
            return 'implementation'

        # Check for explanation intent
        if any(word in query_lower for word in ['what', 'explain', 'how does', 'what is']):
            return 'explanation'

        # Check for usage intent
        if any(word in query_lower for word in ['how to', 'how do i', 'how can i']):
            return 'usage'

        return 'general_inquiry'

    def format_analysis(self, parsed_query: ParsedQuery) -> str:
        """
        Format query analysis for display.

        Args:
            parsed_query: Parsed query object

        Returns:
            Formatted analysis string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("QUERY ANALYSIS")
        lines.append("=" * 70)
        lines.append(f"\nOriginal Query: {parsed_query.original_query}")
        lines.append(f"Inferred Intent: {parsed_query.intent}")

        if parsed_query.entities:
            lines.append(f"\nExtracted Entities ({len(parsed_query.entities)}):")
            for entity in parsed_query.entities:
                lines.append(f"  - {entity.text} [{entity.type.value}] (confidence: {entity.confidence:.2f})")

        if parsed_query.dependencies:
            lines.append(f"\nDependency Relations ({len(parsed_query.dependencies)}):")
            for dep in parsed_query.dependencies:
                lines.append(f"  - {dep.head} --[{dep.relation}]--> {dep.dependent}")

        if parsed_query.key_concepts:
            lines.append(f"\nKey Concepts: {', '.join(parsed_query.key_concepts)}")

        lines.append(f"\nExpanded Query: {parsed_query.expanded_query}")

        return '\n'.join(lines)


def demo():
    """Demonstrate the query understanding system."""
    print("=" * 70)
    print("Advanced Query Understanding System Demo")
    print("=" * 70)

    system = QueryUnderstandingSystem()

    test_queries = [
        "How do I fix a NullPointerException in my Java code?",
        "What's the difference between Python list and tuple?",
        "How to optimize slow database queries in PostgreSQL?",
        "Implement async/await in JavaScript for API calls",
        "My React component is crashing, how do I debug it?",
        "Explain recursion with an example in Python",
        "How do I use Docker to containerize my application?",
    ]

    for query in test_queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        print('=' * 70)

        parsed = system.understand(query)
        print(system.format_analysis(parsed))

    # Demo conversation context
    print(f"\n{'=' * 70}")
    print("CONVERSATION CONTEXT DEMO")
    print('=' * 70)

    context_queries = [
        "What is a Python decorator?",
        "How do I implement it?",  # "it" refers to decorator
        "Can you show me an example?",
    ]

    for query in context_queries:
        print(f"\nUser: {query}")
        parsed = system.understand(query, use_context=True)
        print(f"Resolved: {parsed.original_query}")
        print(f"Intent: {parsed.intent}")
        if parsed.entities:
            print(f"Entities: {', '.join([e.text for e in parsed.entities[:3]])}")


if __name__ == "__main__":
    demo()
