# 🏗️ System Architecture

## Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   AI CHATBOT PROJECT                        │
│                                                             │
│  ┌──────────────────────┐    ┌──────────────────────┐     │
│  │   Rule-Based Bot     │    │   AI-Powered Bot     │     │
│  │   (chatbot.py)       │    │  (chatbot_model.py)  │     │
│  └──────────────────────┘    └──────────────────────┘     │
│           │                            │                    │
│           │                            │                    │
│           ▼                            ▼                    │
│  ┌──────────────────────┐    ┌──────────────────────┐     │
│  │   Pattern Database   │    │  Transformer Model   │     │
│  │     (pairs.py)       │    │  (microsoft/phi-2)   │     │
│  └──────────────────────┘    └──────────────────────┘     │
│           │                                                 │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────────┐                                  │
│  │    Test Suite        │                                  │
│  │  (test_chatbot.py)   │                                  │
│  └──────────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Rule-Based Chatbot Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RULE-BASED CHATBOT                       │
└─────────────────────────────────────────────────────────────┘

                    User Input
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Input Normalization         │
        │   - Convert to lowercase      │
        │   - Tokenize with NLTK        │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Pattern Matching Engine     │
        │   - Load patterns from pairs  │
        │   - Regex search (re.search)  │
        │   - Loop through all patterns │
        └───────────────────────────────┘
                        │
                ┌───────┴───────┐
                │               │
            Match Found?    No Match
                │               │
                ▼               ▼
    ┌───────────────────┐   ┌──────────────────┐
    │ Response Selection│   │ Learning Mode    │
    │ - Random choice   │   │ - Ask user       │
    │ - From list       │   │ - Save to pairs  │
    └───────────────────┘   │ - Write to file  │
                │           └──────────────────┘
                │                   │
                └───────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Response Display    │
            │   - Slow typing effect│
            │   - Character by char │
            └───────────────────────┘
                        │
                        ▼
                   User sees output
```

---

## AI-Powered Chatbot Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AI-POWERED CHATBOT                        │
└─────────────────────────────────────────────────────────────┘

                    User Input
                        │
                        ▼
        ┌───────────────────────────────┐
        │   ChatbotModel Class          │
        │   - Initialize model          │
        │   - Load tokenizer            │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Tokenization                │
        │   - Text → Token IDs          │
        │   - Max length: 128           │
        │   - Truncation enabled        │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Tensor Conversion           │
        │   - Token IDs → PyTorch       │
        │   - return_tensors="pt"       │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Model Inference             │
        │   - Neural network forward    │
        │   - Attention mechanisms      │
        │   - Generate 50 tokens        │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Detokenization              │
        │   - Token IDs → Text          │
        │   - Skip special tokens       │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Error Handling              │
        │   - Try-except wrapper        │
        │   - Return error message      │
        └───────────────────────────────┘
                        │
                        ▼
                   User sees output
```

---

## Data Flow Diagram

### Rule-Based System

```
┌──────────┐
│  User    │
└────┬─────┘
     │ "what is python?"
     ▼
┌─────────────────┐
│  chatbot.py     │
│  respond()      │
└────┬────────────┘
     │ lowercase + tokenize
     ▼
┌─────────────────┐
│  pairs.py       │
│  Pattern DB     │
└────┬────────────┘
     │ match found
     ▼
┌─────────────────┐
│  Random Select  │
│  rd.choice()    │
└────┬────────────┘
     │ "Python is a high-level..."
     ▼
┌─────────────────┐
│  slow_print()   │
│  Typing effect  │
└────┬────────────┘
     │ Display character by character
     ▼
┌──────────┐
│  User    │
│  Sees    │
└──────────┘
```

### AI-Powered System

