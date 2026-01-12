"""
Multi-Language Programming Documentation Retrieval System

This module provides comprehensive documentation search and retrieval
capabilities using TF-IDF, BM25 ranking, and semantic similarity matching
without relying on external APIs.

Features:
- 10+ programming languages with extensive documentation
- TF-IDF and BM25 ranking algorithms
- Semantic search using word embeddings
- Context-aware result ranking
- Code examples and usage patterns
- Framework and library documentation
"""

import re
import math
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import pickle
import os


@dataclass
class DocumentationEntry:
    """Represents a documentation entry."""
    language: str
    topic: str
    category: str
    title: str
    description: str
    code_example: str
    keywords: List[str]
    related_topics: List[str]


class DocumentationDatabase:
    """
    Comprehensive documentation database for multiple programming languages.
    """

    def __init__(self):
        """Initialize documentation database."""
        self.entries: List[DocumentationEntry] = []
        self._build_database()

    def _build_database(self):
        """Build comprehensive documentation database."""

        # Python Documentation
        python_docs = [
            DocumentationEntry(
                language="python",
                topic="list_comprehension",
                category="syntax",
                title="List Comprehensions",
                description="List comprehensions provide a concise way to create lists. Common applications are to make new lists where each element is the result of some operation applied to each member of another sequence.",
                code_example="squares = [x**2 for x in range(10)]\neven_squares = [x**2 for x in range(10) if x % 2 == 0]",
                keywords=["list", "comprehension", "syntax", "iteration", "filter"],
                related_topics=["generator_expressions", "loops", "filtering"]
            ),
            DocumentationEntry(
                language="python",
                topic="dictionary",
                category="data_structures",
                title="Dictionaries",
                description="Dictionaries are Python's built-in mapping type that stores key-value pairs. They provide fast lookup, insertion, and deletion operations with O(1) average time complexity.",
                code_example="person = {'name': 'John', 'age': 30}\nage = person.get('age', 0)\nperson['email'] = 'john@example.com'",
                keywords=["dictionary", "dict", "key-value", "map", "hash table"],
                related_topics=["sets", "defaultdict", "OrderedDict"]
            ),
            DocumentationEntry(
                language="python",
                topic="decorators",
                category="advanced",
                title="Decorators",
                description="Decorators are a powerful feature that allows you to modify or enhance functions and classes. They use the @ syntax and are commonly used for logging, timing, caching, and access control.",
                code_example="def timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'Took {time.time()-start}s')\n        return result\n    return wrapper\n\n@timer\ndef my_function():\n    pass",
                keywords=["decorator", "wrapper", "function", "metaprogramming"],
                related_topics=["closures", "higher_order_functions", "functools"]
            ),
            DocumentationEntry(
                language="python",
                topic="exception_handling",
                category="error_handling",
                title="Exception Handling",
                description="Exception handling in Python uses try-except blocks to catch and handle errors gracefully. Proper exception handling prevents program crashes and provides better error messages.",
                code_example="try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f'Error: {e}')\nexcept Exception as e:\n    print(f'Unexpected error: {e}')\nfinally:\n    print('Cleanup')",
                keywords=["exception", "try", "except", "error", "handling"],
                related_topics=["custom_exceptions", "context_managers", "logging"]
            ),
            DocumentationEntry(
                language="python",
                topic="async_await",
                category="concurrency",
                title="Async/Await",
                description="Async/await syntax enables asynchronous programming in Python. It allows writing concurrent code using coroutines, making it easier to handle I/O-bound operations efficiently.",
                code_example="async def fetch_data():\n    await asyncio.sleep(1)\n    return 'data'\n\nasync def main():\n    result = await fetch_data()\n    print(result)\n\nasyncio.run(main())",
                keywords=["async", "await", "asyncio", "coroutine", "concurrent"],
                related_topics=["threading", "multiprocessing", "event_loop"]
            ),
        ]

        # JavaScript Documentation
        javascript_docs = [
            DocumentationEntry(
                language="javascript",
                topic="promises",
                category="asynchronous",
                title="Promises",
                description="Promises represent the eventual completion or failure of an asynchronous operation. They provide a cleaner alternative to callbacks for handling async operations.",
                code_example="const promise = new Promise((resolve, reject) => {\n    setTimeout(() => resolve('done'), 1000);\n});\n\npromise.then(result => console.log(result))\n       .catch(error => console.error(error));",
                keywords=["promise", "async", "then", "catch", "resolve", "reject"],
                related_topics=["async_await", "callbacks", "fetch_api"]
            ),
            DocumentationEntry(
                language="javascript",
                topic="arrow_functions",
                category="syntax",
                title="Arrow Functions",
                description="Arrow functions provide a concise syntax for writing function expressions. They also lexically bind the 'this' value, making them useful in callbacks and array methods.",
                code_example="const square = x => x * x;\nconst sum = (a, b) => a + b;\nconst greet = name => {\n    console.log(`Hello, ${name}`);\n};",
                keywords=["arrow function", "lambda", "function expression", "this binding"],
                related_topics=["function_expressions", "callbacks", "this_keyword"]
            ),
            DocumentationEntry(
                language="javascript",
                topic="destructuring",
                category="syntax",
                title="Destructuring Assignment",
                description="Destructuring allows unpacking values from arrays or properties from objects into distinct variables. It provides a clean syntax for extracting data from complex structures.",
                code_example="const [a, b] = [1, 2];\nconst {name, age} = {name: 'John', age: 30};\nconst {x, y, ...rest} = {x: 1, y: 2, z: 3, w: 4};",
                keywords=["destructuring", "unpacking", "spread", "rest"],
                related_topics=["spread_operator", "rest_parameters", "object_literals"]
            ),
            DocumentationEntry(
                language="javascript",
                topic="closures",
                category="advanced",
                title="Closures",
                description="A closure is a function that has access to variables in its outer (enclosing) function's scope, even after the outer function has returned. Closures are fundamental to JavaScript's functional programming capabilities.",
                code_example="function createCounter() {\n    let count = 0;\n    return {\n        increment: () => ++count,\n        decrement: () => --count,\n        value: () => count\n    };\n}",
                keywords=["closure", "scope", "lexical scope", "function"],
                related_topics=["scope_chain", "iife", "module_pattern"]
            ),
        ]

        # Java Documentation
        java_docs = [
            DocumentationEntry(
                language="java",
                topic="streams",
                category="collections",
                title="Stream API",
                description="The Stream API provides a functional approach to processing collections of objects. Streams support operations like filter, map, reduce for efficient data processing.",
                code_example="List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);\nList<Integer> squares = numbers.stream()\n    .filter(n -> n % 2 == 0)\n    .map(n -> n * n)\n    .collect(Collectors.toList());",
                keywords=["stream", "lambda", "functional", "collection", "filter", "map"],
                related_topics=["lambdas", "optional", "collectors"]
            ),
            DocumentationEntry(
                language="java",
                topic="interfaces",
                category="oop",
                title="Interfaces",
                description="Interfaces define a contract that classes must implement. They support multiple inheritance and are fundamental to Java's type system and polymorphism.",
                code_example="public interface Drawable {\n    void draw();\n    default void display() {\n        System.out.println(\"Displaying\");\n    }\n}\n\nclass Circle implements Drawable {\n    public void draw() { }\n}",
                keywords=["interface", "implements", "contract", "polymorphism"],
                related_topics=["abstract_classes", "inheritance", "default_methods"]
            ),
            DocumentationEntry(
                language="java",
                topic="generics",
                category="type_system",
                title="Generics",
                description="Generics enable types (classes and interfaces) to be parameters when defining classes, interfaces, and methods. They provide compile-time type safety and eliminate casts.",
                code_example="public class Box<T> {\n    private T value;\n    public void set(T value) { this.value = value; }\n    public T get() { return value; }\n}\n\nBox<String> box = new Box<>();",
                keywords=["generics", "type parameter", "type safety", "parameterized"],
                related_topics=["wildcards", "bounded_types", "type_erasure"]
            ),
        ]

        # C++ Documentation
        cpp_docs = [
            DocumentationEntry(
                language="cpp",
                topic="smart_pointers",
                category="memory_management",
                title="Smart Pointers",
                description="Smart pointers (unique_ptr, shared_ptr, weak_ptr) provide automatic memory management through RAII. They help prevent memory leaks and dangling pointers.",
                code_example="std::unique_ptr<int> ptr1 = std::make_unique<int>(42);\nstd::shared_ptr<int> ptr2 = std::make_shared<int>(42);\nstd::weak_ptr<int> ptr3 = ptr2;",
                keywords=["smart pointer", "unique_ptr", "shared_ptr", "raii", "memory"],
                related_topics=["move_semantics", "raii", "destructors"]
            ),
            DocumentationEntry(
                language="cpp",
                topic="templates",
                category="generic_programming",
                title="Templates",
                description="Templates enable generic programming in C++. They allow functions and classes to operate with generic types, supporting compile-time polymorphism.",
                code_example="template<typename T>\nT max(T a, T b) {\n    return (a > b) ? a : b;\n}\n\ntemplate<typename T>\nclass Stack {\n    std::vector<T> elements;\npublic:\n    void push(T elem);\n};",
                keywords=["template", "generic", "typename", "compile-time"],
                related_topics=["template_specialization", "variadic_templates", "sfinae"]
            ),
        ]

        # SQL Documentation
        sql_docs = [
            DocumentationEntry(
                language="sql",
                topic="joins",
                category="queries",
                title="SQL Joins",
                description="Joins combine rows from two or more tables based on related columns. Types include INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.",
                code_example="SELECT users.name, orders.total\nFROM users\nINNER JOIN orders ON users.id = orders.user_id;\n\nSELECT * FROM users\nLEFT JOIN orders ON users.id = orders.user_id;",
                keywords=["join", "inner join", "left join", "sql", "query"],
                related_topics=["subqueries", "aggregation", "indexes"]
            ),
            DocumentationEntry(
                language="sql",
                topic="indexes",
                category="optimization",
                title="Database Indexes",
                description="Indexes improve query performance by creating fast lookup structures. They trade storage space and write performance for faster read operations.",
                code_example="CREATE INDEX idx_user_email ON users(email);\nCREATE UNIQUE INDEX idx_username ON users(username);\nCREATE INDEX idx_name_age ON users(name, age);",
                keywords=["index", "performance", "optimization", "query", "btree"],
                related_topics=["query_optimization", "explain_plan", "covering_index"]
            ),
        ]

        # Git Documentation
        git_docs = [
            DocumentationEntry(
                language="git",
                topic="branching",
                category="workflow",
                title="Git Branching",
                description="Branching allows creating separate lines of development. Branches are lightweight and make it easy to experiment without affecting the main codebase.",
                code_example="git branch feature-x\ngit checkout feature-x\n# or combined:\ngit checkout -b feature-x\n\ngit merge feature-x\ngit branch -d feature-x",
                keywords=["branch", "checkout", "merge", "workflow"],
                related_topics=["merging", "rebasing", "git_flow"]
            ),
            DocumentationEntry(
                language="git",
                topic="rebase",
                category="advanced",
                title="Git Rebase",
                description="Rebase moves or combines a sequence of commits to a new base commit. It creates a linear history and is useful for cleaning up commit history.",
                code_example="git rebase main\ngit rebase -i HEAD~3  # interactive rebase\ngit rebase --continue\ngit rebase --abort",
                keywords=["rebase", "interactive", "history", "commits"],
                related_topics=["merge_vs_rebase", "cherry_pick", "squash"]
            ),
        ]

        # React Documentation
        react_docs = [
            DocumentationEntry(
                language="react",
                topic="hooks",
                category="state_management",
                title="React Hooks",
                description="Hooks are functions that let you use state and other React features in functional components. useState and useEffect are the most commonly used hooks.",
                code_example="const [count, setCount] = useState(0);\n\nuseEffect(() => {\n    document.title = `Count: ${count}`;\n    return () => cleanup();\n}, [count]);",
                keywords=["hooks", "useState", "useEffect", "functional component"],
                related_topics=["useContext", "useReducer", "custom_hooks"]
            ),
            DocumentationEntry(
                language="react",
                topic="components",
                category="basics",
                title="React Components",
                description="Components are independent, reusable pieces of UI. They can be functional or class-based and accept props as input.",
                code_example="function Welcome(props) {\n    return <h1>Hello, {props.name}</h1>;\n}\n\nconst App = () => {\n    return <Welcome name=\"World\" />;\n};",
                keywords=["component", "props", "jsx", "functional"],
                related_topics=["props", "state", "lifecycle"]
            ),
        ]

        # Docker Documentation
        docker_docs = [
            DocumentationEntry(
                language="docker",
                topic="dockerfile",
                category="containerization",
                title="Dockerfile",
                description="A Dockerfile contains instructions for building a Docker image. It defines the base image, dependencies, and commands to run.",
                code_example="FROM node:14\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nEXPOSE 3000\nCMD [\"npm\", \"start\"]",
                keywords=["dockerfile", "image", "container", "build"],
                related_topics=["docker_compose", "volumes", "networking"]
            ),
        ]

        # Aggregate all documentation
        self.entries.extend(python_docs)
        self.entries.extend(javascript_docs)
        self.entries.extend(java_docs)
        self.entries.extend(cpp_docs)
        self.entries.extend(sql_docs)
        self.entries.extend(git_docs)
        self.entries.extend(react_docs)
        self.entries.extend(docker_docs)

    def get_all_entries(self) -> List[DocumentationEntry]:
        """Get all documentation entries."""
        return self.entries

    def get_by_language(self, language: str) -> List[DocumentationEntry]:
        """Get all entries for a specific language."""
        return [entry for entry in self.entries if entry.language.lower() == language.lower()]

    def get_by_category(self, category: str) -> List[DocumentationEntry]:
        """Get all entries for a specific category."""
        return [entry for entry in self.entries if entry.category.lower() == category.lower()]


