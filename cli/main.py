"""
Spanish Learning Chatbot - Main Entry Point
Run this file to start the chatbot application
"""

import os
import sys
import time
from src.chatbot import SpanishChatbot

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display welcome message"""
    clear_screen()
    print("\n" + "=" * 60)
    print("🇪🇸  WELCOME TO THE SPANISH LEARNING CHATBOT  🇪🇸")
    print("=" * 60)
    print("\nThis program will help you learn spanish through:")
    print("  • Vocabulary flashcards")
    print("  • Interactive quizzes")
    print("  • Conversation practice")
    print("\nLet's start learning Spanish today!")
    print("\n" + "=" * 60)
    time.sleep(1)

def main_menu():
    """Display the main menu and handle user input"""
    chatbot = SpanishChatbot()

    while True:
        clear_screen()
        print("\n🇪🇸  SPANISH LEARNING CHATBOT - MAIN MENU  🇪🇸\n")
        print("1. Learn Vocabulary")
        print("2. Practice with Flashcards")
        print("3. Take a Quiz")
        print("4. Practice Conversations")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            chatbot.learn_vocabulary()
        elif choice == '2':
            chatbot.practice_flashcards()
        elif choice == '3':
            chatbot.take_quiz()
        elif choice == '4':
            chatbot.practice_conversations()
        elif choice == '5':
            print("\nGracias for using the Spanish Learning Chatbot! ¡Adiós!")
            time.sleep(1.5)
            sys.exit(0)
        else:
            print("\nInvalid choice. Pkease try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        display_welcome()
        input("\nPress Enter to continue...")
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. ¡Adiós!")
        sys.exit(0)