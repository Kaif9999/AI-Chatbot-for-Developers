# AI-Chatbot-for-Developers

A Python-based chatbot project featuring two different implementations: a rule-based chatbot using NLTK and regular expressions, and an AI-powered chatbot using transformer models.

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Code Documentation](#code-documentation)
  - [chatbot.py - Rule-Based Chatbot](#chatbotpy---rule-based-chatbot)
  - [chatbot_model.py - AI-Powered Chatbot](#chatbot_modelpy---ai-powered-chatbot)
  - [pairs.py - Pattern-Response Database](#pairspy---pattern-response-database)
- [How It Works](#how-it-works)
- [Extending the Chatbot](#extending-the-chatbot)
- [Contributing](#contributing)

---

## 🎯 Overview

This project contains two chatbot implementations designed for developers and programmers:

1. **Rule-Based Chatbot** (`chatbot.py`): Uses pattern matching with regular expressions and NLTK for natural language processing. Features a learning mechanism that allows it to adapt to new questions.

2. **AI-Powered Chatbot** (`chatbot_model.py`): Leverages the Microsoft Phi-2 transformer model for more sophisticated conversational AI capabilities.

---

## 📁 Project Structure

```
AI-Chatbot-for-Developers/
├── chatbot.py           # Rule-based chatbot with NLTK
├── chatbot_model.py     # AI-powered chatbot with transformers
├── pairs.py             # Pattern-response pairs database
├── test_chatbot.py      # Test suite for chatbot functionality
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore patterns
└── README.md            # Project documentation
```

---

## ✨ Features

### Rule-Based Chatbot (chatbot.py)
- ✅ Pattern matching using regular expressions
- ✅ Natural language tokenization with NLTK
- ✅ Random response selection for variety
- ✅ Self-learning capability (adds new Q&A pairs)
- ✅ Slow typing effect for human-like interaction
- ✅ Python programming knowledge base

### AI-Powered Chatbot (chatbot_model.py)
- ✅ Uses Microsoft Phi-2 transformer model
- ✅ Advanced natural language understanding
- ✅ Context-aware responses
- ✅ Error handling and graceful degradation
- ✅ Token-based text generation

---

## 🚀 Installation

### Prerequisites
```bash
# Python 3.7 or higher required
python --version
```

### Install Dependencies

**Quick Install (All Dependencies):**
```bash
pip install -r requirements.txt
```

**Or Install Individually:**

**For Rule-Based Chatbot:**
```bash
pip install nltk
```

**For AI-Powered Chatbot:**
```bash
pip install transformers torch
```

### Download NLTK Data
```python
import nltk
nltk.download('punkt')
```

### Run Tests
```bash
# Test the rule-based chatbot functionality
python test_chatbot.py
```

---

## 💻 Usage

### Running the Rule-Based Chatbot
```bash
python chatbot.py
```

**Example Interaction:**
```
Welcome to the Python Chatbot for Programmers!
Ask me any questions about Python programming language.
Enter 'quit' to exit the chatbot.

Programmer: hello
KAI: Hey there

Programmer: what is python?
KAI: Python is a high-level, interpreted, general-purpose programming language.

Programmer: quit
Chat ended.
```

### Running the AI-Powered Chatbot
```bash
python chatbot_model.py
```

**Example Interaction:**
```
User: What is inheritance in Python?
Bot: [AI-generated response based on context]

User: exit
Goodbye!
```

---

## 📚 Code Documentation

### chatbot.py - Rule-Based Chatbot

#### **1. Module Imports**
```python
import nltk
import re
import random as rd
import pairs  # user defined module
import time   # used to provide slow_typing
from nltk.chat.util import Chat, reflections
```

**Dependencies:**
- **nltk**: Natural Language Toolkit for text processing and tokenization
- **re**: Regular expression operations for pattern matching
- **random**: Random response selection from multiple options
- **pairs**: Custom module containing pattern-response pairs
- **time**: Provides delay functionality for typing effect
- **Chat, reflections**: NLTK utilities for chatbot functionality

---

#### **2. Core Functions**

##### `respond(user_input)` - Main Response Logic

```python
def respond(user_input):
    user_input = user_input.lower()
    user_input_tokens = nltk.word_tokenize(user_input)
    
    for pattern, responses in pairs.pairs:         
        match = re.search(pattern, user_input)
        if match:
            return rd.choice(responses)
        
    new_question = input("Bot: Sorry I didn't understand. Can you provide the answer to \"" + user_input + "\"?")
    pairs.pairs.append([user_input, [new_question]])
    with open("pairs.py", "w") as f:
        f.write('pairs = ' + str(pairs.pairs))
    return new_question
```

**Function Flow:**
1. **Normalization**: Converts user input to lowercase for case-insensitive matching
2. **Tokenization**: Breaks input into individual words using `nltk.word_tokenize()`
3. **Pattern Matching**: Iterates through predefined patterns in `pairs.pairs`
4. **Response Selection**: If match found, randomly selects a response using `rd.choice()`
5. **Learning Mechanism**: If no match found:
   - Prompts user to provide the answer
   - Appends new pattern-response pair to `pairs.pairs`
   - Persists the updated pairs to `pairs.py` file
   - Returns the user-provided answer

**Key Features:**
- Self-learning capability through dynamic pair addition
- Persistent storage of learned responses
- Random response variation for natural conversation

---

##### `slow_print(text, delay=0.07)` - Typing Effect

```python
def slow_print(text, delay=0.07):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')
```

**Parameters:**
- `text` (str): The string to be printed
- `delay` (float): Time delay between characters (default: 0.07 seconds)

**Functionality:**
- Iterates through each character in the text
- Prints character without newline (`end=''`)
- Flushes output buffer immediately (`flush=True`)
- Introduces delay using `time.sleep()`
- Adds newline after complete text

**Purpose:** Creates a human-like typing effect for more engaging user experience

---

#### **3. Main Program Loop**

```python
print("Welcome to the Python Chatbot for Programmers!")
print("Ask me any questions about Python programming language.")
print("Enter 'quit' to exit the chatbot.")

while True:
    user_input = input("Programmer: ")
    if user_input.lower() == 'quit':
        break
    response = respond(user_input)
    slow_print("KAI: " + response, delay=0.07)

print("Chat ended.")
```

**Execution Flow:**
1. Displays welcome message and instructions
2. Enters infinite loop for continuous interaction
3. Prompts user for input with "Programmer: " prefix
4. Checks for exit command ('quit')
5. Processes input through `respond()` function
6. Displays response with typing effect using `slow_print()`
7. Exits gracefully when user types 'quit'

---

### chatbot_model.py - AI-Powered Chatbot

#### **1. Class Definition**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

class ChatbotModel:
    def __init__(self, model_id):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
```

**Components:**
- **AutoTokenizer**: Converts text to tokens that the model can understand
- **AutoModelForCausalLM**: Causal language model for text generation
- **model_id**: Identifier for the pre-trained model (Microsoft Phi-2)

**Initialization:**
- Downloads and loads the tokenizer from Hugging Face
- Downloads and loads the model weights
- `trust_remote_code=True`: Allows execution of custom model code

---

#### **2. Response Generation**

##### `get_response_from_model(user_input)` - Model Inference

```python
def get_response_from_model(self, user_input):
    try:
        inputs = self.tokenizer(user_input, return_tensors="pt", max_length=128, truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=50)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error processing user input: {str(e)}"
```

**Process:**
1. **Tokenization**: 
   - Converts input text to PyTorch tensors
   - Limits input to 128 tokens with truncation
2. **Generation**:
   - Generates up to 50 new tokens
   - Uses model's learned patterns for response
3. **Decoding**:
   - Converts token IDs back to readable text
   - Removes special tokens (padding, EOS, etc.)
4. **Error Handling**:
   - Catches exceptions during processing
   - Returns user-friendly error message

---

##### `handle_user_input(user_input)` - Input Handler

```python
def handle_user_input(self, user_input):
    model_response = self.get_response_from_model(user_input)
    return model_response
```

**Purpose:** Wrapper function for processing user input through the model

---

#### **3. Model Initialization and Loop**

```python
model_id = "microsoft/phi-2"
chatbot = ChatbotModel(model_id)

while True:
    user_input = input("User: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
   
    response = chatbot.handle_user_input(user_input)
    print(f"Bot: {response}")
```

**Configuration:**
- Uses Microsoft Phi-2 model (2.7B parameters)
- Supports multiple exit commands
- Simple input-output loop without typing effect

---

### pairs.py - Pattern-Response Database

#### **Structure**

```python
pairs = [
    [r"pattern", ["response1", "response2", ...]],
    ...
]
```

**Format:**
- List of pattern-response pairs
- Each pair contains:
  - **Pattern**: Regular expression string
  - **Responses**: List of possible responses

---

#### **Sample Patterns**

**1. Greeting Patterns:**
```python
[r"hi|hey|hello", ["Hello", "Hey there"]]
```
- Matches: "hi", "hey", "hello"
- Responses: Random selection from list

**2. Name Extraction:**
```python
[r"my name is (.*)", ["Hello %l, How are you today?"]]
```
- Captures name using `(.*)`
- Uses `%l` placeholder for captured group

**3. Python Knowledge:**
```python
[r"what is python ?", 
 ["Python is a high-level, interpreted, general-purpose programming language."]]
```

**4. Exit Commands:**
```python
[r"quit|sleep|bye bot|bye|I'm bored|exit",
 ["Bye bye, take care. See you soon :) "]]
```

---

#### **Knowledge Base Topics**

The `pairs.py` file includes responses for:
- ✅ Python basics and features
- ✅ Data structures (tuples, dictionaries, lists)
- ✅ Functions and recursion
- ✅ Object-oriented programming (inheritance)
- ✅ Greetings and social interactions
- ✅ Bot identity and developer information

---

## 🔧 How It Works

### Rule-Based Chatbot Flow

```
User Input
    ↓
Lowercase Conversion
    ↓
Tokenization (NLTK)
    ↓
Pattern Matching (Regex)
    ↓
Match Found? ──Yes──→ Random Response Selection
    ↓                        ↓
    No                  Slow Print Output
    ↓
Ask User for Answer
    ↓
Store New Pair
    ↓
Update pairs.py
    ↓
Return User Answer
```

### AI-Powered Chatbot Flow

```
User Input
    ↓
Tokenization (AutoTokenizer)
    ↓
Convert to Tensors
    ↓
Model Generation (Phi-2)
    ↓
Token Decoding
    ↓
Text Output
```

---

## 🛠️ Extending the Chatbot

### Adding New Patterns (Rule-Based)

**Method 1: Manual Addition**
Edit `pairs.py` and add new pattern-response pairs:

```python
pairs = [
    # ... existing pairs ...
    [
        r"what is machine learning ?",
        ["Machine learning is a subset of AI that enables systems to learn from data."]
    ],
]
```

**Method 2: Interactive Learning**
Simply ask the chatbot a question it doesn't know:
```
Programmer: What is Django?
Bot: Sorry I didn't understand. Can you provide the answer to "what is django?"
[Your answer will be saved automatically]
```

### Customizing the AI Model

Change the model in `chatbot_model.py`:

```python
# Options:
model_id = "microsoft/phi-2"           # 2.7B parameters
model_id = "gpt2"                      # Smaller, faster
model_id = "facebook/opt-1.3b"         # Alternative model
```

### Adjusting Generation Parameters

```python
outputs = self.model.generate(
    **inputs, 
    max_new_tokens=100,      # Longer responses
    temperature=0.7,         # Creativity (0.0-1.0)
    top_p=0.9,              # Nucleus sampling
    do_sample=True          # Enable sampling
)
```

---

## 🧪 Testing

The project includes a test suite to verify chatbot functionality.

### Running Tests

```bash
python test_chatbot.py
```

### Test Coverage

The test suite (`test_chatbot.py`) validates:
- ✅ Greeting patterns (hi, hello, hey)
- ✅ Python concept questions (tuples, dictionaries, functions)
- ✅ Pattern matching accuracy
- ✅ Response generation
- ✅ Regular expression matching

### Sample Test Output

```
============================================================
Running Chatbot Tests
============================================================
✓ PASS: 'hello'
  Response: Hello

✓ PASS: 'what is python?'
  Response: Python is a high-level, interpreted, general-purpose programming language.

============================================================
Test Results: 7 passed, 0 failed
============================================================
```

### Adding New Tests

Edit `test_chatbot.py` and add test cases to the `test_cases` list:

```python
test_cases = [
    ("your question", ["expected response 1", "expected response 2"]),
    # Add more test cases here
]
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- Add more Python programming Q&A pairs
- Implement conversation history
- Add sentiment analysis
- Create a GUI interface
- Improve error handling
- Add multi-language support
- Implement context awareness
- Expand test coverage

---

## 📝 Technical Notes

### Regular Expression Patterns
- Use `r"pattern"` for raw strings to avoid escape issues
- `(.*)` captures any text for dynamic responses
- `|` acts as OR operator for multiple matches
- Patterns are case-insensitive (input converted to lowercase)

### Model Considerations
- **Phi-2** requires ~5GB RAM for inference
- First run downloads model weights (~2.5GB)
- GPU acceleration recommended for faster responses
- CPU inference is supported but slower

### File Persistence
- `pairs.py` is dynamically updated during runtime
- Changes persist across sessions
- Backup recommended before extensive testing

---

## 🐛 Troubleshooting

**Issue: NLTK tokenization error**
```bash
# Solution: Download required NLTK data
python -c "import nltk; nltk.download('punkt')"
```

**Issue: Model download fails**
```bash
# Solution: Check internet connection and disk space
# Ensure ~5GB free space for model weights
```

**Issue: Slow response times**
```bash
# Solution: Use smaller model or enable GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 📄 License

This project is open-source and available for educational purposes.

---

## 👨‍💻 Developer

Developed by Kaif

---

**Happy Coding! 🚀**




