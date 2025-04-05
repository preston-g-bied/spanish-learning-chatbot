"""
Spanish Learning Chatbot - Utility Functions
This module contains utility functions used across the application
"""

import json
import os
import sys

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json_data(file_path):
    """
    Load data from a JSON file

    Args:
        file_path (str): Path to the JSON file

    Returns:
        dict: Loaded JSON data

    Raises:
        SystemExit: If file cannot be loaded
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
        print("Make sure you have the correct data files in the 'data' directory")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        sys.exit(1)

def save_json_data(data, file_path):
    """
    Save data to a JSON file

    Args:
        data (dict): Data to save
        file_path (str): Path to save the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False
    
def create_directory_if_not_exists(directory):
    """
    Create a directory if it doesn't exist

    Args:
        directory (str): Directory path to create

    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False
    
def ensure_data_files_exist():
    """
    Make sure required data files exist, create with default data if they don't
    """
    required_files = {
        'data/vocabulary.json': {
            'categories': []
        },
        'data/dialogues.json': {
            'dialogues': []
        }
    }

    # create data directory if it doesn't exist
    create_directory_if_not_exists('data')

    # check each required file
    for file_path, default_data in required_files.items():
        if not os.path.exists(file_path):
            print(f"Creating default {file_path}...")
            save_json_data(default_data, file_path)