```
┌──────────┐
│  User    │
└────┬─────┘
     │ "explain decorators"
     ▼
┌─────────────────────┐
│  chatbot_model.py   │
│  ChatbotModel       │
└────┬────────────────┘
     │ handle_user_input()
     ▼
┌─────────────────────┐
│  AutoTokenizer      │
│  Text → Tokens      │
└────┬────────────────┘
     │ [1234, 5678, 9012]
     ▼
┌─────────────────────┐
│  Phi-2 Model        │
│  2.7B parameters    │
└────┬────────────────┘
     │ Neural network inference
     ▼
┌─────────────────────┐
│  Token Generation   │
│  50 new tokens      │
└────┬────────────────┘
     │ [3456, 7890, 1111, ...]
     ▼
┌─────────────────────┐
│  AutoTokenizer      │
│  Tokens → Text      │
└────┬────────────────┘
     │ "Decorators are functions..."
     ▼
┌──────────┐
│  User    │
│  Sees    │
└──────────┘
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────────┐         ┌─────────────┐                 │
│   │   User      │◄───────►│  Terminal   │                 │
│   │  Interface  │         │   Input     │                 │
│   └─────────────┘         └─────────────┘                 │
│          │                        │                        │
│          │                        │                        │
│          ▼                        ▼                        │
│   ┌──────────────────────────────────────┐                │
│   │         Main Program Loop            │                │
│   │  - while True                        │                │
│   │  - input() / print()                 │                │
│   └──────────────────────────────────────┘                │
│          │                        │                        │
│          │                        │                        │
│    ┌─────┴─────┐           ┌─────┴─────┐                 │
│    ▼           ▼           ▼           ▼                  │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐             │
│ │respond │ │ slow_  │ │handle_ │ │get_res │             │
│ │  ()    │ │print() │ │user_   │ │ponse() │             │
│ └────────┘ └────────┘ │input() │ └────────┘             │
│     │                  └────────┘      │                  │
│     │                       │          │                  │
│     ▼                       ▼          ▼                  │
│ ┌────────┐           ┌──────────────────┐                │
│ │ pairs  │           │  Transformers    │                │
│ │  .py   │           │    Library       │                │
│ └────────┘           └──────────────────┘                │
│     │                       │                             │
│     │                       │                             │
│     ▼                       ▼                             │
│ ┌────────┐           ┌──────────────────┐                │
│ │ NLTK   │           │   Phi-2 Model    │                │
│ │Library │           │   (Hugging Face) │                │
│ └────────┘           └──────────────────┘                │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## File Dependency Graph

```
                    ┌──────────────┐
                    │  chatbot.py  │
                    └──────┬───────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
                ▼          ▼          ▼
         ┌──────────┐ ┌────────┐ ┌──────┐
         │  pairs   │ │  nltk  │ │  re  │
         │   .py    │ │        │ │      │
         └──────────┘ └────────┘ └──────┘


                ┌──────────────────┐
                │chatbot_model.py  │
                └────────┬─────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ transformers    │
                │  - AutoModel    │
                │  - AutoTokenizer│
                └─────────────────┘


                ┌──────────────────┐
                │test_chatbot.py   │
                └────────┬─────────┘
                         │
                ┌────────┼────────┐
                │        │        │
                ▼        ▼        ▼
         ┌──────────┐ ┌────┐ ┌──────┐
         │  pairs   │ │ re │ │random│
         │   .py    │ │    │ │      │
         └──────────┘ └────┘ └──────┘
```

---

## State Diagram - Rule-Based Chatbot

```
                    ┌─────────┐
                    │  START  │
                    └────┬────┘
                         │
                         ▼
                ┌────────────────┐
                │  Display       │
                │  Welcome       │
                └────┬───────────┘
                     │
                     ▼
            ┌────────────────────┐
            │  WAITING FOR INPUT │◄──────┐
            └────────┬───────────┘       │
                     │                   │
                     ▼                   │
            ┌────────────────────┐       │
            │  Check if "quit"   │       │
            └────────┬───────────┘       │
                     │                   │
              ┌──────┴──────┐            │
              │             │            │
          Yes │             │ No         │
              ▼             ▼            │
        ┌─────────┐  ┌──────────────┐   │
        │  EXIT   │  │  Process     │   │
        └─────────┘  │  Input       │   │
                     └──────┬───────┘   │
                            │           │
                            ▼           │
                   ┌────────────────┐   │
                   │  Pattern Match │   │
                   └────────┬───────┘   │
                            │           │
                     ┌──────┴──────┐    │
                     │             │    │
                 Match         No Match │
                     │             │    │
                     ▼             ▼    │
            ┌────────────┐  ┌──────────┐│
            │  Return    │  │  Learn   ││
            │  Response  │  │  New     ││
            └────────┬───┘  └────┬─────┘│
                     │           │      │
                     └─────┬─────┘      │
                           │            │
                           ▼            │
                   ┌────────────────┐   │
                   │  Display       │   │
                   │  Response      │   │
                   └────────┬───────┘   │
                            │           │
                            └───────────┘
```

---

## Sequence Diagram - Pattern Matching

```
User          chatbot.py      pairs.py       NLTK          Terminal
 │                │              │            │               │
 │  "hello"       │              │            │               │
 ├───────────────►│              │            │               │
 │                │              │            │               │
 │                │ lower()      │            │               │
 │                ├─────────────►│            │               │
 │                │              │            │               │
 │                │ tokenize()   │            │               │
 │                ├──────────────┼───────────►│               │
 │                │              │            │               │
 │                │◄─────────────┼────────────┤               │
 │                │ ["hello"]    │            │               │
 │                │              │            │               │
 │                │ get patterns │            │               │
 │                ├─────────────►│            │               │
 │                │              │            │               │
 │                │◄─────────────┤            │               │
 │                │ patterns list│            │               │
 │                │              │            │               │
 │                │ re.search()  │            │               │
 │                │ (loop)       │            │               │
 │                │              │            │               │
 │                │ match found! │            │               │
 │                │              │            │               │
 │                │ rd.choice()  │            │               │
 │                │ "Hello"      │            │               │
 │                │              │            │               │
 │                │ slow_print() │            │               │
 │                ├──────────────┼────────────┼──────────────►│
 │                │              │            │               │
 │◄───────────────┼──────────────┼────────────┼───────────────┤
 │  "KAI: Hello"  │              │            │               │
 │                │              │            │               │
