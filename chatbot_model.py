from transformers import AutoModelForCausalLM, AutoTokenizer

class ChatbotModel:
    def __init__(self, model_id):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

    def get_response_from_model(self, user_input):
        try:
            inputs = self.tokenizer(user_input, return_tensors="pt", max_length=128, truncation=True)
            outputs = self.model.generate(**inputs, max_new_tokens=50)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error processing user input: {str(e)}"

    def handle_user_input(self, user_input):
        # Fetch response from the model
        model_response = self.get_response_from_model(user_input)
        return model_response

# Model ID
model_id = "microsoft/phi-2"
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
