"""
Spanish Learning Chatbot - Spaced Repetition System
This module implements the spaced repetition algorithm for optimized learning
"""

import datetime
import random
import math
from src.utils import clear_screen

class SpacedRepetitionSystem:
    """
    Implements a spaced repetition system for flashcards
    Uses a simplified SuperMemo-2 algorithm to schedule reviews
    """
    
    def __init__(self, user_profile=None):
        """
        Initialize the spaced repetition system
        
        Args:
            user_profile (UserProfile, optional): User profile for tracking progress
        """
        self.user_profile = user_profile
    
    def get_next_review_date(self, mastery_level, last_reviewed=None, correct=True):
        """
        Calculate the next review date based on mastery level
        
        Args:
            mastery_level (int): Current mastery level (0-5)
            last_reviewed (str, optional): ISO date string of last review
            correct (bool): Whether the last answer was correct
            
        Returns:
            datetime.date: Next review date
        """
        today = datetime.datetime.now().date()
        
        if not last_reviewed:
            return today
        
        try:
            last_date = datetime.datetime.fromisoformat(last_reviewed).date()
        except (ValueError, TypeError):
            return today
        
        # If answer was incorrect, review sooner
        if not correct:
            return today
        
        # Calculate interval based on mastery level
        if mastery_level == 0:
            interval = 1  # New word - review the next day
        elif mastery_level == 1:
            interval = 2  # Review after 2 days
        elif mastery_level == 2:
            interval = 4  # Review after 4 days
        elif mastery_level == 3:
            interval = 7  # Review after a week
        elif mastery_level == 4:
            interval = 14  # Review after two weeks
        else:  # mastery_level == 5
            interval = 30  # Review after a month
        
        next_date = last_date + datetime.timedelta(days=interval)
        
        # If next date is in the past, review today
        if next_date < today:
            return today
        
        return next_date
    
    def get_words_due_for_review(self, vocabulary_manager):
        """
        Get words that are due for review
        
        Args:
            vocabulary_manager (VocabularyManager): Vocabulary manager
            
        Returns:
            list: Words due for review with their category info
        """
        if not self.user_profile or not self.user_profile.current_profile:
            # If no profile, return random words from all categories
            all_words = []
            for category in vocabulary_manager.get_categories():
                for word in category['words']:
                    word_with_category = word.copy()
                    word_with_category['category_name'] = category['name']
                    word_with_category['category_display'] = category['display_name']
                    all_words.append(word_with_category)
            
            # Return a random subset
            random.shuffle(all_words)
            return all_words[:10]
        
        # Get words due for review from user profile
        due_words = []
        today = datetime.datetime.now().date()
        
        for category_name, words in self.user_profile.current_profile['mastered_words'].items():
            category = vocabulary_manager.get_category_by_name(category_name)
            
            if not category:
                continue
                
            for word_spanish, word_data in words.items():
                # Calculate next review date
                next_review = self.get_next_review_date(
                    word_data['mastery_level'],
                    word_data['last_practiced'],
                    True
                )
                
                # If word is due for review
                if next_review <= today:
                    # Find full word data in vocabulary
                    for vocab_word in category['words']:
                        if vocab_word['spanish'] == word_spanish:
                            # Add category info to word
                            word_with_info = vocab_word.copy()
                            word_with_info['category_name'] = category['name']
                            word_with_info['category_display'] = category['display_name']
                            word_with_info['mastery_level'] = word_data['mastery_level']
                            due_words.append(word_with_info)
                            break
        
        # If no words are due, get some words that haven't been reviewed yet
        if not due_words:
            # Find words not in mastered_words
            new_words = []
            for category in vocabulary_manager.get_categories():
                mastered_words_in_category = self.user_profile.current_profile['mastered_words'].get(category['name'], {})
                
                for word in category['words']:
                    if word['spanish'] not in mastered_words_in_category:
                        word_with_category = word.copy()
                        word_with_category['category_name'] = category['name']
                        word_with_category['category_display'] = category['display_name']
                        word_with_category['mastery_level'] = 0
                        new_words.append(word_with_category)
            
            # Return a subset of new words
            random.shuffle(new_words)
            return new_words[:min(10, len(new_words))]
        
        # Mix in some new words with due words
        if len(due_words) < 10:
            # Find words not in mastered_words
            new_words = []
            for category in vocabulary_manager.get_categories():
                mastered_words_in_category = self.user_profile.current_profile['mastered_words'].get(category['name'], {})
                
                for word in category['words']:
                    if word['spanish'] not in mastered_words_in_category:
                        word_with_category = word.copy()
                        word_with_category['category_name'] = category['name']
                        word_with_category['category_display'] = category['display_name']
                        word_with_category['mastery_level'] = 0
                        new_words.append(word_with_category)
            
            # Add some new words
            random.shuffle(new_words)
            due_words.extend(new_words[:min(10 - len(due_words), len(new_words))])
        
        return due_words
    
    def run_spaced_repetition_session(self, vocabulary_manager):
        """
        Run a spaced repetition flashcard session
        
        Args:
            vocabulary_manager (VocabularyManager): Vocabulary manager
        """
        # Get words due for review
        due_words = self.get_words_due_for_review(vocabulary_manager)
        
        if not due_words:
            clear_screen()
            print("\n🇪🇸  SPACED REPETITION  🇪🇸\n")
            print("No words available for review.")
            input("\nPress Enter to return to menu...")
            return
        
        # Shuffle words
        random.shuffle(due_words)
        
        # Track number of cards reviewed
        cards_reviewed = 0
        
        for word in due_words:
            clear_screen()
            print("\n🇪🇸  SPACED REPETITION FLASHCARD  🇪🇸\n")
            
            # Show category and difficulty
            print(f"Category: {word['category_display']}")
            if 'difficulty' in word:
                print(f"Difficulty: {word['difficulty'].capitalize()}")
            
            # Show mastery level if available
            if 'mastery_level' in word:
                mastery = word['mastery_level']
                mastery_display = "★" * mastery + "☆" * (5 - mastery)
                print(f"Mastery: {mastery_display}")
            
            # Randomly choose direction (Spanish to English or English to Spanish)
            direction = random.choice([1, 2])
            
            if direction == 1:  # Spanish to English
                print(f"\nSpanish word: {word['spanish']}")
                
                # If pronunciation tip is available, show it
                if 'pronunciation_tip' in word:
                    print(f"Pronunciation: {word['pronunciation_tip']}")
                
                input("\nThink of the English translation, then press Enter...")
                print(f"\nEnglish translation: {word['english']}")
            else:  # English to Spanish
                print(f"\nEnglish word: {word['english']}")
                input("\nThink of the Spanish translation, then press Enter...")
                print(f"\nSpanish translation: {word['spanish']}")
                
                # If pronunciation tip is available, show it
                if 'pronunciation_tip' in word:
                    print(f"Pronunciation: {word['pronunciation_tip']}")
            
            # Show example
            if 'example' in word and word['example']:
                print(f"\nExample: {word['example']}")
                print(f"Translation: {word['example_translation']}")
            
            # Ask if they got it right
            while True:
                got_it = input("\nDid you get it right? (y/n): ").lower()
                if got_it in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            # Update user profile if available
            if self.user_profile and self.user_profile.current_profile:
                self.user_profile.update_word_mastery(
                    word['spanish'],
                    word['category_name'],
                    got_it == 'y'
                )
            
            cards_reviewed += 1
            
            # Ask if they want to continue
            if cards_reviewed < len(due_words):
                continue_choice = input("\nPress Enter for next word or 'q' to quit: ").lower()
                if continue_choice == 'q':
                    break
        
        # Update flashcard practice count in user profile
        if self.user_profile and self.user_profile.current_profile:
            self.user_profile.update_flashcard_practice(cards_reviewed)
        
        # Show session summary
        clear_screen()
        print("\n🇪🇸  SPACED REPETITION SESSION COMPLETE  🇪🇸\n")
        print(f"You reviewed {cards_reviewed} cards in this session.")
        
        if self.user_profile and self.user_profile.current_profile:
            print("\nYour progress has been saved!")
            
            # Show total flashcards practiced
            stats = self.user_profile.get_statistics()
            print(f"Total flashcards practiced: {stats['flashcards_practiced']}")
        
        input("\nPress Enter to return to menu...")