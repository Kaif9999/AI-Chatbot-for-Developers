# AI Chatbot for Developers

A Python-based chatbot project with two implementations: a rule-based chatbot using NLTK and an AI-powered chatbot using transformer models.

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Code Explanation](#code-explanation)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

## 🔍 Overview

This project contains two chatbot implementations designed to answer Python programming questions:

1. **Rule-Based Chatbot** (`chatbot.py`) - Uses pattern matching with regular expressions
2. **AI-Powered Chatbot** (`chatbot_model.py`) - Uses GPT-2 transformer model

## 📁 Project Structure

```
AI-Chatbot-for-Developers/
├── chatbot.py              # Rule-based chatbot implementation
├── chatbot_model.py        # AI-powered chatbot using GPT-2 model
├── pairs.py                # Predefined question-answer patterns
├── tests/
│   ├── test_chatbot.py
│   └── test_chatbot_model.py
├── pytest.ini              # Pytest configuration
├── README.md               # Project documentation
└── .github/
    └── workflows/
        └── python-package.yml  # CI/CD workflow
```

## ✨ Features

### Rule-Based Chatbot (chatbot.py)
- ✅ Pattern matching using regular expressions
- ✅ Predefined responses for common Python questions
- ✅ Case-insensitive input handling

### AI-Powered Chatbot (chatbot_model.py)
- ✅ Uses GPT-2 transformer model
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Handles complex queries
- ✅ Error handling for model failures

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install nltk transformers torch pytest
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
Goodbye!
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

## 🧪 Testing
To run the tests, use the following command:
```bash
pytest
```

## 📖 Code Explanation

### 1. chatbot.py - Rule-Based Chatbot

#### Import Modules
```python
import nltk
from nltk.chat.util import Chat, reflections
import pairs
```

**Module Purposes:**
- `nltk` - Natural Language Toolkit for text processing
- `Chat, reflections` - NLTK utilities for chatbot functionality
- `pairs` - User-defined module containing Q&A patterns

#### Core Function: chatbot()
```python
def chatbot():
    """
    This function is the main function for the chatbot.
    """
    print("Welcome to the Python Chatbot for Programmers!")
    print("Ask me any questions about Python programming language.")
    print("Enter 'quit' to exit the chatbot.")
    chat = Chat(pairs.pairs, reflections)
    while True:
        user_input = input("Programmer: ")
        if user_input.lower() == 'quit':
            break
        elif user_input:
            response = chat.respond(user_input)
            print("KAI:", response)
    print("Goodbye!")
```

**How it works:**
1. **Initialization**: Creates a `Chat` object with the patterns from `pairs.py` and reflections.
2. **User Input**: Takes user input in a loop.
3. **Response Generation**: Uses the `chat.respond()` method to find a matching pattern and return a response.
4. **Exit**: Exits the loop when the user types "quit".

### 2. chatbot_model.py - AI-Powered Chatbot

#### ChatbotModel Class
```python
class ChatbotModel:
    def __init__(self, model_id, max_length=128, max_new_tokens=50):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
```

**Initialization:**
- Loads GPT-2 model (`gpt2`)
- Initializes tokenizer for text encoding/decoding
- Loads causal language model for text generation

#### Response Generation
```python
def get_response_from_model(self, user_input):
    try:
        inputs = self.tokenizer(user_input, return_tensors="pt", max_length=self.max_length, truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    except (ValueError, RuntimeError) as e:
        return f"Error processing user input: {str(e)}"
```

**Process:**
1. **Tokenization**: Converts text to model-readable format
2. **Generation**: Model generates new tokens based on the input
3. **Decoding**: Converts tokens back to human-readable text
4. **Error Handling**: Returns error message if processing fails

#### User Interaction Loop
```python
def main():
    # Model ID
    model_id = "gpt2"
    chatbot = ChatbotModel(model_id)

    # User input loop
    while True:
        user_input = input("User: ")
        
        # Exit the loop if the user wants to quit
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
    
        response = chatbot.handle_user_input(user_input)
        print(f"Bot: {response}")
```

**Features:**
- Continuous conversation loop
- Multiple exit commands ("exit" or "quit")
- Direct response display

### 3. pairs.py - Pattern-Response Database

Contains predefined regex patterns and corresponding responses for the rule-based chatbot.

## 🔧 How It Works

### Rule-Based Chatbot Workflow
```
User Input → Pattern Matching → Response Selection → Display Response
```

### AI-Powered Chatbot Workflow
```
User Input → Tokenization → Model Processing → Token Generation → Decode to Text → Display Response
```

## 🎯 Key Differences

| Feature | Rule-Based (chatbot.py) | AI-Powered (chatbot_model.py) |
|---------|------------------------|-------------------------------|
| **Approach** | Pattern matching | Neural network |
| **Learning** | None | Pre-trained model |
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

- AI model requires significant memory (GPT-2 is smaller than Phi-2, but still requires resources)
- No conversation history tracking

## 🔮 Future Enhancements

- [ ] Add conversation context memory
- [ ] Implement database storage for patterns
- [ ] Create web interface using Flask/FastAPI
- [ ] Add multi-language support
- [ ] Implement sentiment analysis
- [ ] Add voice input/output capabilities
- [ ] Create hybrid model combining both approaches

---

**Note**: This chatbot is designed for educational purposes to demonstrate different chatbot implementation approaches in Python.
