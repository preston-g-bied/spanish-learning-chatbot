"""
Spanish Learning Chatbot - Quiz System
This module handles the quiz functionality of the chatbot
"""

import random
import time
from src.utils import clear_screen

class QuizSystem:
    """Handles quiz creation and scoring for vocabulary practice"""

    def __init__(self, vocabulary_data):
        """Initialize with vocabulary data"""
        self.vocabulary = vocabulary_data

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

                    # run the quiz
                    self._run_quiz(category, num_questions, direction)
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nPlease enter a number.")
                time.sleep(1)

    def _run_quiz(self, category, num_questions, direction):
        """Run a quiz with the specified parameters"""
        words = random.sample(category['words'], num_questions)
        score = 0

        for i, word in enumerate(words, 1):
            clear_screen()
            print(f"\n🇪🇸 QUESTION {i}/{num_questions} 🇪🇸\n")

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
            if user_answer - 1 == correct_index:
                print("\n✓ Correct! ¡Muy bien!")
                score += 1
            else:
                print(f"\n✗ Incorrect. The correct answer is: {correct_answer}")

            # if there's an example, show it
            if 'example' in word:
                print(f"\nExample: {word['example']}")
                print(f"\nTranslation: {word['example_translation']}")

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
        
        input("\nPress Enter to return to the Quiz menu...")