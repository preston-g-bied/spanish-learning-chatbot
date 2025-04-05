"""
Spanish Learning Chatbot - Core Functionality
This module contains the main chatbot class that handles interactions with the user
"""

import json
import os
import random
import time
from src.quiz import QuizSystem
from src.utils import clear_screen, load_json_data

class SpanishChatbot:
    """Main chatbot class that handles user interactions and learning activities"""

    def __init__(self):
        """Initialize the chatbot with vocabulary and dialogue data"""
        self.vocabulary = load_json_data('../data/vocabulary.json')
        self.dialogues = load_json_data('../data/dialogues.json')
        self.quiz_system = QuizSystem(self.vocabulary)

    def learn_vocabulary(self):
        """Show vocabulary by category for learning"""
        while True:
            clear_screen()
            print("\n🇪🇸  LEARN VOCABULARY  🇪🇸\n")

            # display available categories
            print("Choose a category to learn:")
            for i, category in enumerate(self.vocabulary['categories'], 1):
                print(f"{i}. {category['display_name']}")
            print(f"{len(self.vocabulary['categories']) + 1}. Return to Main Menu")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == len(self.vocabulary['categories']) + 1:
                    return
                
                if 1 <= choice <= len(self.vocabulary['categories']):
                    self._display_category_words(self.vocabulary['categories'][choice - 1])
                else:
                    print("\nInvalid choice. Please try agian.")
                    time.sleep(1)
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _display_category_words(self, category):
        """Display all words in a specific category"""
        clear_screen()
        print(f"\n🇪🇸  {category['display_name'].upper()}  🇪🇸\n")

        for i, word in enumerate(category['words'], 1):
            print(f"Word {i}: {word['spanish']} - {word['english']}")
            print(f"Example: {word['example']}")
            print(f"Translation: {word['example_translation']}")
            print("-" * 50)

            # if not the last word, wait for user to press Enter to continue
            if i < len(category['words']):
                input("\nPress Enter to see the next word...")

        input("\nPress Enter to return to categories...")

    def practice_flashcards(self):
        """Practice vocabulary with flashcards"""
        while True:
            clear_screen()
            print("\n🇪🇸  FLASHCARDS  🇪🇸\n")

            # display available categories
            print("Choose a category for flashcards:")
            for i, category in enumerate(self.vocabulary['categories'], 1):
                print(f"{i}. {category['display_name']}")
            print(f"{len(self.vocabulary['categories']) + 1}. Return to Main Menu")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == len(self.vocabulary['categories']) + 1:
                    return
                
                if 1 <= choice <= len(self.vocabulary['categories']):
                    self._run_flashcards(self.vocabulary['categories'][choice - 1])
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _run_flashcards(self, category):
        """Run flashcard practice for a specific category"""
        words = category['words'].copy()
        random.shuffle(words)

        for word in words:
            clear_screen()
            print(f"\n🇪🇸  FLASHCARD: {category['display_name'].upper()}  🇪🇸\n")

            # show Spanish word and ask user to think of the translation
            print(f"Spanish: {word['spanish']}")
            input("\nThink of the translation, then press Enter to see it...")

            # show the translation
            print(f"\nEnglish: {word['english']}")
            print(f"\nExample: {word['example']}")
            print(f"\nTranslation: {word['example_translation']}")

            # ask if they got it right
            while True:
                got_it = input("\nDid you get it right? (y/n): ").lower()
                if got_it in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")

            # continue to the next card or return to category selection
            if input("\nPress Enter for next word or 'q' to quit: ").lower() == 'q':
                break

        input("\nFlashcard session complete! Press Enter to return to categories...")

    def take_quiz(self):
        """Take a vocabulary quiz"""
        self.quiz_system.start_quiz()

    def practice_conversations(self):
        """Practice with pre-written dialogues"""
        while True:
            clear_screen()
            print("\n🇪🇸  CONVERSATION PRACTICE  🇪🇸\n")

            # display available dialogues
            print("Choose a conversation to practice:")
            for i, dialogue in enumerate(self.dialogues['dialogues'], 1):
                print(f"{i}. {dialogue['title']} (Difficulty: {dialogue['difficulty']})")
            print(f"{len(self.dialogues['dialogues']) + 1}. Return to Main Menu")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == len(self.dialogues['dialogues']) + 1:
                    return
                
                if 1 <= choice <= len(self.dialogues['dialogues']):
                    self._practice_dialogue(self.dialogues['dialogues'][choice - 1])
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _practice_dialogue(self, dialogue):
        """Practice a specific dialogue"""
        clear_screen()
        print(f"\n🇪🇸  DIALOGUE: {dialogue['title'].upper()}  🇪🇸\n")
        print("In this practice, you'll play the role of Person B.")
        print("Read Person A's line, then try to respond as Person B.")
        print("Press Enter to see the correct response.")
        print("\nLet's begin!\n")

        for i, exchange in enumerate(dialogue['exchanges'], 1):
            print(f"\nExchange {i}:")
            print(f"Person A: {exchange['speaker_a']}")
            print(f"Translation: {exchange['translation_a']}")
            
            input("\nThink of how to respond as Person B, then press Enter...")
            
            print(f"\nCorrect response: {exchange['speaker_b']}")
            print(f"Translation: {exchange['translation_b']}")
            
            # continue to next exchange or return to dialogue selection
            if i < len(dialogue['exchanges']):
                if input("\nPress Enter for next exchange or 'q' to quit: ").lower() == 'q':
                    break
            else:
                print("\nDialogue complete!")
        
        input("\nPress Enter to return to conversations...")
