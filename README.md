# AI-Chatbot-for-Developers

This repo contains two small Python chatbots:

1) A **rule-based chatbot** (`chatbot.py`) that matches user messages against a list of regular-expression patterns in `pairs.py`.
2) A **transformer-based chatbot** (`chatbot_model.py`) that uses Hugging Face `transformers` to generate responses from a language model.

## Project structure

- `chatbot.py`: Regex/NLTK chatbot (interactive CLI) + “slow typing” output.
- `pairs.py`: Pattern/response table used by `chatbot.py`.
- `chatbot_model.py`: Hugging Face model chatbot (interactive CLI).

## How `chatbot.py` works (rule-based)

### Main loop

`chatbot.py` runs an infinite input loop until you type `quit`:

1. Read input (`Programmer: ...`).
2. Generate a response via `respond(user_input)`.
3. Print the response via `slow_print(...)` to simulate “typing”.

### `respond(user_input)`

The core behavior is:

1. Lowercase the input for consistent matching.
2. Tokenize the input with `nltk.word_tokenize` (note: the current code does not use the tokens after tokenizing).
3. Iterate over `pairs.pairs`, where each element looks like:

   ```python
   [r"some regex pattern", ["response 1", "response 2"]]
   ```

4. Use `re.search(pattern, user_input)` to find the first matching pattern.
5. If matched, pick a random response using `random.choice(responses)`.

### “Learning” behavior (writing to `pairs.py`)

If no pattern matches, `respond` prompts:

> Bot: Sorry I didn't understand. Can you provide the answer to "..."?

It then appends a new entry into the in-memory `pairs.pairs` list and **overwrites `pairs.py` on disk** with the updated list.

Notes:

- This is a simple persistence mechanism: it stores the raw user input string as the “pattern”.
- Because it rewrites `pairs.py`, any manual formatting changes in that file may be lost.
- Pattern order matters: earlier patterns win because the loop returns on the first match.

### `slow_print(text, delay=0.07)`

Prints a string character-by-character with a short sleep between characters to simulate slow typing.

## How `chatbot_model.py` works (transformer-based)

`chatbot_model.py` wraps a Hugging Face causal language model:

- `ChatbotModel.__init__(model_id)` loads a tokenizer and model via:
  - `AutoTokenizer.from_pretrained(model_id)`
  - `AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)`
- `get_response_from_model(user_input)`:
  1. Tokenizes input into PyTorch tensors.
  2. Calls `model.generate(...)` with `max_new_tokens=50`.
  3. Decodes the generated tokens back to text.

The script runs an input loop until you type `exit` or `quit`.

## Setup

### Install dependencies

The rule-based chatbot needs NLTK; the model chatbot needs `transformers` and a PyTorch backend.

```bash
pip install nltk
pip install transformers torch
```

NLTK tokenization requires the Punkt tokenizer models:

```bash
python -c "import nltk; nltk.download('punkt')"
```

## Run

### Rule-based chatbot

```bash
python chatbot.py
```

### Model-based chatbot

```bash
python chatbot_model.py
```

The first run will download the configured model (`microsoft/phi-2`) if it is not already cached.

## Customization

- Add/edit patterns in `pairs.py` to teach the rule-based chatbot more Q&A.
- Use regex patterns (e.g. `r"hi|hello"`) to match multiple phrasings.
- Keep a backup of `pairs.py` if you plan to use the “learning” feature, since `chatbot.py` rewrites the file.