```

---

## Memory Architecture

### Rule-Based Chatbot Memory

```
┌─────────────────────────────────────┐
│         RUNTIME MEMORY              │
├─────────────────────────────────────┤
│                                     │
│  pairs.pairs (List)                 │
│  ├─ [pattern1, [responses]]         │
│  ├─ [pattern2, [responses]]         │
│  └─ [pattern3, [responses]]         │
│                                     │
│  user_input (String)                │
│  user_input_tokens (List)           │
│  response (String)                  │
│                                     │
└─────────────────────────────────────┘
           │
           │ Persist on learning
           ▼
┌─────────────────────────────────────┐
│      PERSISTENT STORAGE             │
├─────────────────────────────────────┤
│                                     │
│  pairs.py (File)                    │
│  - Written when new pattern learned │
│  - Loaded on startup                │
│                                     │
└─────────────────────────────────────┘
```

### AI-Powered Chatbot Memory

```
┌─────────────────────────────────────┐
│         RUNTIME MEMORY              │
├─────────────────────────────────────┤
│                                     │
│  Model Weights (~2.5GB)             │
│  ├─ Embedding layers                │
│  ├─ Attention layers                │
│  ├─ Feed-forward layers             │
│  └─ Output layer                    │
│                                     │
│  Tokenizer Vocabulary               │
│  ├─ Token → ID mapping              │
│  └─ ID → Token mapping              │
│                                     │
│  Input Tensors (Dynamic)            │
│  Output Tensors (Dynamic)           │
│                                     │
└─────────────────────────────────────┘
           │
           │ Cached after first load
           ▼
┌─────────────────────────────────────┐
│      PERSISTENT STORAGE             │
├─────────────────────────────────────┤
│                                     │
│  ~/.cache/huggingface/              │
│  ├─ model weights                   │
│  ├─ tokenizer config                │
│  └─ model config                    │
│                                     │
└─────────────────────────────────────┘
```

---

## Processing Pipeline Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    RULE-BASED PIPELINE                      │
└─────────────────────────────────────────────────────────────┘

Input → Normalize → Tokenize → Match → Select → Display
 (1)      (2)        (3)       (4)      (5)      (6)

(1) Raw user text
(2) Lowercase conversion
(3) Word tokenization (NLTK)
(4) Regex pattern matching
(5) Random response selection
(6) Slow typing effect

Time: ~10-50ms
Memory: ~1MB


┌─────────────────────────────────────────────────────────────┐
│                   AI-POWERED PIPELINE                       │
└─────────────────────────────────────────────────────────────┘

Input → Tokenize → Tensorize → Infer → Generate → Decode → Display
 (1)      (2)        (3)       (4)      (5)       (6)      (7)

(1) Raw user text
(2) Subword tokenization
(3) Convert to PyTorch tensors
(4) Neural network forward pass
(5) Token-by-token generation
(6) Convert tokens to text
(7) Direct print

Time: ~1-5 seconds (CPU), ~100-500ms (GPU)
Memory: ~5GB
```

---

## Testing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST FRAMEWORK                           │
└─────────────────────────────────────────────────────────────┘

                test_chatbot.py
                      │
                      ▼
        ┌─────────────────────────┐
        │   test_respond()        │
        │   - Isolated function   │
        │   - No user interaction │
        │   - Returns None if     │
        │     no match            │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   run_tests()           │
        │   - Test cases list     │
        │   - Execute each test   │
        │   - Compare results     │
        │   - Report pass/fail    │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Test Results          │
        │   - ✓ PASS              │
        │   - ✗ FAIL              │
        │   - Summary statistics  │
        └─────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT SETUP                         │
└─────────────────────────────────────────────────────────────┘

    Developer Machine
    ├── Python 3.9+
    ├── pip (package manager)
    ├── Virtual environment (optional)
    │
    ├── Install dependencies
    │   ├── pip install nltk
    │   └── pip install transformers torch
    │
    ├── Download NLTK data
    │   └── nltk.download('punkt')
    │
    └── Run chatbots
        ├── python chatbot.py
        └── python chatbot_model.py


┌─────────────────────────────────────────────────────────────┐
│                   PRODUCTION SETUP                          │
└─────────────────────────────────────────────────────────────┘

    Server / Cloud Instance
    ├── Python 3.9+
    ├── requirements.txt
    │   ├── nltk>=3.8.1
    │   ├── transformers>=4.35.0
    │   └── torch>=2.0.0
    │
    ├── Model cache
    │   └── ~/.cache/huggingface/
    │       └── microsoft/phi-2 (~2.5GB)
    │
    ├── Data persistence
    │   └── pairs.py (updated dynamically)
    │
    └── Monitoring
        ├── Test suite (test_chatbot.py)
        └── Error logging
```

---

## Summary

This architecture demonstrates:

✅ **Modular Design**: Separate components for different functionalities
✅ **Two Approaches**: Rule-based and AI-powered systems
✅ **Clear Data Flow**: Input → Processing → Output
✅ **Testability**: Isolated test suite
✅ **Persistence**: File-based storage for learned patterns
✅ **Scalability**: Can add more patterns or switch models
✅ **Error Handling**: Graceful degradation on failures

The system is designed to be educational, maintainable, and extensible!
