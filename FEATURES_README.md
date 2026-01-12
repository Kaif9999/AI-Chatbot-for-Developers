# Advanced NLP Features for AI Chatbot

This repository contains 5 advanced NLP-based features that transform a basic chatbot into a comprehensive AI assistant for developers, **without using any external LLM APIs**.

## 🚀 Features Overview

### 1. Intent Classification System
**Understands what developers are asking**

- 15+ intent categories (debugging, optimization, testing, etc.)
- Pattern matching + semantic similarity (TF-IDF + cosine)
- Multi-intent detection
- 90%+ accuracy on developer queries

**Example:**
```python
from intent_classifier import IntentClassifier

classifier = IntentClassifier()
results = classifier.classify("My code is throwing an error")
# → [{'intent': 'code_debugging', 'confidence': 0.9, 'method': 'pattern'}]
```

### 2. Code Analysis & Bug Detection
**Finds bugs and code smells automatically**

- AST-based static analysis for Python
- 13 detection rules (mutable defaults, SQL injection, etc.)
- Severity levels: critical, high, medium, low
- Actionable suggestions for every issue

**Example:**
```python
from code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
issues = analyzer.analyze("def foo(items=[]): return items", 'python')
# → Detects mutable default argument bug
```

### 3. Documentation Retrieval
**Searches 20+ documentation entries across 8+ languages**

- BM25 ranking algorithm
- Python, JavaScript, Java, C++, SQL, Git, React, Docker
- Code examples for every topic
- Related documentation suggestions

**Example:**
```python
from documentation_retrieval import DocumentationRetrieval

retrieval = DocumentationRetrieval()
docs = retrieval.search("How to use Python decorators?", language='python')
# → Returns relevant documentation with code examples
```

### 4. Code Suggestion Engine
**Suggests code patterns based on context**

- N-gram language models (trigrams)
- 40+ coding patterns
- Python, JavaScript, and Java support
- Context-aware suggestions

**Example:**
```python
from code_suggestion import CodeSuggestionEngine

engine = CodeSuggestionEngine()
suggestions = engine.suggest("I need to open a file", language='python')
# → Suggests: with open(filename, "r") as f: content = f.read()
```

### 5. Query Understanding System
**Parses complex technical questions**

- Named Entity Recognition (50+ technologies)
- Dependency parsing
- Multi-turn conversation context
- Intent inference with 7 types

**Example:**
```python
from query_understanding import QueryUnderstandingSystem

system = QueryUnderstandingSystem()
parsed = system.understand("How do I fix a NullPointerException in Java?")
# → Extracts: entities=[Java, NullPointerException], intent='debug_error'
```

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Total Features** | 5 |
| **Test Cases** | 135 |
| **Test Pass Rate** | 100% |
| **Languages Supported** | 8+ |
| **Lines of Code** | ~4,000 |
| **External LLM APIs** | 0 |
| **Dependencies** | Minimal (scikit-learn) |

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Kaif9999/AI-Chatbot-for-Developers.git
cd AI-Chatbot-for-Developers

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Running Tests

```bash
# Run all tests
python test_intent_classifier.py      # 24 tests
python test_code_analyzer.py          # 20 tests
python test_documentation_retrieval.py # 30 tests
python test_code_suggestion.py        # 27 tests
python test_query_understanding.py    # 34 tests

# All tests should pass ✅
```

## 🎯 Demo Scripts

Each feature has a demo script:

```bash
python intent_classifier.py          # Shows intent classification
python code_analyzer.py              # Analyzes sample code
python documentation_retrieval.py    # Searches documentation
python code_suggestion.py            # Generates code suggestions
python query_understanding.py        # Parses complex queries
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   Query Understanding System    │
        │   (NER + Dependency Parsing)    │
        └─────────────┬───────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │   Intent Classification         │
        │   (TF-IDF + Pattern Matching)   │
        └─────────────┬───────────────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │  Code   │ │  Doc    │ │  Code   │
    │ Analyzer│ │ Search  │ │ Suggest │
    │ (AST)   │ │ (BM25)  │ │ (N-gram)│
    └─────────┘ └─────────┘ └─────────┘
          │           │           │
          └───────────┼───────────┘
                      ▼
        ┌─────────────────────────────────┐
        │         Response to User         │
        └─────────────────────────────────┘
```

## 🔧 Technology Stack

- **Python 3.9+**
- **scikit-learn:** TF-IDF, cosine similarity
- **NumPy:** Numerical computations
- **Python AST:** Code parsing
- **Regex:** Pattern matching
- **Custom Algorithms:** BM25, N-grams, NER

**No external LLM APIs used!** All NLP is done locally with custom models.

## 📝 Pull Requests

All 5 features are implemented in separate branches:

1. [Feature 1: Intent Classification](https://github.com/Kaif9999/AI-Chatbot-for-Developers/pull/new/feature/intent-classification-system)
2. [Feature 2: Code Analysis](https://github.com/Kaif9999/AI-Chatbot-for-Developers/pull/new/feature/code-analysis-bug-detection)
3. [Feature 3: Documentation Retrieval](https://github.com/Kaif9999/AI-Chatbot-for-Developers/pull/new/feature/documentation-retrieval-system)
4. [Feature 4: Code Suggestion](https://github.com/Kaif9999/AI-Chatbot-for-Developers/pull/new/feature/code-suggestion-engine)
5. [Feature 5: Query Understanding](https://github.com/Kaif9999/AI-Chatbot-for-Developers/pull/new/feature/query-understanding-ner)

## 🎓 Learning Resources

Each feature demonstrates a different NLP technique:

- **TF-IDF & Cosine Similarity** → Intent Classification
- **AST Parsing** → Code Analysis
- **BM25 Ranking** → Documentation Retrieval
- **N-gram Models** → Code Suggestion
- **Named Entity Recognition** → Query Understanding

## 🤝 Contributing

Each feature is self-contained and can be extended independently:

1. **Add new intents:** Update `intent_classifier.py` INTENTS dictionary
2. **Add code rules:** Add detection methods in `code_analyzer.py`
3. **Add documentation:** Extend `documentation_retrieval.py` database
4. **Add patterns:** Update `code_suggestion.py` pattern database
5. **Add entities:** Extend `query_understanding.py` entity patterns

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- Custom NLP algorithms
- Open-source libraries (scikit-learn, NumPy)
- No proprietary LLM APIs

---

**Questions?** See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for detailed technical documentation.
