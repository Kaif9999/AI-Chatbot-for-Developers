"""
Context-Aware Code Suggestion Engine

This module provides intelligent code suggestions using N-gram language models,
pattern recognition, and contextual analysis without relying on external APIs.

Features:
- N-gram language models trained on code patterns
- Context-aware suggestions based on current code
- Multi-language support (Python, JavaScript, Java)
- Common coding patterns and idioms
- API usage suggestions
- Code completion and generation
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict, Counter
import json
from dataclasses import dataclass


@dataclass
class CodeSuggestion:
    """Represents a code suggestion."""
    code: str
    description: str
    confidence: float
    category: str
    language: str


class NGramModel:
    """
    N-gram language model for code patterns.

    Learns common sequences of tokens in code and predicts likely continuations.
    """

    def __init__(self, n: int = 3):
        """
        Initialize N-gram model.

        Args:
            n: Size of n-grams to use (default: 3 for trigrams)
        """
        self.n = n
        self.ngrams = defaultdict(Counter)
        self.vocabulary = set()

    def tokenize(self, code: str) -> List[str]:
        """
        Tokenize code into tokens.

        Args:
            code: Source code string

        Returns:
            List of tokens
        """
        # Split on whitespace and common delimiters, keeping them as separate tokens
        tokens = re.findall(r'\w+|[^\w\s]', code)
        return tokens

    def train(self, code_samples: List[str]):
        """
        Train the n-gram model on code samples.

        Args:
            code_samples: List of code strings
        """
        for code in code_samples:
            tokens = self.tokenize(code)
            self.vocabulary.update(tokens)

            # Build n-grams
            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i + self.n - 1])
                next_token = tokens[i + self.n - 1]
                self.ngrams[ngram][next_token] += 1

    def predict_next(self, context: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Predict next tokens given context.

        Args:
            context: List of previous tokens
            top_k: Number of top predictions to return

        Returns:
            List of (token, probability) tuples
        """
        # Get last n-1 tokens as context
        ngram = tuple(context[-(self.n - 1):])

        if ngram not in self.ngrams:
            return []

        # Get token counts and calculate probabilities
        token_counts = self.ngrams[ngram]
        total = sum(token_counts.values())

        # Calculate probabilities
        predictions = [(token, count / total) for token, count in token_counts.items()]

        # Sort by probability and return top-k
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:top_k]


