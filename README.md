# AI Chatbot for Developers

A Python-based chatbot project with two implementations: a rule-based chatbot using NLTK and an AI-powered chatbot using transformer models.

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

## 🔍 Overview

This project contains two chatbot implementations designed to answer Python programming questions:

1. **Rule-Based Chatbot** (`chatbot.py`) - Uses pattern matching with regular expressions
2. **AI-Powered Chatbot** (`chatbot_model.py`) - Uses Microsoft's Phi-2 transformer model

## 📁 Project Structure

```
AI-Chatbot-for-Developers/
├── chatbot.py              # Rule-based chatbot implementation
├── chatbot_model.py        # AI-powered chatbot using Phi-2 model
├── pairs.py                # Predefined question-answer patterns
├── README.md               # Project documentation
└── .github/
    └── workflows/
        └── python-package.yml  # CI/CD workflow
```

## ✨ Features

### Rule-Based Chatbot (chatbot.py)
- ✅ Pattern matching using regular expressions
- ✅ Predefined responses for common Python questions
- ✅ Learning capability - adds new Q&A pairs when it doesn't understand
- ✅ Slow typing effect for human-like responses
- ✅ Case-insensitive input handling
- ✅ Persistent learning (saves to pairs.py)

### AI-Powered Chatbot (chatbot_model.py)
- ✅ Uses Microsoft Phi-2 transformer model
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Handles complex queries
- ✅ Error handling for model failures

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

For **Rule-Based Chatbot**:
```bash
pip install nltk
```

For **AI-Powered Chatbot**:
```bash
pip install transformers torch
```

### Download NLTK Data
```python
import nltk
nltk.download('punkt')
```

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
User: What is a list in Python?
Bot: A list in Python is a mutable, ordered collection...

User: exit
Goodbye!
```

## 📖 Code Explanation

### 1. chatbot.py - Rule-Based Chatbot

#### Import Modules
```python
import nltk
import re
import random as rd
import pairs  # user defined module
import time   # used to provide slow_typing
from nltk.chat.util import Chat, reflections
```

**Module Purposes:**
- `nltk` - Natural Language Toolkit for text processing
- `re` - Regular expressions for pattern matching
- `random` - Generates random responses from multiple options
- `pairs` - User-defined module containing Q&A patterns
- `time` - Creates slow typing effect
- `Chat, reflections` - NLTK utilities for chatbot functionality

#### Core Function: respond()
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

**How it works:**
1. **Standardization**: Converts input to lowercase for consistent matching
2. **Tokenization**: Breaks input into individual words using `nltk.word_tokenize()`
3. **Pattern Matching**: Iterates through predefined patterns in `pairs.py`
4. **Response Selection**: If pattern matches, randomly selects a response
5. **Learning Mode**: If no match found:
   - Asks user for the correct answer
   - Appends new pattern-response pair to `pairs.pairs`
   - Saves updated pairs to `pairs.py` file
   - Returns the user-provided answer

#### Slow Typing Effect: slow_print()
```python
def slow_print(text, delay=0.07):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')
```

**Purpose**: Creates a human-like typing effect by printing characters one at a time with a 0.07-second delay.

#### Main Chatbot Loop
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

**Flow:**
1. Displays welcome message and instructions
2. Enters infinite loop for continuous conversation
3. Takes user input with "Programmer: " prompt
4. Checks for 'quit' command to exit
5. Processes input through `respond()` function
6. Displays response with slow typing effect
7. Repeats until user quits

### 2. chatbot_model.py - AI-Powered Chatbot

#### ChatbotModel Class
```python
class ChatbotModel:
    def __init__(self, model_id):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
```

**Initialization:**
- Loads Microsoft Phi-2 model (`microsoft/phi-2`)
- Initializes tokenizer for text encoding/decoding
- Loads causal language model for text generation

#### Response Generation
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
1. **Tokenization**: Converts text to model-readable format (max 128 tokens)
2. **Generation**: Model generates up to 50 new tokens
3. **Decoding**: Converts tokens back to human-readable text
4. **Error Handling**: Returns error message if processing fails

#### User Interaction Loop
```python
while True:
    user_input = input("User: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
   
    response = chatbot.handle_user_input(user_input)
    print(f"Bot: {response}")
```

**Features:**
- Continuous conversation loop
- Multiple exit commands ("exit" or "quit")
- Direct response display without typing effect

### 3. pairs.py - Pattern-Response Database

Contains predefined regex patterns and corresponding responses:

```python
pairs = [
    [r"my name is (.*)", ["Hello %l, How are you today?"]],
    [r"hi|hey|hello", ["Hello", "Hey there"]],
    [r"what is python ?", ["Python is a high-level, interpreted, general-purpose programming language."]],
    # ... more patterns
]
```

**Pattern Types:**
- **Greeting patterns**: `r"hi|hey|hello"`
- **Question patterns**: `r"what is python ?"`
- **Capture groups**: `r"my name is (.*)"` - captures user's name
- **Multiple responses**: Bot randomly selects from response list

**Supported Topics:**
- Python basics (features, syntax)
- Data structures (lists, tuples, dictionaries)
- Functions and recursion
- Object-oriented programming (inheritance)
- Bot information (name, developer)

## 🔧 How It Works

### Rule-Based Chatbot Workflow
```
User Input → Lowercase Conversion → Tokenization → Pattern Matching
                                                          ↓
                                                    Match Found?
                                                    ↙         ↘
                                                  Yes         No
                                                   ↓           ↓
                                          Random Response   Ask User
                                                   ↓           ↓
                                          Display Response  Learn & Save
```

### AI-Powered Chatbot Workflow
```
User Input → Tokenization → Model Processing → Token Generation
                                                      ↓
                                              Decode to Text
                                                      ↓
                                              Display Response
```

## 🎯 Key Differences

| Feature | Rule-Based (chatbot.py) | AI-Powered (chatbot_model.py) |
|---------|------------------------|-------------------------------|
| **Approach** | Pattern matching | Neural network |
| **Learning** | Manual (user teaches) | Pre-trained model |
| **Flexibility** | Limited to patterns | Handles varied inputs |
| **Setup** | Lightweight | Requires model download |
| **Response Time** | Instant | Slower (model inference) |
| **Accuracy** | Exact matches only | Context-aware |
| **Dependencies** | NLTK only | Transformers + PyTorch |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add more patterns** to `pairs.py` for better coverage
2. **Improve response quality** with more varied answers
3. **Enhance error handling** in both implementations
4. **Add new features** like conversation history or sentiment analysis
5. **Optimize model performance** in `chatbot_model.py`

## 📝 License

This project is open-source and available for educational purposes.

## 👨‍💻 Developer

Developed by **Kaif**

## 🐛 Known Issues

- Rule-based chatbot overwrites `pairs.py` when learning (formatting may change)
- AI model requires significant memory (Phi-2 is ~2.7GB)
- No conversation history tracking
- Learning feature in rule-based chatbot requires manual input

## 🔮 Future Enhancements

- [ ] Add conversation context memory
- [ ] Implement database storage for learned patterns
- [ ] Create web interface using Flask/FastAPI
- [ ] Add multi-language support
- [ ] Implement sentiment analysis
- [ ] Add voice input/output capabilities
- [ ] Create hybrid model combining both approaches

---

**Note**: This chatbot is designed for educational purposes to demonstrate different chatbot implementation approaches in Python.
