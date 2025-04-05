"""
Spanish Learning Chatbot - Vocabulary Management
This module handles vocabulary operations including adding, updating, and retrieving vocabulary
"""

import random
import json
import datetime
from src.utils import save_json_data, load_json_data, clear_screen

class VocabularyManager:
    """Class for handling vocabulary operations"""
    
    def __init__(self, vocabulary_file='data/vocabulary.json'):
        """
        Initialize with vocabulary file path
        
        Args:
            vocabulary_file (str): Path to vocabulary JSON file
        """
        self.vocabulary_file = vocabulary_file
        self.vocabulary = load_json_data(vocabulary_file)
    
    def save_vocabulary(self):
        """Save current vocabulary to file"""
        return save_json_data(self.vocabulary, self.vocabulary_file)
    
    def get_categories(self):
        """Get all vocabulary categories"""
        return self.vocabulary['categories']
    
    def get_category_by_name(self, name):
        """Get a category by its name"""
        for category in self.vocabulary['categories']:
            if category['name'] == name:
                return category
        return None
    
    def get_category_by_display_name(self, display_name):
        """Get a category by its display name"""
        for category in self.vocabulary['categories']:
            if category['display_name'] == display_name:
                return category
        return None
    
    def get_word_of_day(self, user_profile=None):
        """
        Get or generate word of the day
        
        Args:
            user_profile (UserProfile, optional): User profile to save word of day
            
        Returns:
            dict: Word of the day data
        """
        # Check if user already has a word of the day
        if user_profile and user_profile.current_profile:
            existing_word = user_profile.get_word_of_day()
            if existing_word:
                return existing_word
        
        # Select a random word
        all_words = []
        for category in self.vocabulary['categories']:
            # Add category name to each word for reference
            for word in category['words']:
                word_with_category = word.copy()
                word_with_category['category_name'] = category['name']
                word_with_category['category_display'] = category['display_name']
                all_words.append(word_with_category)
        
        if not all_words:
            return None
        
        word_of_day = random.choice(all_words)
        
        # Save to user profile if available
        if user_profile and user_profile.current_profile:
            user_profile.update_word_of_day(word_of_day)
        
        return word_of_day
    
    def add_custom_word(self, spanish, english, example="", example_translation="", 
                        category="custom", difficulty="custom", pronunciation_tip=""):
        """
        Add a custom word to the vocabulary
        
        Args:
            spanish (str): Spanish word
            english (str): English translation
            example (str, optional): Example sentence
            example_translation (str, optional): Translation of example
            category (str, optional): Category name
            difficulty (str, optional): Difficulty level
            pronunciation_tip (str, optional): Pronunciation tip
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Create word data
        word_data = {
            "spanish": spanish,
            "english": english,
            "example": example,
            "example_translation": example_translation,
            "difficulty": difficulty
        }
        
        if pronunciation_tip:
            word_data["pronunciation_tip"] = pronunciation_tip
        
        # Find or create category
        target_category = None
        for cat in self.vocabulary['categories']:
            if cat['name'] == category:
                target_category = cat
                break
        
        # If category doesn't exist, create it
        if not target_category:
            display_name = category.capitalize()
            new_category = {
                "name": category,
                "display_name": display_name,
                "words": []
            }
            self.vocabulary['categories'].append(new_category)
            target_category = new_category
        
        # Add word to category
        target_category['words'].append(word_data)
        
        # Save changes
        return self.save_vocabulary()
    
    def add_custom_category(self, name, display_name=None):
        """
        Add a new vocabulary category
        
        Args:
            name (str): Category name (lowercase, no spaces)
            display_name (str, optional): Display name for the category
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if category already exists
        for category in self.vocabulary['categories']:
            if category['name'] == name:
                return False
        
        # Create new category
        new_category = {
            "name": name,
            "display_name": display_name or name.capitalize(),
            "words": []
        }
        
        self.vocabulary['categories'].append(new_category)
        
        # Save changes
        return self.save_vocabulary()
    
    def get_words_by_difficulty(self, difficulty):
        """
        Get all words of a specific difficulty level
        
        Args:
            difficulty (str): Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            list: List of words with the specified difficulty
        """
        words = []
        
        for category in self.vocabulary['categories']:
            for word in category['words']:
                if word.get('difficulty') == difficulty:
                    words.append(word)
        
        return words
    
    def get_words_by_mastery(self, user_profile, mastery_level):
        """
        Get words by mastery level from user profile
        
        Args:
            user_profile (UserProfile): User profile
            mastery_level (int): Mastery level to filter by (0-5)
            
        Returns:
            list: Words with specified mastery level
        """
        if not user_profile or not user_profile.current_profile:
            return []
        
        result_words = []
        
        for category_name, words in user_profile.current_profile['mastered_words'].items():
            category = self.get_category_by_name(category_name)
            
            if not category:
                continue
                
            for word_spanish, word_data in words.items():
                if word_data['mastery_level'] == mastery_level:
                    # Find full word data in vocabulary
                    for vocab_word in category['words']:
                        if vocab_word['spanish'] == word_spanish:
                            # Add category info to word
                            word_with_info = vocab_word.copy()
                            word_with_info['category_name'] = category['name']
                            word_with_info['category_display'] = category['display_name']
                            result_words.append(word_with_info)
                            break
        
        return result_words
    
    def update_word(self, category_name, spanish_word, new_data):
        """
        Update an existing word
        
        Args:
            category_name (str): Category name
            spanish_word (str): Spanish word to update
            new_data (dict): New data for the word
            
        Returns:
            bool: True if successful, False otherwise
        """
        category = self.get_category_by_name(category_name)
        
        if not category:
            return False
        
        for i, word in enumerate(category['words']):
            if word['spanish'] == spanish_word:
                # Update the word
                for key, value in new_data.items():
                    if key != 'spanish':  # Don't change the spanish word itself
                        category['words'][i][key] = value
                
                # Save changes
                return self.save_vocabulary()
        
        return False