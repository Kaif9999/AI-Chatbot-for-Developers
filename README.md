# AI Chatbot for Developers

A Python-based conversational chatbot designed to answer programming questions and interact with users. This project includes two implementations: a pattern-matching chatbot using NLTK and a transformer-based chatbot using the Microsoft Phi-2 model.

## Overview

This repository contains two chatbot implementations:

1. **Pattern-Matching Chatbot** (`chatbot.py`): A rule-based chatbot using regular expressions and NLTK for natural language processing
2. **AI Model-Based Chatbot** (`chatbot_model.py`): A transformer-based chatbot powered by Microsoft's Phi-2 language model

## Features

### Pattern-Matching Chatbot (`chatbot.py`)
- Pattern matching using regular expressions
- Pre-defined responses for common Python programming questions
- Learning capability - can ask users for responses to unrecognized inputs and store them
- Slow-typing effect for more natural conversation flow
- Tokenization using NLTK
- Self-modifying knowledge base stored in `pairs.py`

### AI Model-Based Chatbot (`chatbot_model.py`)
- Utilizes Microsoft Phi-2 model via HuggingFace Transformers
- Generative AI responses
- Context-aware conversations
- Error handling for robust operation

## Project Structure

```
.
├── chatbot.py           # Pattern-matching chatbot implementation
├── chatbot_model.py     # Transformer-based chatbot implementation
├── pairs.py             # Pattern-response pairs database
├── README.md            # This file
└── .github/
    └── workflows/
        └── python-package.yml  # CI/CD pipeline configuration
```

## Requirements

### For Pattern-Matching Chatbot:
- Python 3.8+
- nltk
- re (built-in)
- random (built-in)
- time (built-in)

### For AI Model-Based Chatbot:
- Python 3.8+
- transformers
- torch (PyTorch)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Chatbot-for-Developers.git
cd AI-Chatbot-for-Developers
```

2. Install dependencies:
```bash
pip install nltk transformers torch
```

3. Download NLTK data (for pattern-matching chatbot):
```python
import nltk
nltk.download('punkt')
```

## Usage

### Running the Pattern-Matching Chatbot

```bash
python chatbot.py
```

Example interaction:
```
Welcome to the Python Chatbot for Programmers!
Ask me any questions about Python programming language.
Enter 'quit' to exit the chatbot.
Programmer: what is python?
KAI: Python is a high-level, interpreted, general-purpose programming language.
Programmer: quit
Chat ended.
```

### Running the AI Model-Based Chatbot

```bash
python chatbot_model.py
```

Example interaction:
```
User: What is a function in Python?
Bot: [AI-generated response based on Phi-2 model]
User: exit
Goodbye!
```

## How It Works

### Pattern-Matching Chatbot Architecture

1. **Input Processing**: User input is converted to lowercase and tokenized using NLTK
2. **Pattern Matching**: Regular expressions in `pairs.py` are searched for matches
3. **Response Selection**: A random response is selected from matching patterns
4. **Learning Mode**: If no match is found, the chatbot asks the user for a response and stores it
5. **Output**: Response is displayed with a slow-typing effect for natural interaction

### AI Model-Based Chatbot Architecture

1. **Model Loading**: Microsoft Phi-2 model is loaded via HuggingFace Transformers
2. **Input Tokenization**: User input is tokenized with max length of 128 tokens
3. **Response Generation**: Model generates up to 50 new tokens as response
4. **Output**: Decoded response is displayed to the user

## Knowledge Base (`pairs.py`)

The pattern-matching chatbot uses a predefined set of pattern-response pairs covering:

- Greetings and basic conversation
- Python language fundamentals
- Data structures (lists, tuples, dictionaries)
- Functions and recursion
- Object-oriented programming concepts (inheritance)
- Developer information

The knowledge base is dynamically updateable - new patterns learned during conversation are automatically saved.

## CI/CD

This project includes a GitHub Actions workflow that:
- Tests on Python 3.8, 3.9, and 3.10
- Runs linting with flake8
- Executes tests with pytest
- Triggers on push/pull requests to main branch

## Key Functions

### `chatbot.py`

- **`respond(user_input)`**: Core function that processes user input and returns appropriate response
  - Tokenizes input
  - Searches for pattern matches
  - Handles learning from unknown inputs

- **`slow_print(text, delay=0.07)`**: Prints text with typing effect for natural conversation flow

### `chatbot_model.py`

- **`ChatbotModel.__init__(model_id)`**: Initializes the transformer model and tokenizer
- **`get_response_from_model(user_input)`**: Generates AI response using the language model
- **`handle_user_input(user_input)`**: Wrapper function for processing user input

## Limitations

### Pattern-Matching Chatbot
- Limited to predefined patterns and responses
- Cannot understand context beyond pattern matching
- Self-modification of `pairs.py` may cause code injection risks

### AI Model-Based Chatbot
- Requires significant computational resources
- Model download is large (several GB)
- Response quality depends on Phi-2 model capabilities

## Future Enhancements

- Implement conversation history tracking
- Add multi-turn context awareness
- Create a web interface using Flask/FastAPI
- Implement proper database for storing learned patterns
- Add sentiment analysis
- Support for multiple languages
- Fine-tune the model on programming-specific datasets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Developer

Developed by Kaif

## Acknowledgments

- Built with NLTK for natural language processing
- Powered by Microsoft Phi-2 model via HuggingFace Transformers
- Inspired by the need for developer-friendly chatbots
