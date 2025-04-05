"""
Spanish Learning Chatbot - User Profile Management
This module handles user profiles, progress tracking, and statistics
"""

import os
import json
import datetime
from src.utils import save_json_data, load_json_data, create_directory_if_not_exists

class UserProfile:
    """Handles user profile creation, loading, and progress tracking"""
    
    def __init__(self):
        """Initialize user profile"""
        self.current_profile = None
        self.profile_name = None
        self.profiles_dir = "data/user_profiles"
        
        # Ensure profiles directory exists
        create_directory_if_not_exists(self.profiles_dir)
        
    def create_profile(self, name):
        """
        Create a new user profile
        
        Args:
            name (str): User's name
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Create a profile ID from the name (lowercase, no spaces)
        profile_id = name.lower().replace(" ", "_")
        
        # Check if profile already exists
        profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
        if os.path.exists(profile_path):
            return False
        
        # Create new profile data
        profile_data = {
            "name": name,
            "created_at": datetime.datetime.now().isoformat(),
            "last_login": datetime.datetime.now().isoformat(),
            "statistics": {
                "quizzes_taken": 0,
                "flashcards_practiced": 0,
                "conversations_practiced": 0,
                "total_score": 0,
                "quiz_history": []
            },
            "mastered_words": {},
            "custom_vocabulary": [],
            "last_word_of_day": None,
            "word_of_day_history": []
        }
        
        # Save profile
        if save_json_data(profile_data, profile_path):
            self.current_profile = profile_data
            self.profile_name = profile_id
            return True
        
        return False
        
    def load_profile(self, name):
        """
        Load an existing user profile
        
        Args:
            name (str): User's name or profile ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Try to find profile by name or ID
        profile_id = name.lower().replace(" ", "_")
        profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
        
        if not os.path.exists(profile_path):
            return False
        
        try:
            profile_data = load_json_data(profile_path)
            profile_data["last_login"] = datetime.datetime.now().isoformat()
            save_json_data(profile_data, profile_path)
            
            self.current_profile = profile_data
            self.profile_name = profile_id
            return True
        except Exception as e:
            print(f"Error loading profile: {e}")
            return False
    
    def save_current_profile(self):
        """Save the current profile to disk"""
        if not self.current_profile or not self.profile_name:
            return False
        
        profile_path = os.path.join(self.profiles_dir, f"{self.profile_name}.json")
        return save_json_data(self.current_profile, profile_path)
    
    def get_available_profiles(self):
        """Get a list of available profile names"""
        profiles = []
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".json"):
                profile_id = filename[:-5]  # Remove .json extension
                try:
                    profile_data = load_json_data(os.path.join(self.profiles_dir, filename))
                    profiles.append({
                        "id": profile_id,
                        "name": profile_data.get("name", profile_id)
                    })
                except:
                    pass
        
        return profiles
    
    def update_quiz_score(self, category, score, max_score):
        """
        Update the profile with a new quiz score
        
        Args:
            category (str): Quiz category
            score (int): Score achieved
            max_score (int): Maximum possible score
        """
        if not self.current_profile:
            return False
        
        # Update statistics
        self.current_profile["statistics"]["quizzes_taken"] += 1
        self.current_profile["statistics"]["total_score"] += score
        
        # Add quiz to history
        quiz_data = {
            "date": datetime.datetime.now().isoformat(),
            "category": category,
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 1)
        }
        
        self.current_profile["statistics"]["quiz_history"].append(quiz_data)
        
        # Save changes
        return self.save_current_profile()
    
    def update_word_mastery(self, word, category, is_correct):
        """
        Update mastery level for a word
        
        Args:
            word (str): The Spanish word
            category (str): Word category
            is_correct (bool): Whether the user got it correct
        """
        if not self.current_profile:
            return False
        
        if category not in self.current_profile["mastered_words"]:
            self.current_profile["mastered_words"][category] = {}
        
        if word not in self.current_profile["mastered_words"][category]:
            self.current_profile["mastered_words"][category][word] = {
                "correct_count": 0,
                "incorrect_count": 0,
                "last_practiced": None,
                "mastery_level": 0  # 0-5 scale: 0=not seen, 5=mastered
            }
        
        word_data = self.current_profile["mastered_words"][category][word]
        
        # Update word data
        if is_correct:
            word_data["correct_count"] += 1
            # Increase mastery (max 5)
            word_data["mastery_level"] = min(5, word_data["mastery_level"] + 1)
        else:
            word_data["incorrect_count"] += 1
            # Decrease mastery (min 0)
            word_data["mastery_level"] = max(0, word_data["mastery_level"] - 1)
        
        word_data["last_practiced"] = datetime.datetime.now().isoformat()
        
        # Save changes
        return self.save_current_profile()
    
    def get_mastery_level(self, word, category):
        """
        Get the mastery level for a specific word
        
        Args:
            word (str): The Spanish word
            category (str): Word category
            
        Returns:
            int: Mastery level (0-5)
        """
        if not self.current_profile:
            return 0
        
        if category not in self.current_profile["mastered_words"]:
            return 0
        
        if word not in self.current_profile["mastered_words"][category]:
            return 0
        
        return self.current_profile["mastered_words"][category][word]["mastery_level"]
    
    def add_custom_word(self, spanish, english, example="", example_translation="", category="custom"):
        """
        Add a custom vocabulary word
        
        Args:
            spanish (str): Spanish word
            english (str): English translation
            example (str): Example sentence (optional)
            example_translation (str): Example translation (optional)
            category (str): Category for the word (optional, defaults to 'custom')
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.current_profile:
            return False
        
        # Create the word
        word_data = {
            "spanish": spanish,
            "english": english,
            "example": example,
            "example_translation": example_translation,
            "category": category,
            "difficulty": "custom",
            "added_on": datetime.datetime.now().isoformat()
        }
        
        # Add to profile
        self.current_profile["custom_vocabulary"].append(word_data)
        
        # Save changes
        return self.save_current_profile()
    
    def get_custom_words(self):
        """Get all custom words added by the user"""
        if not self.current_profile:
            return []
        
        return self.current_profile["custom_vocabulary"]
    
    def update_flashcard_practice(self, count=1):
        """Update stats for flashcard practice"""
        if not self.current_profile:
            return False
        
        self.current_profile["statistics"]["flashcards_practiced"] += count
        return self.save_current_profile()
    
    def update_conversation_practice(self, count=1):
        """Update stats for conversation practice"""
        if not self.current_profile:
            return False
        
        self.current_profile["statistics"]["conversations_practiced"] += count
        return self.save_current_profile()
    
    def get_statistics(self):
        """Get user statistics"""
        if not self.current_profile:
            return None
        
        return self.current_profile["statistics"]
    
    def update_word_of_day(self, word_data):
        """
        Update the word of the day
        
        Args:
            word_data (dict): Word data including spanish, english, etc.
        """
        if not self.current_profile:
            return False
        
        today = datetime.datetime.now().date().isoformat()
        
        # Check if already updated today
        if self.current_profile["last_word_of_day"] == today:
            return False
        
        # Update word of day
        word_history_entry = word_data.copy()
        word_history_entry["date"] = today
        
        self.current_profile["last_word_of_day"] = today
        self.current_profile["word_of_day_history"].append(word_history_entry)
        
        # Save changes
        return self.save_current_profile()
    
    def get_word_of_day(self):
        """
        Get the word of the day
        
        Returns:
            dict: Today's word or None if not set today
        """
        if not self.current_profile:
            return None
        
        today = datetime.datetime.now().date().isoformat()
        
        # Check if we've already set a word today
        if self.current_profile["last_word_of_day"] == today:
            # Return the latest word
            if self.current_profile["word_of_day_history"]:
                return self.current_profile["word_of_day_history"][-1]
        
        return None