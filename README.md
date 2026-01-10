# AI-Chatbot-for-Developers

This repo contains two simple chatbot implementations:

- `chatbot.py`: a rule-based chatbot that matches user text against regex patterns in `pairs.py`.
- `chatbot_model.py`: a model-based chatbot that uses Hugging Face `transformers` (`microsoft/phi-2`).

## File overview

- `chatbot.py`
  - Reads user input in a loop.
  - Calls `respond(user_input)` to pick a response.
  - Prints responses with a “slow typing” effect via `slow_print()`.
- `pairs.py`
  - A list named `pairs` containing `[pattern, responses]` entries.
  - `pattern` is a regex string.
  - `responses` is a list of strings; one is chosen randomly.
- `chatbot_model.py`
  - Defines a `ChatbotModel` wrapper around `AutoTokenizer` and `AutoModelForCausalLM`.
  - Generates responses with `model.generate()`.

## Rule-based chatbot (`chatbot.py`) explained

### Imports

`chatbot.py` uses:

- `nltk`: used for `nltk.word_tokenize()`.
- `re`: regex matching against patterns.
- `random` (as `rd`): random choice of a response.
- `pairs`: local module containing the pattern/response table.
- `time`: delays for the slow-typing output.

Note: `Chat` and `reflections` are imported from `nltk.chat.util` but are not used in the current implementation.

### `respond(user_input)`

High-level flow:

1. Normalizes input with `user_input = user_input.lower()`.
2. Tokenizes with `nltk.word_tokenize(user_input)` (the resulting `user_input_tokens` variable is currently unused).
3. Iterates through `pairs.pairs`:

   - For each `(pattern, responses)`, checks `re.search(pattern, user_input)`.
   - On the first match, returns `rd.choice(responses)`.

4. If nothing matches, it enters a simple “learning” mode:

   - Prompts the user to provide an answer.
   - Appends a new entry to `pairs.pairs`.
   - Writes the updated list back into `pairs.py`.

Important behavior details:

- Patterns in `pairs.py` are regular expressions, not plain strings.
- The “learning” path appends the raw `user_input` as a new pattern, which may behave unexpectedly if it contains regex metacharacters.

### `slow_print(text, delay=0.07)`

Prints one character at a time and sleeps `delay` seconds between characters to simulate typing.

### Main loop

The script prints a welcome message, then loops:

- Reads `input("Programmer: ")`
- Breaks if the user enters `quit`
- Otherwise prints `KAI: <response>`

## Model-based chatbot (`chatbot_model.py`) explained

`chatbot_model.py` defines a `ChatbotModel` class:

- `__init__(model_id)`
  - Loads a tokenizer with `AutoTokenizer.from_pretrained(model_id)`.
  - Loads a causal LM with `AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)`.
- `get_response_from_model(user_input)`
  - Tokenizes the prompt (`max_length=128`, `truncation=True`).
  - Runs generation via `self.model.generate(..., max_new_tokens=50)`.
  - Decodes tokens back to text.
  - Returns an error string if anything fails.
- `handle_user_input(user_input)`
  - Currently just calls `get_response_from_model`.

The script then creates `ChatbotModel("microsoft/phi-2")` and runs an input loop until the user enters `exit` or `quit`.

## Running

### Rule-based

```bash
python chatbot.py
```

If you hit an `nltk` tokenizer error, install/download NLTK data (for example):

```bash
python -c "import nltk; nltk.download('punkt')"
```

### Model-based

```bash
python chatbot_model.py
```

This requires `transformers` and a compatible `torch` install, and will download the model on first run.
