# AI Chatbot for Developers

This repo contains two small, terminal-based chatbot implementations:

- `chatbot.py`: a lightweight rule-based chatbot using regex patterns from `pairs.py`. If it can’t match an input, it asks you for the “right” answer and persists it back into `pairs.py`.
- `chatbot_model.py`: a Hugging Face Transformers example that loads a causal language model (default: `microsoft/phi-2`) and generates responses.

## Project Structure

- `chatbot.py`: main rule-based chatbot loop + slow typing output.
- `pairs.py`: list of `[pattern, responses]` pairs used by `chatbot.py`.
- `chatbot_model.py`: model-backed chatbot using `transformers`.

## How the Rule-Based Chatbot Works (`chatbot.py`)

1. Normalizes input (`lower()`).
2. Iterates through `pairs.pairs` and runs `re.search(pattern, user_input)`.
3. On a match, replies with a random response from that pattern’s response list.
4. On no match, prompts you to provide an answer and appends a new entry to `pairs.pairs`.
5. Writes the updated list back into `pairs.py` (the file is rewritten).

Note: `nltk.word_tokenize()` is called but its tokens are not used in the current implementation.

## Setup

### Python

Use Python 3.8+.

Install dependencies:

```bash
pip install nltk transformers torch
```

Download NLTK tokenizers (needed by `chatbot.py`):

```bash
python -c "import nltk; nltk.download('punkt')"
```

## Usage

### Run the rule-based chatbot

```bash
python chatbot.py
```

- Type messages at the `Programmer:` prompt.
- Type `quit` to exit.

### Run the model-based chatbot

```bash
python chatbot_model.py
```

- Type `exit` or `quit` to stop.
- The first run downloads the model weights and may take time and memory.

## Customizing Responses (`pairs.py`)

`pairs.py` defines a list like:

```python
pairs = [
  [r"hi|hey|hello", ["Hello", "Hey there"]],
]
```

- Patterns are Python regular expressions.
- Responses are a list of strings; one is chosen randomly.

## Notes / Caveats

- `chatbot.py` mutates and rewrites `pairs.py` when it learns a new answer.
- `chatbot_model.py` is a minimal demo and does not maintain conversation history; it generates from the latest prompt only.
