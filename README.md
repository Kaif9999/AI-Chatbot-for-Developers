# AI-Chatbot-for-Developers

An intelligent chatbot system for developers with two implementations: a pattern-matching chatbot and an AI-powered transformer model chatbot.

## Project Overview

This project contains two different chatbot implementations:

1. **Pattern-Matching Chatbot** (`chatbot.py`) - A rule-based chatbot using regular expressions
2. **AI-Powered Chatbot** (`chatbot_model.py`) - A transformer-based chatbot using Microsoft Phi-2 model
3. **Knowledge Base** (`pairs.py`) - Contains pattern-response pairs for the pattern-matching chatbot

## Code Documentation

### 1. Pattern-Matching Chatbot (`chatbot.py`)

This is a rule-based chatbot that uses regular expressions to match user input with predefined patterns and provides appropriate responses.

#### Architecture

**Dependencies:**
- `nltk` - Natural Language Toolkit for text processing
- `re` - Regular expression pattern matching
- `random` - Random response selection
- `time` - Slow typing effect simulation
- `pairs` - Custom module containing pattern-response database

#### Core Functions

##### `respond(user_input)` - Main Response Handler
```python
def respond(user_input):
    user_input = user_input.lower()
    user_input_tokens = nltk.word_tokenize(user_input)

    for pattern, responses in pairs.pairs:
        match = re.search(pattern, user_input)
        if match:
            return rd.choice(responses)

    # Learning mechanism
    new_question = input("Bot: Sorry I didn't understand...")
    pairs.pairs.append([user_input, [new_question]])
    with open("pairs.py", "w") as f:
        f.write('pairs = ' + str(pairs.pairs))
    return new_question
```

**Function Flow:**
1. Converts user input to lowercase for case-insensitive matching
2. Tokenizes the input using NLTK word tokenizer
3. Iterates through pattern-response pairs from `pairs.py`
4. Uses regex to find matching patterns
5. Returns a random response from matching pattern's response list
6. If no match found, prompts user to teach the bot
7. Appends new pattern-response pair to database
8. Persists the updated pairs to `pairs.py` file

**Learning Capability:** The chatbot can learn from interactions by adding new patterns when it doesn't understand a query.

##### `slow_print(text, delay=0.07)` - Typing Animation
```python
def slow_print(text, delay=0.07):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')
```

**Purpose:** Creates a human-like typing effect by printing characters one at a time with a 70ms delay between each character.

#### Main Loop (chatbot.py:37-44)
```python
while True:
    user_input = input("Programmer: ")
    if user_input.lower() == 'quit':
        break
    response = respond(user_input)
    slow_print("KAI: " + response, delay=0.07)
```

Continuously accepts user input until 'quit' is entered, processes each input through the `respond()` function, and displays responses with the slow-typing effect.

---

### 2. AI-Powered Chatbot (`chatbot_model.py`)

This implementation uses a transformer-based language model (Microsoft Phi-2) for generating intelligent, context-aware responses.

#### Architecture

**Dependencies:**
- `transformers` - Hugging Face library for pre-trained models
  - `AutoModelForCausalLM` - Causal language model loader
  - `AutoTokenizer` - Tokenizer for text processing

#### ChatbotModel Class

##### `__init__(self, model_id)` - Constructor
```python
def __init__(self, model_id):
    self.tokenizer = AutoTokenizer.from_pretrained(model_id)
    self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
```

**Initialization Process:**
- Loads pre-trained tokenizer from Hugging Face Hub
- Loads causal language model with `trust_remote_code=True` flag
- Uses Microsoft Phi-2 model by default (`microsoft/phi-2`)

##### `get_response_from_model(self, user_input)` - Text Generation
```python
def get_response_from_model(self, user_input):
    try:
        inputs = self.tokenizer(user_input, return_tensors="pt", max_length=128, truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=50)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error processing user input: {str(e)}"
```

**Process Flow:**
1. Tokenizes user input into PyTorch tensors
2. Limits input to 128 tokens with truncation
3. Generates up to 50 new tokens as response
4. Decodes output tokens back to text
5. Handles errors gracefully with error messages

##### `handle_user_input(self, user_input)` - Main Handler
Simple wrapper that calls `get_response_from_model()` and returns the model's response.

#### Main Loop (chatbot_model.py:26-35)
```python
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    response = chatbot.handle_user_input(user_input)
    print(f"Bot: {response}")
```

Accepts user input, checks for exit commands, generates AI responses, and displays them.

---

### 3. Knowledge Base (`pairs.py`)

Contains the pattern-response database used by the pattern-matching chatbot.

#### Structure

Each entry is a list containing:
1. **Pattern** - Regular expression string
2. **Responses** - List of possible response strings

#### Example Patterns

**Greeting Pattern:**
```python
[r"hi|hey|hello", ["Hello", "Hey there"]]
```
Matches variations of greetings using OR operator (`|`)

**Capture Group Pattern:**
```python
[r"my name is (.*)", ["Hello %l, How are you today?"]]
```
Captures any text after "my name is" using `(.*)` capture group

**Python Knowledge Patterns:**
```python
[r"what is python ?", ["Python is a high-level, interpreted, general-purpose programming language."]]
```

#### Categories Covered:
- Greetings and farewells
- Identity questions (name, developer)
- Python programming concepts (tuples, dictionaries, functions, inheritance)
- Data structure comparisons
- Recursive functions