class CodePatternDatabase:
    """
    Database of common coding patterns and idioms.
    """

    def __init__(self):
        """Initialize pattern database."""
        self.patterns = self._build_patterns()

    def _build_patterns(self) -> Dict[str, List[Dict]]:
        """
        Build comprehensive pattern database.

        Returns:
            Dictionary mapping contexts to patterns
        """
        patterns = {
            'python': {
                'file_operations': [
                    {
                        'trigger': ['open', 'file'],
                        'suggestion': 'with open(filename, "r") as f:\n    content = f.read()',
                        'description': 'Context manager for safe file handling',
                        'category': 'file_io'
                    },
                    {
                        'trigger': ['read', 'json'],
                        'suggestion': 'with open(filename, "r") as f:\n    data = json.load(f)',
                        'description': 'Read JSON file',
                        'category': 'file_io'
                    },
                ],
                'error_handling': [
                    {
                        'trigger': ['try', 'except'],
                        'suggestion': 'try:\n    # risky operation\n    pass\nexcept SpecificException as e:\n    # handle error\n    logging.error(f"Error: {e}")',
                        'description': 'Proper exception handling with logging',
                        'category': 'error_handling'
                    },
                ],
                'list_operations': [
                    {
                        'trigger': ['filter', 'list'],
                        'suggestion': 'filtered = [x for x in items if condition(x)]',
                        'description': 'Filter list using list comprehension',
                        'category': 'data_structures'
                    },
                    {
                        'trigger': ['map', 'list'],
                        'suggestion': 'transformed = [transform(x) for x in items]',
                        'description': 'Transform list using list comprehension',
                        'category': 'data_structures'
                    },
                    {
                        'trigger': ['sort', 'list'],
                        'suggestion': 'sorted_list = sorted(items, key=lambda x: x.attribute)',
                        'description': 'Sort list with custom key',
                        'category': 'data_structures'
                    },
                ],
                'dictionary_operations': [
                    {
                        'trigger': ['default', 'dict'],
                        'suggestion': 'value = my_dict.get(key, default_value)',
                        'description': 'Safe dictionary access with default',
                        'category': 'data_structures'
                    },
                    {
                        'trigger': ['merge', 'dict'],
                        'suggestion': 'merged = {**dict1, **dict2}',
                        'description': 'Merge dictionaries using unpacking',
                        'category': 'data_structures'
                    },
                ],
                'string_operations': [
                    {
                        'trigger': ['join', 'strings'],
                        'suggestion': 'result = "".join(string_list)',
                        'description': 'Efficiently join strings',
                        'category': 'strings'
                    },
                    {
                        'trigger': ['format', 'string'],
                        'suggestion': 'formatted = f"Value: {variable}"',
                        'description': 'F-string formatting',
                        'category': 'strings'
                    },
                ],
                'class_definition': [
                    {
                        'trigger': ['class', 'init'],
                        'suggestion': 'class MyClass:\n    def __init__(self, param):\n        self.param = param\n\n    def method(self):\n        pass',
                        'description': 'Basic class with constructor',
                        'category': 'oop'
                    },
                    {
                        'trigger': ['dataclass'],
                        'suggestion': 'from dataclasses import dataclass\n\n@dataclass\nclass Person:\n    name: str\n    age: int',
                        'description': 'Dataclass for simple data structures',
                        'category': 'oop'
                    },
                ],
            },
            'javascript': {
                'async_operations': [
                    {
                        'trigger': ['fetch', 'api'],
                        'suggestion': 'const response = await fetch(url);\nconst data = await response.json();',
                        'description': 'Fetch API with async/await',
                        'category': 'async'
                    },
                    {
                        'trigger': ['promise', 'then'],
                        'suggestion': 'promise\n    .then(result => { /* success */ })\n    .catch(error => { /* error */ })\n    .finally(() => { /* cleanup */ });',
                        'description': 'Promise chain with error handling',
                        'category': 'async'
                    },
                ],
                'array_operations': [
                    {
                        'trigger': ['filter', 'array'],
                        'suggestion': 'const filtered = array.filter(item => condition);',
                        'description': 'Filter array',
                        'category': 'arrays'
                    },
                    {
                        'trigger': ['map', 'array'],
                        'suggestion': 'const transformed = array.map(item => transform(item));',
                        'description': 'Transform array',
                        'category': 'arrays'
                    },
                    {
                        'trigger': ['reduce', 'array'],
                        'suggestion': 'const result = array.reduce((acc, item) => acc + item, 0);',
                        'description': 'Reduce array to single value',
                        'category': 'arrays'
                    },
                ],
                'destructuring': [
                    {
                        'trigger': ['destructure', 'object'],
                        'suggestion': 'const { prop1, prop2, ...rest } = object;',
                        'description': 'Object destructuring with rest',
                        'category': 'syntax'
                    },
                    {
                        'trigger': ['destructure', 'array'],
                        'suggestion': 'const [first, second, ...rest] = array;',
                        'description': 'Array destructuring',
                        'category': 'syntax'
                    },
                ],
                'functions': [
                    {
                        'trigger': ['arrow', 'function'],
                        'suggestion': 'const myFunc = (param) => {\n    // function body\n    return result;\n};',
                        'description': 'Arrow function with body',
                        'category': 'functions'
                    },
                ],
            },
            'java': {
                'collections': [
                    {
                        'trigger': ['list', 'iterate'],
                        'suggestion': 'list.forEach(item -> {\n    // process item\n});',
                        'description': 'Iterate list with lambda',
                        'category': 'collections'
                    },
                    {
                        'trigger': ['stream', 'filter'],
                        'suggestion': 'List<T> filtered = list.stream()\n    .filter(item -> condition)\n    .collect(Collectors.toList());',
                        'description': 'Filter with streams',
                        'category': 'streams'
                    },
                ],
                'error_handling': [
                    {
                        'trigger': ['try', 'catch'],
                        'suggestion': 'try {\n    // risky operation\n} catch (SpecificException e) {\n    logger.error("Error", e);\n} finally {\n    // cleanup\n}',
                        'description': 'Try-catch with logging',
                        'category': 'exceptions'
                    },
                ],
            }
        }

        return patterns

    def get_patterns(self, language: str, keywords: List[str]) -> List[Dict]:
        """
        Get relevant patterns for given keywords.

        Args:
            language: Programming language
            keywords: List of keywords from context

        Returns:
            List of matching patterns
        """
        if language not in self.patterns:
            return []

        matching_patterns = []

        for category, patterns_list in self.patterns[language].items():
            for pattern in patterns_list:
                # Check if any trigger matches keywords
                if any(trigger in ' '.join(keywords).lower() for trigger in pattern['trigger']):
                    matching_patterns.append(pattern)

        return matching_patterns


