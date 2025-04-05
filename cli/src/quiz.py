"""
Spanish Learning Chatbot - Quiz System
This module handles the quiz functionality of the chatbot
"""

import random
import time
from src.utils import clear_screen

class QuizSystem:
    """Handles quiz creation and scoring for vocabulary practice"""

    def __init__(self, vocabulary_data, user_profile=None):
        """
        Initialize with vocabulary data and user profile
        
        Args:
            vocabulary_data (dict): The vocabulary data
            user_profile (UserProfile, optional): User profile for tracking progress
        """
        self.vocabulary = vocabulary_data
        self.user_profile = user_profile

    def start_quiz(self):
        """Start a vocabulary quiz based on user preferences"""
        while True:
            clear_screen()
            print("\n🇪🇸  VOCABULARY QUIZ  🇪🇸\n")

            # choose quiz category
            print("Choose a category for your quiz:")
            for i, category in enumerate(self.vocabulary['categories'], 1):
                print(f"{i}. {category['display_name']}")
            print(f"{len(self.vocabulary['categories']) + 1}. Return to Main Menu")

            try:
                category_choice = int(input("\nEnter your choice: "))
                if category_choice == len(self.vocabulary['categories']) + 1:
                    return
                
                if 1 <= category_choice <= len(self.vocabulary['categories']):
                    # choose number of questions
                    clear_screen()
                    print("\n🇪🇸  QUIZ SETUP  🇪🇸\n")

                    category = self.vocabulary['categories'][category_choice - 1]
                    max_questions = min(10, len(category['words']))

                    print(f"Category: {category['display_name']}")
                    print(f"Maximum questions available: {max_questions}")

                    num_questions = input(f"\nHow many questions would you like? (1-{max_questions}, default: 5): ")
                    num_questions = int(num_questions) if num_questions.isdigit() else 5
                    num_questions = min(max(num_questions, 1), max_questions)

                    # choose quiz direction (Spanish to English or English to Spanish)
                    direction = input("\nTranslation direction:\n1. Spanish to English\n2. English to Spanish\nYour choice (default: 1): ")
                    direction = int(direction) if direction in ['1', '2'] else 1

                    # Filter by difficulty if user wants
                    if 'difficulty' in category['words'][0]:
                        difficulty = input("\nChoose difficulty:\n1. Beginner\n2. Intermediate\n3. Advanced\n4. All levels\nYour choice (default: 4): ")
                        difficulty = int(difficulty) if difficulty in ['1', '2', '3', '4'] else 4
                        
                        difficulty_map = {1: "beginner", 2: "intermediate", 3: "advanced"}
                        if difficulty in difficulty_map:
                            filtered_words = [w for w in category['words'] if w.get('difficulty') == difficulty_map[difficulty]]
                            if filtered_words:
                                category_words = filtered_words
                                max_questions = min(max_questions, len(filtered_words))
                                num_questions = min(num_questions, max_questions)
                            else:
                                print(f"\nNo words found with {difficulty_map[difficulty]} difficulty. Using all words.")
                                category_words = category['words']
                        else:
                            category_words = category['words']
                    else:
                        category_words = category['words']

                    # run the quiz
                    self._run_quiz(category, category_words, num_questions, direction)
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _run_quiz(self, category, category_words, num_questions, direction):
        """
        Run a quiz with the specified parameters
        
        Args:
            category (dict): The category data
            category_words (list): The words to quiz on
            num_questions (int): Number of questions
            direction (int): 1 for Spanish->English, 2 for English->Spanish
        """
        words = random.sample(category_words, num_questions)
        score = 0
        word_results = []  # Track individual word results

        for i, word in enumerate(words, 1):
            clear_screen()
            print(f"\n🇪🇸 QUESTION {i}/{num_questions} 🇪🇸\n")

            # Display mastery level if a user profile is loaded
            if self.user_profile and self.user_profile.current_profile:
                mastery = self.user_profile.get_mastery_level(word['spanish'], category['name'])
                mastery_display = "★" * mastery + "☆" * (5 - mastery)
                print(f"Mastery: {mastery_display}\n")

            # create multiple choice options (1 correct, 3 incorrect)
            if direction == 1:  # Spanish to English
                question = word['spanish']
                correct_answer = word['english']
                question_prompt = "What is the English translation of this Spanish word?"
            else:   # English to Spanish
                question = word['english']
                correct_answer = word['spanish']
                question_prompt = "What is the Spanish translation of this English word?"

            # get incorrect options from other words
            incorrect_options = []
            other_words = [w for w in category['words'] if w != word]

            if len(other_words) >= 3:
                random_words = random.sample(other_words, 3)
                for wrong_word in random_words:
                    if direction == 1:  # Spanish to English
                        incorrect_options.append(wrong_word['english'])
                    else:   # English to Spanish
                        incorrect_options.append(wrong_word['spanish'])
            else:
                # if not enough words in this category, use placeholders
                for _ in range(3 - len(incorrect_options)):
                    if direction == 1:  # Use placeholder English words
                        placeholders = ["apple", "house", "car", "book", "tree", "dog", "cat"]
                        incorrect_options.append(random.choice(placeholders))
                    else:   # Use placeholder Spanish words
                        placeholders = ["manzana", "casa", "coche", "libro", "árbol", "perro", "gato"]
                        incorrect_options.append(random.choice(placeholders))

            # create answer choices
            all_options = [correct_answer] + incorrect_options
            random.shuffle(all_options)
            correct_index = all_options.index(correct_answer)

            # display question
            print(f"{question_prompt}\n")
            print(f"Word: {question}\n")

            for j, option in enumerate(all_options, 1):
                print(f"{j}. {option}")

            # get user answer
            while True:
                try:
                    user_answer = int(input("\nYour answer (1-4): "))
                    if 1 <= user_answer <= 4:
                        break
                    print("Please enter a number between 1 and 4.")
                except ValueError:
                    print("Please enter a number.")

            # check answer
            is_correct = (user_answer - 1 == correct_index)
            if is_correct:
                print("\n✓ Correct! ¡Muy bien!")
                score += 1
            else:
                print(f"\n✗ Incorrect. The correct answer is: {correct_answer}")

            # Track results for this word
            word_results.append({
                "word": word['spanish'],
                "is_correct": is_correct
            })

            # if there's an example, show it
            if 'example' in word:
                print(f"\nExample: {word['example']}")
                print(f"\nTranslation: {word['example_translation']}")

            # Show pronunciation tip if available
            if 'pronunciation_tip' in word:
                print(f"\nPronunciation tip: {word['pronunciation_tip']}")

            input("\nPress Enter to continue...")

        # show final score
        clear_screen()
        print("\n🇪🇸  QUIZ RESULTS  🇪🇸\n")
        print(f"Your score: {score}/{num_questions} ({int(score/num_questions*100)}%)")

        if score == num_questions:
            print("\n¡Perfecto! You got all questions right!")
        elif score >= num_questions * 0.8:
            print("\n¡Muy bien! Great job!")
        elif score >= num_questions * 0.6:
            print("\n¡Bien! Good effort!")
        else:
            print("\nKeep practicing! You'll improve with time.")
        
        # Save quiz results to user profile if available
        if self.user_profile and self.user_profile.current_profile:
            self.user_profile.update_quiz_score(category['name'], score, num_questions)
            
            # Update word mastery for each word
            for result in word_results:
                self.user_profile.update_word_mastery(result['word'], category['name'], result['is_correct'])
            
            print("\nYour progress has been saved!")
        
        input("\nPress Enter to return to the Quiz menu...")