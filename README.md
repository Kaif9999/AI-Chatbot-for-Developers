# AI Chatbot for Developers

A Python-based conversational chatbot designed to answer programming-related questions, with two implementation approaches: a rule-based pattern matching system and a transformer-based AI model.

## 📋 Overview

This project contains two chatbot implementations:

1. **Rule-Based Chatbot** (`chatbot.py`) - Uses NLTK and regex pattern matching with a self-learning capability
2. **AI Model Chatbot** (`chatbot_model.py`) - Uses Microsoft's Phi-2 transformer model for natural language understanding

## 🚀 Features

### Rule-Based Chatbot (`chatbot.py`)
- **Pattern Matching**: Uses regular expressions to match user queries
- **Self-Learning**: Learns from user interactions by storing new question-answer pairs
- **Slow Typing Effect**: Simulates human-like typing for responses
- **Persistent Storage**: Saves learned patterns to `pairs.py` for future sessions
- **Python Programming Focus**: Pre-configured with Python programming Q&A pairs

### AI Model Chatbot (`chatbot_model.py`)
- **Transformer-Based**: Powered by Microsoft Phi-2 model
- **Natural Language Understanding**: Handles complex conversational queries
- **Error Handling**: Graceful error management for model processing
- **Token Management**: Configurable input/output token limits

## 📦 Installation

### Prerequisites
- Python 3.8, 3.9, or 3.10
- pip package manager

### Dependencies

Install required packages:

```bash
pip install nltk transformers torch
```

For NLTK, you'll also need to download the tokenizer data:

```python
import nltk
nltk.download('punkt')
```

## 🎯 Usage

### Running the Rule-Based Chatbot

```bash
python chatbot.py
```

**Interaction Example:**
```
Welcome to the Python Chatbot for Programmers!
Ask me any questions about Python programming language.
Enter 'quit' to exit the chatbot.

Programmer: what is python?
KAI: Python is a high-level, interpreted, general-purpose programming language.

Programmer: quit
Chat ended.
```

### Running the AI Model Chatbot

```bash
python chatbot_model.py
```

**Interaction Example:**
```
User: Hello, how are you?
Bot: [AI-generated response]

User: exit
Goodbye!
```

## 📁 Project Structure

```
.
├── chatbot.py              # Rule-based chatbot with pattern matching
├── chatbot_model.py        # Transformer-based AI chatbot
├── pairs.py                # Pattern-response pairs database
├── README.md               # Project documentation
├── .github/
│   └── workflows/
│       └── python-package.yml  # CI/CD pipeline configuration
└── .git/                   # Git repository
```

## 🔧 Core Components

### 1. `chatbot.py` - Rule-Based Implementation

**Key Functions:**

- **`respond(user_input)`**: 
  - Converts input to lowercase
  - Tokenizes the input using NLTK
  - Searches for matching patterns in the pairs database
  - Returns a random response from matched patterns
  - If no match found, prompts user to teach the bot and saves the new pair

- **`slow_print(text, delay=0.07)`**:
  - Prints text character by character with a delay
  - Creates a typing effect for more natural interaction

**Self-Learning Mechanism:**
When the bot doesn't understand a query, it:
1. Asks the user for the correct answer
2. Appends the new pattern-response pair to the database
3. Writes the updated pairs to `pairs.py`
4. Uses the new knowledge in future conversations

### 2. `chatbot_model.py` - AI Model Implementation

**Key Components:**

- **`ChatbotModel` Class**:
  - `__init__(model_id)`: Initializes tokenizer and model
  - `get_response_from_model(user_input)`: Generates AI responses
  - `handle_user_input(user_input)`: Processes user queries

**Model Configuration:**
- Model: `microsoft/phi-2`
- Max input length: 128 tokens
- Max new tokens: 50
- Truncation: Enabled

### 3. `pairs.py` - Knowledge Database

Contains regex patterns and corresponding responses for:
- Greetings and introductions
- Python programming concepts (tuples, dictionaries, functions)
- Object-oriented programming (inheritance)
- Data structures (lists vs tuples)
- Recursive functions
- Bot information and metadata

## 🧪 Testing

The project includes GitHub Actions CI/CD pipeline that:
- Tests on Python 3.8, 3.9, and 3.10
- Runs flake8 linting
- Executes pytest tests
- Triggers on push/pull requests to main branch

Run tests locally:
```bash
pytest
```

Run linting:
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 🎨 Customization

### Adding New Patterns (Rule-Based Bot)

Edit `pairs.py` and add new pattern-response pairs:

```python
[
    r"your regex pattern here",
    ["Response 1", "Response 2", "Response 3"]
]
```

### Changing the AI Model

Modify the `model_id` in `chatbot_model.py`:

```python
model_id = "your-preferred-model"  # e.g., "gpt2", "facebook/opt-350m"
```

## 🛠️ Technical Details

### Pattern Matching
- Uses Python's `re` module for regex matching
- Case-insensitive matching (converts input to lowercase)
- Supports capture groups with `%l` placeholder

### Tokenization
- NLTK's `word_tokenize` for text processing
- Transformers' `AutoTokenizer` for AI model input

### Response Generation
- Random selection from multiple possible responses
- AI model uses causal language modeling for generation

## 🚦 Exit Commands

**Rule-Based Bot**: `quit`

**AI Model Bot**: `exit` or `quit`

## ⚠️ Known Limitations

1. **Rule-Based Bot**:
   - Limited to predefined patterns
   - Requires exact or close pattern matches
   - Self-learning requires manual user input

2. **AI Model Bot**:
   - Requires significant computational resources
   - First run downloads the model (~5GB for Phi-2)
   - Response quality depends on model capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Developer

Developed by Kaif

## 🔮 Future Enhancements

- [ ] Add conversation history tracking
- [ ] Implement context-aware responses
- [ ] Add multi-language support
- [ ] Create web interface
- [ ] Add voice interaction capabilities
- [ ] Implement sentiment analysis
- [ ] Add database backend for scalable storage
- [ ] Create REST API endpoints

## 📚 Resources

- [NLTK Documentation](https://www.nltk.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [Microsoft Phi-2 Model](https://huggingface.co/microsoft/phi-2)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)

---

**Note**: This chatbot is designed for educational purposes and demonstrates both traditional NLP techniques and modern transformer-based approaches to conversational AI.
