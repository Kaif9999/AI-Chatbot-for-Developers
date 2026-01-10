from nltk.chat.util import Chat, reflections
import pairs


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


if __name__ == "__main__":
    chatbot()