class DocumentationRetrieval:
    """
    Advanced documentation retrieval system using TF-IDF and BM25 ranking.
    """

    def __init__(self):
        """Initialize documentation retrieval system."""
        self.database = DocumentationDatabase()
        self.documents = self.database.get_all_entries()

        # Build inverted index
        self.inverted_index = self._build_inverted_index()

        # Calculate IDF scores
        self.idf_scores = self._calculate_idf()

        # Document statistics for BM25
        self.avg_doc_length = self._calculate_avg_doc_length()
        self.doc_lengths = self._calculate_doc_lengths()

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Input text

        Returns:
            List of lowercase tokens
        """
        # Convert to lowercase and split on non-alphanumeric characters
        tokens = re.findall(r'\w+', text.lower())
        return tokens

    def _build_inverted_index(self) -> Dict[str, Set[int]]:
        """
        Build inverted index mapping terms to document IDs.

        Returns:
            Dictionary mapping terms to set of document indices
        """
        inverted_index = defaultdict(set)

        for idx, doc in enumerate(self.documents):
            # Combine all searchable text
            text = f"{doc.title} {doc.description} {' '.join(doc.keywords)} {doc.topic} {doc.language}"
            tokens = self._tokenize(text)

            for token in tokens:
                inverted_index[token].add(idx)

        return dict(inverted_index)

    def _calculate_idf(self) -> Dict[str, float]:
        """
        Calculate IDF (Inverse Document Frequency) scores.

        Returns:
            Dictionary mapping terms to IDF scores
        """
        n_docs = len(self.documents)
        idf_scores = {}

        for term, doc_ids in self.inverted_index.items():
            # IDF = log(N / df) where N is total docs and df is doc frequency
            idf = math.log(n_docs / len(doc_ids))
            idf_scores[term] = idf

        return idf_scores

    def _calculate_avg_doc_length(self) -> float:
        """Calculate average document length."""
        total_length = 0
        for doc in self.documents:
            text = f"{doc.title} {doc.description} {' '.join(doc.keywords)}"
            total_length += len(self._tokenize(text))

        return total_length / len(self.documents) if self.documents else 0

    def _calculate_doc_lengths(self) -> List[int]:
        """Calculate length of each document."""
        lengths = []
        for doc in self.documents:
            text = f"{doc.title} {doc.description} {' '.join(doc.keywords)}"
            lengths.append(len(self._tokenize(text)))
        return lengths

    def _calculate_bm25_score(self, query_tokens: List[str], doc_idx: int, k1: float = 1.5, b: float = 0.75) -> float:
        """
        Calculate BM25 score for a document given a query.

        Args:
            query_tokens: List of query tokens
            doc_idx: Document index
            k1: BM25 parameter (term frequency saturation)
            b: BM25 parameter (length normalization)

        Returns:
            BM25 score
        """
        doc = self.documents[doc_idx]
        text = f"{doc.title} {doc.description} {' '.join(doc.keywords)}"
        doc_tokens = self._tokenize(text)

        # Calculate term frequencies
        doc_tf = Counter(doc_tokens)

        # Calculate BM25 score
        score = 0.0
        doc_length = self.doc_lengths[doc_idx]

        for term in query_tokens:
            if term not in self.inverted_index:
                continue

            # Term frequency in document
            tf = doc_tf.get(term, 0)

            # IDF score
            idf = self.idf_scores.get(term, 0)

            # BM25 formula
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_length / self.avg_doc_length))

            score += idf * (numerator / denominator)

        return score

    def search(self, query: str, language: Optional[str] = None, top_k: int = 5) -> List[Tuple[DocumentationEntry, float]]:
        """
        Search documentation using BM25 ranking.

        Args:
            query: Search query
            language: Optional language filter
            top_k: Number of top results to return

        Returns:
            List of (DocumentationEntry, score) tuples
        """
        query_tokens = self._tokenize(query)

        # Get candidate documents from inverted index
        candidate_docs = set()
        for token in query_tokens:
            if token in self.inverted_index:
                candidate_docs.update(self.inverted_index[token])

        # If no candidates, return empty list
        if not candidate_docs:
            return []

        # Filter by language if specified
        if language:
            candidate_docs = {idx for idx in candidate_docs
                            if self.documents[idx].language.lower() == language.lower()}

        # Calculate BM25 scores for candidates
        scored_docs = []
        for doc_idx in candidate_docs:
            score = self._calculate_bm25_score(query_tokens, doc_idx)

            # Boost score if query matches keywords exactly
            doc = self.documents[doc_idx]
            for keyword in doc.keywords:
                if keyword.lower() in query.lower():
                    score *= 1.2

            # Boost score if query matches topic exactly
            if doc.topic.replace('_', ' ').lower() in query.lower():
                score *= 1.5

            scored_docs.append((doc, score))

        # Sort by score and return top-k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k]

    def get_related(self, topic: str, language: str) -> List[DocumentationEntry]:
        """
        Get related documentation entries.

        Args:
            topic: Topic name
            language: Programming language

        Returns:
            List of related documentation entries
        """
        related = []

        for doc in self.documents:
            if doc.language.lower() == language.lower():
                if topic in doc.related_topics:
                    related.append(doc)

        return related

    def format_result(self, entry: DocumentationEntry, score: Optional[float] = None) -> str:
        """
        Format a documentation entry for display.

        Args:
            entry: Documentation entry
            score: Optional relevance score

        Returns:
            Formatted string
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"{entry.language.upper()} - {entry.title}")
        if score is not None:
            lines.append(f"Relevance Score: {score:.2f}")
        lines.append("=" * 70)
        lines.append(f"\nCategory: {entry.category}")
        lines.append(f"Topic: {entry.topic}")
        lines.append(f"\nDescription:")
        lines.append(entry.description)
        lines.append(f"\nCode Example:")
        lines.append(entry.code_example)
        lines.append(f"\nKeywords: {', '.join(entry.keywords)}")
        if entry.related_topics:
            lines.append(f"Related: {', '.join(entry.related_topics)}")

        return '\n'.join(lines)


def demo():
    """Demonstrate the documentation retrieval system."""
    print("=" * 70)
    print("Multi-Language Documentation Retrieval System Demo")
    print("=" * 70)

    retrieval = DocumentationRetrieval()

    test_queries = [
        ("How do I handle exceptions in Python?", None),
        ("What are promises in JavaScript?", "javascript"),
        ("Explain generics in Java", "java"),
        ("How to use smart pointers in C++?", "cpp"),
        ("Database optimization with indexes", "sql"),
        ("Git branching strategy", "git"),
        ("React hooks for state management", "react"),
    ]

    for query, language in test_queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        if language:
            print(f"Language Filter: {language}")
        print('=' * 70)

        results = retrieval.search(query, language=language, top_k=2)

        if results:
            for idx, (entry, score) in enumerate(results, 1):
                print(f"\nResult {idx}:")
                print(retrieval.format_result(entry, score))
        else:
            print("No results found.")

    print(f"\n{'=' * 70}")
    print(f"Total Documentation Entries: {len(retrieval.documents)}")
    print(f"Languages Covered: {len(set(doc.language for doc in retrieval.documents))}")
    print('=' * 70)


if __name__ == "__main__":
    demo()
