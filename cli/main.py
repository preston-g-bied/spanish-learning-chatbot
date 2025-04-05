"""
Spanish Learning Chatbot - Main Entry Point
Run this file to start the chatbot application
"""

import os
import sys
import time
from src.chatbot import SpanishChatbot
from src.user_profile import UserProfile
from src.utils import clear_screen

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
    print("  • Progress tracking")
    print("\nLet's start learning Spanish today!")
    print("\n" + "=" * 60)
    time.sleep(1)

def user_login():
    """Handle user login or profile creation"""
    user_profile = UserProfile()
    
    while True:
        clear_screen()
        print("\n🇪🇸  USER PROFILE  🇪🇸\n")
        
        profiles = user_profile.get_available_profiles()
        
        if profiles:
            print("Available profiles:")
            for i, profile in enumerate(profiles, 1):
                print(f"{i}. {profile['name']}")
            print(f"{len(profiles) + 1}. Create new profile")
            print(f"{len(profiles) + 2}. Continue without profile")
            
            try:
                choice = int(input("\nSelect a profile or create a new one: "))
                
                if 1 <= choice <= len(profiles):
                    # Load existing profile
                    if user_profile.load_profile(profiles[choice-1]['id']):
                        print(f"\nWelcome back, {user_profile.current_profile['name']}!")
                        time.sleep(1)
                        return user_profile
                    else:
                        print("\nError loading profile. Please try again.")
                        time.sleep(1)
                
                elif choice == len(profiles) + 1:
                    # Create new profile
                    name = input("\nEnter your name: ")
                    if name and user_profile.create_profile(name):
                        print(f"\nWelcome, {name}! Your profile has been created.")
                        time.sleep(1)
                        return user_profile
                    else:
                        print("\nError creating profile. Please try again.")
                        time.sleep(1)
                
                elif choice == len(profiles) + 2:
                    # Continue without profile
                    print("\nContinuing without profile. Your progress will not be saved.")
                    time.sleep(1)
                    return None
                
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(1)
            
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)
        
        else:
            print("No profiles found.")
            print("1. Create new profile")
            print("2. Continue without profile")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                name = input("\nEnter your name: ")
                if name and user_profile.create_profile(name):
                    print(f"\nWelcome, {name}! Your profile has been created.")
                    time.sleep(1)
                    return user_profile
                else:
                    print("\nError creating profile. Please try again.")
                    time.sleep(1)
            
            elif choice == "2":
                print("\nContinuing without profile. Your progress will not be saved.")
                time.sleep(1)
                return None
            
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)

def display_user_stats(user_profile):
    """Display user statistics"""
    if not user_profile or not user_profile.current_profile:
        print("\nNo user profile loaded.")
        return
    
    clear_screen()
    stats = user_profile.get_statistics()
    
    print("\n🇪🇸  YOUR LEARNING STATISTICS  🇪🇸\n")
    print(f"Name: {user_profile.current_profile['name']}")
    print(f"Profile created: {user_profile.current_profile['created_at'][:10]}")
    print("\nActivity:")
    print(f"  • Quizzes taken: {stats['quizzes_taken']}")
    print(f"  • Flashcards practiced: {stats['flashcards_practiced']}")
    print(f"  • Conversations practiced: {stats['conversations_practiced']}")
    
    # Calculate mastery statistics
    mastery_count = 0
    mastery_levels = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for category in user_profile.current_profile['mastered_words'].values():
        for word_data in category.values():
            mastery_levels[word_data['mastery_level']] += 1
            mastery_count += 1
    
    print(f"\nVocabulary Mastery ({mastery_count} words tracked):")
    
    if mastery_count > 0:
        print(f"  • Mastered (★★★★★): {mastery_levels[5]} words")
        print(f"  • Strong (★★★★☆): {mastery_levels[4]} words")
        print(f"  • Good (★★★☆☆): {mastery_levels[3]} words")
        print(f"  • Basic (★★☆☆☆): {mastery_levels[2]} words")
        print(f"  • Learning (★☆☆☆☆): {mastery_levels[1]} words")
        print(f"  • New (☆☆☆☆☆): {mastery_levels[0]} words")
    else:
        print("  • No words practiced yet")
    
    # Show recent quiz scores
    if stats['quiz_history']:
        print("\nRecent Quiz Scores:")
        recent_quizzes = sorted(stats['quiz_history'], key=lambda x: x['date'], reverse=True)[:5]
        
        for quiz in recent_quizzes:
            date = quiz['date'][:10]
            print(f"  • {date} - {quiz['category']}: {quiz['score']}/{quiz['max_score']} ({quiz['percentage']}%)")
    
    # Show word of the day if available
    word_of_day = user_profile.get_word_of_day()
    if word_of_day:
        print("\nToday's Word of the Day:")
        print(f"  • {word_of_day['spanish']} - {word_of_day['english']}")
        print(f"  • Example: {word_of_day['example']}")
    
    input("\nPress Enter to return to main menu...")

def main_menu(user_profile=None):
    """Display the main menu and handle user input"""
    chatbot = SpanishChatbot(user_profile)

    while True:
        clear_screen()
        
        # Show a header with user name if profile is loaded
        if user_profile and user_profile.current_profile:
            print(f"\n🇪🇸  SPANISH LEARNING CHATBOT - Welcome, {user_profile.current_profile['name']}!  🇪🇸\n")
        else:
            print("\n🇪🇸  SPANISH LEARNING CHATBOT - MAIN MENU  🇪🇸\n")
        
        # Show word of the day if available
        if user_profile and user_profile.current_profile:
            word_of_day = user_profile.get_word_of_day()
            if word_of_day:
                print(f"📖 Today's Word: {word_of_day['spanish']} - {word_of_day['english']}\n")
        
        print("1. Learn Vocabulary")
        print("2. Practice with Flashcards")
        print("3. Take a Quiz")
        print("4. Practice Conversations")
        
        # Additional options for users with profiles
        if user_profile and user_profile.current_profile:
            print("5. View Your Statistics")
            print("6. Manage Custom Vocabulary")
            print("7. Language & Cultural Notes")
            print("8. Exit")
        else:
            print("5. Exit")

        max_choice = 8 if user_profile and user_profile.current_profile else 5
        
        choice = input(f"\nEnter your choice (1-{max_choice}): ")

        if choice == '1':
            chatbot.learn_vocabulary()
        elif choice == '2':
            chatbot.practice_flashcards()
        elif choice == '3':
            chatbot.take_quiz()
        elif choice == '4':
            chatbot.practice_conversations()
        elif choice == '5' and user_profile and user_profile.current_profile:
            display_user_stats(user_profile)
        elif choice == '6' and user_profile and user_profile.current_profile:
            chatbot.manage_custom_vocabulary()
        elif choice == '7' and user_profile and user_profile.current_profile:
            chatbot.browse_cultural_notes()
        elif (choice == '8' and user_profile and user_profile.current_profile) or (choice == '5' and (not user_profile or not user_profile.current_profile)):
            print("\nGracias for using the Spanish Learning Chatbot! ¡Adiós!")
            time.sleep(1.5)
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        display_welcome()
        input("\nPress Enter to continue...")
        user_profile = user_login()
        main_menu(user_profile)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. ¡Adiós!")
        sys.exit(0)