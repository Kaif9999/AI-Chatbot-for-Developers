from transformers import AutoModelForCausalLM, AutoTokenizer


class ChatbotModel:
    def __init__(self, model_id, max_length=128, max_new_tokens=50):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.max_length = max_length
        self.max_new_tokens = max_new_tokens

    def get_response_from_model(self, user_input):
        try:
            inputs = self.tokenizer(
                user_input, return_tensors="pt",
                max_length=self.max_length, truncation=True
            )
            outputs = self.model.generate(
                **inputs, max_new_tokens=self.max_new_tokens
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except (ValueError, RuntimeError) as e:
            return f"Error processing user input: {str(e)}"

    def handle_user_input(self, user_input):
        # Fetch response from the model
        model_response = self.get_response_from_model(user_input)
        return model_response


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


if __name__ == "__main__":
    main()