class CodeSuggestionEngine:
    """
    Intelligent code suggestion engine combining multiple techniques.
    """

    def __init__(self):
        """Initialize the code suggestion engine."""
        self.ngram_models = {}
        self.pattern_db = CodePatternDatabase()
        self._train_models()

    def _train_models(self):
        """Train N-gram models on sample code."""

        # Python training samples
        python_samples = [
            'with open ( filename , "r" ) as f : content = f . read ( )',
            'try : result = func ( ) except Exception as e : print ( e )',
            'for item in items : print ( item )',
            'if condition : return True else : return False',
            'def function ( param ) : return param * 2',
            'class MyClass : def __init__ ( self ) : self . value = 0',
            'import json with open ( file ) as f : data = json . load ( f )',
            'result = [ x for x in range ( 10 ) if x % 2 == 0 ]',
        ]

        # JavaScript training samples
        javascript_samples = [
            'const result = await fetch ( url ) ;',
            'function myFunc ( param ) { return param ; }',
            'const array = [ 1 , 2 , 3 ] ;',
            'if ( condition ) { return true ; } else { return false ; }',
            'const filtered = array . filter ( item => condition ) ;',
            'try { await operation ( ) ; } catch ( error ) { console . error ( error ) ; }',
        ]

        # Train models
        python_model = NGramModel(n=3)
        python_model.train(python_samples)
        self.ngram_models['python'] = python_model

        javascript_model = NGramModel(n=3)
        javascript_model.train(javascript_samples)
        self.ngram_models['javascript'] = javascript_model

    def suggest(self, code_context: str, language: str = 'python', max_suggestions: int = 5) -> List[CodeSuggestion]:
        """
        Generate code suggestions based on context.

        Args:
            code_context: Current code context
            language: Programming language
            max_suggestions: Maximum number of suggestions

        Returns:
            List of CodeSuggestion objects
        """
        suggestions = []

        # Extract keywords from context
        keywords = re.findall(r'\w+', code_context.lower())

        # Get pattern-based suggestions
        pattern_suggestions = self._get_pattern_suggestions(keywords, language)
        suggestions.extend(pattern_suggestions)

        # Get N-gram based suggestions
        ngram_suggestions = self._get_ngram_suggestions(code_context, language)
        suggestions.extend(ngram_suggestions)

        # Sort by confidence and limit
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return suggestions[:max_suggestions]

    def _get_pattern_suggestions(self, keywords: List[str], language: str) -> List[CodeSuggestion]:
        """
        Get pattern-based suggestions.

        Args:
            keywords: Keywords from context
            language: Programming language

        Returns:
            List of CodeSuggestion objects
        """
        patterns = self.pattern_db.get_patterns(language, keywords)
        suggestions = []

        for pattern in patterns:
            suggestion = CodeSuggestion(
                code=pattern['suggestion'],
                description=pattern['description'],
                confidence=0.9,  # High confidence for pattern matches
                category=pattern['category'],
                language=language
            )
            suggestions.append(suggestion)

        return suggestions

    def _get_ngram_suggestions(self, code_context: str, language: str) -> List[CodeSuggestion]:
        """
        Get N-gram based suggestions.

        Args:
            code_context: Code context
            language: Programming language

        Returns:
            List of CodeSuggestion objects
        """
        if language not in self.ngram_models:
            return []

        model = self.ngram_models[language]
        tokens = model.tokenize(code_context)

        if len(tokens) < model.n - 1:
            return []

        # Predict next tokens
        predictions = model.predict_next(tokens, top_k=3)

        suggestions = []
        for token, prob in predictions:
            suggestion = CodeSuggestion(
                code=token,
                description=f"Next token suggestion based on context",
                confidence=prob,
                category='completion',
                language=language
            )
            suggestions.append(suggestion)

        return suggestions

    def suggest_completion(self, partial_code: str, language: str = 'python') -> List[str]:
        """
        Suggest completions for partial code.

        Args:
            partial_code: Incomplete code
            language: Programming language

        Returns:
            List of completion suggestions
        """
        completions = []

        # Common completions by language
        completion_templates = {
            'python': {
                'if ': 'if condition:\n    pass',
                'for ': 'for item in items:\n    pass',
                'def ': 'def function_name(params):\n    pass',
                'class ': 'class ClassName:\n    def __init__(self):\n        pass',
                'with ': 'with open(filename) as f:\n    pass',
                'try': 'try:\n    pass\nexcept Exception as e:\n    pass',
            },
            'javascript': {
                'if ': 'if (condition) {\n    // code\n}',
                'for ': 'for (let i = 0; i < array.length; i++) {\n    // code\n}',
                'function ': 'function name(params) {\n    // code\n}',
                'const ': 'const variable = value;',
                'async ': 'async function name() {\n    await operation();\n}',
            }
        }

        if language in completion_templates:
            templates = completion_templates[language]
            partial_lower = partial_code.lower().strip()

            for trigger, template in templates.items():
                if partial_lower.endswith(trigger.strip()):
                    completions.append(template)

        return completions


