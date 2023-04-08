# AI-Chatbot-for-Developers
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




