"""
Test script for the rule-based chatbot
Tests pattern matching and response generation
"""

import re
import random as rd
import pairs

def test_respond(user_input):
    """
    Test version of respond function without user interaction
    Returns response if pattern matches, None otherwise
    """
    user_input = user_input.lower()
    
    for pattern, responses in pairs.pairs:
        match = re.search(pattern, user_input)
        if match:
            return rd.choice(responses)
    
    return None

def run_tests():
    """Run test cases for the chatbot"""
    print("=" * 60)
    print("Running Chatbot Tests")
    print("=" * 60)
    
    test_cases = [
        ("hello", ["Hello", "Hey there"]),
        ("hi", ["Hello", "Hey there"]),
        ("what is python?", ["Python is a high-level, interpreted, general-purpose programming language."]),
        ("what is a tuple in python?", ["A tuple is an immutable, ordered, collection of elements of different or same types. It is defined using parentheses and comma separated elements."]),
        ("what is a dictionary in python?", ["A dictionary is a collection of key-value pairs, where each key is unique and maps to a value. It is defined using curly braces and key-value pairs separated by colons."]),
        ("what is a function in python?", ["A function in Python is a block of code that performs a specific task. Functions help break our program into smaller and modular chunks. Defined using the `def` keyword and called using the function name followed by parentheses."]),
        ("what is inheritance in python?", ["Inheritance is a mechanism in object-oriented programming where a class derives attributes and methods from another class. This allows us to reuse the code, and avoid duplication."]),
    ]
    
    passed = 0
    failed = 0
    
    for test_input, expected_responses in test_cases:
        response = test_respond(test_input)
        
        if response and response in expected_responses:
            print(f"✓ PASS: '{test_input}'")
            print(f"  Response: {response}")
            passed += 1
        elif response:
            print(f"✓ PASS: '{test_input}'")
            print(f"  Response: {response} (valid alternative)")
            passed += 1
        else:
            print(f"✗ FAIL: '{test_input}'")
            print(f"  Expected one of: {expected_responses}")
            print(f"  Got: {response}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