def demo():
    """Demonstrate the code suggestion engine."""
    print("=" * 70)
    print("Context-Aware Code Suggestion Engine Demo")
    print("=" * 70)

    engine = CodeSuggestionEngine()

    test_cases = [
        ("I need to open a file and read it", "python"),
        ("How do I filter a list in Python?", "python"),
        ("I want to handle exceptions properly", "python"),
        ("How to fetch data from an API?", "javascript"),
        ("I need to filter an array", "javascript"),
        ("Map over array elements", "javascript"),
    ]

    for context, language in test_cases:
        print(f"\n{'=' * 70}")
        print(f"Context: {context}")
        print(f"Language: {language}")
        print('=' * 70)

        suggestions = engine.suggest(context, language, max_suggestions=3)

        if suggestions:
            for idx, suggestion in enumerate(suggestions, 1):
                print(f"\nSuggestion {idx}:")
                print(f"Category: {suggestion.category}")
                print(f"Confidence: {suggestion.confidence:.2f}")
                print(f"Description: {suggestion.description}")
                print(f"\nCode:")
                print(suggestion.code)
                print("-" * 70)
        else:
            print("No suggestions found.")

    # Completion demo
    print(f"\n{'=' * 70}")
    print("Code Completion Demo")
    print('=' * 70)

    partial_codes = [
        ("if ", "python"),
        ("for ", "python"),
        ("def ", "python"),
    ]

    for partial, lang in partial_codes:
        print(f"\nPartial Code: '{partial}'")
        print(f"Language: {lang}")
        completions = engine.suggest_completion(partial, lang)
        if completions:
            print("Completions:")
            for completion in completions:
                print(completion)
                print("-" * 40)


if __name__ == "__main__":
    demo()