**Total Patterns:** 15+ predefined patterns covering basic conversation and Python programming topics.

---

## Key Differences Between Implementations

| Feature | Pattern-Matching (`chatbot.py`) | AI-Powered (`chatbot_model.py`) |
|---------|--------------------------------|--------------------------------|
| **Response Method** | Regex pattern matching | Transformer model generation |
| **Learning** | Adds new patterns dynamically | Pre-trained, no runtime learning |
| **Response Quality** | Fixed, predefined responses | Context-aware, generated responses |
| **Dependencies** | NLTK, regex | Transformers, PyTorch |
| **Setup** | Lightweight, fast | Requires model download (~2.7GB) |
| **Customization** | Easy to add patterns | Requires model fine-tuning |
| **User Interface** | Slow-typing effect | Instant response |

---

## How the Code Works

### Pattern-Matching Chatbot Flow
1. User enters a question
2. Input is normalized (lowercase) and tokenized
3. System searches through regex patterns in `pairs.py`
4. First matching pattern triggers random response selection
5. If no match, system asks user to teach it
6. New pattern-response pair is saved to `pairs.py`
7. Response is displayed with typing animation

### AI-Powered Chatbot Flow
1. User enters a question
2. Input is tokenized using Phi-2 tokenizer
3. Tokens are fed to the transformer model
4. Model generates contextual response (max 50 tokens)
5. Output tokens are decoded to readable text
6. Response is displayed instantly

---

## Installation and Usage

### Prerequisites
```bash
pip install nltk transformers torch
```

### Running Pattern-Matching Chatbot
```bash
python chatbot.py
```

### Running AI-Powered Chatbot
```bash
python chatbot_model.py
```

---

## Technical Implementation Details

1. Import the required Python modules:
```
import nltk
import re
import random as rd
import pairs #user defined module
import time  #used to provide slow_typing
from nltk.chat.util import Chat, reflections
```
*The **nltk module** is used for natural language processing. 

*The **re module** is used for regular expressions.

*The **random module** is used for generating random responses.

*The **pairs module** is a user-defined module that contains the pairs of patterns and responses for the chatbot.

*The **time module** is used to provide a slow typing effect.

*The **Chat and reflections** modules are imported from nltk.chat.util.

2. Define a `respond` function that takes user input and returns a response based on the provided pairs of patterns and responses.
```
def respond(user_input):
    # Convert user input to lower case for standardization
    user_input = user_input.lower()
    
    # Tokenize the user input
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
    
*The `respond` function takes a `user_input` parameter, which is the input provided by the user.

*The `user_input` is converted to lower case to standardize the input.

*The `nltk.word_tokenize` function is used to tokenize the user input into words.

*A `for` loop is used to iterate through the `pairs` list of patterns and responses.

*The `re.search` function is used to find a match between the user input and the pattern in each pair.

*If a match is found, a random response is chosen from the list of responses in the pair using the `rd.choice` function.

*If no match is found, the chatbot asks the user for a response and appends the user's response to the `pairs` list of patterns and responses.

*The updated `pairs` list is then written to a file called pairs.py.

*The function returns the user's response.

3. Define a `slow_print` function that takes a string and prints it with a delay effect.

```
def slow_print(text, delay=0.07):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')
```
*The `slow_print` function takes a `text` parameter, which is the string to be printed.

*The function also takes an optional `delay` parameter that sets the time delay between printing each character.

*A `for` loop is used to iterate through each character in the string.

*The `print` function is used to print each character with the `end=''` parameter to prevent the cursor from going to the next line.

*The `time.sleep` function is used to introduce a delay between printing each character.
*After printing all the characters, the `print` function is used to go to the next line.

4. Print the welcome message and start the chatbot loop.

```
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
*This block of code initializes and runs the chatbot application. It first welcomes the user and provides instructions on how to interact with the chatbot. It then enters into a loop where it continuously takes the user's input and passes it to the `respond(user_input)` function to get a response. It prints the response using the `slow_print(text, delay)` function to simulate the effect of a slow-typing chatbot. The loop continues until the user enters the keyword 'quit', at which point the chatbot application ends.

5. Respond Function
The `respond` function is the core of the chatbot. It takes a string input, tokenizes it, and searches for a matching regular expression pattern in the `pairs` list. If a pattern is found, a random response is returned from the corresponding list of responses. If no pattern is found, the function prompts the user to provide an answer for the given input and adds it to the `pairs` list. The function then writes the updated `pairs` list to the `pairs.py` file and returns the new question.

6. Slow Typing Function
The `slow_print` function is a helper function that prints text slowly, with a default delay of 0.07 seconds per character. This function is used to simulate a more human-like chatbot response time.

7. Chatbot Interaction Loop
The main program loop uses a `while` loop to continuously prompt the user for input until the user enters the keyword "quit". Each user input is passed to the `respond` function, and the resulting response is printed to the console using the `slow_print` function.

8. User-Defined Regular Expressions and Responses
The `pairs` list contains a set of user-defined regular expressions and their corresponding responses. These regular expressions and responses are used by the respond function to generate appropriate responses for the user's input.

The AI Chatbot project is a simple yet effective demonstration of natural language processing and regular expressions. It provides a basic level of interaction between the user and the chatbot, with the ability to learn and adapt to new user inputs. By modifying the `pairs` list and adding new regular expressions and responses, the chatbot can be easily extended to handle a wider range of user inputs and provide more intelligent responses.




