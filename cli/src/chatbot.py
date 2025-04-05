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
from src.vocabulary_manager import VocabularyManager
from src.spaced_repetition import SpacedRepetitionSystem
from src.cultural_notes import CulturalNotesManager

class SpanishChatbot:
    """Main chatbot class that handles user interactions and learning activities"""

    def __init__(self, user_profile=None):
        """
        Initialize the chatbot with vocabulary and dialogue data
        
        Args:
            user_profile (UserProfile, optional): User profile for tracking progress
        """
        self.vocabulary_manager = VocabularyManager()
        self.vocabulary = self.vocabulary_manager.vocabulary
        self.dialogues = load_json_data('data/dialogues.json')
        self.user_profile = user_profile
        self.quiz_system = QuizSystem(self.vocabulary, self.user_profile)
        self.spaced_repetition = SpacedRepetitionSystem(self.user_profile)
        self.cultural_notes = CulturalNotesManager()
        
        # Check for word of the day if user profile exists
        if self.user_profile and self.user_profile.current_profile:
            # Set word of day if not already set today
            if not self.user_profile.get_word_of_day():
                self.vocabulary_manager.get_word_of_day(self.user_profile)

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
                    print("\nInvalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _display_category_words(self, category):
        """Display all words in a specific category"""
        # Check if filtering by difficulty is possible
        has_difficulty = any('difficulty' in word for word in category['words'])
        
        if has_difficulty:
            clear_screen()
            print(f"\n🇪🇸  {category['display_name'].upper()}  🇪🇸\n")
            print("Filter by difficulty:")
            print("1. Beginner")
            print("2. Intermediate")
            print("3. Advanced")
            print("4. All levels")
            
            difficulty_choice = input("\nEnter your choice (default: 4): ")
            difficulty_map = {
                '1': 'beginner',
                '2': 'intermediate',
                '3': 'advanced'
            }
            
            if difficulty_choice in difficulty_map:
                filtered_words = [w for w in category['words'] if w.get('difficulty') == difficulty_map[difficulty_choice]]
            else:
                filtered_words = category['words']
        else:
            filtered_words = category['words']
        
        clear_screen()
        print(f"\n🇪🇸  {category['display_name'].upper()}  🇪🇸\n")
        
        if not filtered_words:
            print("No words found with this filter.")
            input("\nPress Enter to return...")
            return
        
        for i, word in enumerate(filtered_words, 1):
            # Show mastery level if user profile exists
            if self.user_profile and self.user_profile.current_profile:
                mastery = self.user_profile.get_mastery_level(word['spanish'], category['name'])
                mastery_display = "★" * mastery + "☆" * (5 - mastery)
                print(f"Word {i}: {word['spanish']} - {word['english']} (Mastery: {mastery_display})")
            else:
                print(f"Word {i}: {word['spanish']} - {word['english']}")
            
            print(f"Example: {word['example']}")
            print(f"Translation: {word['example_translation']}")
            
            # Show pronunciation tip if available
            if 'pronunciation_tip' in word:
                print(f"Pronunciation: {word['pronunciation_tip']}")
            
            # Show difficulty if available
            if 'difficulty' in word:
                print(f"Difficulty: {word['difficulty'].capitalize()}")
            
            print("-" * 50)

            # if not the last word, wait for user to press Enter to continue
            if i < len(filtered_words):
                input("\nPress Enter to see the next word...")

        input("\nPress Enter to return to categories...")

    def practice_flashcards(self):
        """Practice vocabulary with flashcards"""
        while True:
            clear_screen()
            print("\n🇪🇸  FLASHCARDS  🇪🇸\n")
            
            print("Choose flashcard mode:")
            print("1. Practice by category")
            print("2. Spaced repetition (recommended)")
            print("3. Return to Main Menu")
            
            try:
                choice = input("\nEnter your choice: ")
                
                if choice == "1":
                    self._practice_by_category()
                elif choice == "2":
                    self.spaced_repetition.run_spaced_repetition_session(self.vocabulary_manager)
                elif choice == "3":
                    return
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _practice_by_category(self):
        """Practice flashcards by category"""
        while True:
            clear_screen()
            print("\n🇪🇸  CATEGORY FLASHCARDS  🇪🇸\n")

            # display available categories
            print("Choose a category for flashcards:")
            for i, category in enumerate(self.vocabulary['categories'], 1):
                print(f"{i}. {category['display_name']}")
            print(f"{len(self.vocabulary['categories']) + 1}. Return to Flashcard Menu")

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
        
        # Track number of cards practiced
        cards_practiced = 0

        for word in words:
            clear_screen()
            print(f"\n🇪🇸  FLASHCARD: {category['display_name'].upper()}  🇪🇸\n")
            
            # Show mastery level if user profile exists
            if self.user_profile and self.user_profile.current_profile:
                mastery = self.user_profile.get_mastery_level(word['spanish'], category['name'])
                mastery_display = "★" * mastery + "☆" * (5 - mastery)
                print(f"Mastery: {mastery_display}\n")
            
            # Randomly choose direction (Spanish to English or English to Spanish)
            direction = random.choice([1, 2])
            
            if direction == 1:  # Spanish to English
                print(f"Spanish: {word['spanish']}")
                
                # Show pronunciation tip if available
                if 'pronunciation_tip' in word:
                    print(f"Pronunciation: {word['pronunciation_tip']}")
                
                input("\nThink of the English translation, then press Enter...")
                print(f"\nEnglish: {word['english']}")
            else:  # English to Spanish
                print(f"English: {word['english']}")
                input("\nThink of the Spanish translation, then press Enter...")
                print(f"\nSpanish: {word['spanish']}")
                
                # Show pronunciation tip if available
                if 'pronunciation_tip' in word:
                    print(f"Pronunciation: {word['pronunciation_tip']}")

            print(f"\nExample: {word['example']}")
            print(f"\nTranslation: {word['example_translation']}")

            # ask if they got it right
            while True:
                got_it = input("\nDid you get it right? (y/n): ").lower()
                if got_it in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            # Update user profile if available
            if self.user_profile and self.user_profile.current_profile:
                self.user_profile.update_word_mastery(
                    word['spanish'],
                    category['name'],
                    got_it == 'y'
                )
            
            cards_practiced += 1

            # continue to the next card or return to category selection
            if input("\nPress Enter for next word or 'q' to quit: ").lower() == 'q':
                break
        
        # Update flashcard practice count in user profile
        if self.user_profile and self.user_profile.current_profile:
            self.user_profile.update_flashcard_practice(cards_practiced)

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
        
        # Track if dialogue was completed
        completed = True
        exchanges_practiced = 0

        for i, exchange in enumerate(dialogue['exchanges'], 1):
            print(f"\nExchange {i}:")
            print(f"Person A: {exchange['speaker_a']}")
            print(f"Translation: {exchange['translation_a']}")
            
            input("\nThink of how to respond as Person B, then press Enter...")
            
            print(f"\nCorrect response: {exchange['speaker_b']}")
            print(f"Translation: {exchange['translation_b']}")
            
            exchanges_practiced += 1
            
            # continue to next exchange or return to dialogue selection
            if i < len(dialogue['exchanges']):
                if input("\nPress Enter for next exchange or 'q' to quit: ").lower() == 'q':
                    completed = False
                    break
            else:
                print("\nDialogue complete!")
        
        # Update user profile if available
        if self.user_profile and self.user_profile.current_profile:
            self.user_profile.update_conversation_practice(1 if completed else 0)
        
        input("\nPress Enter to return to conversations...")
    
    def manage_custom_vocabulary(self):
        """Manage custom vocabulary words"""
        while True:
            clear_screen()
            print("\n🇪🇸  MANAGE CUSTOM VOCABULARY  🇪🇸\n")
            
            print("1. Add new word")
            print("2. View your custom words")
            print("3. Return to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                self._add_custom_word()
            elif choice == "2":
                self._view_custom_words()
            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
    
    def _add_custom_word(self):
        """Add a custom vocabulary word"""
        clear_screen()
        print("\n🇪🇸  ADD CUSTOM WORD  🇪🇸\n")
        
        spanish = input("Spanish word: ")
        if not spanish:
            print("\nSpanish word cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        english = input("English translation: ")
        if not english:
            print("\nEnglish translation cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        example = input("Example sentence (optional): ")
        example_translation = input("Example translation (optional): ")
        pronunciation_tip = input("Pronunciation tip (optional): ")
        
        # Choose or create category
        clear_screen()
        print("\n🇪🇸  SELECT CATEGORY  🇪🇸\n")
        
        print("Select a category for your word:")
        for i, category in enumerate(self.vocabulary['categories'], 1):
            print(f"{i}. {category['display_name']}")
        print(f"{len(self.vocabulary['categories']) + 1}. Create new category")
        
        category_choice = input("\nEnter your choice: ")
        
        if category_choice.isdigit() and 1 <= int(category_choice) <= len(self.vocabulary['categories']):
            category = self.vocabulary['categories'][int(category_choice) - 1]['name']
        elif category_choice == str(len(self.vocabulary['categories']) + 1):
            category_name = input("\nEnter new category name: ")
            if not category_name:
                print("\nCategory name cannot be empty.")
                input("\nPress Enter to continue...")
                return
            
            display_name = input("Enter display name (leave blank to use category name): ")
            if not display_name:
                display_name = category_name.capitalize()
            
            # Create new category
            if self.vocabulary_manager.add_custom_category(category_name, display_name):
                print(f"\nCategory '{display_name}' created.")
                category = category_name
            else:
                print("\nFailed to create category.")
                input("\nPress Enter to continue...")
                return
        else:
            print("\nInvalid choice.")
            input("\nPress Enter to continue...")
            return
        
        # Select difficulty
        difficulty = input("\nDifficulty level (beginner/intermediate/advanced): ").lower()
        if difficulty not in ['beginner', 'intermediate', 'advanced']:
            difficulty = 'custom'
        
        # Add to vocabulary
        if self.vocabulary_manager.add_custom_word(
            spanish, english, example, example_translation, category, difficulty, pronunciation_tip
        ):
            print("\nWord added successfully!")
            
            # Also add to user profile if available
            if self.user_profile and self.user_profile.current_profile:
                self.user_profile.add_custom_word(
                    spanish, english, example, example_translation, category
                )
        else:
            print("\nFailed to add word.")
        
        input("\nPress Enter to continue...")
    
    def _view_custom_words(self):
        """View custom vocabulary words"""
        if not self.user_profile or not self.user_profile.current_profile:
            print("\nYou need to be logged in to view custom words.")
            input("\nPress Enter to continue...")
            return
        
        custom_words = self.user_profile.get_custom_words()
        
        if not custom_words:
            clear_screen()
            print("\n🇪🇸  CUSTOM WORDS  🇪🇸\n")
            print("You haven't added any custom words yet.")
            input("\nPress Enter to continue...")
            return
        
        clear_screen()
        print("\n🇪🇸  YOUR CUSTOM WORDS  🇪🇸\n")
        
        for i, word in enumerate(custom_words, 1):
            print(f"Word {i}: {word['spanish']} - {word['english']}")
            
            if word['example']:
                print(f"Example: {word['example']}")
                print(f"Translation: {word['example_translation']}")
            
            print(f"Category: {word['category']}")
            print(f"Added on: {word['added_on'][:10]}")
            print("-" * 50)
            
            # If not the last word, wait for user input
            if i < len(custom_words):
                if input("\nPress Enter for next word or 'q' to quit: ").lower() == 'q':
                    break
        
        input("\nPress Enter to return...")
    
    def browse_cultural_notes(self):
        """Browse cultural and grammar notes"""
        while True:
            clear_screen()
            print("\n🇪🇸  LANGUAGE & CULTURE  🇪🇸\n")
            
            print("1. Cultural Notes")
            print("2. Grammar Explanations")
            print("3. Return to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                self.cultural_notes.browse_cultural_notes()
            elif choice == "2":
                self.cultural_notes.browse_grammar_notes()
            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)