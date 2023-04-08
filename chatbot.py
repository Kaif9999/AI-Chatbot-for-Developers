import nltk
import re
import random as rd
import pairs #user defined module
import time  #used to provide slow_typing
from nltk.chat.util import Chat, reflections

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
    #return "Sorry I didn't understand, can you ask a different question?"

def slow_print(text, delay=0.07):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')
    
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